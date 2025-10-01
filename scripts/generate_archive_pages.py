#!/usr/bin/env python3
"""
Generate individual HTML archive pages for each day's content.
Each day gets its own standalone HTML file (e.g., 2025-10-01.html).
"""
import os
import json
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(ROOT, "site", "manifest.json")
SITE_DIR = os.path.join(ROOT, "site")


def load_manifest():
    """Load the site manifest."""
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return {"entries": []}
    return {"entries": []}


def generate_archive_html(entry):
    """Generate a complete HTML page for a single day's entry."""
    date = entry.get("date", "")
    title = entry.get("title", "Daily Reflection")
    image = entry.get("image", "")
    topics = entry.get("topics", {})
    
    # Format date nicely
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%B %d, %Y")
    except:
        formatted_date = date
    
    # Build topics HTML
    topics_html = ""
    for topic_name, topic_data in topics.items():
        summary = topic_data.get("summary", "")
        links = topic_data.get("links", [])
        
        links_html = ""
        for link in links[:5]:  # Top 5 links
            link_title = link.get("title", "")
            link_url = link.get("link", "")
            link_source = link.get("source", "")
            
            if link_url and link_title:
                links_html += f'''
          <div class="news-link">
            <a href="{link_url}" target="_blank" rel="noopener noreferrer">
              {link_title}
            </a>
            <span class="source">{link_source}</span>
          </div>
'''
        
        topics_html += f'''
      <div class="topic-card">
        <h3>{topic_name.capitalize()}</h3>
        <p class="topic-summary">{summary}</p>
        <div class="news-links">
{links_html}
        </div>
      </div>
'''
    
    # Generate complete HTML
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  
  <!-- Primary Meta Tags -->
  <title>{title} — {formatted_date} | Humanity Through AI</title>
  <meta name="title" content="{title} — {formatted_date} | Humanity Through AI" />
  <meta name="description" content="AI-curated daily reflection on humanity's collective experience from {formatted_date}. Covering world politics, health, entertainment, sports, and technology." />
  <meta name="keywords" content="AI news, daily reflection, humanity, world politics, health news, technology, sports, entertainment, AI art" />
  <meta name="author" content="Ashwini Rao" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://ashwinirao.com/{date}.html" />
  
  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="article" />
  <meta property="og:url" content="https://ashwinirao.com/{date}.html" />
  <meta property="og:title" content="{title} — {formatted_date}" />
  <meta property="og:description" content="AI-curated daily reflection on humanity's collective experience from {formatted_date}." />
  <meta property="og:image" content="https://ashwinirao.com/{image}" />
  <meta property="og:site_name" content="Humanity Through AI" />
  <meta property="article:published_time" content="{date}T12:00:00Z" />
  <meta property="article:author" content="Ashwini Rao" />
  
  <!-- Twitter -->
  <meta property="twitter:card" content="summary_large_image" />
  <meta property="twitter:url" content="https://ashwinirao.com/{date}.html" />
  <meta property="twitter:title" content="{title} — {formatted_date}" />
  <meta property="twitter:description" content="AI-curated daily reflection from {formatted_date}." />
  <meta property="twitter:image" content="https://ashwinirao.com/{image}" />
  
  <!-- Google Analytics 4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-JDB770NX2L"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-JDB770NX2L', {{
      'anonymize_ip': true,
      'send_page_view': true
    }});
  </script>
  
  <!-- Structured Data -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{title}",
    "datePublished": "{date}T12:00:00Z",
    "dateModified": "{date}T12:00:00Z",
    "author": {{
      "@type": "Person",
      "name": "Ashwini Rao",
      "url": "https://www.linkedin.com/in/ashwini-rao-091490102/"
    }},
    "publisher": {{
      "@type": "Person",
      "name": "Ashwini Rao"
    }},
    "description": "AI-curated daily reflection on humanity's collective experience from {formatted_date}",
    "image": "https://ashwinirao.com/{image}",
    "url": "https://ashwinirao.com/{date}.html",
    "mainEntityOfPage": {{
      "@type": "WebPage",
      "@id": "https://ashwinirao.com/{date}.html"
    }}
  }}
  </script>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --serif: 'Playfair Display', Georgia, serif;
      --sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      --bg-dark: #0a0a0a;
      --bg-card: #111;
      --text-primary: #f5f5f5;
      --text-secondary: #999;
      --text-muted: #666;
      --accent: #fff;
      --border: rgba(255,255,255,0.08);
    }}
    
    * {{ box-sizing: border-box; }}
    
    html, body {{
      height: 100%;
      margin: 0;
      padding: 0;
      background: var(--bg-dark);
      color: var(--text-primary);
      font-family: var(--sans);
      overflow-x: hidden;
      scroll-behavior: smooth;
    }}
    
    body {{
      display: flex;
      flex-direction: column;
      font-size: 16px;
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }}

    header {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(10, 10, 10, 0.95);
      backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--border);
      padding: 1.5rem 2rem;
    }}
    
    .header-content {{
      max-width: 1800px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    
    h1 {{
      font-family: var(--serif);
      font-size: 1.75rem;
      font-weight: 600;
      margin: 0;
      letter-spacing: -0.02em;
      color: var(--accent);
    }}
    
    h1 a {{
      color: inherit;
      text-decoration: none;
    }}
    
    .tagline {{
      font-size: 0.875rem;
      color: var(--text-muted);
      font-weight: 300;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }}

    .art-container {{
      position: relative;
      width: 100%;
      min-height: 85vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem;
      background: linear-gradient(180deg, #0a0a0a 0%, #121212 100%);
    }}
    
    .art-wrapper {{
      position: relative;
      max-width: 1800px;
      width: 100%;
      margin: 0 auto;
    }}
    
    #art {{
      width: 100%;
      height: auto;
      max-height: 90vh;
      object-fit: contain;
      border-radius: 4px;
      box-shadow: 
        0 0 80px rgba(0,0,0,0.5),
        0 20px 60px rgba(0,0,0,0.8);
    }}

    .content {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 4rem 2rem;
    }}
    
    .headline {{
      font-family: var(--serif);
      font-size: 3rem;
      font-weight: 700;
      line-height: 1.2;
      margin: 0 0 1rem 0;
      letter-spacing: -0.03em;
      color: var(--accent);
      max-width: 900px;
    }}
    
    .date {{
      font-size: 0.875rem;
      color: var(--text-muted);
      letter-spacing: 0.1em;
      text-transform: uppercase;
      margin-bottom: 3rem;
      font-weight: 500;
    }}

    .topics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 2rem;
      margin-top: 4rem;
    }}
    
    .topic-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 2rem;
      transition: all 0.3s ease;
    }}
    
    .topic-card:hover {{
      border-color: rgba(255,255,255,0.15);
      transform: translateY(-2px);
    }}
    
    .topic-card h3 {{
      font-family: var(--serif);
      font-size: 1.5rem;
      margin: 0 0 1rem 0;
      color: var(--accent);
      text-transform: capitalize;
    }}
    
    .topic-summary {{
      color: var(--text-secondary);
      font-size: 0.95rem;
      line-height: 1.6;
      margin-bottom: 1.5rem;
    }}
    
    .news-links {{
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }}
    
    .news-link {{
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }}
    
    .news-link a {{
      color: var(--text-primary);
      text-decoration: none;
      font-size: 0.95rem;
      line-height: 1.4;
      transition: color 0.2s;
    }}
    
    .news-link a:hover {{
      color: var(--accent);
    }}
    
    .source {{
      font-size: 0.8rem;
      color: var(--text-muted);
    }}

    footer {{
      margin-top: auto;
      padding: 3rem 2rem;
      text-align: center;
      border-top: 1px solid var(--border);
      background: var(--bg-dark);
    }}
    
    footer p {{
      margin: 0.5rem 0;
      color: var(--text-muted);
      font-size: 0.9rem;
    }}
    
    footer a {{
      color: var(--text-secondary);
      text-decoration: none;
      transition: color 0.2s;
    }}
    
    footer a:hover {{
      color: var(--accent);
    }}

    @media (max-width: 768px) {{
      .headline {{
        font-size: 2rem;
      }}
      
      .topics {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="header-content">
      <h1><a href="/">Humanity Through AI</a></h1>
      <div class="tagline">Archive · {formatted_date}</div>
    </div>
  </header>

  <div class="art-container">
    <div class="art-wrapper">
      <img id="art" src="{image}" alt="AI-generated art for {formatted_date}" />
    </div>
  </div>

  <div class="content">
    <h2 class="headline">{title}</h2>
    <div class="date">{formatted_date}</div>
    
    <div class="topics">
{topics_html}
    </div>
  </div>

  <footer>
    <p>Crafted with curiosity by <a href="https://www.linkedin.com/in/ashwini-rao-091490102/" target="_blank" rel="noopener noreferrer">Ashwini Rao</a></p>
    <p>This blog is AI-written, but imagined by a human who believes in the power of reflection.</p>
    <p><a href="/">← Back to today</a></p>
  </footer>
</body>
</html>'''
    
    return html


def main():
    """Generate HTML archive pages for all entries."""
    manifest = load_manifest()
    entries = manifest.get("entries", [])
    
    if not entries:
        print("⚠️  No entries found in manifest")
        return
    
    generated = 0
    for entry in entries:
        date = entry.get("date", "")
        if not date:
            continue
        
        # Generate HTML
        html = generate_archive_html(entry)
        
        # Save to file
        filename = f"{date}.html"
        filepath = os.path.join(SITE_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        
        generated += 1
        print(f"✅ Generated {filename}")
    
    print(f"\n🎉 Total archive pages generated: {generated}")


if __name__ == "__main__":
    main()
