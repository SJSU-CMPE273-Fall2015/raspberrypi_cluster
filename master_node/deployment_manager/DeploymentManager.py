__author__ = 'adityasharma'

import paramiko
import os
import plumbum


def copyToRemote():
    #write a script that performs scp copy thing from the local to the master or vice versa.
    ssh = createSSHClient("52.32.143.139", "22", "ubuntu", password)
    scp = SCPClient(ssh.get_transport())

    r = plumbum.machines.RemoteMachine("example.net",
    user="username", keyfile=".ssh/some_key")
    fro = plumbum.local.path("some_file")
    to = r.path("/path/to/destination/")
    plumbum.path.utils.copy(fro, to)

    pass


def getProjectLocation():


    pass

def setProjectLocation():
    pass


def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client




