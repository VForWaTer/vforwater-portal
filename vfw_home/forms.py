from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
from django.db.models.aggregates import Count
from django.db.models import Q
from django.utils import timezone

from author_manage.views import MyResourcesView
from vfw_home.fields import DateRangeSliderField
from vfw_home.models import Entries, NmKeywordsEntries, NmPersonsEntries, Details, EntrygroupTypes


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
from vfw_home.widgets import DateRangeSlider


class AdvancedFilterForm(forms.Form):

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


class QuickFilterQuerySets:
    """
    Queries and collection of data for filter menue
    """
    variables_path = 'variable__name'
    date_min_path = 'datasource__temporal_scale__observation_start'
    date_max_path = 'datasource__temporal_scale__observation_end'


    variables_base_qs = Entries.objects.values_list('variable__name', flat=True).order_by('variable__name')
    observation_base_min_qs = Entries.objects.values_list('datasource__temporal_scale__observation_start')
    observation_base_max_qs = Entries.objects.values_list('datasource__temporal_scale__observation_end')
    fair_data_base_qs = Entries.objects.filter(Q(embargo=False) | Q(embargo_end__lt=timezone.now()))
    institution_base_qs = Entries.objects.values_list('nmpersonsentries__person__organisation_name', flat=True)\
        .order_by('nmpersonsentries__person__organisation_name')
    project_base_qs = Entries.objects.filter(nmentrygroups__group__type__name='Project') \
        .values_list('nmentrygroups__group__title', flat=True).order_by('nmentrygroups__group__title')

    variables_qs = variables_base_qs.exclude(variable__name__isnull=True).distinct()
    observation_min_qs = observation_base_min_qs \
        .filter(datasource__temporal_scale__observation_start__isnull=False) \
        .earliest('datasource__temporal_scale__observation_start')[0]
    observation_max_qs = observation_base_max_qs \
        .filter(datasource__temporal_scale__observation_end__isnull=False) \
        .latest('datasource__temporal_scale__observation_end')[0]
    fair_data_qs = fair_data_base_qs
    institution_qs = institution_base_qs.exclude(nmpersonsentries__person__organisation_name__isnull=True).distinct()
    project_qs = project_base_qs \
        .exclude(nmentrygroups__group__title__isnull=True) \
        .values_list('nmentrygroups__group__title', flat=True)\
        .distinct()

class QuickFilterForm(forms.Form):
    """
    Define the quick filter. ChoiceField renders a dropdown, MultipleChoiceField renders a selectBox.
    "onchange" defines the function called on a change/click event and the values send to that function.
    """

    # create menu objects
    variables = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(
        attrs={'onchange': 'get_quick_selection({"variables": $("#id_variables").val()});'}),
        queryset=QuickFilterQuerySets.variables_qs)
    date = DateRangeSliderField(label="Date", minimum=QuickFilterQuerySets.observation_min_qs.date(),
                                maximum=QuickFilterQuerySets.observation_max_qs.date(), step=86400000,
                                # widget=DateRangeSliderFiled(
                                # attrs={'onchange': 'console.log("YEAH!");'}))
                                onchange='get_quick_selection({"date": $("#id_date").data("values")});')
                                # onchange='get_quick_selection({"date": $("#id_date").val()});')
    is_FAIR = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'onchange': 'get_quick_selection({"is_FAIR": [$("#id_is_FAIR").is(":checked")]});'}), initial=True)

    class More(forms.Form):
        institution = forms.ModelMultipleChoiceField(
            widget=forms.
                SelectMultiple(attrs={'onchange': 'get_quick_selection({"institution": $("#id_institution").val()});'}),
            queryset=QuickFilterQuerySets.institution_qs)
        project = forms.\
            ModelMultipleChoiceField(widget=forms.SelectMultiple(
                attrs={'onchange': 'get_quick_selection({"project": $("#id_project").val()});'}),
                queryset=QuickFilterQuerySets.project_qs)
        my_data = forms.BooleanField(widget=forms.CheckboxInput(
            attrs={'onchange': 'get_quick_selection({"my_data": $("#id_my_data").is(":checked")});'}))

