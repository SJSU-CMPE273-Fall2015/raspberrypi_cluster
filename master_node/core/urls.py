from django.conf.urls import patterns, include, url
from core.views import *
from core import views
 
urlpatterns = patterns('',
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^home/$', views.home, name='home'),
    url(r'^insert/$', views.insert, name='insert'),
    url(r'^delete/(?P<project_id>\d+)$', views.delete, name='delete'),
    url(r'^edit/(?P<project_id>\d+)$', views.edit, name='edit')
)
