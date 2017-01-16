from django.conf.urls import url
from . import views

app_name = 'vfwheron'

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^external_links$', views.ExtlinksView.as_view(), name='external_links'),
]
