#!/bin/bash

cd ~/Desktop/CMPE273/raspberrypi_cluster/raspberryq

gnome-terminal -e "bash -c \"source env/bin/activate env;sh startq.sh exec bash\""

sleep 5 

cd ~/Desktop/CMPE273/raspberrypi_cluster/master_node

gnome-terminal -e "bash -c \"source env/bin/activate env;sh startserver.sh exec bash\""




