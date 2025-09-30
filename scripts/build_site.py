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


def main():
    os.makedirs(os.path.join(SITE_DIR, "entries"), exist_ok=True)
    manifest_path = os.path.join(SITE_DIR, "manifest.json")
    manifest = load_manifest(manifest_path)

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

    # Build a minimal entry; topics can be enriched later in pipeline
    entry = {
        "date": today,
        "title": "A day of fragile hope amidst voices rising",
        "image": img_rel,
        "note": md_rel if os.path.exists(os.path.join(SITE_DIR, md_rel)) else "",
        "topics": {
            "health": {"summary": "", "links": []},
            "politics": {"summary": "", "links": []},
            "entertainment": {"summary": "", "links": []},
        },
    }

    # Remove existing entry for today if present, then insert at top
    manifest["entries"] = [e for e in manifest.get("entries", []) if e.get("date") != today]
    manifest["entries"].insert(0, entry)

    save_manifest(manifest_path, manifest)
    print(f"Updated manifest at {manifest_path}")


if __name__ == "__main__":
    main()


