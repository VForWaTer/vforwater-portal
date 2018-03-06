# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.core.cache import cache
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
    # newcolumn_dict = {'domain_name': {'DE': 'Domänenname', 'EN': 'Domain Name'},
    #                'project__project_name': {'DE': 'Projekt', 'EN': 'Project'}}
    newcolumn_dict = {'project__project_name': {'DE': 'Projekt', 'EN': 'Project'}}
    child_column_dict = {'domain_name': {'DE': 'Domänenname', 'EN': 'Domain Name'}}

    menu_name = 'Projekt/Domäne'
    newmenu_name = {'DE': 'Projekt/Domäne', 'EN': 'Project/Domain'}
    submenu_names = {'project': {'DE': 'Projekt', 'EN': 'Project'},
                     'domain': {'DE': 'Domäne', 'EN': 'Domain'},
                     'subdomain': {'DE': 'Subdomäne', 'EN': 'Subdomain'}}
    path = 'domain'
    newpath = 'nmmetadomain__domain'
    # filter_type = {'domain_name': 'recursive'}

    # Recursive exists only in that table, so the build process is highly customized to that one
    filter_type = {'project__project_name': 'recursive'}
    mother = 'LtProject'

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

    column_dict = {'license_abbrev': 'Lizenz', 'commercial': 'Kommerziell'}
    newcolumn_dict = {'license_abbrev': {'DE': 'Lizenzname', 'EN': 'License name'}}
    menu_name = 'Lizenz'
    newmenu_name = {'DE': 'Lizenz', 'EN': 'License'}
    path = 'meta__license'
    newpath = 'license'

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

    column_dict = {'centroid_x': 'X Koordinaten', 'centroid_y': 'Y Koordinaten', 'geometry_type': 'Geometrie'}
    newcolumn_dict = {'centroid_x': {'DE': 'X-Koordinaten', 'EN': 'X-Coordinate'},
                      'centroid_y': {'DE': 'Y Koordinaten', 'EN': 'Y-Coordinate'},
                      'geometry_type': {'DE': 'Geometrie', 'EN': 'Geometry'}}
    menu_name = 'Position'
    newmenu_name = {'DE': 'Position', 'EN': 'Location'}
    path = 'meta__location'
    newpath = 'location'
    filter_type = {'centroid_x': 'slider', 'centroid_y': 'slider'}

    def __str__(self):
        # return '%s %s' % (self.centroid_x, self.centroid_y)
        return '{"type": %s, "coordinates": [%s %s], "srid": %s}' % (
            self.geometry_type, self.centroid_x, self.centroid_y, self.srid)

    class Meta:
        managed = False
        db_table = 'lt_location'


class LtProject(models.Model):
    project_name = models.CharField(unique=True, max_length=65)
    user = models.ForeignKey('LtUser', models.DO_NOTHING, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    menu_name = 'Project & Domain'
    column_dict = {'project_name': 'Projektname'}
    newcolumn_dict = {'project_name': {'DE': 'Projektname', 'EN': 'Project name'}}
    newmenu_name = {'DE': 'Projekt', 'EN': 'project'}
    newpath = 'nmmetadomain__domain__project'

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

    column_dict = {'flag_name': 'Qualität', 'flag_weight': 'Gewichtung'}
    newcolumn_dict = {'flag_name': {'DE': 'Kennzeichen', 'EN': 'Flag'},
                      'flag_weight': {'DE': 'Gewichtung', 'EN': 'Quantifier'}}
    menu_name = 'Qualität'
    newmenu_name = {'DE': 'Qualität', 'EN': 'Quality'}
    path = 'meta__quality'
    newpath = 'quality'

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

    column_dict = {'site_name': 'Standortname', 'elevation': 'Höhe', 'landuse': 'Landnutzung',
                   'site_comment': 'Kommentar'}
    newcolumn_dict = {'site_name': {'DE': 'Standortname', 'EN': 'Site name'},
                      'elevation': {'DE': 'Hohe', 'EN': 'Elevation'},
                      'rel_height': {'DE': 'Relative Höhe', 'EN': 'Relative height'},
                      'orientation_degree': {'DE': 'Richtung', 'EN': 'Orientation'},
                      'slope': {'DE': 'Hangneigung', 'EN': 'Slope'},
                      'landuse': {'DE': 'Landnutzung', 'EN': 'Landuse'},
                      'site_comment': {'DE': 'Kommentar', 'EN': 'Site comment'}}
    menu_name = 'Standort'
    newmenu_name = {'DE': 'Standort', 'EN': 'Site'}
    path = 'meta__site'
    newpath = 'site'
    filter_type = {'elevation': 'slider', 'rel_height': 'slider', 'orientation_degree': 'slider',
                   'slope': 'slider'}

    def __str__(self):
        return self.site_name  # TODO: is this useful? At the moment there is no information in site_name

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

    column_dict = {'geology': 'Geologie', 'soil_type': 'Bodentyp', 'porosity': 'Porosität',
                   'residual_moisture': 'Restfeuchte'}
    newcolumn_dict = {'geology': {'DE': 'Geologie', 'EN': 'Geology'},
                      'soil_type': {'DE': 'Bodentyp', 'EN': 'Soil Type'},
                      'porosity': {'DE': 'Porosität', 'EN': 'Porosity'},
                      'field_capacity': {'DE': 'Feldkapazität', 'EN': 'Field Capacity'},
                      'residual_moisture': {'DE': 'Restfeuchte', 'EN': 'Residual Moisture'}}
    menu_name = 'Boden'
    newmenu_name = {'DE': 'Boden', 'EN': 'Soil'}
    path = 'meta__soil'
    newpath = 'soil'

    def __str__(self):
        return self.geology  # TODO: at the moment only values in geology and nothing in soil_type. Check if geology
        # is always filled

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

    newcolumn_dict = {'unit_name': {'DE': 'Einheit', 'EN': 'Unit'}}
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

    newcolumn_dict = {'first_name': {'DE': 'Vorname', 'EN': 'First name'},
                      'last_name': {'DE': 'Nachname', 'EN': 'Last name'},
                      'institution_name': {'DE': 'Institut', 'EN': 'Institution'},
                      'department': {'DE': 'Abteilung', 'EN': 'Department'},
                      'comment': {'DE': 'Kommentar', 'EN': 'Comment'}}
    column_dict = {'first_name': 'Vorname', 'last_name': 'Nachname', 'institution_name': 'Institut',
                   'department': 'Abteilung', 'comment': 'Kommentar'}
    menu_name = 'Nutzer'
    newmenu_name = {'DE': 'Nutzer', 'EN': 'User'}
    path = 'meta__creator'
    newpath = 'creator'

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
        return self.value  # TODO: is that okay?

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

    # newcolumn_dict = {'ts_start': {'DE': 'Messbeginn', 'EN': 'Start of measurement'},
    #                'ts_stop': {'DE': 'Messende', 'EN': 'End of measurement'},
    #                'support': {'DE': 'Auflage???', 'EN': 'Support'},
    #                'spacing': {'DE': 'Schrittweite', 'EN': 'Spacing'},
    #                'comment': {'DE': 'Kommentar', 'EN': 'Comment'}}

    # TODO: ussed because users are creator and publisher. Improve this!
    newcolumn_dict = {'ts_start': {'DE': 'Messbeginn', 'EN': 'Start of measurement'},
                      'ts_stop': {'DE': 'Messende', 'EN': 'End of measurement'},
                      'support': {'DE': 'Auflage???', 'EN': 'Support'},
                      'spacing': {'DE': 'Schrittweite', 'EN': 'Spacing'},
                      'comment': {'DE': 'Kommentar', 'EN': 'Comment'},
                      # 'creator__LtUser': {'DE': 'Ersteller', 'EN': 'Creator'},
                      # 'publisher__LtUser': {'DE': 'Veröffentlicher', 'EN': 'Publisher'}
                      }

    column_dict = {'ts_start': 'Messbeginn', 'ts_stop': 'Messende', 'support': 'Support???', 'spacing': 'Schrittweite',
                   'comment': 'Kommentar'}
    menu_name = 'Messung'
    newmenu_name = {'DE': 'Messung', 'EN': 'Sampling'}
    path = 'meta'
    newpath = ''
    filter_type = {'ts_start': 'date', 'ts_stop': 'date'}

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

    newcolumn_dict = {'sensor_name': {'DE': 'Name', 'EN': 'Name'},
                      'manufacturer': {'DE': 'Hersteller', 'EN': 'Manufactorer'},
                      'sensor_comment': {'DE': 'Kommentar', 'EN': 'Comment'}}
    column_dict = {'sensor_name': 'Name', 'manufacturer': 'Hersteller', 'sensor_comment': 'Kommentar'}
    menu_name = 'Sensor'
    newmenu_name = {'DE': 'Sensor', 'EN': 'Sensor'}
    path = 'meta__sensor'
    newpath = 'sensor'

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

    newcolumn_dict = {'variable_name': {'DE': 'Variablenname', 'EN': 'Variable Name'}}
    column_dict = {'variable_name': 'Variablenname'}
    menu_name = 'Datentyp'
    newmenu_name = {'DE': 'Datentyp', 'EN': 'Data type'}
    path = 'meta__variable'
    newpath = 'variable'
    struct = {'menu1': variable_name}
    struct_name = {'menu1': menu_name}

    def __str__(self):
        return self.variable_name

    class Meta:
        managed = False
        db_table = 'tbl_variable'


# TODO: Following Code will be removed soon (by Marcus)
# TODO: There is no need to have this as models.Manager (Didn't use it). Find a better place for class
class FilterMenu(models.Manager):
    # Define here which tables to use; which columns are used is defined in the respective table
    menu_tables = [LtDomain, LtLicense, LtSite, LtSoil, LtUser, TblMeta, TblSensor, TblVariable]
    menu_dict = {tables.menu_name: tables for tables in menu_tables}

    def get_menu(detail_of_menu):
        general_struct = []

        for menu in FilterMenu.menu_tables:  # LtSoil,...
            sub_struct = {}
            for key, value in menu.column_dict.items():  # key: geology value: Geologie ...
                query_set = menu.objects.select_related().values_list(key, flat=True).distinct()  # marls, schist, ...
                if len(query_set) >= 1 and query_set[0] is not None:
                    # TODO: some query_sets give numbers --> other menu (from ... to ... instead of tick selection)
                    if detail_of_menu == 'submenu':
                        sub_struct.update({value: {'No Values': 0}})
                    elif detail_of_menu == 'complete_menu':
                        sub_struct.update({value: {str(key): False for key in query_set}})
            if sub_struct:
                general_struct.append({menu.menu_name: sub_struct})
        # print ('menu to send: ', general_struct)
        return general_struct

    # TODO: Can this be integrated in get_menu ? Might become confusing...
    # TODO: check if FilterMenu.menu_dict can be used to eliminate a loop or if
    def tick_submenu(top_menu_value, selection, cache_obj):
        submenu = {}

        for menu_dict in FilterMenu.get_menu('complete_menu'):  # complete menu in function object
            for key_1, value_1 in menu_dict.items():  # all top_level names (key_1 = Boden, Besitzer...)
                if key_1 == top_menu_value:  # check which menu has been clicked / Boden, Besitzer...
                    for key_2 in menu_dict[key_1]:  # all sub_level_names (key_2 = Geologie, Bodentyp...)
                        submenu[key_2] = dict(menu_dict[key_1][key_2])  # all values to choose from / Boolean if chosen
                        # set checked keys as True:
                        counts = FilterMenu.count_query(cache_obj, key_1, key_2, submenu[key_2].items())
                        for add_numbers, org_value in menu_dict[key_1][key_2].items():
                            submenu[key_2].update({add_numbers: [org_value, counts[add_numbers][0]]})
                        if selection:
                            for tick_key, tick_value in submenu[key_2].items():  # marls [True 651]
                                if tick_key in selection:
                                    submenu[key_2][tick_key][0] = True;

        return submenu

    def count_query(cache_obj, active_m_key=False, active_key=False,
                    submenu_key=False):  # , active_value=False):  # Boden Geologie Sandstone
        # def build_sub_query(cache_obj, active_m_key=False, active_key=False, active_value=False): # Boden Geologie
        # Sandstone
        m_map = {}
        paths = {}
        dataset_count = {}
        for menu in FilterMenu.menu_tables:
            m_map.update({menu.menu_name: {value: key for key, value in menu.column_dict.items()}})
            paths.update({value: key for key, value in menu.column_dict.items()})

        for values_3 in submenu_key:
            filter_list = django_data = ''
            if active_m_key and active_key:  # and active_value:
                active_filter_aswellas = FilterMenu.menu_dict[active_m_key].path + "__" + m_map[active_m_key][
                    active_key]  # meta__soil__geology
                filter_list = ".filter(" + active_filter_aswellas + "='" + values_3[0] + "')"

            for m_key in FilterMenu.menu_tables:
                # print('FilterMenu.menu_tables: ', FilterMenu.menu_tables)
                if m_key.menu_name in cache_obj and m_key.menu_name is not active_m_key:
                    for cache_key, cache_value in cache_obj.get(m_key.menu_name).items():  # e.g. Geologie: Sandstone
                        filter_aswellas = m_key.path + "__" + m_map[m_key.menu_name][
                            cache_key]  # e.g. soil +__+ geology
                        for value in cache_value:
                            filter_list = filter_list + ".filter(" + filter_aswellas + "='" + value + "')"

            django_data = eval("NmMetaDomain.objects" + filter_list + ".values('meta_id')")
            locations = django_data.values('meta__site__id').distinct()
            # bla = TblMeta.objects.filter(id=django_data)
            # print('django_data: ', bla)
            # selected_coords = (django_data.objects.filter(meta_id__geometry = LtLocation).distinct())
            # print('len: ', len(selected_coords))
            dataset_count.update({values_3[0]: [len(django_data), django_data]})
        # print('{values_3[0]: django_data}: ', {values_3[0]: [len(django_data), django_data]})
        return dataset_count

    def build_queryset(cache_obj):
        m_map = {}
        for menu in FilterMenu.menu_tables:
            m_map.update({menu.menu_name: {value: key for key, value in menu.column_dict.items()}})

        filter_list = django_data = ''
        for m_key in FilterMenu.menu_tables:
            if m_key.menu_name in cache_obj:
                for cache_key, cache_value in cache_obj.get(m_key.menu_name).items():  # e.g. Geologie: Sandstone
                    filter_aswellas = m_key.path + "__" + m_map[m_key.menu_name][cache_key]  # e.g. soil +__+ geology
                    for value in cache_value:
                        filter_list = filter_list + ".filter(" + filter_aswellas + "='" + value + "')"
                django_data = eval("NmMetaDomain.objects" + filter_list + ".values('meta_id')")
        # print(' + + + ++ ++ :  ', LtDomain.objects.filter(pid = None).all())

        return django_data


# build BW watershed table
class Basiseinzugsgebiet(models.Model):
    # Regular Django fields corresponding to the attributes in the Basiseinzugsgebiet shapefile.
    langname = models.CharField(max_length=100)
    area = models.FloatField()
    objectid = models.BigIntegerField()
    object_id = models.FloatField()
    fg_id = models.BigIntegerField()
    fgkz_nr = models.FloatField('flussgebietskennzahl')
    einzugsgeb = models.IntegerField('einzugsgebietsordnung')  # Einzugsgebiets Ordnung – eines Flusses, Baches
    einzugsg00 = models.CharField('einzugsgebietsordnung in Worten',
                                  max_length=80)  # Quellgebiet – oberstes Teilgebiet eines Flusses,
    # Baches / Zwischengebiet – Teilgebiet eines Flusses, Baches; wird begrenzt von 2 Hauptzuflüssen / Mündungsgebiet
    #  – unterstes Teilgebiet eines Flusses, Baches
    einzugsg01 = models.CharField(max_length=1)
    einzugsg02 = models.CharField(max_length=26)
    vor_fgkz_n = models.FloatField('flussgebietskennzahl des vorfluters')
    vor_fg_id = models.FloatField()
    vor_fg_lan = models.CharField('vorfluter_langname', max_length=100)
    wasserkoer = models.CharField('wasserkoerper_code', max_length=10)
    wasserko00 = models.CharField('wasserkoerper_name', max_length=85)
    aenderungs = models.CharField(max_length=20)
    aenderun00 = models.CharField(max_length=20)
    length = models.FloatField()
    mod_by = models.CharField(max_length=32)
    last_mod = models.CharField(max_length=20)
    se_anno_ca = models.CharField(max_length=254)
    wasserko01 = models.BigIntegerField()
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField(srid=31467)

    # Returns the string representation of the model.
    def __str__(self):  # __unicode__ on Python 2
        return self.langname
