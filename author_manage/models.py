from django.conf import settings
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from vfw_home.models import Entries, Persons, NmPersonsEntries
import logging


logger = logging.getLogger(__name__)

class CustomUser(User):  # == Reader in Resource
    class Meta:
        ordering = ['id']
        # uses proxy model to extend behavior of  Django built-in user (does not generate an extra table in the
        # database)
        proxy = True


class Maintainer(CustomUser):
    class Meta:
        ordering = ['id']
        proxy = True


class Owner(Maintainer):
    class Meta:
        ordering = ['id']
        proxy = True


# corresponds to the table in the database storing all information about a resource
class Resource(models.Model):
    type = models.CharField(max_length=50, default='')
    readers = models.ManyToManyField(CustomUser, related_name='reader')
    maintainers = models.ManyToManyField(Maintainer, related_name='maintainer')
    owners = models.ManyToManyField(Owner, related_name='owner')
    link = models.FileField(upload_to='', blank=True, null=True)
    dataEntry = models.ForeignKey(Entries, models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '{}, {}'.format(self.type, self.dataEntry)


class Request(models.Model):
    sender = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(default=datetime.now, blank=True)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, default='')
    type = ""

    class Meta:
        ordering = ['id']
        # the Request model must be an abstract class, to put some common information into the AccessRequest and DeletionRequest  model
        # This model will not be used to create any database table
        abstract = True
        unique_together = ('sender', 'resource',)  # This tuple must be unique when considered together

    def __str__(self):
        return '{}, {}'.format(self.sender, self.resource)


# corresponds to the table in the database storing all information about an access request
class AccessRequest(Request):
    type = 'access'


# corresponds to the table in the database storing all information about a deletion request
class DeletionRequest(Request):
    type = 'deletion'


class Profile(models.Model):
    checkedAssociation = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    metacatalogPerson = models.ForeignKey(Persons, models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '{} <ID={}>'.format(self.user, self.id)


def __assign_data(user_obj, user_profile):
    """
    Associate the user with data entries in metacatalog based on matching Persons.
    :param user_obj: User object to be associated.
    :param user_profile: Profile object associated with the User.
    """
    lookup = dict.fromkeys(['author', 'custodian', 'distributor', 'originator', 'owner', 'pointOfContact',
                            'principalInvestigator', 'resourceProvider', 'editor', 'rightsHolder'], 'owner')
    lookup.update(dict.fromkeys(['processor', 'publisher', 'collaborator'], 'maintainer'))
    lookup.update(dict.fromkeys(['sponsor', 'user', 'coAuthor', 'contributor', 'stakeholder', 'funder',
                                 'mediator'], 'reader'))

    last_name = user_obj.last_name
    first_name = user_obj.first_name

    try:
        # Retrieve all matching Person objects
        person_matches = Persons.objects.filter(first_name=first_name, last_name=last_name)
        if person_matches.exists():
            if person_matches.count() > 1:
                # Log a warning when multiple matches are found and choose the first match
                logger.warning(f"Multiple persons found for user '{user_obj}'. Associating with the first match.")
            
            # Use the first matching person by default
            person_obj = person_matches.first()
            
            # Check if this person is already linked with another profile
            if Profile.objects.filter(metacatalogPerson=person_obj).exists():
                logger.warning(f"The person '{person_obj}' is already linked to another profile.")

            # Associate the user profile with this Person
            user_profile.metacatalogPerson = person_obj
            user_profile.save()

            # Set roles in author_manage for data entries of this person
            role_list = person_obj.nmpersonsentries_set.values_list('relationship_type__name', flat=True)
            entry_list = person_obj.nmpersonsentries_set.values_list('entry_id', flat=True)
            datatype_list = person_obj.nmpersonsentries_set.values_list('entry__datasource__datatype__name', flat=True)

            for idx, role in enumerate(role_list):
                user_role = lookup.get(role, 'reader')
                new_resource, created = Resource.objects.get_or_create(
                    type=datatype_list[idx], link='/', dataEntry_id=entry_list[idx]
                )
                # Assign role-based permissions to the user on the resource
                if user_role == 'owner':
                    new_resource.owners.add(user_obj)
                elif user_role == 'maintainer':
                    new_resource.maintainers.add(user_obj)
                else:  # reader by default
                    new_resource.readers.add(user_obj)
                new_resource.save()

        else:
            logger.info(f"No persons found in metacatalog matching user '{user_obj}'.")
    
    except Exception as e:
        logger.error(f"Failed to assign data for user '{user_obj}': {e}")
    
    finally:
        # Mark the profile's association as checked
        user_profile.checkedAssociation = True
        user_profile.save()


def __assign_person(user) -> object:
    user_obj = User.objects.get(username=user)
    last_name = user_obj.last_name
    first_name = user_obj.first_name

    try:
        # try to get a person with the same name as the users name:
        person_obj = Persons.objects.filter(first_name=first_name, last_name=last_name)
        user_profile, created = Profile.objects.update_or_create(user=user_obj,
                                                                 defaults={'metacatalogPerson': person_obj},)
    except:
        # no person to connect with
        user_profile = Profile(user=user_obj)
        user_profile.save()
        print('No user to connect entries with auth in metacatalog.')
    return user_profile


def check_profile(sender, user: str, request, **kwargs):
    """
    On first time log in check if there is a profile and if there are data entries from a person with name user in the
    profile.
    :param sender:
    :param user:
    :param request:
    :param kwargs:
    """
    user_obj = User.objects.get(username=user)
    if Profile.objects.filter(user__username=user).exists():  # if user has a profile
        user_profile = Profile.objects.get(user__username=user)
        if user_profile.checkedAssociation:  # Profile should be filled, so there is nothing to do.
            pass
        elif user_profile.metacatalogPerson_id:  # no Association for data checked, so check if there is data now.
            __assign_data(user_obj, user_profile)
            pass
        else:  # only user in profile, so assign_person first
            __assign_data(user_obj, user_profile)
    else:  # there is no profile at all for this user
        user_profile = __assign_person(user)
        __assign_data(user_obj, user_profile)


user_logged_in.connect(check_profile)
