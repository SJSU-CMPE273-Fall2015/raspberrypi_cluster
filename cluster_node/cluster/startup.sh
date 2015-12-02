#!/usr/bin/env bash
source ../env/bin/activate
echo "Script starts"


register_cluster() {
    echo "cluster registered"
    python startup.py
}



start_system_statistics() {
    echo "started system statistics"
    python system_statistics.py

}

pwd
#Changes Start Here for starting deployment worker.py in new terminal
gnome-terminal -e "bash -c \"sh startup_deployment.sh exec bash\""



#changes end here

register_cluster
pid1=$!
start_system_statistics
pid2=$!


