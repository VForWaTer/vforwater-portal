from datetime import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class WebProcessingService(models.Model):
    """
    ORM for Web Processing Services settings.
    """
    name = models.CharField(max_length=30, unique=True)
    endpoint = models.CharField(max_length=1024)
    username = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Web Processing Service'
        verbose_name_plural = 'Web Processing Services'
        managed = True

    def __str__(self):
        return self.name


class WpsResults(models.Model):
    """
    Store data of creation in case datasets get an update.
    Last access time to be able to remove datasets not used for ages
    """
    creation = models.DateTimeField(blank=True, null=True)
    access = models.DateTimeField(blank=True, null=True)
    open = models.BooleanField()
    outputs = models.CharField(max_length=1024)
    wps = models.CharField(max_length=255)
    inputs = models.CharField(max_length=2048)

    def __str__(self):
        return '%s %s' % (self.wps, self.inputs)

    class Meta:
        managed = True


class WpsDescription(models.Model):
    """
    Store information about wps process to reduce time to open workspace
    """
    service = models.CharField(max_length=30, default='')
    title = models.CharField(max_length=120, unique=True, default='')
    identifier = models.CharField(max_length=120, unique=True, default='')
    abstract = models.CharField(max_length=8192, default='')
    inputs = models.CharField(max_length=2048, default='')  # short description
    outputs = models.CharField(max_length=2048, default='')  # short description

    # extended schema for tools
    verbose = models.BooleanField()
    statusSupported = models.BooleanField(blank=True, default=False)
    storeSupported = models.BooleanField(blank=True, default=False)
    metadata = models.CharField(max_length=2048)
    dataInputs = models.CharField(max_length=4096)  # complete description
    processOutputs = models.CharField(max_length=2048)  # complete description

    lastUpdateDateCheck = models.DateTimeField(default=timezone.now, blank=True)
    version = models.CharField(max_length=8, default='', blank=True, null=True)

    def __str__(self):
        return 'service: %s, title: %s' % (self.service, self.title)

    class Meta:
        managed = True
