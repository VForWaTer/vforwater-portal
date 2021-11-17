from django.conf.urls import include
from wps_gui import views
from django.urls import path, re_path


app_name = 'wps_gui'

# service_urls = [
#     url(r'^$', views.service, name='service'),
#     # url(r'^process/(?P<identifier>[\w.]+)/$', views.process, name='process'),
# # url(r'^process$', views.ProcessView.as_view(), name='process'),
# ]

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    path('processview', views.ProcessView.as_view(), name='processview'),
    path('dbload', views.db_load, name='dbload'),
    path('processrun', views.process_run, name='processrun'),
    # url(r'^(?P<service>\w+)/', include(service_urls)),
]
