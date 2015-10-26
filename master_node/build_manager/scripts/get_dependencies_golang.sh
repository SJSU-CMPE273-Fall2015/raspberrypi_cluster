#!/usr/bin/env bash
export PATH=$PATH:/usr/local/go/bin
BaseDir='/home/saurabh/Desktop/'
cd $BaseDir$1
export GOPATH=$BaseDir$1
echo $GOPATH
for i in `cat godep.packages`
do
echo $i
go get $i
done

# Presently building only main package
go build main
go install main

# Remove git repository
rm -rf .git
for i in `cat .slugignore`
do
echo $i
rm -rf $i
done