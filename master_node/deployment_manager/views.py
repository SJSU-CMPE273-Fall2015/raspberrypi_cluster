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
    clusterID = 1

# Method to get the Cluster ID to deploy  on the Slave Node
def deployClusterID(request, cluster_id):
    data = json.dumps({'cluster_id': cluster_id})
    if(StaticClass.clusterID % 2 == 0):
        topicData = "Build_Manager_Queue"+(StaticClass.clusterID+1)
        StaticClass.clusterID = 1
    else:
        topicData = "Build_Manager_Queue"+ StaticClass.clusterID
        StaticClass.clusterID += 1

    params = json.dumps({"topic": topicData, "data": data, "priority": 3})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection("localhost:4242")
    conn.request("POST", "/queue/enqueue", params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    print(data)
    conn.close()
    return HttpResponse(data)






