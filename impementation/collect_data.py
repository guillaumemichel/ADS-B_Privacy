from traffic.data import opensky

def query(start_day, end_day):
    t_dcm = opensky.history(
        start_day+" 00:00",
        end_day+" 23:59",
        callsign="DCM%",
    )
    return t_dcm

def save(data, filename):
    data.to_parquet(filename,allow_truncated_timestamps=True)

if __name__ == "__main__":
    start = "2019-11-01"
    end = "2019-11-30"
    filename = start + "_" + end + "_DCM_recordings.parquet"

    data = query(start, end)
    save(data, filename)