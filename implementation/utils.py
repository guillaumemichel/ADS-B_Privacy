from flights import *
import math
from traffic.core import Traffic
from traffic.data import airports
from datetime import datetime

"""
Couple of useful function about flights, airports, coordinates etc.
"""

time_delta = 600 # min

recordings_folder = '../data/recordings/'
airport_file = '../data/usAirports.json'
country = 'United States'

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
    while ((inc and prop<1) or ((not inc) and prop>0)) and math.isnan(flight.at_ratio(prop).latitude):
        if inc:
            prop += step
        else:
            prop -= step

    if (inc and prop>=1) or ((not inc) and prop<=0):
        return None

    f = flight.at_ratio(prop)
    lat, lon = f.latlon
    alt = f.altitude

    return Position(alt, lat, lon)

def getFlightAirports(airportsList, flight, row):
    dep_time = datetime.strptime(str(row['firstSeen'])[:19], time_format)
    arr_time = datetime.strptime(str(row['lastSeen'])[:19], time_format)

    if airportsList is None and flight is None:
        dep = TakeoffLanding(airport=row['estDepartureAirport'], time=dep_time, airport_position=None, aircraft_position=None)
        arr = TakeoffLanding(airport=row['estArrivalAirport'], time=arr_time, airport_position=None, aircraft_position=None)
        return dep, arr


    if row['estDepartureAirport'] is None:
        dep_ap_pos = None
    else:
        dep_ap_pos = getAirportPosition(airportsList, row['estDepartureAirport'])
    dep_ac_pos = getAicraftPosition(flight, 0)
    if dep_ac_pos != None:
        dep = TakeoffLanding(airport=row['estDepartureAirport'], time=dep_time, airport_position=dep_ap_pos, aircraft_position=dep_ac_pos)
    else:
        dep = TakeoffLanding(airport=row['estDepartureAirport'], time=dep_time, airport_position=dep_ap_pos, aircraft_position=None)

    if row['estArrivalAirport'] is None:
        arr_ap_pos = None
    else:
        arr_ap_pos = getAirportPosition(airportsList, row['estArrivalAirport'])
    arr_ac_pos = getAicraftPosition(flight, 1)
    if arr_ac_pos != None:
        arr = TakeoffLanding(airport=row['estArrivalAirport'], time=arr_time, airport_position=arr_ap_pos, aircraft_position=arr_ac_pos)
    else:
        arr = TakeoffLanding(airport=row['estArrivalAirport'], time=arr_time, airport_position=arr_ap_pos, aircraft_position=None)

    return dep, arr

def getUSAirports():
    usAirports = airports.search(country)
    usAirports.to_json(airport_file)
    return usAirports

def parseAirportsICAO():
    f = open(airport_file, 'r')
    txt = f.read()
    f.close()

    txt = txt[txt.find('icao'):]
    txt = txt[txt.find('{'):]

    icaos = list()

    while True:
        start = txt.find(':"')
        if txt.find('}') < start:
            break
        txt = txt[start+2:]
        end = txt.find('"')
        icaos.append(txt[:end])
        txt = txt[end:]

    return icaos    

def getFlightsFilename(start_day, end_day, callsign):
    return start_day + "_" + end_day + "_"+callsign+"_recordings.parquet"

def loadFlights(start_day, end_day, callsign):
    filename = recordings_folder+getFlightsFilename(start_day, end_day, callsign)
    flights = Traffic.from_file(filename)

    print("Loaded "+str(len(flights))+" flights")

    return flights
