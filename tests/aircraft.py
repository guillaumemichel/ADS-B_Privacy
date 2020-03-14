from traffic.data import aircraft, opensky
from traffic.core import Traffic

aircraft.download_opensky()

logLvl = 2

def getFlightsFilename(start_day, end_day):
    return start_day + "_" + end_day + "_DCM_recordings.parquet"

def loadFlights(start_day, end_day):
    filename = getFlightsFilename(start_day, end_day)
    flights = Traffic.from_file(filename)

    if logLvl >= 1:
        print("Loaded "+str(len(flights))+" flights")

    return flights


print(aircraft["a1c6ba"])

start = "2020-02-01"
end = "2020-02-29"

#flights = loadFlights(start, end)
#f = flights["DCM2234"]
print(opensky.api_aircraft(icao24="a1c6ba", begin="2020-02-01 00:00", end="2020-02-29 23:59"))



