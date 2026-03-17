import plotly.graph_objects as go
from skyfield.api import load, EarthSatellite, wgs84
from tle_fetcher import satellites

ts = load.timescale(builtin=True)
t = ts.now()

lats = []
longs = []
names = []

for s in satellites:
    sat = EarthSatellite(s["line1"], s["line2"], s["name"], ts)
    geocentric = sat.at(t)
    subpoint = wgs84.subpoint(geocentric)
    lats.append(subpoint.latitude.degrees)
    longs.append(subpoint.longitude.degrees)
    names.append(s["name"])
fig = go.Figure(go.Scattergeo(lat=lats, lon=longs, text=names, mode="markers"))
fig.update_layout(title="Live Satellite Tracker")
fig.show()
