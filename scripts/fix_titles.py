#!/usr/bin/env python3
"""
Fix manifest titles and ordering:
- Keep only entries that have a corresponding archived HTML file in site/entries/<date>.html
- Sort entries by date (descending)
- Recompute a clearer human-readable title for the latest entry using its topics
"""
import os
import json
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.join(ROOT, "site")
ENTRIES_DIR = os.path.join(SITE_DIR, "entries")
MANIFEST_PATH = os.path.join(SITE_DIR, "manifest.json")


def load_manifest():
    if not os.path.exists(MANIFEST_PATH):
        return {"entries": []}
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return {"entries": []}


def save_manifest(data):
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def has_archive_html(date_str: str) -> bool:
    return os.path.exists(os.path.join(ENTRIES_DIR, f"{date_str}.html"))


def parse_date(s: str):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except Exception:
        return None


def base_title(t: str) -> str:
    if not t:
        return ""
    t = t.split(" - ")[0].strip()
    return " ".join(t.split())


def shorten(s: str, max_len: int = 70) -> str:
    s = s.strip()
    if len(s) <= max_len:
        return s
    cut = s[:max_len].rsplit(" ", 1)[0]
    return (cut or s[:max_len]).rstrip() + "…"


def generate_clear_title(entry: dict) -> str:
    topics = entry.get("topics", {})
    # Preferred topic order
    order = ["politics", "technology", "entertainment", "health", "sports"]
    picks = []
    for k in order:
        items = topics.get(k, {}).get("links", [])
        if items:
            t = base_title(items[0].get("title", ""))
            if t:
                picks.append(t)
    if not picks:
        return f"Daily Reflection — {entry.get('date','')}"
    selected = [shorten(s, 70) for s in picks[:3]]
    core = " • ".join(selected)
    if len(core) > 140 and len(selected) > 2:
        core = " • ".join([shorten(selected[0], 60), shorten(selected[1], 60)])
    return f"{core} — Daily Reflection"


def main():
    m = load_manifest()
    entries = m.get("entries", [])

    # Keep only entries that have an archived HTML file
    entries = [e for e in entries if e and e.get("date") and has_archive_html(e["date"]) ]

    # Sort by date descending
    entries.sort(key=lambda e: e.get("date", ""), reverse=True)

    if entries:
        # Recompute clearer title for the latest entry only
        latest = entries[0]
        latest["title"] = generate_clear_title(latest)

    save_manifest({"entries": entries})
    print(f"✅ Fixed manifest: {len(entries)} archived entries, latest = {entries[0]['date'] if entries else 'n/a'}")


if __name__ == "__main__":
    main()
