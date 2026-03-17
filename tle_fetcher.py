"""
import requests 
url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=TLE"
response = requests.get(url)
# print(response.text)

lines = response.text.strip().splitlines()
#print("Total lines:", len(lines))
#print("First satellite name:", lines[0])
#print("Second satellite name:", lines[3])

satellites = []
i=0
while i<len(lines) -2:
    if not lines[i].startswith("1 ") and not lines[i].startswith("2 "):
        name = lines[i].strip()
        line1 = lines[i+1]
        line2 = lines[i+2]
        satellites.append({"name": name, "line1": line1, "line2":line2})
        i+=3
    else:
        i+=1
#print("satellites parsed:", len(satellites))
#print("fiest one:", satellites[0])
 

import requests

def load_satellites():
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=TLE"
    response = requests.get(url, timeout=30)
    lines = response.text.strip().splitlines()

    satellites = []
    i = 0
    while i < len(lines) - 2:
        if not lines[i].startswith("1 ") and not lines[i].startswith("2 "):
            name = lines[i].strip()
            line1 = lines[i+1]
            line2 = lines[i+2]
            if line1.startswith("1 ") and line2.startswith("2 "):
                satellites.append({"name": name, "line1": line1, "line2": line2})
                i += 3
                continue
        i += 1
    return satellites


import requests

def load_satellites():
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=TLE"
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
    except Exception as e:
        st.error(f"Could not load satellite data: {e}")
        return []

    lines = response.text.strip().splitlines()
    satellites = []
    i = 0
    while i < len(lines) - 2:
        if not lines[i].startswith("1 ") and not lines[i].startswith("2 "):
            name = lines[i].strip()
            line1 = lines[i+1]
            line2 = lines[i+2]
            if line1.startswith("1 ") and line2.startswith("2 "):
                satellites.append({"name": name, "line1": line1, "line2": line2})
                i += 3
                continue
        i += 1
    return satellites
"""

import requests

FALLBACK_TLES = """ISS (ZARYA)
1 25544U 98067A   24001.50000000  .00016717  00000-0  30757-3 0  9993
2 25544  51.6400 208.9163 0006317  86.9840 273.1530 15.49815849432729
CSS (TIANHE)
1 48274U 21035A   24001.50000000  .00029757  00000-0  34787-3 0  9993
2 48274  41.4663 181.9138 0006689 299.3968  60.6202 15.60904690278280
NOAA 19
1 33591U 09005A   24001.50000000  .00000068  00000-0  68568-4 0  9994
2 33591  99.1920  45.6400 0014027 330.7700  29.2900 14.12362762768523
TERRA
1 25994U 99068A   24001.50000000  .00000076  00000-0  26093-4 0  9990
2 25994  98.2104 106.8945 0001206  89.9870 270.1460 14.57115954282138
AQUA
1 27424U 02022A   24001.50000000  .00000076  00000-0  26093-4 0  9991
2 27424  98.2104 106.8945 0001206  89.9870 270.1460 14.57115954282139"""

import requests

FALLBACK_TLES = """ISS (ZARYA)
1 25544U 98067A   24001.50000000  .00016717  00000-0  30757-3 0  9993
2 25544  51.6400 208.9163 0006317  86.9840 273.1530 15.49815849432729
CSS (TIANHE)
1 48274U 21035A   24001.50000000  .00029757  00000-0  34787-3 0  9993
2 48274  41.4663 181.9138 0006689 299.3968  60.6202 15.60904690278280
NOAA 19
1 33591U 09005A   24001.50000000  .00000068  00000-0  68568-4 0  9994
2 33591  99.1920  45.6400 0014027 330.7700  29.2900 14.12362762768523
TERRA
1 25994U 99068A   24001.50000000  .00000076  00000-0  26093-4 0  9990
2 25994  98.2104 106.8945 0001206  89.9870 270.1460 14.57115954282138
AQUA
1 27424U 02022A   24001.50000000  .00000076  00000-0  26093-4 0  9991
2 27424  98.2104 106.8945 0001206  89.9870 270.1460 14.57115954282139"""


def parse_fallback():
    lines = FALLBACK_TLES.strip().splitlines()
    satellites = []
    i = 0
    while i < len(lines) - 2:
        if not lines[i].startswith("1 ") and not lines[i].startswith("2 "):
            name = lines[i].strip()
            line1 = lines[i+1]
            line2 = lines[i+2]
            if line1.startswith("1 ") and line2.startswith("2 "):
                satellites.append({"name": name, "line1": line1, "line2": line2})
                i += 3
                continue
        i += 1
    return satellites


def load_satellites():
    try:
        url = "https://satchecker.cps.iau.org/tools/tles-at-epoch/?page=1&per_page=100"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        satellites = []
        for item in data:
            satellites.append({
                "name": item["satellite_name"],
                "line1": item["tle_line1"],
                "line2": item["tle_line2"]
            })
        print(f"Loaded {len(satellites)} satellites!")
        return satellites
    except Exception as e:
        print(f"API failed: {e}, using fallback.")
        return parse_fallback()