#from master_node.build_manager.BuilderWorker import addToQueue
#from master_node.build_manager.BuilderWorker import fetchTask

__author__ = 'aditya'

import http.client,urllib.parse
import json
import time
import traceback
import configparser

from django.http import HttpResponse


config = configparser.ConfigParser()
config.read('config.txt')
master_ip = config['CONFIGURATION']['MASTER_IP']
cluster_id = config['CONFIGURATION']['CLUSTER_ID']
rq_id = config['CONFIGURATION']['RQ_ID']
num_clusters = config['CONFIGURATION']['NUMBER_OF_CLUSTERS']



class NodeClusterManager:
    is_initialized = False

    def initialize(self):
        if not self.is_initialized:
            self.initialize_cluster()

    def initialize_cluster(self):
        name = "Deployment_Manager_Queue" + str(cluster_id)
        params = json.dumps({"topic":name , "size": 10})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = http.client.HTTPConnection(rq_id)
        conn.request("POST", "/queue/", params, headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        conn.close()

    def fetchTasks(self):
        while True:
            conn = http.client.HTTPConnection(rq_id)
            conn.request("GET","/queue/dequeue/Deployment_Manager_Queue"+str(cluster_id))
            r1 = conn.getresponse()
            print(r1.status,r1.reason)
            data = r1.read().decode('utf-8')
            request = json.loads(data)
            print(request)
            if 'error' in request.keys():
                print("Nothing to be done")
                time.sleep(5)
            else:
                try:
                    task = json.loads(request['data'])
                    print(task)
                    deployProject(task)
                    addToQueue(True,request)
                    #add logic to extract zip files and to make POST call to the Server and pass the cluster_id and Project_id
                    #topic =
                    post_data = {'cluster_id' : cluster_id,'project_id' : task['project_id']}


                except Exception:
                    print(traceback.format_exc())
                    addToQueue(False,request)
                    print("Exception Occurred",request)


def deployProject(task):
    print("DEPLOYING PROJECT#", task['project_id'])


def addToQueue(success, request):
    topic = "Deployment_Manager_Queue"+str((cluster_id))
    params = json.dumps({"topic": topic, "task_id": request['task_id']})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(rq_id)
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
# call the Addd to queuees functionality multilpe times.
nodeObject.fetchTasks()












