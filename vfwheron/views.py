from django.http.response import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.core.cache import cache

from .query_functions import get_bbox_from_data, get_submenu_values, get_submenu, build_topquery

import logging

# Create your views here.
logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = 'vfwheron/home.html'

    def get_context_data(self, **kwargs):
        return {'dataExt': get_bbox_from_data(), 'menu_list': get_submenu()}


class menuView(TemplateView):
    # TODO: each time you click a new top menu the database is accessed --> implement cache!
    user = 'default'

    def get(self, request):

        # TODO: mix of session and cache looks terribly wrong. Possible to make consistent?
        # querydata = TblSelection.objects.filter(user=self.user).all()
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

        if request.GET.get('onclick_show_datasets'):
            return JsonResponse(build_topquery(cache))

        return JsonResponse(get_submenu_values(menu, selection_list))


class show_datasets(TemplateView):
    def get(self, request):
        print('Bin da! ** ** ** **', request)
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
