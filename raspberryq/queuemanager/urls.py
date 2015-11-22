__author__ = 'saurabh'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.createQueue, name='createqueue'),
    # enqueue
    url(r'^enqueue$', views.enqueue, name='enqueue'),
    # dequeue
    url(r'^dequeue/(?P<topic>\w{0,50})$', views.dequeue, name='views.dequeue'),
    # successq
    url(r'^successq$', views.addToSuccessQueue, name='views.addToSuccessQueue'),
    # failureq
    url(r'^failureq$', views.addToFailureQueue, name='views.addToFailureQueue'),
    # checkStatus
    url(r'^checkStatus$', views.checkStatus, name='views.checkStatus'),

]
