from traffic.data import airports
import pandas as pd

filename = 'usAirports.json'
country = 'United States'

def getUSAirports():
    usAirports = airports.search(country)
    usAirports.to_json(filename)
    return usAirports

def parseAirportsICAO():
    f = open(filename,'r')
    txt = f.read()
    f.close()

    txt = txt[txt.find('icao'):]
    txt = txt[txt.find('{'):]

    icaos = list()

    #while True:
    for i in range(10):
        start = txt.find(':"')
        if txt.find('}') < start:
            break
        txt = txt[start+2:]
        end = txt.find('"')
        icaos.append(txt[:end])
        txt = txt[end:]

    return icaos


if __name__ == "__main__":
    usAirports = getUSAirports()
    icaos = parseAirportsICAO()

    print(len(usAirports))
    