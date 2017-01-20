from django.conf.urls import url

from charts import views


urlpatterns = [
    url(r"^ajax/(?P<module>\w+)/(?P<function>\w+)/", views.ajax, name='ajax'),
    url(r'^$', views.index, name='index')	
]
