from traffic.data import aircraft, opensky, airports
from traffic.core import Traffic
from geopy.distance import geodesic
import pandas as pd
import math
import requests

import json

# update aircraft db
#aircraft.download_opensky()

logLvl = 2
align = 2
time_delta = 600 # min

filename = 'usAirports.json'
country = 'United States'

class Position:
    def __init__(self, altitude, latitude, longitude):
        self.altitude = altitude
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return "Alt: "+str(self.altitude)+", Lat: "+str(self.latitude)+", Lon: "+str(self.longitude)

    def to_json(self, shift=0):
        string = align*shift*' ' + '{\n'
        string += align*(shift+1)*' ' + '"altitude"  : "'+str(self.altitude)  +'",\n'
        string += align*(shift+1)*' ' + '"latitude"  : "'+str(self.latitude)  +'",\n'
        string += align*(shift+1)*' ' + '"longitude" : "'+str(self.longitude) +'"\n'
        string += align*shift*' ' + '}'

        return string

class TakeoffLanding:
    def __init__(self, airport=None, time=None, airport_position=None, aircraft_position=None):
        self.airport = airport
        self.time = time
        self.airport_position = airport_position
        self.aircraft_position = aircraft_position
        if aircraft_position != None and airport_position != None:
            self.h_dist = geodesic((airport_position.latitude, airport_position.longitude),
                (aircraft_position.latitude, aircraft_position.longitude)).m
            self.v_dist = aircraft_position.altitude - airport_position.altitude
        else:
            self.h_dist = None
            self.v_dist = None

    def __str__(self):
        string  = "Airport:   "+str(self.airport)+"\n"
        string += "Time:      "+str(self.time)+"\n"
        string += "Aircraft - "+str(self.aircraft_position)+"\n"
        string += "Airport  - "+str(self.airport_position)+"\n"
        string += "Horizontal distance: "+str(self.h_dist)+" m, vertical distance: "+str(self.v_dist)+" m"
        return string

    def to_json(self, shift=0):
        string = align*shift*' ' + '{\n'
        string += align*(shift+1)*' ' + '"airport"             : "' + str(self.airport) +'",\n'
        string += align*(shift+1)*' ' + '"time"                : "' + str(self.time)    +'",\n'

        if self.airport_position is None:
            string += align*(shift+1)*' ' + '"airport_position"    : "None",\n'
        else:
            string += align*(shift+1)*' ' + '"airport_position"    : \n'
            string += self.airport_position.to_json(shift+1)+',\n'

        if self.aircraft_position is None:
            string += align*(shift+1)*' ' + '"aircraft_position"   : "None",\n'
        else:
            string += align*(shift+1)*' ' + '"aircraft_position"   : \n'
            string += self.aircraft_position.to_json(shift+1)+',\n'

        string += align*(shift+1)*' ' + '"horizontal_distance" : "' + str(self.h_dist)  +'",\n'
        string += align*(shift+1)*' ' + '"vertical_distance"   : "' + str(self.v_dist)  +'"\n'
        string += align*shift*' ' + '}'

        return string


class MyFlight:
    def __init__(self, callsign=None, icao=None, nnumber=None, departure=None, arrival=None):
        self.callsign = callsign
        self.icao = icao
        self.nnumber = nnumber
        self.departure = departure
        self.arrival = arrival

    def __str__(self):
        string  = "Flight:\n"
        string += "  Icao:  "+str(self.icao)+"\n"
        string += "  Callsign:  "+str(self.callsign)+"\n"
        string += "  N-Number:  "+str(self.nnumber)+"\n"
        string += "  Departure -\n"+str(self.departure)+"\n"
        string += "  Arrival -\n"+str(self.arrival)+"\n"
        return string

    def to_json(self, shift=0):
        string = align*shift*' ' + '{\n'
        string += align*(shift+1)*' ' + '"icao"      : "'+str(self.icao)     +'",\n'
        string += align*(shift+1)*' ' + '"callsign"  : "'+str(self.callsign) +'",\n'
        string += align*(shift+1)*' ' + '"nnumber"   : "'+str(self.nnumber)  +'",\n'
        string += align*(shift+1)*' ' + '"departure" :\n'
        string += str(self.departure.to_json(shift+1)) + ',\n'
        string += align*(shift+1)*' ' + '"arrival"   :\n'
        string += str(self.arrival.to_json(shift+1)) + '\n'
        string += align*shift*' ' + '}'

        return string

class Flights:
    def __init__(self):
        self.empty()

    def __str__(self):
        string = ""
        for e in self.elements:
            string += str(e) + "\n"
        return string

    def append(self, flight):
        self.elements.append(flight)

    def remove(self, flight):
        self.elements.remove(flight)

    def empty(self):
        self.elements = list()

    def to_json(self, shift=0):
        json_string = '[\n'

        for e in self.elements:
            json_string += e.to_json(shift+1)+',\n'

        json_string = json_string[:-2]+'\n]'
        return json_string

    def to_file(self, filename):
        file  = open(filename, "w")
        file.write(self.to_json())
        file.close()

    def from_file(self, filename):
        file = open(filename, "r")
        string = file.read()
        file.close()

        json_data = json.loads(string)
        self.elements = list()

        for d in json_data:

            dep = d['departure']
            dep_ap_pos = dep['airport_position']
            if dep_ap_pos != 'None':
                dep_ap_pos = Position(float(dep_ap_pos['altitude']), float(dep_ap_pos['latitude']), float(dep_ap_pos['longitude']))
            else:
                dep_ap_pos = None

            dep_ac_pos = dep['aircraft_position']
            if dep_ac_pos != 'None':
                dep_ac_pos = Position(float(dep_ac_pos['altitude']), float(dep_ac_pos['latitude']), float(dep_ac_pos['longitude']))
            else:
                dep_ac_pos = None
            
            departure = TakeoffLanding(airport=dep['airport'],time=dep['time'],airport_position=dep_ap_pos, aircraft_position=dep_ac_pos)

            arr = d['arrival']
            arr_ap_pos = arr['airport_position']
            if arr_ap_pos != 'None':
                arr_ap_pos = Position(float(arr_ap_pos['altitude']), float(arr_ap_pos['latitude']), float(arr_ap_pos['longitude']))
            else:
                arr_ap_pos = None

            arr_ac_pos = arr['aircraft_position']
            if arr_ac_pos != 'None':
                arr_ac_pos = Position(float(arr_ac_pos['altitude']), float(arr_ac_pos['latitude']), float(arr_ac_pos['longitude']))
            else:
                arr_ac_pos = None
            
            arrival = TakeoffLanding(airport=arr['airport'],time=arr['time'],airport_position=arr_ap_pos, aircraft_position=arr_ac_pos)

            f = MyFlight(callsign=d['callsign'],icao=d['icao'],nnumber=d['nnumber'],departure=departure, arrival=arrival)
            self.append(f)
        
        return str(self)

def getAirportPosition(airports, icao):
    a = airports[icao]
    if a is None:
        return None
    lat, lon = a.latlon
    alt = a.altitude
    return Position(altitude=alt, latitude=lat, longitude=lon)

def getAicraftPosition(flight, prop):
    """
    prop is 0 or 1, for departure and arrival position
    """
    step = 0.001
    inc = (prop == 0)
    while math.isnan(flight.at_ratio(prop).latitude) and ((inc and prop<1) or ((not inc) and prop>0)):
        if inc:
            prop += step
        else:
            prop -= step

    if (inc and prop==1) or ((not inc) and prop==0):
        return None

    f = flight.at_ratio(prop)
    lat, lon = f.latlon
    alt = f.altitude

    return Position(alt, lat, lon)

def getFlightAirports(airportsList, flight, row):

    if row['estDepartureAirport'] is None:
        dep_ap_pos = None
    else:
        dep_ap_pos = getAirportPosition(airportsList, row['estDepartureAirport'])
    dep_ac_pos = getAicraftPosition(flight, 0)
    if dep_ac_pos != None:
        dep = TakeoffLanding(airport=row['estDepartureAirport'], time=row['firstSeen'], airport_position=dep_ap_pos, aircraft_position=dep_ac_pos)
    else:
        dep = TakeoffLanding(airport=row['estDepartureAirport'], time=row['firstSeen'], airport_position=dep_ap_pos, aircraft_position=None)

    if row['estArrivalAirport'] is None:
        arr_ap_pos = None
    else:
        arr_ap_pos = getAirportPosition(airportsList, row['estArrivalAirport'])
    arr_ac_pos = getAicraftPosition(flight, 1)
    if arr_ac_pos != None:
        arr = TakeoffLanding(airport=row['estArrivalAirport'], time=row['lastSeen'], airport_position=arr_ap_pos, aircraft_position=arr_ac_pos)
    else:
        arr = TakeoffLanding(airport=row['estArrivalAirport'], time=row['lastSeen'], airport_position=arr_ap_pos, aircraft_position=None)

    return dep, arr

def getUSAirports():
    usAirports = airports.search(country)
    usAirports.to_json(filename)
    return usAirports

def parseAirportsICAO():
    f = open(filename,'r')
    txt = f.read()
    f.close()

    txt = txt[txt.find('icao'):]
    txt = txt[txt.find('{'):]

    icaos = list()

    while True:
    #for i in range(10):
        start = txt.find(':"')
        if txt.find('}') < start:
            break
        txt = txt[start+2:]
        end = txt.find('"')
        icaos.append(txt[:end])
        txt = txt[end:]

    return icaos    

def getFlightsFilename(start_day, end_day):
    return start_day + "_" + end_day + "_DCM_recordings.parquet"

def loadFlights(start_day, end_day):
    filename = getFlightsFilename(start_day, end_day)
    flights = Traffic.from_file(filename)

    if logLvl >= 1:
        print("Loaded "+str(len(flights))+" flights")

    return flights

def query(start_day, end_day, icao, callsign):
    t_dcm = opensky.history(
        start_day+" 00:00",
        end_day+" 23:59",
        callsign=callsign,
        icao24=icao
    )
    return t_dcm

#print(aircraft["a1c6ba"])



start = "2019-11-01"
end = "2019-11-30"

count = 0

usAirports = getUSAirports()

flights = loadFlights(start, end)
icaos = set()
for f in flights:
    icaos.add(f.icao24)
total = len(icaos)
print("Found "+str(total)+" distinct icaos")

record = open('data/record.txt', 'r')
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


    #aicrafts = opensky.api_aircraft(icao24=icao, begin=start+' 00:00', end=end+' 23:59')
    #aicrafts = opensky.api_aircraft(icao24=icao, begin="2020-01-02"+' 00:00', end=end+' 23:59')

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

    myFlights.to_file('data/'+icao+'.json')
    record = open('data/record.txt', 'a')
    record.write(icao+'\n')
    record.close()
    print('Done '+str(count)+'/'+str(total))



## WRITE IN FILE CONTINUOUSLY
## PRINT PERCENTAGE !!!!!!!!!!!!!
#newFlights = Flights()
#print(newFlights.from_file('a1c6ba.json'))