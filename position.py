import requests
from skyfield.api import load, EarthSatellite, wgs84
from tle_fetcher import satellites

ts = load.timescale(builtin=True)
t = ts.now()

for s in satellites:
    sat = EarthSatellite(s["line1"], s["line2"], s["name"], ts)
    geocentric = sat.at(t)
    subpoint = wgs84.subpoint(geocentric)
    print(s["name"], "→ lat:", subpoint.latitude.degrees, "lon:", subpoint.longitude.degrees, "alt:", subpoint.elevation.km)