from django.shortcuts import render
from django.views import View

from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from heron_upload.forms import UploadForm
from heron_upload.models import UploadedFile


# def home(request):
#     """
#     Dummy page for Heron Upload tool.
#     """
#     return render(request, 'heron_upload/home.html')


class HomeView(TemplateView):
    template_name = 'heron_upload/home.html'

    def get(self, request):
        data_list = UploadedFile.objects.all()
        return render(self.request, 'heron_upload/home.html', {'data': data_list})

    def post(self, request):
        form = UploadForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            file = form.save()
            data = {'is_valid': True, 'name': file.file.name, 'url': file.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


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