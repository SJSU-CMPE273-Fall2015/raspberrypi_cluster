__author__ = 'saurabh'

import psutil
import time
import json
import http.client
import configparser

config = configparser.ConfigParser()
config.read('config.txt')
master_ip = config['CONFIGURATION']['MASTER_IP']
cluster_id = config['CONFIGURATION']['CLUSTER_ID']

while True:
    stat = {}
    stat['disk_usage'] = psutil.disk_usage('/').percent
    stat['memory_usage'] = psutil.virtual_memory().percent
    stat['cpu_usage'] = psutil.cpu_percent()
    netio1 = psutil.net_io_counters()
    time.sleep(1)
    netio2 = psutil.net_io_counters()
    stat['network_usage'] = (netio2.bytes_sent - netio1.bytes_sent) / 1000
    stat['cluster'] = cluster_id

    data = json.dumps(stat)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(master_ip)
    conn.request("POST", "/dyno/", data, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    print(data)
    conn.close()
    time.sleep(5)
