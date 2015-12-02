from django.conf.urls import url
from deployment_manager import views

urlpatterns = [
    # Deploy it on a Cluster
    url(r'^(?P<project_id>\d{0,11})$', views.deployProject, name='views.deployProject'),
    url(r'^/reportStatus$', views.reportStatus, name='views.reportStatus'),
    #url(r'^?(R<report_id>\d{0,11})$', views.reportStatus, name='views.reportStatus'),
    url(r'^/migrate$', views.deployProjectWithHighPriority, name='views.deployProjectWithHighPriority'),

]