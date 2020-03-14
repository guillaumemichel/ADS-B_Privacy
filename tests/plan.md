# Gathering and storing flight data

```python
# load flights from file
flights = loadFlights(start, end)

# we have callsign and icao
# need departure and arrival airports and timestamps

# get all usa airports along with 
usAirports = getUSAirports()
icaos = parseAirportsICAO()

# iterate on all airports and keep the 10 closers to each flight departure
allPotentialDepartures = getDepartures(flights, usAirports, icaos)
# allPotentialDepartures: [ [(icao, dist),(icao, dist),...(icao, dist)], [(icao, dist)...] ... [...] ]

getDepartureAirport()
# [((icao, dist), dest, timestamp), ((icao, dist), dest, timestamp), ..., ((icao, dist), dest, timestamp)]
# we now have departure airport & timestamp

tryDest()
# [ ((icao, dist), timestamp)/None, ((icao, dist), timestamp)/None, ..., ((icao, dist), timestamp)/None]

# get arrival airport if not found in previous step
getArrivalAirport()

# save all flights to json
to_save = Flights()
for i in range(len(flights)):
    f = MyFlight(...)
    to_save.append(f)

to_save.to_json(filename)
```