import base64
import json
import re

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

from vfwheron.previewplot import maelicke_plot

mpl.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib import pylab
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure

from .query_functions import get_bbox_from_data
from datetime import datetime
import time

from .filter import FilterMethods, Menu, newbuild_id_list

import logging
import os

# Create your views here.
logger = logging.getLogger(__name__)


# from Django doc about session: If SESSION_EXPIRE_AT_BROWSER_CLOSE is set to True, Django will use browser-length
# cookies – cookies that expire as soon as the user closes their browser. Use this if you want people to have to log in
# every time they open a browser.
class HomeView(TemplateView):
    template_name = 'vfwheron/home.html'
    Menu = Menu().menu()
    JSON_Menu = json.dumps(Menu['client'])
    # JSON_Menu = Menu().json_menu()

    # Menu = JsonResponse({"Name": "Harry", "Age": 2})

    # Put here everything you need at startup and for refresh
    def get_context_data(self, **kwargs):
        data_style = 'default'
        # data_style = 'Light Blue Circle'
        if cache.get('workspaceData') == None:
            workspaceData = []
        else:
            workspaceData = cache.get('workspaceData')

        try:
            dataExt = get_bbox_from_data()
        except:
            print("ERROR: Data Extend cannot be loaded in views.py")  # TODO: How to write this to a log file?
            dataExt = [645336.034469495, 6395474.75106861, 666358.204722283, 6416613.20733359]

        return {'dataExt': dataExt, 'data_style': data_style,
                'workspaceData': workspaceData, 'Menu': self.JSON_Menu}


class menuView(TemplateView):
    # user = 'default'

    def get(self, request):

        request.session.set_expiry(20)  # expire after 20 seconds

        # bring last used menu to session
        menu = request.GET.get('menu')
        if menu:
            request.session['menu'] = menu
        else:
            menu = request.session.get('menu')

        # save your selections in cache
        selection = request.GET.get('selection')
        submenu = request.GET.get('submenu')
        if selection:
            if cache.get(menu):
                edit_cache = cache.get(menu)
                if selection in edit_cache[submenu]:
                    edit_cache[submenu].remove(selection)
                    cache.set(menu, {submenu: edit_cache[submenu]})
                else:
                    edit_cache[submenu].append(selection)
                    cache.set(menu, {submenu: edit_cache[submenu]})
            else:
                cache.set(menu, {submenu: [selection]})

        selection_list = []
        if cache.get(menu):
            if cache.get(menu).values():
                selection_list = list(cache.get(menu).values())
                selection_list = [item for sublist in selection_list for item in sublist]
            else:
                cache.set(menu, [])

        work_dataset = request.GET.get('workspaceData')
        min_time = request.GET.get('minTime')
        max_time = request.GET.get('maxTime')
        if work_dataset:
            work_query = 'SELECT tbl_data.tstamp, tbl_data.value FROM public.tbl_data WHERE tbl_data.meta_id = ' + \
                         work_dataset
            if min_time:
                work_query = work_query + 'AND tbl_data.tstamp > ' + str(min_time)
            if max_time:
                work_query = work_query + 'AND tbl_data.tstamp < ' + str(max_time)
            if 'work_dataset_list' in request.session:
                if 'dataset' + work_dataset in request.session['work_dataset_list']:
                    # TODO: Need timestamp in name to see if different selection
                    print('A C H T U N G :  gibts schon!')
                    return
                else:
                    # request.session['work_dataset_list'].append('dataset' + work_dataset)
                    request.session['work_dataset_list'].append(work_dataset)
            else:
                # request.session['work_dataset_list'] = ['dataset' + work_dataset]
                request.session['work_dataset_list'] = [work_dataset]

            request.session['dataset' + work_dataset] = work_query
            cache.set('workspaceData', request.session['work_dataset_list'])
            return JsonResponse({'workspaceData': request.session['work_dataset_list']})

        remove_dataset = request.GET.get('remover')
        if remove_dataset:
            if 'work_dataset_list' in request.session:
                request.session['work_dataset_list'].remove(remove_dataset)
                cache.set('workspaceData', request.session['work_dataset_list'])
            return JsonResponse({'workspaceData': request.session['work_dataset_list']})

        if 'preview' in request.GET:
            # plot png the mälicke way:
            imgtag = maelicke_plot(request.GET.get('preview'))
            return JsonResponse({'get': imgtag})  # requested from vfw.js show_preview

        # if request.GET.get('filter_selection'):
        filter_selection = request.GET.get('filter_selection')
        if filter_selection:
            filter_menu = FilterMethods.selection_counts(HomeView.Menu['server'], json.loads(filter_selection))
            return JsonResponse(filter_menu)

        filter_selection_map = request.GET.get('filter_selection_map')
        if filter_selection_map:
            meta_ids = newbuild_id_list(HomeView.Menu['server'], json.loads(filter_selection_map))
            return JsonResponse(meta_ids)

        return JsonResponse({'Error': 'Something is missing. Check views.py'})


class ExtlinksView(TemplateView):
    template_name = 'vfwheron/extlinks.html'


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
