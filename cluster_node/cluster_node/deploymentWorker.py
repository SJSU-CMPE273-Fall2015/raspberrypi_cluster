#from master_node.build_manager.BuilderWorker import addToQueue

__author__ = 'aditya'

import http.client,urllib.parse
import json
import time
import traceback
import config
from django.http import HttpResponse


class NodeClusterManager:
    is_initialized = False

    def initialize(self):
        if not self.is_initialized:
            self.initialize_cluster()

    def initialize_cluster(self):
        name = "Deployment_Manager_Queue" + str(config.tempVariables.clusterID)
        params = json.dumps({"topic":name , "size": 10})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = http.client.HTTPConnection(config.tempVariables.rQIP+":4242")
        conn.request("POST", "/queue/", params, headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        conn.close()

    def fetchTasks(self):
        conn = http.client.HTTPConnection(config.tempVariables.rQIP+":4242")
        conn.request("GET","/queue/dequeue/Deployment_Manager_Queue"+str(config.tempVariables.clusterID))
        r1 = conn.getresponse()
        print(r1.status,r1.reason)
        data = r1.read().decode('utf-8')
        request = json.loads(data)
        if 'error' in request.keys():
            print("Nothing to be done")
            time.sleep(5)
            return
        try:
            print(request)
            task = json.loads(request['data'])
            print(task)
            deployProject(request,task['project_id'])
            addToQueue(True,request)
        except Exception:
            print(traceback.format_exc())
            addToQueue(False,request)
            print("Exception Occurred",request)


def deployProject(request, param):
    data = json.dumps({'project_id': (config.tempVariables.clusterID)})
    topic = "Deployment_Manager_Queue"+str((config.tempVariables.clusterID)%2)
    config.tempVariables.clusterID += 1
    params = json.dumps({"topic": topic, "data": data, "priority": 3})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(config.tempVariables.clusterID.rQIP+":4242")
    conn.request("POST", "/queue/enqueue", params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    print(data)
    conn.close()
    return HttpResponse(data)



def addToQueue(success, request):
    topic = "Deployment_Manager_Queue"+str((config.tempVariables.clusterID)%2)
    params = json.dumps({"topic": topic, "task_id": request['task_id']})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection("localhost:4242")
    if success:
        conn.request("POST", "/queue/successq", params, headers)
    else:
        conn.request("POST", "/queue/failureq", params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    print(data)
    conn.close()


nodeObject = NodeClusterManager()
nodeObject.initialize()
nodeObject.fetchTasks()





