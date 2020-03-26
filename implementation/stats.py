from flights import flightsFromFile
from datetime import datetime

allFlights = flightsFromFile('../data/flight_lists/2019-11_2020-02.json')

date = datetime.strptime('2020-01-01', '%Y-%m-%d')

icaos = set()
for f in allFlights.elements:
    icaos.add(f.icao)

for f in allFlights.elements:
    if f.departure.time > date:
        icaos.remove(f.icao)

print(icaos)

"""
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