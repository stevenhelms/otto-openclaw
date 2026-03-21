import sys
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))

from otto_utils import get_cruise_ship_count

TOURIST_STREETS = ["Greene", "Duval", "Fitzpatrick", "Front"]


def main():
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    ships = get_cruise_ship_count()

    print("--- 🌮 CAYO HUESO MEXICAN FOOD GUIDE ---")
    print(f"🚢 Port Status: {ships} Cruise Ships in harbor today.")

    if ships >= 2:
        print("⚠️ Warning: Port is busy. Strategic choices are below.\n")

    places_url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": (
            "places.displayName,places.formattedAddress,"
            "places.rating,places.currentOpeningHours,places.userRatingCount"
        ),
    }

    try:
        r = requests.post(
            places_url, json={"textQuery": "best mexican food in Key West"}, headers=headers, timeout=10
        )
        results = r.json().get("places", [])

        for p in results[:5]:
            name = p["displayName"]["text"]
            rating = p.get("rating", "N/A")
            reviews = p.get("userRatingCount", 0)
            addr = p.get("formattedAddress", "")
            open_now = p.get("currentOpeningHours", {}).get("openNow", False)

            is_tourist_zone = any(street in addr for street in TOURIST_STREETS)

            if ships >= 2 and is_tourist_zone:
                status = "⏳ Likely Busy"
                advice = " (Tourist zone—try after 4 PM)"
            elif not open_now:
                status = "💤 Currently Closed"
                advice = ""
            else:
                status = "✅ Recommended"
                advice = ""

            print(f"- {name} ({rating} ⭐, {reviews} reviews): {status}{advice}")
            print(f"  📍 {addr}\n")

    except Exception as e:
        print(f"Error pulling live data: {e}")
        # Fallback to curated list if API fails


if __name__ == "__main__":
    main()
