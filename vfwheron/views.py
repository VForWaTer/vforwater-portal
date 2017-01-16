from django.views.generic import TemplateView

# Create your views here.

class HomeView(TemplateView):
    template_name = 'vfwheron/home.html'
    
class LoginView(TemplateView):
    template_name = 'vfwheron/login.html'    
    
class ExtlinksView(TemplateView):
    template_name = 'vfwheron/extlinks.html'
