__author__ = 'saurabh'
import http.client
import json
from django.apps import AppConfig

class BuildManagerConfig(AppConfig):
    name = 'build_manager'
    verbose_name = "build_manager"
    is_initialized = False

    def ready(self):
        if not self.is_initialized:
            self.initialize_queues()

    def initialize_queues(self):
        params = json.dumps({"topic": "Build_Manager_Queue1", "size": 10})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = http.client.HTTPConnection('127.0.0.1:4242')
        conn.request("POST", "/queue/", params, headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        conn.close()
