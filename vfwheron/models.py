# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.contrib.gis.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cluster(models.Model):
    ts = models.DateTimeField()
    meta = models.ForeignKey('TblCore', models.DO_NOTHING)
    val = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cluster'
        unique_together = (('ts', 'meta'),)


class Dim1D(models.Model):
    core = models.ForeignKey('TblCore', models.DO_NOTHING, primary_key=True)
    index_variable = models.ForeignKey('TblVariable', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_1d'


class DimTs(models.Model):
    core = models.ForeignKey('TblCore', models.DO_NOTHING, primary_key=True)
    spacing_in_sec = models.IntegerField(blank=True, null=True)
    elevation = models.FloatField(blank=True, null=True)
    relative_height = models.FloatField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_ts'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class LtAuthor(models.Model):
    first_name = models.CharField(max_length=65, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    institution = models.BooleanField()
    email = models.TextField(blank=True, null=True)  # This field type is a guess.
    url = models.TextField(blank=True, null=True)  # This field type is a guess.
    institution_0 = models.ForeignKey('LtInstitution', models.DO_NOTHING, db_column='institution_id', blank=True, null=True)  # Field renamed because of name conflict.
    institution_department = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lt_author'


class LtInstitution(models.Model):
    institution_name = models.CharField(max_length=255, blank=True, null=True)
  
    class Meta:
        managed = False
        db_table = 'lt_institution'


class LtLicense(models.Model):
    abbrev = models.CharField(max_length=20)
    full_name = models.TextField()
    license_text = models.TextField(blank=True, null=True)
    license_url = models.TextField(blank=True, null=True)  # This field type is a guess.
    access = models.BooleanField()
    share = models.BooleanField()
    edit = models.BooleanField()
    commercial = models.BooleanField()
  
    class Meta:
        managed = False
        db_table = 'lt_license'


class LtSourceType(models.Model):
    source_type = models.CharField(max_length=24, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    mime = models.TextField(blank=True, null=True)
 
    class Meta:
        managed = False
        db_table = 'lt_source_type'


class LtUnit(models.Model):
    full_name = models.CharField(max_length=255)
    abbrev = models.CharField(max_length=20)
    symbol = models.CharField(max_length=10)
    si_base = models.CharField(max_length=255, blank=True, null=True)
    si = models.BooleanField()
 
    class Meta:
        managed = False
        db_table = 'lt_unit'


class NmCoreAdditional(models.Model):
    core = models.ForeignKey('TblCore', models.DO_NOTHING)
    additional = models.ForeignKey('TblAdditional', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'nm_core_additional'


class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=255, blank=True, null=True)
    auth_srid = models.IntegerField(blank=True, null=True)
    srtext = models.TextField(blank=True, null=True)
    proj4text = models.TextField(blank=True, null=True)
  
    class Meta:
        managed = False
        db_table = 'spatial_ref_sys'


class TblAdditional(models.Model):
    meta_key = models.CharField(max_length=60)
    meta_value_str = models.CharField(max_length=255, blank=True, null=True)
    meta_value_real = models.FloatField(blank=True, null=True)
    meta_value_text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_additional'


class TblCore(models.Model):
    ts_start = models.DateTimeField(blank=True, null=True)
    ts_stop = models.DateTimeField(blank=True, null=True)
    geom = models.GeometryField()
    variable = models.ForeignKey('TblVariable', models.DO_NOTHING, blank=True, null=True)
    source = models.ForeignKey('TblSource', models.DO_NOTHING, blank=True, null=True)
    license = models.ForeignKey('LtLicense', models.DO_NOTHING, blank=True, null=True)
    author = models.ForeignKey('LtAuthor', models.DO_NOTHING, blank=True, null=True, related_name='Author')
    publisher = models.ForeignKey('LtAuthor', models.DO_NOTHING, blank=True, null=True, related_name='Publisher')
    srid = models.ForeignKey('SpatialRefSys', models.DO_NOTHING, db_column='srid', blank=True, null=True)
    data_dimension = models.CharField(max_length=3, blank=True, null=True)
    external_id = models.IntegerField(blank=True, null=True)
    identifier_name = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'tbl_core'


class TblSite(models.Model):
    geom = models.GeometryField(blank=True, null=True)
    srid = models.ForeignKey('SpatialRefSys', models.DO_NOTHING, db_column='srid', blank=True, null=True, related_name='Srid')
    site_name = models.CharField(max_length=255, blank=True, null=True)
    external_id = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    geom_local = models.GeometryField(blank=True, null=True)
    srid_local = models.ForeignKey('SpatialRefSys', models.DO_NOTHING, db_column='srid_local', blank=True, null=True, related_name='SridLocal')
  
    class Meta:
        managed = False
        db_table = 'tbl_site'


class TblSource(models.Model):
    type = models.ForeignKey('LtSourceType', models.DO_NOTHING)
    cmd = models.TextField()
    comment = models.TextField(blank=True, null=True)
  
    class Meta:
        managed = False
        db_table = 'tbl_source'


class TblVariable(models.Model):
    full_name = models.CharField(max_length=255)
    unit = models.ForeignKey('LtUnit', models.DO_NOTHING)
    abbrev = models.CharField(max_length=20)
    symbol = models.CharField(max_length=10)
  
    class Meta:
        managed = False
        db_table = 'tbl_variable'
