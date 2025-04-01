# =================================================================
#
# Authors: Marcus Strobl <marcus.strobl@kit.edu>
# Contributors: Safa Bouguezzi <safa.bouguezzi@kit.edu>, Kaoutar Boussaoud <kaoutar.boussaourd@kit.edu>
#
# Copyright (c) 2024 Marcus Strobl
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import csv
import datetime
import json
import re
import sys
from http.cookiejar import CookieJar

import redis
import requests
from django.contrib.gis.db.models.aggregates import Extent
from django.core.cache import cache
from django.core.exceptions import EmptyResultSet, FieldError
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.timezone import make_aware


import matplotlib as mpl
import urllib
from collections import defaultdict
from django.conf import settings
from django.contrib.auth import logout
from django.http import StreamingHttpResponse, QueryDict
from django.http.response import JsonResponse, HttpResponse, Http404, FileResponse
from django.shortcuts import redirect, render
from django.utils import translation, timezone
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.serializers import serialize

from author_manage.views import MyResourcesView
from heron.settings import LOCAL_GEOSERVER, DEMO_VAR, DATA_DIR, DATABASES

from .Geoserver.geoserver_layer import create_layer, has_layer, delete_layer, test_geoserver_env, get_layer, verify_layer

from wps_gui.models import WpsResults
from .Figure.Fig_obj import FigObject
from .Geoserver.checks import check_geoserver_layers
from .Figure.data_tools import DataTypes, get_accessible_data, collect_selection, has_data, get_split_groups
from .utilities.delineator import delineate
from .Forms.forms import QuickFilterForm
from .Figure.data_obj import DataObject
from .utilities.utilities import human_readable_bool, has_pending_embargo, read_data, expressive_layer_name, get_dataset, \
    get_paginatorpage, regex_patterns, is_coord, get_cache, check_data_consistency, clean_database_name, raise_logging_exception, logger

from django.contrib.gis.geos import Polygon, GEOSGeometry
from .utilities.query_functions import get_bbox_from_data

from .utilities.filters import NMPersonsFilter
from .models import Entries, NmEntrygroups, Entrygroups, Timeseries, Timeseries_1D, Locations, Variables, TemporalScales


from pathlib import Path
from datetime import timedelta

from time import time


mpl.use('Agg')

"""

"""


check_data_consistency()



"""
# IMPORTANT:
# From Django doc about session: If SESSION_EXPIRE_AT_BROWSER_CLOSE is set to True, Django will use browser-length
# cookies – cookies that expire as soon as the user closes their browser. Use this if you want people to have to log in
# every time they open a browser.
"""



class HomeView(TemplateView):
    """
    Template View to bring the necessary variables for the startup to the template.
    """
    template_name = 'vfw_home/home.html'
    Database_Name = clean_database_name()
    # Configuration for data layers and workspace
    DATA_LAYER = 'devel'
    AREAL_DATA_LAYER = 'areal_devel'
    MERIT_RIVER_LAYER = ['merit_river_test', 'merit_river']
    MERIT_RIVER_IDS = ['merit_river_simple', 'merit_river_simple']
    MERIT_CATCHMENT_LAYER = ['merit_catchment', 'merit_catchment']
    MERIT_CATCHMENT_COARSE_LAYER = ['merit_catchment_coarse', 'merit_catchment_coarse']
    DATA_EXT = [645336.034469495, 6395474.75106861, 666358.204722283, 6416613.20733359]

    STORE = Database_Name
    WORKSPACE = Database_Name

    UNLOCKED_EMBARGO = []
    if not getattr(settings, 'TEST_MODE', False):  # Only run in non-test mode

        check_geoserver_layers(STORE, WORKSPACE,
                            [MERIT_RIVER_LAYER, MERIT_RIVER_IDS, MERIT_CATCHMENT_LAYER, MERIT_CATCHMENT_COARSE_LAYER])


    def __set_layer_name(self):
        """
        Set name for layer in geoserver according to username or as admin_layer.
        """
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                self.DATA_LAYER = 'admin_layer'
                self.AREAL_DATA_LAYER = 'admin_areal_layer'
            else:
                self.DATA_LAYER = expressive_layer_name(self.request.user)
                self.AREAL_DATA_LAYER = f"{expressive_layer_name(self.request.user)}_areal"

    def get_context_data(self, **kwargs):
        """
        Collect data needed for startup of V-FOR-WaTer Portal home.
        """
        self.__set_layer_name()
        endpoint = self.request.path

        try:
            unblocked_ids = self.request.session.get('datasets', [])
            if not unblocked_ids:
                self.request.session['datasets'] = []
        except Exception as e:

            raise_logging_exception(e, endpoint, None)
            unblocked_ids = []
            self.request.session['datasets'] = []

        try:
            verify_layer(request=self.request, datastore=self.STORE, workspace=self.WORKSPACE, filename=self.DATA_LAYER)
            print(f"Calling verify_layer with {self.DATA_LAYER}")

            verify_layer(request=self.request, datastore=self.STORE, workspace=self.WORKSPACE, filename=self.AREAL_DATA_LAYER, layertype='areal_data')

            # verify_layer(self.request, self.DATA_LAYER, self.STORE, self.WORKSPACE) 
            print(f"Calling verify_layer with {self.AREAL_DATA_LAYER}")
            # verify_layer(self.request, self.AREAL_DATA_LAYER, self.STORE, self.WORKSPACE,  layertype='areal_data')

        except Exception as e:
            raise_logging_exception(e, endpoint, None)
            self.DATA_LAYER = 'Error: Found no geoserver!'
            self.AREAL_DATA_LAYER = 'Error: Found no geoserver!'
            print(f'Still no geoserver: {e}')

        self.DATA_EXT = get_bbox_from_data()
        context = quick_filter_defaults(self)
       

        return {
            'dataExt': self.DATA_EXT,
            'data_layer': self.DATA_LAYER,
            'areal_data_layer': self.AREAL_DATA_LAYER,
            'messages': messages.get_messages(self.request),
            'unblocked_ids': unblocked_ids,
            **context
        }
        
class TestView(View):

    def get(self, request):
        print('request: ', request)
        return JsonResponse({'answer': 'läuft'})


class Echo:
    """
    An object that implements just the write method of the file-like interface.
    """

    def write(self, value):
        """
        Write the value by returning it, instead of storing in a buffer.
        """
        return value


class DatasetDownloadView(TemplateView):
    """
    Handles dataset downloads in various formats (CSV, GeoJSON, Shapefile, XML).
    """

    def get(self, request):
        """

        :param request:
        :type request:
        :return:
        :rtype:
        """
    
        store = HomeView.STORE  # 'new_vforwater_gis'
        workspace = HomeView.WORKSPACE  # 'CAOS_update'
        test_geoserver_env(store, workspace)
        endpoint = request.path

        format_mapping = {
            'csv': self.handle_csv,
            'geojson': self.handle_geojson,
            'shp': self.handle_shapefile,
            'xml': self.handle_xml
        }


        for fmt, handler in format_mapping.items():
            if fmt in request.GET:
                try:
                    return handler(request, store, workspace)
                except Exception as e:
                    additional_message = f"Error processing {fmt} request on endpoint {endpoint}: {e}"
                    raise_logging_exception(e, endpoint, additional_message)
                    return HttpResponseServerError(f"An error occurred while processing your request: {e}")

        additional_message = f"Unsupported or missing file format on endpoint {endpoint}."
        raise_logging_exception(e, endpoint, additional_message)
        return HttpResponseBadRequest("Unsupported or missing file format.")

       

    def handle_csv(self, request, *args):
        s_id =  request.GET.get('csv')

        accessible_data = get_accessible_data(request, s_id)
        error_list = accessible_data['blocked']
        data = accessible_data.get('open', [])

        if not data:
            try:
                raise ValueError("No accessible data found.")  # Step 1: This raises an error
            except Exception as e:
                additional_message = f"No accessible data found for CSV request with dataset ID {s_id}."
                raise_logging_exception(e, endpoint, additional_message)

     

        rows = get_dataset(data[0])
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)

        response = StreamingHttpResponse(
            (writer.writerow(row) for row in rows),
            content_type="text/csv"
        )
        response['Content-Disposition'] = 'attachment; filename="dataset.csv"'
        return response

            
    def handle_geojson(self, request, *args):
        s_id =  request.GET.get('geojson')

        accessible_data = get_accessible_data(request, s_id)
        error_list = accessible_data['blocked']
        data = accessible_data.get('open', [])

        if not data:
            try:
                raise ValueError("No accessible data found.")  # Step 1: This raises an error
            except Exception as e:
                additional_message = f"No accessible data found for geojson request with dataset ID {s_id}."
                raise_logging_exception(e, endpoint, additional_message)


        geojson_data = serialize("geojson", Locations.objects.filter(id = data[0]) , geometry_field="point_location", fields=["name"])

        response = HttpResponse(json.dumps(geojson_data), content_type="application/json")
        response['Content-Disposition'] = 'attachment; filename="somefilename.geojson"'
        return response


    def handle_shapefile(self, request, *args):
        s_id = request.GET.get('shp')

        accessible_data = get_accessible_data(request, s_id)
        error_list = accessible_data['blocked']
        data = accessible_data.get('open', [])

        if not data:
            try:
                raise ValueError("No accessible data found.")  # Step 1: This raises an error
            except Exception as e:
                additional_message = f"No accessible data found for ShapeFile request with dataset ID {s_id}."
                raise_logging_exception(e, endpoint, additional_message)


        layer_name = f'shp_{request.user}_{request.user.id}_{s_id}'
        srid = 4326

        create_layer(request, layer_name, store, workspace, s_id)

        try:
            url = (
                f"{LOCAL_GEOSERVER}/{workspace}/ows?service=wfs&version=1.0.0&"
                f"request=GetFeature&typeName={workspace}:{layer_name}&"
                f"outputFormat=shape-zip&srsname=EPSG:{srid}"
            )
            response = requests.get(url)
            pzfile = PyZip().from_bytes(response.content)

            try:
                del pzfile['wfsrequest.txt']
            except Exception as e:
                raise_logging_exception(e, endpoint, None)
                pass

        except Exception as e:
            additional_message = f"Error fetching Shapefile from GeoServer for dataset ID {s_id}: {e}"
            raise_logging_exception(e, endpoint, additional_message)
            raise

        finally:
            delete_layer(layer_name, store, workspace)

        return HttpResponse(pzfile.to_bytes(), content_type='application/zip')

    def handle_xml(self, request, *args):
        id = request.GET.get('xml')

        accessible_data = get_accessible_data(request, s_id)
        error_list = accessible_data['blocked']
        data = accessible_data.get('open', [])

        if not data:
            try:
                raise ValueError("No accessible data found.")  # Step 1: This raises an error
            except Exception as e:
                additional_message = f"No accessible data found for xml request with dataset ID {s_id}."
                raise_logging_exception(e, endpoint, additional_message)

        try:

            opener = urllib.request.build_opener(
                urllib.request.HTTPBasicAuthHandler(password_manager),
                
                urllib.request.HTTPCookieProcessor(cookie_jar))
            urllib.request.install_opener(opener)

            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)

            

            body = response.read()
            

        except Exception as e:

            additional_message = f"Error fetching XML for dataset ID {s_id}: {e}"
            raise_logging_exception(e, endpoint, additional_message)
            delete_layer(layer_name, store, workspace)
            raise
            
        return HttpResponse(body.decode('utf-8'), content_type="application/xml")



class LoginView(View):
    """

    """

    def post(self, request):
        """

        :param request:
        :type request:
        :return:
        :rtype:
        """

        if 'watts_rsp.auth.WattsBackend' in settings.AUTHENTICATION_BACKENDS:
            logger.debug('Redirect to home/rsp/login/init...')
            return redirect('vfw_home:watts_rsp:login_init')
        elif settings.DEBUG:  # default django login
            return redirect('vfw_home:login')
        else:
            raise Http404

    def dispatch(self, request, *args, **kwargs):
        """
        When clicked on login, this is the first(?) function to access.
        If not user.is_authenticated, next function is post and redirect to watts
        (django-watts-rsp/auth.py->WattsBackend->redirect) or django login.

        :param request:
        :type request:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        if not request.user.is_authenticated:
            logger.debug('The user is not authenticated!')
        else:
            logger.debug(f'{request.user.username} logged in as')

        return super().dispatch(request, *args, **kwargs)



class LogoutView(View):
    def logout_user(self, request):
        """
        Logs out the user and clears their session.
        
        :param request: The HTTP request object
        :type request: HttpRequest
        """
        username = request.user.username
        # print(f'Logging out: {username}')  # Debug print
        # print(f'Logging out: (auth status: {request.user.is_authenticated})')  # Debug print

        logout(request)
        logger.debug(f'{username} logged out (auth status: {request.user.is_authenticated})')


    def post(self, request):
        """
        Handles POST requests to log out the user.
        
        :param request: The HTTP request object
        :type request: HttpRequest
        :return: A redirect to the home page
        :rtype: HttpResponseRedirect
        """
        self.logout_user(request)
        return redirect('vfw_home:home')



class DevLoginView(TemplateView):

    def get(self, request):
        context = {}
        return render(request, 'home/login.html', {'context': context})


class Legals(TemplateView):

    def get(self, request):
        return render(request, 'vfw_home/legals.html')


class PrivacyPolicy(TemplateView):

    def get(self, request):
        return render(request, 'vfw_home/privacypolicy.html')



class HelpView(TemplateView):
    template_name = 'home/help.html'
    
    def get(self, request):
        help_file_path = Path(settings.BASE_DIR) / 'USERHELP.md'
        
        # Using a context manager to read file lines
        with open(help_file_path, 'r') as f:
            # Creating a dictionary comprehension to store lines with indexes
            context = {i: line for i, line in enumerate(f)}
        
        # Returning the rendered template with context
        return render(request, self.template_name, {'context': context})



class ToggleLanguageView(View):
    """View to toggle the website's language and update the language cookie."""

    @staticmethod
    def post(request):
        """
        Toggle the language of the website between 'de' and 'en-gb',
        set the session and cookie to reflect the change, and redirect to the homepage.

        :param request: Django HttpRequest object
        :return: HttpResponseRedirect to the homepage
        """
        endpoint = request.path
        try:
            current_language = translation.get_language()
            logger.debug(f"Current language: {current_language}")

            new_language = "de" if current_language in {"en-gb", "en-us"} else "en-gb"

            translation.activate(new_language)

            if hasattr(request, "session"):
                request.session[settings.LANGUAGE_COOKIE_NAME] = new_language

            logger.debug(f"new language: {translation.get_language()}")
            logger.debug(f'translation test: {translation.gettext("help")}')

            response = redirect(f"{DEMO_VAR}/")

            response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            request.session[settings.LANGUAGE_COOKIE_NAME],)

            return response

        except Exception as e:
            additional_message = "Error while toggling language"
            raise_logging_exception(e, endpoint, additional_message)
            return redirect(f"{DEMO_VAR}/")


class FailedLoginView(View):
    """
    View for handling failed login attempts.
    """
    @staticmethod
    def get(self, request):
        """
        Handles GET requests and displays a login failed message.
        
        :param request: The HTTP request object
        :type request: HttpRequest
        :return: A redirect to the home page
        :rtype: HttpResponseRedirect
        """

        messages.warning(request, 'Login failed.')
        return redirect('vfw_home:home')


class GeoserverView(View):
    """
    Build URL to get layers from Geoserver
    """

    @staticmethod
    def get(request, service, layer, bbox, srid):
        """

        :param service: e.g. wfs
        :type service: str
        :param layer: name of the requested layer
        :type layer: str
        :param bbox: style e.g. -976.82,530.56,2741.65,702.43
        :type bbox: str
        :param srid:
        :type srid: int
        :return:
        :rtype:
        """
        # wfsLayerName = 'new_ID_as_identifier_update'
        # wfsLayerName = layer
        work_space_name = HomeView.WORKSPACE  # 'CAOS_update'
        # url = LOCAL_GEOSERVER + '/' + work_space_name + '/ows?service=' + service + \
        #       '&version=1.0.0&request=GetFeature&typeName=' + work_space_name + ':' + layer + \
        #       '&outputFormat=application%2Fjson&srsname=EPSG:' + srid + '&bbox=' + bbox + ',EPSG:' + srid
        url = '{0}/{1}/ows?service={2}&version=1.0.0&request=GetFeature&typeName={1}:{3}&outputFormat=application%2' \
              'Fjson&srsname=EPSG:{4}&bbox={5},EPSG:{6}'.format(LOCAL_GEOSERVER, work_space_name, service, layer,
                                                                srid, bbox, srid)
        request_url = urllib.request.Request(url)
        response = urllib.request.urlopen(request_url)

        return HttpResponse(response.read().decode('utf-8'))


class PreviewPlotView(View):
    """
    Class-based view to handle preview plot requests.
    """

    def get(self, request, *args, **kwargs):

        endpoint = request.path

        try:
            # Step 1: Process webID
            webID = request.GET.get('preview')
            if not webID:
                logger.error("No 'preview' parameter provided in the request.")
                return JsonResponse({'error': "Missing 'preview' parameter."})

            entriesID, parts = self._process_webID(webID)

            # Step 2: Validate accessible data
            if len(parts) > 1:
                accessible_data = get_accessible_data(request, [parts[1]])
                error_list = accessible_data['blocked']
                data = accessible_data.get('open', [])

                if not data:
                    logger.warning(f"No accessible data found for parts: {parts}")
                    return JsonResponse({'warning': translation.gettext(
                        'No plot available. <br/>First access to this dataset is needed.')})

            else:
                additional_message = f"Invalid 'parts' structure: {parts}"
                raise_logging_exception(None, endpoint, additional_message)
                return JsonResponse({'error': "Invalid 'parts' structure parsed from 'webID'."})

        except Exception as e:
            additional_message = "Error during processing of 'webID'."
            raise_logging_exception(e, endpoint, additional_message)
            return JsonResponse({'error': f"An unexpected error occurred: {str(e)}"})


        full_res = False
        plot_size = [700, 500]
        date = self._get_date_range(request)

        
        cache_obj = self._initialize_cache(webID, plot_size, date)
        cache_obj, img = get_cache(cache_obj)

        if not cache_obj['in_cache']:
            try:
                dataset = self._get_dataset(webID, entriesID, date)
            except Exception as e:
                additional_message = "Error while constructing the dataset."
                raise_logging_exception(e, endpoint, additional_message)
                raise Http404

            try:
                plot = FigObject(dataset, plot_size)
                img = plot.get_plot()
            except Exception as e:
                additional_message = "Error while generating the plot."
                raise_logging_exception(e, endpoint, additional_message)
                raise Http404

        return JsonResponse(img)


    def _process_webID(self, webID):
        """
        Process the 'webID' parameter and extract its components.

        :param webID: The webID from the request.
        :return: A tuple of entriesID and parts.
        """
        entriesID = webID
        parts = []

        if webID.startswith('db['):
            parts = webID[0:-1].split('[')
            webID = [f'db{id.strip()}' for id in parts[1].split(',')]
        elif webID.startswith('db'):
            parts = [0, webID[2:]]
            entriesID = webID[2:]
        else:
            logger.warning(f"Unexpected ID format encountered: {webID} (type: {type(webID)})")
            raise ValueError(f"Unhandled ID format: {webID}")

        return entriesID, parts

    def _get_date_range(self, request):
        """
        Extract the date range from the request.

        :param request: The HTTP request containing startdate and enddate.
        :return: A list containing the start and end dates, or None.
        """
        startdate = request.GET.get('startdate')
        enddate = request.GET.get('enddate')

        if startdate and startdate != 'None':
            return [
                make_aware(datetime.datetime.strptime(startdate, '%Y-%m-%d')),
                make_aware(datetime.datetime.strptime(enddate, '%Y-%m-%d'))
            ]
        return None

    def _initialize_cache(self, webID, plot_size, date):
        """
        Initialize the cache object for the plot.

        :param webID: The webID parameter.
        :param plot_size: The size of the plot.
        :param date: The date range for the plot.
        :return: A dictionary representing the cache object.
        """
        cache_name = f"plot_b{webID}{plot_size}{date}"
        return {
            'use_redis': True,
            'redis': redis.StrictRedis(),
            'in_cache': False,
            'name': cache_name
        }

    def _get_dataset(self, webID, entriesID, date):
        """
        Construct the dataset based on the webID and date range.

        :param webID: The webID parameter.
        :param entriesID: Extracted entries ID.
        :param date: The date range for the dataset.
        :return: A list of dataset objects.
        """
        dataset = []

        if isinstance(webID, list):
            for entry in webID:
                if has_data(entry[2:]):
                    dataset.append(DataObject(entry, date))
                else:
                    logger.warning(f"No data available for dataset with entries ID: {entry}")
        else:
            if has_data(entriesID):
                if int(entriesID) not in cache.get('ids_data_on_path'):
                    dataset = DataObject(webID, date)
                else:
                    logger.warning("Data on path not handled. Check if raster or netCDF.")
                    raise ValueError(f"Plot for entries ID {webID} needs implementation.")
            else:
                logger.warning(f"No data available for dataset with entries ID: {webID}")
                raise ValueError(f"No data available for dataset with entries ID: {webID}")

        return dataset



class ShortInfoPaginationView(View):
    """
    View to return only a little metadata and give access to more details.
    """

    def get(self, request):

        endpoint = request.path

        try:
            datasets, field, field_name = self.get_initial_data(request)
            entries_list = self.get_entries_list(datasets, field)
            accessible_ids = self.get_accessible_ids(request, datasets)

            if datasets:
                entries_list = self.process_grouped_entries(datasets, entries_list)
            
            current_page = self.paginate_entries(request, entries_list, 5)
            entries = self.build_entries_dict(current_page, field_name, accessible_ids)
            
            return render(request, 'vfw_home/mapmodal_entrieslist.html', {
                'entries_page': entries,
                'data_sets': datasets,
                'current_page': current_page
            })

        except Exception as e:
            additional_message = f'Exception while getting short info pagination: {e}'
            raise_logging_exception(e, endpoint, additional_message)
            raise Http404

    def get_initial_data(self, request):
        """
        Retrieve initial data from request.
        """
        datasets = json.loads(request.GET.get('datasets', '[]'))
        if isinstance(datasets, str):
            datasets = [int(datasets)]
        
        field = [
            'title', 'id', 'uuid', 'variable__name', 'embargo', 'embargo_end'
        ]
        field_name = {
            'title': 'Title', 'variable__name': 'Variable name', 'id': 'ID', 'uuid': 'UUID',
            'embargo': 'Embargo', 'has_access': 'has_access', 'embargo_end': 'embargo_end'
        }
        
        return datasets, field, field_name

    def get_entries_list(self, datasets, field):
        """
        Retrieve the list of entries based on the provided datasets and fields.
        """
        if datasets:
            return list(Entries.objects.values(*field).filter(pk__in=datasets).order_by('variable__name', 'title', 'id'))
        return list(Entries.objects.values(*field).order_by('variable__name', 'title', 'id'))

    def get_accessible_ids(self, request, datasets):
        """
        Get the accessible dataset IDs for the user.
        """
        if datasets:
            accessible_data = get_accessible_data(request, datasets)
            return accessible_data.get('open', [])
        return []

    def process_grouped_entries(self, datasets, entries_list):
        """
        Process grouped entries by handling split data.
        """
        grouped_dict = get_split_groups(datasets)
        entries_id_map = {d['id']: idx for idx, d in enumerate(entries_list)}

        append_dict, delete_list = self.build_append_delete_dicts(grouped_dict)
        delete_indices = [entries_id_map[i] for i in delete_list]

        for target, split_list in append_dict.items():
            for dataset in split_list:
                for k, v in entries_list[entries_id_map[target]].items():
                    if v != entries_list[entries_id_map[dataset]][k]:
                        entries_list[entries_id_map[target]][k] = [entries_list[entries_id_map[target]][k], entries_list[entries_id_map[dataset]][k]]
        
        for delete_id in sorted(delete_indices, reverse=True):
            entries_list.remove(entries_list[delete_id])
        
        return entries_list

    def build_append_delete_dicts(self, grouped_dict):
        """
        Build dictionaries for appending and deleting grouped entries.
        """
        append_dict = {}
        delete_list = []
        for k, v in grouped_dict.items():
            append_dict[v[0]] = v[1:]
            delete_list.extend(v[1:])
        return append_dict, delete_list

    def paginate_entries(self, request, entries_list, per_page):
        """
        Paginate the entries list.
        """
        page_number = request.GET.get('page', 1)
        paginator = Paginator(entries_list, per_page)
        return paginator.get_page(page_number)

    def build_entries_dict(self, current_page, field_name, accessible_ids):
        """
        Build a dictionary of entries for the current page.
        """
        naive_today = timezone.make_naive(timezone.now())
        newdict = defaultdict(list)

        for d in current_page:
            for key, val in d.items():
                if key != 'embargo_end':
                    newdict[translation.gettext(field_name[key])].append(val)
                else:
                    if not has_pending_embargo(d['embargo'], val) or d['id'] in accessible_ids:
                        newdict['has_access'].append({'access': True, 'ssid': d['id']})
                    else:
                        newdict['has_access'].append({'access': False, 'ssid': d['id']})
        
        return dict(newdict.items())




class ShowInfoView(View):


    """
    Handles requests to collect metadata for preview on a map and sidebar selection.
    """

    def get(self, request, *args, **kwargs):

        endpoint = request.path
        webID = request.GET.get('show_info')
        if not webID:
            logger.error("No 'show_info' parameter provided.")
            return JsonResponse({'error': "Missing 'show_info' parameter."})

        if webID.startswith('wps'):
            return self.handle_wps(webID)
        elif webID.startswith('db'):
            ids = webID[2:]
        else:
            ids = webID

        try:

            return self.collect_data(ids)

        except Exception as e:

            additional_message =  f'Error while processing webID {webID}: {e}'
            raise_logging_exception(e, endpoint, additional_message)
            raise Http404


    def handle_wps(self, webID):

        wpsData = WpsResults.objects.get(pk=webID[3:])  
        result_path = json.loads(wpsData.outputs)['path']
        loaded_data = json.loads(read_data(result_path, ''))

        table = {'id': loaded_data['meta']['id'],
                translation.gettext('Name'): translation.gettext(loaded_data['meta']['variable']['name']),
                translation.gettext('Commercial use allowed'):
                    human_readable_bool(loaded_data['meta']['license']['commercial_use']),
                translation.gettext('Embargo'): human_readable_bool(
                    has_pending_embargo(loaded_data['meta']['embargo'], loaded_data['meta']['embargo_end'])),
                'has_embargo': str(
                    has_pending_embargo(loaded_data['meta']['embargo'], loaded_data['meta']['embargo_end']))}

        return JsonResponse({'table': table, 'warning': ''})

   


    def collect_data(self, ids):
        """
        Called when clicked on more to see metadata of single dataset.
        TODO: Data should be accessed through 'NmEntrygroups', but for some datasets it's only working through 'Entries'

        :param ids: ID, styled depending on sender. E.g. could be wps12, db12 or just 12.
        :type ids: str
        :return: dict
        """
        
        prefix, nm_prefix, warning = 'entry__', '', ''

        def get_queryvalues(prefix, nm_prefix):
            return [prefix + 'uuid', prefix + 'variable__name', prefix + 'abstract',
                    prefix + 'license__commercial_use',
                    prefix + 'embargo', prefix + 'embargo_end',
                    prefix + 'datasource__temporal_scale__observation_start',
                    prefix + 'datasource__temporal_scale__observation_end',
                    prefix + 'datasource__spatial_scale__resolution',
                    prefix + 'datasource__temporal_scale__resolution',
                    nm_prefix + 'group__title', nm_prefix + 'group_id']

        try:
           
            if ids.startswith('['):
                ids = list(map(int, ids[1:-1].split(",")))
                db_info = NmEntrygroups.objects.filter(entry_id__in=ids).values(*get_queryvalues(prefix, nm_prefix))
            else: 
                db_info = NmEntrygroups.objects.filter(entry_id=int(ids)).values(*get_queryvalues(prefix, nm_prefix))
                
        except Exception as e:

            additional_message =  f'Error in views.show_info.collect_data: {e}'
            raise_logging_exception(e, endpoint, additional_message)
            raise Http404


        if not db_info.exists():
            warning = 'This dataset cannot be accessed from the Nm table. Please inform the database admin.'
            prefix, nm_prefix = '', 'nmentrygroups__'
            db_info = Entries.objects.filter(id=int(ids)).values(*get_queryvalues(prefix, nm_prefix))
            group_entry_ids = Entries.objects.filter(nmentrygroups__group_id=db_info[0][nm_prefix + 'group_id']) \
                .values_list('id', flat=True)
        else:
            group_entry_ids = NmEntrygroups.objects.filter(group_id=db_info[0]['group_id']) \
                .values_list('entry_id', flat=True)
        
        variable_name = translation.gettext(db_info[0][prefix + 'variable__name'])

        table = {
            'id': ids,
            'uuid': db_info[0][prefix + 'uuid'],
            'Name': db_info[0][prefix + 'variable__name'],
            'Commercial use allowed': human_readable_bool(db_info[0][prefix + 'license__commercial_use']),
            'Embargo': human_readable_bool(
                has_pending_embargo(db_info[0][prefix + 'embargo'], db_info[0][prefix + 'embargo_end'])
            ),
            'Abstract': db_info[0][prefix + 'abstract'] or '-',
            'has_embargo': str(
                has_pending_embargo(db_info[0][prefix + 'embargo'], db_info[0][prefix + 'embargo_end'])
            ),
            'Group': db_info[0][nm_prefix + 'group__title'] or '-',
            'group_entry_ids': list(group_entry_ids),
        }

        if db_info[0][prefix + 'datasource__spatial_scale__resolution']:
            table['Spatial Resolution'] = f"{db_info[0][prefix + 'datasource__spatial_scale__resolution']} m"

        if db_info[0][prefix + 'datasource__temporal_scale__resolution']:
            temporal_resolution = self._parse_iso8601_duration(
                db_info[0][prefix + 'datasource__temporal_scale__resolution']
            )
            table['Temporal Resolution'] = self._format_duration_to_detailed_str(temporal_resolution)

        table['Observation Start'] = (
            db_info[0][prefix + 'datasource__temporal_scale__observation_start'].strftime('%d %b %Y')
            if db_info[0][prefix + 'datasource__temporal_scale__observation_start']
            else '-'
        )
        table['Observation End'] = (
            db_info[0][prefix + 'datasource__temporal_scale__observation_end'].strftime('%d %b %Y')
            if db_info[0][prefix + 'datasource__temporal_scale__observation_end']
            else '-'
        )

        return JsonResponse({'table': table, 'warning': warning})
       


    def parse_iso8601_duration(self, duration_str):
        """
        Parse an ISO 8601 duration string into a timedelta object.

        :param duration_str: A string representing a duration in ISO 8601 format.
        :type duration_str: str
        :return: A timedelta object representing the parsed duration.
        :rtype: timedelta

        The function removes the 'P' prefix and splits the string into date and time parts. 

        Example:

        >>> parse_iso8601_duration('P3DT1H5M6S')
        output : 3 days, 1:05:06
           
        """
        
        duration_str = duration_str[1:]
        date_time_split = duration_str.split('T')
        days, hours, minutes, seconds = 0, 0, 0, 0

        print("date time split: " , date_time_split)
        
        if date_time_split[0]:
            date_part = date_time_split[0]
            days += int(date_part[:-1]) if date_part.endswith('D') else 0

       
        if len(date_time_split) > 1:
            time_part = date_time_split[1]
            hours += int(time_part.split('H')[0]) if 'H' in time_part else 0
            minutes += int(time_part.split('H')[-1].split('M')[0]) if 'M' in time_part else 0
            seconds += int(time_part.split('M')[-1].split('S')[0]) if 'S' in time_part else 0

        return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    def format_duration_to_detailed_str(self, duration):
        """
        Format a duration object into a detailed string.

        :param duration: A datetime.timedelta object representing the duration.
        :type duration: datetime.timedelta

        :return: A string representation of the duration in the format "days day(s), hours hour(s), minutes minute(s), seconds second(s)".
        :rtype: str

        If the duration has no days (Similarly for hours, minutes, seconds) , it will not be included in the string.
        """
        parts = []
        days = duration.days
        seconds = duration.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
       
        if days: parts.append(f"{days} day{'s' if days > 1 else ''}")
        if hours: parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
        if minutes: parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
        if seconds: parts.append(f"{seconds} second{'s' if seconds > 1 else ''}")

        return ", ".join(parts) if parts else "0 seconds"



class WorkspaceData(View):
    """
    Preload selected data when changing web page to workspace

    :param request:
    :return:
    """

    def get(self, request):

        endpoint =request.path

        try:
            
            start_date = request.get('startDate')
            end_date = request.get('endDate')
            result = collect_selection(request,
                                    json.loads(request.get('workspaceData')),
                                    start_date, end_date
                                    )
            return JsonResponse({'workspaceData': result['data'], 'error': result['error'], 'group': result['group'],
                                'selectedDate': [start_date, end_date]})

        except Exception as e:
            additional_message =  f'Error in vfw_home/views/workspace_data: {e}'
            raise_logging_exception(e, endpoint, additional_message)
            raise Http404
            





class EntriesPaginationView(View):
    """
    View to return result in several pages (5 datasets per page) instead of hundreds of results on one page.
    """

    def get(self, request):
        """
        Handles GET requests to paginate entries.

        :param request: HTTP request object
        :return: HttpResponse with rendered 'entrieslist.html' template
        """
        datasets = json.loads(request.GET.get('datasets', '[]'))
        field = {
            'id', 'uuid', 'embargo', 'title', 'version', 'citation', 'abstract',
            'variable__name', 'variable__symbol', 'variable__unit__symbol',
            'variable__keyword__value', 'datasource__datatype__name',
            'datasource__temporal_scale__resolution', 'datasource__temporal_scale__observation_start',
            'datasource__temporal_scale__observation_end', 'datasource__spatial_scale__extent',
            'license__short_title', 'license__title'
        }

        entries_list = self.get_entries_list(datasets, field)
        accessible_ids = self.get_accessible_ids(request, datasets) if datasets else []

        owndata = request.session.get('datasets', None)
        entriespage = self.paginate_entries(request, entries_list, 5)

        return render(request, 'vfw_home/entrieslist.html', {
            'entries': entriespage,
            'ownData': owndata,
            'accessible_ids': accessible_ids
        })

    def get_entries_list(self, datasets, field):
        """
        Retrieve the list of entries based on the provided datasets and fields.

        :param datasets: List of dataset IDs
        :param field: Set of fields to retrieve
        :return: QuerySet of entries
        """
        if datasets:
            return Entries.objects.values(*field).order_by('title').filter(pk__in=datasets)
        return Entries.objects.values(*field).order_by('title')

    def get_accessible_ids(self, request, datasets):
        """
        Get the accessible dataset IDs for the user.

        :param request: HTTP request object
        :param datasets: List of dataset IDs
        :return: List of accessible dataset IDs
        """
        accessible_data = get_accessible_data(request, datasets)
        return accessible_data.get('open', [])

    def paginate_entries(self, request, entries_list, per_page):
        """
        Paginate the entries list.

        :param request: HTTP request object
        :param entries_list: List of entries to paginate
        :param per_page: Number of entries per page
        :return: Page object with paginated entries
        """
        page_number = request.GET.get('page', 1)
        paginator = Paginator(entries_list, per_page)
        return paginator.get_page(page_number)




class Delineator(View):
    @staticmethod
    def get(request, catchout):

        endpoint = request.path
        try:
            if "catchout=" in catchout:
                catchment = Delineator._handle_coordinates(catchout, endpoint)
            elif "catchStartID=" in catchout:
                catchment = Delineator._handle_start_id(catchout, endpoint)
            else:
                raise ValueError(f"Unknown input for delineator: {catchout}")
                

            if 'error' in catchment:
                raise ValueError(f"Problems in delineation tool: {catchment['error']}")
               

            return JsonResponse(catchment)

        except ValueError as e :
            
            raise_logging_exception(e, endpoint, None)
            return JsonResponse({'error': str(e)}, status=400)

        except Exception as e:
            additional_message =  "Unhandled error in Delineator view."
            raise_logging_exception(e, endpoint, additional_message)
            return JsonResponse({'error': 'Unhandled server error.'}, status=500)

    @staticmethod
    def _handle_coordinates(catchout, endpoint):
        try:
            parts = catchout.split("catchout=")
            lng, lat = parts[1][:-1], parts[2]
            coords = {'lat': [lat], 'lng': [lng]}

            # Validate coordinates
            if not is_coord(lat, 'lat') or not is_coord(lng, 'lon'):
                raise ValueError(f"Invalid coordinates from client: {coords}")
                

            return delineate(coords=coords)

        except ValueError as e:
            raise_logging_exception(e, endpoint, None)
            return {'error': 'Invalid coordinates provided.'}

      
        except Exception as e:
            additional_message =  f"Error parsing coordinates: {e}"
            raise_logging_exception(e, endpoint, additional_message)
            return {'error': 'Malformed coordinates input.'}

    @staticmethod
    def _handle_start_id(catchout, endpoint):

        try:

            start_id = int(catchout.split("catchStartID=")[1])
            return delineate(terminal_comid=start_id, precise=True)

        except ValueError as e:

            additional_message = f"Error parsing start ID: {e}"
            raise_logging_exception(e, endpoint, additional_message)
            return {'error': 'Invalid start ID provided.'}



class AdvancedFilterView(View):
    """
    View to handle advanced filtering of entries.
    """
    
    def get(self, request):
        
        selection = Entries.objects.all().distinct('entry_id')
        
        
        advfilter = NMPersonsFilter(request.GET, queryset=selection)
        selection = advfilter.qs
        
        
        context = {
            'advFilter': advfilter,
            'selection': selection
        }
        
        
        return render(request, 'vfw_home/advanced_filter.html', context)


def quick_filter_defaults(request):
    """
    Function to create default html for the quick filter.
    :param request:
    :return:
    """
    total = Entries.objects.exclude(Q(embargo=True) & Q(embargo_end__gte=timezone.now())).count()

    quickfilter = QuickFilterForm()  
    more = QuickFilterForm.More()  
    selection = []
    return {'quickfilter': quickfilter, 'more': more, 'selection': selection, 'total': total}


class QuickFilter(View):

    @staticmethod
    def get(request):
        context = quick_filter_defaults(request)
        return render(request, 'vfw_home/quick_filter.html', context)


class QuickFilterResults(View):
    """
    When the user selects something on the map or in the quick filter, here the result is produced.
    """

    @staticmethod
    def post(request, selection):

        endpoint = request.path

        try:
            
            selection_query = QueryDict(selection)
            simple_queries = {
                'variables': 'variable__name__in',
                'institution': 'nmpersonsentries__person__organisation_name__in',
                'project': 'nmentrygroups__group__type__name__in'
            }

            filter_dict, filter_area, filter_area_or, fair_query = QuickFilterResults.initialize_filters()
            
            
            for key in selection_query:
                QuickFilterResults.handle_filter_key(key, simple_queries, selection_query, filter_dict, fair_query , filter_area, filter_area_or )
            
            query = QuickFilterResults.build_query(filter_dict, filter_area, filter_area_or, fair_query)
            
            
            total_results = query.count()
            

            data_ext, layertype = QuickFilterResults.get_data_extent(query)
            
            response_data = QuickFilterResults.prepare_response_data(request, query, total_results, data_ext, layertype)
            

        except Exception as e:

            additional_message = f'Unable to prepare your selection: {e}'
            raise_logging_exception(e, endpoint, additional_message)
            response_data = QuickFilterResults.prepare_error_response(selection)
            print('response_data 2 : ', e)

        return JsonResponse(response_data)


    @staticmethod
    def initialize_filters():
        filter_dict = {}
        filter_area = {}
        filter_area_or = {}
        fair_query = Q(embargo=True) & Q(embargo_end__gte=timezone.now())
        return filter_dict, filter_area, filter_area_or, fair_query


    @staticmethod
    def add_fair_filters(key, selection_query, fair_query ):
        if selection_query.getlist(key) == ['false']:
            fair_query = Q(embargo=True) & Q(embargo=False)



    @staticmethod
    def add_date_filters(selection_query, filter_dict):
        date_end = make_aware(datetime.datetime.strptime(selection_query.getlist('date')[0], "%Y-%m-%d"))
        date_start = make_aware(datetime.datetime.strptime(selection_query.getlist('date')[1], "%Y-%m-%d"))

        filter_dict['datasource__temporal_scale__observation_end__gte'] = date_end

        filter_dict['datasource__temporal_scale__observation_start__lte'] = date_start

    @staticmethod
    def add_draw_filters(key, selection_query, filter_area, filter_area_or  ):
        values = selection_query.getlist(key)[0] 
        coordinates = iter([float(item) for item in values.split(',')])  
        poly = Polygon(tuple(zip(coordinates, coordinates)), srid=4326)  
        filter_area['location__intersects'] = poly  
        filter_area_or['datasource__spatial_scale__extent__intersects'] = poly 

    @staticmethod
    def add_catch_start_id_filters(key, selection_query, filter_area, filter_area_or):

        catchment = delineate(terminal_comid=selection_query.getlist(key)[0], precise=True)
        poly = GEOSGeometry(catchment['wkt'])
        filter_area['location__intersects'] = poly
        filter_area_or['datasource__spatial_scale__extent__intersects'] = poly

    @staticmethod
    def add_catchout_filters(key, selection_query, filter_area, filter_area_or):
        coords = json.loads(request.POST.get('coords'))
        if coords:
            catchment = tuple(tuple(x) for x in coords)
            poly = Polygon(catchment, srid=4326)  
        else:
            catchment = delineate(coords={'lng': [selection_query.getlist(key)[0]],
                                                'lat': [selection_query.getlist(key)[1]]}, precise=True)
            poly = GEOSGeometry(catchment['wkt'])
        filter_area['location__intersects'] = poly  #
        filter_area_or['datasource__spatial_scale__extent__intersects'] = poly 

                    
    @staticmethod
    def handle_filter_key(key, simple_queries, selection_query, filter_dict, fair_query , filter_area, filter_area_or ):

        
        if key in simple_queries:        
            filter_dict[simple_queries[key]] = selection_query.getlist(key)
        elif key == 'date':
            QuickFilterResults.add_date_filters(selection_query, filter_dict)
        elif key == 'is_FAIR':
            QuickFilterResults.add_fair_filters(key, selection_query, fair_query)
        elif key == 'draw':
            QuickFilterResults.add_draw_filters(key, selection_query, filter_area, filter_area_or)
        elif key == 'catchStartID':
            QuickFilterResults.add_catch_start_id_filters(key, selection_query, filter_area, filter_area_or)
        elif key == 'catchout':
            QuickFilterResults.add_catchout_filters(key, selection_query, filter_area, filter_area_or)


    @staticmethod
    def build_query(filter_dict, filter_area, filter_area_or, fair_query):
        return Entries.objects.filter(Q(**filter_dict), Q(**filter_area) | Q(**filter_area_or)).exclude(fair_query).only('id')


    @staticmethod
    def get_data_extent(query):
        data_ext = [7.574234, 47.581351, 10.351323, 49.625873]
        layertype = "point"
        if query:
            data_ext = QuickFilterResults.calculate_extent(query, layertype)
        return data_ext, layertype

    @staticmethod
    def calculate_extent(query, layertype):
        data_ext = None
        entry_ext = query.aggregate(Extent('location'))['location__extent']
        if entry_ext:
            data_ext = list(entry_ext)
        else:
            layertype = "areal_data"
            spatial_ext = query.aggregate(
                Extent('datasource__spatial_scale__extent'))['datasource__spatial_scale__extent__extent']
            if spatial_ext:
                data_ext = list(spatial_ext)
            else:
                geom_ext = query.aggregate(Extent('geom'))['geom__extent']
                if geom_ext:
                    data_ext = list(geom_ext)

        #print(data_ext)
        return data_ext

    @staticmethod
    def prepare_response_data(request, query, total_results, data_ext, layertype):

        endpoint = request.path

        IDs = list(query.values_list('id', flat=True))
        id_layer = 'ID_layer' + str(request.user)
        areal_id_layer = 'areal_ID_layer' + str(request.user)
        QuickFilterResults.delete_geoserver_layer(id_layer)
        QuickFilterResults.delete_geoserver_layer(areal_id_layer)

        if IDs:
            try:
                create_layer(request, id_layer, HomeView.STORE, HomeView.WORKSPACE, IDs, layertype="point")
                create_layer(request, areal_id_layer, HomeView.STORE, HomeView.WORKSPACE, IDs, layertype="areal_data")
            except Exception as e:

                additional_message = f'unhandled exception in vfw_home/views/QuickFilterResults(): {e}'
                raise_logging_exception(e, endpoint, additional_message)
        
        
        return {
            'selection': request.POST.get('selection', ''),
            'total': total_results,
            'areal_ID_layer': areal_id_layer,
            'ID_layer': id_layer,
            'dataExt': data_ext,
            'IDs': IDs
        }

    @staticmethod
    def prepare_error_response(selection):
        return {
            'selection': selection,
            'total': 0,
            'areal_ID_layer': '',
            'ID_layer': '',
            'dataExt': [7.574234, 47.581351, 10.351323, 49.625873],
            'IDs': []
        }

    @staticmethod
    def delete_geoserver_layer(name):
        if has_layer(name, HomeView.STORE, HomeView.WORKSPACE):
            delete_layer(name, HomeView.STORE, HomeView.WORKSPACE)


   
def error_404_view(request, exception):
   
    return render(request, 'vfw_home/404.html')


class DownloadView(View):
    """
    Give direct access to data without using the webportal
    """

    @staticmethod
    def get(request, name):

        endpoint = request.path

        try :

            if name == 'vfwVM':
                file_path = '/data/VBox_VFORWaTer.zip'
                
                if Path(file_path).exists():
                    with open(file_path, 'rb') as fh:
                        response = FileResponse(open(file_path, 'rb'))
                    
                        return response
                else:
                    
                    raise ValueError(f'no file at: {file_path}')   
            else:
                raise ValueError(f"Invalid file request: {name}")
        
        except Exception as error_message:

            raise_logging_exception(error_message, endpoint, None)

            raise Http404(error_message)


