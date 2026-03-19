import os
import googlemaps
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# CONFIGURATION
API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
HOME_ADDR = '30 Kingfisher Ln, Key West, FL 33040' 
WORK_ADDR = 'Florida Keys Aqueduct Authority, 1100 Kennedy Dr, Key West, FL 33040'

# FL511 Monroe County Alerts (Key West)
FL511_URL = "https://fl511.com/List/Alerts"

def get_commute_estimates():
    if not API_KEY:
        return {"car": "⚠️ Data Unavailable", "bike": "⚠️ Data Unavailable"}
    
    gmaps = googlemaps.Client(key=API_KEY)
    now = datetime.now()
    results = {}
    
    try:
        # Get Driving Estimate
        matrix_drive = gmaps.distance_matrix(HOME_ADDR, WORK_ADDR, 
                                            mode="driving", 
                                            departure_time=now)
        
        drive_element = matrix_drive['rows'][0]['elements'][0]
        if drive_element['status'] == 'OK':
            duration = drive_element.get('duration_in_traffic', drive_element['duration'])['text']
            distance = drive_element['distance']['text']
            results['car'] = f"{duration} ({distance})"
        else:
            results['car'] = "⚠️ Driving Data Unavailable"

        # Get Biking Estimate
        # Note: Biking doesn't support 'departure_time' for traffic, but provides a steady base time
        matrix_bike = gmaps.distance_matrix(HOME_ADDR, WORK_ADDR, mode="bicycling")
        bike_element = matrix_bike['rows'][0]['elements'][0]
        if bike_element['status'] == 'OK':
            results['bike'] = bike_element['duration']['text']
        else:
            results['bike'] = "⚠️ Biking Data Unavailable"
            
    except Exception as e:
        results['error'] = str(e)
        
    return results

def scrape_fl511_incidents():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(FL511_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        alerts = soup.find_all(string=lambda t: t and ("Monroe" in t or "Key West" in t or "US-1" in t))
        if alerts:
            return " | ".join(list(set([a.strip() for a in alerts[:2]])))
        return "✅ No major incidents reported on US-1."
    except:
        return "⚠️ FL511 Scraper Offline"

def main():
    estimates = get_commute_estimates()
    incidents = scrape_fl511_incidents()
    
    print(f"--- KEY WEST COMMUTE REPORT ---")
    print(f"🚗 CAR: {estimates.get('car', 'Error')}")
    print(f"🚲 BIKE: {estimates.get('bike', 'Error')}")
    print(f"🚨 ALERTS: {incidents}")
    
    if 'error' in estimates:
        print(f"\n❌ Note: {estimates['error']}")

if __name__ == "__main__":
    main()
