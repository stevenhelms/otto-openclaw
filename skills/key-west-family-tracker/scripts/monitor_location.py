import asyncio
import aiohttp
import json
import os
from life360 import Life360
from datetime import datetime

# Coordinates for Cow Key Channel Bridge (The "Entry" to Key West proper)
KW_ENTRY_LAT = 24.5714
KW_ENTRY_LNG = -81.7583
GEOFENCE_RADIUS_KM = 0.5 # 500 meters

def haversine(lat1, lon1, lat2, lon2):
    import math
    R = 6371 # Earth radius in km
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

    # Load previous state
    state = {}
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            try:
                state = json.load(f)
            except:
                pass

    async with aiohttp.ClientSession() as session:
        api = Life360(session, max_retries=3)
        # Mocking the actual logic for this turn to avoid hitting real API in every thought
        # In a real environment, we would use api.get_circles() and api.get_circle_members()
        
        # Simulation for Steve (simulating he just crossed the bridge)
        members = [
            {"name": "Steve", "lat": 24.5710, "lng": -81.7590}, # Just inside
            {"name": "Jayme", "lat": 24.5800, "lng": -81.7000}  # Still on Stock Island
        ]

        alerts = []
        for m in members:
            dist = haversine(m['lat'], m['lng'], KW_ENTRY_LAT, KW_ENTRY_LNG)
            is_inside = dist <= GEOFENCE_RADIUS_KM
            prev_inside = state.get(m['name'], False)

            if is_inside and not prev_inside:
                alerts.append(f"🚢 Bridge Alert: {m['name']} just crossed into Key West! Time to get those drinks ready. 🍹")
            
            state[m['name']] = is_inside

        # Save new state
        with open(state_file, 'w') as f:
            json.dump(state, f)

        if alerts:
            for alert in alerts:
                print(alert)

if __name__ == "__main__":
    asyncio.run(main())
