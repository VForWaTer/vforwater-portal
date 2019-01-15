import base64
import csv
import decimal
import hashlib
import json
import zipfile
from builtins import filter
from wsgiref.util import FileWrapper

import requests
from pyzip import PyZip

import matplotlib as mpl
import urllib
from collections import defaultdict
from django.conf import settings
from django.contrib.auth import logout
from django.core.cache import cache
from django.db import connections
from django.http import StreamingHttpResponse
from django.http.response import JsonResponse, HttpResponse
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.utils import translation
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from django.template import RequestContext

from future.builtins import isinstance

from heron.settings import LOCAL_GEOSERVER
from io import StringIO, BytesIO

from vfwheron.geoserver_layer import create_layer, get_layer, delete_layer, create_id_layer, create_data_layer, \
    test_geoserver_env
from vfwheron.previewplot import get_preview

mpl.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib import pylab
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure

from .query_functions import get_bbox_from_data
from datetime import datetime, date
import time

from .filter import FilterMethods, Menu, build_id_list, Table
from .models import TblMeta, TblVariable, TblData

import logging
import os
# for debugging:
from time import time
from django.db import connections

# Create your views here.
"""

"""
logger = logging.getLogger(__name__)


def get_dataset(self, request, **kwargs):
    """

    :param self:
    :type self:
    :param request:
    :type request:
    :param kwargs:
    :type kwargs:
    :return:
    :rtype:
    """
    # here
    m_id = request.POST.get('meta_id')

    data = TblData.objects.get(meta=m_id).value
    result = "test"

    return result


class WorkflowView(TemplateView):
    """
    Template View for plain workflow HTML Template.
    Template so far does only contain iframe in content Block, that embedds wps_workflow app
    """
    template_name = "vfwheron/workflow.html"


# from Django doc about session: If SESSION_EXPIRE_AT_BROWSER_CLOSE is set to True, Django will use browser-length
# cookies – cookies that expire as soon as the user closes their browser. Use this if you want people to have to log in
# every time they open a browser.
class HomeView(TemplateView):
    """
    Template View to bring the necessary variables for the startup to the template
    """
    template_name = 'vfwheron/home.html'
    user = 'default'
    Menu = Menu().menu(user)
    # print(connections['vforwater'].queries)
    # print(len(connections['vforwater'].queries))
    JSON_Menu = json.dumps(Menu['client'])
    data_layer = 'testlayer2'#'default_layer_prod'

    # JSON_Menu = Menu().json_menu()
    # if not dataExt:
    data_ext = [645336.034469495, 6395474.75106861, 666358.204722283, 6416613.20733359]

    store = 'teststore2'#'new_vforwater_gis'
    workspace = 'testworkspace2'#'CAOS_update'
    test_geoserver_env(store, workspace)

    # dataExt = get_bbox_from_data()

    # TODO: Test with users if this makes any sense
    def set_layer_name(self):
        if self.request.user.is_authenticated:
            data_layer = 'default_layer'
        else:
            data_layer = self.data_layer
        return data_layer

    # Put here everything you need at startup and for refresh
    def get_context_data(self, **kwargs):

        self.data_layer = self.set_layer_name()

        if not get_layer(self.data_layer, self.store, self.workspace):
            create_layer(self.request, self.data_layer, self.store, self.workspace)
        else:
            # TODO: don't do that in production! That's just for development to make sure geoserver is updated after
            # restart of django
            delete_layer(self.data_layer, self.store, self.workspace)
            create_layer(self.request, self.data_layer, self.store, self.workspace)

        try:
            data_ext = get_bbox_from_data()
        except:
            data_ext = [645336.034469495, 6395474.75106861, 666358.204722283, 6416613.20733359]
            logger.warning('Data Extend cannot be loaded in views.py. Using fixed values.')
        return {'dataExt': data_ext, 'Filter_Menu': self.JSON_Menu, 'data_layer': self.data_layer,
                'messages': messages.get_messages(self.request)}


class MenuView(TemplateView):
    """
    View to build the filter menu on the start page and interact with the sidebar
    """

    # user = 'default'

    def get(self, request, user='default'):
        """

        :param request:
        :type request:
        :param user:
        :type user:
        :return:
        :rtype:
        """

        request.session.set_expiry(20)  # TODO: expire after 20 seconds/ this is only for development!!!

        # bring last used menu to session
        if 'menu' in request.GET:
            request.session['menu'] = request.GET.get('menu')
            request.session.modified = True
        else:
            menu = request.session.get('menu')

        # build_selection is called if the following request.GET.get('workspaceData') is true
        def build_selection(work_dataset, dataset_dict, min_time=0, max_time=0):
            data_definition = {}
            work_query = 'SELECT tbl_data.tstamp, tbl_data.value FROM public.tbl_data WHERE tbl_data.meta_id = ' + \
                         work_dataset
            if min_time != 0:
                work_query = work_query + 'AND tbl_data.tstamp > ' + str(min_time)
            if max_time != 0:
                work_query = work_query + 'AND tbl_data.tstamp < ' + str(max_time)

            definition_query = TblMeta.objects.values('variable__variable_name', 'variable__variable_abbrev',
                                                      'variable__unit__unit_abbrev').get(pk=work_dataset)
            data_definition['name'] = definition_query['variable__variable_name']
            data_definition['abbr'] = definition_query['variable__variable_abbrev']
            data_definition['unit'] = definition_query['variable__unit__unit_abbrev']

            # if 'work_dataset_dict' in request.session:
            if dataset_dict != {}:
                # TODO: Need timestamp in name to see if different selection
                dataset_dict.update({work_dataset: data_definition})
            else:
                dataset_dict = {work_dataset: data_definition}
            return dataset_dict

        if 'workspaceData' in request.GET:
            min_time = request.GET.get('minTime')
            max_time = request.GET.get('maxTime')
            result = {}
            # prepare work_dataset differently for list and single value to use in build_selection
            conv_work_dataset = json.loads(request.GET.get('workspaceData'))
            if type(conv_work_dataset) == list:
                for datasetId in conv_work_dataset:
                    result = build_selection(str(datasetId), result, min_time, max_time)
            elif type(conv_work_dataset) == int:
                result = build_selection(str(conv_work_dataset), result, min_time, max_time)
            return JsonResponse({'workspaceData': result})

        if 'preview' in request.GET:
            # plot png the mälicke way:
            imgtag = get_preview(request.GET.get('preview'))
            return JsonResponse({'get': imgtag})  # requested from vfw.js show_preview

        # TODO: maybe it's enough to send here only a list with values, and load the list with fields in Homeview?
        # on request collect metadata for preview on map ans selection in the sidebar
        if 'show_info' in request.GET:
            # get field names from models:
            field = []
            field_name = {}
            for i in Menu().menu_list:
                for j in i.column_dict.items():
                    fieldpath = j[0] if i.path == '' else i.path + '__' + j[0]
                    field.append(fieldpath)
                    field_name[fieldpath] = j[1]

            # build dict of lists for preview:
            ids = json.loads(request.GET.get('show_info'))
            preview = defaultdict(list)
            for k in ids:
                preview['id'].append(k)
                imgtag = TblMeta.objects.filter(id=str(k)).values(*field)

                for i in imgtag[0]:
                    # preview[translation.gettext(field_name[i])].append(str(imgtag[0][i]))
                    preview[translation.gettext(field_name[i])].append(str(imgtag[0][i])) if imgtag[0][
                                                                                                 i] is not None else \
                        preview[translation.gettext(field_name[i])].append('-')

            # remove rows only containing no value:
            comparelist = ['-'] * len(ids)
            deleteable = []
            for i in preview:
                if preview[i] == comparelist:
                    deleteable.append(i)
            for i in deleteable:
                del preview[i]

            return JsonResponse({'get': preview})  # requested from map.js show_info

# get selection as json Object from js getCountFromServer() and send int(as json) with amount of items back
        if 'filter_selection' in request.GET:
            filter_menu = FilterMethods.selection_counts(HomeView.Menu['server'],
                                                         json.loads(request.GET.get('filter_selection')))
            return JsonResponse(filter_menu)

        if 'filter_selection_map' in request.GET:
            m_ids = None
            if json.loads(request.GET.get('filter_selection_map')) == 0:
                id_layer = HomeView.set_layer_name(self)
                dataExt = get_bbox_from_data()
            else:
                meta_ids = build_id_list(HomeView.Menu['server'], json.loads(request.GET.get('filter_selection_map')))
                dataExt = get_bbox_from_data(str(meta_ids['all_filters'])[1:-1])
                id_layer = 'ID_layer'  # + user
                if get_layer(id_layer, HomeView.store, HomeView.workspace):
                    delete_layer(id_layer, HomeView.store, HomeView.workspace)
                create_id_layer(request, id_layer, str(meta_ids['all_filters'])[1:-1], HomeView.store, HomeView.workspace)
                m_ids = meta_ids['all_filters']
                # TODO: Instead of recreating the layer on each click, add a hash to the name and build only none
                # existing layers
                # ID_layer = 'ID_layer' + str(hashlib.md5(str(meta_ids['all_filters'])[1:-1].encode())) # + user
                # if not get_ID_layer(ID_layer):
                #     create_ID_layer(ID_layer, str(meta_ids['all_filters'])[1:-1])
            #             else:
            # # TODO: don't do that in production! That's just for develpment to make sure geoserver is updatet after
            #  restart of django
            #                 delete_ID_layer(ID_layer)
            #                 create_ID_layer(ID_layer, str(meta_ids['all_filters'])[1:-1])
            return JsonResponse({'ID_layer': id_layer, 'dataExt': dataExt, 'IDs': m_ids})

        return JsonResponse({'Error': 'Something about your data is missing. Tell admin to check views.py'})


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

    def get(self, request, user='default'):
        """

        :param request:
        :type request:
        :param user:
        :type user:
        :return:
        :rtype:
        """
        store = HomeView.store  # 'new_vforwater_gis'
        workspace = HomeView.workspace  # 'CAOS_update'
        test_geoserver_env(store, workspace)
        print('im get')

        def get_metadata(m_id):
            """
            the metadata for export includes only the values that are also used for filtering.
            Change get_metadata if you want to have more information in the export file.
            :return:
            """
            catalog = {}
            for table in Menu.menu_list:
                for i in table.column_dict:
                    if table.path != '':
                        query = TblMeta.objects.filter(pk=m_id).values_list(table.path + '__' + i, flat=True)
                    else:
                        query = TblMeta.objects.filter(pk=m_id).values_list(i, flat=True)
                    if query[0] is not None:
                        try:
                            catalog[table.menu_name][i] = query[0]
                        except KeyError:
                            catalog[table.menu_name] = {i: query[0]}
            return catalog

        if 'csv' in request.GET:
            # if 'download_data' in request.GET:
            rows = TblMeta.objects.values_list('tbldata__tstamp', 'tbldata__value').filter(
                pk=json.loads(request.GET.get('csv')))
            # rows = TblData.objects.get(meta_id=json.loads(request.GET.get('download_data')))
            # rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
            pseudo_buffer = Echo()
            writer = csv.writer(pseudo_buffer)
            response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                             content_type="text/csv")
            # response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
            return response

        # TODO: test if shp file is correct
        if 'shp' in request.GET:
            s_id = request.GET.get('shp')
            layer_name = 'shp' + s_id
            srid = str(TblMeta.objects.filter(pk=s_id).values_list('geometry__srid__srid', flat=True)[0])

            # create layer on geoserver to request shp file
            create_data_layer(request, layer_name, s_id, store, workspace)

            # use GEOSERVER shape-zip
            url = LOCAL_GEOSERVER + '/' + workspace + '/ows?service=wfs' \
                '&version=1.0.0&request=GetFeature&typeName=' + workspace + ':' + layer_name + \
                '&outputFormat=shape-zip&srsname=EPSG:' + srid
            request = requests.get(url)

            pzfile = PyZip().from_bytes(request.content)
            try:
                del pzfile['wfsrequest.txt']
            except KeyError:
                pass

            # clean up right after request:
            delete_layer(layer_name, store, workspace)
            return HttpResponse(pzfile.to_bytes(), content_type='application/zip')

        # TODO: schemaLocation shows too much information for possible intruder. Figure out how to improve?
        if 'xml' in request.GET:
            id = request.GET.get('xml')
            layer_name = 'XML_' + id
            srid = str(TblMeta.objects.filter(pk=id).values_list('geometry__srid__srid', flat=True)[0])

            create_id_layer(request, layer_name, id, HomeView.store, HomeView.workspace)

            # use GEOSERVER GML
            url = LOCAL_GEOSERVER + '/' + workspace + '/ows?service=wfs' \
                                                      '&version=1.0.0&request=GetFeature&typeName=' + workspace + ':' \
                  + layer_name + \
                  '&outputFormat=text%2Fxml%3B%20subtype%3Dgml%2F2.1.2&&srsname=EPSG:' + srid

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
            logger.debug('Redirect to vfwheron/rsp/login/init...')
            return redirect('vfwheron:watts_rsp:login_init')
        else: # default django login
            return redirect('vfwheron:login')

    def dispatch(self, request, *args, **kwargs):
        """

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


class HelpView(TemplateView):
    """

    """

    #     template_name = 'vfwheron/help.html'
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
        return render(request, 'vfwheron/help.html', {'context': context})


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
        # message = _("Login failed.")
        # message = "Login failed."
        # request.user.message_set.create(message = message)
        messages.warning(request, 'Login failed.')
        return redirect('vfwheron:home')


class GeoserverView(View):
    """
    Build URL to get layers from Geoserver
    """

    @staticmethod
    def get(request, service, layer, bbox, srid):
        """

        :param request:
        :type request:
        :param service:
        :type service:
        :param layer:
        :type layer:
        :param bbox:
        :type bbox:
        :param srid:
        :type srid:
        :return:
        :rtype:
        """
        # wfsLayerName = 'new_ID_as_identifier_update'
        # wfsLayerName = layer
        work_space_name = HomeView.workspace  # 'CAOS_update'
        url = LOCAL_GEOSERVER + '/' + work_space_name + '/ows?service=' + service + \
            '&version=1.0.0&request=GetFeature&typeName=' + work_space_name + ':' + layer + \
            '&outputFormat=application%2Fjson&srsname=EPSG:' + srid + '&bbox=' + bbox + ',EPSG:' + srid
        # url = '{}/{}/ows?service={}&version=1.0.0&request=GetFeature&typeName={}:{
        # }&outputFormat=application%2Fjson&' \
        #       'srsname=EPSG:{}&bbox={},EPSG:{}'.format(LOCAL_GEOSERVER, workSpaceName, service, workSpaceName, layer,
        #                                                srid, bbox, srid)
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        return HttpResponse(response.read().decode('utf-8'))
