from django.urls import re_path, include
from upload import views
from . import views

app_name = 'upload'

service_urls = [
]

urlpatterns = [
    # re_path(r'^$', views.home, name='home'),
    re_path(r'^$', views.HomeView.as_view(), name='home'),
    re_path(r'^clear/$', views.ClearDatabaseView.as_view(), name='clear_database'),
    re_path(r'^clear/(?P<pk>\d+)/delete/$', views.DeleteDataView.as_view(), name='delete_data'),
    re_path(r'^(?P<service>\w+)/', include(service_urls)),
    re_path(r'^upload/$', views.HomeView.as_view(), name='upload'),
]

