from traffic.data import opensky
from traffic.core import Traffic, Flight

import pandas as pd


start = "2020-02-26"
end = "2020-02-26"
filename = start + "_" + end + "_DCM_recordings.parquet"

if __name__ == "__main__":
    t_dcm = Traffic.from_file(filename)
    print(len(t_dcm.callsigns))

    flight = t_dcm[8]