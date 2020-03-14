import json

callsign = "DCM8346"
icao = "a1c6ba"
departure = "KTEB"
arrival = "KBED"
start = "2020-02-26 13:38:34"
end = "2020-02-26 14:12:11"

class MyFlight:

    def __init__(self, callsign=None, icao=None, departure=None,
            arrival=None, start=None, end=None):
        self.callsign = callsign
        self.icao = icao
        self.departure = departure
        self.arrival = arrival
        self.start = start
        self.end = end

    def __str__(self):
        string =  "Flight:" + \
                "\n  Callsign:  " + str(self.callsign) + \
                "\n  Icao:      " + str(self.icao) + \
                "\n  Departure: " + str(self.departure) + \
                "\n  Arrival:   " + str(self.arrival) + \
                "\n  Start:     " + str(self.start) + \
                "\n  End:       " + str(self.end)
        return string

class Flights:

    def __init__(self):
        self.empty()

    def __str__(self):
        string = ""
        for e in self.elements:
            string += str(e) + "\n"
        return string

    def append(self, flight):
        self.elements.append(flight)

    def remove(self, flight):
        self.elements.remove(flight)

    def empty(self):
        self.elements = list()

    def to_json(self):
        json_string = '[\n'

        for e in self.elements:
            json_string += '  {\n'
            json_string += '    "callsign"  : "'+str(e.callsign)+'",\n'
            json_string += '    "icao"      : "'+str(e.icao)+'",\n'
            json_string += '    "departure" : "'+str(e.departure)+'",\n'
            json_string += '    "arrival"   : "'+str(e.arrival)+'",\n'
            json_string += '    "start"     : "'+str(e.start)+'",\n'
            json_string += '    "end"       : "'+str(e.end)+'"\n'
            json_string += '  },\n'

        json_string = json_string[:-2]+'\n]\n'
        return json_string

    def to_file(self, filename):
        file  = open(filename, "w")
        file.write(self.to_json())
        file.close()

    def from_file(self, filename):
        file = open(filename, "r")
        string = file.read()
        file.close()

        json_data = json.loads(string)
        self.elements = list()

        for d in json_data:
            f = MyFlight(d['callsign'], d['icao'], d['departure'],
                d['arrival'], d['start'], d['end'])
            self.append(f)
        
        return str(self)

myFlight = MyFlight(callsign, icao, departure, arrival, start, end)

flight2 = MyFlight("ABC123")

flights = Flights()
flights.append(myFlight)
flights.append(flight2)

flights.to_file("flights_test.json")
flights.from_file("flights_test.json")