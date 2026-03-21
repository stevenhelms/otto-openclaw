import os
import requests
import sys
import json
from bs4 import BeautifulSoup

def search_craigslist(query, city="keys"):
    url = f"https://{city}.craigslist.org/search/sss?query={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = []
        for item in soup.select('.cl-search-result'):
            title = item.select_one('.cl-app-anchor').text.strip()
            price = item.select_one('.priceinfo').text.strip() if item.select_one('.priceinfo') else "N/A"
            link = item.select_one('.cl-app-anchor')['href']
            results.append(f"- {title} ({price}) -> {link}")
        return results[:5]
    except Exception as e:
        return [f"Error searching Craigslist: {e}"]

def get_local_knowledge():
    try:
        with open("/home/openclaw/.openclaw/workspace/scripts/local_knowledge.json", 'r') as f:
            return json.load(f)
    except:
        return {}

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "kayak"
    print(f"--- 🏝️ ISLAND EXPLORER: {query.upper()} ---")
    
    if query.lower() in ["kayak", "kayaking", "paddling", "sandbar"]:
        knowledge = get_local_knowledge()
        spots = knowledge.get("kayaking_spots", [])
        if spots:
            print("\n📍 Local Paddling Spots & Sandbars:")
            for spot in spots:
                print(f"- {spot['name']} ({spot['type']}): {spot['description']}")

    cl_results = search_craigslist(query)
    if cl_results:
        print("\n💰 Gear Deals on Craigslist (FL Keys):")
        for res in cl_results:
            print(res)
    else:
        print("\n💨 No new gear deals found on Craigslist right now.")
        print("- Tip: Check 'Island Vibe' on Eaton St for e-bike/kayak leads.")

if __name__ == "__main__":
    main()
