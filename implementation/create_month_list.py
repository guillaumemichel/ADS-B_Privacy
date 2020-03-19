from flights import Flights

from os import listdir
from os.path import isfile, join

month = 'february'
mypath = '../data/'+month
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

full_list_filename = 'all_flights.json'

allFlights = Flights()
for s in onlyfiles:
    if '.json' in s and full_list_filename not in s:
        newFlights = Flights()
        try:
            newFlights.from_file(mypath+'/'+s)
        except:
            continue
        allFlights.concat(newFlights)

allFlights.to_file(mypath+'/'+full_list_filename)

d = dict()
for f in allFlights.elements:
    if f.icao not in d:
        d[f.icao] = dict()

    if f.callsign not in d[f.icao]:
        d[f.icao][f.callsign] = 0

    d[f.icao][f.callsign]+=1

for e in d:
    print(e+': ',d[e])

print(len(d))

"""
timerange = dict()
for f in allFlights.elements:
    if f.icao not in timerange:
        timerange[f.icao]= (f, f)
    else:
        if f.departure.time < timerange[f.icao][0].departure.time:
            timerange[f.icao] = (f, timerange[f.icao][1])
        if f.arrival.time > timerange[f.icao][1].arrival.time:
            timerange[f.icao] = (timerange[f.icao][0], f)

for e0 in timerange:
    for e1 in timerange:

        if timerange[e0][1].arrival.time < timerange[e1][0].departure.time:
            if timerange[e0][1].arrival.aircraft_position is not None and timerange[e1][0].arrival.aircraft_position is not None:
                dist = timerange[e0][1].arrival.aircraft_position.distance(timerange[e1][0].departure.aircraft_position).km
                if dist < 100:
                    print(dist,'km')
                    print(timerange[e0][1])
                    print(timerange[e1][0])
                    print()
"""