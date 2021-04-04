from django import forms
from django.contrib.gis import forms
from django.forms import DateField
# To upload the file to a model check the django documentation
# https://docs.djangoproject.com/en/1.11/topics/http/file-uploads/
#
import datetime

from vfwheron.models import Entries, NmPersonsEntries, Persons


class MultiUploadFileForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'multiple': True,
        'id': 'select_data_button',
        'style': 'display: none',
        'onchange': "this.form.submit()",
        }), label='')


from .models import UploadedFile

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('file', )


class EntriesForm(forms.ModelForm):

    class Meta:
        model = Entries
        fields = ('title', 'embargo_end', 'geom', 'external_id', 'variable', 'version', 'abstract',
                  'comment', 'embargo', 'publication', 'citation', 'license', 'location')
        # widgets = {
        #     'embargo_end': forms.DateField(initial=datetime.date.today),
        #     # 'embargo_end': DateField(attrs={'cols': 80, 'rows': 20}),
        # }
        # fields = '__all__'
        # model = NmPersonsEntries
        # fields = {'entry', 'order', 'person', 'relationship_type'}

class PersonsForm(forms.ModelForm):

    class Meta:
        model = Persons
        fields = ('first_name', 'last_name', 'organisation_name', 'affiliation', 'attribution')


from vfwheron.models import *

# class MetadataForm(forms.Form):
#     name = forms.CharField(max_length=30,
#                            widget=forms.TextInput(
#                                attrs={
#                                    'style': 'border-color: lightblue;',
#                                    'placeholder': 'Write your name here'
#                                }))
#     title = forms.CharField(max_length=254,
#                             widget=forms.TextInput(
#                                 attrs={
#                                     'style': 'border-color: lightblue;',
#                                     'placeholder': 'Extra awesome dataset.'
#                                 }))
#     abstract = forms.CharField(max_length=2000,
#                                widget=forms.Textarea(attrs={
#                                     'style': 'border-color: lightblue;',
#                                     'placeholder': 'Strong wind during measurement add an error of 1m to the position.'
#                                 }),
#                                help_text='You can describe your data here.'
#                                )
#     source = forms.CharField(       # A hidden input for internal use
#         max_length=50,              # tell from which page the user sent the message
#         widget=forms.HiddenInput()
#     )
#
#     def clean(self):
#         cleaned_data = super(MetadataForm, self).clean()
#         name = cleaned_data.get('name')
#         title = cleaned_data.get('title')
#         abstract = cleaned_data.get('abstract')
#         if not name and not title and not abstract:
#             raise forms.ValidationError('Please describe your data!')
#
