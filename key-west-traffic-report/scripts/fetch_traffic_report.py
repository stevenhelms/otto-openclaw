import os
import googlemaps
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# CONFIGURATION
API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
HOME_ADDR = '30 Kingfisher Ln, Key West, FL 33040' # Defaulting to Stock Island as mentioned earlier
WORK_ADDR = 'Florida Keys Aqueduct Authority, 1100 Kennedy Dr, Key West, FL 33040'

# FL511 Monroe County Alerts (Key West)
FL511_URL = "https://fl511.com/List/Alerts"

def get_google_maps_traffic():
    if not API_KEY:
        return "⚠️ Maps Data Unavailable (API Key missing)"
    
    gmaps = googlemaps.Client(key=API_KEY)
    now = datetime.now()
    try:
        # We use departure_time='now' to get traffic-aware duration
        matrix = gmaps.distance_matrix(HOME_ADDR, WORK_ADDR, 
                                      mode="driving", 
                                      departure_time=now)
        
        element = matrix['rows'][0]['elements'][0]
        if element['status'] == 'OK':
            # Note: distance_matrix only returns 'duration_in_traffic' if mode='driving' and departure_time is provided
            # and the request is not for a generic city name if traffic model requires precision.
            duration_in_traffic = element.get('duration_in_traffic', element['duration'])['text']
            distance = element['distance']['text']
            return f"{duration_in_traffic} ({distance})"
        return "⚠️ Maps Data Unavailable"
    except Exception as e:
        return f"❌ Google API Error: {str(e)}"

def scrape_fl511_incidents():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(FL511_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Look for Monroe/Key West specific alerts
        alerts = soup.find_all(string=lambda t: t and ("Monroe" in t or "Key West" in t or "US-1" in t))
        
        if alerts:
            # Return the first 2 unique alerts to keep it concise
            return " | ".join(list(set([a.strip() for a in alerts[:2]])))
        return "✅ No major incidents reported on US-1."
    except:
        return "⚠️ FL511 Scraper Offline"

def main():
    traffic = get_google_maps_traffic()
    incidents = scrape_fl511_incidents()
    
    print(f"--- KEY WEST TRAFFIC REPORT ---")
    print(f"🚗 COMMUTE: {traffic}")
    print(f"🚨 ALERTS: {incidents}")

if __name__ == "__main__":
    main()
