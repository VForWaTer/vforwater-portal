from django.db import models


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
