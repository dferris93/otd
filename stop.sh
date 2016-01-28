#!/bin/bash
PIDFILE="otd.pid"

kill -9 $(cat $PIDFILE)
