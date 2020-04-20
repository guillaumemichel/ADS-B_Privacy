from flights import flightsFromFile
from datetime import datetime
from geopy.distance import geodesic

allFlights = flightsFromFile('../data/flight_lists/2019-11_2020-03.json')

time_format = '%Y-%m-%d %H:%M:%S'

def date(string):
    return datetime.strptime(string, time_format)

def flightDistance(f):
    if f.departure.airport == 'None' or f.departure.airport == 'None':
        return None
    
    return geodesic((f.departure.airport_position.latitude, f.departure.airport_position.longituve),\
        (f.arrival.airport_position.latitide, f.arrival.airport_position.longitude)).km

def getAircraftByIcao():
    by_aircraft = dict()
    for f in allFlights.elements:
        if date(f.departure.time)<fromDate or date(f.arrival.time)>untilDate:
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
        if a == 'None':
            continue
        print(a, airports[a])



# only aircraft which n% of their flight have both departure and arrival airports
# are taken into account
accurateFlightPercentagePerAircraft = 65

# minimal number of DCM or FFL callsigns that an aircraft should use to be valid
minDCMFFLthreshold = 2

# valid callsigns
callsigns = ['DCM', 'FFL']

# only take account of flight in the given time period
fromDate="2000-01-01 00:00:00"
untilDate="2020-01-01 00:00:00"

if __name__ == "__main__":    
    fromDate=date(fromDate)
    untilDate=date(untilDate)

    our_aircraft=filterAircraft(getAircraftByIcao())

    for ac in our_aircraft:
        print(ac)
        airportsPerAircraft(our_aircraft[ac])
        print(flightDistance(our_aircraft[ac][0]))
        print()
