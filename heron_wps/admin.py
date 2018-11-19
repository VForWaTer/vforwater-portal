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
