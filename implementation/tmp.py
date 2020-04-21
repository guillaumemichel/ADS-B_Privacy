from traffic.data import airports
from geopy.distance import geodesic

if __name__ == '__main__':
    lax = airports['KLAX']
    lga = airports['KLGA']
    print(geodesic((lax.latitude, lax.longitude),(lga.latitude, lga.longitude)).km)

