from django.db import models

# Create your models here.
class WebProcessingService(models.Model):
    """
    
    """
    name = models.CharField(max_length=100)
    uri = models.CharField(max_length=250)
