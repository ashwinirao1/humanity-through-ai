#!/usr/bin/env python3
"""
Archive yesterday's page as a static HTML snapshot.
Instead of copying the dynamic index.html (which re-fetches manifest),
we render a standalone page from the manifest entry so archives are immutable.
"""
import os
import json
from datetime import date, timedelta
from datetime import datetime as dt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES_DIR = os.path.join(ROOT, "site", "entries")
MANIFEST_PATH = os.path.join(ROOT, "site", "manifest.json")


def load_latest_entry():
    if not os.path.exists(MANIFEST_PATH):
        return None
    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        entries = manifest.get("entries", [])
        return entries[0] if entries else None
    except Exception:
        return None


def render_archive_html(entry: dict) -> str:
    date_str = entry.get("date", "")
    title = entry.get("title", "Daily Reflection")
    topics = entry.get("topics", {})

    # Resolve image relative to /site/entries
    image_rel = entry.get("image", "")  # e.g., entries/YYYY-MM-DD.png
    # When served from /site/entries/DATE.html, use just DATE.png
    image_file = f"{date_str}.png"
    if image_rel.endswith(".svg"):
        image_file = f"{date_str}.svg"

    try:
        d = dt.strptime(date_str, "%Y-%m-%d")
        formatted_date = d.strftime("%B %d, %Y")
    except Exception:
        formatted_date = date_str

    def topic_block():
        blocks = []
        for topic_name, topic_data in topics.items():
            summary = topic_data.get("summary", "")
            links = topic_data.get("links", [])
            link_divs = []
            for link in links[:5]:
                t = link.get("title"); u = link.get("link"); s = link.get("source", "")
                if t and u:
                    link_divs.append(
                        f"""
          <div class=\"news-link\">
            <a href=\"{u}\" target=\"_blank\" rel=\"noopener noreferrer\">{t}</a>
            <span class=\"source\">{s}</span>
          </div>
                        """
                    )
            blocks.append(
                f"""
      <div class=\"topic-card\">
        <h3>{topic_name.capitalize()}</h3>
        <p class=\"topic-summary\">{summary}</p>
        <div class=\"news-links\">{''.join(link_divs)}</div>
      </div>
                """
            )
        return "\n".join(blocks)

    html = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\" />
  <title>{title} — {formatted_date} | Humanity Through AI</title>
  <meta name=\"description\" content=\"AI-curated reflection from {formatted_date}.\" />
  <meta property=\"og:type\" content=\"article\" />
  <meta property=\"og:url\" content=\"https://ashwinirao.com/site/entries/{date_str}.html\" />
  <meta property=\"og:title\" content=\"{title} — {formatted_date}\" />
  <meta property=\"og:description\" content=\"AI-curated daily reflection on humanity's collective experience from {formatted_date}.\" />
  <meta property=\"og:image\" content=\"https://ashwinirao.com/site/entries/{image_file}\" />
  <meta property=\"og:site_name\" content=\"Humanity Through AI\" />
  <meta property=\"article:published_time\" content=\"{date_str}T12:00:00Z\" />
  <meta property=\"article:author\" content=\"Ashwini Rao\" />
  <meta property=\"twitter:card\" content=\"summary_large_image\" />
  <meta property=\"twitter:image\" content=\"https://ashwinirao.com/site/entries/{image_file}\" />
  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
  <link href=\"https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap\" rel=\"stylesheet\">
  <style>
    :root {{ --serif: 'Playfair Display', Georgia, serif; --sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; --bg-dark: #0a0a0a; --bg-card: #111; --text-primary: #f5f5f5; --text-secondary: #999; --text-muted: #666; --accent: #fff; --border: rgba(255,255,255,0.08); }}
    * {{ box-sizing: border-box; }} html, body {{ height: 100%; margin: 0; padding: 0; background: var(--bg-dark); color: var(--text-primary); font-family: var(--sans); }}
    header {{ position: sticky; top: 0; z-index: 100; background: rgba(10,10,10,0.95); backdrop-filter: blur(20px); border-bottom: 1px solid var(--border); padding: 1.5rem 2rem; }}
    .header-content {{ max-width: 1800px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }}
    h1 {{ font-family: var(--serif); font-size: 1.75rem; font-weight: 600; margin: 0; letter-spacing: -0.02em; color: var(--accent); }}
    h1 a {{ color: inherit; text-decoration: none; }} .tagline {{ font-size: 0.875rem; color: var(--text-muted); text-transform: uppercase; }}
    .art-container {{ position: relative; width: 100%; min-height: 70vh; display: flex; align-items: center; justify-content: center; padding: 2rem; background: linear-gradient(180deg, #0a0a0a 0%, #121212 100%); }}
    .art-wrapper {{ position: relative; max-width: 1800px; width: 100%; margin: 0 auto; }}
    #art {{ width: 100%; height: auto; max-height: 80vh; object-fit: contain; border-radius: 4px; box-shadow: 0 0 80px rgba(0,0,0,0.5), 0 20px 60px rgba(0,0,0,0.8); }}
    .content {{ max-width: 1400px; margin: 0 auto; padding: 3rem 2rem; }}
    .headline {{ font-family: var(--serif); font-size: 2.5rem; font-weight: 700; color: var(--accent); margin: 0 0 1rem 0; }}
    .date {{ font-size: 0.875rem; color: var(--text-muted); letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 2rem; }}
    .topics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2rem; }}
    .topic-card {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 1.75rem; }}
    .topic-card h3 {{ font-family: var(--serif); font-size: 1.25rem; margin: 0 0 1rem 0; color: var(--accent); }}
    .topic-summary {{ color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1rem; }}
    .news-link a {{ color: var(--text-primary); text-decoration: none; }}
    .news-link .source {{ font-size: 0.8rem; color: var(--text-muted); margin-left: 0.5rem; }}
    footer {{ margin-top: auto; padding: 3rem 2rem; text-align: center; border-top: 1px solid var(--border); background: var(--bg-dark); }}
  </style>
</head>
<body>
  <header>
    <div class=\"header-content\">
      <h1><a href=\"/\">Humanity Through AI</a></h1>
      <div class=\"tagline\">Archive · {formatted_date}</div>
    </div>
  </header>

  <div class=\"art-container\">
    <div class=\"art-wrapper\">
      <img id=\"art\" src=\"{image_file}\" alt=\"AI-generated art for {formatted_date}\" />
    </div>
  </div>

  <div class=\"content\">
    <h2 class=\"headline\">{title}</h2>
    <div class=\"date\">{formatted_date}</div>
    <div class=\"topics\">{topic_block()}</div>
  </div>

  <footer>
    <p>Crafted with curiosity by <a href=\"https://www.linkedin.com/in/ashwini-rao-091490102/\" target=\"_blank\" rel=\"noopener noreferrer\">Ashwini Rao</a></p>
    <p>This blog is AI-written, but imagined by a human who believes in the power of reflection.</p>
    <p><a href=\"/\">← Back to today</a></p>
  </footer>
</body>
</html>"""
    return html


def main():
    entry = load_latest_entry()
    if not entry:
        print("⚠️  No current entry found in manifest - skipping archive")
        return

    current_date = entry.get("date")
    if not current_date:
        print("⚠️  Current entry missing date - skipping archive")
        return

    os.makedirs(ENTRIES_DIR, exist_ok=True)
    archive_path = os.path.join(ENTRIES_DIR, f"{current_date}.html")

    html = render_archive_html(entry)
    with open(archive_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Archived {current_date} to site/entries/{current_date}.html (static snapshot)")


if __name__ == "__main__":
    main()
