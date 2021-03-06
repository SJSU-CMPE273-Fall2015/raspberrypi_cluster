import json
import http.client

import MySQLdb as db
from core.forms import *
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader, Context, RequestContext
from django.views.decorators.http import require_http_methods
from .models import Project
from .models import ClusterProject
from .models import ProjectAudit
from .models import ProjectBuild
from .models import DBuser
from .models import SystemAudit
from .models import Cluster
import configparser
import MySQLdb as db


config = configparser.ConfigParser()
config.read('config.txt')
rq_id = config['CONFIGURATION']['RQ_ID']


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
        create_databaseschema(user)
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

def create_databaseschema(user):
    con = db.connect(host='127.0.0.1',user="pi",passwd="raspberry")
    cur = con.cursor()
    cur.execute('CREATE DATABASE '+user.username)





def create_databaseschema(user):
    con = db.connect(host='127.0.0.1', user="pi", passwd='raspberry')
    cur = con.cursor()
    cur.execute('CREATE DATABASE ' + 'clusterdb_' + user.username)
    entry = DBuser()
    entry.user_id = user.id
    entry.url = '192.168.137.4:3306'
    entry.dbname = 'clusterdb_' + user.username
    entry.save()


def register_success(request):
    return render_to_response(
        'registration/success.html',
    )


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def getProjects(request):
    projects = Project.objects.all()
    output = []
    for project in projects:
        output.append(project.to_dict())
    return HttpResponse(json.dumps(output))


def home(request):
    people = Project.objects.filter(owner=request.user)
    print(request.user.id)
    db = DBuser.objects.filter(user_id = request.user.id)
    response = {}
    if len(db) > 0:
        response['user'] = db[0].user.username
        response['url'] = db[0].url
        response['dbname'] = db[0].dbname
    print(response)
    t = loader.get_template('home.html')
    c = Context({'people': people, 'profiles': response})
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


@csrf_exempt
@require_http_methods(["POST"])
def checkStatus(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    params = json.dumps(body_data)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(rq_id)
    conn.request("POST", "/queue/checkStatus", params, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return HttpResponse(data)

