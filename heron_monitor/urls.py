from django.conf.urls import url, include
from heron_monitor import views

app_name = 'monitor'

service_urls = [
]

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<service>\w+)/', include(service_urls)),
]