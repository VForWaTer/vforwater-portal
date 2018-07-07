import base64
import json
import re
import urllib
import hashlib

from io import StringIO, BytesIO

from django.db import connections
from django.http.response import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.core.cache import cache
from django.conf import settings

import matplotlib as mpl

from heron.settings import LOCAL_GEOSERVER
from vfwheron.geoserver_layer import create_layer, get_layer, delete_layer, create_ID_layer, get_ID_layer, delete_ID_layer
from vfwheron.previewplot import get_preview

mpl.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib import pylab
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure

from .query_functions import get_bbox_from_data
from datetime import datetime
import time

from .filter import FilterMethods, Menu, build_id_list
from .models import TblMeta, TblVariable, TblData

import logging
import os

# Create your views here.
logger = logging.getLogger(__name__)


def get_dataset(self, request, **kwargs):
    # here 
    id = request.POST.get('meta_id')
    
    data = TblData.objects.get(meta=id).value
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
    template_name = 'vfwheron/home.html'
    user = 'default'
    Menu = Menu().menu(user)
    JSON_Menu = json.dumps(Menu['client'])
    # JSON_Menu = Menu().json_menu()
    data_layer = 'default_layer'
    if not get_layer(data_layer):
        create_layer(data_layer)
    # else:
    # # TODO: don't do that in production! That's just for develpment to make sure geoserver is updatet after restart of django
    #     delete_layer(data_layer)
    #     create_layer(data_layer)

    # Put here everything you need at startup and for refresh
    def get_context_data(self, **kwargs):

        try:
            dataExt = get_bbox_from_data()
        except:
            logger.warning('Data Extend cannot be loaded in views.py. Using fixed values.')
            dataExt = [645336.034469495, 6395474.75106861, 666358.204722283, 6416613.20733359]

        return {'dataExt': dataExt, 'Filter_Menu': self.JSON_Menu, 'data_layer': self.data_layer}


class menuView(TemplateView):
    # user = 'default'

    def get(self, request, user='default'):

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

        if 'filter_selection' in request.GET:
            filter_menu = FilterMethods.selection_counts(HomeView.Menu['server'], json.loads(request.GET.get('filter_selection')))
            return JsonResponse(filter_menu)

        if 'filter_selection_map' in request.GET:
            if json.loads(request.GET.get('filter_selection_map')) == 0:
                ID_layer = HomeView.data_layer
            else:
                meta_ids = build_id_list(HomeView.Menu['server'], json.loads(request.GET.get('filter_selection_map')))
                ID_layer = 'ID_layer' # + user
                if get_ID_layer(ID_layer):
                    delete_ID_layer(ID_layer)
                create_ID_layer(ID_layer, str(meta_ids['all_filters'])[1:-1])
    # TODO: Instead of recreating the layer on each click, add a hash to the name and build only none existing layers
            # ID_layer = 'ID_layer' + str(hashlib.md5(str(meta_ids['all_filters'])[1:-1].encode())) # + user
            # if not get_ID_layer(ID_layer):
            #     create_ID_layer(ID_layer, str(meta_ids['all_filters'])[1:-1])
#             else:
# # TODO: don't do that in production! That's just for develpment to make sure geoserver is updatet after restart of django
#                 delete_ID_layer(ID_layer)
#                 create_ID_layer(ID_layer, str(meta_ids['all_filters'])[1:-1])
            return JsonResponse({'ID_layer': ID_layer})

        return JsonResponse({'Error': 'Something is missing. Check views.py'})


class LoginView(View):
    def post(self, request):
        logger.debug('Redirect to vfwheron/rsp/login/init...')
        return redirect('vfwheron:watts_rsp:login_init')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            logger.debug('The user is not authenticated!')
        else:
            logger.debug('{} logged in as'.format(request.user.username))

        return super().dispatch(request, *args, **kwargs)


class LogoutView(View):
    def logout(self, request):
        logger.debug('{} logged out'.format(request.user.username))
        logout(request)

    def post(self, request):
        self.logout(request)
        return redirect('vfwheron:home')


class HelpView(TemplateView):
    #     template_name = 'vfwheron/help.html'
    def get(self, request):
        f = open(os.path.join(settings.BASE_DIR, 'USERHELP.md'), 'r')
        context = {}
        i = 0
        for line in f:
            context[i] = line
            i += 1
        f.close()
        return render(request, 'vfwheron/help.html', {'context': context})


class GeoserverView(View):

    def get(self, request, service, layer, bbox, srid):
        wfsLayerName = 'new_ID_as_identifier_update'
        wfsLayerName = layer
        workSpaceName = 'CAOS_update'
        url = LOCAL_GEOSERVER + '/' + workSpaceName + '/ows?service=' + service + \
              '&version=1.0.0&request=GetFeature&typeName=' + workSpaceName + ':' + wfsLayerName + \
              '&outputFormat=application%2Fjson&srsname=EPSG:' + srid + '&bbox=' + bbox + ',EPSG:' + srid
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        return HttpResponse(response.read().decode('utf-8'))
