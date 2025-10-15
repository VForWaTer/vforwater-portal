from __future__ import unicode_literals

#from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import Q
from django.http import QueryDict
from django.utils.translation import gettext, gettext_lazy
import uuid

# TODO write docstrings! Devs not used to these models will have a hard time understanding these model names without
#  explanation

# TODO: Models are read at startup. To get translations later when the project is running
#  make translations lazy.
#  https://simpleisbetterthancomplex.com/tips/2016/10/17/django-tip-18-translations.html


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

class MetacatalogInfo(models.Model):
    db_version = models.IntegerField(null=False)
    min_py_version = models.CharField(max_length=64, blank=True, null=True)
    max_py_version = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metacatalog_info'


class Datasources(models.Model):
    type = models.ForeignKey('DatasourceTypes', models.DO_NOTHING)
    path = models.TextField()
    #args = models.TextField(blank=True, null=True)
    args = models.JSONField(default=dict, blank=True, null=True)
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
        # return "%s data source at %s <ID=%d>" % (self.type.name, self.path, self.id)


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
    #key = models.CharField(max_length=20) 
    key = models.TextField(blank=False, null=False)
    #stem = models.CharField(max_length=20)
    stem = models.TextField(blank=False, null=True)
    value = models.TextField()
    description = models.TextField(blank=True, null=True)
    thesaurus = models.ForeignKey('Thesaurus', models.DO_NOTHING, blank=True, null=True)
    # raw_value = models.JSONField()  # TODO: This lines reveals a bug. Try to catch it...
    title = models.CharField()

    class Meta:
        managed = False
        db_table = 'details'
        constraints = [ models.UniqueConstraint(fields=['entry', 'key'], name='details_entry_id_key'),]
        #unique_together = (('entry', 'key'),)

    def __str__(self):
        return f'{self.key}: {self.value}'


def generate_uuid_str():
    return str(uuid.uuid4())

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


    author = models.ForeignKey( 'Persons', on_delete=models.SET_NULL, null=True, blank=True, db_column='author_id', 
                               #on_update=models.CASCADE
                               )    
    #uuid = models.CharField(max_length=36, default=lambda: str(uuid4()))

    uuid = models.CharField(max_length=36, default=generate_uuid_str, editable=False)
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
   # name = models.CharField(max_length=40)
    name = models.TextField()

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

    # def keyword_path(self):
    #     """Keyword path
    #     Returns the full keyword path for the given level.
    #     The levels are separated by a '>' sign. The levels are:
    #     Topic > Term > Variable_Level_1 > Variable_Level_2 > Variable_Level_3 > Detailed_Variable
    #     Returns
    #     -------
    #     keyword_path : str
    #         The full keyword path
    #     """
    #     keyword_path = [self.value]
    #     parent = self.parent
    #     print('keyword_path: ', keyword_path)
    #     print('parent: ', parent)
    #
    #     while parent is not None:
    #         keyword_path.append(parent.value)
    #         parent = parent.parent
    #
    #     return ' > '.join(reversed(keyword_path))

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
        # return '{} <ID={}>'.format(self.title, self.id)


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
    # uuid = models.CharField(max_length=36)

    full_name = f'{first_name} {last_name}'

    class Meta:
        managed = False
        db_table = 'persons'

    def __str__(self):
        return f'{self.full_name} <ID={self.id}>'

    @staticmethod
    def filter(column, selection):
        filter_items = {f'nmpersonsentries__person__{column}__in': selection}
        print('filter_items: ', filter_items)
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
        return '<ID={}>   <UUID={}>    Name={}/{}'.format(self.uuid, self.uuid, self.name)

# TODO: check if DecimalField or FloatField fits better to 'real' here.
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
        # return '{} [{}] <ID={}>'.format(self.name, self.unit.symbol, self.id)

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
    # entry = models.ForeignKey(Entries, on_delete=models.DO_NOTHING)
    # st_asewkt = models.CharField()  # TODO: why do I get a list of points for point data?
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
    # has_access =

    # menu_entries = {'Embargo': embargo, 'Creation': creation, 'End': end, 'License': licenses,
    #                 'Variables': variables}
    # menu_entries = [variables]
    menu_entries = [Variables, Licenses, Entries]  # Licenses]

    # class Meta:
    #     abstract = True


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
# Delineate Watershed Data models

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
    pfaf_level_02
    shp2pgsql -a -s 4326 cat_pfaf_26_MERIT_Hydro_v07_Basins_v01_bugfix1.shp cat_pfaf_MERIT_Hydro_v07_Basins_v01 | psql -h localhost -d metacatalog-dev -U postgres -p 5434
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
    add new shapes with:
     shp2pgsql -a -s 4326 riv_pfaf_21_MERIT_Hydro_v07_Basins_v01_bugfix1.shp riv_pfaf_MERIT_Hydro_v07_Basins_v01 | psql -h localhost -d metacatalog-dev -U postgres -p 5434

    """
    comid = models.BigIntegerField()
    unitarea = models.FloatField()
    geom = models.PolygonField(srid=4326)

    def __str__(self):
        return self.comid

    class Meta:
        managed = True
        db_table = 'cat_pfaf_merit_hydro_v07_basins_v01'



class UserAccessToken(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Persons', on_delete=models.CASCADE, db_column='user_id', related_name='access_tokens')
    token_hash = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'user_access_tokens'
        #constraints = [ models.ForeignKeyConstraint(['user_id'], ['persons.id'], name='persons_access_token', on_delete=models.CASCADE,),]

    def __str__(self):
        return f'{self.user} - {self.token_hash[:10]}...'
    


# TODO: the simple basins should be used for bigger catchments to reduce processing time. But the given data has the wrong comID. Maybe created by yourself
# class cat_pfaf_MERIT_Hydro_v07_Basins_v01_simple(models.Model):
#     """
#     Datasource at https://www.reachhydro.org/home/params/merit-basins
#     pfaf_level_02
#     add new shapes with:
#     shp2pgsql -a -I -s 4326 cat_pfaf_29_MERIT_Hydro_v07_Basins_v01.shp cat_pfaf_MERIT_Hydro_v07_Basins_v01_simple | psql -h localhost -d metacatalog-dev -U postgres -p 5434
#     shp2pgsql -I -i -s 4326 cat_pfaf_22_MERIT_Hydro_v07_Basins_v01.shp cat_pfaf_merit_hydro_v07_basins_v01_simple | psql -h localhost -d metacatalog-dev -U postgres -p 5434
#     """
#     comid = models.BigIntegerField()
#     unitarea = models.FloatField()
#     geom = models.PolygonField(srid=4326)
#
#     def __str__(self):
#         return self.comid
#
#     class Meta:
#         managed = True
#         db_table = 'cat_pfaf_merit_hydro_v07_basins_v01_simple'

# add a shape file: -a = add; -I = Create a GiST index on the geometry column; -i = Coerce all integers to standard 32-bit integers.
# shp2pgsql -a -s 4326 riv_pfaf_21_MERIT_Hydro_v07_Basins_v01_bugfix1.shp riv_pfaf_MERIT_Hydro_v07_Basins_v01 | psql -h localhost -d metacatalog-dev -U postgres -p 5434

# raster data to db
# raster2pgsql -s 4326 -I -C /home/marcus/github/delineator/delineator-1.0/data/raster/flowdir_basins/flowdir27.tif -t 50x50 -F public.flowdirbasins > /home/marcus/github/delineator/delineator-1.0/flowdir_basin.sql
# psql -p 5434 -U postgres -h localhost -d metacatalog-dev -f flowdir_basin.sql
#
# raster2pgsql -s 4326 -I -C /home/marcus/github/delineator/delineator-1.0/data/raster/accum_basins/accum27.tif -t 50x50 -F public.accumbasins > /home/marcus/github/delineator/delineator-1.0/accum_basin.sql
# psql -p 5434 -U postgres -h localhost -d metacatalog-dev -f accum_basin.sql

#
# entries_list = [{'title': 'LUBW gauge data: Weinheim', 'id': 386, 'uuid': 'c67343d3-4ca6-418a-90d1-a6f50ba23e73', 'variable__name': 'discharge', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 29, 44, 292824)},{'title': 'LUBW gauge data: Weinheim', 'id': 387, 'uuid': 'fa7a06ba-7180-4c62-b10d-17ef2038b487', 'variable__name': 'discharge', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 29, 44, 326063)},{'title': 'LUBW gauge data: Weinheim-SKA', 'id': 866, 'uuid': 'ade15e99-ab11-41c7-8bfa-6f1b5722978d', 'variable__name': 'discharge', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 30, 16, 201908)},{'title': 'LUBW gauge data: Weinheim-SKA', 'id': 867, 'uuid': 'db8bf0f6-5ba5-4277-924b-49f2c0bd73e5', 'variable__name': 'discharge', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 30, 16, 235210)},{'title': 'LUBW gauge data: Weinheim', 'id': 388, 'uuid': '3d4a4b91-7acf-4fb6-bd05-009b14284462', 'variable__name': 'river water level', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 29, 44, 417271)},{'title': 'LUBW gauge data: Weinheim', 'id': 389, 'uuid': '416351da-6812-4ced-a5da-31cd6641d0f6', 'variable__name': 'river water level', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 29, 44, 451066)},{'title': 'LUBW gauge data: Weinheim-SKA', 'id': 868, 'uuid': '65222d16-04d8-418c-a5dd-d1c8a9d86ad8', 'variable__name': 'river water level', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 30, 16, 335406)},{'title': 'LUBW gauge data: Weinheim-SKA', 'id': 869, 'uuid': 'f634afb4-0d0b-4775-9a84-c2c87e72778f', 'variable__name': 'river water level', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 30, 16, 368602)}]
# split_datasets = [{'id': 386, 'nmentrygroups__group_id': 183}, {'id': 387, 'nmentrygroups__group_id': 183}, {'id': 388, 'nmentrygroups__group_id': 184}, {'id': 389, 'nmentrygroups__group_id': 184}, {'id': 866, 'nmentrygroups__group_id': 423}, {'id': 867, 'nmentrygroups__group_id': 423}, {'id': 868, 'nmentrygroups__group_id': 424}, {'id': 869, 'nmentrygroups__group_id': 424}]
# entries_list = [
#     {'title': 'LUBW gauge data: Weinheim', 'id': 386, 'uuid': 'c67343d3', 'variable__name': 'discharge', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 29, 44, 292824)},
#     {'title': 'LUBW gauge data: Weinheim', 'id': 387, 'uuid': 'fa7a06ba', 'variable__name': 'discharge', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 29, 44, 326063)},
#     {'title': 'LUBW gauge data: Weinheim-SKA', 'id': 866, 'uuid': 'ade15e99', 'variable__name': 'discharge', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 30, 16, 201908)},
#     {'title': 'LUBW gauge data: Weinheim-SKA', 'id': 867, 'uuid': 'db8bf0f6', 'variable__name': 'discharge', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 30, 16, 235210)},
#     {'title': 'LUBW gauge data: Weinheim', 'id': 388, 'uuid': '3d4a4b91', 'variable__name': 'river water level', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 29, 44, 417271)},
#     {'title': 'LUBW gauge data: Weinheim', 'id': 389, 'uuid': '416351da', 'variable__name': 'river water level', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 29, 44, 451066)},
#     {'title': 'LUBW gauge data: Weinheim-SKA', 'id': 868, 'uuid': '65222d16', 'variable__name': 'river water level', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 30, 16, 335406)},
#     {'title': 'LUBW gauge data: Weinheim-SKA', 'id': 869, 'uuid': 'f634afb4', 'variable__name': 'river water level', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 30, 16, 368602)}
# ]
# entries_list_new = [
#     {'title': 'LUBW gauge data: Weinheim', 'id': 386, 'uuid': 'c67343d3', 'variable__name': 'discharge', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 29, 44, 292824),
#      'split_ids': [386, 387], 'split_uuid': ['c67343d3', 'fa7a06ba'], 'split_embargo_end': [datetime.datetime(2023, 5, 6, 10, 29, 44, 292824), datetime.datetime(2023, 5, 6, 10, 29, 44, 326063)]},
#     {'title': 'LUBW gauge data: Weinheim-SKA', 'id': 866, 'uuid': 'ade15e99', 'variable__name': 'discharge', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 30, 16, 201908),
#      'split_ids': [866, 861], 'split_uuid': ['ade15e99', 'db8bf0f6'], 'split_embargo_end': [datetime.datetime(2023, 5, 6, 10, 30, 16, 201908), datetime.datetime(2023, 5, 6, 10, 30, 16, 235210)]},
#     {'title': 'LUBW gauge data: Weinheim', 'id': 388, 'uuid': '3d4a4b91', 'variable__name': 'river water level', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 29, 44, 417271),
#      'split_ids': [388, 389], 'split_uuid': ['3d4a4b91', '416351da'], 'split_embargo_end': [datetime.datetime(2023, 5, 6, 10, 29, 44, 417271), datetime.datetime(2023, 5, 6, 10, 29, 44, 451066)]},
#     {'title': 'LUBW gauge data: Weinheim-SKA', 'id': 868, 'uuid': '65222d16', 'variable__name': 'river water level', 'embargo': False, 'embargo_end': datetime.datetime(2023, 5, 6, 10, 30, 16, 335406),
#      'split_ids': [868, 869], 'split_uuid': ['65222d16', 'f634afb4'], 'split_embargo_end': [datetime.datetime(2023, 5, 6, 10, 30, 16, 335406), datetime.datetime(2023, 5, 6, 10, 30, 16, 368602)]},
# ]
