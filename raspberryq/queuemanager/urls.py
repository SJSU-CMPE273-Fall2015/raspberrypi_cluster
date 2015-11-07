__author__ = 'saurabh'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.createQueue, name='createqueue'),
    url(r'^enqueue$', views.enqueue, name='enqueue'),
    url(r'^dequeue/(?P<topic>\w{0,50})$', views.dequeue, name='views.dequeue'),
    url(r'^successq$', views.addToSuccessQueue, name='views.addToSuccessQueue'),
    url(r'^checkStatus$', views.checkStatus, name='views.checkStatus'),

]
