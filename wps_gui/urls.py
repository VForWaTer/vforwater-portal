from wps_gui import views
from django.urls import path, re_path, include


app_name = 'wps_gui'

# service_urls = [
#     url(r'^$', views.service, name='service'),
#     # url(r'^process/(?P<identifier>[\w.]+)/$', views.process, name='process'),
# # url(r'^process$', views.ProcessView.as_view(), name='process'),
# ]

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    path('processview', views.ProcessView.as_view(), name='processview'),
    # path('dbload', views.db_load, name='dbload'),
    path('deleteresult', views.delete_result, name='deleteresult'),
    path('processrun', views.process_run, name='processrun'),
    path('resultdownload', views.ToolResultsDownload.as_view(), name='resultdownload'),
    path('processstate', views.process_state, name='processstate'),
    path('updatetools', views.update_tools, name='updatetools'),
    path('workflowrun', views.workflow_run, name='workflowrun'),
    # url(r'^(?P<service>\w+)/', include(service_urls)),
]
