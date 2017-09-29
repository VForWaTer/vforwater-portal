from django.http.response import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.shortcuts import redirect

from vfwheron.query_functions import get_bbox_from_data, get_submenu_values, get_submenu

import logging

# Create your views here.
logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = 'vfwheron/home.html'

    def get_context_data(self, **kwargs):
        return { 'dataExt': get_bbox_from_data(), 'menu_list':get_submenu()}

class menuView(TemplateView):

    def get(self, request):
        clicked_menu_value = request.GET
        return JsonResponse(get_submenu_values(clicked_menu_value['menu']))


class show_datasets(TemplateView):

    def get(self, request):
        print('Bin da! ** ** ** **')
        clicked_menu_value = request.GET
        return JsonResponse(get_submenu_values(clicked_menu_value['menu']))


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
