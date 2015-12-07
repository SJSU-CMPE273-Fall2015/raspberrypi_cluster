import configparser
import json
import http.client
import datetime

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core.models import ClusterProject, ProjectBuild, Cluster


# Create your views here.

# Create class just for the purpose of Static Function

config = configparser.ConfigParser()
config.read('config.txt')
rq_id = config['CONFIGURATION']['RQ_ID']


class StaticClass:
    id = 1
    rQIP = "127.0.0.1"
    # numberOfClusters = 1

    # numberOfClusters[] = Cluster.objects.filter(status = "active")


# Method to get the Cluster ID to deploy  on the Slave Node
def deployProject(request, project_id):
    project_BuildLoc = ProjectBuild.objects.filter(project_id=project_id).order_by('-time')[:1]
    data = json.dumps({'project_id': project_id, 'build_location': project_BuildLoc[0].build.name})
    print(data)

    clusters = Cluster.objects.filter(status="active")

    print("Clusters " + str(clusters))

    index = StaticClass.id % len(clusters)

    print(index)


    # idFromList = StaticClass.id%len(StaticClass.numberOfClusters)
    # print(idFromList)

    # print("%%%%%%"+str(StaticClass.numberOfClusters[idFromList]))

    topic = "Deployment_Manager_Queue" + str(clusters[index].id)

    # topic = "Deployment_Manager_Queue"+str(clusters)

    # topic = "Deployment_Manager_Queue"+str((StaticClass.id%StaticClass.numberOfClusters ) + 1)
    StaticClass.id += 1
    params = json.dumps({"topic": topic, "data": data, "priority": 3})
    print(params)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(StaticClass.rQIP + ":4242")
    conn.request("POST", "/queue/enqueue", params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    print(data)
    conn.close()
    return HttpResponse(data)


def reportStatus(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    data_cluster_id = data['cluster_id']
    data_url = data['url']
    # data_pid = json.loads(request['pid'])
    
    entry = ClusterProject()
    # Add the entry to the DataBase and to models.py,parse the corresponding entry
    entry.cluster_id = data_cluster_id
    entry.project_id = data_project_id
    entry.status = "Deployed"
    entry.time = datetime.datetime.now()
    entry.url = data_url
    entry.pid = 1

    entry.save()


@csrf_exempt
@require_http_methods(["POST"])
def deployProjectWithHighPriority(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    params = json.dumps(body_data)
    projects = params['projects']
    id = 1
    for project_id in projects:
        project_BuildLoc = ProjectBuild.objects.filter(project_id=project_id).order_by('-time')[:1]
        data = json.dumps({'project_id': project_id, 'build_location': project_BuildLoc[0].build.name})
        print(data)
        clusters = Cluster.objects.filter(status="active")
        print("Clusters " + str(clusters))
        index = id % len(clusters)
        print(index)
        topic = "Deployment_Manager_Queue" + str(clusters[index].id)
        params = json.dumps({"topic": topic, "data": data, "priority": 0})
        print(params)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = http.client.HTTPConnection(rq_id)
        conn.request("POST", "/queue/enqueue", params, headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        print(data)
        conn.close()
        id = id + 1
    return HttpResponse(data)
