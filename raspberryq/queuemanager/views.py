from django.shortcuts import render
from django.http import HttpResponse
from .models import RQueue, QueueTask
from django.views.decorators.http import require_http_methods
from .queue import manager


# Create your views here.
# @require_http_methods(["POST"])
def createQueue(request):
    print(request.POST)
    manager.createQueue(request.POST['topic'])
    return HttpResponse("Create Queue")


@require_http_methods(["POST"])
def enqueue(request):
    return HttpResponse("Enqueue")
    pass


@require_http_methods(["GET"])
def dequeue(request):
    return HttpResponse("Dequeue")
    pass
