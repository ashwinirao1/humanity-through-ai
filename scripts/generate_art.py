import datetime
import json
import os
import base64
import requests


HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.join(ROOT, "site")


def target_date_from_news() -> str:
    """Get the target content date from data/today_news.json (yesterday, in PT).
    Falls back to yesterday based on system date if file missing.
    """
    news_path = os.path.join(ROOT, "data", "today_news.json")
    if os.path.exists(news_path):
        try:
            with open(news_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                d = data.get("date")
                if d:
                    return d
        except Exception:
            pass
    # Fallback: yesterday
    return (datetime.date.today() - datetime.timedelta(days=1)).isoformat()


def create_generative_art(seed_date: str) -> bytes:
    """Create beautiful, unique generative SVG art using seed_date for determinism."""
    import random
    import hashlib
    
    # Use the target content date as seed for consistent daily art
    seed = int(hashlib.md5(seed_date.encode()).hexdigest()[:8], 16)
    random.seed(seed)
    
    # Color palettes inspired by famous artists
    palettes = [
        # Rothko-inspired
        ['#8B4513', '#DC143C', '#FF8C00', '#4B0082'],
        # Kandinsky-inspired  
        ['#1E3A8A', '#DC2626', '#FBBF24', '#059669'],
        # Picasso blue period
        ['#1E40AF', '#3B82F6', '#60A5FA', '#93C5FD'],
        # Abstract expressionism
        ['#991B1B', '#B91C1C', '#DC2626', '#F87171'],
        # Mondrian-inspired
        ['#000000', '#EF4444', '#3B82F6', '#FBBF24']
    ]
    palette = random.choice(palettes)
    
    # Generate abstract shapes
    shapes = []
    num_shapes = random.randint(5, 12)
    
    for i in range(num_shapes):
        shape_type = random.choice(['circle', 'rect', 'ellipse', 'polygon'])
        color = random.choice(palette)
        opacity = random.uniform(0.3, 0.85)
        
        if shape_type == 'circle':
            cx = random.randint(0, 1200)
            cy = random.randint(0, 700)
            r = random.randint(50, 300)
            shapes.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="{opacity}"/>')
        
        elif shape_type == 'rect':
            x = random.randint(-200, 1200)
            y = random.randint(-200, 700)
            w = random.randint(100, 600)
            h = random.randint(100, 400)
            rotate = random.randint(0, 45)
            shapes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" opacity="{opacity}" transform="rotate({rotate} {x+w//2} {y+h//2})"/>')
        
        elif shape_type == 'ellipse':
            cx = random.randint(0, 1200)
            cy = random.randint(0, 700)
            rx = random.randint(80, 350)
            ry = random.randint(50, 250)
            shapes.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{color}" opacity="{opacity}"/>')
        
        else:  # polygon
            points = []
            num_points = random.randint(3, 6)
            for _ in range(num_points):
                px = random.randint(0, 1200)
                py = random.randint(0, 700)
                points.append(f"{px},{py}")
            points_str = " ".join(points)
            shapes.append(f'<polygon points="{points_str}" fill="{color}" opacity="{opacity}"/>')
    
    # Create gradient background
    bg_colors = random.sample(palette, 2)
    
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 700" style="background: linear-gradient(135deg, {bg_colors[0]}22 0%, {bg_colors[1]}22 100%);">
  <defs>
    <filter id="blur">
      <feGaussianBlur in="SourceGraphic" stdDeviation="2" />
    </filter>
  </defs>
  <rect width="100%" height="100%" fill="#0a0a0a" opacity="0.4"/>
  {chr(10).join(shapes)}
  <rect width="100%" height="100%" fill="url(#overlay)" opacity="0.1"/>
</svg>'''
    return svg_content.encode('utf-8')

def create_svg_placeholder(seed_date: str) -> bytes:
    # Use generative art instead of static placeholder
    return create_generative_art(seed_date)

def placeholder_png_bytes(seed_date: str) -> bytes:
    # Return SVG bytes instead of tiny PNG
    return create_svg_placeholder(seed_date)


def try_generate(prompt: str) -> bytes:
    # Transform the prompt into deeply artistic, abstract expression
    # Inspired by masters: Picasso's cubism, da Vinci's composition, Rothko's emotion, Kandinsky's abstraction
    import random
    
    artistic_styles = [
        "abstract expressionism",
        "cubist fragmentation",
        "surrealist dreamscape",
        "color field painting",
        "neo-impressionist"
    ]
    chosen_style = random.choice(artistic_styles)
    
    # Simplified prompt for URL encoding - Pollinations has length limits
    # Keep the artistic essence but make it concise
    enhanced_prompt = (
        f"Fine art {chosen_style}: humanity's emotions, "
        f"abstract symbolic forms, golden ratio composition, "
        f"Rothko color depth, Kandinsky spirituality, "
        f"chiaroscuro lighting, museum quality"
    )
    
    print(f"Attempting AI art generation with prompt: {enhanced_prompt[:150]}...")
    

    try:
        # Use Pollinations.ai - a free, no-auth-required AI image service
        print("Attempting AI art generation via Pollinations.ai...")
        
        import urllib.parse
        
        # Try with full prompt first
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        pollinations_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=700&nologo=true"
        
        print(f"Fetching image from Pollinations (attempt 1)...")
        try:
            resp = requests.get(pollinations_url, timeout=60)
            if resp.ok and resp.content and len(resp.content) > 1000:
                print(f"✅ Successfully generated AI art via Pollinations! Size: {len(resp.content)} bytes")
                return resp.content
        except Exception as e:
            print(f"Attempt 1 failed: {e}")
        
        # Retry with simpler prompt
        simple_prompt = f"{chosen_style} abstract art humanity"
        encoded_simple = urllib.parse.quote(simple_prompt)
        simple_url = f"https://image.pollinations.ai/prompt/{encoded_simple}?width=1200&height=700"
        
        print(f"Retrying with simpler prompt (attempt 2)...")
        try:
            resp = requests.get(simple_url, timeout=60)
            if resp.ok and resp.content and len(resp.content) > 1000:
                print(f"✅ Successfully generated AI art via Pollinations! Size: {len(resp.content)} bytes")
                return resp.content
        except Exception as e:
            print(f"Attempt 2 failed: {e}")
        
        print("❌ All Pollinations attempts failed")
            
        # Fallback: Try Hugging Face models (requires PRO or may not work)
        if HF_HEADERS:
            print("\nTrying Hugging Face as backup...")
            models = [
                "stabilityai/stable-diffusion-2-1",
                "CompVis/stable-diffusion-v1-4",
            ]
            
            for model in models:
                try:
                    print(f"Trying model: {model}")
                    resp = requests.post(
                        f"https://api-inference.huggingface.co/models/{model}",
                        headers=HF_HEADERS,
                        json={"inputs": enhanced_prompt},
                        timeout=120,
                    )
                    if resp.ok and resp.content and len(resp.content) > 1000:
                        print(f"✅ Successfully connected to {model}")
                        return resp.content
                    else:
                        print(f"❌ Model {model} returned {resp.status_code}")
                        if resp.text:
                            print(f"  Error: {resp.text[:200]}")
                except Exception as e:
                    print(f"❌ Error with {model}: {e}")
                    continue
    except Exception as e:
        print(f"❌ AI generation error: {e}")
    
    print("Falling back to placeholder image")
    # Will be replaced by caller with seeded placeholder
    return b""


def main():
    # Align art date with news/content date (yesterday in PT)
    target_date = target_date_from_news()
    
    # Read news data to create a better prompt
    news_path = os.path.join(ROOT, "data", "today_news.json")
    news_context = "Global news and events shaping humanity's daily experience"
    if os.path.exists(news_path):
        try:
            with open(news_path, "r", encoding="utf-8") as f:
                news_data = json.load(f)
            # Gather a few top titles across topics
            titles = []
            topics = news_data.get("topics", {})
            for tkey in ["politics", "health", "entertainment", "sports", "technology"]:
                for item in topics.get(tkey, [])[:1]:  # take top 1 from each topic
                    title = item.get("title")
                    if title:
                        titles.append(title)
            if titles:
                news_context = " ".join(titles)[:400]
        except Exception:
            pass
    
    # Read curator note for emotional context
    md_path = os.path.join(SITE_DIR, "entries", f"{target_date}.md")
    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            note_text = f.read()
    else:
        note_text = "A day of reflection on humanity's journey through time."

    # Create a rich prompt combining news and emotional context
    prompt = (
        f"Create abstract digital art representing humanity's experience on {target_date}. "
        f"News context: {news_context[:200]}. "
        f"Emotional tone: {note_text[:200]}. "
        f"Style: modern abstract, emotional, representing global humanity's mood and feelings."
    )
    
    print(f"Generating AI art with prompt: {prompt[:150]}...")
    img_bytes = try_generate(prompt)

    os.makedirs(os.path.join(SITE_DIR, "entries"), exist_ok=True)
    
    # If generation failed fully, use our seeded placeholder SVG
    if not img_bytes:
        img_bytes = create_svg_placeholder(target_date)
    
    # Save as SVG if it's our placeholder, PNG if it's from models
    if img_bytes.startswith(b'<?xml') or img_bytes.startswith(b'<svg'):
        out_path = os.path.join(SITE_DIR, "entries", f"{target_date}.svg")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(img_bytes.decode('utf-8'))
        print(f"Saved SVG placeholder to {out_path}")
    else:
        out_path = os.path.join(SITE_DIR, "entries", f"{target_date}.png")
        with open(out_path, "wb") as f:
            f.write(img_bytes)
        print(f"Saved AI-generated PNG to {out_path}")


if __name__ == "__main__":
    main()

