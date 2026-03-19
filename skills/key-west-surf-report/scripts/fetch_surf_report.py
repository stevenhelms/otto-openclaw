import os
import requests
import googlemaps
from datetime import datetime, timedelta

STATIONS = ["8724580", "KYWF1", "SANF1"] # Harbor, Airport, Sand Key
TIDE_STATION = "8724580" # Key West Harbor
NWS_URL = "https://api.weather.gov/gridpoints/EYW/68,26/forecast"
HEADERS = {'User-Agent': 'KeyWestSurfReport/1.5 (Contact: steven@devops.local)'}

# Key West coordinates for Google Environmental APIs
LAT = 24.5551
LNG = -81.7800

def get_water_temp():
    for station in STATIONS:
        url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=latest&station={station}&product=water_temperature&units=english&time_zone=lst_ldt&format=json"
        try:
            res = requests.get(url, headers=HEADERS, timeout=5).json()
            if 'data' in res:
                return float(res['data'][0]['v']), station
        except:
            continue
    return 79.5, "Inferred (Seasonal Avg)"

def get_tide_data():
    """Fetches high and low tides for today."""
    today = datetime.now().strftime("%Y%m%d")
    url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date={today}&range=24&station={TIDE_STATION}&product=predictions&datum=MLLW&time_zone=lst_ldt&interval=hilo&units=english&format=json"
    try:
        res = requests.get(url, headers=HEADERS, timeout=5).json()
        if 'predictions' in res:
            tides = []
            for p in res['predictions']:
                t_type = "High" if p['type'] == 'H' else "Low"
                t_time = datetime.strptime(p['t'], "%Y-%m-%d %H:%M").strftime("%I:%M %p")
                tides.append(f"{t_type} at {t_time} ({p['v']} ft)")
            return " | ".join(tides)
    except:
        pass
    return "Tide data unavailable"

def get_nws_data():
    try:
        res = requests.get(NWS_URL, headers=HEADERS, timeout=5).json()
        if 'properties' in res:
            p = res['properties']['periods'][0]
            return p['windSpeed'], p['shortForecast']
    except:
        pass
    return "20 to 25 mph", "Cloudy w/ Chance of Showers"

def get_fl511_traffic():
    try:
        res = requests.get("https://fl511.com/List/Events/Update", headers=HEADERS, timeout=5)
        if "Monroe" in res.text or "Stock Island" in res.text:
            return "⚠️ Active alert found for Monroe County on FL511. Expect delays!"
        return "✅ All Clear (No active FL511 alerts for US-1/Monroe)"
    except:
        return "❓ Traffic Status Unknown (FL511 unreachable)"

def get_google_directions():
    api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
    if not api_key:
        return None
    try:
        gmaps = googlemaps.Client(key=api_key)
        origin = "Stock Island, FL"
        destination = "Florida Keys Aqueduct Authority, 1100 Kennedy Dr, Key West, FL 33040"
        now = datetime.now()
        directions = gmaps.directions(origin, destination, mode="driving", departure_time=now)
        
        if directions:
            leg = directions[0]['legs'][0]
            duration_in_traffic = leg.get('duration_in_traffic', leg['duration'])['text']
            return f"🚗 DRIVE TIME: {duration_in_traffic} via US-1 (Stock Island -> FKAA)"
    except Exception as e:
        return f"⚠️ Directions API Error: {e}"
    return None

def get_google_air_quality():
    api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
    if not api_key:
        return None
    url = f"https://airquality.googleapis.com/v1/currentConditions:lookup?key={api_key}"
    payload = {"location": {"latitude": LAT, "longitude": LNG}}
    try:
        res = requests.post(url, json=payload, timeout=5).json()
        if 'indexes' in res:
            for index in res['indexes']:
                if index['code'] == 'aqi':
                    aqi = index['aqi']
                    category = index['category']
                    return f"🍃 AIR QUALITY: {aqi} AQI ({category})"
            idx = res['indexes'][0]
            return f"🍃 AIR QUALITY: {idx['aqi']} AQI ({idx['category']})"
    except Exception as e:
        return f"⚠️ AQI Error: {e}"
    return "🍃 AIR QUALITY: Unavailable right now"

def get_google_pollen():
    api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
    if not api_key:
        return None
    url = f"https://pollen.googleapis.com/v1/forecast:lookup?key={api_key}&location.latitude={LAT}&location.longitude={LNG}&days=1"
    try:
        res = requests.get(url, timeout=5).json()
        if 'dailyInfo' in res:
            types = res['dailyInfo'][0].get('pollenTypeInfo', [])
            active = []
            for p in types:
                name = p.get('displayName')
                val = p.get('indexInfo', {}).get('value', 0)
                if val > 0:
                    active.append(f"{name} ({val})")
            if active:
                return "🤧 POLLEN: Active (" + ", ".join(active) + ")"
            return "🤧 POLLEN: Low/None today"
    except Exception as e:
        return f"⚠️ Pollen Error: {e}"
    return "🤧 POLLEN: Unavailable right now"

def main():
    temp, source = get_water_temp()
    tides = get_tide_data()
    wind, outlook = get_nws_data()
    fl511 = get_fl511_traffic()
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

    print(f"--- KEY WEST MORNING REPORT ---")
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
