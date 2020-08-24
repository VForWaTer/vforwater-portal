from django import forms
from .models import Resource

class AddNewResourceForm(forms.ModelForm):
    """

    """
    class Meta:
        model = Resource
        fields = ("type", "link")
        # fields = ("name", "type", "description", "link")

    def __init__(self, *args, **kwargs):
        """

        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        """
        super(AddNewResourceForm, self).__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs.update({'class': 'new-res-name', 'placeholder': 'max 150 characters'})
        self.fields['type'].widget.attrs.update({'class': 'new-res-type', 'placeholder': 'max 50 characters'})
        # self.fields['description'].widget.attrs.update({'class': 'new-res-description',
        #                                                 'placeholder': 'max 250 characters'})
        self.fields['link'].widget.attrs.update({'class': 'new-res-link'})
