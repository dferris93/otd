#!/bin/bash

#activate the virtualenv
source /home/dferris/otd/bin/activate

PORT=4443
IP=127.0.0.1
PROCESSES=4
BUFFER_SIZE=65536
LOGFILE="otd.log"
PIDFILE="otd.pid"
VIRTUALENV=""

uwsgi --socket $IP:$PORT -w WSGI:app --processes $PROCESSES --buffer-size $BUFFER_SIZE --master --daemonize2 $LOGFILE --pidfile $PIDFILE --virtualenv $VIRTUALENV
