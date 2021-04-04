from django.contrib.gis import admin
from django.forms import ModelForm

from vfwheron import models
# The Admin.py is used to create fields in the django admin web page

# Register your models here.

class EntriesAdminForm(ModelForm):
    class Meta:
        model = models.Entries
        fields = ['title', 'abstract', 'external_id', 'location', 'geom', 'version', 'latest_version', 'comment',
                  'license', 'variable', 'datasource', 'embargo', 'embargo_end', 'publication', 'lastupdate',
                  'is_partial', 'uuid', 'citation']


class EntriesAdmin(admin.OSMGeoAdmin):
    form = EntriesAdminForm
    list_display = ['id', 'title', 'abstract']


    def variable_fname(self, obj):
        return obj.variable.variable_name


    variable_fname.admin_order_field = 'title'
    variable_fname.short_description = 'Titel'


    def creator_last_name(self, obj):
        return obj.creator.last_name


    creator_last_name.short_description = 'creator Name'


admin.site.register(models.Entries, EntriesAdmin)
# admin.site.register(models.Entries, admin.GeoModelAdmin)


class VariablesAdminForm(ModelForm):
    class Meta:
        model = models.Variables
        fields = ['name', 'keyword', 'unit', 'symbol']


class VariablesAdmin(admin.ModelAdmin):
    form = VariablesAdminForm
    list_display = ['name', 'unit']


admin.site.register(models.Variables, VariablesAdmin)


class LicensesAdminForm(ModelForm):
    class Meta:
        model = models.Licenses
        fields = ['short_title', 'title', 'summary', 'full_text', 'link', 'by_attribution', 'share_alike',
                  'commercial_use']


class LicensesAdmin(admin.ModelAdmin):
    form = LicensesAdminForm
    list_display = ['short_title', 'title']


admin.site.register(models.Licenses, LicensesAdmin)


class PersonsAdminForm(ModelForm):
    class Meta:
        model = models.Persons
        fields = ['first_name', 'last_name', 'affiliation', 'organisation_name', 'attribution']


class PersonsAdmin(admin.ModelAdmin):
    form = PersonsAdminForm
    search_fields = ['first_name', 'last_name']
    list_display = ['first_name', 'last_name', 'affiliation']
    list_filter = ['last_name']


admin.site.register(models.Persons, PersonsAdmin)
