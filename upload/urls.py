from django.conf.urls import url, include
from upload import views
from . import views

app_name = 'upload'

service_urls = [
]

urlpatterns = [
    # url(r'^$', views.home, name='home'),
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^clear/$', views.clear_database, name='clear_database'),
    url(r'^clear/(?P<pk>\d+)/delete/$', views.delete_data, name='delete_data'),
    url(r'^(?P<service>\w+)/', include(service_urls)),
    url(r'^upload/$', views.HomeView.as_view(), name='upload'),
]

