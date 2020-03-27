from traffic.data import aircraft, opensky, airports
from traffic.core import Traffic
from utils import *
from flights import Flights, MyFlight

import pandas as pd
import math
import requests

import json

# update aircraft db
#aircraft.download_opensky()

callsigns = ['FFL', 'DCM']
month = 'feb_test'
start = "2020-02-01"
end = "2020-02-29"
output_path = '../data/'+month+'/'


if __name__ == "__main__":
    count = 0

    usAirports = getUSAirports()

    icaos = set()
    for c in callsigns:
        flights = loadFlights(start, end, c)
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
            aicrafts = opensky.api_aircraft(icao24=icao, begin=start+' 00:00', end=end+' 23:59')
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 404:
                print("No result for icao "+icao)
                continue
            else:
                raise

        myFlights = Flights()
        for _, row in aicrafts.iterrows():
            flight = None
            if row['callsign'] is None:
                print('callsign missing for '+row['icao24'])
                continue
            for f in flights:
                # GET CLOSEST FLIGHT TO TIME WITH SAME CALLSIGN AND ICAO
                if f.callsign is None:
                    continue
                #if f.icao24 == row['icao24'] and (row['callsign'] in f.callsign or f.callsign in row['callsign'] or (f.registration is not None and f.registration in row['callsign'])) and (flight is None or abs(row['firstSeen']-f.start)<abs(row['firstSeen']-flight.start)):
                if f.icao24 == row['icao24']:
                    a = row['callsign'] in f.callsign
                    b = f.callsign in row['callsign']
                    c = f.registration is not None and f.registration in row['callsign']
                    if (a or b or c) and (flight is None or abs(row['firstSeen']-f.start)<abs(row['firstSeen']-flight.start)):
                        flight = f
            if flight is None:
                dep, arr = getFlightAirports(None, None, row)
                myFlights.append(MyFlight(row['callsign'].strip(), row['icao24'].strip(), None, dep, arr))
            else:
                dep, arr = getFlightAirports(usAirports, flight, row)
                f2 = MyFlight(row['callsign'].strip(), row['icao24'].strip(), flight.registration, dep, arr)
                #myFlights.append(MyFlight(flight.callsign, flight.icao24, flight.registration, dep, arr))
                myFlights.append(f2)

        myFlights.to_file(output_path+icao+'.json')
        record = open(output_path+'record.txt', 'a')
        record.write(icao+'\n')
        record.close()
        print('Done '+str(count)+'/'+str(total))