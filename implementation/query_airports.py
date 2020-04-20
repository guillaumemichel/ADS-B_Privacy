from traffic.data import opensky

airport = 'KSDM'
start_day = '2019-11-01'
end_day = '2019-11-30'

t_dcm = opensky.history(
    start_day+" 00:00",
    end_day+" 23:59",
    airport=airport,
)

filename = '../data/recordings/KSDM_nov2019_recordings.parquet'
t_dcm.to_parquet(filename,allow_truncated_timestamps=True)
"""
print(len(t_dcm))

icaos = set()
for f in t_dcm:
    icaos.add(f.icao24)

icaos = list(icaos)
print(len(icaos))
string = ""
for i in icaos:
    string += i + '\n'

f = open('../data/recordings/KSDM_flights.txt', 'w')
f.write(string)
f.close()
"""