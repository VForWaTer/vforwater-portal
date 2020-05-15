from django.db import models
from django.contrib.auth.models import User as CustomUser
from django.contrib.auth.models import User as Owner
from django.contrib.auth.models import User
from datetime import datetime
# from django.core.mail.message import EmailMessage
import logging
# from django.template.loader import render_to_string
from django.core.validators import MaxLengthValidator

# from wps_workflow.models import Workflow, Process

from vfwheron.models import TblMeta

# class CustomUser(User):
#
#    class Meta:
#      # uses proxy model to extend behavior of Django built-in user (does not generate an extra table in the database)
#        proxy = True

# CustomUser = User

# Owner = CustomUser

# class Owner(CustomUser):
#
#    class Meta:
#        proxy = True


class PostgresReader(models.Model):
    """
    Table that links Users to Data in Postgres DB reader rights
    """
    psql_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)


class PostgresOwner(models.Model):
    """
    Table that links Users to Data in Postgres DB with owner rights
    """
    psql_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)


class Resource(models.Model):
    """
    Corresponds to the table in the database storing all information about a resource
    """
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=250, blank=True,
                                   validators=[MaxLengthValidator(250)])
    creationDate = models.DateTimeField(default=datetime.now, blank=True)
    readers = models.ManyToManyField(User, related_name='reader')
    owners = models.ManyToManyField(User, related_name='owner')
    link = models.FileField(upload_to='', default=' ')


class Request(models.Model):
    """
    Represents the Request table in the Database
    """
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(default=datetime.now, blank=True)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, blank=True)
    type = ""

    class Meta:
        """
        The Request model must be an abstract class, to put some common information into the AccessRequest and DeletionRequest  model
        This model will not be used to create any database table
        """
        abstract = True
        unique_together = ('sender', 'resource',)  # This tuple must be unique when considered together


class AccessRequest(Request):
    """
    Corresponds to the table in the database storing all information about an access request
    """
    type = 'access'


class DeletionRequest(Request):
    """
    Corresponds to the table in the database storing all information about a deletion request
    """
    type = 'deletion'


class MetaMap(models.Model):
    """
    This table acts as the connection between sqlite3 (user) and postgres (TblMeta) DB.
    IDs have to validated seperately
    """
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    mid = models.IntegerField()


class WorkflowOwner(models.Model):
    """
    """
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    wfid = models.IntegerField()  # models.ForeignKey(Workflow, on_delete = models.CASCADE)

class WorkflowShared(models.Model):
    """
    """
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    wfid = models.IntegerField()  # models.ForeignKey(Workflow, on_delete = models.CASCADE)


class ProcessOwner(models.Model):
    """
    """
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    pid = models.IntegerField()  # models.ForeignKey(Process, on_delete = models.CASCADE)


class RequestOwner(models.Model):
    """
    """
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    rid = models.IntegerField()  # models.ForeignKey(Request, on_delete = models.CASCADE)
