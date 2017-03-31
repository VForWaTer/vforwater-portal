from django.views.generic import TemplateView
from vfwheron.models import TblVariable

# Create your views here.

class HomeView(TemplateView):
    template_name = 'vfwheron/home.html'

    def get_context_data(self, **kwargs):
        all_variable_names = TblVariable.objects.all() 
        return {'all_names': all_variable_names} 
    
class ExtlinksView(TemplateView):
    template_name = 'vfwheron/extlinks.html'
