from django.contrib import admin
from .models import User, Cluster, ClusterProject, Project, ProjectAudit, ProjectBuild, SystemAudit

# Register your models here.

admin.site.register(User)
admin.site.register(Cluster)
admin.site.register(ClusterProject)
admin.site.register(Project)
admin.site.register(ProjectAudit)
admin.site.register(ProjectBuild)
admin.site.register(SystemAudit)
