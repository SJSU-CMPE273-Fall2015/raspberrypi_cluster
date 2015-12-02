import configparser

__author__ = 'saurabh'

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "master_node.settings")

# Appending path of master node into sys.path
import sys

sys.path.append('../')

from core.models import Cluster, ClusterProject
import time
import json
import django

django.setup()

import http.client

config = configparser.ConfigParser()
config.read('config.txt')
rq_id = config['CONFIGURATION']['RQ_ID']

class DynoManager():
    def __init__(self):
        self.clusters = []
        self.registerInQueue()

    def check_failure(self):
        print("Checking failures")

        while True:
            conn = http.client.HTTPConnection("localhost:4242")
            conn.request("POST", "/queue/fetch/Dyno_Manager")
            r1 = conn.getresponse()
            data = r1.read().decode("utf-8")
            request = json.loads(data)

            if 'error' in request:
                print("No data")
                break
            payload = json.loads(request['data'])
            self.mark_cluster_present(int(payload['cluster_id']))

            # Checking status to remove element fromo queue
            request['topic'] = 'Dyno_Manager'

        print("Marked clusters:", self.clusters)
        for cluster in Cluster.objects.filter(status='active'):
            if not cluster.id in self.clusters:
                print("Server failed")
                print(cluster.id)
                cluster.status = 'failed'
                self.migrate(cluster)
                cluster.save()
            else:
                self.clusters.remove(cluster.pk)

    def mark_cluster_present(self, cluster):
        if cluster not in self.clusters:
            print("Marking cluster present", cluster)
            self.clusters.append(cluster)

    def migrate(self, failedCluster):
        print("Starting migrations..")
        activeClusters = Cluster.objects.filter(status='active')
        deployedProjects = ClusterProject.objects.filter(cluster_id=failedCluster.id)
        i = 0
        for project in deployedProjects:
            okCluster = activeClusters[i % len(activeClusters)]
            data = json.dumps({'project_id': project.id})
            topic = "Deployment_Manager_Queue" + str(okCluster.id)
            params = json.dumps({"topic": topic, "data": data, "priority": 1})
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
            conn = http.client.HTTPConnection(StaticClass.rQIP + ":4242")
            conn.request("POST", "/queue/enqueue", params, headers)
            response = conn.getresponse()
            print(response.status, response.reason)
            data = response.read()
            print(data)
            conn.close()

    def registerInQueue(self):
        params = json.dumps({"topic": "Dyno_Manager", "size": 50})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = http.client.HTTPConnection("localhost:4242")
        conn.request("POST", "/queue/", params, headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        conn.close()

    def runForever(self):
        print("Starting DynoManager")
        while True:
            self.check_failure()
            time.sleep(20)


dynomanager = DynoManager()
dynomanager.runForever()
