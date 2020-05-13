from flights import flightsFromFile
from datetime import datetime

if __name__ == "__main__":
    allFlights = flightsFromFile('../data/flight_lists/2019-06_2020-04.json')

    date = datetime.strptime('2020-01-01', '%Y-%m-%d')

    icaos=dict()
    for f in allFlights.elements:
        if f.departure.time > date:
            continue

        if f.icao not in icaos:
            icaos[f.icao]=[0, f.departure.time, f.departure.time]
        
        icaos[f.icao][0]+=1
        if f.departure.time < icaos[f.icao][1]:
            icaos[f.icao][1]=f.departure.time
        if f.departure.time > icaos[f.icao][2]:
            icaos[f.icao][2]=f.departure.time

    valid=list()
    for icao in icaos:
        if icaos[icao][1]<datetime.strptime('2019-08-01', '%Y-%m-%d') and \
            icaos[icao][2]>datetime.strptime('2019-11-01', '%Y-%m-%d'):

            l = (icaos[icao][2]-icaos[icao][1]).days
            #print(l)
            valid.append(icaos[icao][0]/l)

    print(sum(valid)/len(valid))
