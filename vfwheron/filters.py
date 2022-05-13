"""
The filter doesn't have to care about users, as all metadata is supposed to be accessible to all users.
"""

import django_filters

from vfwheron.models import NmPersonsEntries


# class NMPersonsFilter(django_filters.FilterSet):
class org_NMPersonsFilter(django_filters.FilterSet):
    # first_name = django_filters.ChoiceFilter(field_name='person__last_name', lookup_expr='icontains')
    # first_name = django_filters.TypedChoiceFilter(field_name='person__last_name', lookup_expr='icontains')
    embargo = django_filters.AllValuesFilter(field_name='entry__title', lookup_expr='icontains')
    first_name = django_filters.AllValuesFilter(field_name='person__first_name', lookup_expr='icontains')
    last_name = django_filters.AllValuesFilter(field_name='person__last_name', lookup_expr='icontains')
    variable_name = django_filters.AllValuesFilter(field_name='entry__variable__name', lookup_expr='icontains')
    variable_unit = django_filters.AllValuesFilter(field_name='entry__variable__unit__name', lookup_expr='icontains')
    publication_year_from = django_filters.DateTimeFilter(field_name='entry__publication', lookup_expr='gte')
    publication_year_to = django_filters.DateTimeFilter(field_name='entry__publication', lookup_expr='lte')

    class Meta:
        model = NmPersonsEntries
        # fields = '__all__'
        # fields = {
        #     'Person': ['exact', ],
        #     'Entry': ['icontains', ],
        # }
        # options for lookup_expr: icontains
        fields = {
            # 'person__first_name': ['icontains', ],
                  'entry__abstract': ['icontains', ],
                  # 'entry__title': ['icontains', ],
                  'entry__embargo': ['icontains', ],
                  }
                  # 'entry__publication': ['date__gt', ],}
        # fields = ['person__first_name', 'entry__title']
        # fields = ['person__first_name', 'person__last_name']

from django.db.models import Q
from django.utils import timezone
from django import forms

class NMPersonsFilter(django_filters.FilterSet):

    variables = django_filters.AllValuesFilter(field_name='variable__name', lookup_expr='icontains')
    # start_date = DateTimeFilter(name='datasource__temporal_scale__observation_start', lookup_type=('gt'),)
    # end_date = DateTimeFilter(name='datasource__temporal_scale__observation_end', lookup_type=('lt'))
    # date_range = DateTimeFromToRangeFilter(name='datasource__temporal_scale__observation_start')
    # fair_data = django_filters.AllValuesFilter(method='filter_q')
    institution = django_filters.AllValuesFilter(field_name='nmpersonsentries__person__organisation_name', lookup_expr='icontains')
    # project = django_filters.\
    #     AllValuesFilter(
    #     field_name='nmentrygroups__group__title',
    #     entries=Entries.objects.filter(nmentrygroups__group__type__name='Project'),
    #     lookup_expr='icontains')

    def filter_q(self, qs):
        return qs.filter(Q(embargo=False) | Q(embargo_end__lt=timezone.now()))

    # class Meta:
    #     model = Entries
        # fields = ['datasource__temporal_scale__observation_starts',]
