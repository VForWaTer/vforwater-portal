import django_filters
from vfwheron.models import Details, NmPersonsEntries, NmEntrygroups, NmKeywordsEntries


# class for person and person role
class PersonsFilter(django_filters.FilterSet):
    class Meta:
        model = NmPersonsEntries
        fields = '__all__'
        # fields = {'relationship_type': ['icontains', ],
        #           'person': ['icontains', ]
        #           }


# class for thesaurus, entries [licenses, variables [keywords],
# datasource {datasource_type, temporal_scales, spatial_scales, datatypes}]
class DetailsFilter(django_filters.FilterSet):
    class Meta:
        model = Details
        fields = '__all__'
        # fields = {'thesaurus': ['icontains', ],
        #           'entries__licenses': ['icontains', ],
        #           'entries__datasources__datatypes': ['icontains', ],
        #           'entries__datasources__spatial_scales': ['icontains', ],  # from data?
        #           'entries__datasources__temporal_scales': ['icontains', ],  # from data?
        #           'entries__variables': ['icontains', ],
        #           'entries__keywords': ['icontains', ]
        #           }


class EntryGroupsFilter(django_filters.FilterSet):
    class Meta:
        model = NmEntrygroups
        fields = '__all__'
        # fields = {'entrygroups': ['icontains', ],
        #           'entrygroups__entrygroup_types': ['icontains', ]
        #           }


# keywords filled through details
class KeyWordsFilter(django_filters.FilterSet):
    class Meta:
        model = NmKeywordsEntries
        fields = '__all__'

