from django.conf.urls import url, include
from django.urls import path

from heron import settings
from . import views


app_name = 'vfwheron'

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^login$', auth_views.LoginView.as_view(template_name='vfwheron/login.html'), {'template_name': 'vfwheron/login.html'}, name='login'),
    # url(r'^failedlogin$', auth_views.LoginView, {'template_name': 'vfwheron/failedlogin.html'}, name='failedlogin'),
    url(r'^watts_login$', views.LoginView.as_view(), name='watts_login'),
    url(r'^help$', views.HelpView.as_view(), name='help'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    url(r'^menu$', views.MenuView.as_view(), name='menu'),
    url(r'^geoserver/(?P<service>[\w{3,4}]+)/(?P<layer>[\w]+)/(?P<bbox>[\-.,\d]+)/(?P<srid>[\d]{4,5})$',
        views.GeoserverView.as_view()),
    url(r'^togglelang$', views.ToggleLanguageView.as_view(), name='togglelang'),
    url(r'^failedlogin$', views.FailedLoginView.as_view(), name='failedlogin'),
    url(r'^datasetdownload$', views.DatasetDownloadView.as_view(), name='datasetdownload'),
    ]

if settings.ON_VFW_SERVER:
    urlpatterns.append(url(r'^rsp/', include('watts_rsp.urls')))
else:
    urlpatterns.append(path('', include('django.contrib.auth.urls')))
