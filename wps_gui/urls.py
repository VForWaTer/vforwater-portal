# =================================================================
#
# Authors: Marcus Strobl <marcus.strobl@gmx.de>
# Contributors: Safa Bouguezzi <safa.bouguezzi@kit.edu>
#
# Copyright (c) 2024 Marcus Strobl
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

from wps_gui import views
from django.urls import path, re_path, include


app_name = 'wps_gui'

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    path('processview', views.ProcessView.as_view(), name='processview'),
    path('deleteresult', views.delete_result, name='deleteresult'),
    path('processrun', views.process_run, name='processrun'),
    path('resultdownload', views.ToolResultsDownload.as_view(), name='resultdownload'),
    path('resultdisplay', views.FileDownloadView.as_view(), name='resultdisplay'),
    path('processstate', views.process_state, name='processstate'),
    path('updatetools', views.update_tools, name='updatetools'),
    path('workflowrun', views.workflow_run, name='workflowrun'),
    # url(r'^(?P<service>\w+)/', include(service_urls)),
]
