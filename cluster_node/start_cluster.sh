#!/usr/bin/env bash
if [ ! -d "env" ]; then
    virtualenv -p /usr/bin/python3 env && echo "Env creation succeeded"
    pip install -r requirements.txt && echo "Dependency installation succeeded"
fi
source env/bin/activate
echo "Script starts"

start_system_stat_service() {
    echo "Starting system statistics service"
    python ./cluster/system_statistics.py
}

start_cluster_server() {
echo "Starting cluster server"
python ./manage.py runserver 8000

}

start_system_stat_service &
pid1=$!
start_cluster_server &
pid2=$!

echo $pid1>./.pids
echo $pid2>>./.pids
