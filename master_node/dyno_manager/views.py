from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from core.models import SystemAudit


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
