from __future__ import unicode_literals

from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import Q
from django.http import QueryDict
from django.utils.translation import gettext, gettext_lazy


### New Database Schemata for vfw 2.0
### from metacatalog 2.0
"""
More information about the meaning of the tables and entries can be found at the code of metacatalog at
https://github.com/VForWaTer/metacatalog/tree/a9da92f23659ef7c3c3845cfecf470bc28ed93f8/metacatalog/models
(https://github.com/VForWaTer/metacatalog/models)
"""


class DatasourceTypes(models.Model):
    name = models.CharField(max_length=64)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datasource_types'

    def __str__(self):
        return f'Data source type {self.name}'


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
    data_names = models.TextField(null=True)
    variable_names = models.TextField(null=True)

    class Meta:
        managed = False
        db_table = 'datasources'

    def __str__(self):
        return f'{self.type.name} data source at {self.path} <ID={self.id}>'


class Datatypes(models.Model):
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=64)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datatypes'

    def __str__(self):
        return f'Data type {self.name}'


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
    title = models.CharField()

    class Meta:
        managed = False
        db_table = 'details'
        unique_together = (('entry', 'stem'),)

    def __str__(self):
        return f'{self.key}: {self.value}'


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
    uuid = models.CharField(max_length=36, default=lambda: str(uuid4()))
    title = models.CharField(max_length=512, blank=False)
    abstract = models.TextField(blank=True, null=True)
    external_id = models.TextField(blank=True, null=True)
    location = models.PointField(srid=4326)
    version = models.IntegerField(default=1)
    latest_version = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    is_partial = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    citation = models.CharField(max_length=2048, blank=True, null=True)

    license = models.ForeignKey('Licenses', models.DO_NOTHING, blank=True, null=True)
    variable = models.ForeignKey('Variables', models.DO_NOTHING)
    datasource = models.ForeignKey(Datasources, models.DO_NOTHING, blank=True, null=True)

    embargo = models.BooleanField(default=False)
    embargo_end = models.DateTimeField(blank=True, null=True)

    publication = models.DateTimeField(blank=True, null=True)
    lastupdate = models.DateTimeField(db_column='lastUpdate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'entries'

    def __str__(self):
        return f'<ID={self.id} {self.title[:20]} [{self.variable.name}] >'


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
        return f'{self.name} <ID={self.id}>'


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
        db_table = 'generic_geometry_data'
        unique_together = (('entry', 'index'),)

    def __str__(self):
        return f'<ID={self.id}>'


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
        return f'<ID={self.id}>'


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
        return f'<ID={self.id}>'


class Geom_Timeseries(models.Model):
    entry = models.OneToOneField(Entries, models.DO_NOTHING, primary_key=True)
    tstamp = models.DateTimeField()
    geom = models.GeometryField(srid=0)
    srid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geom_timeseries'
        unique_together = (('entry', 'tstamp'),)

    def __str__(self):
        return f'<ID={self.id}>'


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
        return f'{self.full_path} <ID={self.id}>'


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
        return f'{self.short_title} ({self.title})'


class Logs(models.Model):
    """
    Only used from metacatalog. Keeping an eye on that might help to keep track of changes on the database.
    """
    tstamp = models.DateTimeField()
    code = models.IntegerField()
    description = models.TextField()
    migration_head = models.IntegerField(blank=True, null=True)
    code_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'logs'

    def __str__(self):
        return f'Date={self.tstamp} Code={self.code}'


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
        return f'<Entry ID={self.entry.id}> tagged {self.keyword.value}'


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
        return (f'{self.person.full_name} <ID={self.person.id}> as {self.relationship_type.name} '
                f'for Entry <ID={self.entry.id}>')


class PersonRoles(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person_roles'

    def __str__(self):
        return f'{self.name} <ID={self.id}>'


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

    full_name = f'{first_name} {last_name}'

    class Meta:
        managed = False
        db_table = 'persons'

    def __str__(self):
        return f'{self.full_name} <ID={self.id}>'

    @staticmethod
    def filter(column, selection):
        filter_items = {f'nmpersonsentries__person__{column}__in': selection}
        return filter_items


class SpatialScales(models.Model):
    resolution = models.IntegerField()
    extent = models.PolygonField()
    support = models.DecimalField(max_digits=999, decimal_places=999)
    dimension_names = models.CharField(null=True, max_length=128)

    class Meta:
        managed = False
        db_table = 'spatial_scales'

    def __str__(self):
        return f'<ID={self.id}> extent={self.extent}'


class TemporalScales(models.Model):
    resolution = models.TextField()
    observation_start = models.DateTimeField()
    observation_end = models.DateTimeField()
    support = models.DecimalField(max_digits=999, decimal_places=999)
    dimension_names = models.CharField(null=True, max_length=128)

    class Meta:
        managed = False
        db_table = 'temporal_scales'


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
        return '<ID={}>   <UUID={}>    Name={}/{}'.format(self.uuid, self.uuid, self.name)

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
        return f'<ID={self.entry}>'


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
        return f'<ENTRY={self.entry}>'


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
        return f'<ID={self.id}>'


class Units(models.Model):
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=12)
    si = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'units'

    def __str__(self):
        return f'{self.name} <ID={self.id}>'


class Variables(models.Model):
    """
    Names of the dataset. Used in the Filter menu.
    """
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=12)
    unit = models.ForeignKey(Units, models.DO_NOTHING)
    keyword = models.ForeignKey(Keywords, models.DO_NOTHING, blank=True, null=True)
    column_names = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'variables'

    def __str__(self):
        return '{n} ({s}) [{u}]'.format(n=self.name, s=self.symbol, u=self.unit.symbol)

    @staticmethod
    def filter(column, selection):
        filter_items = {f'variable__{column}__in': selection}
        return filter_items

"""
*** End of Database description. Next block is for Database views ***
"""
class Locations(models.Model):
    """
    Access db view
    """
    id = models.BigIntegerField(primary_key=True, db_column='id')
    point_location = models.PointField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)
    area_sqm = models.DecimalField(max_digits=999, decimal_places=999)
    point_location_st_asewkt = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locations'

"""
*** End of Database views. Next block is for Functions/Classes ***
"""

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


class merit_hydro_vect_level2(models.Model):
    basin = models.BigIntegerField()
    geom = models.PolygonField(srid=4326)

    def __str__(self):
        return f'basin_id is {self.basin}'

    class Meta:
        managed = True
        db_table = 'merit_hydro_vect_level2'


class riv_pfaf_MERIT_Hydro_v07_Basins_v01(models.Model):
    """
    Datasource at https://www.reachhydro.org/home/params/merit-basins
    """
    comid = models.BigIntegerField()
    lengthkm = models.FloatField()
    lengthdir = models.FloatField()
    sinuosity = models.FloatField()
    slope = models.FloatField()
    uparea = models.FloatField()
    order = models.BigIntegerField()
    strmdrop_t = models.FloatField()
    slope_taud = models.FloatField()
    nextdownid = models.BigIntegerField()
    maxup = models.BigIntegerField()
    up1 = models.BigIntegerField()
    up2 = models.BigIntegerField()
    up3 = models.BigIntegerField()
    up4 = models.BigIntegerField()
    geom = models.MultiLineStringField(srid=4326)

    def __str__(self):
        return self.comid

    class Meta:
        managed = True
        db_table = 'riv_pfaf_merit_hydro_v07_basins_v01'


class cat_pfaf_MERIT_Hydro_v07_Basins_v01(models.Model):
    """
    Datasource at https://www.reachhydro.org/home/params/merit-basins
    pfaf_level_02

    """
    comid = models.BigIntegerField()
    unitarea = models.FloatField()
    geom = models.PolygonField(srid=4326)

    def __str__(self):
        return self.comid

    class Meta:
        managed = True
        db_table = 'cat_pfaf_merit_hydro_v07_basins_v01'
