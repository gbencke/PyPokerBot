#!/bin/bash

if [ "$EUID" -ne 0 ]
then echo "Please run as root"
        exit
fi

cd src
export FLASK_APP=server.py
export FLASK_DEBUG=1
flask run --host=0.0.0.0


