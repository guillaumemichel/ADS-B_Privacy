from traffic.data import opensky

callsign = "DCM"

def query(start_day, end_day):
    t_dcm = opensky.history(
        start_day+" 00:00",
        end_day+" 23:59",
        callsign=callsign+'%',
    )
    return t_dcm

def save(data, filename):
    data.to_parquet(filename,allow_truncated_timestamps=True)

prefix = '../data/recordings/'
start = "2020-03-01"
end = "2020-03-30"

if __name__ == "__main__":
    filename = prefix + start + "_" + end + "_"+callsign+"_recordings.parquet"

    data = query(start, end)
    save(data, filename)
    print('Done =)')