__author__ = 'saurabh'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.systemstatus, name='views.systemstatus'),
]
