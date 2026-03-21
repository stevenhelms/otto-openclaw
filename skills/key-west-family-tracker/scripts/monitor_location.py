import sys
import asyncio
import aiohttp
import json
import os
import math
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))

from life360 import Life360
from otto_utils import load_json_file, save_json_file

# CONFIGURATION
KW_ENTRY_LAT = 24.5714
KW_ENTRY_LNG = -81.7583
# JAYME_WORK_LAT = 24.5800  # Standby until job is found
# JAYME_WORK_LNG = -81.7300
GEOFENCE_RADIUS_KM = 0.5

STATE_FILE = Path(__file__).parent / "../data/tracker_state.json"


def haversine(lat1, lon1, lat2, lon2):
    """Returns the great-circle distance in km between two GPS coordinates."""
    if lat1 is None or lon1 is None:
        return 999
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    )
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


async def main():
    username = os.getenv("LIFE360_USERNAME")
    password = os.getenv("LIFE360_PASSWORD")

    if not username or not password:
        print("⚠️ Missing LIFE360_USERNAME or LIFE360_PASSWORD in .env")
        return

    state = load_json_file(str(STATE_FILE))
    if not isinstance(state, dict):
        state = {}

    async with aiohttp.ClientSession() as session:
        api = Life360(session, max_retries=3)  # noqa: F841 — auth wiring pending real API

        # PROD-READY Simulation — replace with real api.get_members() call
        members = [
            {"name": "Steve", "lat": 24.5710, "lng": -81.7590, "battery": 85, "on_water": False},
            {"name": "Jayme", "lat": 24.5700, "lng": -81.7100, "battery": 12, "on_water": True},
        ]

        alerts = []
        now_ts = datetime.now().timestamp()

        for m in members:
            # 1. Bridge Alert (Entering KW)
            dist_bridge = haversine(m["lat"], m["lng"], KW_ENTRY_LAT, KW_ENTRY_LNG)
            is_inside_kw = dist_bridge <= GEOFENCE_RADIUS_KM
            prev_inside_kw = state.get(f"{m['name']}_in_kw", False)

            if is_inside_kw and not prev_inside_kw:
                alerts.append(f"🚢 Bridge Alert: {m['name']} just crossed into Key West! 🍹")
            state[f"{m['name']}_in_kw"] = is_inside_kw

            # 2. Commute Sync (Disabled until Jayme has a work address)
            # if m['name'] == "Jayme":
            #    ... logic ...

            # 3. Boat Safety (Battery checks while on water, deduplicated per 4 hours)
            if m.get("on_water") and m["battery"] < 15:
                prev_batt_alert = state.get(f"{m['name']}_batt_alert", 0)
                if now_ts - prev_batt_alert > 14400:
                    alerts.append(
                        f"⚠️ BOAT SAFETY: {m['name']} is on the water with low battery "
                        f"({m['battery']}%). Checking location..."
                    )
                    state[f"{m['name']}_batt_alert"] = now_ts

    save_json_file(str(STATE_FILE), state)

    for alert in alerts:
        print(alert)


if __name__ == "__main__":
    asyncio.run(main())
