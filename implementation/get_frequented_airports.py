from flights import flightsFromFile
from datetime import datetime

icaos = ['a4e931', 'a4e94e', 'a4e954', 'a4e970', 'a4ed4f', 'a4ede7', 'a4f0af', 'a4f0cc', 'a4f131', 'a4f4ad', 'a4f4e3', 'a4f4f6', 'a4f86a', 'a4f8a7', 'a4f8c4', 'a4fe94','a4ff46']

allFlights = flightsFromFile('../data/flight_lists/2019-06_2020-04.json')


airports=set()
for f in allFlights.elements:
    if f.departure.time < datetime.strptime('2020-01-01', '%Y-%m-%d'):
        continue
    if f.icao in icaos and 'FFL' in f.callsign:
        airports.add(f.departure.airport)
        airports.add(f.arrival.airport)

print(airports)
print(len(airports))

