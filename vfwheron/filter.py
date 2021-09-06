"""
The filter doesn't have to care about users, as all metadata is supposed to be accessible to all users.
"""

import logging
from django.db.models import Q
from django.utils import timezone
from vfwheron.models import Entries

logger = logging.getLogger(__name__)


class Option:

    def __init__(self, name, HTMLtype, items):
        self.name = name
        # TODO: Pass/build here directly the html code
        self.HTMLtype = HTMLtype
        self.items = items


class QuickFilter:

    variables = Option('variables', 'DDLmulti',
                       Entries.objects.values_list('variable__name', flat=True).distinct())
                       # forms.SelectMultiple(attrs={'size': 10, 'title': 'Your name'}))
    fair_data = Option('fair_data', 'bool',
                       Entries.objects.filter(Q(embargo=False) | Q(embargo_end__lt=timezone.now())))
    institution = Option('institution', 'DDL',
                         Entries.objects.values_list('nmpersonsentries__person__organisation_name', flat=True).distinct())


    def items(self):

        variables = Entries.objects.values_list('variable__name', flat=True).distinct()
        observation_min = Entries.objects.values('datasource__temporal_scale__observation_start') \
            .filter(datasource__temporal_scale__observation_start__isnull=False)\
            .earliest('datasource__temporal_scale__observation_start')
        observation_max = Entries.objects.values('datasource__temporal_scale__observation_end') \
            .filter(datasource__temporal_scale__observation_end__isnull=False)\
            .latest('datasource__temporal_scale__observation_end')
        fair_data = Entries.objects.filter(Q(embargo=False) | Q(embargo_end__lt=timezone.now()))
        institution = Entries.objects.values_list('nmpersonsentries__person__organisation_name', flat=True).distinct()
        project = Entries.objects.filter(nmentrygroups__group__type__name='Project')\
            .values_list('nmentrygroups__group__title', flat=True).distinct()
        # user_data = Entries.objects.

        return ''
