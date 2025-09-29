import datetime
import os
import base64
import requests


HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.join(ROOT, "site")


def placeholder_png_bytes() -> bytes:
    # Simple tiny PNG (1x1 transparent) as absolute fallback
    return base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII="
    )


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
        note_text = "Abstract artwork representing today’s mood and themes."

    prompt = (
        "Abstract digital painting representing today’s mood: "
        + note_text[:400]
    )
    img_bytes = try_generate(prompt)

    os.makedirs(os.path.join(SITE_DIR, "entries"), exist_ok=True)
    out_path = os.path.join(SITE_DIR, "entries", f"{today}.png")
    with open(out_path, "wb") as f:
        f.write(img_bytes)
    print(f"Wrote image to {out_path}")


if __name__ == "__main__":
    main()


