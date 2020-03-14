from traffic.data import opensky

callsign = "DCM8346"

KTEB_departures = opensky.api_departure('KTEB', '2020-02-26 13:30', '2020-02-26 13:45')
KBED_arrivals = opensky.api_arrival('KBED', '2020-02-26 13:30', '2020-02-26 14:30')

#for d in KTEB_departures.callsign:

for _, row in KTEB_departures.iterrows():
    if callsign in row['callsign']:
        print(row['estArrivalAirport'])
        print(row['firstSeen'])
    #print(row['callsign'], row['estArrivalAirport'])


