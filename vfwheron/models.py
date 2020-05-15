# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models


# TODO write docstrings! Devs not used to these models will have a hard time understanding these model names without
# explanation

class DjangoMigrations(models.Model):
    """

    """
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class LtDomain(models.Model):
    """

    """
    pid = models.ForeignKey('self', models.DO_NOTHING, db_column='pid', blank=True, null=True)
    domain_name = models.CharField(max_length=65)
    project = models.ForeignKey('LtProject', models.DO_NOTHING, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    column_dict = {'project__project_name': 'Project'}
    menu_name = 'Project/Domain'
    submenu_names = {'Project': 'Project', 'Domain': 'Domain', 'Subdomain': 'Subdomain'}
    path = 'nmmetadomain__domain'

    # Recursive exists only in that table, so the build process is highly customized to that one
    filter_type = {'project__project_name': 'recursive'}
    mother = 'LtProject'

    def __str__(self):
        return self.domain_name

    class Meta:
        managed = False
        db_table = 'lt_domain'


class LtLicense(models.Model):
    """

    """
    license_abbrev = models.CharField(max_length=20)
    license_name = models.CharField(max_length=255)
    legal_text = models.TextField(blank=True, null=True)
    text_url = models.CharField(max_length=255, blank=True, null=True)
    # TODO: Try to reduse flags in a table and use choices instead:
    # https://steelkiwi.com/blog/best-practices-working-django-models-python/
    access = models.BooleanField()
    share = models.BooleanField()
    edit = models.BooleanField()
    commercial = models.BooleanField()
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    column_dict = {'license_abbrev': 'License name'}
    menu_name = 'License'
    path = 'license'

    def __str__(self):
        return self.license_name

    class Meta:
        managed = False
        db_table = 'lt_license'


class LtLocation(models.Model):
    """

    """
    centroid_x = models.DecimalField("X-Coordinate", max_digits=65535, decimal_places=65535, blank=True, null=True)
    centroid_y = models.DecimalField("Y-Coordinate", max_digits=65535, decimal_places=65535, blank=True, null=True)
    srid = models.ForeignKey('SpatialRefSys', models.DO_NOTHING, db_column='srid', blank=True, null=True)
    geometry_type = models.CharField("Geometry", max_length=15, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    geom = models.GeometryField(unique=True, srid=0)

    column_dict = {'geometry_type': 'Geometry'}
    menu_name = 'Location'
    path = 'geometry'
    filter_type = {'geometry_type': 'draw'}

    def __str__(self):
        return '{"type": %s, "coordinates": [%s %s], "srid": %s}' % (
            self.geometry_type, self.centroid_x, self.centroid_y, self.srid)

    class Meta:
        managed = False
        db_table = 'lt_location'


class LtProject(models.Model):
    """

    """
    project_name = models.CharField(unique=True, max_length=65)
    user = models.ForeignKey('LtUser', models.DO_NOTHING, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    column_dict = {'project_name': 'Project name'}
    menu_name = 'project'
    path = 'nmmetadomain__domain__project'

    def __str__(self):
        return self.project_name

    class Meta:
        managed = False
        db_table = 'lt_project'


class LtQuality(models.Model):
    """

    """
    flag_name = models.CharField("flag", max_length=25)
    flag_weight = models.IntegerField("quantifier", blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    column_dict = {'flag_name': 'Flag', 'flag_weight': 'Quantifier'}
    menu_name = 'Quality'
    path = 'quality'
    filter_type = {'flag_weight': 'slider'}

    def __str__(self):
        return self.flag_name

    class Meta:
        managed = False
        db_table = 'lt_quality'


class LtSite(models.Model):
    """

    """
    site_name = models.CharField(max_length=65, blank=True, null=True)
    elevation = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    rel_height = models.DecimalField("relative height", max_digits=65535, decimal_places=65535, blank=True, null=True)
    orientation_degree = models.IntegerField("orientation", blank=True, null=True)
    slope = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    landuse = models.CharField(max_length=65, blank=True, null=True)
    site_comment = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    column_dict = {
        'site_name': 'Site name', 'elevation': 'Elevation', 'rel_height': 'Relative height',
        'orientation_degree': 'Orientation', 'slope': 'Slope', 'landuse': 'Landuse',
        'site_comment': 'Site comment'
    }
    menu_name = 'Site'
    path = 'site'
    filter_type = {
        'elevation': 'slider', 'rel_height': 'slider', 'orientation_degree': 'slider', 'slope': 'slider'
    }

    def __str__(self):
        return self.site_name  # TODO: is this useful? At the moment there is no information in site_name

    class Meta:
        managed = False
        db_table = 'lt_site'


class LtSoil(models.Model):
    """

    """
    geology = models.CharField(max_length=65, blank=True, null=True)
    soil_type = models.CharField(max_length=65, blank=True, null=True)
    porosity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    field_capacity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    residual_moisture = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    column_dict = {
        'geology': 'Geology', 'soil_type': 'Soil Type', 'porosity': 'Porosity',
        'field_capacity': 'Field Capacity', 'residual_moisture': 'Residual Moisture'
    }
    menu_name = 'Soil'
    path = 'soil'

    def __str__(self):
        return self.geology  # TODO: at the moment only values in geology and nothing in soil_type. Check if geology
        # is always filled

    class Meta:
        managed = False
        db_table = 'lt_soil'


class LtSourceType(models.Model):
    """

    """
    type_name = models.CharField(unique=True, max_length=65)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.type_name

    class Meta:
        managed = False
        db_table = 'lt_source_type'


class LtUnit(models.Model):
    """

    """
    unit_name = models.CharField("unit", unique=True, max_length=65)
    unit_abbrev = models.CharField(max_length=15)
    unit_symbol = models.CharField(max_length=5)
    derived_si = models.NullBooleanField()
    to_derived_si = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    column_dict = {'unit_name': 'Unit'}

    def __str__(self):
        return self.unit_name

    class Meta:
        managed = False
        db_table = 'lt_unit'


class LtUser(models.Model):
    """

    """

    is_institution = models.BooleanField()
    first_name = models.CharField(max_length=65, blank=True, null=True)
    last_name = models.CharField(max_length=65, blank=True, null=True)
    institution_name = models.CharField("institution", max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    comment = models.TextField("user Comment", blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    column_dict = {
        'institution_name': 'Institution', 'department': 'Department',
        'last_name': 'Last name', 'first_name': 'First name', 'comment': 'User Comment'
    }
    menu_name = 'User'
    path = 'creator'

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        managed = False
        db_table = 'lt_user'


class NmMetaDomain(models.Model):
    """

    """
    meta = models.ForeignKey('TblMeta', models.DO_NOTHING, blank=True, null=True)
    domain = models.ForeignKey(LtDomain, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nm_meta_domain'


class SpatialRefSys(models.Model):
    """

    """
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
    """

    """
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
    """

    """
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
    """

    """
    ts_start = models.DateTimeField("start of measurement", blank=True, null=True)
    ts_stop = models.DateTimeField("end of measurement", blank=True, null=True)
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

    # TODO: ussed because users are creator and publisher. Improve this!

    column_dict = {
        'ts_start': 'Start of measurement', 'ts_stop': 'End of measurement',
        'support': 'Support', 'spacing': 'Spacing', 'comment': 'Comment',
        }

    menu_name = 'Sampling'
    path = ''
    filter_type = {'ts_start': 'date', 'ts_stop': 'date'}

    class Meta:
        managed = False
        db_table = 'tbl_meta'


class TblSensor(models.Model):
    """

    """
    sensor_name = models.CharField(max_length=65, blank=True, null=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    documentation_url = models.TextField(blank=True, null=True)
    last_configured = models.DateTimeField(blank=True, null=True)
    valid_until = models.DateTimeField(blank=True, null=True)
    sensor_comment = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    column_dict = {'sensor_name': 'Name', 'manufacturer': 'Manufacturer', 'sensor_comment': 'sensor comment'}
    menu_name = 'Sensor'
    path = 'sensor'

    def __str__(self):
        return self.sensor_name

    class Meta:
        managed = False
        db_table = 'tbl_sensor'


class TblVariable(models.Model):
    """

    """
    variable_name = models.CharField(unique=True, max_length=65)
    variable_abbrev = models.CharField(max_length=15)
    variable_symbol = models.CharField(max_length=5)
    unit = models.ForeignKey(LtUnit, models.DO_NOTHING)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    column_dict = {'variable_name': 'Variable Name'}
    menu_name = 'Data type'
    path = 'variable'

    def __str__(self):
        return self.variable_name

    class Meta:
        managed = False
        db_table = 'tbl_variable'
