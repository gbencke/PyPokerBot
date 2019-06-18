#!/bin/bash

source ../env.server/bin/activate
cd PyPokerBotAPI
python3 -m pudb ./server.py

