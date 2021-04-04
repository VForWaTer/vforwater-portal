import ast
import csv
import json
import sys
from json import JSONDecodeError

import requests
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from pyzip import PyZip

import matplotlib as mpl
import urllib
from collections import defaultdict
from django.conf import settings
from django.contrib.auth import logout
from django.http import StreamingHttpResponse
from django.http.response import JsonResponse, HttpResponse, Http404, FileResponse
from django.shortcuts import redirect, render
from django.utils import translation
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from future.builtins import isinstance

from author_manage.views import MyResourcesView
from heron.settings import LOCAL_GEOSERVER, DEBUG

from vfwheron.geoserver_layer import create_layer, get_layer, delete_layer, test_geoserver_env
from vfwheron.previewplot import get_preview, get_fullres_plot
from wps_gui.models import WpsResults
from .filters import VariableFilter
from .forms import AdvancedFilterForm

mpl.use('Agg')

from .query_functions import get_bbox_from_data
from datetime import datetime, date
import time
from .filter import FilterMethods, Menu, build_id_list, Table
from .filters import NMPersonsFilter
from .models import Entries, Timeseries, Timeseries2D, Generic1DData, Generic2DData, GenericGeometryData, \
    GeomTimeseries, NmPersonsEntries

import logging
import os
# for debugging:
from time import time
from django.db import connections

# Create your views here.
"""

"""
logger = logging.getLogger(__name__)



# from Django doc about session: If SESSION_EXPIRE_AT_BROWSER_CLOSE is set to True, Django will use browser-length
# cookies – cookies that expire as soon as the user closes their browser. Use this if you want people to have to log in
# every time they open a browser.
def expressive_layer_name(user: object) -> str:
    """
    Build an expressive name for the layer o the geoserver
    :param user:
    :return: String of user id + username + "_layer"
    """
    namestring = str(user.id) + "_"
    if user.first_name and user.last_name:
        namestring += (user.first_name + "_" + user.last_name)
    else:
        namestring += user.username.translate({ord(c): "_" for c in "!@#$%^&*()[]{};:,./<>?\|`=+"})

    return namestring + "_layer"


class HomeView(TemplateView):
    """
    Template View to bring the necessary variables for the startup to the template
    """
    template_name = 'vfwheron/home.html'

    # Before you make migrations
    Menu = Menu().get_menu()
    JSON_Menu = json.dumps(Menu['client'])
    data_layer = 'testlayer'

    # if not dataExt:
    data_ext = [645336.034469495, 6395474.75106861, 666358.204722283, 6416613.20733359]

    # IMPORTANT! Don't use "-" in geoserver names!!!
    store = 'teststore'
    workspace = 'testworkspace'
    unlocked_embargo = []

    try:
        test_geoserver_env(store, workspace)

    except:
        print('\033[91mno geoserver\033[0m ', sys.exc_info()[0])

    # TODO: Test with users if this makes any sense
    def __set_layer_name(self):
        """
        Set name for layer in geoserver according to username or as admin_layer.
        """
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                self.data_layer = 'admin_layer'
            else:
                self.data_layer = expressive_layer_name(self.request.user)

    # Put here everything you need at startup and for refresh of 'Home'
    def get_context_data(self, **kwargs: object):
        """
        Collect data needed for startup of V-FOR-WaTer Portal home.

        :param kwargs:
        :return:
        """
        self.__set_layer_name()

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
        except:
            self.data_layer = 'Error: Found no geoserver!'
            print('Still no geoserver: ', sys.exc_info()[0])

        self.data_ext = get_bbox_from_data()

        return {'dataExt': self.data_ext, 'Filter_Menu': self.JSON_Menu, 'data_layer': self.data_layer,
                'messages': messages.get_messages(self.request), 'unblocked_ids': unblocked_ids}


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


def get_accessible_data(request: object, requested_ids: list) -> (list, list):
    """
    Use request object to check if user has read access to a list of data (entries_id). Output is a list with
    accessible data and a second list with inaccessible data.

    :param request:
    :param requested_ids:
    :return: accessible_ids, error_ids
    """
    if isinstance(requested_ids, int):
        requested_ids = [requested_ids]
    elif isinstance(requested_ids, str):
        requested_ids = [int(requested_ids)]
    # first get datasets without embargo / open for for everyone
    accessible_data = list(Entries.objects.
                           values_list('id', flat=True).filter(pk__in=requested_ids, embargo=False))
    # check if the user wanted more and is authenticated. If yes check if user has access and get the rest
    if len(requested_ids) > len(accessible_data) and request.user.is_authenticated:
        accessible_embargo_datasets = list(set(requested_ids) & set(request.session['datasets']))  # intersect sets
        accessible_data.extend(accessible_embargo_datasets)
    # check if there is still data not accessible and create error for these
    error_list = list(set(requested_ids) - set(accessible_data))
    return {'open': accessible_data, 'blocked': error_list}


def get_dataset(s_id: int) -> object:
    """

    :param s_id: ID in metacatalob
    :return:
    """
    entry_type = Entries.objects.filter(pk=s_id).values_list('datasource__datatype__name', flat=True)[0]

    # build string of values for django query
    type_values = {'generic1ddata': ['index', 'value', 'precision'],
                   'generic2ddata': ['index', 'value1', 'value2', 'precision1', 'precision2'],
                   'genericgeometrydata': ['index', 'geom', 'srid'],
                   'geomtimeseries': ['tstamp', 'geom', 'srid'],
                   'timeseries': ['tstamp', 'value', 'precision'],
                   'timeseries2d': ['tstamp', 'value1', 'value2', 'precision1', 'precision2']}
    db_values = type_values[entry_type]

    query_values = []
    for value in db_values:
        query_values.append('{}__{}'.format(entry_type, value))

    query_filter = {entry_type: s_id}
    return Entries.objects.filter(**query_filter).values_list(*query_values)


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

        # TODO: schema Location shows too much information for possible intruder. Figure out how to improve?
        if 'xml' in request.GET:
            id = request.GET.get('xml')
            accessible_data = get_accessible_data(request, id)
            error_list = accessible_data['blocked']
            accessible_data = accessible_data['open']

            if len(accessible_data) > 0:
                layer_name = 'XML_{}_{}_{}'.format(request.user, request.user.id, id)
                srid = 4326
                # create layer on geoserver to request xml file
                create_layer(request, layer_name, store, workspace, id)
                # use GEOSERVER GML
                url = '{0}/{1}/ows?service=wfs&version=1.0.0&request=GetFeature&typeName={1}:{2}&outputFormat=' \
                      'text%2Fxml%3B%20subtype%3Dgml%2F2.1.2&&srsname=EPSG:{3}'.format(LOCAL_GEOSERVER,
                                                                                       workspace, layer_name, srid)
                request = urllib.request.Request(url)
                response = urllib.request.urlopen(request)
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
            return redirect('vfwheron:watts_rsp:login_init')
        elif settings.DEBUG:  # default django login
            return redirect('vfwheron:login')
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
            logger.debug('{} logged in as'.format(request.user.username))

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
        logger.debug('{} logged out'.format(request.user.username))
        logout(request)

    def post(self, request):
        """

        :param request:
        :type request:
        :return:
        :rtype:
        """
        self.logout(request)
        return redirect('vfwheron:home')


class DevLoginView(TemplateView):

    def get(self, request):
        context = {}
        return render(request, 'home/login.html', {'context': context})


class HelpView(TemplateView):
    """

    """

    def get(self, request):
        """

        :param request:
        :type request:
        :return:
        :rtype:
        """
        f = open(os.path.join(settings.BASE_DIR, 'USERHELP.md'), 'r')
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

        :param request:
        :type request:
        :return:
        :rtype:
        """
        lang = translation.get_language()
        logger.debug('current language: {}'.format(lang))
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
        logger.debug('new language: {}'.format(translation.get_language()))
        logger.debug('translation test: {}'.format(translation.gettext("help")))
        return redirect('/')


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
        return redirect('vfwheron:home')


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
        work_space_name = HomeView.workspace  # 'CAOS_update'
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
    webID = request.GET.get('preview')
    if webID[0:2] == 'db':
        try:
            accessible_data = get_accessible_data(request, webID[2:])
            error_list = accessible_data['blocked']
            accessible_data = accessible_data['open']
            # plot with bokeh
            return JsonResponse(get_fullres_plot(accessible_data[0]))

        except TypeError as e:
            print('Type error in previewplot: ', e)
            raise Http404
        except IndexError as e:
            if request.user.is_authenticated:
                # TODO: Rethink how to handle unallowed requests
                print('Index Error in previewplot: ', e)
                raise Http404
            else:
                # TODO: Redirect to login
                raise Http404
        except Exception as e:
            print('\033[31mAn unhandled error in previewplot func:\033[0m ', e)

    elif webID[0:3] == 'wps':
        print('def previewplot: You have to implement something to show wps results!')
        print('webID: ', webID)
        dataset = WpsResults.objects.filter(id=webID[3::])
        typelist = ast.literal_eval(dataset.values('outputs')[0]['outputs'])
        print('typelist: ', typelist)
        if 'figure' in typelist:
            return JsonResponse('Warning: Not implemented yet.')

        raise Http404

    else:
        raise Http404


def short_datainfo(request):
    """
    Requested from map.js popupContent
    :param request:
    :return:
    """
    try:
        ids = json.loads(request.GET.get('short_info'))
        field = ['title', 'variable__name', 'embargo']
        field_name = {'title': 'Titel', 'variable__name': 'Variablenname', 'embargo': 'Embargo'}
        preview = defaultdict(list)

        for k in ids:
            row_name = Entries.objects.filter(id=str(k)).values(*field)
            counter = 0
            for i in row_name[0]:
                if counter == 1:
                    preview['id'].append(k)
                counter += 1
                preview[translation.gettext(field_name[i])].append(str(row_name[0][i]).title())

        return JsonResponse(preview)

    except TypeError:
        raise Http404


def filter_selection(request):
    """
    get selection as json Object from js getCountFromServer() and send int(as json) with amount of items back
    :param request:
    :return:
    """
    try:
        return JsonResponse(FilterMethods.selection_counts(HomeView.Menu['server'],
                                                           json.loads(request.GET.get('filter_selection'))))

    except TypeError:
        raise Http404


def filter_map_selection(request):
    try:
        m_ids = None
        entry_ids = build_id_list(HomeView.Menu['server'], json.loads(request.GET.get('filter_map_selection')))
        dataExt = get_bbox_from_data(entry_ids['all_filters'])
        print('request.user: ', request.user)
        id_layer = 'ID_layer' + str(request.user)
        if get_layer(id_layer, HomeView.store, HomeView.workspace):
            delete_layer(id_layer, HomeView.store, HomeView.workspace)
        create_layer(request, id_layer, HomeView.store, HomeView.workspace, str(entry_ids['all_filters'])[1:-1])
        m_ids = entry_ids['all_filters']
        # TODO: Instead of recreating the layer on each click, add a hash to the name and build only none
        # existing layers
        # ID_layer = 'ID_layer' + str(hashlib.md5(str(entry_ids['all_filters'])[1:-1].encode())) # + user
        # if not get_ID_layer(ID_layer):
        #     create_ID_layer(ID_layer, str(entry_ids['all_filters'])[1:-1])
        #             else:
        # # TODO: don't do that in production! That's just for development to make sure geoserver is updatet after
        #  restart of django
        #                 delete_ID_layer(ID_layer)
        #                 create_ID_layer(ID_layer, str(entry_ids['all_filters'])[1:-1])
        print('ID_layer ', id_layer)
        print('IDs ', m_ids)
        return JsonResponse({'ID_layer': id_layer, 'dataExt': dataExt, 'IDs': m_ids})

    except TypeError:
        raise Http404


# TODO: maybe it's enough to send here only a list with values, and load the list with fields in Homeview?
# TODO: Handle this with an http request!
def show_info(request):
    """
    On request collect metadata for preview on map and selection in the sidebar.
    Requested from map.js show_info.
    :param request:
    :return:
    """

    def collectData(ids):
        """

        :param ids: ID, styled depending on sender. E.g. could be wps12, db12 or just 12.
        :type ids: str
        :return: dict
        """
        # get field names from models:
        field = []
        field_name = {}
        for i in Menu().menu_list:
            for j in i.db_alias_child.items():
                fieldpath = j[0] if i.path == '' else i.path + '__' + j[0]
                field.append(fieldpath)
                field_name[fieldpath] = j[1]
        # build dict of lists for preview:
        preview = defaultdict(list)
        preview['id'].append(ids)
        imgtag = Entries.objects.filter(id=str(ids)).values(*field)

        for i in imgtag[0]:
            if imgtag[0][i] is not None:
                preview[translation.gettext(field_name[i])].append(str(imgtag[0][i]))
            else:
                preview[translation.gettext(field_name[i])].append('-')

        return JsonResponse(preview)

    webID = request.GET.get('show_info')
    if webID[0:3] == 'wps':
        print('you have to implement something to show wps results!')
        raise Http404
    else:
        if webID[0:2] == 'db':
            ids = webID[2:]
        else:
            ids = webID

        try:
            return collectData(ids)

        except TypeError:
            raise Http404


def workspace_data(request):
    """

    :param request:
    :return:
    """

    def build_selection(requested_id, min_time=0, max_time=0):
        """
        function distinguishes only between default user (non-embargo data) and rest (+user embargo data)
        :param requested_id:
        :param min_time:
        :param max_time:
        :return:
        """
        dataset_dict = {}
        error_dict = {}

        accessible_data = get_accessible_data(request, requested_id)
        error_ids = accessible_data['blocked']
        accessible_ids = accessible_data['open']

        result_dataset = Entries.objects. \
            values('id', 'variable__name', 'variable__symbol', 'variable__unit__symbol',
                   'datasource__datatype__name').filter(pk__in=accessible_ids)

        if len(error_ids) > 0:
            error_dict = {'message': 'no access', 'id': error_ids}

        for dataset in result_dataset:
            dataset_dict.update({'db' + str(dataset['id']): {'name': dataset['variable__name'],
                                                             'abbr': dataset['variable__symbol'],
                                                             'unit': dataset['variable__unit__symbol'],
                                                             'type': dataset['datasource__datatype__name'],
                                                             'source': 'db',
                                                             'dbID': dataset['id'],
                                                             'orgID': 'db' + str(dataset['id']),
                                                             'start': '',
                                                             'end': '',
                                                             'inputs': [],
                                                             'outputs': dataset['datasource__datatype__name']
                                                             }
                                 })

        # TODO: Need timestamp in name to see if different selection
        return {'data': dataset_dict, 'error': error_dict}

    try:
        min_time = request.GET.get('minTime')
        max_time = request.GET.get('maxTime')
        # prepare dataset_iddatasetdownload differently for list and single value to use in build_selection
        result = build_selection(json.loads(request.GET.get('workspaceData')), min_time, max_time)
        return JsonResponse({'workspaceData': result['data'], 'error': result['error']})

    except TypeError:
        raise Http404


def entries_pagination(request):
    """

    :param request: list of integers
    :type request: object
    :return:
    """
    datasets = json.loads(request.GET.get('datasets', 1))
    if datasets:
        # entries_list = NmPersonsEntries.objects.all().order_by('entry__title').filter(entry_id=datasets).distinct()
        entries_list = Entries.objects.all().order_by('title').filter(
            pk__in=json.loads(request.GET.get('datasets', 1)))
    else:
        entries_list = Entries.objects.all().order_by('title')
    try:
        owndata = request.session['datasets']
    except KeyError:
        owndata = None

    page = request.GET.get('page', 1)
    paginator = Paginator(entries_list, 5)
    try:
        entriespage = paginator.page(page)
    except PageNotAnInteger:
        entriespage = paginator.page(1)
    except EmptyPage:
        entriespage = paginator.page(paginator.num_pages)

    return render(request, 'vfwheron/entrieslist.html', {'entries': entriespage,
                                                         'ownData': owndata})


def advanced_filter(request):
    selection = NmPersonsEntries.objects.all().distinct('entry_id')

    filter = NMPersonsFilter(request.GET, queryset=selection)
    selection = filter.qs

    context = {'advFilter': filter, 'selection': selection}
    return render(request, 'vfwheron/advanced_filter.html', context)


def error_404_view(request, exception):
    return render(request, 'vfwheron/404.html')


class DownloadView(View):
    """
    Give direct access to data without using the webportal
    """

    @staticmethod
    def get(request, name):

        if name == 'vfwVM':

            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = FileResponse(open(file_path, 'rb'))
                    print('response: ', response)
                    return response
            else:
                print('no file at: ', file_path)
                error_404_view(request, 'not available')
        else:
            error_404_view(request, 'not available')
