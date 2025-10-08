import datetime
import json
import os


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.join(ROOT, "site")


def load_manifest(path: str):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return {"entries": []}
    return {"entries": []}


def save_manifest(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_categorized_news():
    """Load news from today_news.json and return date + topics"""
    news_path = os.path.join(ROOT, "data", "today_news.json")
    if os.path.exists(news_path):
        with open(news_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Return both date and topics
            return data.get("date", None), data.get("topics", {})
    return None, {}

def generate_topic_summary(topic_news, topic_name):
    """Generate a summary for a topic based on news items"""
    if not topic_news:
        return f"No {topic_name} news available today."
    
    titles = [item.get("title", "") for item in topic_news[:3]]  # Top 3 items
    summary_text = ". ".join(titles)
    
    # Simple summary generation
    if len(summary_text) > 150:
        summary_text = summary_text[:150] + "..."
    
    return summary_text


def generate_headline(categorized_news: dict, content_date: str) -> str:
    """Compose a smart, poetic, and captivating title from the day's news.
    - No trailing suffix like "Daily Reflection".
    - No ellipses; keep phrases whole and intentional.
    - Prefer narrative clauses over keyword scraps.
    """
    def clean_base(t: str) -> str:
        if not t:
            return ""
        t = t.replace("“", "").replace("”", "").replace("’", "'").strip()
        # Remove trailing source like "Title - Source"
        t = t.split(" - ")[0].strip()
        # Drop secondary parts joined with pipes or em-dashes
        t = t.split(" | ")[0].strip()
        t = t.split(" — ")[0].strip()
        # Collapse whitespace
        return " ".join(t.split())

    def short_words(s: str, max_words: int = 8) -> str:
        # Keep the first N whole words without adding ellipses
        words = s.split()
        return " ".join(words[:max_words])

    def compress_phrase(s: str, topic: str) -> str:
        base = clean_base(s)
        low = base.lower()
        # A few gentle, topic-aware rewrites to feel human
        if topic == "technology":
            if "now available" in low or "available" in low:
                subject = short_words(base, 2) or "AI"
                return f"{subject} goes global"
            if "ai" in low and "chip" in low:
                return "AI chips enter a new contest"
        if topic == "politics":
            if "peace" in low:
                return f"{short_words(base, 4)} reconsidered"
            return f"{short_words(base, 6)} debated"
        if topic == "entertainment":
            return f"{short_words(base, 6)} takes the stage"
        if topic == "health":
            if "nobel" in low or "prize" in low:
                return "Medicine's breakthroughs take a bow"
            return f"{short_words(base, 6)} reshapes care"
        if topic == "sports":
            return f"{short_words(base, 6)} in tight contests"
        return short_words(base, 6)

    # Preferred topic order influences the story arc
    topic_order = ["politics", "technology", "entertainment", "health", "sports"]

    segments = []
    for tkey in topic_order:
        items = categorized_news.get(tkey, [])
        if not items:
            continue
        headline = items[0].get("title", "")
        if headline:
            phrase = compress_phrase(headline, tkey)
            if phrase:
                segments.append(phrase)
        if len(segments) >= 4:
            break

    if not segments:
        return f"Notes from {content_date}"

    # Compose a narrative line from 2–4 segments; avoid ellipses and dull endings
    if len(segments) == 1:
        title = segments[0]
    elif len(segments) == 2:
        title = f"{segments[0]}; {segments[1]}"
    elif len(segments) == 3:
        title = f"{segments[0]}; {segments[1]}; {segments[2]}"
    else:
        title = f"{segments[0]}; {segments[1]}; {segments[2]}"

    # Safety: keep under ~100 words by trimming tokens, without ellipses
    words = title.split()
    if len(words) > 100:
        title = " ".join(words[:100])

    return title


def main():
    os.makedirs(os.path.join(SITE_DIR, "entries"), exist_ok=True)
    manifest_path = os.path.join(SITE_DIR, "manifest.json")
    
    # Load existing manifest to preserve archive
    manifest = load_manifest(manifest_path)

    # Get the date from the news data (this is the actual content date)
    news_date, categorized_news = load_categorized_news()
    
    # Use news date if available, otherwise use today
    content_date = news_date if news_date else datetime.date.today().isoformat()
    
    # Check for both PNG and SVG files using content date
    img_png = f"entries/{content_date}.png"
    img_svg = f"entries/{content_date}.svg"
    md_rel = f"entries/{content_date}.md"
    
    # Use whichever image file exists
    if os.path.exists(os.path.join(SITE_DIR, img_png)):
        img_rel = img_png
    elif os.path.exists(os.path.join(SITE_DIR, img_svg)):
        img_rel = img_svg
    else:
        img_rel = ""

    # Also refresh an easy social preview: entries/latest.png when PNG is available
    try:
        import shutil
        src_png_path = os.path.join(SITE_DIR, img_png)
        latest_png_path = os.path.join(SITE_DIR, "entries", "latest.png")
        if os.path.exists(src_png_path):
            shutil.copyfile(src_png_path, latest_png_path)
            print("✅ Updated entries/latest.png for social share preview")
    except Exception as e:
        print(f"ℹ️ Could not update latest.png: {e}")

    # Generate topic summaries and links - all 5 topics
    topics = {}
    for topic_name in ["politics", "health", "entertainment", "sports", "technology"]:
        topic_news = categorized_news.get(topic_name, [])
        if topic_news:  # Only include topics that have actual news
            topics[topic_name] = {
                "summary": generate_topic_summary(topic_news, topic_name),
                "links": topic_news[:5]  # Top 5 links per topic
            }
            print(f"✅ Added {topic_name} topic with {len(topic_news)} articles")
        else:
            print(f"⚠️  Skipping {topic_name} topic - no content")

    # Build a unique headline from today's news
    headline = generate_headline(categorized_news, content_date)

    # Build today's entry
    entry = {
        "date": content_date,
        "title": headline,
        "image": img_rel,
        "note": md_rel if os.path.exists(os.path.join(SITE_DIR, md_rel)) else "",
        "topics": topics,
    }

    # Remove existing entry with same date (update if already exists)
    manifest["entries"] = [e for e in manifest["entries"] if e.get("date") != content_date]
    
    # Add new entry at the top
    manifest["entries"].insert(0, entry)

    save_manifest(manifest_path, manifest)
    print(f"✅ Updated manifest with entry for {content_date}")
    print(f"   Total entries in archive: {len(manifest['entries'])}")


if __name__ == "__main__":
    main()


