import ast
import csv
import datetime
import json
import sys

import pandas as pd
import redis
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

import vfw_home
from author_manage.views import MyResourcesView
from heron.settings import LOCAL_GEOSERVER, DEMO_VAR, DATA_DIR

from vfw_home.geoserver_layer import create_layer, get_layer, delete_layer, test_geoserver_env
from vfw_home.previewplot import get_plot_from_db_id, get_bokeh_std_fullres, format_label, get_cache
from wps_gui.models import WpsResults
from .data_tools import __get_timescale, find_data_gaps, precision_to_minmax, is_data_short, DataTypes, \
    __get_axis_limits, __reduce_dataset, get_accessible_data
from .forms import QuickFilterForm
from .data_obj import DataObject
from .plot_obj import PlotObject
from .utilities import human_readable_bool, has_pending_embargo, read_data, expressive_layer_name, get_dataset, \
    get_paginatorpage

mpl.use('Agg')

from django.contrib.gis.geos import Polygon
from .query_functions import get_bbox_from_data
# from .filter import QuickFilter
from .filters import NMPersonsFilter
from .models import Entries, NmEntrygroups

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

class HomeView(TemplateView):
    """
    Template View to bring the necessary variables for the startup to the template
    """
    template_name = 'vfw_home/home.html'

    # Before you make migrations
    data_layer = 'devel'

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
            bla = Entries.objects.filter(pk=webID[2:]).values_list('datasource__data_names',
                                                                   'datasource__path',
                                                                   'datasource__datatype__parent',
                                                                   'datasource__datatype__name',
                                                                   'datasource__datatype__title',
                                                                   'datasource__datatype__description',
                                                                   'datasource__temporal_scale__resolution',
                                                                   'datasource__temporal_scale__observation_start',
                                                                   'datasource__temporal_scale__support',
                                                                   )

            dataset = DataObject(webID, date)

        except TypeError as e:
            print('\033[33mType error in Data Object:\033[0m ', e)
            raise Http404
        except IndexError as e:
            print('\033[33mindex error in Data Object:\033[0m ', e)
            if request.user.is_authenticated:
                # TODO: Rethink how to handle unallowed requests
                raise Http404
            else:
                # TODO: Redirect to login
                raise Http404
                # return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
                # return redirect('vfw_home:login')
        except EmptyResultSet as e:
            print('\033[33mEmptyResultSet Error in Data Object:\033[0m ', e)
            return JsonResponse({'error': e})
        except LookupError as e:
            print('\033[33mLookupError in Data Object:\033[0m ', e)
            return JsonResponse({'error': e})
        except FieldError as e:
            print('\033[33mField Error in Data Object:\033[0m ', e)
        except Exception as e:
            print('\033[31mAn unhandled error in Data Object func:\033[0m ', e)

        plot = PlotObject(dataset, plot_size)
        img = plot.get_plot
    return JsonResponse(img)

    if webID[0:2] == 'db':
        try:
            accessible_data = get_accessible_data(request, webID[2:])
            error_list = accessible_data['blocked']
            accessible_data = accessible_data['open']

            if len(accessible_data) < 1:
                return JsonResponse({'warning': translation.gettext(
                    'No plot available. <br/>First access to this dataset is needed.')})

            full_res = is_data_short(accessible_data[0], 'db', date)

            if type(full_res) is dict and 'error' in full_res:
                return JsonResponse(full_res)
            # plot with bokeh
            return JsonResponse(get_plot_from_db_id(ID=accessible_data[0], full_res=full_res, date=date))

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
            if len(df.index) > 50000:
                data = __reduce_dataset(df, full_res)

            if metadata['meta']['variable']['name'] in data['df'].columns:
                data['df'].rename(columns={metadata['meta']['variable']['name']: "value"}, inplace=True)
            elif metadata['meta']['variable']['name'].replace(" ", "_") in data['df'].columns:
                data['df'].rename(columns={metadata['meta']['variable']['name'].replace(" ", "_"): "value"}, inplace=True)
            else:
                print('Error: Unknown name of column name in your dataset. '
                      'Should be ', metadata['meta']['variable']['name'])

            if not 'tstamp' in data['df'].columns:
                data['df'] = data['df'].reset_index()

            if 'scale' in metadata:
                # TODO: scale should be in metadata. Add and get it here
                scale = metadata['scale']
            else:
                scale = __get_timescale(data['df'])

            # prepare dataset for plot
            if 'entry_id' in data['df']:
                del data['df']['entry_id']

            plot_data = {'df': data['df'], 'scale': scale}
            if 'precision' in plot_data['df'].columns and not data['df']['precision'].isnull().all():
                plot_data['df'] = precision_to_minmax(plot_data['df'])
                plot_data['has_preci'] = True
            else:
                plot_data['has_preci'] = False

            plot_data = find_data_gaps(plot_data)
            plot_data = __get_axis_limits(plot_data)
            return JsonResponse(get_bokeh_std_fullres(plot_data, full_res=full_res, size=[700, 500], label=label))

        if 'figure' in typelist:
            return JsonResponse('Warning: Not implemented yet.')

        raise Http404

    else:
        raise Http404


def short_info_pagination(request):
    """
    Requested from map.js buildMapModal, show only little metadata and give access to more details
    :param request:
    :return:
    """
    try:
        naive_today = timezone.make_naive(timezone.now())
        datasets = json.loads(request.GET.get('datasets'))
        if type(datasets) is str:
            datasets = [int(datasets)]

        field = ['title', 'id', 'variable__name', 'embargo', 'embargo_end']
        field_name = {'title': 'Title', 'variable__name': 'Variable name', 'id': 'ID', 'embargo': 'Embargo',
                      'has_access': 'has_access', 'embargo_end': 'embargo_end'}

        if datasets:
            entries_list = Entries.objects.values(*field).filter(pk__in=datasets) \
                .order_by('variable__name', 'title', 'id')
            accessible_data = get_accessible_data(request, datasets)
            # error_ids = accessible_data['blocked']
            accessible_ids = accessible_data['open']
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
        raise Http404

    except Exception as e:
        print('Exception while getting short info pagination: ', e)


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

        db_info = NmEntrygroups.objects.filter(entry_id=int(ids)).values(*get_queryvalues(prefix, nm_prefix))

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

        table = {'id': ids, translation.gettext('Name'): translation.gettext(db_info[0][prefix + 'variable__name'])}

        table[translation.gettext('Commercial use allowed')] = \
            human_readable_bool(db_info[0][prefix + 'license__commercial_use'])
        table[translation.gettext('Embargo')] = human_readable_bool(
            has_pending_embargo(db_info[0][prefix + 'embargo'], db_info[0][prefix + 'embargo_end']))
        table[translation.gettext('Abstract')] = translation.gettext(db_info[0][prefix + 'abstract']) \
            if db_info[0][prefix + 'abstract'] else '-'
        table['has_embargo'] = str(has_pending_embargo(db_info[0][prefix + 'embargo'], db_info[0][prefix + 'embargo_end']))

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

        result_dataset = NmEntrygroups.objects. \
            values('entry__id', 'entry__variable__name', 'entry__variable__symbol', 'entry__variable__unit__symbol',
                   'entry__datasource__datatype__name', 'group__title', 'group_id').filter(pk__in=accessible_ids)

        if len(error_ids) > 0:
            error_dict = {'message': 'no access', 'id': error_ids}

        for dataset in result_dataset:
            dataset_dict.update({'db' + str(dataset['entry__id']): {'name': dataset['entry__variable__name'],
                                                                    'abbr': dataset['entry__variable__symbol'],
                                                                    'unit': dataset['entry__variable__unit__symbol'],
                                                                    'type': dataset['entry__datasource__datatype__name'],
                                                                    'source': 'db',
                                                                    'dbID': dataset['entry__id'],
                                                                    'orgID': 'db' + str(dataset['entry__id']),
                                                                    'start': startdate,
                                                                    'end': enddate,
                                                                    'inputs': [],
                                                                    'outputs': dataset['entry__datasource__datatype__name'],
                                                                    'group': dataset['group__title'],
                                                                    'groupID': dataset['group_id']
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
    :return: dict with 'entries, ownData, accessible_ids' to render entrieslist.html
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
    elif len(datasets) == 0:
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


def advanced_filter(request):
    selection = Entries.objects.all().distinct('entry_id')
    advfilter = NMPersonsFilter(request.GET, queryset=selection)
    selection = advfilter.qs

    context = {'advFilter': advfilter, 'selection': selection}
    return render(request, 'vfw_home/advanced_filter.html', context)


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
    return render(request, 'vfw_home/404.html')


class DownloadView(View):
    """
    Give direct access to data without using the webportal
    """

    @staticmethod
    def get(request, name):

        if name == 'vfwVM':
            file_path = '/data/'
            if Path(file_path).exists():
                with open(file_path, 'rb') as fh:
                    response = FileResponse(open(file_path, 'rb'))
                    return response
            else:
                error_404_view(request, 'not available')
        else:
            error_404_view(request, 'not available')
