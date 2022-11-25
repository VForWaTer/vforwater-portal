"""
The filter doesn't have to care about users, as all metadata is supposed to be accessible to all users.
"""

import django_filters

from vfw_home.models import NmPersonsEntries


class org_NMPersonsFilter(django_filters.FilterSet):
    embargo = django_filters.AllValuesFilter(field_name='entry__title', lookup_expr='icontains')
    first_name = django_filters.AllValuesFilter(field_name='person__first_name', lookup_expr='icontains')
    last_name = django_filters.AllValuesFilter(field_name='person__last_name', lookup_expr='icontains')
    variable_name = django_filters.AllValuesFilter(field_name='entry__variable__name', lookup_expr='icontains')
    variable_unit = django_filters.AllValuesFilter(field_name='entry__variable__unit__name', lookup_expr='icontains')
    publication_year_from = django_filters.DateTimeFilter(field_name='entry__publication', lookup_expr='gte')
    publication_year_to = django_filters.DateTimeFilter(field_name='entry__publication', lookup_expr='lte')

    class Meta:
        model = NmPersonsEntries
        fields = {

from django.db.models import Q
from django.utils import timezone
from django import forms

class NMPersonsFilter(django_filters.FilterSet):

    variables = django_filters.AllValuesFilter(field_name='variable__name', lookup_expr='icontains')
    institution = django_filters.AllValuesFilter(field_name='nmpersonsentries__person__organisation_name', lookup_expr='icontains')

    def filter_q(self, qs):
        return qs.filter(Q(embargo=False) | Q(embargo_end__lt=timezone.now()))
