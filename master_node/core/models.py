from django.db import models

# Create your models here.
from django.contrib import admin

#TODO: For now allowed null. Remove when not required.

class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    lname = models.CharField(max_length=255, null=True)
    is_admin = models.BooleanField(default=False)


class Project(models.Model):
    project_name = models.CharField(max_length=255)
    url = models.URLField(max_length=255, null=True)
    owner = models.ForeignKey(User, null=True)
    last_build_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)


class Cluster(models.Model):
    ip = models.GenericIPAddressField(max_length=20, null=True)
    location = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    last_boot_time = models.DateTimeField(auto_now=True)


class SystemAudit(models.Model):
    disk_usage = models.FloatField(null=True)
    memory_usage = models.FloatField(null=True)
    cpu_usage = models.FloatField(null=True)
    network_usage = models.FloatField(null=True)
    cluster_id = models.ForeignKey(Cluster, null=True)
    time = models.DateTimeField(auto_now_add=True)


class ProjectAudit(models.Model):
    message = models.CharField(max_length=255, null=True)
    tag = models.CharField(max_length=255, null=True)
    time = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, null=True)


class ClusterProject(models.Model):
    cluster = models.ForeignKey(Cluster, null=True)
    project = models.ForeignKey(Project, null=True)
    status = models.CharField(max_length=255, null=True)
    time = models.DateTimeField(auto_now_add=True)


class ProjectBuild(models.Model):
    project = models.ForeignKey(Project, null=True)

    #TODO: Kept this field as binary. If required will change this.
    build = models.BinaryField(null=True)
    time = models.DateTimeField(auto_now_add=True)
