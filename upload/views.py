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
        visible_fields = form.visible_fields()

        return render(self.request, self.template_name, {'context': context})

    def post(self, request):
        form = UploadForm(request.POST)
        context = upload_defaults(request)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
        return render(self.request, self.template_name, {'context': context})


def clear_database(request):
    for file in UploadedFile.objects.all():
        file.file.delete()
        file.delete()
    return redirect(request.POST.get('next'))


def delete_data(request, pk):
    data = get_object_or_404(UploadedFile, pk=pk)
    if request.method == 'POST':
        form = UploadForm(request.POST, instance=data)
    else:
        form = UploadForm(instance=data)
    return HomeView.get(request)

    for file in UploadedFile.objects.all():
        file.file.delete()
        file.delete()
    return redirect(request.POST.get('next'))

