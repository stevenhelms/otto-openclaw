import sys
import os
import requests
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))

from otto_utils import load_json_file, save_json_file

DATA_FILE = Path(__file__).parent / "../data/history.json"


def get_serp_api_prices(api_key, departure_id="EYW", arrival_id="XNA") -> list:
    """
    Fetch flight prices using SerpApi (Google Flights) for 30/60/90-day offsets.

    Always returns a list of price-point dicts. Raises ValueError if the API
    key is missing so the caller can decide how to handle it.
    """
    if not api_key:
        raise ValueError("SERPAPI_API_KEY is not set — add it to scripts/.env")

    results = []
    for offset in [30, 60, 90]:
        outbound_date = (datetime.now() + timedelta(days=offset)).strftime("%Y-%m-%d")
        return_date = (datetime.now() + timedelta(days=offset + 7)).strftime("%Y-%m-%d")

        params = {
            "engine": "google_flights",
            "departure_id": departure_id,
            "arrival_id": arrival_id,
            "outbound_date": outbound_date,
            "return_date": return_date,
            "currency": "USD",
            "api_key": api_key,
        }

        try:
            r = requests.get("https://serpapi.com/search.json", params=params, timeout=20)
            data = r.json()
            best_flights = data.get("best_flights", [])
            if best_flights:
                results.append({
                    "check_date": datetime.now().strftime("%Y-%m-%d"),
                    "flight_date": outbound_date,
                    "price": best_flights[0].get("price"),
                    "route": f"{departure_id}-{arrival_id}",
                })
        except Exception as e:
            print(f"Error fetching {departure_id}->{arrival_id} for {outbound_date}: {e}")

    return results


def main():
    api_key = os.getenv("SERPAPI_API_KEY")

    new_data = []
    for departure, arrival in [("EYW", "XNA"), ("XNA", "EYW")]:
        try:
            new_data.extend(get_serp_api_prices(api_key, departure, arrival))
        except ValueError as e:
            print(f"--- ✈️ FLIGHT TRACKER ERROR --- {e}")
            return
        except Exception as e:
            print(f"--- ✈️ FLIGHT TRACKER ERROR ({departure}->{arrival}) --- {e}")
            # Continue with results already collected from the other direction

    if not new_data:
        print("--- ✈️ FLIGHT TRACKER --- No price data returned. Check API key and quota.")
        return

    history = load_json_file(str(DATA_FILE))
    history.extend(new_data)
    save_json_file(str(DATA_FILE), history)

    print("--- ✈️ FLIGHT TRACKER UPDATED ---")
    print(f"Tracked {len(new_data)} price points for EYW <-> XNA.")
    for entry in new_data:
        print(f"  - {entry['route']} on {entry['flight_date']}: ${entry['price']}")


if __name__ == "__main__":
    main()
