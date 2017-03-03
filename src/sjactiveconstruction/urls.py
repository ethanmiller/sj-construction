from django.conf.urls import url
from django.contrib import admin

from mapview import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^init/$', views.init, name='init'),
    url(r'^subtype_filters/(?P<fid>[0-9]+)/$', views.subtype_filters)
]
