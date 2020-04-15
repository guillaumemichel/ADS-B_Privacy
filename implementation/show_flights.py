from flights import flightsFromFile
import sys

"""
Show flights that include a given N-Number, ICAO or Callsign
"""

if __name__ == "__main__":
    allFlights = flightsFromFile('../data/flight_lists/2019-11_2020-03.json')

    if len(sys.argv)-1 != 1:
        sys.exit()

    for f in allFlights.elements:
        if sys.argv[1] in [f.callsign, f.icao, f.nnumber]:
            print(f)
