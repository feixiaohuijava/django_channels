#!/usr/bin/env bash


while :
do
    current_time=`date '+%Y-%m-%d %H:%M:%S'`
    sleep 5
    echo $current_time >> deploy.log
done