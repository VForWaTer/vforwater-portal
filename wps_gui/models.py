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
