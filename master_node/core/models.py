from django.db import models
from django.contrib.auth.models import User


# Create your models here.


# TODO: For now allowed null. Remove when not required.
# TODO: USe auth_user defaut table
# class User(models.Model):
#     username = models.CharField(max_length=255)
#     password = models.CharField(max_length=255)
#     email = models.EmailField(max_length=255, null=True)
#     name = models.CharField(max_length=255, null=True)
#     lname = models.CharField(max_length=255, null=True)
#     is_admin = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.username


class Project(models.Model):
    project_name = models.CharField(max_length=255)
    url = models.URLField(max_length=255, null=True)
    owner = models.ForeignKey(User, null=True)
    last_build_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name

    def to_dict(self):
        data={}
        data['project_name']=self.project_name
        data['url']=self.url
        data['owner']=self.owner.username
        data['last_build_time']=str(self.last_build_time)
        data['created_time']=str(self.created_time)
        return data


class Cluster(models.Model):
    ip = models.GenericIPAddressField(max_length=20, null=True)
    location = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    last_boot_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, null = True)

    def __str__(self):
        return self.ip


class SystemAudit(models.Model):
    disk_usage = models.FloatField(null=True)
    memory_usage = models.FloatField(null=True)
    cpu_usage = models.FloatField(null=True)
    network_usage = models.FloatField(null=True)
    cluster = models.ForeignKey(Cluster, null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.cluster) + ":" + str(self.time)

    def to_dict(self):
        data={}
        data['disk_usage']=self.disk_usage
        data['memory_usage']=self.memory_usage
        data['cpu_usage']=self.cpu_usage
        data['network_usage']=self.network_usage
        data['cluster']=self.cluster.ip
        data['time']=self.time
        return data

class ProjectAudit(models.Model):
    message = models.CharField(max_length=255, null=True)
    tag = models.CharField(max_length=255, null=True)
    time = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, null=True)

    def __str__(self):
        return self.project + ":" + self.time


class ClusterProject(models.Model):
    cluster = models.ForeignKey(Cluster, null=True)
    project = models.ForeignKey(Project, null=True)
    status = models.CharField(max_length=255, null=True)
    time = models.DateTimeField(auto_now_add=True)
    #newly added.
    url = models.CharField(max_length=255, null=True)
    pid = models.IntegerField(blank=False)

    def __str__(self):
        return self.cluster + ":" + self.project


class ProjectBuild(models.Model):
    project = models.ForeignKey(Project, null=True)
    build = models.FileField(null=True)
    log = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project + ":" + self.time
