from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis import forms
from django.shortcuts import render
from django.views import View

from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from upload.forms import UploadForm, EntriesForm, PersonsForm
from upload.models import UploadedFile
from vfw_home.Forms.fields import CustomOSMField
from vfw_home.models import Entries
from vfw_home.Forms.widgets import TableSelect, CustomOSMWidget




def upload_defaults(request):

    generalInfo = UploadForm.GeneralInfo
    geoInfo = UploadForm.GeoInfo
    DataInfo = UploadForm.DataspecificInfo
    selection = []
    return {'generalInfo': generalInfo, 'geoInfo': geoInfo, 'selection': selection, 'DataInfo': DataInfo}

class HomeView(LoginRequiredMixin, TemplateView):
    template_name: str = 'upload/home.html'

    def get(self, request):
        form = UploadForm()
        context = upload_defaults(request)
        print('0 _____________________________________________________________________')
        print('context: ', context['geoInfo'])
        print(' G E T ! ')
        print('entries title: ', Entries.objects.values_list('title').exclude(title=None))
     
        visible_fields = form.visible_fields()
      
        print(' I ____________________________________')
        
        print(' II ____________________________________')

        return render(self.request, self.template_name, {'context': context})
       
    def post(self, request):
        print('1 _____________________________________________________________________')
        print('P O S T: ', request.POST)
        
        form = UploadForm(request.POST)
        context = upload_defaults(request)
      
        print('  aaaaa ____________________: ')
        print('\033[91m' + 'form.is_valid()!', form.is_valid(), '\033[0m')
       
        print('  aa ____________________: ')
        if form.is_valid():
            print('user: ', request.user)
            
        return render(self.request, self.template_name, {'context': context})
       

def clear_database(request):
    for file in UploadedFile.objects.all():
        file.file.delete()
        file.delete()
    return redirect(request.POST.get('next'))


def delete_data(request, pk):
    data = get_object_or_404(UploadedFile, pk=pk)
    print('in delete / data: ', data)
    if request.method == 'POST':
        form = UploadForm(request.POST, instance=data)
    else:
        form = UploadForm(instance=data)
    return HomeView.get(request)

    for file in UploadedFile.objects.all():
        file.file.delete()
        file.delete()
    return redirect(request.POST.get('next'))
