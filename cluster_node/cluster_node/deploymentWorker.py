from master_node.build_manager.BuilderWorker import addToQueue

__author__ = 'aditya'

import http.client,urllib.parse
import json
import time
import traceback
import cluster_node.cluster_node.config
from master_node.build_manager.BuildManager import find_project
from master_node.deployment_manager.views import deployProject

class NodeClusterManager:
    is_initialized = False

    def initialize(self):
        if not self.is_initialized:
            self.initialize_cluster()

    def initialize_cluster(self):
        name = "Deployment_Manager_Queue" + cluster_node.tempVariables.clusterID
        params = json.dumps({"topic":name , "size": 10})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = http.client.HTTPConnection(cluster_node.tempVariables.rQIP+":4242")
        conn.request("POST", "/queue/", params, headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        conn.close()

    def fetchTasks(self):
        conn = http.client.HTTPConnection(cluster_node.tempVariables.rQIP+":4242")
        conn.request("GET","/queue/dequeue/Deployment_Manager_Queue"+cluster_node.tempVariables.clusterID)
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
            find_project(task['project_id'])
            print("Deploy the Project")
            deployProject(request,task['project_id'])
            addToQueue(True,request)
        except Exception:
            print(traceback.format_exc())
            addToQueue(False,request)
            print("Exception Occurred",request)








