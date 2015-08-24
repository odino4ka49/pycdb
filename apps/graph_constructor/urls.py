__author__ = '1ka'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'graph_constructor.views.index', name="constructor-index"),
    url(r'^configData', 'graph_constructor.views.configData', name="views-configdata"),
)
