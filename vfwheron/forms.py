from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models.aggregates import Count
from django.db.models import Q
from django.utils import timezone

from vfwheron.fields import RangeSliderField, SliderField, DateTimeRangeSliderField, DateRangeSliderField
from vfwheron.models import Entries, NmKeywordsEntries, NmPersonsEntries, Details, EntrygroupTypes


# Filter:
# - Zeitraum
# - hat Daten
# - embargo
# - variable
# - [license (oder besser nach einem der bools in der lizenz)  kann man auch weglassen da embargo das wichtigste abbildet]
#
# advanced Filter auf eigener seite (nicht aktuell)
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


class QuickFilterForm(forms.Form):
    """
    Define the quick filter. ChoiceField renders a dropdown, MultipleChoiceField renders a selectBox
    """

    # collect data for dateRangeSlider
    observation_min = Entries.objects.values_list('datasource__temporal_scale__observation_start') \
        .filter(datasource__temporal_scale__observation_start__isnull=False) \
        .earliest('datasource__temporal_scale__observation_start')[0]
    observation_max = Entries.objects.values_list('datasource__temporal_scale__observation_end') \
        .filter(datasource__temporal_scale__observation_end__isnull=False) \
        .latest('datasource__temporal_scale__observation_end')[0]
    # fair_data = Entries.objects.filter(Q(embargo=False) | Q(embargo_end__lt=timezone.now()))

    # create menu objects
    variables = forms.\
        ModelMultipleChoiceField(widget=forms.SelectMultiple(
        attrs={'onchange': 'change_quickfilter({"variables": $("#id_variables").val()});'}),
        queryset=Entries.objects.values_list('variable__name', flat=True)
            .exclude(variable__name__isnull=True).distinct())
    # time = DateRangeSliderField(label="Date", minimum=observation_min.date(),
    date = DateRangeSliderField(label="Date", minimum=observation_min.date(),
                                maximum=observation_max.date(), step=86400000,
                                # widget=DateRangeSliderFiled(
                                # attrs={'onchange': 'console.log("YEAH!");'}))
                                onchange='change_quickfilter({"date": $("#id_date").val()});')
    is_FAIR = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'onchange': 'change_quickfilter({"is_FAIR": $("#id_is_FAIR").is(":checked")});'}))
    # choices = [(0, 'create new folder'), (1, 'delete'), (2, 'read'), (3, 'unread')]
    # action = forms.ChoiceField(choices=choices,
    #                           widget=forms.Select(attrs={'onchange': 'console.log("YEAH!");'}))

    class More(forms.Form):
        institution = forms.\
            ModelMultipleChoiceField(
            widget=forms.
                SelectMultiple(attrs={'onchange': 'change_quickfilter({"institution": $("#id_institution").val()});'}),
            queryset=Entries.objects.values_list('nmpersonsentries__person__organisation_name', flat=True)
                .exclude(nmpersonsentries__person__organisation_name__isnull=True).distinct())
        project = forms.\
            ModelMultipleChoiceField(widget=forms.SelectMultiple(
            attrs={'onchange': 'change_quickfilter({"project": $("#id_project").val()});'}),
            queryset=Entries.objects
                .filter(nmentrygroups__group__type__name='Project')
                .values_list('nmentrygroups__group__title', flat=True)
                .exclude(nmentrygroups__group__title__isnull=True).distinct())
        my_data = forms.BooleanField(widget=forms.CheckboxInput(
            attrs={'onchange': 'change_quickfilter({"my_data": $("#id_my_data").is(":checked")});'}))

