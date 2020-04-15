#!/bin/bash

# Loop over the get_flights_information.py script as
# it keeps crashing because of networks issues

for (( ; ; ))
do
    /home/guissou/.miniconda3/bin/python /mnt/SHARED/Documents/eth/project/implementation/get_flights_information.py
    echo 'starting again'
done

