from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views
from heron import settings
from .views import WorkflowView
from wps_workflow.views import EditorView

app_name = 'vfwheron'
print('   *   vfwheron urls.py')

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^login$', auth_views.login, {'template_name': 'vfwheron/login.html'}, name='login'),
    url(r'^failedlogin$', auth_views.login, {'template_name': 'vfwheron/failedlogin.html'}, name='failedlogin'),
    url(r'^watts_login$', views.LoginView.as_view(), name='watts_login'),
    url(r'^help$', views.HelpView.as_view(), name='help'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    url(r'^menu$', views.menuView.as_view(), name='menu'),
    url(r'^geoserver/(?P<service>[\w{3,4}]+)/(?P<layer>[\w]+)/(?P<bbox>[\-.,\d]+)/(?P<srid>[\d]{4,5})$', views.GeoserverView.as_view()),
    url(r'^workflowtool/', WorkflowView.as_view(), name='workflowtool'),
]

if settings.ON_VFW_SERVER:
    urlpatterns.append(url(r'^rsp/', include('watts_rsp.urls')))
