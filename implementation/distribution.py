from flights import flightsFromFile
from datetime import datetime
from geopy.distance import geodesic
from math import sqrt

allFlights = flightsFromFile('../data/flight_lists/2019-09_2020-03.json')

time_format = '%Y-%m-%d %H:%M:%S'

def avg(elements):
    if len(elements)==0:
        return None
    return sum(elements)/len(elements)

def stddev(elements):
    if len(elements)==0:
        return None
    a = avg(elements)
    s=0
    for e in elements:
        s += (e-a)**2
    return sqrt(s/len(elements))

def date(string):
    return datetime.strptime(string, time_format)

def getUSAirportsICAOs():
    f=open('../data/usAirportsICAOs.json', 'r')
    string=f.read()
    f.close()
    icaos=string.split('\n')[:-1]
    return icaos    


def flightDistance(f):
    if f.departure.airport is None or f.arrival.airport is None:
        return None
    if f.departure.airport_position is None or f.arrival.airport_position is None:
        #print(f.departure.airport, f.arrival.airport)
        return None
    
    return round(geodesic((f.departure.airport_position.latitude, f.departure.airport_position.longitude),\
        (f.arrival.airport_position.latitude, f.arrival.airport_position.longitude)).km,0)

def getAircraftByIcao():
    by_aircraft = dict()
    for f in allFlights.elements:
        if f.departure.time<fromDate or f.arrival.time>untilDate:
            continue

        if f.icao not in by_aircraft:
            by_aircraft[f.icao]=(list(),list()) # correct, hidden

        if f.departure.airport == 'None' or f.arrival.airport is 'None':
            by_aircraft[f.icao][1].append(f)
        else:
            by_aircraft[f.icao][0].append(f)
    return by_aircraft

def checkCallsignUseThreshold(entry):
    count=0
    for i in range(2):
        for f in entry[i]:
            for cs in callsigns:
                if cs in f.callsign:
                    count+=1
    return count>=minDCMFFLthreshold

def filterAircraft(by_aircraft):
    tot=0
    over80=0
    new_aircraft=dict()
    for i in by_aircraft:
        if not checkCallsignUseThreshold(by_aircraft[i]):
            continue

        v = 100*len(by_aircraft[i][0])/(len(by_aircraft[i][0])+len(by_aircraft[i][1]))
        if v >= accurateFlightPercentagePerAircraft:
            over80+=1
        tot+=v
        new_aircraft[i]=by_aircraft[i][0]
        new_aircraft[i].extend(by_aircraft[i][1])
        #print(i+" "+str(v)+"%")

    avg=tot/len(new_aircraft)
    #print("Average:",avg)
    print("Over "+str(accurateFlightPercentagePerAircraft)+"%:", over80)
    return new_aircraft

def filterFlights(flights):
    return [f for f in flights if f.departure.airport is not None and \
        f.departure.airport in usAirportsICAOs and \
        f.arrival.airport is not None and f.arrival.airport in usAirportsICAOs]

def airportsPerAircraft(flights):
    airports=dict()
    for f in flights:
        if f.departure.airport not in airports:
            airports[f.departure.airport]=0
        if f.arrival.airport not in airports:
            airports[f.arrival.airport]=0

        airports[f.departure.airport]+=1
        airports[f.arrival.airport]+=1
    
    for a in airports:
        if a is None:
            continue
        print(a, airports[a])



# only aircraft which n% of their flight have both departure and arrival airports
# are taken into account
accurateFlightPercentagePerAircraft = 85

# minimal number of DCM or FFL callsigns that an aircraft should use to be valid
minDCMFFLthreshold = 2

# valid callsigns
callsigns = ['DCM', 'FFL']

# only take account of flight in the given time period
fromDate="2000-01-01 00:00:00"
untilDate="2020-01-01 00:00:00"

usAirportsICAOs = getUSAirportsICAOs()

if __name__ == "__main__":  
    fromDate=date(fromDate)
    untilDate=date(untilDate)

    our_aircraft=filterAircraft(getAircraftByIcao())

    for ac in our_aircraft:
        print(ac)
        flights = filterFlights(our_aircraft[ac])
        airportsPerAircraft(flights)
        if len(flights)==0:
            continue
        distances = list()
        shortFlights=0
        for f in flights:
            d = flightDistance(f)
            if d is not None:
                distances.append(d)
                if d<200:
                    shortFlights+=1
        
        print('Elements:', len(distances))
        print(distances)
        print('Average:', avg(distances))
        print('Standard Deviation:', stddev(distances))
        print('Short Flights:', shortFlights)
        
        print()
