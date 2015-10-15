from django.db import models
from django.contrib import admin
class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)
class Project(models.Model):
    projectname = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    owner = models.EmailField(max_length=254)
    last_builttime = models.DateTimeField(auto_now=False)
    created_time = models.DateTimeField(auto_now=False) 
class Cluster(models.Model):
    ip = models.CharField(max_length=20)
    location = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    last_boottime = models.DateTimeField(auto_now=False)
class Audit(models.Model):
    disk_usage = models.FloatField()
    memory_usage = models.FloatField()
    cpu_usage = models.FloatField()  
    network_usage = models.FloatField()
    cluster_id = models.IntegerField()
    time = models.DateTimeField(auto_now=True)
class Cluster_project(models.Model):
    cluster_id = models.IntegerField()
    project_id = models.IntegerField()
    time = models.DateTimeField(auto_now=True)
admin.site.register(User)
