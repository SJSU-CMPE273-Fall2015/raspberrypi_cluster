import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .queue import manager, SimpleQueueTask


# Create your views here.
@csrf_exempt
@require_http_methods(["POST", "DELETE"])
def createQueue(request):
    """
    { "topic" : "<TOPIC NAME>", "size" : <SIZE> }

    POST:
    http://127.0.0.1:8000/queue/
    {"topic":"testQ",  "size":3}


    :param request:
    :return:
    """
    if request.method == 'DELETE':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        manager.removeQueue(body_data['topic'])
        return HttpResponse("")

    elif request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        success = manager.createQueue(body_data['topic'], body_data['size'])
        if not success:
            return HttpResponse(json.dumps({"error": "Topic name already taken"}))
        return HttpResponse(json.dumps({"topic": body_data['topic']}))


@csrf_exempt
@require_http_methods(["POST"])
def enqueue(request):
    """
    { "data":"<DATA>", "priority": 1 to 3, "topic":"<TOPIC>"}

     http://127.0.0.1:8000/queue/enqueue
     {"topic":"testQ", "data":"{'project_id':10}", "priority":3}

    :param request:
    :return:
    """
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)

    task = SimpleQueueTask(body_data['data'], 0, body_data['priority'])

    success = manager.enqueue(body_data['topic'], task)
    if not success:
        error = {"error": "Either queue is not present or is Full", "task": task.task_id}
        return HttpResponse(json.dumps(error))

    reply = {"topic": body_data['topic'], "task_id": task.task_id}
    return HttpResponse(json.dumps(reply))


def dequeue(request, topic):
    """
    Use get method;
     http://127.0.0.1:8000/queue/dequeue/<topic>

     http://127.0.0.1:8000/queue/dequeue/testQ
    :param request:
    :param topic:
    :return:
    """
    success = manager.getQueue(topic).dequeue()
    if not success:
        error = {"error": "Either queue is not present or is Empty", "topic": topic}
        return HttpResponse(json.dumps(error))
    return HttpResponse(success)

@csrf_exempt
@require_http_methods(["POST"])
def fetch(request, topic):
    """
    Use get method;
     http://127.0.0.1:8000/queue/fetch/<topic>

     http://127.0.0.1:8000/queue/fetch/testQ
    :param request:
    :param topic:
    :return:
    """
    success = manager.getQueue(topic).pop()
    if not success:
        error = {"error": "Either queue is not present or is Empty", "topic": topic}
        return HttpResponse(json.dumps(error))
    return HttpResponse(success)

@csrf_exempt
@require_http_methods(["POST"])
def addToSuccessQueue(request):
    """
     http://127.0.0.1:8000/queue/successq
    {"topic":"<topic>", "task_id":<task_id>}

    :param request:
    :return:
    """
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)

    success = manager.addToSuccessQueue(body_data['topic'], body_data['task_id'])
    if not success:
        error = {"error": "Either queue is not present or is Empty", "topic": body_data['topic']}
        return HttpResponse(json.dumps(error))
    return HttpResponse("")


@csrf_exempt
@require_http_methods(["POST"])
def addToFailureQueue(request):
    """
     http://127.0.0.1:8000/queue/failureq
    {"topic":"<topic>", "task_id":<task_id>}
    :param request:
    :return:
    """
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    print(body_data)
    success = manager.addToFailureQueue(body_data['topic'], body_data['task_id'])
    if not success:
        error = {"error": "Either queue is not present or is Empty", "topic": body_data['topic']}
        return HttpResponse(json.dumps(error))
    return HttpResponse("")


@csrf_exempt
@require_http_methods(["POST"])
def checkStatus(request):
    """
     http://127.0.0.1:8000/queue/checkStatus
     { "task_id": 2090706289, "topic":"testQ"}
    :param request:
    :return:
    """
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    status = manager.checkStatus(body_data['topic'], body_data['task_id'])
    reply = {"status": status, "topic": body_data['topic'], "task_id": body_data['task_id']}
    return HttpResponse(json.dumps(reply))
