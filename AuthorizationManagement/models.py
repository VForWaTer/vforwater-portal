from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.mail.message import EmailMessage
import logging
from django.template.loader import render_to_string
from django.core.validators import MaxLengthValidator



class CustomUser(User):
    
    class Meta:
        #uses proxy model to extend behavior of  Django built-in user (does not generate an extra table in the database)
        proxy = True
   
class Owner(CustomUser):
    
    class Meta:
        proxy = True
        
# corresponds to the table in the database storing all information about a resource
class Resource(models.Model):
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=250, blank=True,
                                   validators=[MaxLengthValidator(250)])
    creationDate = models.DateTimeField(default=datetime.now, blank=True)
    readers = models.ManyToManyField(CustomUser, related_name= 'reader')
    owners = models.ManyToManyField(Owner, related_name= 'owner')
    link = models.FileField(upload_to='')

    
class Request(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    creationDate = models.DateTimeField(default=datetime.now, blank=True)
    resource = models.ForeignKey(Resource, on_delete = models.CASCADE)
    description = models.CharField(max_length=250, blank=True)
    type=""
    
    class Meta:
        # the Request model must be an abstract class, to put some common information into the AccessRequest and DeletionRequest  model
        #This model will not be used to create any database table
        abstract = True        
        unique_together=('sender','resource',) # This tuple must be unique when considered together


# corresponds to the table in the database storing all information about an access request    
class AccessRequest(Request):
    type = 'access'
# corresponds to the table in the database storing all information about a deletion request    
class DeletionRequest(Request):
    type = 'deletion' 
    