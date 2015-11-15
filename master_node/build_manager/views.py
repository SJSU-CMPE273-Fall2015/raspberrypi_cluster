# Create your views here.
from django.http import HttpResponse
import http.client, urllib.parse
from .BuildManager import *


def index(request):
    find_project(4)
    params = urllib.parse.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection("bugs.python.org")
    conn.request("POST", "", params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    conn.close()
    return HttpResponse("Hello, world. You're at the build manager index.")
