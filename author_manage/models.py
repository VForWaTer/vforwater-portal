# from PIL.PngImagePlugin import _idat
from django.conf import settings
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User, AbstractUser
from django.db import models
# from django.contrib.auth.models import User as CustomUser, AbstractUser
# from django.contrib.auth.models import User as Owner
# from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
# from django.core.mail.message import EmailMessage
# import logging
# from django.template.loader import render_to_string
# from django.core.validators import MaxLengthValidator

# from wps_workflow.models import Workflow, Process

# from vfwheron.models import TblMeta
# from pandas.tests.arithmetic.conftest import id_func

from vfwheron.models import Entries, Persons, NmPersonsEntries


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
    # name = models.CharField(max_length=150, default='')
    # description = models.CharField(max_length=250, default='')
    # creationDate = models.DateTimeField(default=datetime.now, blank=True)
    readers = models.ManyToManyField(CustomUser, related_name='reader')
    maintainers = models.ManyToManyField(Maintainer, related_name='maintainer')
    owners = models.ManyToManyField(Owner, related_name='owner')
    link = models.FileField(upload_to='', blank=True, null=True)
    dataEntry = models.ForeignKey(Entries, models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '{}, {}'.format(self.type, self.dataEntry)


class Request(models.Model):
    sender = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
    metacatalogPerson = models.ForeignKey(Persons, models.SET_NULL, blank=True, null=True)
#     resources = models.ManyToManyField(Resource, related_name='profile_resources')

    def __str__(self):
        return '{} <ID={}>'.format(self.user, self.id)


def __assign_data(user_obj, user_profile):
    """

    :param user_obj:
    :param person_obj:
    :param user_profile:
    """
    lookup = dict.fromkeys(['author', 'custodian', 'distributor', 'originator', 'owner', 'pointOfContact',
                            'principalInvestigator', 'resourceProvider', 'editor', 'rightsHolder'], 'owner')
    lookup.update(dict.fromkeys(['processor', 'publisher', 'collaborator'], 'maintainer'))
    lookup.update(dict.fromkeys(['sponsor', 'user', 'coAuthor', 'contributor', 'stakeholder', 'funder',
                                 'mediator'], 'reader'))

    last_name = user_obj.last_name
    first_name = user_obj.first_name

    try:
        person_obj = Persons.objects.filter(first_name=first_name, last_name=last_name)
        matching_persons = person_obj.values_list('pk', flat=True)
        for idx, person in enumerate(matching_persons):
            if Profile.objects.filter(metacatalogPerson_id=person).exists():
                print('\033[91mAsk user if (s)he is the same as already linked with!\033[0m')
            else:
                # associate user with entry person in profile:
                user_profile.metacatalogPerson = person_obj[idx]
                user_profile.save()

        # set roles in author_manage for data of this person and create resources:
        role_list = person_obj.values_list('nmpersonsentries__relationship_type__name', flat=True)
        entry_list = person_obj.values_list('nmpersonsentries__entry_id', flat=True)
        datatype_list = person_obj.values_list('nmpersonsentries__entry__datasource__datatype__name', flat=True)
        for idx, role in enumerate(role_list):
            user_role = lookup[role]
            new_resource, created = Resource.objects.get_or_create(type=datatype_list[idx], link='/',
                                                                   dataEntry_id=entry_list[idx])
            if user_role == 'owner':
                new_resource.owners.add(user_obj.id)
            elif user_role == 'maintainer':
                new_resource.maintainers.add(user_obj.id)
            elif user_role == 'reader':
                new_resource.readers.add(user_obj.id)
            else:
                print('\033[91mError in author_manage models: Unexpected user role!\033[0m')
            new_resource.save()
        # TODO: Implement something to ask user if (s)he is the user from person_obj!
        #  Test with several users with same name.
        print('\033[91mImplement something to ask user if (s)he is the user from person_obj!\033[0m')
    except:
        # no user to connect with
        print('No user to connect entries with auth in metacatalog.')
        pass

    finally:
        user_profile.checkedAssociation = True
        user_profile.save()


def __assign_person(user) -> object:
    user_obj = User.objects.get(username=user)
    last_name = user_obj.last_name
    first_name = user_obj.first_name

    try:
        # try to get a person with the same name as the users name:
        person_obj = Persons.objects.filter(first_name=first_name, last_name=last_name)
        # TODO: what to do when there a several persons with this name?
        user_profile, created = Profile.objects.update_or_create(user=user_obj,
                                                                 defaults={'metacatalogPerson': person_obj},)
        # TODO: what to do with a person without data? Check on every login if there is data, or do nothing
        #  (in first case checkedAssociation is True, in second case do not fill checkedAssociation).
        #  By not filling checkedAssociation the second case is implemented.
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
            # TODO: implement this! __assign_data()
            __assign_data(user_obj, user_profile)
            pass
        else:  # only user in profile, so assign_person first
            __assign_data(user_obj, user_profile)
            #     print('\033[91mYour user needs first and last name to associate user with data.\033[0m')
    else:  # there is no profile at all for this user
        user_profile = __assign_person(user)
        __assign_data(user_obj, user_profile)


user_logged_in.connect(check_profile)
