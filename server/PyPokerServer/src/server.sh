#!/bin/sh

export LD_LIBRARY_PATH=/home/gbencke/git/pbots_calc/export/linux2/lib:$LD_LIBRARY_PATH
export FLASK_APP=server.py
export FLASK_DEBUG=1
flask run --host=0.0.0.0


