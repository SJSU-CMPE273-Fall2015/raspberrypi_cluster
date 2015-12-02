__author__ = 'saurabh'
import http.client
import json
import time
import traceback
import configparser

from .BuildManager import find_project

config = configparser.ConfigParser()
config.read('config.txt')
rq_id = config['CONFIGURATION']['RQ_ID']

def fetchTask():
    conn = http.client.HTTPConnection(rq_id)
    conn.request("GET", "/queue/dequeue/Build_Manager_Queue1")
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    data1 = r1.read().decode("utf-8")
    request = json.loads(data1)
    if 'error' in request.keys():
        print("Nothing to do... Sleeping.. ")
        time.sleep(5)
        return

    try:
        print(request)
        task = json.loads(request['data'])
        print(task)
        find_project(task['project_id'])
        print("Adding task to success queue", request)
        addToQueue(True, request)
    except Exception:
        print(traceback.format_exc())
        addToQueue(False, request)
        print("Exception occurred... Failing task.. ", request)


def addToQueue(success, request):
    params = json.dumps({"topic": "Build_Manager_Queue1", "task_id": request['task_id']})
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


def startWorker():
    while True:
        fetchTask()
