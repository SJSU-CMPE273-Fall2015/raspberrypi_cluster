__author__ = 'saurabh'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<project_id>\d{0,11})$', views.index, name='views.index'),
]
