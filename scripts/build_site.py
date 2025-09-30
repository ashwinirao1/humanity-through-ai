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
    """Load categorized news from the curator script"""
    categorized_path = os.path.join(ROOT, "data", "categorized_news.json")
    if os.path.exists(categorized_path):
        with open(categorized_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"health": [], "politics": [], "entertainment": []}

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

def main():
    os.makedirs(os.path.join(SITE_DIR, "entries"), exist_ok=True)
    manifest_path = os.path.join(SITE_DIR, "manifest.json")
    
    # Start fresh - only keep today's entry
    manifest = {"entries": []}

    today = datetime.date.today().isoformat()
    
    # Check for both PNG and SVG files
    img_png = f"entries/{today}.png"
    img_svg = f"entries/{today}.svg"
    md_rel = f"entries/{today}.md"
    
    # Use whichever image file exists
    if os.path.exists(os.path.join(SITE_DIR, img_png)):
        img_rel = img_png
    elif os.path.exists(os.path.join(SITE_DIR, img_svg)):
        img_rel = img_svg
    else:
        img_rel = ""

    # Load categorized news
    categorized_news = load_categorized_news()
    
    # Generate topic summaries and links
    topics = {}
    for topic_name in ["health", "politics", "entertainment"]:
        topic_news = categorized_news.get(topic_name, [])
        topics[topic_name] = {
            "summary": generate_topic_summary(topic_news, topic_name),
            "links": topic_news[:5]  # Top 5 links per topic
        }

    # Build today's entry
    entry = {
        "date": today,
        "title": "A day of fragile hope amidst voices rising",
        "image": img_rel,
        "note": md_rel if os.path.exists(os.path.join(SITE_DIR, md_rel)) else "",
        "topics": topics,
    }

    # Add today's entry to the manifest
    manifest["entries"].insert(0, entry)

    save_manifest(manifest_path, manifest)
    print(f"Updated manifest at {manifest_path} with fresh archive starting from {today}")


if __name__ == "__main__":
    main()


