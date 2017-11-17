from django.http.response import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.core.cache import cache

from .query_functions import get_bbox_from_data
from vfwheron.models import FilterMenu

import requests
import logging

# Create your views here.
logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = 'vfwheron/home.html'

    def get_context_data(self, **kwargs):
        return {'dataExt': get_bbox_from_data(), 'menu_list': FilterMenu.get_menu('submenu')}


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
            print('selection_list : ', selection_list)
            return JsonResponse(FilterMenu.build_queryset(cache))

        # --- playing with geoserver:
        # get all styles on geoserver:
        # curl - u admin: geoserver - XGET http: // localhost: 8080 / geoserver / rest / cite / styles.xml
        r = requests.get("http://vforwater-gis.scc.kit.edu:8080/geoserver/rest/styles.json", auth=('admin', 'vforwater'))
        # print('geoserver: ', r)
        # for i in r:
        #     print(i)

        # get one style from geoserver:
        # curl - u admin: geoserver - XGET http: // localhost: 8080 / geoserver / rest / cite / styles.xml
        r = requests.get("http://vforwater-gis.scc.kit.edu:8080/geoserver/rest/styles/new_point.sld", auth=('admin', 'vforwater'))
        # print('one style:: ', r.content, r.status_code)

        # Edit / reupload the content of an existing style on the server when the style is in a workspace:
        selected_data = '<ogc:Literal>192</ogc:Literal>'
        chosen_data = '<ogc:Literal>716</ogc:Literal>'
        data = '<?xml version="1.0" encoding="ISO-8859-1"?><StyledLayerDescriptor version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><NamedLayer><Name>Attribute-based point</Name><UserStyle><Title>Attribute-based point</Title><FeatureTypeStyle><Rule><Name>AllData</Name><Title>All avaiable Datensets</Title><PointSymbolizer><Graphic><Mark><WellKnownName>circle</WellKnownName><Fill><CssParameter name="fill">#00DDFF</CssParameter></Fill></Mark><Size>3</Size></Graphic></PointSymbolizer></Rule><Rule><Name>SelectedData</Name><Title>Selected Datasets</Title><ogc:Filter><ogc:PropertyIsEqualTo><ogc:PropertyName>id</ogc:PropertyName>' + selected_data + '</ogc:PropertyIsEqualTo></ogc:Filter><PointSymbolizer><Graphic><Mark><WellKnownName>circle</WellKnownName><Fill><CssParameter name="fill">#0088EE</CssParameter></Fill></Mark><Size>12</Size></Graphic></PointSymbolizer></Rule><Rule><Name>ChosenData</Name><Title>Chosen Datasets</Title><ogc:Filter><ogc:PropertyIsEqualTo><ogc:PropertyName>id</ogc:PropertyName>' + chosen_data + '</ogc:PropertyIsEqualTo></ogc:Filter><PointSymbolizer><Graphic><Mark><WellKnownName>circle</WellKnownName><Fill><CssParameter name="fill">#0033CC</CssParameter></Fill></Mark><Size>16</Size></Graphic></PointSymbolizer></Rule></FeatureTypeStyle></UserStyle>  </NamedLayer></StyledLayerDescriptor>'
        s = requests.put("http://vforwater-gis.scc.kit.edu:8080/geoserver/rest/workspaces/CAOS/styles/new_point", data=data, auth=('admin', 'vforwater'), headers={'content-type': 'application/vnd.ogc.sld+xml'})
        # print('s: ', s.content, s.status_code)

        # with open('vfwheron/point_style.xml', 'r') as myfile:
        #     data = myfile.read().replace('\n', '')
        # --- end of playing with geoserver

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
