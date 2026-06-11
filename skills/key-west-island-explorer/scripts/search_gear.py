import sys
import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))

LOCAL_KNOWLEDGE_FILE = Path("/home/openclaw/.openclaw/workspace/scripts/local_knowledge.json")
KAYAK_QUERIES = {"kayak", "kayaking", "paddling", "sandbar"}


def get_local_knowledge() -> dict:
    """Loads curated local spot data from the OpenClaw workspace, if available."""
    try:
        with open(LOCAL_KNOWLEDGE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def search_craigslist(query, city="keys"):
    """Basic Craigslist scraper for the Florida Keys."""
    url = f"https://{city}.craigslist.org/search/sss"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    try:
        r = requests.get(url, params={"query": query}, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        results = []

        for item in soup.select(".cl-search-result"):
            anchor = item.select_one(".cl-app-anchor")
            price_el = item.select_one(".priceinfo")
            if not anchor:
                continue
            title = anchor.text.strip()
            price = price_el.text.strip() if price_el else "N/A"
            link = anchor["href"]
            results.append(f"- {title} ({price}) -> {link}")

        return results[:5]
    except Exception as e:
        return [f"Error searching Craigslist: {e}"]


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "paddleboard"
    print(f"--- 🏝️ ISLAND EXPLORER: {query.upper()} ---")

    # For water activity queries, surface local knowledge first
    if query.lower() in KAYAK_QUERIES:
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
