from traffic.data import airports
from flights import flightsFromFile, Position
from os import listdir
from os.path import isfile, join


months = ['oct02-31', 'november_test', 'december01-30_test', 'dec31-jan01_test', 'january02-31_test', 'feb_test', 'march01-30']

def correct_airports(flights):
    for f in flights:
        pass

for month in months:
    mypath = '../data/'+month+"/"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.split('.')[1]=='json']

    for file in onlyfiles:
        fullpath = mypath+file
        flights = flightsFromFile(fullpath)

        for f in flights.elements:
            if f.departure.airport is not None and f.departure.airport_position is None:
                ap = airports[f.departure.airport]
                if ap is not None:
                    f.departure.airport_position=Position(altitude=ap.altitude,latitude=ap.latitude,longitude=ap.longitude)
                else:
                    print(f.departure.airport)
            if f.arrival.airport is not None and f.arrival.airport_position is None:
                ap = airports[f.arrival.airport]
                if ap is not None:
                    f.arrival.airport_position=Position(altitude=ap.altitude,latitude=ap.latitude,longitude=ap.longitude)
                else:
                    print(f.arrival.airport)
        flights.to_file(fullpath)