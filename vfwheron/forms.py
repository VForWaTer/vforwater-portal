from django import forms


class AdvancedFilterForm(forms.Form):

    # title = forms.ModelChoiceField(queryset=Entries.objects.values_list('title', flat=True)
    #                                .order_by('title').distinct('title'))
    # abstract = forms.ModelChoiceField(queryset=Entries.objects.values_list('abstract', flat=True)
    #                                   .order_by('abstract').distinct('abstract'))
    # license = forms.ModelChoiceField(queryset=Entries.objects.values_list('license__title', flat=True)
    #                                  .order_by('license__title').distinct('license__title'))
    # comment = forms.ModelChoiceField(queryset=Entries.objects.values_list('comment', flat=True)
    #                                  .order_by('comment').distinct('comment'))
    # variable = forms.ModelChoiceField(queryset=Entries.objects.values_list('variable__name', flat=True)
    #                                   .order_by('variable__name').distinct('variable__name'))
    # datasource = forms.ModelChoiceField(queryset=Entries.objects.values_list('datasource__datatype__name', flat=True)
    #                                     .order_by('datasource__datatype__name').distinct('datasource__datatype__name'))
    # embargo = forms.BooleanField()
    # citation = forms.ModelChoiceField(queryset=Entries.objects.values_list('citation', flat=True)
    #                                   .order_by('citation').distinct('citation'))
    persons = forms.ModelChoiceField(queryset=NmPersonsEntries.objects.values_list('person__last_name', flat=True)
                                     .order_by('person__last_name').distinct('person__last_name'))
    keywords = forms.ModelChoiceField(queryset=NmKeywordsEntries.objects.values_list('keyword__keywords', flat=True)
                                      .order_by('keyword__keywords').distinct('keyword__keywords'))
    details = forms.ModelChoiceField(queryset=Details.objects.values_list('key', 'value')
                                     .order_by('value').distinct('value'))
    projects = forms.ModelChoiceField(queryset=EntrygroupTypes.objects.values_list('name', 'id')
                                      .order_by('name').distinct('name'))
    versions = forms.ModelChoiceField(queryset=Entries.objects.values_list('version', flat=True)
                                      .order_by('version').distinct('version'))

    source = forms.CharField(  # A hidden input for internal use
        max_length=50,  # tell from which page the user sent the message
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super(AdvancedFilterForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')

