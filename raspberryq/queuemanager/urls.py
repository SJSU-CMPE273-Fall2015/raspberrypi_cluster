__author__ = 'saurabh'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^', views.createQueue, name='createqueue'),
    url(r'^enqueue$', views.enqueue, name='enqueue'),
    url(r'^dequeue$', views.dequeue, name='dequeue'),
]
