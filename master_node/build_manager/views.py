# Create your views here.
import http.client
import json
import threading

from django.http import HttpResponse
from .BuildWorker import startWorker

workerStarted = False


def index(request, project_id):
    global workerStarted
    data = json.dumps({'project_id': project_id})
    params = json.dumps({"topic": "Build_Manager_Queue1", "data": data, "priority": 3})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection("localhost:4242")
    conn.request("POST", "/queue/enqueue", params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    print(data)
    conn.close()
    if not workerStarted:
        thread = threading.Thread(target=startWorker)
        thread.start()
        workerStarted = True
    return HttpResponse(data)
