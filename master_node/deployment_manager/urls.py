from django.conf.urls import url
from .import views

urlpatterns = [
    # Deploy it on a Cluster
    url(r'^(?P<project_id>\d{0,11})$', views.deployProject, name='views.deployProject'),
]