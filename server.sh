#!/bin/bash

if [ "$EUID" -ne 0 ]
then echo "Please run as root"
        exit
fi

cd server/PyPokerBotAPI
python ./server.py


