from django.conf.urls import url, include
from heron_visual import views

app_name = 'visual'

service_urls = [
]

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<service>\w+)/', include(service_urls)),
]