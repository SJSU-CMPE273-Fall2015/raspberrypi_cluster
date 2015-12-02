#!/usr/bin/env bash
BaseDir='/home/pi/Desktop/'
cd $BaseDir$1
virtualenv -p /usr/bin/python3 env
source env/bin/activate
pip install -r requirements.txt
rm -rf .git
for i in `cat .slugignore`
do
echo $i
rm -rf $i
done
