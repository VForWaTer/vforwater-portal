from django.urls import path, re_path, include

from vfw_status import views

app_name = 'vfw_status'

service_urls = [
]

urlpatterns = [
    #re_path(r'^$', views.home, name='home'),
    re_path(r'^$', views.HomeStatusView.as_view(), name='home'),
    path('<service>/', include(service_urls)),
    
]
