from django.conf.urls import url, include
from visual_app import views
from django.urls import path, re_path


app_name = 'visual'

service_urls = [
]

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    path('<service>/', include(service_urls)),
]
