#!/usr/bin/env bash
for i in `cat ./.pids`
do
echo "Killing".$i
kill -9 $i
done