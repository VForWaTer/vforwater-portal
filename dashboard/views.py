from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'dashboard/index.html', {'message': 'Hallo! :)'})

def template(request):
    '''Return the blank template page. Just for development purposes.'''
    return render(request, 'dashboard/dashboard.html')
