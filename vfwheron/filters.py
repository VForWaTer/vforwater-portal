import django_filters
from vfwheron.models import Entries, NmPersonsEntries


#
# class VariableFilter(django_filters.FilterSet):
#     name = django_filters.CharFilter(method='my_custom_filter')
#     # name = django_filters.CharFilter(lookup_expr='iexact')
#     print('name: ', name)
#
#     class Meta:
#         print('+++++')
#         model = Entries
#         fields = ['variable_name', 'created_on']
#
#     def my_custom_filter(self, queryset, name, value):
#         print('self: ', self)
#         print('queryset: ', queryset)
#         print('name: ', name)
#         print('value: ', value)
#         return queryset.filter(**{
#             name: value,
#         })

class VariableFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Entries
        fields = ['title', 'abstract']


class NMPersonsFilter(django_filters.FilterSet):
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
