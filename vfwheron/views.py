from django.http.response import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.shortcuts import redirect, render_to_response

from django.apps import apps

from vfwheron.models import TblVariable, LtLocation, LtProject, LtDomain, LtLicense, TblMeta

from vfwheron.query_functions import get_bbox_from_data, get_submenu_values, get_first_level, get_submenu

import logging

# Create your views here.
logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = 'vfwheron/home.html'
    get_submenu_values('Boden')
    # my_app = apps.get_app_config('vfwheron')
    # all_tables = [m._meta.object_name for m in my_app.models.values()]
    # unused_tables = ['Basiseinzugsgebiet', 'NmMetaDomain', 'DjangoMigrations', 'SpatialRefSys', 'TblMeta',
    #                  'LtQuality', 'LtLicense', 'LtUnit']
    # level_one_tables_sql = list(set(all_tables) - set(unused_tables))
    #
    # level_one_tables = {'variable':'Datentyp', 'soil':'Boden', 'site':'Standort','publisher':'Besitzer',
    #                     'nmmetadomain':'Domäne'}
    #
    # for m in get_submenu():
    #     print('***, m: ', m)
    #     print('1, m.keys(): ', m.keys())
    #     print('2, m.values(): ', m.values())
    #     for n in m.values():
    #         print('3, n: ', n)
    #         print('4, n[0]: ', n[0])
    #         for o in n:
    #             print ('5:', o.keys(), o.values())

    def get_context_data(self, **kwargs):
        # get_unit_id = TblVariable.objects.select_related('unit').values_list('variable_name', 'variable_symbol')
        # all_variable_names = get_unit_id.values('variable_name', 'variable_symbol', 'unit__unit_symbol')
        return {'dataExt': get_bbox_from_data(), 'menu_list':get_submenu()}

class menuView(TemplateView):

    def get(self, request):
        clicked_menu_value = request.GET
        print('*****: ', clicked_menu_value['menu'])
        new_values = get_submenu_values(clicked_menu_value['menu'])
        return JsonResponse(new_values)


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
