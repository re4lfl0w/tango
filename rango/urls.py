from django.conf.urls import patterns, include, url
from django.contrib import admin
from rango import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category,
        name='category'),
    # url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),  # New!
)
