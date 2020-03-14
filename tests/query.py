
from traffic.data import opensky
from traffic.core import Traffic
import pandas as pd

"""
t_dcm = opensky.history(
    "2020-02-26 00:00",
    "2020-02-26 23:59",
    callsign="DCM%",
)
"""
t_dcm = Traffic.from_file("test.parquet")

#t_dcm = pd.read_parquet("test.parquet")

print(len(t_dcm))

unique_callsigns = set()
for f in t_dcm:
    unique_callsigns.add(f.callsign)

print(len(unique_callsigns))

by_callsign = {}
for c in t_dcm:
    if c.callsign in by_callsign:
        by_callsign[c.callsign].append(c)
    else:
        by_callsign[c.callsign] = [ c ]


for c in by_callsign:
    if len(by_callsign[c]) == 1:
        print(c, by_callsign[c][0].icao24)



t_dcm.to_parquet("test.parquet",allow_truncated_timestamps=True)