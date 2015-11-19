from django.shortcuts import render

import json
import http.client

from django.http import HttpResponse
from django.http import HttpRequest

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from raspberryq.queuemanager.queue import manager


# Create your views here.

#Create class just for the purpose of Static Function
class StaticClass:
    id = 1
    rQIP = "127.0.0.1"

# Method to get the Cluster ID to deploy  on the Slave Node
def deployProject(request, project_id):
    data = json.dumps({'cluster_id': project_id})
    topic = "Deployment_Manager_Queue"+(StaticClass.id%2)
    StaticClass.id += 1
    params = json.dumps({"topic": topic, "data": data, "priority": 3})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(StaticClass.rQIP+":4242")
    conn.request("POST", "/queue/enqueue", params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    print(data)
    conn.close()
    return HttpResponse(data)






