import datetime
import datetime as dt
import requests


def iss_passes(lat: float, lng: float, alt_m: int = 0,
               days: int = 5, min_visibility_s: int = 50,
               api_key: str = "33Q884-HFUV8K-SCS3LG-55CU"):
    """
    Query N2YO 'visual passes' for ISS (NORAD ID: 25544) and return in UTC.
    api_key: N2YO requires a license key for every transaction and enforces per-endpoint quotas.
    NORAD ID: A unique integer assigned to each tracked object in orbit.
    """
    
    url = ( f"https://api.n2yo.com/rest/v1/satellite/visualpasses/"
        f"25544/{lat}/{lng}/{alt_m}/{days}/{min_visibility_s}&apiKey={api_key}")

    
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    payload = resp.json()

    
    passes = payload.get("passes", [])
    if not passes:
        return []

    # Change Unix to readable UTC
    to_str = lambda ts: dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    intervals = [(to_str(p["startUTC"]), to_str(p["endUTC"])) for p in passes]
    return intervals



def time_range(start_time, end_time, number_of_intervals=1, gap_between_intervals_s=0):
    start_time_s = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time_s = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    if end_time_s <= start_time_s:
        raise ValueError(f"end_time ({end_time}) must be after start_time ({start_time})")
    d = (end_time_s - start_time_s).total_seconds() / number_of_intervals + gap_between_intervals_s * (1 / number_of_intervals - 1)
    sec_range = [(start_time_s + datetime.timedelta(seconds=i * d + i * gap_between_intervals_s),
                  start_time_s + datetime.timedelta(seconds=(i + 1) * d + i * gap_between_intervals_s))
                 for i in range(number_of_intervals)]
    return [(ta.strftime("%Y-%m-%d %H:%M:%S"), tb.strftime("%Y-%m-%d %H:%M:%S")) for ta, tb in sec_range]


def compute_overlap_time(range1, range2):
    overlap_time = []
    for start1, end1 in range1:
        for start2, end2 in range2:
            low = max(start1, start2)
            high = min(end1, end2)
            # Record only if there is a real overlap duration
            if low < high:
                overlap_time.append((low, high))
    return overlap_time

if __name__ == "__main__":
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    print(compute_overlap_time(large, short))