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
    order = ["politics", "technology", "entertainment", "health", "sports"]

    def clean_base(t: str) -> str:
        if not t:
            return ""
        t = t.replace("“", "").replace("”", "").replace("’", "'").strip()
        t = t.split(" - ")[0].strip()
        t = t.split(" | ")[0].strip()
        t = t.split(" — ")[0].strip()
        return " ".join(t.split())

    def short_words(s: str, max_words: int = 8) -> str:
        return " ".join(s.split()[:max_words])

    def compress_phrase(s: str, topic: str) -> str:
        base = clean_base(s)
        low = base.lower()
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

    segments = []
    for k in order:
        items = topics.get(k, {}).get("links", [])
        if not items:
            continue
        t = items[0].get("title", "")
        if t:
            seg = compress_phrase(t, k)
            if seg:
                segments.append(seg)
        if len(segments) >= 4:
            break

    if not segments:
        return f"Notes from {entry.get('date','')}"

    if len(segments) == 1:
        title = segments[0]
    elif len(segments) == 2:
        title = f"{segments[0]}; {segments[1]}"
    elif len(segments) == 3:
        title = f"{segments[0]}; {segments[1]}; {segments[2]}"
    else:
        title = f"{segments[0]}; {segments[1]}; {segments[2]}"

    words = title.split()
    if len(words) > 100:
        title = " ".join(words[:100])

    return title


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
