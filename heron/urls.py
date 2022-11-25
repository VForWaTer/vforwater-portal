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
from vfw_home import views as vfw_views
from django.views.i18n import JavaScriptCatalog

# TODO: for JS translations see:
#  https://docs.djangoproject.com/en/2.2/topics/i18n/translation/#note-on-performance
urlpatterns = [
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^$', RedirectView.as_view(url='home/', permanent=False)),
    path('home/', include('vfw_home.urls')),
    path('admin/', admin.site.urls),
    path('legals', vfw_views.Legals.as_view(), name='legals'),
    path('privacypolicy', vfw_views.PrivacyPolicy.as_view(), name='privacy_policy'),
    path('workspace/', include('wps_gui.urls', namespace='wps_gui')),
    path('monitor/', include('vfw_status.urls', namespace='vfw_status')),
    path('visual/', include('visual_app.urls', namespace='visual_app')),
    path('upload/', include('upload.urls', namespace='upload')),
    path('download/<str:name>', vfw_views.DownloadView.as_view()),
    path('admin/doc/', include('django.contrib.admindocs.urls')),  # from wps_workflow
    path('user/', include('author_manage.urls', namespace='author_manage')),
    path('oidc/', include('mozilla_django_oidc.urls')),
]

handler404 = 'vfw_home.views.error_404_view'

# This is just to test the upload in the development environment
if settings.DEBUG and settings.DEBUG != '':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
