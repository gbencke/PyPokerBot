#!/bin/bash

source ../env.simulator/bin/activate
cd src
python3 ./PyPokerBot.py simulator ../test/tables POKERSTARS 6-SEATS --observer_url http://poker_app.ddns.net:5000/observe --tableid 1

