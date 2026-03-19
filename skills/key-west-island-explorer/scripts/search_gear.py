import os
import requests
import sys
from bs4 import BeautifulSoup

def search_craigslist(query, city="keys"):
    """Basic Craigslist scraper for the Florida Keys."""
    url = f"https://{city}.craigslist.org/search/sss?query={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = []
        
        # Craigslist structure check (simplified for initial version)
        for item in soup.select('.cl-search-result'):
            title = item.select_one('.cl-app-anchor').text.strip()
            price = item.select_one('.priceinfo').text.strip() if item.select_one('.priceinfo') else "N/A"
            link = item.select_one('.cl-app-anchor')['href']
            results.append(f"- {title} ({price}) -> {link}")
            
        return results[:5]
    except Exception as e:
        return [f"Error searching Craigslist: {e}"]

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "paddleboard"
    print(f"--- 🏝️ ISLAND EXPLORER: {query.upper()} ---")
    
    # We'll start with Craigslist Florida Keys and build out from there
    cl_results = search_craigslist(query)
    
    if cl_results:
        print("\nFound on Craigslist (FL Keys):")
        for res in cl_results:
            print(res)
    else:
        print("\nNo immediate results found on Craigslist. Checking local shop leads...")
        # Placeholder for local shop web indexing
        print("- Tip: Check 'Island Vibe' on Eaton St for e-bike rentals/sales.")

if __name__ == "__main__":
    main()
