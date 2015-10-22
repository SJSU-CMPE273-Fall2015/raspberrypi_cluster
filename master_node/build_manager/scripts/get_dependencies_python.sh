#!/usr/bin/env bash
BaseDir='/home/saurabh/Desktop/'
cd $BaseDir$1
virtualenv -p /usr/bin/python3 env
source env/bin/activate
pip install -r requirements.txt
