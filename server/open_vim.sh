#!/bin/sh

export PYTHONPATH='/home/gbencke/git/2017.03.14.PyPokerBot/server/PyPokerServer/lib/python2.7/site-packages'
ctags -R  --languages=python -f  ./tags .
vim

