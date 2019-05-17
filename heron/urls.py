"""heron URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView


print('   *   heron urls.py')

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='vfwheron/', permanent=False)),
    url(r'^vfwheron/', include('vfwheron.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^heron_wps/', include('heron_wps.urls', namespace='heron_wps')),
    url(r'^heron_monitor/', include('heron_monitor.urls', namespace='heron_monitor')),
    url(r'^heron_visual/', include('heron_visual.urls', namespace='heron_visual')),    
    url(r'^heron_upload/', include('heron_upload.urls', namespace='heron_upload')),
    #  url(r'^', include('wps_workflow.urls')),  # from wps_workflow
    url(r'^wps_workflow/', include('wps_workflow.urls', namespace='wps_workflow')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),  # from wps_workflow
    url(r'^AuthorizationManagement/', include('AuthorizationManagement.urls', namespace='AuthorizationManagement')),
]


# This is just to test the upload in the development environment
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
