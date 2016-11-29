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
    pid = models.ForeignKey('self', models.DO_NOTHING, db_column='pid')
    name = models.CharField(max_length=65)
    project = models.ForeignKey('LtProject', models.DO_NOTHING, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lt_domain'


class LtGround(models.Model):
    geology = models.CharField(max_length=65, blank=True, null=True)
    soil_type = models.CharField(max_length=65, blank=True, null=True)
    porosity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    field_capacity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    residual_moisture = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lt_ground'


class LtLicense(models.Model):
    abbrev = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    legal_text = models.CharField(max_length=-1, blank=True, null=True)
    text_url = models.CharField(max_length=255, blank=True, null=True)
    access = models.BooleanField()
    share = models.BooleanField()
    edit = models.BooleanField()
    commercial = models.BooleanField()
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lt_license'


class LtLocation(models.Model):
    wkt = models.CharField(unique=True, max_length=-1)
    centroid_x = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    centroid_y = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    srid = models.ForeignKey('SpatialRefSys', models.DO_NOTHING, db_column='srid', blank=True, null=True)
    geometry_type = models.CharField(max_length=15, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lt_location'


class LtProject(models.Model):
    name = models.CharField(unique=True, max_length=65)
    user = models.ForeignKey('LtUser', models.DO_NOTHING, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lt_project'


class LtUnit(models.Model):
    name = models.CharField(unique=True, max_length=65)
    abbrev = models.CharField(max_length=15)
    symbol = models.CharField(max_length=5)
    derived_si = models.NullBooleanField()
    to_derived_si = models.CharField(max_length=-1, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lt_unit'


class LtUser(models.Model):
    is_institution = models.BooleanField()
    first_name = models.CharField(max_length=65, blank=True, null=True)
    last_name = models.CharField(max_length=65, blank=True, null=True)
    institution_name = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=60)
    comment = models.CharField(max_length=-1, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lt_user'


class NmMetaDomain(models.Model):
    mid = models.ForeignKey('TblMeta', models.DO_NOTHING, db_column='mid', blank=True, null=True)
    domain = models.ForeignKey(LtDomain, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nm_meta_domain'


class TblMeta(models.Model):
    mid = models.AutoField(primary_key=True)
    ts_start = models.DateTimeField(blank=True, null=True)
    ts_stop = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey(LtUser, models.DO_NOTHING, blank=True, null=True)
    publisher = models.ForeignKey(LtUser, models.DO_NOTHING)
    geometry = models.ForeignKey(LtLocation, models.DO_NOTHING, blank=True, null=True)
    license = models.ForeignKey(LtLicense, models.DO_NOTHING)
    site = models.ForeignKey('TblSite', models.DO_NOTHING, blank=True, null=True)
    variable = models.ForeignKey('TblVariable', models.DO_NOTHING, blank=True, null=True)
    sensor = models.ForeignKey('TblSensor', models.DO_NOTHING, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_meta'


class TblSensor(models.Model):
    name = models.CharField(max_length=65, blank=True, null=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    documentation_url = models.CharField(max_length=-1, blank=True, null=True)
    last_configured = models.DateTimeField(blank=True, null=True)
    valid_until = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=-1, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_sensor'


class TblSite(models.Model):
    name = models.CharField(max_length=65, blank=True, null=True)
    elevation = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    rel_height = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    orientation_degree = models.IntegerField(blank=True, null=True)
    slope = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    landuse = models.CharField(max_length=65, blank=True, null=True)
    ground = models.ForeignKey(LtGround, models.DO_NOTHING, blank=True, null=True)
    comment = models.CharField(max_length=-1, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_site'


class TblVariable(models.Model):
    name = models.CharField(unique=True, max_length=65)
    abbrev = models.CharField(max_length=15)
    symbol = models.CharField(max_length=5)
    unit = models.ForeignKey(LtUnit, models.DO_NOTHING)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_variable'
