import sys
import os
import googlemaps
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))

from otto_utils import get_fl511_incidents

HOME_ADDR = "30 Kingfisher Ln, Key West, FL 33040"
WORK_ADDR = "Florida Keys Aqueduct Authority, 1100 Kennedy Dr, Key West, FL 33040"


def get_commute_estimates():
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not api_key:
        return {"car": "⚠️ Data Unavailable (GOOGLE_PLACES_API_KEY not set)", "bike": "⚠️ Data Unavailable"}

    gmaps = googlemaps.Client(key=api_key)
    now = datetime.now()
    results = {}

    try:
        # Driving estimate (with live traffic)
        matrix_drive = gmaps.distance_matrix(HOME_ADDR, WORK_ADDR, mode="driving", departure_time=now)
        drive_el = matrix_drive["rows"][0]["elements"][0]
        if drive_el["status"] == "OK":
            duration = drive_el.get("duration_in_traffic", drive_el["duration"])["text"]
            distance = drive_el["distance"]["text"]
            results["car"] = f"{duration} ({distance})"
        else:
            results["car"] = "⚠️ Driving Data Unavailable"

        # Biking estimate (no live traffic, but a reliable baseline)
        matrix_bike = gmaps.distance_matrix(HOME_ADDR, WORK_ADDR, mode="bicycling")
        bike_el = matrix_bike["rows"][0]["elements"][0]
        results["bike"] = bike_el["duration"]["text"] if bike_el["status"] == "OK" else "⚠️ Biking Data Unavailable"

    except Exception as e:
        results["error"] = str(e)

    return results


def main():
    estimates = get_commute_estimates()
    incidents = get_fl511_incidents()

    print("--- KEY WEST COMMUTE REPORT ---")
    print(f"🚗 CAR: {estimates.get('car', 'Error')}")
    print(f"🚲 BIKE: {estimates.get('bike', 'Error')}")
    print(f"🚨 ALERTS: {incidents}")

    if "error" in estimates:
        print(f"\n❌ Note: {estimates['error']}")


if __name__ == "__main__":
    main()
