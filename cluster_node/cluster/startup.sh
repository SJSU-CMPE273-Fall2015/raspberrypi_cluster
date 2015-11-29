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

register_cluster
pid1=$!
start_system_statistics
pid2=$!


