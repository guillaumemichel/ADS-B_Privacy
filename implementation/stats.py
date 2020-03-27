from flights import flightsFromFile
from datetime import datetime

allFlights = flightsFromFile('../data/flight_lists/2019-11_2020-02.json')

date0 = datetime.strptime('2019-12-30', '%Y-%m-%d')
date1 = datetime.strptime('2020-01-02', '%Y-%m-%d')
icao = 'ad8471'

l = list()
for f in allFlights.elements:
    if f.icao == icao:# and date0 < datetime.strptime(f.departure.time, '%Y-%m-%d %H:%M:%S') < date1:
        print(f.departure.time)

for e in l:
    print(e)

"""
# Print frequencies of callsigns for icaos that were not observed before 2020-01-01
date = datetime.strptime('2020-01-01', '%Y-%m-%d')

icaos = set()
for f in allFlights.elements:
    icaos.add(f.icao)

for f in allFlights.elements:
    if f.icao in icaos and datetime.strptime(f.departure.time, '%Y-%m-%d %H:%M:%S') < date:
        icaos.remove(f.icao)

d = dict()
for f in allFlights.elements:
    if f.icao in icaos:
        if f.icao not in d:
            d[f.icao] = dict()

        if f.callsign not in d[f.icao]:
            d[f.icao][f.callsign] = 0

        d[f.icao][f.callsign]+=1

for e in d:
    print(e+' ',d[e])
"""

"""
# All flights that icao did not appear before 2020-01-01 
date = datetime.strptime('2020-01-01', '%Y-%m-%d')

icaos = set()
for f in allFlights.elements:
    icaos.add(f.icao)

for f in allFlights.elements:
    if f.icao in icaos and datetime.strptime(f.departure.time, '%Y-%m-%d %H:%M:%S') < date:
        icaos.remove(f.icao)

print(icaos)
"""

"""
# All flights that icao did not appear after 2020-01-01 
date = datetime.strptime('2020-01-01', '%Y-%m-%d')

icaos = set()
for f in allFlights.elements:
    icaos.add(f.icao)

for f in allFlights.elements:
    if f.icao in icaos and datetime.strptime(f.departure.time, '%Y-%m-%d %H:%M:%S') > date:
        icaos.remove(f.icao)

print(icaos)
"""


"""
# For each icao print all callsigns it is associated with and frequencies
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