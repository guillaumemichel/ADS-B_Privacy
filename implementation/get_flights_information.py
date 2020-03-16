from traffic.data import aircraft, opensky, airports
from traffic.core import Traffic
from utils import *
from flights import *

import pandas as pd
import math
import requests

import json

# update aircraft db
#aircraft.download_opensky()

month = 'december01-30'
start = "2019-12-01"
end = "2019-12-31"
output_path = '../data/'+month+'/'


if __name__ == "__main__":
    count = 0

    usAirports = getUSAirports()

    flights = loadFlights(start, end)
    icaos = set()
    for f in flights:
        icaos.add(f.icao24)
    total = len(icaos)
    print("Found "+str(total)+" distinct icaos")

    record = open(output_path+'record.txt', 'r')
    done = record.read()
    record.close()

    for icao in icaos:
        count+=1
        if icao in done:
            print(icao+' is already done')
            continue

        try:
            aicrafts = opensky.api_aircraft(icao24=icao, begin=start+' 00:00', end="2019-12-30"+' 23:59')
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 404:
                print("No result for icao "+icao)
                continue
            else:
                raise

        myFlights = Flights()
        for _, row in aicrafts.iterrows():
            flight = None
            for f in flights:
                # GET CLOSEST FLIGHT TO TIME WITH SAME CALLSIGN AND ICAO
                if f.icao24 == row['icao24'] and (row['callsign'] in f.callsign or f.callsign in row['callsign'] or (f.registration is not None and f.registration in row['callsign'])) and (flight is None or abs(row['firstSeen']-f.start)<abs(row['firstSeen']-flight.start)):
                    flight = f
            if flight is None:
                print("Flight not found!")
                print(row)
            else:
                dep, arr = getFlightAirports(usAirports, flight, row)
                myFlights.append(MyFlight(row['callsign'], row['icao24'], flight.registration, dep, arr))

        myFlights.to_file(output_path+icao+'.json')
        record = open(output_path+'record.txt', 'a')
        record.write(icao+'\n')
        record.close()
        print('Done '+str(count)+'/'+str(total))