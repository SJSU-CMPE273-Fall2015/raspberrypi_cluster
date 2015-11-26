from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from core.models import SystemAudit, Cluster


@csrf_exempt
def systemstatus(request):
    body_unicode = request.body.decode('utf-8')
    stat = json.loads(body_unicode)
    auditEntry = SystemAudit(disk_usage=stat['disk_usage'],
                             memory_usage=stat['memory_usage'],
                             cpu_usage=stat['cpu_usage'],
                             network_usage=stat['network_usage'],
                             )
    auditEntry.cluster_id = stat['cluster']
    auditEntry.save()
    return HttpResponse(stat.__str__())


@csrf_exempt
def registerCluster(request):
    body_unicode = request.body.decode('utf-8')
    clusterData = json.loads(body_unicode)
    cluster = Cluster()
    cluster.ip = clusterData['ip']
    cluster.location = clusterData['location']
    cluster.type = clusterData['type']
    cluster.last_boot_time = clusterData['last_boot_time']
    cluster.status='active'
    cluster.save()

