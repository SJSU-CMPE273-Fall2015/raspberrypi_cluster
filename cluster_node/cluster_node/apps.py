__author__ = 'aditya'

import http.client,urllib.parse
import json

class NodeClusterManager:
    is_initialized = False

    def initialize(self):
        if not self.is_initialized:
            self.initialize_cluster()

    def initialize_cluster(self):
        params = json.dumps({"topic": "Cluster_Node_Manager_Queue1", "size": 10})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = http.client.HTTPConnection("localhost:4242")
        conn.request("POST", "/queue/", params, headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        conn.close()