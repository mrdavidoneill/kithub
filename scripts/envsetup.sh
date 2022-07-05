#!/bin/sh

if [ -d "env" ] 
then
    echo "Python virtual environment exists." 
else
    python3 --version
    python3 -m pip3 install --user virtualenv
    python3 -m virtualenv env
fi

source env/bin/activate


pip install -r requirements.txt

if [ -d "logs" ] 
then
    echo "Log folder exists." 
else
    mkdir logs
    touch logs/error.log logs/access.log
fi

sudo chmod -R 777 logs