#!/usr/bin/env python3
"""
Generate sitemap.xml with proper ISO 8601 date formatting for Google Search Console.
"""
import os
import datetime
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP_PATH = os.path.join(ROOT, "sitemap.xml")
MANIFEST_PATH = os.path.join(ROOT, "site", "manifest.json")


def load_manifest():
    """Load the site manifest to get all entry dates."""
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return {"entries": []}
    return {"entries": []}


def generate_sitemap():
    """Generate a sitemap.xml file with all site URLs."""
    manifest = load_manifest()
    
    # Current timestamp in ISO 8601 format
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    
    # Start building the sitemap
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Main page (highest priority)
    sitemap_content += '  <url>\n'
    sitemap_content += '    <loc>https://ashwinirao.com/</loc>\n'
    sitemap_content += f'    <lastmod>{now}</lastmod>\n'
    sitemap_content += '    <changefreq>daily</changefreq>\n'
    sitemap_content += '    <priority>1.0</priority>\n'
    sitemap_content += '  </url>\n'
    
    # Site index page
    sitemap_content += '  <url>\n'
    sitemap_content += '    <loc>https://ashwinirao.com/site/index.html</loc>\n'
    sitemap_content += f'    <lastmod>{now}</lastmod>\n'
    sitemap_content += '    <changefreq>daily</changefreq>\n'
    sitemap_content += '    <priority>0.9</priority>\n'
    sitemap_content += '  </url>\n'
    
    # Add archive entries (if any)
    # These are lower priority but still important for SEO
    for entry in manifest.get("entries", [])[:30]:  # Include up to 30 most recent entries
        entry_date = entry.get("date", "")
        if entry_date:
            # Convert date to ISO 8601 with time
            try:
                date_obj = datetime.datetime.strptime(entry_date, "%Y-%m-%d")
                lastmod = date_obj.strftime("%Y-%m-%dT12:00:00+00:00")
            except:
                lastmod = now
            
            # Add entry to sitemap (these would be archive pages when you create them)
            # For now, they point to the main page with fragment
            sitemap_content += '  <url>\n'
            sitemap_content += f'    <loc>https://ashwinirao.com/#{entry_date}</loc>\n'
            sitemap_content += f'    <lastmod>{lastmod}</lastmod>\n'
            sitemap_content += '    <changefreq>weekly</changefreq>\n'
            sitemap_content += '    <priority>0.6</priority>\n'
            sitemap_content += '  </url>\n'
    
    # Close the sitemap
    sitemap_content += '</urlset>\n'
    
    # Write to file
    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    
    print(f"✅ Generated sitemap.xml with {len(manifest.get('entries', [])) + 2} URLs")
    print(f"   Main pages: 2")
    print(f"   Archive entries: {min(len(manifest.get('entries', [])), 30)}")


if __name__ == "__main__":
    generate_sitemap()
