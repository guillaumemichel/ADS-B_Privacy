#!/bin/bash

for (( ; ; ))
do
    /home/guissou/.miniconda3/bin/python /mnt/SHARED/Documents/eth/project/query_historic_db/collect.py
    echo 'starting again'
done