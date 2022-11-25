from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from upload.forms import UploadForm
from upload.models import UploadedFile



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

