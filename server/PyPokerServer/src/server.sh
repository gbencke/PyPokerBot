#!/bin/sh

cd /home/gbencke/git/2017.03.14.PyPokerBot/server/PyPokerServer/src 
export LD_LIBRARY_PATH=/home/gbencke/git/pbots_calc/export/linux2/lib:$LD_LIBRARY_PATH
export FLASK_APP=server.py
export FLASK_DEBUG=1
flask run --host=0.0.0.0


