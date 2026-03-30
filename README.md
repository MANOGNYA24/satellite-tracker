# 🛰️ Live Satellite Tracker

A real-time satellite tracking dashboard built with Python that visualizes satellite positions across Earth using live orbital data.

🔗 **Live Demo:** https://satellite-tracker-pfqhukegybtm5mdzrtxe8g.streamlit.app/

---

## Screenshot

<img width="1500" height="776" alt="Screenshot 2026-03-30 at 7 51 45 PM" src="https://github.com/user-attachments/assets/e9186278-b342-446e-ab0e-fe18b694d4f5" />

---

## Features
- Real-time satellite position tracking using orbital mechanics
- Interactive world map with glowing satellite markers
- Orbit path visualization for any searched satellite
- Search satellites by name with live map + table filtering
- Adjustable slider to control number of satellites displayed
- Data table showing latitude, longitude, and altitude for each satellite
- Dark-themed professional dashboard UI

---

## How It Works
Satellites are tracked using **Two-Line Element (TLE)** data — a standard format that encodes orbital parameters. The **Skyfield** library uses the **SGP4 propagation model** to compute each satellite's exact position at the current time, which is then plotted on an interactive Plotly world map.

---

## Satellites Tracked
Includes satellites from multiple orbit types:
- **LEO** (Low Earth Orbit) — ISS, Hubble, Starlink, Sentinel, Landsat
- **MEO** (Medium Earth Orbit) — GPS, Galileo, GLONASS, BeiDou
- **GEO** (Geostationary) — GOES-16, Meteosat, Intelsat, IRNSS

---

## 🛠️ Tech Stack
| Tool | Purpose |
|---|---|
| Python | Core language |
| Skyfield | Orbital mechanics & position computation |
| Plotly | Interactive world map |
| Streamlit | Web dashboard |
| Pandas | Data handling |
| Requests | TLE data fetching |

---

## Run Locally
```bash
git clone https://github.com/MANOGNYA24/satellite-tracker
cd satellite-tracker
pip install -r requirements.txt
streamlit run dashboard.py
```

---

## Data Source
TLE orbital data from [CelesTrak](https://celestrak.org) — a public satellite catalog maintained since 1985.
