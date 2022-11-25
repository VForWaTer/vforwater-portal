from django.contrib import admin
from .models import WebProcessingService
from .import models
from django.forms import ModelForm, PasswordInput


class WebProcessingServiceForm(ModelForm):
    class Meta:
        model = WebProcessingService
        fields = ['name', 'endpoint', 'username', 'password']
        widgets = {
            'password': PasswordInput()
        }


class WebProcessingServiceAdmin(admin.ModelAdmin):
    """
    Admin model for Web Processing Service Model
    """
    form = WebProcessingServiceForm
    list_display = ['name', 'endpoint', 'username']


admin.site.register(models.WebProcessingService, WebProcessingServiceAdmin)



class WpsResultsAdmin(admin.ModelAdmin):
    """
    Admin model for Web Processing Service Rsults
    """
    model = WpsResults
    fields = ('wps', 'inputs', 'outputs', 'open', 'creation', 'access')
    list_display = ['wps', 'inputs', 'outputs', 'open', 'creation', 'access']


admin.site.register(models.WpsResults, WpsResultsAdmin)


class WpsDescriptionAdmin(admin.ModelAdmin):
    """
    Admin model for Web Processing Service Rsults
    """
    model = WpsDescription
    fields = ('service', 'title', 'identifier', 'abstract', 'inputs', 'outputs', 'verbose', 'statusSupported',
              'storeSupported', 'metadata', 'dataInputs', 'processOutputs', 'lastUpdateDateCheck', 'version')
    list_display = ['title', 'identifier', 'inputs', 'outputs', 'verbose', 'statusSupported', 'storeSupported',
                    'metadata', 'dataInputs', 'processOutputs', 'lastUpdateDateCheck', 'version', 'service']


admin.site.register(models.WpsDescription, WpsDescriptionAdmin)
