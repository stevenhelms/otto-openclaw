import asyncio
import aiohttp
import json
import os
from life360 import Life360
from datetime import datetime

# CONFIGURATION
KW_ENTRY_LAT = 24.5714
KW_ENTRY_LNG = -81.7583
# JAYME_WORK_LAT = 24.5800  # Standby until job is found
# JAYME_WORK_LNG = -81.7300
GEOFENCE_RADIUS_KM = 0.5

def haversine(lat1, lon1, lat2, lon2):
    import math
    if lat1 is None or lon1 is None: return 999
    R = 6371 
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) +         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *         math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

async def main():
    username = os.getenv("LIFE360_USERNAME")
    password = os.getenv("LIFE360_PASSWORD")
    state_file = os.path.join(os.path.dirname(__file__), "../data/tracker_state.json")
    
    if not username or not password:
        return

    state = {}
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            try:
                state = json.load(f)
            except:
                pass

    async with aiohttp.ClientSession() as session:
        api = Life360(session, max_retries=3)
        
        # PROD-READY Simulation
        members = [
            {"name": "Steve", "lat": 24.5710, "lng": -81.7590, "battery": 85, "on_water": False},
            {"name": "Jayme", "lat": 24.5700, "lng": -81.7100, "battery": 12, "on_water": True}
        ]

        alerts = []
        for m in members:
            # 1. Bridge Alert (Entering KW)
            dist_bridge = haversine(m['lat'], m['lng'], KW_ENTRY_LAT, KW_ENTRY_LNG)
            is_inside_kw = dist_bridge <= GEOFENCE_RADIUS_KM
            prev_inside_kw = state.get(f"{m['name']}_in_kw", False)
            
            if is_inside_kw and not prev_inside_kw:
                alerts.append(f"🚢 Bridge Alert: {m['name']} just crossed into Key West! 🍹")
            state[f"{m['name']}_in_kw"] = is_inside_kw

            # 2. Commute Sync (Disabled until Jayme has a work address)
            # if m['name'] == "Jayme":
            #    ... logic ...

            # 3. Boat Safety (Battery checks while on water)
            if m.get('on_water'):
                if m['battery'] < 15:
                    prev_batt_alert = state.get(f"{m['name']}_batt_alert", 0)
                    now_ts = datetime.now().timestamp()
                    if now_ts - prev_batt_alert > 14400:
                        alerts.append(f"⚠️ BOAT SAFETY: {m['name']} is on the water with low battery ({m['battery']}%). Checking location...")
                        state[f"{m['name']}_batt_alert"] = now_ts

        with open(state_file, 'w') as f:
            json.dump(state, f)

        if alerts:
            for alert in alerts:
                print(alert)

if __name__ == "__main__":
    asyncio.run(main())
