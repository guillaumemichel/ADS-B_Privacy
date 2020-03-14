from traffic.data import opensky

t_dcm = opensky.history(
    "2020-02-24 00:00",
    "2020-02-24 23:59",
    #departure_airport="KLAX",
    #arrival_airport="KLAX",
    callsign="DCM%",
)

cs = set()

for f in t_dcm:
    cs.add(f.callsign)

print(cs)
print(len(cs))