from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views


app_name = 'vfwheron'

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^login$', auth_views.login, {'template_name': 'vfwheron/login.html'}, name='login'),
    url(r'^external_links$', views.ExtlinksView.as_view(), name='external_links'),
    #url(r'^rsp/', include('watts_rsp.urls')),
    url(r'^watts_login/', views.LoginView.as_view(), name='watts_login'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout')
]
