#!/bin/bash

source ../env.simulator/bin/activate
cd src
python3 ./PyPokerBot.py simulator ../test/tables POKERSTARS 6-SEATS  --print_result True

