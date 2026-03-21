import os
import requests
import json
from datetime import datetime, timedelta

def get_serp_api_prices(api_key, departure_id="EYW", arrival_id="XNA"):
    """Fetch flight prices using SerpApi (Google Flights)."""
    if not api_key:
        return {"error": "SERPAPI_API_KEY missing"}
    
    results = []
    offsets = [30, 60, 90]
    
    for offset in offsets:
        outbound_date = (datetime.now() + timedelta(days=offset)).strftime("%Y-%m-%d")
        return_date = (datetime.now() + timedelta(days=offset+7)).strftime("%Y-%m-%d")
        
        url = "https://serpapi.com/search.json"
        params = {
            "engine": "google_flights",
            "departure_id": departure_id,
            "arrival_id": arrival_id,
            "outbound_date": outbound_date,
            "return_date": return_date,
            "currency": "USD",
            "api_key": api_key
        }
        
        try:
            r = requests.get(url, params=params, timeout=20)
            data = r.json()
            
            best_flights = data.get("best_flights", [])
            if best_flights:
                price = best_flights[0].get("price")
                results.append({
                    "check_date": datetime.now().strftime("%Y-%m-%d"),
                    "flight_date": outbound_date,
                    "price": price,
                    "route": f"{departure_id}-{arrival_id}"
                })
        except Exception as e:
            print(f"Error fetching for date {outbound_date}: {e}")
            
    return results

def main():
    api_key = os.getenv("SERPAPI_API_KEY")
    data_file = os.path.join(os.path.dirname(__file__), "../data/history.json")
    
    # Track both directions
    eyw_to_xna = get_serp_api_prices(api_key, "EYW", "XNA")
    xna_to_eyw = get_serp_api_prices(api_key, "XNA", "EYW")
    
    if isinstance(eyw_to_xna, dict) and "error" in eyw_to_xna:
        new_data = eyw_to_xna
    elif isinstance(xna_to_eyw, dict) and "error" in xna_to_eyw:
        new_data = xna_to_eyw
    else:
        new_data = eyw_to_xna + xna_to_eyw
    
    if not new_data or (isinstance(new_data, dict) and "error" in new_data):
        print(f"--- ✈️ FLIGHT TRACKER ERROR ---\n{new_data}")
        return

    # Load and update history
    history = []
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            try:
                history = json.load(f)
            except:
                pass
    
    history.extend(new_data)
    
    with open(data_file, 'w') as f:
        json.dump(history, f, indent=2)
        
    print(f"--- ✈️ FLIGHT TRACKER UPDATED ---")
    print(f"Tracked {len(new_data)} price points for EYW <-> XNA.")
    for entry in new_data:
        print(f"  - {entry['route']} on {entry['flight_date']}: ${entry['price']}")

if __name__ == "__main__":
    main()
