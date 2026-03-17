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
"""

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
