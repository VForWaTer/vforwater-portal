from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.apps import apps
from vfwheron.models import TblVariable, LtLocation, LtProject, LtDomain, LtLicense, TblMeta

from vfwheron.query_functions import get_bbox_from_data, get_filter_values, get_first_level, get_second_level

import logging

# Create your views here.

logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = 'vfwheron/home.html'

    my_app = apps.get_app_config('vfwheron')
    # print('----------', my_app.models)
    all_tables = [m._meta.object_name for m in my_app.models.values()]
    # print('##classes: ', all_tables)
    unused_tables = ['Basiseinzugsgebiet', 'NmMetaDomain', 'DjangoMigrations', 'SpatialRefSys', 'TblMeta',
                     'LtQuality', 'LtLicense', 'LtUnit']
    level_one_tables_sql = list(set(all_tables) - set(unused_tables))
    # print('level_one_tables_sql: ', level_one_tables_sql)

    level_one_tables = {'variable':'Datentyp', 'soil':'Boden', 'site':'Standort','publisher':'Besitzer',
                        'nmmetadomain':'Domäne'}
    # print('level_one_tables: ', level_one_tables)

    # print('get_filter_values: ', get_filter_values())
    # print('my app: ', my_app.models)
    # for m in my_app.models:
    #     print('keys: ', m, ' | values: ', my_app.models[m])

    # print('#+#+#: ', my_app.models['tblvariable'].objects.select_related('unit').values_list('variable_name',
    # 'variable_symbol'))
    # print('**domain_name**', LtDomain.objects.select_related('project').values('domain_name').distinct)
    # print('+TblVariable+',TblVariable.objects.select_related('unit').values('variable_name', 'variable_symbol','unit__unit_symbol').distinct)
    # print('+LtProject+', LtProject.objects.select_related('project_name').values('project_name').distinct)

    # print('****', LtLicense.objects.select_related('license_abbrev').distinct()) // geht nix
    # print('****', LtLocation.objects.select_related('srid').distinct())

    # print(' m e t a : ', TblMeta.objects.select_related('creator', 'publisher', 'geometry',
    #                                                     'license', 'quality','site', 'soil', 'variable', 'sensor', 'source').all())


    # metaquest = TblMeta.objects.using('vforwater').select_related('creator__last_name', 'publisher__last_name', 'geometry__srid',
    #     'license', 'quality','site', 'soil', 'variable', 'sensor', 'source').all()

    # filterworthy_values = ['variable__variable_name', 'soil__geology', 'soil__soil_type',
    #                        'site__site_name','publisher__last_name', 'publisher__institution_name', 'publisher__department',
    #                        'nmmetadomain__domain__domain_name', 'nmmetadomain__domain__project__project_name']
    # print('filterworthy_values: ',filterworthy_values)

    # metaquest = TblMeta.objects.filter(variable__variable_name='Lufttemperatur',soil__geology = 'marls', site__landuse = 'forest' ). \
    #     values(*filterworthy_values).distinct()
    # # print('######## # # # # ',metaquest)
    #
    # metaquest = TblMeta.objects.filter(variable__variable_name='Lufttemperatur',soil__geology = 'marls', site__landuse = 'forest' ). \
    #     values(*filterworthy_values)
    # print('######## # # # # ',metaquest)
    # print('## ## ## M e T a : ', [m for m in metaquest.values('variable__variable_name', 'source__source_type')] )

    # print('second_filter_level: ', second_filter_level())
    for m in get_second_level():
        print('***, m: ', m)
        print('1, m.keys(): ', m.keys())
        print('2, m.values(): ', m.values())
        for n in m.values():
            print('3, n: ', n)
            print('4, n[0]: ', n[0])
            for o in n:
                print ('5:', o.keys(), o.values())

    def get_context_data(self, **kwargs):
        get_unit_id = TblVariable.objects.select_related('unit').values_list('variable_name', 'variable_symbol')
        all_variable_names = get_unit_id.values('variable_name', 'variable_symbol', 'unit__unit_symbol')
        return {'dataExt': get_bbox_from_data(), 'first_level':get_first_level(), 'menue_list':get_second_level(), 'all_names': all_variable_names}


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
