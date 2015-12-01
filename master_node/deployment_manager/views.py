from django.shortcuts import render

import json
import http.client
import datetime


from django.http import HttpResponse
from django.http import HttpRequest

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core.models import ClusterProject,ProjectBuild,Cluster

# Create your views here.

#Create class just for the purpose of Static Function


class StaticClass:
    id = 1
    rQIP = "127.0.0.1"
    #numberOfClusters = 1

    #numberOfClusters[] = Cluster.objects.filter(status = "active")

# Method to get the Cluster ID to deploy  on the Slave Node
def deployProject(request, project_id):
    project_BuildLoc = ProjectBuild.objects.filter(project_id = project_id).order_by('-time')[:1]
    data = json.dumps({'project_id': project_id,'build_location' : project_BuildLoc[0].build.name})
    print(data)

    clusters = Cluster.objects.filter(status="active")

    print("Clusters "+str(clusters))

    index = StaticClass.id%len(clusters)

    print(index)


    #idFromList = StaticClass.id%len(StaticClass.numberOfClusters)
    #print(idFromList)

    #print("%%%%%%"+str(StaticClass.numberOfClusters[idFromList]))

    topic = "Deployment_Manager_Queue"+str(clusters[index].id)

    #topic = "Deployment_Manager_Queue"+str(clusters)

    #topic = "Deployment_Manager_Queue"+str((StaticClass.id%StaticClass.numberOfClusters ) + 1)
    StaticClass.id += 1
    params = json.dumps({"topic": topic, "data": data, "priority": 3})
    print(params)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(StaticClass.rQIP+":4242")
    conn.request("POST", "/queue/enqueue", params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    print(data)
    conn.close()
    return HttpResponse(data)

def reportStatus(request):
    data_project_id = json.loads(request['project_id'])
    data_cluster_id = json.loads(request['cluster_id'])
    data_url = json.loads(request['url'])
    #data_pid = json.loads(request['pid'])

    # Add the entry to the DataBase and to models.py,parse the corresponding entry
    ClusterProject.cluster = data_cluster_id
    ClusterProject.project = data_project_id
    ClusterProject.status = "Deployed"
    ClusterProject.time = datetime.datetime.now()
    ClusterProject.url = data_url
    ClusterProject.pid = 1

    ClusterProject.save()





