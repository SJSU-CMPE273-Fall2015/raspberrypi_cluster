from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Context, RequestContext
from crud.models import User

def index(request):
     people = User.objects.all()
     t = loader.get_template('index.html')
     c = Context({'people': people})
     return HttpResponse(t.render(c))

def insert(request):
    # If this is a post request we insert the person
    if request.method == 'POST':
        p = User(
            name=request.POST['name'],
            lname=request.POST['lname'],
            username=request.POST['username'],
            password=request.POST['password'],
            email=request.POST['email'],
            is_admin=request.POST['is_admin']
        )
        p.save()

    t = loader.get_template('insert.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))

def delete(request, user_id):
    p = User.objects.get(pk=user_id)
    p.delete()
    return HttpResponseRedirect('/')

def edit(request, user_id):
    p = User.objects.get(pk=user_id)
    if request.method == 'POST':
        p.name = request.POST['name']
        p.lname = request.POST['lname']
        p.username = request.POST['username']
        p.password = request.POST['password']
        p.email = request.POST['email']
        p.is_admin = request.POST['is_admin']
        p.save()
    t = loader.get_template('insert.html')
    c = RequestContext(request, {
        'person': p
    })
    return HttpResponse(t.render(c))
