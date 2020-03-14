import warnings
import math
import pandas as pd
import json

from geopy.distance import geodesic

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    from traffic.data import opensky, airports
    from traffic.core import Traffic, Flight

airportsFilename = 'usAirports.json'
country = 'United States'
nClosestAirports = 10
timeDelta = 30
largeDistance = 100000
logLvl = 3

class MyFlight:
    
    def __init__(self, callsign=None, icao=None, departure=None,
            arrival=None, start=None, end=None):
        self.callsign = callsign
        self.icao = icao
        self.departure = departure
        self.arrival = arrival
        self.start = start
        self.end = end

    def __str__(self):
        string =  "Flight:" + \
                "\n  Callsign:  " + str(self.callsign) + \
                "\n  Icao:      " + str(self.icao) + \
                "\n  Departure: " + str(self.departure) + \
                "\n  Arrival:   " + str(self.arrival) + \
                "\n  Start:     " + str(self.start) + \
                "\n  End:       " + str(self.end)
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

    def to_json(self):
        json_string = '[\n'

        for e in self.elements:
            json_string += '  {\n'
            json_string += '    "callsign"  : "'+str(e.callsign)+'",\n'
            json_string += '    "icao"      : "'+str(e.icao)+'",\n'
            json_string += '    "departure" : "'+str(e.departure)+'",\n'
            json_string += '    "arrival"   : "'+str(e.arrival)+'",\n'
            json_string += '    "start"     : "'+str(e.start)+'",\n'
            json_string += '    "end"       : "'+str(e.end)+'"\n'
            json_string += '  },\n'

        json_string = json_string[:-2]+'\n]\n'
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
            f = MyFlight(d['callsign'], d['icao'], d['departure'],
                d['arrival'], d['start'], d['end'])
            self.append(f)
        
        return str(self)

def getUSAirports():
    if logLvl >= 1:
        print("Getting US Airports from remote database")
    usAirports = airports.search(country)
    usAirports.to_json(airportsFilename)

    if logLvl >= 1:
        print("Found "+str(len(usAirports))+" US Airports")

    return usAirports

def parseAirportsICAO():
    if logLvl >= 2:
        print("Parsing Aiports ICAOS from json file")

    f = open(airportsFilename,'r')
    txt = f.read()
    f.close()

    txt = txt[txt.find('icao'):]
    txt = txt[txt.find('{'):]

    icaos = list()

    while True:
    #for i in range(20):
        start = txt.find(':"')
        if txt.find('}') < start:
            break
        txt = txt[start+2:]
        end = txt.find('"')
        icaos.append(txt[:end])
        txt = txt[end:]

    if logLvl >= 2:
        print("Parsed "+str(len(icaos))+" Aiports ICAOS")

    return icaos

def computeDist(aircraft, airport):
    return geodesic(aircraft.latlon, (airport.latitude, airport.longitude)).km

def findClosestAirportsCandidates(aircrafts, airports, icaos, departure=True, arrival=False):
    # at least one of departure and arrival should be true
    if not departure and not arrival:
        return None

    if logLvl >= 1:
        if departure and arrival:
            word = "departure and arrival"
        elif departure:
            word = "departure"
        else:
            word = "arrival"
        print("Starting to find closest airports for "+word+" for "+
            str(len(aircrafts))+" flights")

    closests = list()
    positions = list()
    minDists = list()

    # create the list of # closest airports to each flight start/end position (closests)
    # compute the start/end position according to the flags
    # minDists is minimal distance for each departure/arrival to be included in the top #
    # when both departure and arrival are true, the location of items in closests/positions
    # is [dep0,arr0,dep1,arr1, etc.]
    for i in aircrafts:
        if departure:
            closests.append(list())
            minDists.append(largeDistance)
            ratio = 0
            position = i.at_ratio(ratio)
            # find the first moment where latitude is non null
            while math.isnan(position.latitude) and ratio < 1:
                position = i.at_ratio(ratio)
                ratio += 0.001
            if ratio >= 1:
                positions.append(None)
            else:
                positions.append(position)
        if arrival:
            closests.append(list())
            minDists.append(largeDistance)
            ratio = 1
            position = i.at_ratio(ratio)
            # find the last moment where latitude is non null
            while math.isnan(position.latitude) and ratio > 0:
                position = i.at_ratio(ratio)
                ratio -= 0.001
            if ratio <= 0:
                positions.append(None)
            else:
                positions.append(position)

    if logLvl >= 2:
        print("Lists initialized, starting to iterate over all "+str(len(icaos))+" airports")

    i=0
    p=0
    for icao in icaos:
        airport = airports[icao]
        if airport is not None:
            for i in range(len(positions)):
                if positions[i] is None or math.isnan(positions[i].latlon[0]):
                    continue

                dist = computeDist(positions[i], airports[icao])

                if dist < minDists[i]:
                    closests[i].append((icao, dist))
                    if len(closests[i])>nClosestAirports:
                        # remove the furthest airport
                        furthest = ("None", 0)
                        for a in closests[i]:
                            if furthest == None or a[1] > furthest[1]:
                                furthest = a
                        closests[i].remove(furthest)

                        # define new max distance for aiport to be added to the list
                        furthest = ("None", 0)
                        for a in closests[i]:
                            if furthest == None or a[1] > furthest[1]:
                                furthest = a
                        minDists[i] = furthest[1]

        if i%(len(icaos)/100)==0:
            print(str(p)+"%")
            p+=1
        i+=1

    
    if logLvl >= 1:
        print("Found closest airports")

    for c in closests:
        c.sort(key=lambda tup: tup[1])

    return closests

def getClosestAirport(aircraft, airports, icaos, departure=True):
    """
    Returns the #nClosestAirports (10 by default) closest airports to the first
    location of the aircraft.
    Output format:
      (Airport, distance)
      ("LSZH", 10.5km)
    """

    if departure:
        # get the first position with non null latlon
        ratio = 0
        position = aircraft.at_ratio(ratio)
        while math.isnan(position.latitude) and ratio < 1:
            ratio += 0.001
            position = aircraft.at_ratio(ratio)
    else:
        ratio = 1
        position = aircraft.at_ratio(ratio)
        while math.isnan(position.latitude) and ratio > 0:
            ratio -= 0.001
            position = aircraft.at_ratio(ratio)

    # itearate over all airports to get the closer airports
    closest = list()
    minDist = 100000
    for icao in icaos:
        airport = airports[icao]
        if airport is not None:
            dist = computeDist(position, airports[icao])

            if dist < minDist:
                closest.append((icao, dist))
                if len(closest)>nClosestAirports:
                    # remove the furthest airport
                    furthest = ("None", 0)
                    for a in closest:
                        if furthest == None or a[1] > furthest[1]:
                            furthest = a
                    closest.remove(furthest)

                    # define new max distance for aiport to be added to the list
                    furthest = ("None", 0)
                    for a in closest:
                        if furthest == None or a[1] > furthest[1]:
                            furthest = a
                    minDist = furthest[1]

    closest.sort(key=lambda tup: tup[1])
    return closest

def getExactAirport(flight, closestAirports, departure=True):

    if departure:
        time=flight.start
    else:
        time=flight.stop
    
    earlier = time + pd.Timedelta(minutes=-timeDelta)
    later = time + pd.Timedelta(minutes=timeDelta)

    for a in closestAirports:
        try:
            if departure:
                schedule = opensky.api_departure(a[0], earlier, later)
            else:
                schedule = opensky.api_arrival(a[0], earlier, later)
            for _, row in schedule.iterrows():
                if flight.callsign in row['callsign']:
                    if departure:
                        return a, row['estArrivalAirport'], row['firstSeen']
                    else:
                        return a, row['lastSeen'], _
        except:
            continue
    
    print("Couldn't get the closest airport for flight")
    print(flight)
    return (None, None), None, None

def getDestinations(flights, airports, icaos, pot_dests):
    destinations = list()
    last_seens = list()

    if logLvl >= 1:
        print("Getting arrival airports")

    # speculate on the destination found at departure airport
    # either find arrival airport or input None in list
    for flight in flights:
        time = flight.stop
        earlier = time + pd.Timedelta(minutes=-timeDelta)
        later = time + pd.Timedelta(minutes=timeDelta)

        if dest is not None:
            done = False
            arrivals = opensky.api_arrival(dest, earlier, later)
            for _, row in arrivals.iterrows():
                if flight.callsign in row['callsign']:
                    dist = computeDist(flight.at_ratio(1), airports[dest])
                    destinations.append((dest, dist))
                    last_seens.append(row['lastSeen'])
                    done = True
                    break
            if not done:
                destinations.append(None)
                last_seens.append(None)

    # find missing destinations and create a list with missing destinations
    to_complete = list()
    indices = list()
    for i in range(len(destinations)):
        if destinations[i]==None:
            to_complete.append(flights[i])
            indices.append(i)

    if logLvl >= 2:
        print("Destination for "+str(len(to_complete))+" flights was not found at "+
            "departure airport. Starting lookup")

    closests = findClosestAirportsCandidates(to_complete, usAirports, icaos, departure=False, arrival=True)
    for i in range(len(closests)):
        (airport, distance), last_seen, _ = getExactAirport(to_complete[i],closests[i],departure=False)
        destinations[indices[i]] = (airport, distance)
        last_seens[indices[i]] = last_seen
        #destinations[indices[i]], last_seens[indices[i]] = \
        #    getExactAirport(to_complete[i],closests[i],departure=False)
    
    return destinations, last_seens


def getDepartureAirport(flight, closestAirports):
    time = flight.start
    earlier = time + pd.Timedelta(minutes=-timeDelta)
    later = time + pd.Timedelta(minutes=timeDelta)

    for a in closestAirports:
        try:
            departures = opensky.api_departure(a[0], earlier, later)
            for _, row in departures.iterrows():
                if flight.callsign in row['callsign']:
                    return a, row['estArrivalAirport'], row['firstSeen']
        except:
            continue
    
    print("Couldn't get the closest airport")
    return (None, None), None, None

def getArrivalAirport(flight, dest, closestAirports):
    time = flight.stop
    earlier = time + pd.Timedelta(minutes=-timeDelta)
    later = time + pd.Timedelta(minutes=timeDelta)

    if dest is not None:
        arrivals = opensky.api_arrival(dest, earlier, later)
        for _, row in arrivals.iterrows():
            if flight.callsign in row['callsign']:
                dist = computeDist(flight.at_ratio(1), airports[dest])
                return (dest, dist), row['lastSeen']

    for a in closestAirports:
        try:
            departures = opensky.api_departure(a[0], earlier, later)
            for _, row in departures.iterrows():
                if flight.callsign in row['callsign']:
                    return a, row['estArrivalAirport'], row['firstSeen']
        except:
            continue
    
    print("Couldn't get the closest airport for flight")
    print(flight)
    return (None, None), None, None

def getFlightsFilename(start_day, end_day):
    return start_day + "_" + end_day + "_DCM_recordings.parquet"

def queryFlights(start_day, end_day):
    t_dcm = opensky.history(
        start_day+" 00:00",
        end_day+" 23:59",
        callsign="DCM%",
    )
    filename = getFlightsFilename(start_day, end_day)
    t_dcm.to_parquet(filename, allow_truncated_timestamps=True)
    return t_dcm

def loadFlights(start_day, end_day):
    filename = getFlightsFilename(start_day, end_day)
    flights = Traffic.from_file(filename)

    if logLvl >= 1:
        print("Loaded "+str(len(flights))+" flights")

    return flights

def getFlightInformation(airports, icaos, flight):
    callsign = flight.callsign
    icao = flight.icao24

    departure = 'KTEB'
    dep_dist = 2.481448157650562
    start = "2020-02-26 13:38:34"

    dest = 'KBED'

    #closestAirports = getClosestAirport(flight, usAirports, icaos)
    #(departure, dep_dist), dest, start = getDepartureAirport(flights[2], closestAirports)

    print(getArrivalAirport(flight, dest, None))

start = "2020-02-01"
end = "2020-02-29"
manual=False

if __name__ == "__main__":
    flights = loadFlights(start, end)

    if manual:
        usAirports = getUSAirports()
        icaos = parseAirportsICAO()

        arrival=False
        closests = findClosestAirportsCandidates(flights, usAirports, icaos, departure=True, arrival=arrival)
        print(closests)

        # arrival = False
        dep_airports = list()
        dep_time = list()
        pot_dest = list()
        for i in range(len(flights)):
            (airport, dist), dest, time = getExactAirport(flights[i], closests[i], departure=True)
            dep_airports.append(airport)
            dep_time.append(time)
            pot_dest.append(dest)

        arr_airports, arr_time = getDestinations(flights, usAirports, icaos, pot_dest)

        allFlights = Flights()
        for i in range(len(flights)):
            allFlights.append(MyFlight(flights[i].callsign, flights[i].icao24, \
                dep_airports[i], arr_airports[i][0], dep_time[i], arr_time[i]))

        allFlights.to_file("Feb.json")

    else:
        allFlights = Flights()
        for flight in flights:
            allFlights.append(MyFlight(flight.callsign, flight.icao24, \
                flight.origin, flight.destination, flight.start, flight.stop))

        allFlights.to_file("Feb.json")

        

    
"""
    for i in range(len(closests)):
        c = closests[i]
        if arrival and i%2==0:


    
    print(flights[2])
    getFlightInformation(usAirports, icaos, flights[2])

    closestAirports = getClosestAirport(flights[2], usAirports, icaos)
    print(closestAirports)
    (airport, distance), dest, time = getDepartureAirport(flights[2], closestAirports)
    print(airport, distance)
    print(time)
    print(dest)
    """



