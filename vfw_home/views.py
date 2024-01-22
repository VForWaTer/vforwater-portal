import ast
import csv
import datetime
import json
import re
import sys
from http.cookiejar import CookieJar

import pandas as pd
import redis
import requests
from django.contrib.gis.db.models.aggregates import Extent
from django.core.exceptions import EmptyResultSet, FieldError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Count, Exists, OuterRef, Sum
from django.utils.timezone import make_aware
from pyzip import PyZip

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

from author_manage.views import MyResourcesView
from heron.settings import LOCAL_GEOSERVER, DEMO_VAR, DATA_DIR

from vfw_home.geoserver_layer import create_layer, get_layer, delete_layer, test_geoserver_env
# from vfw_home.previewplot import get_plot_from_db_id, get_bokeh_std_fullres, format_label, get_cache
from wps_gui.models import WpsResults
from .Fig_obj import FigObject
from .checks import check_geoserver_layers
from .data_tools import __get_timescale, find_data_gaps, precision_to_minmax, is_data_short, DataTypes, \
    __get_axis_limits, __reduce_dataset, get_accessible_data, collect_selection, has_data, get_split_groups
from .delineator import delineate
from .forms import QuickFilterForm
from .data_obj import DataObject
from .utilities import human_readable_bool, has_pending_embargo, read_data, expressive_layer_name, get_dataset, \
    get_paginatorpage, regex_patterns, is_coord, get_cache, check_data_consistency

mpl.use('Agg')

from django.contrib.gis.geos import Polygon, GEOSGeometry
from .query_functions import get_bbox_from_data
# from .filter import QuickFilter
from .filters import NMPersonsFilter
from .models import Entries, NmEntrygroups, Entrygroups, Timeseries_1D, Locations, Variables

import logging
from pathlib import Path

# for debugging:
from time import time

"""

"""
logger = logging.getLogger(__name__)

check_data_consistency()
# class WorkflowView(TemplateView):
#     """
#     Template View for plain workflow HTML Template.
#     Template so far does only contain iframe in content Block, that embeds wps_workflow app
#     """
#     template_name = "vfw_home/workflow.html"

"""
# IMPORTANT:
# From Django doc about session: If SESSION_EXPIRE_AT_BROWSER_CLOSE is set to True, Django will use browser-length
# cookies – cookies that expire as soon as the user closes their browser. Use this if you want people to have to log in
# every time they open a browser.
"""

class HomeView(TemplateView):
    """
    Template View to bring the necessary variables for the startup to the template
    """
    template_name = 'vfw_home/home.html'

    # Before you make migrations
    # QuickFilter.items(requests)
    # data_layer = 'metacatalogdev'  # 'default_layer_prod'
    # data_layer = 'metacatalogdevnew'  # 'default_layer_prod'
    data_layer = 'devel'
    areal_data_layer = 'areal_devel'
    # data_layer = 'play'
    merit_river_layer = ['merit_river_test', 'merit_river']  # [layername, layertype]
    merit_river_ids = ['merit_river_simple', 'merit_river_simple']
    merit_catchment_layer = ['merit_catchment', 'merit_catchment']
    merit_catchment_coarse_layer = ['merit_catchment_coarse', 'merit_catchment_coarse']

    # if not dataExt:
    data_ext = [645336.034469495, 6395474.75106861, 666358.204722283, 6416613.20733359]

    """
    IMPORTANT! Don't use "-" in geoserver names!!!
    """
    store = 'metacatalogdev'  # 'marcus'  # 'new_vforwater_gis'
    workspace = 'metacatalogdev'  # 'marcus'  # 'CAOS_update'
    # store = 'play'  # 'new_vforwater_gis'
    # workspace = 'play'  # 'CAOS_update'
    unlocked_embargo = []

    check_geoserver_layers(store, workspace,
                           [merit_river_layer, merit_river_ids, merit_catchment_layer, merit_catchment_coarse_layer])

    # TODO: Test with users if this makes any sense
    def __set_layer_name(self):
        """
        Set name for layer in geoserver according to username or as admin_layer.
        """
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                self.data_layer = 'admin_layer'
                self.areal_data_layer = 'admin_areal_layer'
            else:
                self.data_layer = expressive_layer_name(self.request.user)
                self.areal_data_layer = expressive_layer_name(f'{self.request.user}_areal')

    # Put here everything you need at startup and for refresh of 'Home'
    def get_context_data(self, **kwargs: object):
        """
        Collect data needed for startup of V-FOR-WaTer Portal home.

        :param kwargs:
        :return:
        """
        self.__set_layer_name()
        # get_dataset(self, **kwargs)

        try:
            unblocked_ids = self.request.session['datasets']
        except KeyError:
            unblocked_ids = []
            self.request.session['datasets'] = []

        try:
            if not get_layer(self.data_layer, self.store, self.workspace):
                create_layer(self.request, self.data_layer, self.store, self.workspace)
            else:
                # TODO: don't do that in production! That's just for development to make sure geoserver is updated
                #  after restart of django
                delete_layer(self.data_layer, self.store, self.workspace)
                create_layer(self.request, self.data_layer, self.store, self.workspace)
                # get_layer(self.data_layer, self.store, self.workspace)

            if not get_layer(self.areal_data_layer, self.store, self.workspace):
                create_layer(request=self.request, filename=self.areal_data_layer, datastore=self.store,
                             workspace=self.workspace, layertype='areal_data')
            else:
                delete_layer(self.areal_data_layer, self.store, self.workspace)
                create_layer(request=self.request, filename=self.areal_data_layer, datastore=self.store,
                             workspace=self.workspace, layertype='areal_data')
        except:
            self.data_layer = 'Error: Found no geoserver!'
            print('Still no geoserver: ', sys.exc_info()[0])

        self.data_ext = get_bbox_from_data()

        context = quick_filter_defaults(self)

        return {'dataExt': self.data_ext, 'data_layer': self.data_layer, 'areal_data_layer': self.areal_data_layer,
                'messages': messages.get_messages(self.request), 'unblocked_ids': unblocked_ids,
                # 'merit_river_layer': self.merit_river_layer[0], 'merit_catchment_layer': self.merit_catchment_layer[0],
                # 'merit_river_simple': self.merit_river_ids[0],
                # 'merit_catchment_coarse_layer': self.merit_catchment_coarse_layer[0],
                **context}


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
        store = HomeView.store  # 'new_vforwater_gis'
        workspace = HomeView.workspace  # 'CAOS_update'
        test_geoserver_env(store, workspace)

        # def get_metadata(m_id):
        #     """
        #     the metadata for export includes only the values that are also used for filtering.
        #     Change get_metadata if you want to have more information in the export file.
        #     :return:
        #     """
        #     # TODO: Portal uses code from class MenuView.get, 'show_info'. Bad style to use two classes for popup.
        #     catalog = {}
        #     for table in Menu.menu_list:
        #         for i in table.db_alias_child:
        #             if table.path != '':
        #                 query = Entries.objects.filter(pk=m_id).values_list(table.path + '__' + i, flat=True)
        #                 # query = TblMeta.objects.filter(pk=m_id).values_list(table.path + '__' + i, flat=True)
        #             else:
        #                 query = Entries.objects.filter(pk=m_id).values_list(i, flat=True)
        #                 # query = TblMeta.objects.filter(pk=m_id).values_list(i, flat=True)
        #             if query[0] is not None:
        #                 try:
        #                     catalog[table.menu_name][i] = query[0]
        #                 except KeyError:
        #                     catalog[table.menu_name] = {i: query[0]}
        #     return catalog

        if 'csv' in request.GET:
            # if 'download_data' in request.GET:
            s_id = json.loads(request.GET.get('csv'))
            accessible_data = get_accessible_data(request, s_id)
            error_list = accessible_data['blocked']
            accessible_data = accessible_data['open']

            if len(accessible_data) > 0:
                # TODO: There are 3 Solutions to get data from the different tables.
                #  Solution 1 produces many None fields, hence is discarded.
                #  Solution 2 makes a query from 'Entries' to get datatype and builds another query from 'Entries'
                #  according to the result.
                #  Solution 3 gets the datatype and 'eval' a query for the respective table.
                #  Decide if solution 2 or 3 is better.
                #  Check if results are the right datasets!!!
                #  (Unused solutions deleted. Check commit from Sept 3, 2020)

                # Solution 2:
                # ===========
                rows = get_dataset(accessible_data[0])

                pseudo_buffer = Echo()
                writer = csv.writer(pseudo_buffer)
                response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
                response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
            return response

        if 'shp' in request.GET:
            s_id = request.GET.get('shp')
            accessible_data = get_accessible_data(request, s_id)
            error_list = accessible_data['blocked']
            accessible_data = accessible_data['open']

            if len(accessible_data) > 0:
                layer_name = 'shp_{}_{}_{}'.format(request.user, request.user.id, s_id)
                # srid = str(Entries.objects.filter(pk=s_id).values_list('geometry__srid__srid', flat=True)[0])
                srid = 4326
                # create layer on geoserver to request shp file
                # TODO: later this ids are compared to a list of numbers, so the s_id here has to be a list of numbers
                print('TODO: later this ids are compared to a list of numbers, so the s_id here has to be a list of numbers')
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

        # TODO: schema Location shows too much information for possible intruder. Figure out how to improve?
        if 'xml' in request.GET:
            id = request.GET.get('xml')
            accessible_data = get_accessible_data(request, id)
            error_list = accessible_data['blocked']
            accessible_data = accessible_data['open']
            try:

                opener = urllib.request.build_opener(
                    urllib.request.HTTPBasicAuthHandler(password_manager),
                    # urllib.request.HTTPHandler(debuglevel=1),    # Uncomment these two lines to see
                    # urllib.request.HTTPSHandler(debuglevel=1),   # details of the requests/responses
                    urllib.request.HTTPCookieProcessor(cookie_jar))
                urllib.request.install_opener(opener)

                request = urllib.request.Request(url)
                response = urllib.request.urlopen(request)

                # Print out the result (not a good idea with binary data!)

                body = response.read()
                # print('loaded xml', body)

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
    """

    """

    def logout(self, request):
        """

        :param request:
        :type request:
        :return:
        :rtype:
        """
        print('logout view: ', self)
        print('logut request: ', request)
        logger.debug(f'{request.user.username} logged out')
        logout(request)

    def post(self, request):
        """

        :param request:
        :type request:
        :return:
        :rtype:
        """
        print('post view: ', self)
        print('post request: ', request)
        self.logout(request)
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
    """

    """

    @staticmethod
    def post(request):
        """
        Set a cookie to switch language of web site. Tutorial how to set language cookie at
        https://samulinatri.com/blog/django-translation/

        :param request:
        :type request:
        :return:
        :rtype:
        """
        lang = translation.get_language()
        logger.debug(f'current language: {lang}')
        logger.debug('check_for_language: de {}, en-us {}, en-gb {}'.format(translation.check_for_language('de'),
                                                                            translation.check_for_language('en-us'),
                                                                            translation.check_for_language('en-gb')))
        if lang == 'en-gb' or lang == 'en-us':
            translation.activate('de')
            request.session[translation.LANGUAGE_SESSION_KEY] = 'de'
        else:
            translation.activate('en-gb')
            if hasattr(request, 'session'):
                request.session[translation.LANGUAGE_SESSION_KEY] = 'en-gb'
        logger.debug(f'new language: {translation.get_language()}')
        logger.debug(f'translation test: {translation.gettext("help")}')
        response = redirect(DEMO_VAR + '/')
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, request.session[translation.LANGUAGE_SESSION_KEY])
        return response


class FailedLoginView(View):
    """
    View for failed logins
    """

    @staticmethod
    def get(request):
        print('failed login view get')
        for i in request:
            print('request: ', i)
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
        work_space_name = HomeView.workspace  # 'CAOS_update'
        # url = LOCAL_GEOSERVER + '/' + work_space_name + '/ows?service=' + service + \
        #       '&version=1.0.0&request=GetFeature&typeName=' + work_space_name + ':' + layer + \
        #       '&outputFormat=application%2Fjson&srsname=EPSG:' + srid + '&bbox=' + bbox + ',EPSG:' + srid
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
        # webID = 'db869'
        if webID[0:3] == 'db[':
            parts = webID[0:-1].split('[')
            webID = [f'db{id.strip()}' for id in parts[1].split(',')]
        elif webID[0:2] == 'db':
            parts = [0, webID[2:]]
            entriesID = webID[2:]
        else:
            print('views.py: Figure how to handle such an ID: ', webID, type(webID))
            # logger.warning(f'Figure how to handle an ID like {webID}')

        accessible_data = get_accessible_data(request, [parts[1]])
        error_list = accessible_data['blocked']
        accessible_data = accessible_data['open']

        # ID = 1013
        # datatype = Entries.objects.filter(id=ID).values_list('datasource__datatype__name', flat=True)[0]

        # accessible_data = [1014]  # 1014: wind direction, 1013: 3D direction
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

    # TODO: Add the redis cache properly (https://docs.djangoproject.com/en/4.2/topics/cache/#redis)
    cache_obj = {'use_redis': True, 'redis': redis.StrictRedis(),
                 'in_cache': False, 'name': "plot_{}".format('b' + str(webID) + str(plot_size) + str(date))}
    cache_obj, img = get_cache(cache_obj)

    if not cache_obj['in_cache']:
        try:
            # bla = Entries.objects.filter(pk=webID[2:]).values_list('datasource__data_names',
            #                                                        'datasource__path',
            #                                                        'datasource__datatype__parent',
            #                                                        'datasource__datatype__name',
            #                                                        'datasource__datatype__title',
            #                                                        'datasource__datatype__description',
            #                                                        'datasource__temporal_scale__resolution',
            #                                                        'datasource__temporal_scale__observation_start',
            #                                                        'datasource__temporal_scale__support',
            #                                                        )
            if isinstance(webID, list):
                dataset = []
                for i in webID:
                    if has_data(i[2:]):
                        dataset.append(DataObject(i, date))
                    else:
                        print('\033[33mNo Data for dataset with entries ID:\033[0m ', webID)
            else:
                if has_data(entriesID):
                    t0 = time()
                    dataset = DataObject(webID, date)
                    t1 = time()
                else:
                    print('\033[33mNo Data for dataset with entries ID:\033[0m ', webID)
                    return JsonResponse({'error': f'No Data for dataset with entries ID {webID}'})

        except TypeError as e:
            print('\033[33mhome.views.previewplot: Type error in Data Object:\033[0m ', e)
            logger.debug('Type Error in Data Object: ', e)
            raise Http404
        except IndexError as e:
            print('\033[33mhome.views.previewplot: index error in Data Object:\033[0m ', e)
            logger.debug('Index Error in Data Object: ', e)
            if request.user.is_authenticated:
                # TODO: Rethink how to handle unallowed requests
                raise Http404
            else:
                # TODO: Redirect to login
                raise Http404
                # return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
                # return redirect('vfw_home:login')
        except EmptyResultSet as e:
            print('\033[33mhome.views.previewplot: EmptyResultSet Error in Data Object:\033[0m ', e)
            logger.debug('EmptyResultSet Error in Data Object: ', e)
            return JsonResponse({'error': e})
        except LookupError as e:
            print('\033[33mhome.views.previewplot: LookupError in Data Object:\033[0m ', e)
            logger.debug('LookupError in Data Object: ', e)
            return JsonResponse({'error': e})
        except FieldError as e:
            print('\033[33mhome.views.previewplot: Field Error in Data Object:\033[0m ', e)
            logger.debug('Field Error in Data Object: ', e)
            raise Http404
        except Exception as e:
            print('\033[31mhome.views.previewplot: An unhandled error in Data Object:\033[0m ', e)
            logger.debug('An unhandled Error in Data Object: ', e)
            raise Http404

        # plot = MultiplePlotsObject(dataset, plot_size=plot_size)
        plot = FigObject(dataset, plot_size)
        img = plot.get_plot()
    return JsonResponse(img)


def short_info_pagination(request):
    """
    Requested from map.js buildMapModal, show only little metadata and give access to more details
    :param request:
    :return:
    """
    try:
        accessible_ids = []
        naive_today = timezone.make_naive(timezone.now())
        datasets = json.loads(request.GET.get('datasets'))
        if type(datasets) is str:
            datasets = [int(datasets)]

        field = ['title', 'id', 'uuid', 'variable__name', 'embargo', 'embargo_end']
        field_name = {'title': 'Title', 'variable__name': 'Variable name', 'id': 'ID', 'uuid': 'UUID',
                      'embargo': 'Embargo', 'has_access': 'has_access', 'embargo_end': 'embargo_end'}

        # field = ['entry__title', 'entry__id', 'entry__uuid', 'entry__variable__name',
        #          'entry__embargo', 'entry__embargo_end', 'group__type__name']
        # field_name = {'entry__title': 'Title', 'entry__variable__name': 'Variable name',
        #               'entry__id': 'ID', 'entry__uuid': 'UUID',
        #               'entry__embargo': 'Embargo', 'entry__has_access': 'has_access',
        #               'entry__embargo_end': 'embargo_end', 'group__type__name': 'Group name',
        #               'entries': 'entries'}

        if datasets:
            entries_list = list(Entries.objects.values(*field).filter(pk__in=datasets) \
                .order_by('variable__name', 'title', 'id'))


            accessible_data = get_accessible_data(request, datasets)
            # error_ids = accessible_data['blocked']
            accessible_ids = accessible_data['open']

            split_datasets = (Entries.objects.filter(pk__in=datasets, nmentrygroups__group__type__name='Split dataset')
                              .values('id', 'nmentrygroups__group_id')
                              .order_by('nmentrygroups__group_id'))

            # put ids of a all parts of a split dataset in one list (with their group id as key)
            grouped_dict = defaultdict(list)
            for i in split_datasets:
                grouped_dict[i['nmentrygroups__group_id']].append(i['id'])

            # create a dict with indices and ids of datasets in entries_list, for a quick change of values
            entries_id_map = {d['id']: idx for idx, d in enumerate(entries_list)}

            # the first dataset from the split_ids, defined in append_dict,  will get all necessary info,
            # the values in the delete dict can be deleted
            append_dict = {}
            delete_list = []
            for k, v in grouped_dict.items():
                append_dict[v[0]] = v[1:]
                delete_list.extend(v[1:])

            # get the indices for the elements to delete:
            delete_indices = []
            for i in delete_list:
                delete_indices.append(entries_id_map[i])

            # now extend datasets according to the append_dict
            for target, split_list in append_dict.items():
                for dataset in split_list:
                    for k, v in entries_list[entries_id_map[target]].items():
                        if v != entries_list[entries_id_map[dataset]][k]:
                            entries_list[entries_id_map[target]][k] = [entries_list[entries_id_map[target]][k], entries_list[entries_id_map[dataset]][k]]

            # next remove the additional split datasets:
            for delete_id in sorted(delete_indices, reverse=True):
                entries_list.remove(entries_list[delete_id])

        else:
            entries_list = Entries.objects.values(*field).order_by('variable__name', 'title', 'id')

        # build pagination for entries
        current_page = get_paginatorpage(request.GET.get('page', 1), Paginator(entries_list, 5))

        newdict = defaultdict(list)
        for d in current_page:
            for key, val in d.items():
                if key != 'embargo_end':
                    newdict[translation.gettext(field_name[key])].append(val)
                else:
                    # if val < naive_today or d['embargo'] is False or d['id'] in accessible_ids:
                    if not has_pending_embargo(d['embargo'], val) or d['id'] in accessible_ids:
                        newdict['has_access'].append({'access': True, 'ssid': d['id']})
                    else:
                        newdict['has_access'].append({'access': False, 'ssid': d['id']})

        entries = dict(newdict.items())

        return render(request, 'vfw_home/mapmodal_entrieslist.html', {'entries_page': entries,
                                                                      'data_sets': datasets,
                                                                      'current_page': current_page})

    except TypeError:
        print('Short info Pagination failed.')
        logger.debug('Short info Pagination failed.')
        raise Http404

    except Exception as e:
        print('Exception while getting short info pagination: ', e)
        logger.debug('Exception while getting short info pagination: ', e)


# TODO: maybe it's enough to send here only a list with values, and load the list with fields in Homeview?
# TODO: Handle this with an http request (response, not request?)!
def show_info(request):
    """
    On request collect metadata for preview on map and selection in the sidebar.
    Requested from map.js show_info.
    :param request:
    :return:
    """

    def collect_data(ids):
        """
        Called when clicked on more to see metadata of single dataset.
        TODO: Data should be accessed through 'NmEntrygroups', but for some datasets it's only working through 'Entries'

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
                    nm_prefix + 'group__title', nm_prefix + 'group_id']

        try:
            if ids[0] == '[':
                string_list = ids[1:-1].split(",")
                ids = list(map(int, string_list))
                db_info = NmEntrygroups.objects.filter(entry_id__in=ids).values(*get_queryvalues(prefix, nm_prefix))
            else:
                db_info = NmEntrygroups.objects.filter(entry_id=int(ids)).values(*get_queryvalues(prefix, nm_prefix))
        except Exception as e:
            print('Error in views.show_info.collect_data: ', e)
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

        table = {'id': ids, 'uuid': db_info[0][prefix + 'uuid'],
                 translation.gettext('Name'): translation.gettext(db_info[0][prefix + 'variable__name'])}

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

        # table[translation.gettext('Abstract')] = translation.gettext(db_info[0][prefix + 'abstract']) \
        #     if db_info[0][prefix + 'abstract'] else '-'
        #
        # table[translation.gettext('Group')] = translation.gettext(db_info[0][nm_prefix + 'group__title']) \
        #     if db_info[0][nm_prefix + 'group__title'] else '-'
        # table['group_entry_ids'] = list(group_entry_ids)
        return JsonResponse({'table': table, 'warning': ''})

    else:
        if webID[0:2] == 'db':
            ids = webID[2:]
        else:
            ids = webID

        try:
            # print('json.loads(webID): ', json.loads(ids))
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
        print('Type Error in vfw_home/views/workspace_data: ', e)
        logger.debug('Type Error in vfw_home/views/workspace_data: ', e)
        raise Http404
    except Exception as e:
        print('unhandled exception in vfw_home/views/workspace_data(): ', e)
        logger.debug('unhandled exception in vfw_home/views/workspace_data(): ', e)


def entries_pagination(request):
    """
    Return result in several pages (5 datasets per page) instead of hundreds of results on one page.

    :param request: list of integers
    :type request: object
    :return: dict with 'entries, ownData, accessible_ids' to render entrieslist.html
    """
    accessible_ids = []
    datasets = json.loads(request.GET.get('datasets', 1))
    field = {'id', 'uuid', 'embargo', 'title', 'version', 'citation', 'abstract', 'variable__name', 'variable__symbol',
             'variable__unit__symbol', 'variable__keyword__value',
             'datasource__datatype__name', 'datasource__temporal_scale__resolution',
             'datasource__temporal_scale__observation_start', 'datasource__temporal_scale__observation_end',
             'datasource__spatial_scale__extent', 'license__short_title', 'license__title'}
    if datasets and len(datasets) > 0:
        entries_list = Entries.objects.values(*field).order_by('title').filter(pk__in=datasets)
        accessible_data = get_accessible_data(request, datasets)
        # error_ids = accessible_data['blocked']
        accessible_ids = accessible_data['open']
    elif datasets and len(datasets) == 0:
        entries_list = []
    else:
        entries_list = Entries.objects.values(*field).order_by('title')
    try:
        owndata = request.session['datasets']
    except KeyError:
        owndata = None

    entriespage = get_paginatorpage(request.GET.get('page', 1), Paginator(entries_list, 5))

    return render(request, 'vfw_home/entrieslist.html', {'entries': entriespage,
                                                         'ownData': owndata,
                                                         'accessible_ids': accessible_ids})


class Delineator(View):

    @staticmethod
    def get(request, catchout):

        coords = {
            'lat': [catchout.split("catchout=")[2]],
            'lng': [catchout.split("catchout=")[1][:-1]],
        }
        # validate input data:
        if not is_coord(coords['lat'][0], 'lat') or not is_coord(coords['lng'][0], 'lon'):
            logger.error(f'Wrong coordinates from client: ({coords}). Improve coordinate handling on client')
            return {'Error': 'Error in Coordinates.'}

        catchment = delineate(coords)

        if 'error' in catchment:
            print('Problems in delineation tool: ', catchment['error'])

        return JsonResponse(catchment)


def advanced_filter(request):
    # selection = NmPersonsEntries.objects.all().distinct('entry_id')
    selection = Entries.objects.all().distinct('entry_id')
    advfilter = NMPersonsFilter(request.GET, queryset=selection)
    selection = advfilter.qs

    context = {'advFilter': advfilter, 'selection': selection}
    return render(request, 'vfw_home/advanced_filter.html', context)


def quick_filter_defaults(request):
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

    @staticmethod
    def get(request, selection):

        simple_queries = {'variables': 'variable__name__in',
                          'institution': 'nmpersonsentries__person__organisation_name__in',
                          'project': 'nmentrygroups__group__type__name__in'}

        filter_dict = {}
        fair_query = Q(embargo=True) & Q(embargo_end__gte=timezone.now())

        for i in QueryDict(selection):
            if i in simple_queries:
                filter_dict[simple_queries[i]] = QueryDict(selection).getlist(i)
            elif i == 'date':
                filter_dict['datasource__temporal_scale__observation_end__gte'] = \
                    make_aware(datetime.datetime.strptime(QueryDict(selection).getlist('date')[0], "%Y-%m-%d"))
                filter_dict['datasource__temporal_scale__observation_start__lte'] = \
                    make_aware(datetime.datetime.strptime(QueryDict(selection).getlist('date')[1], "%Y-%m-%d"))
            # elif i == 'is_FAIR' and QueryDict(selection).getlist(i) == ['true']:
            #     fair_query = Q(embargo=True) & Q(embargo_end__gte=timezone.now())
            elif i == 'is_FAIR' and QueryDict(selection).getlist(i) == ['false']:
                # TODO: figure out how to avoid the following useless query
                #  (this exists because in exclude query is always some input needed)
                fair_query = Q(embargo=True) & Q(embargo=False)
            elif i == 'draw':
                values = QueryDict(selection).getlist(i)[0]
                it = iter([float(item) for item in values.split(',')])
                poly = Polygon(tuple(zip(it, it)), srid=4326)
                filter_dict['location__intersects'] = poly

        query = Entries.objects.filter(**filter_dict).exclude(fair_query).only('id')
        total_results = query.count()

        # From here collect data to update map:
        data_ext = [7.574234, 47.581351, 10.351323, 49.625873]  # an arbitrary zoom location for NO RESULT
        layertype = "point"
        try:
            if query:
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

        except TypeError as e:
            print('Selection has no extend: ', e)
        except Exception as e:
            print('unhandled exception in vfw_home/views/QuickFilterResults(): ', e)
            logger.debug('unhandled exception in vfw_home/views/QuickFilterResults(): ', e)

        IDs = list(query.values_list('id', flat=True))
        id_layer = 'ID_layer' + str(request.user)
        if get_layer(id_layer, HomeView.store, HomeView.workspace):
            delete_layer(id_layer, HomeView.store, HomeView.workspace)

        if IDs:
            try:
                create_layer(request, id_layer, HomeView.store, HomeView.workspace, IDs, layertype=layertype)
            except Exception as e:
                print('unhandled exception in vfw_home/views/QuickFilterResults(): ', e)
                logger.debug('unhandled exception in vfw_home/views/QuickFilterResults(): ', e)
            # create_layer(request, id_layer, HomeView.store, HomeView.workspace, IDs)
            # create_layer(request, id_layer, HomeView.store, HomeView.workspace, str(IDs)[1:-1])
        else:
            # TODO: Selection with no result has to be handled properly
            pass

        return JsonResponse({'selection': selection, 'total': total_results,
                             'ID_layer': id_layer, 'dataExt': data_ext, 'IDs': IDs})


def error_404_view(request, exception):
    # data = {"name": "Some Error"}
    # return render(request,'vfw_home/404.html', data)
    return render(request, 'vfw_home/404.html')


class DownloadView(View):
    """
    Give direct access to data without using the webportal
    """

    @staticmethod
    def get(request, name):

        if name == 'vfwVM':
            file_path = '/data/VBox_VFORWaTer.zip'
            # file_path = '/home/marcus/tmp/customs.shp'
            if Path(file_path).exists():
                with open(file_path, 'rb') as fh:
                    response = FileResponse(open(file_path, 'rb'))
                    print('response: ', response)
                    return response
            else:
                print('no file at: ', file_path)
                error_404_view(request, 'not available')
            # raise Http404
        else:
            error_404_view(request, 'not available')

# Attempt to load a 1-band rasterimage 'Testlayer' from disc and render it as map
# # def Eddytestdata(request):
# #     print('________________________- here: ', request)
# #     return FileResponse(open('/home/marcus/Nextcloud/BRIDGET/EC/Graswang_2014/Graswang_footprint_0012330.asc', 'rb'))
# #     return FileResponse(open('/home/marcus/Nextcloud/BRIDGET/EC/Graswang_2014/Graswang_footprint_0012330.tif', 'rb'))
# def Eddytestdata(request):
#     #     # url = '{0}/{1}/ows?service={2}&version=1.0.0&request=GetFeature&typeName={1}:{3}&outputFormat=application%2' \
#     #     #       'Fjson&srsname=EPSG:{4}&bbox={5},EPSG:{6}'.format(LOCAL_GEOSERVER, work_space_name, service, layer,
#     #     #                                                         srid, bbox, srid)
#     #     url = '{0}/NewRaster/wms?service=WMS&version=1.1.0&request=GetMap&layers=NewRaster:Graswang_footprint_0012330' \
#     #           '&styles=&bbox=652081.14,5269701.79,653681.14,5270869.79&width=768&height=560&srs=EPSG:25832' \
#     #           '&format=application/openlayers'.format(LOCAL_GEOSERVER)
#     url = 'http://localhost:8080/geoserver/NewRaster/wms?service=WMS&version=1.1.0&request=GetMap&layers=NewRaster:Graswang_footprint_0012330&styles=&bbox=652081.14,5269701.79,653681.14,5270869.79&width=768&height=560&srs=EPSG:25832&format=application/openlayers'
#     # url = 'http://localhost:8080/geoserver/NewRaster/wms?service=WMS&version=1.1.0&request=GetMap&layers=NewRaster:Graswang_footprint_0011930&styles=&bbox=652081.14,5269701.79,653681.14,5270869.79&width=768&height=560&srs=EPSG:25832&format=application/openlayers'
#     url = 'http://localhost:8080/geoserver/NewRaster/wms?service=WMS&version=1.1.0&request=GetMap&layers=NewRaster:Graswang_footprint_0011630&styles=&bbox=652081.14,5269701.79,653681.14,5270869.79&width=768&height=560&srs=EPSG:25832&format=application/openlayers'
#
#     request_url = urllib.request.Request(url)
#     response = urllib.request.urlopen(request_url)
#     print('response: ', response)
#     return HttpResponse(response.read().decode('utf-8'))
