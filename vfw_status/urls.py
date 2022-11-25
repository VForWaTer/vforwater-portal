from django.conf.urls import include
from django.urls import path, re_path

from vfw_status import views

app_name = 'vfw_status'

service_urls = [
]

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    path('<service>/', include(service_urls)),
]
