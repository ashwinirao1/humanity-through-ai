import datetime
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
    if not HF_HEADERS:
        return placeholder_png_bytes()
    try:
        resp = requests.post(
            "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5",
            headers=HF_HEADERS,
            json={"inputs": prompt},
            timeout=120,
        )
        if resp.ok and resp.content:
            return resp.content
    except Exception:
        pass
    return placeholder_png_bytes()


def main():
    today = datetime.date.today().isoformat()
    md_path = os.path.join(SITE_DIR, "entries", f"{today}.md")
    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            note_text = f.read()
    else:
        note_text = "Abstract artwork representing today's mood and themes."

    prompt = (
        "Abstract digital painting representing today's mood: "
        + note_text[:400]
    )
    img_bytes = try_generate(prompt)

    os.makedirs(os.path.join(SITE_DIR, "entries"), exist_ok=True)
    
    # Save as SVG if it's our placeholder, PNG if it's from Hugging Face
    if img_bytes.startswith(b'<?xml') or img_bytes.startswith(b'<svg'):
        out_path = os.path.join(SITE_DIR, "entries", f"{today}.svg")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(img_bytes.decode('utf-8'))
    else:
        out_path = os.path.join(SITE_DIR, "entries", f"{today}.png")
        with open(out_path, "wb") as f:
            f.write(img_bytes)
    
    print(f"Wrote image to {out_path}")


if __name__ == "__main__":
    main()


