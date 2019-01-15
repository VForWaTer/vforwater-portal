from django.shortcuts import render

#from heron_wps.forms import InputForm


def home(request):
    """
    Dummy page for Heron Monitor tool. 
    """
    return render(request, 'heron_monitor/home.html')

