from django import forms
from .models import Resource

class AddNewResourceForm(forms.ModelForm):
    """

    """
    class Meta:
        model = Resource
        fields = ("type", "link")

    def __init__(self, *args, **kwargs):
        """

        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        """
        super(AddNewResourceForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({'class': 'new-res-type', 'placeholder': 'max 50 characters'})
        self.fields['link'].widget.attrs.update({'class': 'new-res-link'})
