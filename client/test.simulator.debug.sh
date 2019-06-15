#!/bin/bash

source ../env.simulator/bin/activate
cd src
python3 -m pudb ./PyPokerBot.py simulator ../test/tables POKERSTARS 6-SEATS

