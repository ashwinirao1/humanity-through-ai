import datetime
import json
import os
import feedparser


def fetch_google_news(limit: int = 5):
    rss_url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    items = []
    for entry in feed.entries[:limit]:
        items.append({
            "title": entry.title,
            "link": getattr(entry, 'link', ''),
            "source": getattr(entry, 'source', {}).get('title') if getattr(entry, 'source', None) else ''
        })
    return items


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(root, "data")
    os.makedirs(data_dir, exist_ok=True)
    items = fetch_google_news()
    today = datetime.date.today().isoformat()
    out_path = os.path.join(data_dir, "today_news.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"date": today, "items": items}, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(items)} headlines to {out_path}")


if __name__ == "__main__":
    main()


