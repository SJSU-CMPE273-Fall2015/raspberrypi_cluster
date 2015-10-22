# Create your views here.
from django.http import HttpResponse
from .BuildManager import *


def index(request):
    find_project(3)
    return HttpResponse("Hello, world. You're at the build manager index.")
