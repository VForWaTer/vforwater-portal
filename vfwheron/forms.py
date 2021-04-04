from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models.aggregates import Count

from vfwheron.models import Entries, NmKeywordsEntries, NmPersonsEntries, Details, EntrygroupTypes


# Filter:
# - Zeitraum
# - hat Daten
# - embargo
# - variable
# - [license (oder besser nach einem der bools in der lizenz)  kann man auch weglassen da embargo das wichtigste abbildet]
#
# advanced Filter (auf eigener seite?)
# - nach personen filtern
# - liste 10 (25) häufigsten keywords, die nicht jeder entry hat und nutze die zum filtern
# - list 5 (10) häufigsten Detai.stem und biete jeweils den wert zum filtern an
# - liste alle verwendeten keywords (in extra ansicht? können viele sein)
# - filter nach Projekt
# - finde alle Versionen (checkmark)
# - volltextsuche (sobald ich da ein konzept für metacatalog habe.)

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

    # details = forms.ModelChoiceField(queryset=Details.objects.values_list('key', 'value')
    #                                  .order_by('value').distinct('value'))
    # print('details: ', Details.objects.values('entry_id').distinct())
    # print('original: ', Details.objects.values_list('key', 'value')
    #       .order_by('value').distinct('value'))
    # print('distinct entry: ', Details.objects.values_list('key', 'value')
    #       .order_by('entry_id', 'id'))
    # bla = Details.objects.values('entry_id').distinct()
    # entries = bla.values('key', 'value')
    # print('distinct entry: ', entries)
    # print('len entry: ', len(entries))

    # print('annotate: ', Details.objects.values('entry_id')
    #       .annotate(entries='value'))
    # print('annotate: ', Details.objects.values_list('key', 'value')
    #       .annotate('entry_id'))
    project_type = forms.ModelChoiceField(queryset=EntrygroupTypes.objects.values_list('name', flat=True)
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

# CHOICES = [('1', 'First'), ('2', 'Second')]
# >>> choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
# >>> choice_field.choices
# [('1', 'First'), ('2', 'Second')]
# >>> choice_field.widget.choices
# [('1', 'First'), ('2', 'Second')]
# >>> choice_field.widget.choices = []
# >>> choice_field.choices = [('1', 'First and only')]
# >>> choice_field.widget.choices
# [('1', 'First and only')]
