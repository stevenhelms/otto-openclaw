import sys
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))

import googlemaps
from otto_utils import get_fl511_incidents

STATIONS = ["8724580", "KYWF1", "SANF1"]  # Harbor, Airport, Sand Key
TIDE_STATION = "8724580"  # Key West Harbor
NWS_URL = "https://api.weather.gov/gridpoints/EYW/68,26/forecast"
HEADERS = {"User-Agent": "KeyWestSurfReport/1.5 (Contact: steven@devops.local)"}

# Key West coordinates for Google Environmental APIs
LAT = 24.5551
LNG = -81.7800


def get_water_temp():
    for station in STATIONS:
        url = (
            f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
            f"?date=latest&station={station}&product=water_temperature"
            f"&units=english&time_zone=lst_ldt&format=json"
        )
        try:
            res = requests.get(url, headers=HEADERS, timeout=5).json()
            if "data" in res:
                return float(res["data"][0]["v"]), station
        except Exception:
            continue
    return 79.5, "Inferred (Seasonal Avg)"


def get_tide_data():
    """Fetches high and low tides for today."""
    today = (
        __import__("datetime").datetime.now().strftime("%Y%m%d")
    )
    url = (
        f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
        f"?begin_date={today}&range=24&station={TIDE_STATION}&product=predictions"
        f"&datum=MLLW&time_zone=lst_ldt&interval=hilo&units=english&format=json"
    )
    try:
        from datetime import datetime as _dt
        res = requests.get(url, headers=HEADERS, timeout=5).json()
        if "predictions" in res:
            tides = []
            for p in res["predictions"]:
                t_type = "High" if p["type"] == "H" else "Low"
                t_time = _dt.strptime(p["t"], "%Y-%m-%d %H:%M").strftime("%I:%M %p")
                tides.append(f"{t_type} at {t_time} ({p['v']} ft)")
            return " | ".join(tides)
    except Exception:
        pass
    return "Tide data unavailable"


def get_nws_data():
    try:
        res = requests.get(NWS_URL, headers=HEADERS, timeout=5).json()
        if "properties" in res:
            period = res["properties"]["periods"][0]
            return period["windSpeed"], period["shortForecast"]
    except Exception:
        pass
    return "20 to 25 mph", "Cloudy w/ Chance of Showers"


def get_google_directions():
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not api_key:
        return None
    from datetime import datetime
    try:
        gmaps = googlemaps.Client(key=api_key)
        directions = gmaps.directions(
            "Stock Island, FL",
            "Florida Keys Aqueduct Authority, 1100 Kennedy Dr, Key West, FL 33040",
            mode="driving",
            departure_time=datetime.now(),
        )
        if directions:
            leg = directions[0]["legs"][0]
            duration = leg.get("duration_in_traffic", leg["duration"])["text"]
            return f"🚗 DRIVE TIME: {duration} via US-1 (Stock Island -> FKAA)"
    except Exception as e:
        return f"⚠️ Directions API Error: {e}"
    return None


def get_google_air_quality():
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not api_key:
        return None
    url = f"https://airquality.googleapis.com/v1/currentConditions:lookup?key={api_key}"
    try:
        res = requests.post(url, json={"location": {"latitude": LAT, "longitude": LNG}}, timeout=5).json()
        indexes = res.get("indexes", [])
        if indexes:
            # Prefer the dedicated 'aqi' index; fall back to the first available index
            idx = next((i for i in indexes if i.get("code") == "aqi"), indexes[0])
            return f"🍃 AIR QUALITY: {idx['aqi']} AQI ({idx['category']})"
    except Exception as e:
        return f"⚠️ AQI Error: {e}"
    return "🍃 AIR QUALITY: Unavailable right now"



def get_google_pollen():
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not api_key:
        return None
    url = (
        f"https://pollen.googleapis.com/v1/forecast:lookup"
        f"?key={api_key}&location.latitude={LAT}&location.longitude={LNG}&days=1"
    )
    try:
        res = requests.get(url, timeout=5).json()
        if "dailyInfo" in res:
            active = [
                f"{p.get('displayName')} ({p.get('indexInfo', {}).get('value', 0)})"
                for p in res["dailyInfo"][0].get("pollenTypeInfo", [])
                if p.get("indexInfo", {}).get("value", 0) > 0
            ]
            if active:
                return "🤧 POLLEN: Active (" + ", ".join(active) + ")"
            return "🤧 POLLEN: Low/None today"
    except Exception as e:
        return f"⚠️ Pollen Error: {e}"
    return "🤧 POLLEN: Unavailable right now"


def main():
    from datetime import datetime
    temp, source = get_water_temp()
    tides = get_tide_data()
    wind, outlook = get_nws_data()
    fl511 = get_fl511_incidents()
    google_traffic = get_google_directions()
    aqi = get_google_air_quality()
    pollen = get_google_pollen()

    numeric_wind = [int(s) for s in wind.split() if s.isdigit()]
    max_wind = max(numeric_wind) if numeric_wind else 0

    if max_wind > 20:
        flag = "🔴 RED (Small Craft Advisory)"
    elif max_wind > 15:
        flag = "🟡 YELLOW (Moderate Chop)"
    else:
        flag = "🟢 GREEN (Calm)"

    print("--- KEY WEST MORNING REPORT ---")
    if google_traffic:
        print(google_traffic)
    print(f"🚧 ALERTS: {fl511}")
    if aqi:
        print(aqi)
    if pollen:
        print(pollen)
    print(f"🚩 FLAG STATUS: {flag}")
    print(f"🌊 TIDES: {tides}")
    print(f"🌡️ WATER TEMP: {temp}°F (Source: {source})")
    print(f"💨 WIND: {wind}")
    print(f"🌦️ OUTLOOK: {outlook}")


if __name__ == "__main__":
    main()
