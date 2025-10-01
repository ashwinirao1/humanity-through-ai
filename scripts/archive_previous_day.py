#!/usr/bin/env python3
"""
Archive the current index.html to site/entries/ before generating new content.
This preserves yesterday's content as a complete HTML snapshot.
"""
import os
import shutil
import json
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, "index.html")
ENTRIES_DIR = os.path.join(ROOT, "site", "entries")
MANIFEST_PATH = os.path.join(ROOT, "site", "manifest.json")


def get_current_date_from_manifest():
    """Get the current date from manifest (what's currently showing on the site)."""
    if os.path.exists(MANIFEST_PATH):
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                manifest = json.load(f)
                entries = manifest.get("entries", [])
                if entries and len(entries) > 0:
                    return entries[0].get("date")
        except:
            pass
    return None


def main():
    """Archive the current index.html to site/entries/."""
    
    # Get the date that's currently displayed
    current_date = get_current_date_from_manifest()
    
    if not current_date:
        print("⚠️  No current date found in manifest - this might be the first run")
        print("   Skipping archive (nothing to archive yet)")
        return
    
    # Check if index.html exists
    if not os.path.exists(INDEX_PATH):
        print("⚠️  index.html not found - nothing to archive")
        return
    
    # Create entries directory if it doesn't exist
    os.makedirs(ENTRIES_DIR, exist_ok=True)
    
    # Archive filename
    archive_filename = f"{current_date}.html"
    archive_path = os.path.join(ENTRIES_DIR, archive_filename)
    
    # Check if archive already exists
    if os.path.exists(archive_path):
        print(f"ℹ️  Archive for {current_date} already exists, skipping")
        return
    
    # Copy index.html to archive
    shutil.copy2(INDEX_PATH, archive_path)
    print(f"✅ Archived {current_date} content to {archive_filename}")
    print(f"   Path: site/entries/{archive_filename}")


if __name__ == "__main__":
    main()
