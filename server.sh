#!/bin/bash

if [ "$EUID" -ne 0 ]
then echo "Please run as root"
        exit
fi

export LD_LIBRARY_PATH=/usr/local/lib

cd server/PyPokerBotAPI
export FLASK_APP=server.py
export FLASK_DEBUG=1
flask run --host=0.0.0.0 --port=80


