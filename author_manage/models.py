from django.conf import settings
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
from vfwheron.models import Entries
from vfwheron.models import Persons


# class CustomUser(User):
#     class Meta:
#         # uses proxy model to extend behavior of  Django built-in user (does not generate an extra table in the
#         # database)
#         proxy = True


# class Maintainer(CustomUser):
#     class Meta:
#         proxy = True
#
#
# class Owner(CustomUser):
#     class Meta:
#         proxy = True


# corresponds to the table in the database storing all information about a resource
class Resource(models.Model):
    type = models.CharField(max_length=50, default='')
    # name = models.CharField(max_length=150, default='')
    # description = models.CharField(max_length=250, default='')
    # creationDate = models.DateTimeField(default=datetime.now, blank=True)
    # readers = models.ManyToManyField(CustomUser, related_name='reader')
    # owners = models.ManyToManyField(Owner, related_name='owner')
    # maintainers = models.ManyToManyField(Owner, related_name='maintainer')
    link = models.FileField(upload_to='', blank=True, null=True)
    dataEntry = models.ForeignKey(Entries, models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '{}, {}'.format(self.type, self.dataEntry)

class Request(models.Model):
    sender = models.OneToOneField(User, on_delete=models.CASCADE)
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

    # def __str__(self):
    #     user = User.objects.get(pk=self.uid)
    #     return '{} <ID={}>'.format(user, self.uid)


class Profile(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    metacatalog_user = models.ForeignKey(Persons, models.SET_NULL, blank=True, null=True)
    resources = models.ManyToManyField(Resource, related_name='profile_resources')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class UserRole(models.Model):
    user = models.ManyToManyField(Profile)
    resource = models.ForeignKey(Resource, models.DO_NOTHING)

