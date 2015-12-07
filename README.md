#Distributed computing using Raspberry PI

###Mini Heroku on Raspberry PI cluster

https://www.heroku.com/ is a leading application hosting platform. In our CMPE-273 Distributed Systems class, we developed a Raspberry PI cluster with 3 nodes (1 master, 2 workers) and developed functionality similar to heroku.com. 

User can provide git repository url in the system and system can build and deploy python projects. we have implemented support for golang too. (Only build part implemented.)

We took this opportunity to learn distributed system from scratch. We developed our own queue called raspberry queue which is in-memory priority queue. It is the backbone of our application. 

The system has following components:

* queue
* master node server
* build worker
* dyno (cluster) manager
* deployment worker
* system statistics (similar to heartbeat)
* cluster registration script (one time activity during a booted life)

We have uploaded screenshots in screenshots directory. (https://github.com/SJSU-CMPE273-Fall2015/raspberrypi_cluster/tree/master/screenshots)


#####We used following configuration to set up our cluster:

Cluster information

* master node - 192.168.137.4

* cluster node 1 - 192.168.137.3

* cluster node 2 - 192.168.137.2

Website for user login and registration = https://192.168.137.4:8000

Login to Admin Dashboard = https://192.168.137.4:8000/admin

base path = /home/pi/raspberrypi_cluster

##Queue is started to save different tasks with priority , id 
Start the Raspberry queue -
```
path = /home/pi/raspberrypi_cluster/raspberryq
command = ./startq.sh
```


##start the master node server -
```
path = /home/pi/raspberrypi_cluster/master_node/
command = python manage.py
```

##Register cluster with server and send system statistics -
```
path = /home/pi/raspberrypi_cluster/clusternode/cluster
command = ./startup.py
```

##Check the Health of the cluster ---
##Start the dynomanager -
```
path = /home/pi/raspberrypi_cluster/master_node/build_manager
./BuildManager.py
```

##Cluster side configuration 
Register the cluster to master and send system statistics such as CPU usage , network usage , disk Usage 
```
path = /home/pi/raspberrypi_cluster/cluster_node/cluster
./startup.sh
```

##To Build and deploy an application onto the master Node and retrieve application to master node
```
path = /home/pi/raspberrypi_cluster/master_node/build_manager
python BuildWorker.py
```
