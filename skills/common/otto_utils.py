"""
otto_utils.py — Shared utility helpers for OpenClaw skills.

Each skill script imports from this module by inserting the common
directory into sys.path at the top of the script:

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))
    from otto_utils import ...
"""

import json
import requests
from bs4 import BeautifulSoup


# ---------------------------------------------------------------------------
# Cruise Ship Count
# ---------------------------------------------------------------------------

def get_cruise_ship_count() -> int:
    """
    Scrapes the City of Key West cruise-ship calendar and returns the
    number of ships in port today. Falls back to 1 if the scrape fails.

    NOTE: The calendar currently requires advanced HTML table parsing to
    reliably extract today's ships. The placeholder returns 2 (typical for
    peak season) until that parser is implemented.
    """
    url = "https://www.cityofkeywest-fl.gov/543/Cruise-Ship-Calendar"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            # TODO: Parse the calendar table for today's date to get a real count.
            return 2  # Simulated — typical for March peak season
    except Exception:
        pass
    return 1  # Fallback


# ---------------------------------------------------------------------------
# FL511 Monroe County Incidents
# ---------------------------------------------------------------------------

FL511_URL = "https://fl511.com/List/Alerts"
_FL511_HEADERS = {"User-Agent": "Mozilla/5.0 (KeyWestOtto/1.0)"}


def get_fl511_incidents() -> str:
    """
    Scrapes FL511 for active Monroe County / US-1 / Key West incidents.
    Returns a human-readable status string.
    """
    try:
        res = requests.get(FL511_URL, headers=_FL511_HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        alerts = soup.find_all(
            string=lambda t: t and ("Monroe" in t or "Key West" in t or "US-1" in t)
        )
        if alerts:
            unique = list(set(a.strip() for a in alerts[:2]))
            return " | ".join(unique)
        return "✅ No major incidents reported on US-1."
    except Exception:
        return "⚠️ FL511 Scraper Offline"


# ---------------------------------------------------------------------------
# JSON File Persistence
# ---------------------------------------------------------------------------

def load_json_file(path: str) -> list | dict:
    """
    Loads and returns JSON from *path*. Returns an empty list if the file
    does not exist or cannot be parsed.
    """
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_json_file(path: str, data: list | dict, indent: int = 2) -> None:
    """Serialises *data* to *path* as JSON."""
    with open(path, "w") as f:
        json.dump(data, f, indent=indent)
