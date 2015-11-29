import json

from core.models import SystemAudit, Cluster
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


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
    cluster.status='active'
    cluster.save()

    reply = {}
    reply['ip'] = cluster.ip
    reply['location'] = cluster.location
    reply['type'] = cluster.type
    reply['id'] = cluster.id
    reply['boot_time'] = str(cluster.last_boot_time)
    return HttpResponse(json.dumps(reply))

