#Distributed computing using Raspberry PI

Cluster information

* master node - 192.168.137.4

* cluster node 1 - 192.168.137.3

* cluster node 2 - 192.168.137.2

Website for user login and registration = https://192.168.137.4:8000

Login to Admin Dashboard = https://192.168.137.4/admin

base path = /home/pi/raspberrypi_cluster

##Queue is started to save different tasks with priority , id 
Start the Raspberry queue -

path = /home/pi/raspberrypi_cluster/raspberryq
command = ./startq.sh

##start the master node server -

path = /home/pi/raspberrypi_cluster/master_node/
command = python manage.py

##Register cluster with server and send system statistics -

path = /home/pi/raspberrypi_cluster/clusternode/cluster
command = ./startup.py

##Check the Health of the cluster ---
##Start the dynomanager -

path = /home/pi/raspberrypi_cluster/master_node/build_manager
./BuildManager.py

##Cluster side configuration 
Register the cluster to master and send system statistics such as CPU usage , network usage , disk Usage 

path = /home/pi/raspberrypi_cluster/cluster_node/cluster
./startup.sh

##To Build and deploy an application onto the master Node and retrieve application to master node

path = /home/pi/raspberrypi_cluster/master_node/build_manager
python BuildWorker.py





