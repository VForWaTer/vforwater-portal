from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis import forms
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from upload.forms import UploadForm, EntriesForm, PersonsForm
from upload.models import UploadedFile
from vfw_home.Forms.fields import CustomOSMField
from vfw_home.models import Entries
from vfw_home.Forms.widgets import TableSelect, CustomOSMWidget
from vfw_home.utilities.utilities import raise_logging_exception, logger

class HomeView(LoginRequiredMixin, FormView):

    template_name: str = 'upload/home.html'
    form_class = UploadForm

    def get(self, request):

        form = UploadForm()
        context = self.upload_defaults(request)  


        logger.debug(f"Context: {context['geoInfo']}")
        logger.debug("GET request received.")
        logger.debug(f"Entries title: {Entries.objects.values_list('title').exclude(title=None)}")

        return render(request, self.template_name, context) 
       
    def post(self, request):
      
        """Handles POST requests, validates the form, and processes the uploaded file."""
        
        form = UploadForm(request.POST)
        context = self.upload_defaults(request)

        logger.info("POST request received.")
        logger.debug(f"Form Data: {request.POST}")
      
        
        if form.is_valid():
            logger.info(f"User {request.user} submitted a valid form.")
            
        return render(self.request, self.template_name, {'context': context})


    @staticmethod
    def upload_defaults(cls, request):

        return {
            'generalInfo': UploadForm.GeneralInfo,
            'geoInfo': UploadForm.GeoInfo,
            'selection': [],
            'DataInfo': UploadForm.DataspecificInfo
            }
       
class ClearDatabaseView(View):
    """
    Class-based view to delete all uploaded files and their database records.
    """

    def post(self, request, *args, **kwargs):
        """Handles POST requests to clear the database."""
        
        next_url = request.POST.get('next', '/')
        endpoint = request.path

        try:
            files = UploadedFile.objects.all()
            if files.exists():
                file_count = files.count()
                for file in files:
                    logger.info(f"Deleting file: {file.file.name}")
                    file.file.delete(save=False)  
                    file.delete()
                messages.success(request, f"Deleted {file_count} uploaded files.")
                logger.info(f"Successfully deleted {file_count} files from the database.")
            else:
                messages.info(request, "No files found to delete.")
                logger.warning("Attempted to delete files, but no files were found.")

        except Exception as e:
            messages.error(request, f"Error deleting files: {e}")
            raise_logging_exception(e, endpoint, f"Failed to delete files: {e}" )

        return redirect(next_url)


class DeleteDataView(View):

    """
    Class-based view to delete a specific uploaded file.
    """

    def get(self, request, pk):
        
        """Handles GET requests and shows the deletion form."""

        data = get_object_or_404(UploadedFile, pk=pk)

        logger.info(f"Retrieving file for deletion: {data}")

        form = UploadForm(instance=data) 

        return HomeView.get(self, request) 


    def post(self, request, *args, **kwargs):
        """Handles POST requests and deletes the specified file."""

        endpoint = request.path

        data = get_object_or_404(UploadedFile, pk=pk)

        logger.info(f"Attempting to delete file: {data.file.name}")

        try:
            data.file.delete(save=False)  

            data.delete() 

            messages.success(request, f"File {data.file.name} deleted successfully.")

            logger.info(f"File {data.file.name} deleted successfully.")

        except Exception as e:

            messages.error(request, f"Error deleting file: {e}")
            
            raise_logging_exception(e, endpoint, f"Error deleting file {data.file.name}: {e}" )

        return redirect(request.POST.get('next', '/')) 
