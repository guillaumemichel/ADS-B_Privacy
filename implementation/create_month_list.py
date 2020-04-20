from flights import Flights
from datetime import datetime

from os import listdir
from os.path import isfile, join

"""
Create a monthly lists of flights from individual icao recordings
"""

months = ['oct02-31', 'november_test', 'december01-30_test', 'dec31-jan01_test', 'january02-31_test', 'feb_test', 'march01-30']

allFlights = Flights()

for month in months:
    mypath = '../data/'+month
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    for s in onlyfiles:
        newFlights = Flights()
        try:
            newFlights.from_file(mypath+'/'+s)
        except:
            continue
        allFlights.concat(newFlights)

for f in allFlights.elements:
    f.departure.time = f.departure.time
    f.arrival.time = f.arrival.time

monthly_lists = dict()
first_month = datetime.strptime('2030-01-01', '%Y-%m-%d')
last_month = datetime.strptime('2010-01-01', '%Y-%m-%d')
for f in allFlights.elements:
    #time = datetime.strptime(f.departure.time, '%Y-%m-%d %H:%M:%S')
    time = f.departure.time
    m = time.strftime("%Y-%m").lower()

    if time < first_month:
        first_month = time
    if time > last_month:
        last_month = time

    if m not in monthly_lists:
        monthly_lists[m] = Flights()
    
    monthly_lists[m].append(f)

allFlightsFilename = first_month.strftime("%Y-%m") + '_' + last_month.strftime("%Y-%m") + '.json'
allFlights.to_file('../data/flight_lists/'+allFlightsFilename)

for m in monthly_lists:
    monthly_lists[m].to_file('../data/flight_lists/'+m+'.json')

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