from django.contrib.gis import admin
from django.forms import ModelForm

from vfwheron import models


# Register your models here.

class TblMetaAdminForm(ModelForm):
    class Meta:
        model = models.TblMeta
        fields = ['ts_start', 'ts_stop', 'external_id', 'creator', 'publisher', 'geometry', 'license', 'quality', 'site', 'soil', 'variable', 'sensor', 'source', 'comment', 'created_on', 'updated_on']


class TblMetaAdmin(admin.OSMGeoAdmin):
    form = TblMetaAdminForm
    list_display = ['id', 'variable_fname', 'creator_last_name']


    def variable_fname(self, obj):
        return obj.variable.variable_name


    variable_fname.admin_order_field = 'variable'
    variable_fname.short_description = 'Variable Name'


    def creator_last_name(self, obj):
        return obj.creator.last_name


    creator_last_name.short_description = 'creator Name'


admin.site.register(models.TblMeta, TblMetaAdmin)


class TblVariableAdminForm(ModelForm):
    class Meta:
        model = models.TblVariable
        fields = ['variable_name', 'variable_abbrev', 'unit', 'variable_symbol']


class TblVariableAdmin(admin.ModelAdmin):
    form = TblVariableAdminForm
    list_display = ['variable_name', 'variable_abbrev']


admin.site.register(models.TblVariable, TblVariableAdmin)


class LtLicenseAdminForm(ModelForm):
    class Meta:
        model = models.LtLicense
        fields = ['license_abbrev', 'license_name', 'legal_text', 'text_url', 'access', 'share', 'edit', 'commercial']


class LtLicenseAdmin(admin.ModelAdmin):
    form = LtLicenseAdminForm
    list_display = ['license_abbrev', 'license_name']


admin.site.register(models.LtLicense, LtLicenseAdmin)


class LtUserAdminForm(ModelForm):
    class Meta:
        model = models.LtUser
        fields = ['first_name', 'last_name', 'institution_name', 'email', 'department']


class LtUserAdmin(admin.ModelAdmin):
    form = LtUserAdminForm
    search_fields = ['first_name', 'last_name']
    list_display = ['first_name', 'last_name', 'institution_name']
    list_filter = ['last_name']


admin.site.register(models.LtUser, LtUserAdmin)
