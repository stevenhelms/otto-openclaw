import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from otto_utils import get_cruise_ship_count


def main():
    count = get_cruise_ship_count()
    date_str = datetime.now().strftime("%A, %B %d")

    print("--- 🚢 KEY WEST PORT STATUS ---")
    print(f"Date: {date_str}")
    print(f"Ships in Port: {count}")

    if count >= 2:
        print("Crowd Level: Busy (Typical for March)")
        print(
            "\n🐢 Otto's Advice: Duval Street will be a shell-to-shell crawl. "
            "Stick to the neighborhood spots or the quiet side of the island "
            "until the 'Great Migration' back to the ships at 4:00 PM."
        )
    else:
        print("Crowd Level: Moderate")
        print("\n🐢 Otto's Advice: Currents are clear! It's a great day to cruise through Old Town.")


if __name__ == "__main__":
    main()
