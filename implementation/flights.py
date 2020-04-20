from geopy.distance import geodesic
from datetime import datetime
import json

"""
Implement useful Flight structure that is used in other scripts
"""

align = 2
time_format = '%Y-%m-%d %H:%M:%S'

class Position:
    def __init__(self, altitude, latitude, longitude):
        if altitude == 'None':
            altitude=None
        if latitude == 'None':
            latitude=None
        if longitude == 'None':
            longitude=None

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

    def distance(self, other):
        return geodesic((self.latitude, self.longitude), (other.latitude, other.longitude))

    def equal(self, other):
        return other is not None and \
             self.altitude == other.altitude and \
             self.latitude == other.latitude and \
             self.longitude == other.longitude

class TakeoffLanding:
    def __init__(self, airport=None, time=None, airport_position=None, aircraft_position=None):
        if airport == 'None':
            airport=None
        if time=='None':
            time=None
        if airport_position=='None':
            airport_position=None
        if aircraft_position=='None':
            aircraft_position=None

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
        string += align*(shift+1)*' ' + '"time"                : "' + str(datetime.strftime(self.time, time_format))    +'",\n'

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
    
    def equal(self, other):
        return other is not None and \
            self.airport == other.airport and \
            self.time == other.time

class MyFlight:
    def __init__(self, callsign=None, icao=None, nnumber=None, departure=None, arrival=None):
        if callsign=='None':
            callsign=None
        if icao=='None':
            icao=None
        if nnumber=='None':
            nnumber=None
        if departure=='None':
            departure=None
        if arrival=='None':
            arrival=None

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

    def equal(self, other):
        return other is not None and \
            self.callsign == other.callsign and \
            self.icao == other.icao and \
            self.departure.time == other.departure.time

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

    def concat(self, flights):
        self.elements = self.elements + flights.elements

    def remove(self, flight):
        self.elements.remove(flight)

    def empty(self):
        self.elements = list()

    def to_json(self, shift=0):
        if len(self.elements)==0:
            return '[]'

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
            
            departure = TakeoffLanding(airport=dep['airport'],time=datetime.strptime(dep['time'][:19], time_format),airport_position=dep_ap_pos, aircraft_position=dep_ac_pos)

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
            
            arrival = TakeoffLanding(airport=arr['airport'],time=datetime.strptime(dep['time'][:19], time_format),airport_position=arr_ap_pos, aircraft_position=arr_ac_pos)

            f = MyFlight(callsign=d['callsign'],icao=d['icao'],nnumber=d['nnumber'],departure=departure, arrival=arrival)
            self.append(f)
        
        return str(self)

def flightsFromFile(filename):
    f = Flights()
    f.from_file(filename)
    return f