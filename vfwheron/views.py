import ast
import csv
import datetime
import json
import sys

import pandas as pd
import requests
from django.contrib.gis.db.models.aggregates import Extent
from django.core.exceptions import EmptyResultSet, FieldError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
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
from future.builtins import isinstance

import vfwheron
from author_manage.views import MyResourcesView
from heron.settings import LOCAL_GEOSERVER, DEMO_VAR, DATA_DIR

from vfwheron.geoserver_layer import create_layer, get_layer, delete_layer, test_geoserver_env
from vfwheron.previewplot import get_plot_from_db_id, get_bokeh_std_fullres, format_label
from wps_gui.models import WpsResults
from .data_tools import __get_timescale, fill_data_gaps, precision_to_minmax, is_data_short, DataTypes, \
    __get_axis_limits, __reduce_dataset
from .forms import QuickFilterForm

mpl.use('Agg')

from django.contrib.gis.geos import Polygon
from .query_functions import get_bbox_from_data
# from .filter import QuickFilter
from .filters import NMPersonsFilter
from .models import Entries

import logging
from pathlib import Path
# for debugging:
from time import time

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

        context = quick_filter_defaults(self)

        return {'dataExt': self.data_ext, 'data_layer': self.data_layer,
                'messages': messages.get_messages(self.request), 'unblocked_ids': unblocked_ids,
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
    type_values = {'generic_1d_data': ['index', 'value', 'precision'],
                   'generic_2d_data': ['index', 'value1', 'value2', 'precision1', 'precision2'],
                   'generic_geometry_data': ['index', 'geom', 'srid'],
                   'geom_timeseries': ['tstamp', 'geom', 'srid'],
                   'timeseries_1d': ['tstamp', 'value', 'precision'],
                   'timeseries_2d': ['tstamp', 'value1', 'value2', 'precision1', 'precision2']}
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


class Legals(TemplateView):
    """

    """

    def get(self, request):
        """

        :param request:
        :type request:
        :return:
        :rtype:
        """

        return render(request, 'vfwheron/legals.html')


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
    full_res = False
    if request.GET.get('startdate') != 'None':
        date = [make_aware(datetime.datetime.strptime(request.GET.get('startdate'), '%Y-%m-%d')),
                make_aware(datetime.datetime.strptime(request.GET.get('enddate'), '%Y-%m-%d'))]
    else:
        date = None

    if webID[0:2] == 'db':
        try:
            accessible_data = get_accessible_data(request, webID[2:])
            error_list = accessible_data['blocked']
            accessible_data = accessible_data['open']

            # accessible_data = [1078]

            full_res = is_data_short(accessible_data[0], 'db', date)
            # plot with bokeh
            return JsonResponse(get_plot_from_db_id(ID=accessible_data[0], full_res=full_res, date=date))
            # else:
            # return JsonResponse(get_preview(accessible_data[0]))

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
                # return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
                # return redirect('vfwheron:login')
        except EmptyResultSet as e:
            print('EmptyResultSet Error in previewplot: ', e)
        except FieldError as e:
            print('Field Error in previewplot: ', e)
        except Exception as e:
            print('\033[31mAn unhandled error in previewplot func:\033[0m ', e)

    elif webID[0:3] == 'wps':
        dataset = WpsResults.objects.filter(id=webID[3:])
        typelist = ast.literal_eval(dataset.values('outputs')[0]['outputs'])
        path = DATA_DIR + typelist['path'][1::]
        with open(path + ".json") as json_file:
            metadata = json.loads(json.load(json_file))
        json_file.close()
        label = format_label(metadata['meta']['variable']['name'],
                             metadata['meta']['variable']['symbol'],
                             metadata['meta']['variable']['unit']['symbol'])

        if typelist['type'] == 'timeseries':
            dataReader = DataTypes()
            df = dataReader.read_data(filepath=path, datatype=typelist['type'])
            # df = pd.read_csv(path + ".csv")
            # df['tstamp'] = pd.to_datetime(df['tstamp'])
            if len(df.index) > 50000:
                df = __reduce_dataset(df, full_res)

            if metadata['meta']['variable']['name'] in df.columns:
                df.rename(columns={metadata['meta']['variable']['name']: "value"}, inplace=True)
            elif metadata['meta']['variable']['name'].replace(" ", "_") in df.columns:
                df.rename(columns={metadata['meta']['variable']['name'].replace(" ", "_"): "value"}, inplace=True)
            else:
                print('Error: Unknown name of column name in your dataset. '
                      'Should be ', metadata['meta']['variable']['name'])

            if not 'tstamp' in df:
                # df['tstamp'] = df.index.values
                df = df.reset_index()

            if 'scale' in metadata:
                # TODO: scale should be in metadata. Add and get it here
                scale = metadata['scale']
            else:
                scale = __get_timescale(df)

            # prepare dataset for plot
            if 'entry_id' in df:
                del df['entry_id']

            plot_data = {'df': df, 'scale': scale}
            # timescale = pd.to_timedelta(timescale)
            # plotdata = {'data': result, 'df': df, 'axis': axis, 'scale': timescale}
            if 'precision' in plot_data['df'].columns and not df['precision'].isnull().all():
                plot_data['df'] = precision_to_minmax(plot_data['df'])
                plot_data['has_preci'] = True
            else:
                plot_data['has_preci'] = False

            plot_data = fill_data_gaps(plot_data)
            plot_data = __get_axis_limits(plot_data)
            # print('11 wps: ', plot_data)
            # return JsonResponse(get_plot(ID=plot_data))
            return JsonResponse(get_bokeh_std_fullres(plot_data, full_res=full_res, size=[700, 500], label=label))

        if 'figure' in typelist:
            return JsonResponse('Warning: Not implemented yet.')

        raise Http404

    else:
        raise Http404


def short_info_pagination(request):
    """
    Requested from map.js popupContent
    :param request:
    :return:
    """
    try:
        datasets = json.loads(request.GET.get('datasets'))
        page = request.GET.get('page', 1)

        field = ['title', 'id', 'variable__name', 'embargo', 'embargo_end']
        field_name = {'title': 'Title', 'variable__name': 'Variable name', 'id': 'ID', 'embargo': 'Embargo',
                      'has_access': 'has_access', 'embargo_end': 'embargo_end'}

        if datasets:
            entries_list = Entries.objects.values(*field).filter(pk__in=datasets)\
                .order_by('variable__name', 'title', 'id')
            accessible_data = get_accessible_data(request, datasets)
            error_ids = accessible_data['blocked']
            accessible_ids = accessible_data['open']
        else:
            entries_list = Entries.objects.values(*field).order_by('variable__name', 'title', 'id')

        naive_today = timezone.make_naive(timezone.now())
        paginator = Paginator(entries_list, 5)

        try:
            orgpage = paginator.page(page)
        except PageNotAnInteger:
            orgpage = paginator.page(1)
        except EmptyPage:
            orgpage = paginator.page(paginator.num_pages)

        # TODO: That is to blame for having nothing in web site
        newdict = defaultdict(list)
        for d in orgpage:
            for key, val in d.items():
                if key != 'embargo_end':
                    newdict[translation.gettext(field_name[key])].append(val)
                else:
                    if val < naive_today or d['embargo'] is False or d['id'] in accessible_ids:
                        newdict['has_access'].append({'access': True, 'ssid': d['id']})
                    else:
                        newdict['has_access'].append({'access': False, 'ssid': d['id']})

        entries = dict(newdict.items())

        return render(request, 'vfwheron/mapmodal_entrieslist.html', {'entries_page': entries,
                                                                      'data_sets': datasets,
                                                                      'org_page': orgpage})

    except TypeError:
        raise Http404

# TODO: maybe it's enough to send here only a list with values, and load the list with fields in Homeview?
# TODO: Handle this with an http request (response, not request?)!
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
        # build dict of lists for preview:
        db_info = Entries.objects.filter(id=int(ids))\
            .values('uuid', 'variable__name', 'license__commercial_use', 'embargo', 'embargo_end', 'abstract',
                    'datasource__temporal_scale__observation_start', 'datasource__temporal_scale__observation_end')
        # table = {}
        # table['id'] = ids
        # table[translation.gettext('Name')] = translation.gettext(db_info[0]['variable__name'])
        table = {'id': ids,
                 translation.gettext('Name'): translation.gettext(db_info[0]['variable__name'])}
        table[translation.gettext('Commercial use allowed')] = translation.gettext('Yes') \
            if db_info[0]['license__commercial_use'] else translation.gettext('No')
        table[translation.gettext('Embargo')] = translation.gettext('Yes') \
            if db_info[0]['embargo'] == 'True' and timezone.now() < db_info[0]['embargo_end'].astimezone() \
            else translation.gettext('No')
        table[translation.gettext('Abstract')] = translation.gettext(db_info[0]['abstract']) \
            if db_info[0]['abstract'] else '-'

        return JsonResponse(table)

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

    def build_selection(requested_id, startdate='', enddate=''):
        """
        function distinguishes only between default user (non-embargo data) and rest (+user embargo data)
        :param requested_id:
        :param startdate: string
        :param enddate: string
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
                                                             'start': startdate,
                                                             'end': enddate,
                                                             'inputs': [],
                                                             'outputs': dataset['datasource__datatype__name']
                                                             }
                                 })

        # TODO: Need timestamp in name to see if different selection
        return {'data': dataset_dict, 'error': error_dict}

    try:
        # prepare dataset_iddatasetdownload differently for list and single value to use in build_selection
        result = build_selection(json.loads(request.GET.get('workspaceData')),
                                 request.GET.get('startDate'), request.GET.get('endDate'))
        return JsonResponse({'workspaceData': result['data'], 'error': result['error']})

    except TypeError:
        raise Http404


def entries_pagination(request):
    """
    Return result in several pages (5 datasets per page) instead of hundreds of results on one page.

    :param request: list of integers
    :type request: object
    :return:
    """
    accessible_ids = []
    datasets = json.loads(request.GET.get('datasets', 1))
    field = {'id', 'embargo', 'title', 'version', 'citation', 'abstract', 'variable__name', 'variable__symbol',
             'variable__unit__symbol', 'variable__keyword__value',
             'datasource__datatype__name', 'datasource__temporal_scale__resolution',
             'datasource__temporal_scale__observation_start', 'datasource__temporal_scale__observation_end',
             'datasource__spatial_scale__extent', 'license__short_title', 'license__title'}
    if datasets:
        entries_list = Entries.objects.values(*field).order_by('title').filter(pk__in=datasets)
        accessible_data = get_accessible_data(request, datasets)
        error_ids = accessible_data['blocked']
        accessible_ids = accessible_data['open']
    else:
        entries_list = Entries.objects.values(*field).order_by('title')
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
                                                         'ownData': owndata,
                                                         'accessible_ids': accessible_ids})


def advanced_filter(request):
    # selection = NmPersonsEntries.objects.all().distinct('entry_id')
    selection = Entries.objects.all().distinct('entry_id')
    advfilter = NMPersonsFilter(request.GET, queryset=selection)
    selection = advfilter.qs

    context = {'advFilter': advfilter, 'selection': selection}
    return render(request, 'vfwheron/advanced_filter.html', context)


def quick_filter_defaults(request):
    total = Entries.objects.exclude(Q(embargo=True) & Q(embargo_end__gte=timezone.now())).count()

    quickfilter = QuickFilterForm()
    more = QuickFilterForm.More()
    selection = []
    return {'quickfilter': quickfilter, 'more': more, 'selection': selection, 'total': total}


class QuickFilter(View):

    @staticmethod
    def get(request):
        context = quick_filter_defaults(request)
        return render(request, 'vfwheron/quick_filter.html', context)


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
        data_ext = [7.574234, 47.581351, 10.351323, 49.625873]  # an arbitrarily zoom location for NO RESULT
        if query:
            data_ext = list(query.aggregate(Extent('location'))['location__extent'])

        IDs = list(query.values_list('id', flat=True))
        id_layer = 'ID_layer' + str(request.user)
        if get_layer(id_layer, HomeView.store, HomeView.workspace):
            delete_layer(id_layer, HomeView.store, HomeView.workspace)

        if IDs:
            create_layer(request, id_layer, HomeView.store, HomeView.workspace, str(IDs)[1:-1])
        else:
            # TODO: Selection with no result has to be handled properly
            pass

        return JsonResponse({'selection': selection, 'total': total_results,
                             'ID_layer': id_layer, 'dataExt': data_ext, 'IDs': IDs})


def error_404_view(request, exception):
    return render(request, 'vfwheron/404.html')


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
        else:
            error_404_view(request, 'not available')
