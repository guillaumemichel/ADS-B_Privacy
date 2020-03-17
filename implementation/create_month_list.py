from flights import *

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
        d[f.icao] = set()

    d[f.icao].add(f.callsign)

for e in d:
    print(e+': ',d[e])
