from django.contrib import admin
from .models import Cluster, ClusterProject, Project, ProjectAudit, ProjectBuild, SystemAudit
from django.template import loader, Context, RequestContext
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
# Register your models here.

#admin.site.register(User)
admin.site.register(Cluster)
admin.site.register(ClusterProject)
admin.site.register(Project)
#admin.site.register(ProjectAudit)
#admin.site.register(ProjectBuild)
admin.site.register(SystemAudit)


def index(request):
    p = Project.objects.all()
    t = loader.get_template('admin/index.html')
    c = Context({'p': p})
    return HttpResponse(t.render(c))