import base64
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

from .query_functions import get_bbox_from_data, build_id_list
from vfwheron.models import FilterMenu, TblData, TblMeta, TblVariable
# from vfwheron.models import TblData, TblMeta, TblVariable
# from vfwheron.filter import FilterMenu
from datetime import datetime

import matplotlib.pyplot as plt
import logging
import os

# Create your views here.
logger = logging.getLogger(__name__)

# from Django doc about session: If SESSION_EXPIRE_AT_BROWSER_CLOSE is set to True, Django will use browser-length
# cookies – cookies that expire as soon as the user closes their browser. Use this if you want people to have to log in
# every time they open a browser.
class HomeView(TemplateView):
    template_name = 'vfwheron/home.html'

    # Put here everything you need at startup and for refresh
    def get_context_data(self, **kwargs):
        data_style = 'default'
        #print('+++ items: ', cache.get('workspaceData'))
        #print("+++ FilterMenu.get_menu('submenu'): ", FilterMenu.get_menu('submenu'))
        #print("+++ get_bbox_from_data(): ", get_bbox_from_data())
        #print("+++data_style: ", data_style)
        # data_style = 'Light Blue Circle'
        if cache.get('workspaceData') == None:
            workspaceData = []
        else:
            workspaceData = cache.get('workspaceData')
        return {'dataExt': get_bbox_from_data(), 'menu_list': FilterMenu.get_menu('submenu'), 'data_style': data_style,
                'workspaceData': workspaceData}

class menuView(TemplateView):
    # TODO: each time you click a new top menu the database is accessed --> implement cache!
    # user = 'default'

    def get(self, request):

        # TODO: mix of session and cache looks terribly wrong. Possible to make consistent?
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

        # available_datasets = build_topquery(cache)['results'] if selection_list else len(TblMeta.objects.all())

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
            preview = request.GET.get('preview')
            label = TblMeta.objects.filter(id=preview).values_list('variable__variable_name',
                                       'variable__variable_symbol', 'variable__unit__unit_abbrev')
            ylabel = label[0][0] + ' (' + label[0][1] + ')' + ' [' + label[0][2] + ']'

            # connect to database
            cursor = connections['vforwater'].cursor()
            cursor.execute(
                'SELECT tbl_data.tstamp, tbl_data.value FROM public.tbl_data WHERE tbl_data.meta_id = %s' % preview)
            m = cursor.fetchall()
            cursor.close()

            # create image
            fig, ax = plt.subplots(1, 1, figsize=(6, 4))
            ax.plot([row[0] for row in m], [row[1] for row in m], '-b', lw=2)
            fig.autofmt_xdate(),
            ax.set_xlabel('Date')
            ax.grid(which='major', axis='x')
            ax.set_ylabel(ylabel)
            ax.set_title('Dataset preview')

            # create tempfile and read as base64
            tmpFile = BytesIO()
            fig.savefig(tmpFile, format='png')
            tmpFile.seek(0)
            b64 = base64.b64encode(tmpFile.getvalue())

            # create the image-tag
            imgtag = "<img alt='data image' src='data:image/png;base64,%s'>" % b64.decode('utf8')
            # imgtag = maelicke_plot()
            return JsonResponse({'get': imgtag}) # requested from vfw.js show_preview

        if request.GET.get('onclick_show_datasets'):
            # if cache.get('point_style_name'):
            #     cache.set({'point_style_name': False})
            # else:
            #     cache.set({'point_style_name': True})
            result = FilterMenu.build_queryset(cache);
            meta_ids = build_id_list(result)
            # locations = result.values('meta__site__id').distinct()  # location id for map
            # TODO: läuft nur wenn ich den Stylenamen ändere
            # id_list = build_id_list(locations)
            # data_style = 'CAOS:selection'
            return JsonResponse({'results': len(result), 'data_style': meta_ids})

        return JsonResponse(FilterMenu.tick_submenu(menu, selection_list, cache))


class show_datasets(TemplateView):
    def get(self, request):
        clicked_menu_value = request.GET
        return JsonResponse(FilterMenu.tick_submenu(clicked_menu_value['menu']))


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
        return render(request, 'vfwheron/help.html', {'context':context})
