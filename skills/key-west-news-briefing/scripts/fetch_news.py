import requests
from bs4 import BeautifulSoup
import warnings
from bs4 import XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

MAX_LENGTH=300

def fetch_rss(url, limit=5):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.find_all('item')
        return [i.title.text.replace('<![CDATA[', '').replace(']]>', '').strip() for i in items[:limit]]
    except Exception as e:
        return [f"Error fetching {url}: {e}"]

def main():
    # Prioritizing International, then National/General
    sources = {
        "🌍 International (BBC/Reuters)": "http://feeds.bbci.co.uk/news/world/rss.xml",
        "🇺🇸 National & Trending (AP/Google)": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
        "🦅 Trump Tracker (X/Google Bridge)": "https://news.google.com/rss/search?q=when:24h+Trump+site:twitter.com+OR+site:x.com&hl=en-US&gl=US&ceid=US:en"
    }
    
    report = "--- 🗞️ MORNING NEWS BRIEFING ---\n"
    for category, url in sources.items():
        headlines = fetch_rss(url)
        if headlines:
            report += f"\n**{category}:**\n"
            for h in headlines:
                clean_h = (h[:MAX_LENGTH-3] + '...') if len(h) > MAX_LENGTH else h
                report += f"  - {clean_h}\n"
    
    print(report)

if __name__ == "__main__":
    main()
