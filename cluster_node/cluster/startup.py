import datetime
import json
import http.client
import configparser



config = configparser.ConfigParser()

config.read('config.txt')
master_ip = config['CONFIGURATION']['MASTER_IP']
cluster_id = config['CONFIGURATION']['CLUSTER_ID']

def writetoconfig(id):
    config = configparser.ConfigParser()

    config.add_section('CONFIGURATION')
    config.set('CONFIGURATION', 'MASTER_IP', '192.168.137.4:8000')
    config.set('CONFIGURATION', 'CLUSTER_ID', str(id))
    config.set('CONFIGURATION', 'RQ_ID', '127.0.0.1:4242')
    config.set('CONFIGURATION', 'NUMBER_OF_CLUSTERS', '2')


# Writing our configuration file to 'example.cfg'
    with open('config.txt', 'w') as configfile:
        config.write(configfile)

def register():
    clusterData = {}
    clusterData['ip'] = "127.0.0.1"
    clusterData['location'] = "USA"
    clusterData['type'] = "Raspberry PI"
    #clusterData['id'] = cluster_id
    #clusterData['last_boot_time']=str(datetime.datetime.now())

    data = json.dumps(clusterData)
    print(data)

    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection('localhost:8000')
    conn.request("POST", "/dyno/register", data, headers)
    response = conn.getresponse().read()
    print(response)
    body_unicode = response.decode('utf-8')
    cluster_data = json.loads(body_unicode)
    writetoconfig(cluster_data["id"])

register()


