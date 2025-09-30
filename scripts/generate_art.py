import datetime
import json
import os
import base64
import requests


HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.join(ROOT, "site")


def create_svg_placeholder() -> bytes:
    # Create a beautiful SVG placeholder
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 700">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#764ba2;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#f093fb;stop-opacity:1" />
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="30%" r="40%">
      <stop offset="0%" style="stop-color:#ffffff;stop-opacity:0.3" />
      <stop offset="100%" style="stop-color:#ffffff;stop-opacity:0" />
    </radialGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#bg)"/>
  <circle cx="300" cy="200" r="150" fill="url(#glow)" opacity="0.6"/>
  <circle cx="900" cy="500" r="200" fill="url(#glow)" opacity="0.4"/>
  <path d="M0,400 Q300,200 600,400 T1200,400 L1200,700 L0,700 Z" fill="rgba(255,255,255,0.1)"/>
  <text x="600" y="350" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="48" font-weight="bold" opacity="0.9">Humanity Through AI</text>
  <text x="600" y="400" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="24" opacity="0.7">Daily Reflection</text>
</svg>'''
    return svg_content.encode('utf-8')

def placeholder_png_bytes() -> bytes:
    # Return SVG bytes instead of tiny PNG
    return create_svg_placeholder()


def try_generate(prompt: str) -> bytes:
    # Enhanced prompt for better AI art generation
    enhanced_prompt = (
        f"Digital art painting, {prompt}, "
        "vibrant colors, emotional depth, artistic composition, "
        "representing human experience and global events, "
        "high quality, detailed, modern art style"
    )
    
    print(f"Attempting AI art generation with prompt: {enhanced_prompt[:150]}...")
    
    try:
        # Use Pollinations.ai - a free, no-auth-required AI image service
        # This is more reliable than Hugging Face's free tier which has many restrictions
        print("Attempting AI art generation via Pollinations.ai...")
        
        # Pollinations.ai offers free image generation via simple URL
        import urllib.parse
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        pollinations_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=700&nologo=true"
        
        print(f"Fetching image from: {pollinations_url[:100]}...")
        resp = requests.get(
            pollinations_url,
            timeout=60,
        )
        
        if resp.ok and resp.content and len(resp.content) > 1000:
            print(f"✅ Successfully generated AI art via Pollinations! Size: {len(resp.content)} bytes")
            return resp.content
        else:
            print(f"❌ Pollinations generation failed: {resp.status_code}")
            
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
    return placeholder_png_bytes()


def main():
    today = datetime.date.today().isoformat()
    
    # Read news data to create a better prompt
    news_path = os.path.join(ROOT, "data", "today_news.json")
    if os.path.exists(news_path):
        with open(news_path, "r", encoding="utf-8") as f:
            news_data = json.load(f)
        headlines = [item.get("title", "") for item in news_data.get("items", [])[:3]]
        news_context = " ".join(headlines)
    else:
        news_context = "Global news and events shaping humanity's daily experience"
    
    # Read curator note for emotional context
    md_path = os.path.join(SITE_DIR, "entries", f"{today}.md")
    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            note_text = f.read()
    else:
        note_text = "A day of reflection on humanity's journey through time."

    # Create a rich prompt combining news and emotional context
    prompt = (
        f"Create abstract digital art representing today's human experience. "
        f"News context: {news_context[:200]}. "
        f"Emotional tone: {note_text[:200]}. "
        f"Style: modern abstract, emotional, representing global humanity's mood and feelings."
    )
    
    print(f"Generating AI art with prompt: {prompt[:150]}...")
    img_bytes = try_generate(prompt)

    os.makedirs(os.path.join(SITE_DIR, "entries"), exist_ok=True)
    
    # Save as SVG if it's our placeholder, PNG if it's from Hugging Face
    if img_bytes.startswith(b'<?xml') or img_bytes.startswith(b'<svg'):
        out_path = os.path.join(SITE_DIR, "entries", f"{today}.svg")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(img_bytes.decode('utf-8'))
        print(f"Saved SVG placeholder to {out_path}")
    else:
        out_path = os.path.join(SITE_DIR, "entries", f"{today}.png")
        with open(out_path, "wb") as f:
            f.write(img_bytes)
        print(f"Saved AI-generated PNG to {out_path}")


if __name__ == "__main__":
    main()


