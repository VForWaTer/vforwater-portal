from django.shortcuts import render
from django.views import View

#from heron_wps.forms import InputForm






class HomeMonitorView(View):
    """
    Class-based view for Heron Monitor tool.
    """

    def get(self, request):
        """Handles GET requests and renders process monitor tool template."""

   
        return render(request, 'process_monitor/home.html')
