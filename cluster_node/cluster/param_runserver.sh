#!/usr/bin/env bash
echo "installer started"  > log
echo $1 >>log
cd $1
source env/bin/activate
echo "In the Installer.sh Shell" >> log
cat run.txt >> log
python `cat run.txt` $2 >> log
echo "installer end" 