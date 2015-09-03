__author__ = '1ka'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'graph_constructor.views.index', name="constructor-index"),
    url(r'^configData', 'graph_constructor.views.configData', name="views-configdata"),
    url(r'^templateData', 'graph_constructor.views.templateData', name="views-templatedata"),
    url(r'^getGraphData', 'graph_constructor.views.getGraphData', name="views-graph-data"),
    url(r'^saveGraph', 'graph_constructor.views.saveGraph', name="views-save-graph"),
)
