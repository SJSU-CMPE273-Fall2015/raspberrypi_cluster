from django.conf.urls import url
from .import views

urlpatterns = [
    # Deploy it on a Cluster
    url(r'^deploy/(?<projectID>\w{0,50})$', views.deployProject, name='views.deployProject'),
]