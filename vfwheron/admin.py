from django.contrib.gis import admin
from .import models
from django.forms import ModelForm

# Register your models here.

class TblCoreAdminForm(ModelForm):
    class Meta:
        model = models.TblCore
        fields = ['ts_start', 'ts_stop', 'geom', 'variable', 'source', 'license', 'author', 'publisher','srid', 'data_dimension', 'external_id', 'identifier_name', 'comment']
 
class TblCoreAdmin(admin.OSMGeoAdmin):

    form = TblCoreAdminForm
    list_display = ['identifier_name', 'variable_full_name', 'author_last_name']
    
    def variable_full_name(self, obj):
        return obj.variable.full_name
    variable_full_name.admin_order_field = 'variable'
    variable_full_name.short_description = 'Variable Name'
    
    def author_last_name(self, obj):
        return obj.author.last_name
    author_last_name.short_description = 'Author Name'
    
admin.site.register(models.TblCore, TblCoreAdmin)


class TblVariableAdminForm(ModelForm):
    class Meta:
        model = models.TblVariable
        fields = ['full_name', 'abbrev', 'unit', 'symbol']

class TblVariableAdmin(admin.ModelAdmin):

    form = TblVariableAdminForm
    list_display = ['full_name', 'abbrev']

admin.site.register(models.TblVariable, TblVariableAdmin)


class LtLicenseAdminForm(ModelForm):
    class Meta:
        model = models.LtLicense
        fields = ['abbrev', 'full_name', 'license_text', 'license_url', 'access', 'share', 'edit', 'commercial']

class LtLicenseAdmin(admin.ModelAdmin):

    form = LtLicenseAdminForm
    list_display = ['abbrev', 'full_name']
    
admin.site.register(models.LtLicense, LtLicenseAdmin)


class LtAuthorAdminForm(ModelForm):
    class Meta:
        model = models.LtAuthor
        fields = ['first_name', 'last_name', 'institution', 'email', 'url', 'institution_department']

class LtAuthorAdmin(admin.ModelAdmin):

    form = LtAuthorAdminForm
    search_fields = ['first_name', 'last_name']
    list_display = ['first_name', 'last_name', 'institution']
    list_filter = ['last_name']

admin.site.register(models.LtAuthor, LtAuthorAdmin)