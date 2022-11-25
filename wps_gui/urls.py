from django.conf.urls import include
from wps_gui import views
from django.urls import path, re_path


app_name = 'wps_gui'

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    path('processview', views.ProcessView.as_view(), name='processview'),
    path('dbload', views.db_load, name='dbload'),
    path('processrun', views.process_run, name='processrun'),
    path('workflowrun', views.workflow_run, name='workflowrun'),
    path('updatetools', views.update_tools, name='updatetools'),
]
