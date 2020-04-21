from traffic.data import opensky


"""
Download all flights that used the parameter callsign during the given period
"""

callsign = "FFL"
airport = "KSDM"

def query(start_day, end_day):
    t_dcm = opensky.history(
        start_day+" 00:00",
        end_day+" 23:59",
        callsign=callsign+'%',
        #airport=airport,
    )
    return t_dcm

def save(data, filename):
    data.to_parquet(filename,allow_truncated_timestamps=True)

prefix = '../data/recordings/'
start = "2019-05-05"
end = "2019-06-03"

if __name__ == "__main__":
    filename = prefix + start + "_" + end + "_"+callsign+"_recordings.parquet"
    #filename = prefix + airport +"_recordings.parquet"

    data = query(start, end)
    save(data, filename)
    print('Done =)')