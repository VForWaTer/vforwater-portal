from django.views.generic import TemplateView
from vfwheron.models import TblVariable

from django.contrib.gis.db.models import Extent
from vfwheron.models import LtLocation
from vfwheron.models import LtUnit

from vfwheron.models import TblMeta
# Create your views here.

class HomeView(TemplateView):
    template_name = 'vfwheron/home.html'

    def get_context_data(self, **kwargs):
        # TODO: Revert these changes once database migration is complete.
        #get_unit_id = TblVariable.objects.select_related('unit').values_list('variable_name', 'variable_symbol')
        #all_variable_names = get_unit_id.values('variable_name', 'variable_symbol','unit__unit_symbol')
        all_variable_names = []
        return {'all_names': all_variable_names}
       
    
class ExtlinksView(TemplateView):
    template_name = 'vfwheron/extlinks.html'
