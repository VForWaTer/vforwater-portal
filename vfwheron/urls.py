from django.conf.urls import url, include
from django.urls import path

from heron import settings
from . import views


app_name = 'vfwheron'

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^watts_login$', views.LoginView.as_view(), name='watts_login'),
    url(r'^help$', views.HelpView.as_view(), name='help'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    url(r'^geoserver/(?P<service>[\w{3,4}]+)/(?P<layer>[\w]+)/(?P<bbox>[\-.,\d]+)/(?P<srid>[\d]{4,5})$',
        views.GeoserverView.as_view()),
    url(r'^togglelang$', views.ToggleLanguageView.as_view(), name='togglelang'),
    url(r'^failedlogin$', views.FailedLoginView.as_view(), name='failedlogin'),
    url(r'^datasetdownload$', views.DatasetDownloadView.as_view(), name='datasetdownload'),
    url(r'^entries_pagination$', views.entries_pagination, name='entries_pagination'),
    url(r'^advanced_filter$', views.advanced_filter),
    # url(r'^advanced_filter$', views.filter_entries),
    # addresses for fetch:
    # url(r'^previewplot/id(db[\d]{1,6}|wps[\d]{1,6})$', views.PreviewPlot.as_view()),
    # url(r'^showinfo/id(db[\d]{1,6}|wps[\d]{1,6})$', views.ShowInfo.as_view()),
    # addresses for ajax:
    url(r'^previewplot$', views.previewplot, name='previewplot'),
    url(r'^short_datainfo', views.short_datainfo, name='short_datainfo'),
    url(r'^show_info', views.show_info, name='show_info'),
    url(r'^filter_selection', views.filter_selection, name='filter_selection'),
    url(r'^filter_map_selection', views.filter_map_selection, name='filter_map_selection'),
    url(r'^workspace_data', views.workspace_data, name='workspace_data'),
]

# use watts for authorization, or django for development environment
if settings.ON_VFW_SERVER:
    urlpatterns.append(url(r'^rsp/', include('watts_rsp.urls')))
else:
    urlpatterns.append(path('', include('django.contrib.auth.urls')))
