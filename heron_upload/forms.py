from django import forms

# To upload the file to a model check the django documentation
# https://docs.djangoproject.com/en/1.11/topics/http/file-uploads/
# 
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
