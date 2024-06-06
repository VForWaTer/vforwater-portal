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


# def home(request):
#     """
#     Dummy page for Heron Upload tool.
#     """
#     return render(request, 'upload/home.html')
#
# def home(request):
#     if request.method == 'POST':
#         form = MetadataForm(request.POST)
#         if form.is_valid():
#             pass  # does nothing, just trigger the validation
#     else:
#         form = MetadataForm()
#     return render(request, 'home.html', {'form': form})

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
        # for i, j in newform.items():
        #     print(i)
        visible_fields = form.visible_fields()
        # form = UploadForm()
        print(' I ____________________________________')
        # print(' form: ', form)
        print(' II ____________________________________')

        return render(self.request, self.template_name, {'context': context})
        # return render(self.request, self.template_name, {'form': form, 'generalInfo': generalInfo,
        #                                                  'geoInfo': geoInfo, 'DataInfo': DataInfo})
        # data_list = UploadedFile.objects.all()
        # return render(request, 'home.html', {'form': form})

    def post(self, request):
        print('1 _____________________________________________________________________')
        print('P O S T: ', request.POST)
        # form = EntriesForm(request.POST)
        form = UploadForm(request.POST)
        context = upload_defaults(request)
        # print('form: ', form)
        # form = EntriesForm(request.POST)
        print('  aaaaa ____________________: ')
        print('\033[91m' + 'form.is_valid()!', form.is_valid(), '\033[0m')
        # print('form["citation"]: ', form["citation"])
        print('  aa ____________________: ')
        if form.is_valid():
            print('user: ', request.user)
            # new_entry = form.save(commit=False)
            # new_entry.user = request.user
            # new_entry.save()
            # return redirect('home')
            pass  # does nothing, just trigger the validation
        return render(self.request, self.template_name, {'context': context})
        # return render(self.request, self.template_name, {'form': form})
        # form = UploadForm(self.request.POST, self.request.FILES)
        # if form.is_valid():
        #     file = form.save()
        #     data = {'is_valid': True, 'name': file.file.name, 'url': file.file.url}
        # else:
        #     data = {'is_valid': False}
        # return JsonResponse(data)


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

 # class DataUploadView(View):
 #     def get(self, request):
 #         data_list = UploadedFile.objects.all()
 #         return render(self.request, 'base_app/workspace.html', {'data': data_list})
