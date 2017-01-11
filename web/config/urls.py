## @file web/urls.py
#  @brief Django urls

from django.conf.urls import patterns, include, url
#from django.conf import settings

import views
#import version.models

#web_srv_prefix = version.models.getWebSrvPrefix()

urlpatterns = patterns('',
                       url(r"^ajax/(?P<module>\w+)/(?P<function>\w+)/", views.ajax, name='ajax'),
                       url(r'^$', views.index, name='index')
                       #url(r'^', views.index, name='index')
)



