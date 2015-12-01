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
#base_path = "/home/adityasharma/Desktop/"


script_path = os.getcwd()

from django.http import HttpResponse


config = configparser.ConfigParser()
config.read('config.txt')
master_ip = config['CONFIGURATION']['master_ip']
cluster_id = config['CONFIGURATION']['cluster_id']
rq_id = config['CONFIGURATION']['rq_id']
num_clusters = config['CONFIGURATION']['number_of_clusters']

path = "/home/adityasharma/Desktop/py_MIUT5A.tar.gz"

serverName = master_ip

#path = config['CONFIGURATION']['DESKTOP_PATH']+"/"+""

#outpath = "/home/adityasharma/Desktop/"

outpath = config['CONFIGURATION']['deployment_path']
base_path = config['CONFIGURATION']['deployment_path']

extractFolderName = ""
portNumberURL = ""




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
                    post_data = json.dumps({'cluster_id' : cluster_id,'project_id' : task['project_id'],'url':portNumberURL})
                    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                    conn = http.client.HTTPConnection(master_ip)
                    conn.request("POST", "/deployment_manager/reportStatus", post_data, headers)
                    response = conn.getresponse()
                    print(response.status,response.reason)
                    data = response.read
                    print(data)
                    conn.close()

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

def copyToRemote(fileName,user,serverName,destinationPath):

    print("Inside the SCP Functionality")

    print("Filename "+fileName)
    print("ServerName "+serverName)
    print("Destination Path"+destinationPath)

    os.system("scp "+fileName+" "+user+"@"+serverName+":"+destinationPath)
    # e.g. os.system("scp foo.bar joe@srvr.net:/path/to/foo.bar")
    #To be followed : You need to generate (on the source machine)
    # and install (on the destination machine) an ssh key beforehand so that the
    # scp automatically gets authenticated with your public ssh key
    # (in other words, so your script doesn't ask for a password)
    pass

def deployProject(task):
    print("DEPLOYING PROJECT#", task['project_id'])

    fullFilePath = task['build_location']

    p = fullFilePath.split('/')

    fileName = p[len(p) - 1].split('.')[0].split('_')[1]

    global extractFolderName

    #extractFolderName = outpath + p[len(p) - 1].split('.')[0].split('_')[1]

    extractFolderName = outpath + fileName

    print("File has been extracetd at the location "+extractFolderName)

    copyToRemote(fileName,'pi',serverName, outpath)

    #fh = open(path)

    #p = path.split('/')

    # global extractFolderName
    # extractFolderName = outpath + p[len(p) - 1].split('.')[0].split('_')[1]
    #
    # print("File has been extracetd at the location "+extractFolderName)

    tarExt = tarfile.open(extractFolderName+".tar.gz")

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

    print("Current working directory is "+os.getcwd())

    global portNumberURL
    portNumberURL = "127.0.0.1:"+str(NodeClusterManager.portNumber)

    rtnVal = subprocess.check_call(['gnome-terminal','-x',cmd,str(extractFolderName+"/"),str(NodeClusterManager.portNumber)])

    NodeClusterManager.portNumber += 1

    if rtnVal == 0:
        return False
    else:
        return True


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












