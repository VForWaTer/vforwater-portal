from django.urls import path, re_path, include

from process_monitor import views

app_name = 'monitor'

service_urls = [
]

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    path('<service>/', include(service_urls)),
]
