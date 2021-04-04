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
from django.urls import path
from django.views.generic.base import RedirectView
from vfwheron import views as vfw_views


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='home/', permanent=False)),
    url(r'^home/', include('vfwheron.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^workspace/', include('wps_gui.urls', namespace='wps_gui')),
    url(r'^monitor/', include('heron_monitor.urls', namespace='heron_monitor')),
    url(r'^visual/', include('heron_visual.urls', namespace='heron_visual')),
    url(r'^upload/', include('upload.urls', namespace='upload')),
    url(r'^download/(?P<name>\w{4,5})$', vfw_views.DownloadView.as_view()),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),  # from wps_workflow
    url(r'^user/', include('author_manage.urls', namespace='author_manage')),
]

handler404 = 'vfwheron.views.error_404_view'

# This is just to test the upload in the development environment
if settings.DEBUG and settings.DEBUG is not '':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
