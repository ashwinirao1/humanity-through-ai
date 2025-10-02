import datetime
import json
import os
import feedparser
from datetime import datetime as dt
from zoneinfo import ZoneInfo


def fetch_topic_news(topic_query: str, limit: int = 5):
    """Fetch news for a specific topic from Google News RSS"""
    # Google News RSS with topic query
    rss_url = f"https://news.google.com/rss/search?q={topic_query}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    items = []
    for entry in feed.entries[:limit]:
        items.append({
            "title": entry.title,
            "link": getattr(entry, 'link', ''),
            "source": getattr(entry, 'source', {}).get('title') if getattr(entry, 'source', None) else ''
        })
    return items


def fetch_all_topics():
    """Fetch news across diverse topics - world politics, health, entertainment, sports, technology"""
    topics = {
        "politics": "world+politics+OR+geopolitics+OR+international+relations",
        "health": "health+OR+medicine+OR+wellness+OR+medical+breakthrough",
        "entertainment": "entertainment+OR+movies+OR+music+OR+culture+OR+arts",
        "sports": "sports+OR+athletics+OR+championship+OR+games",
        "technology": "technology+OR+innovation+OR+AI+OR+science+OR+space"
    }
    
    results = {}
    for topic_key, query in topics.items():
        print(f"Fetching {topic_key} news...")
        items = fetch_topic_news(query, limit=5)
        results[topic_key] = items
        print(f"  Found {len(items)} {topic_key} headlines")
    
    return results


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(root, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Use YESTERDAY's date in America/Los_Angeles (we reflect on the day that just ended in PT)
    now_pt = dt.now(ZoneInfo("America/Los_Angeles"))
    yesterday_pt = (now_pt.date() - datetime.timedelta(days=1)).isoformat()
    print(f"Fetching news for {yesterday_pt} (Pacific yesterday)")
    
    # Fetch diverse topic news
    topic_news = fetch_all_topics()
    
    # Save categorized news
    out_path = os.path.join(data_dir, "today_news.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "date": yesterday_pt,
            "topics": topic_news
        }, f, ensure_ascii=False, indent=2)
    
    total = sum(len(items) for items in topic_news.values())
    print(f"\n✅ Saved {total} headlines across {len(topic_news)} topics to {out_path}")


if __name__ == "__main__":
    main()


