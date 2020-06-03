# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models


class DatasourceTypes(models.Model):
    name = models.CharField(max_length=64)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'datasource_types'

    def __str__(self):
        return '%s data source <ID=%d>' % (self.name, self.id)


class Datasources(models.Model):
    type = models.ForeignKey(DatasourceTypes, models.DO_NOTHING)
    path = models.TextField()
    args = models.TextField(blank=True, null=True)

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'datasources'

    def __str__(self):
        return "%s data source at %s <ID=%d>" % (self.type.name, self.path, self.id)


class Details(models.Model):
    """
    Used for the advanced Filter.
    """
    entry = models.ForeignKey('Entries', models.DO_NOTHING, blank=True, null=True)
    key = models.CharField(max_length=20)
    stem = models.CharField(max_length=20)
    value = models.TextField()

    column_dict_adv = {'value': 'details_text'}
    menu_name_adv = 'Details'
    path = 'details'
    filter_type = {'value': 'text'}

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'details'
        unique_together = (('entry', 'stem'),)

    def __str__(self):
        return "%s = %s" % (self.key, self.value)


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
    title = models.CharField(max_length=512)
    abstract = models.TextField(blank=True, null=True)
    external_id = models.TextField(blank=True, null=True)
    location = models.PointField(srid=0)
    geom = models.GeometryField(srid=0, blank=True, null=True)
    creation = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    version = models.IntegerField()
    latest_version = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    license = models.ForeignKey('Licenses', models.DO_NOTHING, blank=True, null=True)
    variable = models.ForeignKey('Variables', models.DO_NOTHING)
    datasource = models.ForeignKey(Datasources, models.DO_NOTHING, blank=True, null=True)
    embargo = models.BooleanField()
    embargo_end = models.DateTimeField(blank=True, null=True)
    publication = models.DateTimeField(blank=True, null=True)
    lastupdate = models.DateTimeField(db_column='lastUpdate', blank=True, null=True)  # Field name made lowercase.

    column_dict = {'creation': 'creation/start', 'end': 'end of measurement', 'embargo': 'embargo'}
    column_dict_adv = {'version': 'version'}
    menu_name = 'Entries'
    path = ''
    filter_type = {'creation': 'date', 'end': 'date', 'embargo': 'bool'}

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'entries'

    def __str__(self):
        return "<ID=%d %s [%s] >" % (self.id, self.title[:20], self.variable.name)


class EntrygroupTypes(models.Model):
    """
    Filter (advanced) only entrygroup 'project'
    """
    name = models.CharField(max_length=40)
    description = models.TextField()

    column_dict = {'creation': 'creation/start', 'end': 'end of measurement', 'embargo': 'embargo'}
    column_dict_adv = {'version': 'version'}
    menu_name = 'Entries'
    path = ''

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'entrygroup_types'

    def __str__(self):
        return "%s <ID=%d>" % (self.name, self.id)


class Entrygroups(models.Model):
    type = models.ForeignKey(EntrygroupTypes, models.DO_NOTHING)
    title = models.CharField(max_length=40, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'entrygroups'

    def __str__(self):
        return "%s%s <ID=%d>" % (self.type.name, " %s" % self.title[:20] if self.title is not None else '', self.id)


class GenericGeometryData(models.Model):
    entry = models.ForeignKey(Entries, models.DO_NOTHING, primary_key=True)
    index = models.IntegerField()
    geom = models.GeometryField(srid=0)
    srid = models.IntegerField(blank=True, null=True)

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'geneic_geometry_data'
        unique_together = (('entry', 'index'),)


class Generic1DData(models.Model):
    entry = models.ForeignKey(Entries, models.DO_NOTHING, primary_key=True)
    index = models.DecimalField(max_digits=65535, decimal_places=65535)
    value = models.DecimalField(max_digits=65535, decimal_places=65535)
    precision = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'generic_1d_data'
        unique_together = (('entry', 'index'),)


class Generic2DData(models.Model):
    entry = models.ForeignKey(Entries, models.DO_NOTHING, primary_key=True)
    index = models.DecimalField(max_digits=65535, decimal_places=65535)
    value1 = models.DecimalField(max_digits=65535, decimal_places=65535)
    value2 = models.DecimalField(max_digits=65535, decimal_places=65535)
    precision1 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    precision2 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'generic_2d_data'
        unique_together = (('entry', 'index'),)


class GeomTimeseries(models.Model):
    entry = models.ForeignKey(Entries, models.DO_NOTHING, primary_key=True)
    tstamp = models.DateTimeField()
    geom = models.GeometryField(srid=0)
    srid = models.IntegerField(blank=True, null=True)

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'geom_timeseries'
        unique_together = (('entry', 'tstamp'),)


class Keywords(models.Model):
    """
    Used for advanced filter. Shows a complete list and the 10 most common (but not the ones every dataset has)
    """
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    value = models.CharField(max_length=1024)
    uuid = models.CharField(unique=True, max_length=64, blank=True, null=True)
    full_path = models.TextField(blank=True, null=True)

    class Meta:
        # app_label = 'mcdev'
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
        return "%s <ID=%d>" % (self.full_path, self.id)


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

    column_dict = {'commercial_use': 'Commercial use allowed'}  # menu text
    column_dict_adv = {'commercial_use': 'Commercial use allowed'}
    menu_name = 'Licenses'
    path = 'license'
    filter_type = {'commercial_use': 'bool'}

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'licenses'

    def __str__(self):
        return "%s <ID=%d>" % (self.title, self.id)


class NmEntrygroups(models.Model):
    entry = models.ForeignKey(Entries, models.DO_NOTHING, primary_key=True)
    group = models.ForeignKey(Entrygroups, models.DO_NOTHING)

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'nm_entrygroups'
        unique_together = (('entry', 'group'),)


class NmKeywordsEntries(models.Model):
    keyword = models.ForeignKey(Keywords, models.DO_NOTHING, primary_key=True)
    entry = models.ForeignKey(Entries, models.DO_NOTHING)
    alias = models.CharField(max_length=1024, blank=True, null=True)
    associated_value = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'nm_keywords_entries'
        unique_together = (('keyword', 'entry'),)

    def __str__(self):
        return "<Entry ID=%d> tagged %s" % (self.entry.id, self.keyword.value)


class NmPersonsEntries(models.Model):
    person = models.ForeignKey('Persons', models.DO_NOTHING, primary_key=True)
    entry = models.ForeignKey(Entries, models.DO_NOTHING)
    relationship_type = models.ForeignKey('PersonRoles', models.DO_NOTHING)
    order = models.IntegerField()

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'nm_persons_entries'
        unique_together = (('person', 'entry'),)

    def __str__(self):
        return '%s <ID=%d> as %s for Entry <ID=%d>' % (
        self.person.full_name, self.person.id, self.role.name, self.entry.id)


class PersonRoles(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'person_roles'

    def __str__(self):
        return "%s <ID=%d>" % (self.name, self.id)


class Persons(models.Model):
    """
    Filter for persons in advanced filter.
    """
    first_name = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=128)
    affiliation = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'persons'

    def __str__(self):
        return "%s <ID=%d>" % (self.full_name, self.id)


class Timeseries(models.Model):
    entry = models.ForeignKey(Entries, models.DO_NOTHING, primary_key=True)
    tstamp = models.DateTimeField()
    value = models.DecimalField(max_digits=65535, decimal_places=65535)
    precision = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'timeseries'
        unique_together = (('entry', 'tstamp'),)


class Timeseries2D(models.Model):
    entry = models.ForeignKey(Entries, models.DO_NOTHING, primary_key=True)
    tstamp = models.DateTimeField()
    value1 = models.DecimalField(max_digits=65535, decimal_places=65535)
    value2 = models.DecimalField(max_digits=65535, decimal_places=65535)
    precision1 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    precision2 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'timeseries_2d'
        unique_together = (('entry', 'tstamp'),)


class Units(models.Model):
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=12)
    si = models.TextField(blank=True, null=True)

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'units'

    def __str__(self):
        return "%s <ID=%d>" % (self.name, self.id)


class Variables(models.Model):
    """
    Names of the dataset. Used in the Filter menu.
    """
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=12)
    unit = models.ForeignKey(Units, models.DO_NOTHING)
    keyword = models.ForeignKey(Keywords, models.DO_NOTHING, blank=True, null=True)

    column_dict = {'name': 'Name'}  # menu text
    column_dict_adv = {'name': 'Name'}
    menu_name = 'Variables'
    path = 'variable'
    # print('\033[31m' + 'path: \033[0m', path)

    class Meta:
        # app_label = 'mcdev'
        managed = False
        db_table = 'variables'

    def __str__(self):
        return "%s [%s] <ID=%d>" % (self.name, self.unit.symbol, self.id)


class BasicFilter:
    """
    Class to collect relevant information for filter
    """

    embargo = Entries.objects.using('mcdev').values_list('embargo', flat=True).distinct()
    creation = Entries.objects.using('mcdev').values_list('creation', flat=True).distinct()
    end = Entries.objects.using('mcdev').values_list('end', flat=True).distinct()
    licenses = Licenses.objects.using('mcdev').values_list('commercial_use', flat=True).distinct()
    variables = Variables.objects.using('mcdev').values_list('name', flat=True).distinct()

    # menu_entries = {'Embargo': embargo, 'Creation': creation, 'End': end, 'License': licenses,
    #                 'Variables': variables}
    # menu_entries = [variables]
    menu_entries = [Variables]#, Entries]#, Licenses]

    print('________')
    # a = Entries.objects.using('mcdev').filter(variable__name='sap flow')
    # a = Entries.objects.using('mcdev').filter(nmpersonsentries__person__first_name='Inst.')
    # print(a)
    # class Meta:
    #     abstract = True

class AdvancedFilter(BasicFilter):
    """
    Class to collect relevant information for advanced filter
    """

