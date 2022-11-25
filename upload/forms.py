from django.contrib.gis import forms
from django.db.models import DateTimeField, CharField, FloatField
from django.db.models.functions import Cast, TruncSecond
# To upload the file to a model check the django documentation
# https://docs.djangoproject.com/en/1.11/topics/http/file-uploads/
#
from django.utils import translation

from vfw_home.fields import CustomOSMField, AutocompleteCharField
from vfw_home.widgets import TableSelect, CustomOSMWidget, AutocompleteCharWidget
from vfw_home.models import Entries, NmPersonsEntries, Persons, Variables, Datasources, DatasourceTypes, Datatypes, \
    TemporalScales, SpatialScales, Licenses


class MultiUploadFileForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'multiple': True,
        'id': 'select_data_button',
        'style': 'display: none',
        'onchange': "this.form.submit()",
        }), label='')


class UploadForm(forms.Form):

    class GeneralInfo(forms.Form):

        title = forms.CharField(label=translation.gettext('Title'), max_length=512,
                                help_text="A full title to describe the datasource as well as possible (max 512 chars). " \
                                          "E.g. Sap Flow - Hohes Holz - Tree 022")
        abstract = forms.CharField(label=translation.gettext('Abstract'), required=False,
                                   help_text="Full abstract of the datasource. The abstract should include all"
                                             "necessary information that is needed to fully understand the data.")
        version = forms.IntegerField(label=translation.gettext('Version'))
        partial = forms.BooleanField(label=translation.gettext('Part of greater dataset'), required=False)
        comment = forms.CharField(label=translation.gettext('Comment'), required=False)
        citation = AutocompleteCharField(label=translation.gettext('Citation'), required=False,
                                         widget=AutocompleteCharWidget(
                                             choices=Entries.objects.values_list('citation', flat=True)
                                             .order_by('citation').exclude(citation=None).distinct())
                                         )

        license = forms.ModelChoiceField(label=translation.gettext('License'),
                                         widget=TableSelect(item_attrs={'class': 'lic',
                                                                        'heading': ['Short Title', 'Title'],
                                                                        'title-col': 3,}),
                                     queryset=Licenses.objects.values_list('pk', 'short_title', 'title', 'summary').distinct())

        # TODO: Embargo end has to be set automatic two years from now
        embargo = forms.BooleanField(label=translation.gettext('Has Embargo'), required=False)
        # TODO: Publication and lastupdate have to be set to now.

    class GeoInfo(forms.Form):
        # TODO: Enable users to use another SRID (Transform before writng to db and show users transformed location on map)
        location = CustomOSMField(widget=CustomOSMWidget(attrs={'map_width': 600, 'map_height': 350}),
                                  help_text="The location as a POINT Geometry in unprojected WGS84 (EPSG: 4326)."
                                            "The location is primarily used to show all Entry objects on a map, "
                                            "or perform geo-searches. If the data-source needs to store more "
                                            "complex Geometries, you can use the ``geom`` argument.")

    class DataspecificInfo(forms.Form):

        file = forms.FileField()

        variable = forms.ModelChoiceField(
            label=translation.gettext('Variable'),
            widget=TableSelect(item_attrs={'class': 'var', 'heading': ['Name', 'Symbol', 'Unit', 'SI'],
                                           'title-col': 4, }),
            queryset=Variables.objects.values_list('pk', 'name', 'symbol', 'unit__name', 'unit__si', 'keyword')
            .distinct())


        Datatype = forms.ModelChoiceField(
            label=translation.gettext('Datatype'),
            widget=TableSelect(item_attrs={'class': 'foo', 'heading': ['Name',
                                                                       'Title', 'Description', 'Parent Name']}),
            queryset=Datatypes.objects.values_list('name', 'title', 'description', 'parent__name').order_by('name')
            .exclude(name__isnull=True).distinct())
    # datasource block
    class Datasource(forms.Form):

        # TODO: User shouldn't set the type (datasourcetypes), path. Find way to automate these!
        datasourcetype = forms.ModelChoiceField(queryset=DatasourceTypes
                                                .objects.values_list('name', 'title', 'description')
                                                .order_by('name').distinct())
        path = forms.ModelChoiceField(queryset=Datasources.objects.values_list('path').distinct())
        ###
        # args are Optional. If the I/O classes need further arguments, these can be stored as a JSON-serializable str.
        # Will be parsed into a dict and passed to the I/O functions as **kwargs.
        ###
        args = forms.ModelChoiceField(queryset=Datasources.objects.values_list('args', flat=True).distinct())
        ###
        # The encoding of the file or database representation of the actual data.
        # Defaults to ``'utf-8'``. Do only change if necessary.
        ###
        encoding = forms.ModelChoiceField(queryset=Datasources.objects.values_list('encoding', flat=True).distinct())
        name = forms.ModelChoiceField(label='Data Column Names',
                                      queryset=Datasources.objects.values_list('data_names', flat=True).distinct())

        Datatype = forms \
            .ModelChoiceField(label=translation.gettext('Datatype'),
                              widget=TableSelect(item_attrs={'class': 'foo',
                                                             'heading': ['Name', 'Title', 'Description',
                                                                         'Parent Name']}),
                              queryset=Datatypes.objects
                              .values_list('name', 'title', 'description', 'parent__name')
                              .order_by('name').exclude(name__isnull=True).distinct()
                              )

        ###
        # The scales should be read from the data automatic
        ###
        TempScale = forms \
            .ModelChoiceField(label=translation.gettext('Temporal Scale'),
                              widget=TableSelect(item_attrs={'class': 'foo',
                                                             'heading': ['Start Time', 'End Time', 'Resolution',
                                                                         'Support']}),
                              queryset=TemporalScales.objects
                              .annotate(
                                  start_time=Cast(TruncSecond('observation_start', DateTimeField()), CharField()),
                                  end_time=Cast(TruncSecond('observation_end', DateTimeField()), CharField()),
                                  sup=Cast('support', FloatField()))
                              .values_list('id', 'start_time', 'end_time', 'resolution', 'sup')
                              .order_by('start_time').distinct()
                              )
        # TODO: Use other Widget. Extent should be shown on a map.
        SpatialScale = forms \
            .ModelChoiceField(label=translation.gettext('Spatial Scale'),
                              widget=TableSelect(item_attrs={'class': 'foo',
                                                             'heading': ['Resolution', 'Extent', 'Support']}),
                              queryset=SpatialScales.objects.values_list('resolution', 'extent', 'support')
                              .order_by('resolution').distinct()
                              )

    class Add_Scales(forms.Form):
        pass

    # variables block
    class Variable(forms.Form):
        Variable = forms\
            .ModelChoiceField(label=translation.gettext('Variable'),
                              widget=TableSelect(item_attrs={'class': 'foo',
                                                             'heading': ['Name', 'SI', 'Unit symbol', 'Unit name'],
                                                             'data-forsearch': ['Keywords']}),
                              queryset=Variables.objects
                              .values_list('id', 'name', 'unit__si', 'unit__symbol', 'unit__name', 'keyword__full_path')
                              .order_by('name').exclude(name__isnull=True).distinct()
                              )

    class Add_Variable(forms.Form):

        name = forms.CharField(max_length=64)
        symbol = forms.CharField(max_length=12)
        unit = forms.ModelChoiceField(widget=forms.Select(),
                                      queryset=Entries.objects.values_list('variable__unit__name', flat=True)
                                      .order_by('variable__name')
                                      .exclude(variable__name__isnull=True).distinct())

    class Add_Unit(forms.Form):
        name = forms.CharField(max_length=64)
        symbol = forms.CharField(max_length=12)
        symbol = forms.CharField(max_length=64)



class EntriesForm(forms.ModelForm):

    class Meta:
        model = Entries
        fields = ('title', 'variable', 'abstract', 'comment', 'geom', 'location', 'version', 'embargo', 'publication',
                  'citation', 'license',
                  )
        widgets = {
            'location': forms.TextInput(),
        }


class PersonsForm(forms.ModelForm):

    class Meta:
        model = Persons
        fields = ('first_name', 'last_name', 'organisation_name', 'affiliation', 'attribution')

