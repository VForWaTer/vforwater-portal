import django_filters
from vfw_home.models import Details, NmPersonsEntries, NmEntrygroups, NmKeywordsEntries


# class for person and person role
class PersonsFilter(django_filters.FilterSet):
    class Meta:
        model = NmPersonsEntries
        fields = '__all__'


# class for thesaurus, entries [licenses, variables [keywords],
# datasource {datasource_type, temporal_scales, spatial_scales, datatypes}]
class DetailsFilter(django_filters.FilterSet):
    class Meta:
        model = Details
        fields = '__all__'


class EntryGroupsFilter(django_filters.FilterSet):
    class Meta:
        model = NmEntrygroups
        fields = '__all__'


# keywords filled through details
class KeyWordsFilter(django_filters.FilterSet):
    class Meta:
        model = NmKeywordsEntries
        fields = '__all__'

