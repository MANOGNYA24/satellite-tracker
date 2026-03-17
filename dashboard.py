import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
import plotly.graph_objects as go
from skyfield.api import load, EarthSatellite, wgs84
from tle_fetcher import load_satellites

satellites = load_satellites()

st.set_page_config(layout="wide")
st.title("Live Satellite Tracker")
st.write("Tracking satellites in real time")

ts = load.timescale(builtin=True)
t = ts.now()

max_sats = st.slider("How many satellites to track?", 10, 1000, 32)
satellites = satellites[:max_sats]

lats = []
longs = []
names = []
alts = []

for s in satellites:
    sat = EarthSatellite(s["line1"], s["line2"], s["name"], ts)
    geocentric = sat.at(t)
    subpoint = wgs84.subpoint(geocentric)
    lats.append(subpoint.latitude.degrees)
    longs.append(subpoint.longitude.degrees)
    names.append(s["name"])
    alts.append(subpoint.elevation.km)

search = st.session_state.get("search", "")



def split_orbit(lats, lons):
    segments_lat, segments_lon = [[]], [[]]
    for i in range(1, len(lons)):
        segments_lat[-1].append(lats[i-1])
        segments_lon[-1].append(lons[i-1])
        if abs(lons[i] - lons[i-1]) > 180:
            segments_lat.append([])
            segments_lon.append([])
    segments_lat[-1].append(lats[-1])
    segments_lon[-1].append(lons[-1])
    return segments_lat, segments_lon

orbit_lats = []
orbit_lons = []

match = None
if search:
    match = next((s for s in satellites if search.upper() in s["name"].upper()), None)
    if match:
        sat_obj = EarthSatellite(match["line1"], match["line2"], match["name"], ts)
        now = datetime.now(timezone.utc)
        for minutes in range(0, 90, 2):
            future_time = now + timedelta(minutes=minutes)
            future_t = ts.from_datetime(future_time)
            pos = wgs84.subpoint(sat_obj.at(future_t))
            orbit_lats.append(pos.latitude.degrees)
            orbit_lons.append(pos.longitude.degrees)



fig = go.Figure(go.Scattergeo(
    lat=lats, lon=longs, text=names,
    mode="markers",
    marker=dict(size=8, color="#00FFD1", symbol="circle"),
    showlegend=False
))

if orbit_lats:
    seg_lats, seg_lons = split_orbit(orbit_lats, orbit_lons)
    for seg_lat, seg_lon in zip(seg_lats, seg_lons):
        fig.add_trace(go.Scattergeo(
            lat=seg_lat, lon=seg_lon,
            mode="lines",
            line=dict(color="yellow", width=2),
            showlegend=False,
            name="Orbit path"
        ))
if search and match:
    match_idx = next((i for i, n in enumerate(names) if search.upper() in n.upper()), None)
    if match_idx is not None:
        fig.add_trace(go.Scattergeo(
            lat=[lats[match_idx]],
            lon=[longs[match_idx]],
            text=[names[match_idx]],
            mode="markers",
            marker=dict(
                size=15,
                color="red",
                symbol="circle",
                line=dict(color="white", width=2)
            ),
            showlegend=False,
            name=names[match_idx]
        ))

fig.update_layout(
    paper_bgcolor="#0d1117",
    geo=dict(
        showland=True,
        landcolor="#1c2535",
        showocean=True,
        oceancolor="#0a1628",
        showcountries=True,
        countrycolor="#2a3a50",
        bgcolor="#0d1117",
    ),
    height=600,
)




df = pd.DataFrame({
    "Satellite": names,
    "Latitude": lats,
    "Longitude": longs,
    "Altitude (km)": alts
})

col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    search = st.text_input("Search for a satellite to see its orbit", key="search")
    if search:
        df_filtered = df[df["Satellite"].str.contains(search, case=False, na=False)]
        if len(df_filtered) == 0:
            st.warning(f"No satellite found matching '{search}'")
        else:
            st.dataframe(df_filtered, use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)

import time
time.sleep(30)
st.rerun()

