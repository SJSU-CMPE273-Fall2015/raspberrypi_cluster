from django.shortcuts import render
from core.forms import *
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader, Context, RequestContext
from .models import Project
from .models import ClusterProject
from .models import ProjectAudit
from .models import ProjectBuild



@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
        return HttpResponseRedirect('/register/success/')

    else:
        form = RegistrationForm()
        variables = RequestContext(request, {
            'form': form
        })

        return render_to_response(
            'registration/register.html',
            variables,
        )


def register_success(request):
    return render_to_response(
        'registration/success.html',
    )


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def home(request):
    people = Project.objects.filter(owner=request.user)
    t = loader.get_template('home.html')
    c = Context({'people': people})
    return HttpResponse(t.render(c))


def insert(request):
    # If this is a post request we insert the person
    if request.method == 'POST':
        p = Project(
            project_name=request.POST['project_name'],
            url=request.POST['url'],
            owner=request.user
        )
        p.save()
        return HttpResponseRedirect('/')
    t = loader.get_template('insert.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


def delete(request, project_id):
    p = Project.objects.get(pk=project_id)
    p.delete()
    return HttpResponseRedirect('/')


def edit(request, project_id):
    p = Project.objects.get(pk=project_id)
    if request.method == 'POST':
        p.project_name = request.POST['project_name']
        p.url = request.POST['url']
        p.owner = request.user
        p.save()
        return HttpResponseRedirect('/')
    t = loader.get_template('insert.html')
    c = RequestContext(request, {
        'project': p
    })
    return HttpResponse(t.render(c))


def info(request):
    build = ProjectBuild.objects.all()
    deploy = ClusterProject.objects.all()
    dyno = ProjectAudit.objects.all()
    t = loader.get_template('info.html')
    c = Context({'build': build}, {'deploy': deploy}, {'dyno': dyno})
    return HttpResponse(t.render(c))
