from django.views.generic import TemplateView
from django.contrib.gis.db.models import Extent
from django.contrib.auth import logout

from vfwheron.models import TblVariable
from vfwheron.models import LtLocation
from vfwheron.models import LtUnit
from vfwheron.models import TblMeta

from watts_rsp import auth
import logging

# Create your views here.

logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    template_name = 'vfwheron/home.html'

    def get_context_data(self, **kwargs):
        get_unit_id = TblVariable.objects.using('vforwater').select_related('unit').values_list('variable_name', 'variable_symbol')
        all_variable_names = get_unit_id.values('variable_name', 'variable_symbol','unit__unit_symbol')
        return {'all_names': all_variable_names} 
       
    
class ExtlinksView(TemplateView):
    template_name = 'vfwheron/extlinks.html'

class LoginView(TemplateView):
    def post(self, request):
        return auth.WattsBackend.redirect(request)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            logger.debug('A stranger passed by')
        else:
            logger.debug('{} passed by'.format(request.user.username))

        return super().dispatch(request, *args, **kwargs)

