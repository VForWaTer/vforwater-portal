from PIL.PngImagePlugin import _idat
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
        # uses proxy model to extend behavior of  Django built-in user (does not generate an extra table in the
        # database)
        proxy = True


class Maintainer(CustomUser):
    class Meta:
        proxy = True


class Owner(Maintainer):
    class Meta:
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
    metacatalogUser = models.ForeignKey(Persons, models.SET_NULL, blank=True, null=True)
#     resources = models.ManyToManyField(Resource, related_name='profile_resources')

    def __str__(self):
        return '{} <ID={}>'.format(self.user, self.id)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# class UserRole(models.Model):
#     user = models.ManyToManyField(Profile)
#     resource = models.ForeignKey(Resource, models.DO_NOTHING)


def make_association(user_object, person_entry, user_profile):
    """

    :param user_object:
    :param person_entry:
    :param user_profile:
    """
    lookup = dict.fromkeys(['author', 'custodian', 'distributor', 'originator', 'owner', 'pointOfContact',
                            'principalInvestigator', 'resourceProvider', 'editor', 'rightsHolder'], 'owner')
    lookup.update(dict.fromkeys(['processor', 'publisher', 'collaborator'], 'maintainer'))
    lookup.update(dict.fromkeys(['sponsor', 'user', 'coAuthor', 'contributor', 'stakeholder'], 'reader'))

    matching_persons = person_entry.values_list('pk', flat=True)
    for idx, person in enumerate(matching_persons):
        if Profile.objects.filter(metacatalogUser_id=person).exists():
            print('\033[91mAsk user if (s)he is the same as already linked with!\033[0m')
        else:
            # associate user with entry person in profile:
            user_profile.metacatalogUser = person_entry[idx]
            user_profile.save()

    # set roles in author_manage for data of this person and create resources:
    role_list = person_entry.values_list('nmpersonsentries__relationship_type__name', flat=True)
    entry_list = person_entry.values_list('nmpersonsentries__entry_id', flat=True)
    datatype_list = person_entry.values_list('nmpersonsentries__entry__datasource__datatype__name', flat=True)
    for idx, role in enumerate(role_list):
        user_role = lookup[role]
        new_resource = Resource(type=datatype_list[idx], link='/', dataEntry_id=entry_list[idx])
        new_resource.save()
        if user_role == 'owner':
            new_resource.owners.add(user_object.id)
        elif user_role == 'maintainer':
            new_resource.maintainers.add(user_object.id)
        elif user_role == 'reader':
            new_resource.readers.add(user_object.id)
        else:
            print('\033[91mError in author_manage models: Unexpected user role!\033[0m')
        new_resource.save()
    # TODO: Implement something to ask user if (s)he is the user from person_entry!
    #  Test with several users with same name.
    print('\033[91mImplement something to ask user if (s)he is the user from person_entry!\033[0m')

def check_association(sender, user: str, request, **kwargs):
    """
    On first time log in check if there are data entries from a person with name user
    :param sender:
    :param user:
    :param request:
    :param kwargs:
    """
    print('sender: ', type(sender))
    print('sender: ', type(request))
    user_profile = Profile.objects.get(user__username=user)
    if not user_profile.checkedAssociation:
        user_object = User.objects.get(username=user)
        last_name = user_object.last_name
        first_name = user_object.first_name
        if first_name and last_name:
            try:
                person_entry = Persons.objects.filter(first_name=first_name, last_name=last_name)
                make_association(user_object, person_entry, user_profile)
            except:
                # no user to connect with
                print('No user to connect entries with auth in metacatalog.')
                pass
            finally:
                print('profile.checkedAssociation: ', user_profile.checkedAssociation)
                user_profile.checkedAssociation = True
                user_profile.save()
                # print('profile.checkedAssociation2: ', user_profile.checkedAssociation)
        else:
            print('\033[91mYour user needs first and last name to associate user with data.\033[0m')


user_logged_in.connect(check_association)
