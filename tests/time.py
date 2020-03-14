import pandas as pd
from traffic.core import Traffic, Flight

def getFlightsFilename(start_day, end_day):
    return start_day + "_" + end_day + "_DCM_recordings.parquet"

def loadFlights(start_day, end_day):
    filename = getFlightsFilename(start_day, end_day)
    return Traffic.from_file(filename)

start = "2020-02-26"
end = "2020-02-26"

if __name__ == "__main__":
    flights = loadFlights(start, end)

    print(flights[2].start)
    print(flights[2].start + pd.Timedelta(minutes=-30))
    print(flights[2].start + pd.Timedelta(minutes=30))