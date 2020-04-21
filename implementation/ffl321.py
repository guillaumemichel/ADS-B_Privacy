from traffic.core import Traffic
from traffic.data import airports, opensky
from flights import MyFlight, Flights, TakeoffLanding, time_format, flightsFromFile
from datetime import datetime
import requests

recording_folder = '../data/recordings/'
months = ['oct2019', 'nov2019', 'dec2019', 'jan2020']
#months = ['dec2019']
files = [recording_folder+'KSDM_'+m+'_recordings.parquet' for m in months]
airport='KSDM'

monthly_flights=10

def load_flights():
    flights=list()
    for file in files:
        flights.extend(Traffic.from_file(file))

    callsigns=dict()
    for flight in flights:
        if flight.callsign not in callsigns:
            callsigns[flight.callsign]=0
        callsigns[flight.callsign]+=1
    print(callsigns)

    filtered=set()
    for c in callsigns:
        if callsigns[c]>monthly_flights:
            filtered.add(c)
    print(filtered)

def callsign_monthly_frequency():
    all_callsigns=set()
    for file in files:
        flights=Traffic.from_file(file)
        callsigns=dict()
        for flight in flights:
            if flight.callsign not in callsigns:
                callsigns[flight.callsign]=0
            callsigns[flight.callsign]+=1
        #print(callsigns)

        filtered=set()
        for c in callsigns:
            if callsigns[c]>monthly_flights:
                filtered.add((c, callsigns[c]))
                all_callsigns.add(c)
        
        print(file[len(recording_folder)+5:len(recording_folder)+12], filtered)
    return all_callsigns

def icaos_monthly_frequency():
    all_icaos=set()
    for file in files:
        flights=Traffic.from_file(file)
        icaos=dict()
        for flight in flights:
            if flight.icao24 not in icaos:
                icaos[flight.icao24]=0
            icaos[flight.icao24]+=1
        #print(icaos)

        filtered=set()
        for c in icaos:
            if icaos[c]>monthly_flights:
                filtered.add((c, icaos[c]))
                all_icaos.add(c)
        
        print(file[len(recording_folder)+5:len(recording_folder)+12], filtered)
    return all_icaos


def query_opensky(callsigns):
    myFlights = Flights()
    for callsign in callsigns:
        start='2020-01-01'
        end  ='2020-01-30'
        try:
            aicrafts = opensky.api_aircraft(icao24=callsign, begin=start+' 00:00', end=end+' 23:59')
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 404:
                print("No result for callsign "+callsign+" in "+str(start)+"-"+str(end))
                continue
            else:
                raise
        for _, row in aicrafts.iterrows():
            dep_time = datetime.strptime(str(row['firstSeen'])[:19], time_format)
            arr_time = datetime.strptime(str(row['lastSeen'])[:19], time_format)

            dep_ap=row['estDepartureAirport']
            if dep_ap is not None:
                dep_ap=dep_ap.strip()
            arr_ap=row['estArrivalAirport']
            if arr_ap is not None:
                arr_ap=arr_ap.strip()
            departure=TakeoffLanding(airport=dep_ap, time=dep_time)
            arrival=TakeoffLanding(airport=arr_ap,time=arr_time)
            f=MyFlight(callsign=row['callsign'].strip(),icao=row['icao24'].strip(), nnumber=row['callsign'].strip(),departure=departure,arrival=arrival)
            myFlights.append(f)

            """
            if row['callsign'] is None:
                print('callsign missing for '+row['icao24'])
                continue
            for f in flights:
                # GET CLOSEST FLIGHT TO TIME WITH SAME CALLSIGN AND ICAO
                if f.callsign is None:
                    continue
                #if f.icao24 == row['icao24'] and (row['callsign'] in f.callsign or f.callsign in row['callsign'] or (f.registration is not None and f.registration in row['callsign'])) and (flight is None or abs(row['firstSeen']-f.start)<abs(row['firstSeen']-flight.start)):
                if f.icao24 == row['icao24']:
                    a = row['callsign'] in f.callsign
                    b = f.callsign in row['callsign']
                    c = f.registration is not None and f.registration in row['callsign']
                    if (a or b or c) and (flight is None or abs(row['firstSeen']-f.start)<abs(row['firstSeen']-flight.start)):
                        flight = f
            if flight is None:
                dep, arr = getFlightAirports(None, None, row)
                myFlights.append(MyFlight(row['callsign'].strip(), row['icao24'].strip(), None, dep, arr))
            else:
                dep, arr = getFlightAirports(usAirports, flight, row)
                f2 = MyFlight(row['callsign'].strip(), row['icao24'].strip(), flight.registration, dep, arr)
                #myFlights.append(MyFlight(flight.callsign, flight.icao24, flight.registration, dep, arr))
                myFlights.append(f2)
            """
    myFlights.to_file('../data/ffl321/jan_flights.json')
    print(myFlights)

def filterFlights(flights):
    new_flights=Flights()
    for f in flights.elements:
        #print(f.departure.airport, f.arrival.airport, f.departure.airport==f.arrival.airport==airport)
        if f.departure.airport==f.arrival.airport==airport:
            new_flights.append(f)
    #print('\n')
    return new_flights

def analyzeFlights(flights):
    analyzed=dict()
    for f in flights.elements:
        if f.icao not in analyzed:
            analyzed[f.icao]=[0, set(), datetime.strptime('2020-02-01','%Y-%m-%d'), datetime.strptime('2019-11-30', '%Y-%m-%d')]
        analyzed[f.icao][0]+=1
        analyzed[f.icao][1].add(f.callsign)
        if f.departure.time < analyzed[f.icao][2]:
            analyzed[f.icao][2]=f.departure.time
        if f.arrival.time > analyzed[f.icao][3]:
            analyzed[f.icao][3]=f.arrival.time
    
    for icao in analyzed:
        print(icao+" : "+str(analyzed[icao][0])+" "+str(analyzed[icao][1])+str(analyzed[icao][2])+" "+str(analyzed[icao][3]))

if __name__ == '__main__':
    #print(icaos_monthly_frequency())
    #frequent_callsigns={'N961CC', 'N27XD', 'N3990A', 'N9641F', 'N3927R', 'N6026L', 'N51ED', 'N50EA', 'N155SH', 'N4195W', 'N95173', 'N469TS', 'N5918Q', 'N5058U', 'N227WA', 'N3933A', 'N45MM', 'N709SD', 'N9150M', 'N2334K', 'N9151H', 'N9113K', 'N1347B', 'N34164', 'N745TB', 'N52FW', 'N5161U', 'N192WW', 'N78708', 'N461SA', 'N1198Q', 'N3594F', 'N618LG', 'N3797W', 'N901ST'}
    frequent_icaos={'aaad00', 'ad6d83', 'a1fcf7', 'ad3bc7', 'a05121', 'a80d77', 'ac9d2d', 'acabc1', 'a570e2', 'a65006', 'a67a47', 'a7d1e2', 'a59ee3', 'aa06c8', 'a2a634', 'a48d94', 'a21693', 'a5bcc4', 'a3c44c', 'a171a2', 'a65f7e', 'a40926', 'a97791', 'a4a691', 'a08d5c', 'ac7485', 'a637fc', 'acaba2', 'a0de5a', 'a7a49d', 'a68727', 'a4589c', 'a4f8ab', 'a490b0', 'a796ad', 'a4f0cc'}
    #query_opensky(frequent_icaos)

    #flights=flightsFromFile('../data/ffl321/dec_flights.json')
    #flights.extend(flightsFromFile('../data/ffl321/jan_flights.json'))
    #filtered=filterFlights(flights)
    #filtered.to_file('../data/ffl321/filtered_dec-jan_flights.json')

    flights=flightsFromFile('../data/ffl321/filtered_dec-jan_flights.json')
    analyzeFlights(flights)

    # files[1]
    # multiple flights >5
    # get icaos
    # get all flights
    """
    oct2019 = {('N709SD', 14), ('N4195W', 17), ('N227WA', 13), ('N3990A', 28), ('N5161U', 78), ('N5058U', 96), ('N5918Q', 15), ('N155SH', 41), ('N3933A', 32), ('N52FW', 11), ('N9113K', 12), ('N3797W', 22), ('N3927R', 78), ('N9150M', 68), ('N961CC', 16), ('N45MM', 11), ('N34164', 16), ('N95173', 16)}
    nov2019 = {('N192WW', 48), ('N3927R', 71), ('N95173', 16), ('N5058U', 97), ('N3933A', 35), ('N1347B', 13), ('N155SH', 28), ('N5161U', 100), ('N1198Q', 12), ('N745TB', 15), ('N4195W', 15), ('N469TS', 16), ('N461SA', 11), ('N901ST', 13), ('N9150M', 37)}
    dec2019 = {('N95173', 13), ('N3990A', 19), ('N3927R', 43), ('N5058U', 87), ('N78708', 12), ('N34164', 11), ('N9150M', 53), ('N4195W', 12), ('N155SH', 26), ('N9151H', 68)}
    jan2020 = {('N3927R', 71), ('N3990A', 50), ('N51ED', 12), ('N155SH', 37), ('N50EA', 26), ('N2334K', 21), ('N745TB', 14), ('N5058U', 88), ('N27XD', 11), ('N5161U', 45), ('N3594F', 15), ('N52FW', 11), ('N9150M', 38), ('N618LG', 13), ('N95173', 15), ('N4195W', 23), ('N9151H', 76), ('N34164', 11), ('N6026L', 13), ('N9641F', 36)}
    """