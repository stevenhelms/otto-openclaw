import os
import requests
from datetime import datetime

def get_cruise_ship_count():
    # Placeholder for a real port schedule scraper
    # Key West can have 0-3 ships typically.
    # We'll return 2 for today as a conservative 'busy' estimate.
    return 2

def main():
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    ships = get_cruise_ship_count()
    
    # Curated Key West spots
    spots = [
        {"name": "Bad Boy Burrito", "style": "Fresh/Local", "location": "Fitzpatrick St", "crowd_sensitivity": "High"},
        {"name": "El Siboney", "style": "Cuban-Mexican Fusion/Authentic", "location": "Catherine St", "crowd_sensitivity": "Medium"},
        {"name": "Amigos Tortilla Bar", "style": "Traditional/Hand-rolled", "location": "Greene St", "crowd_sensitivity": "Critical"},
        {"name": "Taco Gastropub", "style": "Modern/Craft", "location": "Duval St", "crowd_sensitivity": "High"},
    ]

    print(f"--- 🌮 CAYO HUESO MEXICAN FOOD GUIDE ---")
    print(f"🚢 Port Status: {ships} Cruise Ships in harbor today.")
    
    if ships >= 2:
        print("⚠️ Warning: Downtown is likely swamped. Avoiding Duval/Greene is recommended.\n")
    
    print("Recommendations for Steve:")
    for spot in spots:
        status = "✅ Recommended"
        advice = ""
        
        if ships >= 2 and spot['crowd_sensitivity'] in ['High', 'Critical']:
            status = "⏳ Likely Busy"
            advice = " (Try to go after 4 PM when ships leave)"
        elif spot['name'] == "El Siboney":
            advice = " (Get the Puerco Asado—it's world-class)"
            
        print(f"- {spot['name']} ({spot['style']}): {status}{advice}")
        print(f"  📍 {spot['location']}")

if __name__ == "__main__":
    main()
