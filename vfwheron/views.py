from django.http.response import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.core.cache import cache

from .query_functions import get_bbox_from_data, build_id_list
from vfwheron.models import FilterMenu

import requests
import logging
import os
# Create your views here.
logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = 'vfwheron/home.html'

    def get_context_data(self, **kwargs):
        # data_style = 'Light Blue Circle'
        data_style = 'default'
        return {'dataExt': get_bbox_from_data(), 'menu_list': FilterMenu.get_menu('submenu'), 'data_style': data_style}

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

        if request.GET.get('onclick_show_datasets'):
            # if cache.get('point_style_name'):
            #     cache.set({'point_style_name': False})
            # else:
            #     cache.set({'point_style_name': True})
            result = FilterMenu.build_queryset(cache)
            meta_ids = build_id_list(result)
            # locations = result.values('meta__site__id').distinct()  # location id for map
            # TODO: läuft nur wenn ich den Stylenamen ändere
            # id_list = build_id_list(locations)
            # data_style = 'CAOS:selection'
            return JsonResponse({'results': len(result), 'data_style': meta_ids})

        return JsonResponse(FilterMenu.tick_submenu(menu, selection_list, cache))


class show_datasets(TemplateView):
    def get(self, request):
        print('Bin da! ** ** ** **', request)
        clicked_menu_value = request.GET
        return JsonResponse(FilterMenu.tick_submenu(clicked_menu_value['menu']))


class ExtlinksView(TemplateView):
    template_name = 'vfwheron/extlinks.html'


class LoginView(TemplateView):
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
        return redirect('vfwheron:login')

    
class HelpView(TemplateView):
    template_name = 'vfwheron/help.html'
    
