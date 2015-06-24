from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tango_with_django_project.views.home', name='home'),
    url(r'^rango/', include('rango.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
