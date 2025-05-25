# =================================================================
#
# Authors: Marcus Strobl <marcus.strobl@gmx.de>
# Contributors: Safa Bouguezzi <safa.bouguezzi@kit.edu>, Kaoutar Boussaoud <kaoutar.boussaourd@kit.edu>, Elnaz Azmi <elnaz.azmi@kit.edu>
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
from pyzip import PyZip

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
    get_paginatorpage, regex_patterns, is_coord, get_cache, check_data_consistency, clean_database_name

mpl.use('Agg')

from django.contrib.gis.geos import Polygon, GEOSGeometry
from .utilities.query_functions import get_bbox_from_data
from .utilities.filters import NMPersonsFilter
from .models import Entries, NmEntrygroups, Entrygroups, Timeseries, Timeseries_1D, Locations, Variables, TemporalScales

import logging
from pathlib import Path
from datetime import timedelta

# for debugging:
from time import time

"""

"""
logger = logging.getLogger(__name__)

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

        try:
            unblocked_ids = self.request.session.get('datasets', [])
            if not unblocked_ids:
                self.request.session['datasets'] = []
        except KeyError:
            unblocked_ids = []
            self.request.session['datasets'] = []

        try:
            verify_layer(request=self.request, datastore=self.STORE, workspace=self.WORKSPACE, filename=self.DATA_LAYER)
            print(f"Calling verify_layer with {self.DATA_LAYER}")

            verify_layer(request=self.request, datastore=self.STORE, workspace=self.WORKSPACE, filename=self.AREAL_DATA_LAYER, layertype='areal_data')

            print(f"Calling verify_layer with {self.AREAL_DATA_LAYER}")

        except Exception as e:
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

        if 'csv' in request.GET:
            # if 'download_data' in request.GET:
            s_id =  request.GET.get('csv')

            accessible_data = get_accessible_data(request, s_id)
            error_list = accessible_data['blocked']
            accessible_data = accessible_data['open']

            if len(accessible_data) > 0:
                rows = get_dataset(accessible_data[0])

                pseudo_buffer = Echo()
                writer = csv.writer(pseudo_buffer)
                response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
                response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
            return response

        if 'geojson' in request.GET:
            s_id =  request.GET.get('geojson')

            accessible_data = get_accessible_data(request, s_id)
            error_list = accessible_data['blocked']
            accessible_data = accessible_data['open']

            geojson_data = serialize("geojson", Locations.objects.filter(id = accessible_data[0]) , geometry_field="point_location", fields=["name"])

            response = HttpResponse(json.dumps(geojson_data), content_type="application/json")
            response['Content-Disposition'] = 'attachment; filename="somefilename.geojson"'
            return response

        if 'shp' in request.GET:
            s_id = request.GET.get('shp')
            accessible_data = get_accessible_data(request, s_id)
            error_list = accessible_data['blocked']
            accessible_data = accessible_data['open']

            if len(accessible_data) > 0:
                layer_name = 'shp_{}_{}_{}'.format(request.user, request.user.id, s_id)
                srid = 4326
                # create layer on geoserver to request shp file
                create_layer(request, layer_name, store, workspace, s_id)
                # use GEOSERVER shape-zip
                url = '{0}/{1}/ows?service=wfs&version=1.0.0&request=GetFeature&typeName={1}:{' \
                      '2}&outputFormat=shape-zip&srsname=EPSG:{3}'.format(LOCAL_GEOSERVER, workspace, layer_name, srid)
                request = requests.get(url)
                pzfile = PyZip().from_bytes(request.content)
                try:
                    del pzfile['wfsrequest.txt']
                except KeyError:
                    pass

                # clean up right after request:
                delete_layer(layer_name, store, workspace)
            return HttpResponse(pzfile.to_bytes(), content_type='application/zip')

        if 'xml' in request.GET:
            id = request.GET.get('xml')
            accessible_data = get_accessible_data(request, id)
            error_list = accessible_data['blocked']
            accessible_data = accessible_data['open']
            try:

                opener = urllib.request.build_opener(
                    urllib.request.HTTPBasicAuthHandler(password_manager),
                    urllib.request.HTTPCookieProcessor(cookie_jar))
                urllib.request.install_opener(opener)

                request = urllib.request.Request(url)
                response = urllib.request.urlopen(request)

                body = response.read()

            except Exception as e:
                print('e: ', e)
                # clean up right after request:
                delete_layer(layer_name, store, workspace)
            return HttpResponse(response.read().decode('utf-8'))


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
    """
    """

    #     template_name = 'vfw_home/help.html'
    def get(self, request):
        """

        :param request:
        :type request:
        :return:
        :rtype:
        """

        f = open(Path(settings.BASE_DIR) / 'USERHELP.md', 'r')
        context = {}
        i = 0
        for line in f:
            context[i] = line
            i += 1
        f.close()
        return render(request, 'home/help.html', {'context': context})

class ToggleLanguageView(View):
    """ """

    @staticmethod
    def post(request):
        """
        Set a cookie to switch language of website. Tutorial how to set language cookie at
        https://samulinatri.com/blog/django-translation/

        :param request:
        :type request:
        :return:
        :rtype:
        """
        lang = translation.get_language()
        logger.debug(f"current language: {lang}")
        logger.debug(
            "check_for_language: de {}, en-us {}, en-gb {}".format(
                translation.check_for_language("de"),
                translation.check_for_language("en-us"),
                translation.check_for_language("en-gb"),
            )
        )
        if lang == "en-gb" or lang == "en-us":
            translation.activate("de")
            request.session[settings.LANGUAGE_COOKIE_NAME] = "de"

        else:
            translation.activate("en-gb")
            if hasattr(request, "session"):
                request.session[settings.LANGUAGE_COOKIE_NAME] = "en-gb"
        logger.debug(f"new language: {translation.get_language()}")
        logger.debug(f'translation test: {translation.gettext("help")}')
        response = redirect(DEMO_VAR + "/")
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            request.session[settings.LANGUAGE_COOKIE_NAME],
        )
        return response



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
        work_space_name = HomeView.WORKSPACE  # 'CAOS_update'
        url = '{0}/{1}/ows?service={2}&version=1.0.0&request=GetFeature&typeName={1}:{3}&outputFormat=application%2' \
              'Fjson&srsname=EPSG:{4}&bbox={5},EPSG:{6}'.format(LOCAL_GEOSERVER, work_space_name, service, layer,
                                                                srid, bbox, srid)
        request_url = urllib.request.Request(url)
        response = urllib.request.urlopen(request_url)

        return HttpResponse(response.read().decode('utf-8'))


def previewplot(request):
    """
    Requested from vfw.js show_preview
    :param request:
    :return:
    """
    try:
        webID = request.GET.get('preview')
        entriesID = webID
        if webID[0:3] == 'db[':
            parts = webID[0:-1].split('[')
            webID = [f'db{id.strip()}' for id in parts[1].split(',')]
        elif webID[0:2] == 'db':
            parts = [0, webID[2:]]
            entriesID = webID[2:]
        else:
            logger.warning(f'Figure how to handle an ID like {webID}')

        accessible_data = get_accessible_data(request, [parts[1]])
        error_list = accessible_data['blocked']
        accessible_data = accessible_data['open']

        if len(accessible_data) < 1:
            return JsonResponse({'warning': translation.gettext(
                'No plot available. <br/>First access to this dataset is needed.')})

    except Exception as e:
        print('Exception: ', e)

    full_res = False
    plot_size = [700, 500]
    if request.GET.get('startdate') != 'None':
        date = [make_aware(datetime.datetime.strptime(request.GET.get('startdate'), '%Y-%m-%d')),
                make_aware(datetime.datetime.strptime(request.GET.get('enddate'), '%Y-%m-%d'))]
    else:
        date = None

    cache_obj = {'use_redis': True, 'redis': redis.StrictRedis(),
                 'in_cache': False, 'name': "plot_{}".format('b' + str(webID) + str(plot_size) + str(date))}
    cache_obj, img = get_cache(cache_obj)

    if not cache_obj['in_cache']:

        try:
            if isinstance(webID, list):
                dataset = []
                for i in webID:
                    if has_data(i[2:]):
                        dataset.append(DataObject(i, date))
                    else:
                        print('\033[33mNo Data for dataset with entries ID:\033[0m ', webID)
            else:
                if has_data(entriesID):
                    if int(entriesID)  not in cache.get('ids_data_on_path')  :
                        dataset = DataObject(webID, date)
                    else:
                        print('One must handle data on path/ check if raster (= has spatial resolution) => '
                              'plot raster image, if netCDF => datacube')
                        return JsonResponse({'error': f'Plot for entries ID {webID} has to be implemented.'})
                else:
                    print('\033[33mNo Data for dataset with entries ID:\033[0m ', webID)
                    return JsonResponse({'error': f'No Data for dataset with entries ID {webID}'})

        except TypeError as e:
            # print('\033[33mhome.views.previewplot: Type error in Data Object:\033[0m ', e)
            logger.debug('Type Error in Data Object: ', e)
            raise Http404
        except IndexError as e:
            # print('\033[33mhome.views.previewplot: index error in Data Object:\033[0m ', e)
            logger.debug('Index Error in Data Object: ', e)
            if request.user.is_authenticated:
                raise Http404
            else:
                raise Http404
        except EmptyResultSet as e:
            # print('\033[33mhome.views.previewplot: EmptyResultSet Error in Data Object:\033[0m ', e)
            logger.debug('EmptyResultSet Error in Data Object: ', e)
            return JsonResponse({'error': e})
        except LookupError as e:
            # print('\033[33mhome.views.previewplot: LookupError in Data Object:\033[0m ', e)
            logger.debug('LookupError in Data Object: ', e)
            return JsonResponse({'error': e})
        except FieldError as e:
            # print('\033[33mhome.views.previewplot: Field Error in Data Object:\033[0m ', e)
            logger.debug('Field Error in Data Object: ', e)
            raise Http404
        except Exception as e:
            # print('\033[31mhome.views.previewplot: An unhandled error in Data Object:\033[0m ', e)
            logger.debug('An unhandled Error in Data Object: ', e)
            raise Http404

        plot = FigObject(dataset, plot_size)
        img = plot.get_plot()
    return JsonResponse(img)


class ShortInfoPaginationView(View):
    """
    View to return only a little metadata and give access to more details.
    """

    def get(self, request):
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

        except TypeError:
            logger.debug('Short info Pagination failed.')
            raise Http404

        except Exception as e:
            logger.debug(f'Exception while getting short info pagination: {e}')
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

def show_info(request):
    """
    On request collect metadata for preview on map and selection in the sidebar.
    Requested from map.js show_info.
    :param request:
    :return:
    """

    def parse_iso8601_duration(duration_str):
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
        # Remove the 'P' and split into date and time parts
        duration_str = duration_str[1:]
        date_time_split = duration_str.split('T')
        days, hours, minutes, seconds = 0, 0, 0, 0

        print("date time split: " , date_time_split)
        # If there's a date component, parse it
        if date_time_split[0]:
            date_part = date_time_split[0]
            days += int(date_part[:-1]) if date_part.endswith('D') else 0

        # If there's a time component, parse it
        if len(date_time_split) > 1:
            time_part = date_time_split[1]
            hours += int(time_part.split('H')[0]) if 'H' in time_part else 0
            minutes += int(time_part.split('H')[-1].split('M')[0]) if 'M' in time_part else 0
            seconds += int(time_part.split('M')[-1].split('S')[0]) if 'S' in time_part else 0

        return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)


    def format_duration_to_detailed_str(duration):
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
        # return f"{days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} second(s)"
        if days: parts.append(f"{days} day{'s' if days > 1 else ''}")
        if hours: parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
        if minutes: parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
        if seconds: parts.append(f"{seconds} second{'s' if seconds > 1 else ''}")

        return ", ".join(parts) if parts else "0 seconds"

    def collect_data(ids):
        """
        Called when clicked on more to see metadata of single dataset.

        :param ids: ID, styled depending on sender. E.g. could be wps12, db12 or just 12.
        :type ids: str
        :return: dict
        """
        # build dict of lists for preview:
        prefix = 'entry__'
        nm_prefix = ''  # nmentrygroups__
        warning = ''

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
            # For a list of datasets use this
            if ids[0] == '[':
                string_list = ids[1:-1].split(",")
                ids = list(map(int, string_list))
                db_info = NmEntrygroups.objects.filter(entry_id__in=ids).values(*get_queryvalues(prefix, nm_prefix))
            else:  # For one dataset use this
                db_info = NmEntrygroups.objects.filter(entry_id=int(ids)).values(*get_queryvalues(prefix, nm_prefix))
        except Exception as e:
            # print('Error in views.show_info.collect_data: ', e)
            logger.debug('Error in views.show_info.collect_data: ', e)

        if not db_info.exists():
            warning = '[TODO]  This dataset can not be accessed from the Nm table. Please inform database admin.'
            prefix = ''
            nm_prefix = 'nmentrygroups__'
            db_info = Entries.objects.filter(id=int(ids)).values(*get_queryvalues(prefix, nm_prefix))
            group_entry_ids = Entries.objects.filter(nmentrygroups__group_id=db_info[0][nm_prefix + 'group_id']) \
                .values_list('id', flat=True)
        else:
            group_entry_ids = NmEntrygroups.objects.filter(group_id=db_info[0]['group_id']) \
                .values_list('entry_id', flat=True)

        variable_name = translation.gettext(db_info[0][prefix + 'variable__name'])
        table = {'id': ids, 'uuid': db_info[0][prefix + 'uuid'],
                 translation.gettext('Name'): variable_name }


        table[translation.gettext('Commercial use allowed')] = \
            human_readable_bool(db_info[0][prefix + 'license__commercial_use'])
        table[translation.gettext('Embargo')] = human_readable_bool(
            has_pending_embargo(db_info[0][prefix + 'embargo'], db_info[0][prefix + 'embargo_end']))
        table[translation.gettext('Abstract')] = translation.gettext(db_info[0][prefix + 'abstract']) \
            if db_info[0][prefix + 'abstract'] else '-'
        table['has_embargo'] = str(
            has_pending_embargo(db_info[0][prefix + 'embargo'], db_info[0][prefix + 'embargo_end']))
        table[translation.gettext('Group')] = translation.gettext(db_info[0][nm_prefix + 'group__title']) \
            if db_info[0][nm_prefix + 'group__title'] else '-'
        table['group_entry_ids'] = list(group_entry_ids)

        if db_info[0][prefix + 'datasource__spatial_scale__resolution'] is not None :
            table[translation.gettext('Spatial Resolution')] = str(db_info[0][prefix + 'datasource__spatial_scale__resolution']) + " " + "m"

        if db_info[0][prefix + 'datasource__temporal_scale__resolution'] is not None :
            parsed_date = parse_iso8601_duration(db_info[0][prefix + 'datasource__temporal_scale__resolution'])
            table[translation.gettext('Temporal Resolution')] = format_duration_to_detailed_str(parsed_date)

        table[translation.gettext('Observation Start')] = db_info[0][prefix + 'datasource__temporal_scale__observation_start'].strftime('%d %b %Y') if db_info[0][prefix + 'datasource__temporal_scale__observation_start'] else '-'
        table[translation.gettext('Observation End')] = db_info[0][prefix + 'datasource__temporal_scale__observation_end'].strftime('%d %b %Y') if db_info[0][prefix + 'datasource__temporal_scale__observation_end'] else '-'

        return JsonResponse({'table': table, 'warning': warning})

    webID = request.GET.get('show_info')
    if webID[0:3] == 'wps':
        wpsData = WpsResults.objects.get(pk=webID[3:])  # .values('inputs', 'outputs', 'open')
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

    else:
        if webID[0:2] == 'db':
            ids = webID[2:]
        else:
            ids = webID

        try:
            return collect_data(ids)

        except TypeError:
            raise Http404


def workspace_data(request):
    """
    Preload selected data when changing web page to workspace

    :param request:
    :return:
    """

    try:
        # prepare dataset_iddatasetdownload differently for list and single value to use in collect_selection
        start_date = request.GET.get('startDate')
        end_date = request.GET.get('endDate')
        result = collect_selection(request,
                                   json.loads(request.GET.get('workspaceData')),
                                   start_date, end_date
                                   )
        return JsonResponse({'workspaceData': result['data'], 'error': result['error'], 'group': result['group'],
                             'selectedDate': [start_date, end_date]})

    except TypeError as e:
        logger.debug('Type Error in vfw_home/views/workspace_data: ', e)
        raise Http404
    except FieldError as e:
        logger.debug('Field Error in vfw_home/views/workspace_data: ', e)
        raise Http404
    except Exception as e:
        # print('unhandled exception in vfw_home/views/workspace_data(): ', e)
        logger.debug('unhandled exception in vfw_home/views/workspace_data(): ', e)





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
        catchment = {'error': 'Neither catchout nor catchStartID is defined to Delineate a catchment.'}
        if "catchout=" in catchout:
            coords = {
                'lat': [catchout.split("catchout=")[2]],
                'lng': [catchout.split("catchout=")[1][:-1]],
            }
            # validate input data:
            if not is_coord(coords['lat'][0], 'lat') or not is_coord(coords['lng'][0], 'lon'):
                logger.error(f'Wrong coordinates from client: ({coords}). Improve coordinate handling on client')
                return {'Error': 'Error in Coordinates.'}

            catchment = delineate(coords=coords)

        elif "catchStartID=" in catchout:
            start_id = int(catchout.split("catchStartID=")[1])
            catchment = delineate(terminal_comid=start_id, precise=True)

        else:
            # print(f'unknown input for delineator: {catchout}')
            logger.error(f'unknown input for delineator: {catchout}')

        if 'error' in catchment:
            print('Problems in delineation tool: ', catchment['error'])
            # logger.error('Problems in delineation tool: ', catchment['error'])

        return JsonResponse(catchment)



class AdvancedFilterView(View):
    """
    View to handle advanced filtering of entries.
    """

    def get(self, request):
        # Initial query to get all entries with distinct entry_id
        selection = Entries.objects.all().distinct('entry_id')

        # Apply the advanced filter based on GET parameters
        advfilter = NMPersonsFilter(request.GET, queryset=selection)
        selection = advfilter.qs

        # Prepare context data for the template
        context = {
            'advFilter': advfilter,
            'selection': selection
        }

        # Render the template with the context data
        return render(request, 'vfw_home/advanced_filter.html', context)


def quick_filter_defaults(request):
    """
    Function to create default html for the quick filter.
    :param request:
    :return:
    """
    total = Entries.objects.exclude(Q(embargo=True) & Q(embargo_end__gte=timezone.now())).count()

    quickfilter = QuickFilterForm()  # standard of django is a required attribute for all forms.
    more = QuickFilterForm.More()  # you can remove the required with use_required_attribute=False
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

        # create query according to selection
        try:

            selection_query = QueryDict(selection)
            simple_queries = {
                'variables': 'variable__name__in',
                'institution': 'nmpersonsentries__person__organisation_name__in',
                'project': 'nmentrygroups__group__type__name__in'
            }

            filter_dict, filter_area, filter_area_or, fair_query = QuickFilterResults.initialize_filters()


            for key in selection_query:
                QuickFilterResults.handle_filter_key(key, simple_queries, selection_query, filter_dict, fair_query, filter_area, filter_area_or, request)

            query = QuickFilterResults.build_query(filter_dict, filter_area, filter_area_or, fair_query)

            total_results = query.count()

            data_ext, layertype = QuickFilterResults.get_data_extent(query)

            response_data = QuickFilterResults.prepare_response_data(request, query, total_results, data_ext, layertype)

        except Exception as e:

            logger.debug(f'Unable to prepare your selection: {e}')
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
    def add_catchout_filters(key, selection_query, filter_area, filter_area_or, request):
        coords = json.loads(request.POST.get('coords'))
        if coords and len(coords) == 1 and len(coords[0]) > 3:
            catchment = tuple(tuple(x) for x in coords[0])
            poly = Polygon(catchment, srid=4326)
        elif coords and len(coords) == 1 and len(coords[0]) < 4:
            raise 'Error: Not enough coordinates. Not a valid polygon.'
        elif coords and len(coords) < 4:
            raise 'Error: Not enough coordinates. Not a valid polygon.'
        elif coords:
            catchment = tuple(tuple(x) for x in coords)
            poly = Polygon(catchment, srid=4326)
        else:
            catchment = delineate(coords={'lng': [selection_query.getlist(key)[0]],
                                                'lat': [selection_query.getlist(key)[1]]}, precise=True)
            poly = GEOSGeometry(catchment['wkt'])
        filter_area['location__intersects'] = poly  #
        filter_area_or['datasource__spatial_scale__extent__intersects'] = poly

    @staticmethod
    def handle_filter_key(key, simple_queries, selection_query, filter_dict, fair_query, filter_area, filter_area_or, request):
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
            QuickFilterResults.add_catchout_filters(key, selection_query, filter_area, filter_area_or, request)


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

        return data_ext

    @staticmethod
    def prepare_response_data(request, query, total_results, data_ext, layertype):
        #print(request.user)

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
                logger.debug(f'unhandled exception in vfw_home/views/QuickFilterResults(): {e}')

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

        if name == 'vfwVM':
            file_path = '/data/VBox_VFORWaTer.zip'
            if Path(file_path).exists():
                with open(file_path, 'rb') as fh:
                    response = FileResponse(open(file_path, 'rb'))
                    return response
            else:
                print('no file at: ', file_path)
                error_404_view(request, 'not available')
        else:
            error_404_view(request, 'not available')

