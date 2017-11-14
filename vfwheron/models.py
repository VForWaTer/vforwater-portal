# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.contrib.gis.db import models

class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class LtDomain(models.Model):
    pid = models.ForeignKey('self', models.DO_NOTHING, db_column='pid', blank=True, null=True)
    domain_name = models.CharField(max_length=65)
    project = models.ForeignKey('LtProject', models.DO_NOTHING, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    column_dict = {'domain_name': 'Domänenname', 'project__project_name': 'Projekt'}
    menu_name = 'Domäne'
    path = 'domain'

    def __str__(self):
        return self.domain_name

    class Meta:
        managed = False
        db_table = 'lt_domain'


class LtLicense(models.Model):
    license_abbrev = models.CharField(max_length=20)
    license_name = models.CharField(max_length=255)
    legal_text = models.TextField(blank=True, null=True)
    text_url = models.CharField(max_length=255, blank=True, null=True)
    access = models.BooleanField()
    share = models.BooleanField()
    edit = models.BooleanField()
    commercial = models.BooleanField()
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    column_dict = {'license_name': 'Lizenzname', 'commercial': 'Kommerziell'}
    menu_name = 'Lizenz'
    path = 'meta__license'

    def __str__(self):
        return self.license_name

    class Meta:
        managed = False
        db_table = 'lt_license'


class LtLocation(models.Model):
    centroid_x = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    centroid_y = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    srid = models.ForeignKey('SpatialRefSys', models.DO_NOTHING, db_column='srid', blank=True, null=True)
    geometry_type = models.CharField(max_length=15, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    geom = models.GeometryField(unique=True, srid=0)

    def __str__(self):
        # return '%s %s' % (self.centroid_x, self.centroid_y)
        return '{"type": %s , "coordinates": [%s %s], "srid": %s}' % (self.geometry_type, self.centroid_x, self.centroid_y, self.srid )

    class Meta:
        managed = False
        db_table = 'lt_location'
        
        
class LtProject(models.Model):
    project_name = models.CharField(unique=True, max_length=65)
    user = models.ForeignKey('LtUser', models.DO_NOTHING, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.project_name

    class Meta:
        managed = False
        db_table = 'lt_project'


class LtQuality(models.Model):
    flag_name = models.CharField(max_length=25)
    flag_weight = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.flag_name

    class Meta:
        managed = False
        db_table = 'lt_quality'


class LtSite(models.Model):
    site_name = models.CharField(max_length=65, blank=True, null=True)
    elevation = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    rel_height = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    orientation_degree = models.IntegerField(blank=True, null=True)
    slope = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    landuse = models.CharField(max_length=65, blank=True, null=True)
    site_comment = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    column_dict = {'site_name': 'Standortname', 'elevation': 'Höhe NN', 'landuse': 'Landnutzung', 'site_comment': 'Kommentar'}
    menu_name = 'Standort'
    path = 'meta__site'

    def __str__(self):
        return self.site_name # TODO: is this useful? At the moment there is no information in site_name 

    class Meta:
        managed = False
        db_table = 'lt_site'


class LtSoil(models.Model):
    geology = models.CharField(max_length=65, blank=True, null=True)
    soil_type = models.CharField(max_length=65, blank=True, null=True)
    porosity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    field_capacity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    residual_moisture = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    column_dict = {'geology': 'Geologie', 'soil_type': 'Bodentyp', 'porosity': 'Porosität', 'residual_moisture': 'Restfeuchte'}
    menu_name = 'Boden'
    path = 'meta__soil'

    def __str__(self):
        return self.geology # TODO: at the moment only values in geology and nothing in soil_type. Check if geology is always filled

    class Meta:
        managed = False
        db_table = 'lt_soil'


class LtSourceType(models.Model):
    type_name = models.CharField(unique=True, max_length=65)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.type_name
    
    class Meta:
        managed = False
        db_table = 'lt_source_type'


class LtUnit(models.Model):
    unit_name = models.CharField(unique=True, max_length=65)
    unit_abbrev = models.CharField(max_length=15)
    unit_symbol = models.CharField(max_length=5)
    derived_si = models.NullBooleanField()
    to_derived_si = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    column_dict = {'unit_name': 'Einheit'}

    def __str__(self):
        return self.unit_name
    
    class Meta:
        managed = False
        db_table = 'lt_unit'


class LtUser(models.Model):
    is_institution = models.BooleanField()
    first_name = models.CharField(max_length=65, blank=True, null=True)
    last_name = models.CharField(max_length=65, blank=True, null=True)
    institution_name = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    column_dict = {'first_name': 'Vorname', 'last_name': 'Nachname', 'institution_name': 'Institut', 'department': 'Abteilung'}
    menu_name = 'Besitzer bzw Ersteller'
    path = 'meta__creator'

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        managed = False
        db_table = 'lt_user'


class NmMetaDomain(models.Model):
    meta = models.ForeignKey('TblMeta', models.DO_NOTHING, blank=True, null=True)
    domain = models.ForeignKey(LtDomain, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nm_meta_domain'


class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=255, blank=True, null=True)
    auth_srid = models.IntegerField(blank=True, null=True)
    srtext = models.TextField(blank=True, null=True)
    proj4text = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return '%s %s' % (self.auth_name, self.auth_srid)
  
    class Meta:
        managed = False
        db_table = 'spatial_ref_sys'


class TblData(models.Model):
    tstamp = models.DateTimeField()
    meta = models.ForeignKey('TblMeta', models.DO_NOTHING)
    value = models.DecimalField(max_digits=65535, decimal_places=65535)

    def __str__(self):
        return self.value # TODO: is that okay?

    class Meta:
        managed = False
        db_table = 'tbl_data'
        unique_together = (('tstamp', 'meta'),)


class TblDataSource(models.Model):
    source_type = models.ForeignKey(LtSourceType, models.DO_NOTHING, blank=True, null=True)
    source_path = models.TextField()
    settings = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.source_path

    class Meta:
        managed = False
        db_table = 'tbl_data_source'


class TblMeta(models.Model):
    ts_start = models.DateTimeField(blank=True, null=True)
    ts_stop = models.DateTimeField(blank=True, null=True)
    external_id = models.CharField(max_length=255, blank=True, null=True)
    support = models.CharField(max_length=255, blank=True, null=True)
    spacing = models.CharField(max_length=255, blank=True, null=True)
    creator = models.ForeignKey(LtUser, models.DO_NOTHING, blank=True, null=True, related_name='creator')
    publisher = models.ForeignKey(LtUser, models.DO_NOTHING, blank=True, null=True, related_name='Publisher')
    geometry = models.ForeignKey(LtLocation, models.DO_NOTHING, blank=True, null=True)
    license = models.ForeignKey(LtLicense, models.DO_NOTHING, blank=True, null=True)
    quality = models.ForeignKey(LtQuality, models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey(LtSite, models.DO_NOTHING, blank=True, null=True)
    soil = models.ForeignKey(LtSoil, models.DO_NOTHING, blank=True, null=True)
    variable = models.ForeignKey('TblVariable', models.DO_NOTHING, blank=True, null=True)
    sensor = models.ForeignKey('TblSensor', models.DO_NOTHING, blank=True, null=True)
    source = models.ForeignKey(TblDataSource, models.DO_NOTHING, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    column_dict = {'ts_start': 'Messbeginn', 'ts_stop': 'Messende', 'support': 'Support???', 'spacing': 'Schrittweite', 'comment': 'Kommentar'}
    menu_name = 'Messung'
    path = 'meta'

    # def __str__(self):
    #     return 'ID %s, %s' % (self.external_id, self.comment)
    
    class Meta:
        managed = False
        db_table = 'tbl_meta'


class TblSensor(models.Model):
    sensor_name = models.CharField(max_length=65, blank=True, null=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    documentation_url = models.TextField(blank=True, null=True)
    last_configured = models.DateTimeField(blank=True, null=True)
    valid_until = models.DateTimeField(blank=True, null=True)
    sensor_comment = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    column_dict = {'sensor_name': 'Name', 'manufacturer': 'Hersteller', 'sensor_comment': 'Kommentar'}
    menu_name = 'Sensor'
    path = 'meta__sensor'

    def __str__(self):
        return self.sensor_name

    class Meta:
        managed = False
        db_table = 'tbl_sensor'


class TblVariable(models.Model):

    variable_name = models.CharField(unique=True, max_length=65)
    variable_abbrev = models.CharField(max_length=15)
    variable_symbol = models.CharField(max_length=5)
    unit = models.ForeignKey(LtUnit, models.DO_NOTHING)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    column_dict = {'variable_name': 'Variablenname'}
    menu_name = 'Datentyp'
    path = 'meta__variable'

    def __str__(self):
        return self.variable_name

    class Meta:
        managed = False
        db_table = 'tbl_variable'



# TODO: There is no need to have this as models.Manager. Find a better place for class
class FilterMenu(models.Manager):
    # Define here which tables to use; which columns are used is defined in the respective table
    menu_tables = [LtDomain, LtLicense, LtSite, LtSoil, LtUser, TblMeta, TblSensor, TblVariable]

    def get_menu(detail_of_menu):
        general_struct = []

        for menu in FilterMenu.menu_tables:  # LtSoil,...
            sub_struct = {}
            for key, value in menu.column_dict.items():   # key: geology value: Geologie ...
                query_set = menu.objects.select_related().values_list(key, flat=True).distinct()  # marls, schist, ...
                if len(query_set) >= 1 and query_set[0] is not None:
        # TODO: some query_sets give numbers --> other menu (from ... to ... instead of tick selection)
                    if detail_of_menu == 'submenu':
                        sub_struct.update({value: {'No Values': 0}})
                    elif detail_of_menu == 'complete_menu':
                        sub_struct.update({value: {str(key): False for key in query_set}})
            if sub_struct:
                general_struct.append({menu.menu_name: sub_struct})
        return general_struct

    # TODO: Can this be integrated in get_menu ? Might become confusing...
    def tick_submenu(top_menu_value, selection):
        selection = {}

        for top_level_dict in FilterMenu.get_menu('complete_menu'):  # complete top_level_dict in function object
            for top_key in top_level_dict:  # all top_level names (top_key = Boden, Besitzer...)
                if top_key == top_menu_value:  # check which menu has been clicked / Boden, Besitzer...
                    for sub_key in top_level_dict[top_key]:  # all sub_level_names (sub_key = Geologie, Bodentyp...)
                        selection[sub_key] = dict(top_level_dict[top_key][sub_key])  # all values to choose from / Boolean if chosen
                        # set checked keys as True:
                        if selection:
                            for get_key, get_value in selection[sub_key].items():
                                if get_key in selection:
                                    selection[sub_key][get_key] = True;
        return selection

    def build_query(cache_obj):
        m_map = {}
        for menu in FilterMenu.menu_tables:
            m_map.update({menu.menu_name: {value: key for key, value in menu.column_dict.items()}})

        filter_list = ''
        for m_key in FilterMenu.menu_tables:
            if m_key.menu_name in cache_obj:
                for cache_key, cache_value in cache_obj.get(m_key.menu_name).items():  # e.g. Geologie: Sandstone
                    filter_aswellas = m_key.path + "__" + m_map[m_key.menu_name][cache_key]  # e.g. soil +__+ geology
                    for value in cache_value:
                        filter_list = filter_list + ".filter(" + filter_aswellas + "='" + value + "')"
                django_data = eval("NmMetaDomain.objects" + filter_list + ".values('meta_id')")

        return {'results': len(django_data)}


# build BW watershed table
class Basiseinzugsgebiet(models.Model):
    # Regular Django fields corresponding to the attributes in the Basiseinzugsgebiet shapefile.
    langname = models.CharField(max_length=100)
    area = models.FloatField()
    objectid = models.BigIntegerField()
    object_id = models.FloatField()
    fg_id = models.BigIntegerField()
    fgkz_nr = models.FloatField('flussgebietskennzahl')
    einzugsgeb = models.IntegerField('einzugsgebietsordnung') # Einzugsgebiets Ordnung – eines Flusses, Baches
    einzugsg00 = models.CharField('einzugsgebietsordnung in Worten', max_length = 80) # Quellgebiet – oberstes Teilgebiet eines Flusses, Baches / Zwischengebiet – Teilgebiet eines Flusses, Baches; wird begrenzt von 2 Hauptzuflüssen / Mündungsgebiet – unterstes Teilgebiet eines Flusses, Baches
    einzugsg01 = models.CharField( max_length = 1) 
    einzugsg02 = models.CharField( max_length = 26) 
    vor_fgkz_n = models.FloatField('flussgebietskennzahl des vorfluters')
    vor_fg_id = models.FloatField()
    vor_fg_lan = models.CharField('vorfluter_langname', max_length = 100)
    wasserkoer = models.CharField('wasserkoerper_code', max_length = 10)
    wasserko00 = models.CharField('wasserkoerper_name', max_length = 85)
    aenderungs = models.CharField( max_length= 20)
    aenderun00 = models.CharField( max_length= 20)
    length = models.FloatField()
    mod_by = models.CharField(max_length= 32)
    last_mod = models.CharField(max_length= 20)
    se_anno_ca = models.CharField(max_length = 254)
    wasserko01 = models.BigIntegerField()
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField(srid=31467)

    # Returns the string representation of the model.
    def __str__(self):              # __unicode__ on Python 2
        return self.langname


