# Create your views here.
from django.http import HttpResponse
import http.client, urllib.parse
from .BuildManager import *
import json
from .BuildWorker import startWorker
import threading


def index(request, project_id):
    data = json.dumps({'project_id': project_id})
    params = json.dumps({"topic": "Build_Manager_Queue1", "data": data, "priority": 3})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection("localhost:4242")
    conn.request("POST", "/queue/enqueue", params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    print(data)
    conn.close()
    thread = threading.Thread(target=startWorker)
    thread.start()
    return HttpResponse(data)
