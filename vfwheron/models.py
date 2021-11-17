# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import Q
from django.http import QueryDict
from django.utils.translation import gettext, gettext_lazy


# TODO write docstrings! Devs not used to these models will have a hard time understanding these model names without
#  explanation

# TODO: Models are read at startup. To get translations later when the project is running
#  make translations lazy.
#  https://simpleisbetterthancomplex.com/tips/2016/10/17/django-tip-18-translations.html


# class DjangoMigrations(models.Model):
#     """
#
#     """
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()
#
#     class Meta:
#         managed = True
#         db_table = 'django_migrations'

### New Database Schemata for vfw 2.0
### from metacatalog 2.0


class DatasourceTypes(models.Model):
    name = models.CharField(max_length=64)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datasource_types'

    def __str__(self):
        return 'Data source type {}'.format(self.name)


class Datasources(models.Model):
    type = models.ForeignKey('DatasourceTypes', models.DO_NOTHING)
    path = models.TextField()
    args = models.TextField(blank=True, null=True)
    creation = models.DateTimeField(blank=True, null=True)
    lastupdate = models.DateTimeField(db_column='lastUpdate', blank=True, null=True)  # Field name made lowercase.
    encoding = models.CharField(max_length=64, blank=True, null=True)
    datatype = models.ForeignKey('Datatypes', models.DO_NOTHING)
    temporal_scale = models.ForeignKey('TemporalScales', models.DO_NOTHING, blank=True, null=True)
    spatial_scale = models.ForeignKey('SpatialScales', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datasources'

    def __str__(self):
        return '{} data source at {} <ID={}}>'.format(self.type.name, self.path, self.id)


class Datatypes(models.Model):
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=64)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datatypes'

    def __str__(self):
        return 'Data type {}'.format(self.name)


class Details(models.Model):
    """
    Used for the advanced Filter.
    """
    entry = models.ForeignKey('Entries', models.DO_NOTHING, blank=True, null=True)
    key = models.CharField(max_length=20)
    stem = models.CharField(max_length=20)
    value = models.TextField()
    description = models.TextField(blank=True, null=True)
    thesaurus = models.ForeignKey('Thesaurus', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'details'
        unique_together = (('entry', 'stem'),)

    def __str__(self):
        return '{}: {}'.format(self.key, self.value)


class Entries(models.Model):
    """
    Main Table.
    For Filter use ID, creation, end, embargo, version (all versions for advanced filter).
    Filter connections to other tables:
    variable_id, license_id.

        From django docs (https://docs.djangoproject.com/en/2.2/ref/contrib/gis/model-api/):

    If you wish to perform arbitrary distance queries using non-point geometries in WGS84 in PostGIS and you want
    decent performance, enable the GeometryField.geography keyword so that geography database type is used instead.

    """
    uuid = models.CharField(max_length=36)
    title = models.CharField(max_length=512)
    abstract = models.TextField(blank=True, null=True)
    external_id = models.TextField(blank=True, null=True)
    location = models.PointField(srid=4326)
    geom = models.GeometryField(srid=4326, blank=True, null=True)
    version = models.IntegerField()
    latest_version = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    is_partial = models.BooleanField()
    comment = models.TextField(blank=True, null=True)
    citation = models.CharField(max_length=2048, blank=True, null=True)

    license = models.ForeignKey('Licenses', models.DO_NOTHING, blank=True, null=True)
    variable = models.ForeignKey('Variables', models.DO_NOTHING)
    datasource = models.ForeignKey(Datasources, models.DO_NOTHING, blank=True, null=True)

    embargo = models.BooleanField()
    embargo_end = models.DateTimeField(blank=True, null=True)

    publication = models.DateTimeField(blank=True, null=True)
    lastupdate = models.DateTimeField(db_column='lastUpdate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'entries'

    def __str__(self):
        return '<ID={} {} [{}] >'.format(self.id, self.title[:20], self.variable.name)


class EntrygroupTypes(models.Model):
    """
    Filter (advanced) only entrygroup 'project'
    """
    name = models.CharField(max_length=40)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'entrygroup_types'

    def __str__(self):
        return '{} <ID={}>'.format(self.name, self.id)


class Entrygroups(models.Model):
    type = models.ForeignKey('EntrygroupTypes', models.DO_NOTHING)
    title = models.CharField(max_length=40, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    uuid = models.CharField(max_length=36)
    publication = models.DateTimeField(blank=True, null=True)
    lastupdate = models.DateTimeField(db_column='lastUpdate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'entrygroups'

    def __str__(self):
        return '{}{} <ID={}>'.format(self.type.name, " %s" % self.title[:20] if self.title is not None else '',
                                     self.id)


class Generic_Geometry_Data(models.Model):
    entry = models.OneToOneField(Entries, models.DO_NOTHING, primary_key=True)
    index = models.IntegerField()
    geom = models.GeometryField(srid=0)
    srid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geneic_geometry_data'
        unique_together = (('entry', 'index'),)

    def __str__(self):
        return '<ID={}>'.format(self.id)


class Generic_1D_Data(models.Model):
    entry = models.OneToOneField(Entries, models.DO_NOTHING, primary_key=True)
    index = models.DecimalField(max_digits=999, decimal_places=999)
    value = models.DecimalField(max_digits=999, decimal_places=999)
    precision = models.DecimalField(max_digits=999, decimal_places=999, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'generic_1d_data'
        unique_together = (('entry', 'index'),)

    def __str__(self):
        return '<ID={}>'.format(self.id)


class Generic_2D_Data(models.Model):
    entry = models.OneToOneField(Entries, models.DO_NOTHING, primary_key=True)
    index = models.DecimalField(max_digits=999, decimal_places=999)
    value1 = models.DecimalField(max_digits=999, decimal_places=999)
    value2 = models.DecimalField(max_digits=999, decimal_places=999)
    precision1 = models.DecimalField(max_digits=999, decimal_places=999, blank=True, null=True)
    precision2 = models.DecimalField(max_digits=999, decimal_places=999, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'generic_2d_data'
        unique_together = (('entry', 'index'),)

    def __str__(self):
        return '<ID={}>'.format(self.id)


class Geom_Timeseries(models.Model):
    # entry = models.ForeignKey(Entries, models.DO_NOTHING, primary_key=True)  # This produces a django warning
    entry = models.OneToOneField(Entries, models.DO_NOTHING, primary_key=True)
    tstamp = models.DateTimeField()
    geom = models.GeometryField(srid=0)
    srid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geom_timeseries'
        unique_together = (('entry', 'tstamp'),)

    def __str__(self):
        return '<ID={}>'.format(self.id)


class Keywords(models.Model):
    """
    Used for advanced filter. Shows a complete list and the 10 most common (but not the ones every dataset has)
    """
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    value = models.CharField(max_length=1024)
    uuid = models.CharField(unique=True, max_length=64, blank=True, null=True)
    full_path = models.TextField(blank=True, null=True)
    thesaurus = models.ForeignKey('Thesaurus', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'keywords'


    def __str__(self):
        return '{} <ID={}>'.format(self.full_path, self.id)


class Licenses(models.Model):
    """
    Use one of the Boolean Fields for the Filter menu.
    """
    short_title = models.CharField(max_length=40)
    title = models.TextField()
    summary = models.TextField(blank=True, null=True)
    full_text = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    by_attribution = models.BooleanField()
    share_alike = models.BooleanField()
    commercial_use = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'licenses'

    def __str__(self):
        return '{} ({})'.format(self.short_title, self.title)


class Logs(models.Model):
    tstamp = models.DateTimeField()
    code = models.IntegerField()
    description = models.TextField()
    migration_head = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logs'

    def __str__(self):
        return 'Date={} Code={}'.format(self.tstamp, self.code)


class NmEntrygroups(models.Model):
    entry = models.OneToOneField(Entries, models.DO_NOTHING, primary_key=True)
    group = models.ForeignKey(Entrygroups, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'nm_entrygroups'
        unique_together = (('entry', 'group'),)


class NmKeywordsEntries(models.Model):
    keyword = models.OneToOneField(Keywords, models.DO_NOTHING, primary_key=True)
    entry = models.ForeignKey(Entries, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'nm_keywords_entries'
        unique_together = (('keyword', 'entry'),)

    def __str__(self):
        return '<Entry ID={}> tagged {}'.format(self.entry.id, self.keyword.value)


class NmPersonsEntries(models.Model):
    person = models.OneToOneField('Persons', models.DO_NOTHING, primary_key=True)
    entry = models.ForeignKey(Entries, models.DO_NOTHING)
    relationship_type = models.ForeignKey('PersonRoles', models.DO_NOTHING)
    order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nm_persons_entries'
        unique_together = (('person', 'entry'),)

    def __str__(self):
        return '{} <ID={}> as {} for Entry <ID={}>'.format(self.person.full_name, self.person.id,
                                                           self.relationship_type.name, self.entry.id)


class PersonRoles(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person_roles'

    def __str__(self):
        return '{} <ID={}>'.format(self.name, self.id)


class Persons(models.Model):
    """
    Filter for persons in advanced filter.
    """
    is_organisation = models.BooleanField(default=False)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    affiliation = models.CharField(max_length=1024, blank=True, null=True)
    organisation_name = models.CharField(max_length=1024, blank=True, null=True)
    organisation_abbrev = models.CharField(max_length=64, blank=True, null=True)
    attribution = models.CharField(max_length=1024, blank=True, null=True)

    full_name = '{} {}'.format(first_name, last_name)

    class Meta:
        managed = False
        db_table = 'persons'

    def __str__(self):
        return '{} <ID={}>'.format(self.full_name, self.id)

    @staticmethod
    def filter(column, selection):
        filter_items = {'nmpersonsentries__person__' + column + '__in': selection}
        print('filter_items: ', filter_items)
        return filter_items


class SpatialScales(models.Model):
    resolution = models.IntegerField()
    extent = models.PolygonField()
    support = models.DecimalField(max_digits=999, decimal_places=999)

    class Meta:
        managed = False
        db_table = 'spatial_scales'

    def __str__(self):
        return '<ID={}> extent={}'.format(self.id, self.extent)


class TemporalScales(models.Model):
    resolution = models.TextField()
    observation_start = models.DateTimeField()
    observation_end = models.DateTimeField()
    support = models.DecimalField(max_digits=999, decimal_places=999)

    class Meta:
        managed = False
        db_table = 'temporal_scales'

    # def __str__(self):
    #     return '<ID={}> observation start/end={}/{}'.format(self.id, self.observation_start, self.observation_end)


class Thesaurus(models.Model):
    uuid = models.CharField(unique=True, max_length=64)
    name = models.CharField(unique=True, max_length=1024)
    title = models.TextField()
    organisation = models.TextField()
    description = models.TextField(blank=True, null=True)
    url = models.TextField()

    class Meta:
        managed = False
        db_table = 'thesaurus'

    def __str__(self):
        return '<ID={}>   <UUID={}>    Name={}/{}'.format(self.id, self.uuid, self.name)


class Timeseries(models.Model):
    entry = models.OneToOneField(Entries, models.DO_NOTHING, primary_key=True)
    tstamp = models.DateTimeField()
    data = ArrayField(models.DecimalField(max_digits=999, decimal_places=999, blank=False, null=True), size=3)
    precision = ArrayField(models.DecimalField(max_digits=999, decimal_places=999, blank=True, null=True), size=3)

    class Meta:
        managed = False
        db_table = 'timeseries'
        unique_together = (('entry', 'tstamp'),)

    def __str__(self):
        return '<ID={}>'.format(self.id)


class Timeseries_1D(models.Model):
    entry = models.OneToOneField(Entries, models.DO_NOTHING, primary_key=True)
    tstamp = models.DateTimeField()
    value = models.DecimalField(max_digits=999, decimal_places=999)
    precision = models.DecimalField(max_digits=999, decimal_places=999, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'timeseries_1d'
        unique_together = (('entry', 'tstamp'),)

    def __str__(self):
        return '<ID={}>'.format(self.id)


class Timeseries_2D(models.Model):
    entry = models.OneToOneField(Entries, models.DO_NOTHING, primary_key=True)
    tstamp = models.DateTimeField()
    value1 = models.DecimalField(max_digits=999, decimal_places=999)
    value2 = models.DecimalField(max_digits=999, decimal_places=999)
    precision1 = models.DecimalField(max_digits=999, decimal_places=999, blank=True, null=True)
    precision2 = models.DecimalField(max_digits=999, decimal_places=999, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'timeseries_2d'
        unique_together = (('entry', 'tstamp'),)

    def __str__(self):
        return '<ID={}>'.format(self.id)


class Units(models.Model):
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=12)
    si = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'units'

    def __str__(self):
        return '{} <ID={}>'.format(self.name, self.id)


class Variables(models.Model):
    """
    Names of the dataset. Used in the Filter menu.
    """
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=12)
    unit = models.ForeignKey(Units, models.DO_NOTHING)
    keyword = models.ForeignKey(Keywords, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'variables'

    def __str__(self):
        return '{n} ({s}) [{u}]'.format(n=self.name, s=self.symbol, u=self.unit.symbol)
        # return '{} [{}] <ID={}>'.format(self.name, self.unit.symbol, self.id)

    @staticmethod
    def filter(column, selection):
        filter_items = {'variable__' + column + '__in': selection}
        return filter_items


class BasicFilter:
    """
    Class to collect relevant information for filter
    """
    embargo = Entries.objects.values_list('embargo', flat=True).distinct()
    licenses = Licenses.objects.values_list('commercial_use', flat=True).distinct()
    variables = Variables.objects.values_list('name', flat=True).distinct()

    menu_entries = [Variables, Licenses, Entries]  # Licenses]


class AdvancedFilter(BasicFilter):
    """
    Class to collect relevant information for advanced filter
    """
    details = Details.objects.values_list('value', flat=True).distinct()


# class LocationFilter(models.Model):
#     """
#     Fake class to write location from Entries to a separate entry online in the menu.
#     """
#     location = models.PointField(srid=0)
#
#     db_alias_child = {'location': 'Location'}
#     db_alias_child_adv = {'bla': 'blala'}
#     menu_name = gettext("Filter from map")
#     path = ''
#     filter_type = {'location': 'draw'}
#
#     class Meta:
#         managed = False
#         db_table = 'entries'
#
