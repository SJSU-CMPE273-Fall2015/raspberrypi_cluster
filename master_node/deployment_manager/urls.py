from django.conf.urls import url
from .import views

urlpatterns = [
    # Deploy it on a Cluster
    url(r'^deploy/(?<topic>\w{0,50})$', views.dequeue, name='views.deployClusterID'),
]