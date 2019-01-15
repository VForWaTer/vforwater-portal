from django.conf.urls import url, include
from heron_wps import views

app_name = 'wps'

service_urls = [
    url(r'^$', views.service, name='service'),
    url(r'^process/(?P<identifier>[\w.]+)/$', views.process, name='process'),
]

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<service>\w+)/', include(service_urls)),
]
