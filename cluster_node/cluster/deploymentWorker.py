#from master_node.build_manager.BuilderWorker import addToQueue
#from master_node.build_manager.BuilderWorker import fetchTask

__author__ = 'aditya'

import http.client,urllib.parse
import json
import time
import traceback
import configparser

import tarfile
import os
import subprocess
from subprocess import Popen,PIPE

import re

# Base url to store cloned project
base_path = "/home/adityasharma/Desktop/"
script_path = os.getcwd()

from django.http import HttpResponse


config = configparser.ConfigParser()
config.read('config.txt')
master_ip = config['CONFIGURATION']['MASTER_IP']
cluster_id = config['CONFIGURATION']['CLUSTER_ID']
rq_id = config['CONFIGURATION']['RQ_ID']
num_clusters = config['CONFIGURATION']['NUMBER_OF_CLUSTERS']

path = "/home/adityasharma/Desktop/py_MIUT5A.tar.gz"
outpath = "/home/adityasharma/Desktop/"
extractFolderName = ""




class NodeClusterManager:
    is_initialized = False
    portNumber = 5454

    def initialize(self):
        if not self.is_initialized:
            self.initialize_cluster()

    def initialize_cluster(self):
        name = "Deployment_Manager_Queue" + str(cluster_id)
        params = json.dumps({"topic":name , "size": 10})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = http.client.HTTPConnection(rq_id)
        conn.request("POST", "/queue/", params, headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        conn.close()

    def fetchTasks(self):
        while True:
            conn = http.client.HTTPConnection(rq_id)
            conn.request("GET","/queue/dequeue/Deployment_Manager_Queue"+str(cluster_id))
            r1 = conn.getresponse()
            print(r1.status,r1.reason)
            data = r1.read().decode('utf-8')
            request = json.loads(data)
            print(request)
            if 'error' in request.keys():
                print("Nothing to be done")
                time.sleep(5)
            else:
                try:
                    task = json.loads(request['data'])
                    print(task)
                    deployProject(task)
                    addToQueue(True,request)
                    #add logic to extract zip files and to make POST call to the Server and pass the cluster_id and Project_id
                    #topic =
                    post_data = json.dumps({'cluster_id' : cluster_id,'project_id' : task['project_id']})
                    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                    conn = http.client.HTTPConnection(master_ip)
                    conn.request("POST", "/deployment_manager/reportStatus", post_data, headers)
                    response = conn.getresponse()
                    print(response.status,response.reason)
                    data = response.read
                    print(data)
                    conn.close()
                    #Call to get the process id of the process that has been started recently from our end
                    #getProcessID()

                except Exception:
                    print(traceback.format_exc())
                    addToQueue(False,request)
                    print("Exception Occurred",request)


#Get the process id of the python prog started through the runserver command and return its PID.
def getProcessID():
    pids = []
    list = os.popen("tasklist").readlines()
    for program in list:
        try:
            pids.append(int(program[29:34]))
        except:
            pass
        for each in pids:
            print(each)



def deployProject(task):
    print("DEPLOYING PROJECT#", task['project_id'])

    fh = open(path)

    p = path.split('/')

    global extractFolderName
    extractFolderName = outpath + p[len(p) - 1].split('.')[0].split('_')[1]

    print("File has been extracetd at the location "+extractFolderName)

    tarExt = tarfile.open(path)

    #Extract the Tar file contents to the Desktop and the Extract all would then name the Fodler as the Tar File name
    tarExt.extractall(outpath)

    tarExt.close()

    #Check if the run.txt file exists in the Folder or not.
    dataFile = open(extractFolderName+"/run.txt",'r')

    for line in dataFile:
        if ".go" in line:
            print("GO File Present")
        else :
            if ".py" in line:
                print("Python File Present")
                errorExists = executeFile()
                if errorExists == True:
                    print("Error Exists while return from executeFile function")
                    return
                else :
                    print("The file has been run and now changes have to be saved in the DataBase.")
            else :
                print("Error , no file present")


def executeFile():
    print("In the function for running the executable file")

    cmd = "./param_runserver.sh"


    # subprocess.call('echo $HOME',shell=True)
    #
    # subprocess.call('echo $PWD',shell=True)

    #subprocess.call('$python home/adityasharma/Desktop/ZZ64Y0/manage.py runserver 5656',shell=True)

    # print ('\nread:')
    # proc = subprocess.Popen(['echo', '"to stdout"'],
    #                     stdout=subprocess.PIPE,
    #                     )
    # stdout_value = proc.communicate()[0]
    # print ('\tstdout:', repr(stdout_value))

    #path1 = "home/adityasharma/Desktop/ZZ64Y0/manage.py"

    # dataFile = open("/home/adityasharma/Desktop/ZZ64Y0/manage.py",'r')
    #
    #
    #
    #
    # print ('\nread:')
    # proc1 = subprocess.Popen('python '+path1+' runserver',stdout=subprocess.PIPE,shell=True,stdin=subprocess.PIPE)
    # stdout_value1 = proc1.communicate()[0]
    # print ('\tstdout:', repr(stdout_value1))

    # proc1 = subprocess.Popen(['python','manage.py','runserver',' 5656'],shell=True,stdout=PIPE,stderr=PIPE)
    #
    # out1,err1 = proc1.communicate()
    #
    # print("Error Value :"+str(err1.rstrip()))

    # output = subprocess.check_output(['python','manage.py','runserver','5656'])
    #
    # print(output)

    #subprocess.call(cmd,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    #cmd = "python manage.py runserver ~/"

    #cmd = "python /home/adityasharma/Desktop/ZZ64Y0/test.py"


    #subprocess.call(['gnome-terminal','-x',cmd])

    print(os.getcwd())

    rtnVal = subprocess.check_call(['gnome-terminal','-x',cmd,str(extractFolderName+"/"),str(NodeClusterManager.portNumber)])

    NodeClusterManager.portNumber += 1

    if rtnVal == 0:
        return False
    else:
        return True



    #Comment to test Gnome Terminal Functionality.
    #######p = subprocess.Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE)

    #dataFile = open("/home/adityasharma/Desktop/ZZ64Y0/manage.py",'r')

    #p = subprocess.Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE,stdin=dataFile)

    #p = subprocess.Popen([dataFile, cmd],stdout=subprocess.PIPE)

    #p =subprocess.call(["python /home/adityasharma/Desktop/ZZ64Y0/manage.py runserver"])

    #os.system("/home/adityasharma/Desktop/ZZ64Y0/manage.py runserver 5656")


    # out,err = p.communicate()
    # print("Return Code:" +str(p.returncode))
    # print("Out.rstrip  value "+str(out.rstrip()))
    # print("Error Value :"+str(err.rstrip()))
    # error = err.rstrip()
    # print(error)
    # if not error:
    #     return False
    # else:
    #     return True


def addToQueue(success, request):
    topic = "Deployment_Manager_Queue"+str((cluster_id))
    params = json.dumps({"topic": topic, "task_id": request['task_id']})
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


nodeObject = NodeClusterManager()
nodeObject.initialize()
# call the Addd to queuees functionality multilpe times.
nodeObject.fetchTasks()












