from django.conf.urls import include
from django.urls import path, re_path

from heron import settings
from . import views


app_name = 'vfw_home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('watts_login', views.LoginView.as_view(), name='watts_login'),
    path('help', views.HelpView.as_view(), name='help'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('geoserver/<str:service>/<str:layer>/<str:bbox>/<int:srid>', views.GeoserverView.as_view()),
    path('togglelang', views.ToggleLanguageView.as_view(), name='togglelang'),
    path('failedlogin', views.FailedLoginView.as_view(), name='failedlogin'),
    path('datasetdownload', views.DatasetDownloadView.as_view(), name='datasetdownload'),
    path('entries_pagination', views.entries_pagination, name='entries_pagination'),
    path('short_info_pagination', views.short_info_pagination, name='short_info_pagination'),
    path('advanced_filter', views.advanced_filter),
    path('quick_filter_args/<selection>', views.QuickFilterResults.as_view(), name='quick_filter_args'),
    # addresses for ajax:
    path('previewplot', views.previewplot, name='previewplot'),
    path('show_info', views.show_info, name='show_info'),
    path('workspace_data', views.workspace_data, name='workspace_data'),
]

# use watts for authorization, or django for development environment
if settings.ON_VFW_SERVER:
    urlpatterns.append(re_path(r'^rsp/', include('watts_rsp.urls')))
else:
    urlpatterns.append(path('', include('django.contrib.auth.urls')))
