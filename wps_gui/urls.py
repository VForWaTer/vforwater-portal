from django.conf.urls import url, include
from wps_gui import views

app_name = 'wps_gui'

# service_urls = [
#     url(r'^$', views.service, name='service'),
#     # url(r'^process/(?P<identifier>[\w.]+)/$', views.process, name='process'),
# # url(r'^process$', views.ProcessView.as_view(), name='process'),
# ]

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^processview$', views.ProcessView.as_view()),
    # url(r'^(?P<service>\w+)/', include(service_urls)),
]
