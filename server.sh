#!/bin/bash

if [ "$EUID" -ne 0 ]
then echo "Please run as root"
        exit
fi

export LD_LIBRARY_PATH=/usr/local/lib

cd server/PyPokerBotAPI
python ./server.py
