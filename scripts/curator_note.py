import datetime
import json
import os
import textwrap
import requests


HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
SITE_DIR = os.path.join(ROOT, "site")


def summarize_text_fallback(text: str) -> str:
    text = text.strip().replace("\n", " ")
    if len(text) <= 220:
        return text
    return text[:200].rsplit(" ", 1)[0] + "…"


def hf_summarize(text: str) -> str:
    if not HF_HEADERS:
        return summarize_text_fallback(text)
    try:
        resp = requests.post(
            "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
            headers=HF_HEADERS,
            json={"inputs": text},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list) and data and "summary_text" in data[0]:
            return data[0]["summary_text"]
    except Exception:
        pass
    return summarize_text_fallback(text)


def hf_generate(prompt: str) -> str:
    if not HF_HEADERS:
        return textwrap.fill(
            "Today’s humanity felt conflicted yet hopeful. Storms reminded us of fragility, "
            "but breakthroughs lit sparks of resilience.", 80
        )
    try:
        resp = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
            headers=HF_HEADERS,
            json={"inputs": prompt, "parameters": {"max_new_tokens": 120}},
            timeout=90,
        )
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list) and data and "generated_text" in data[0]:
            return data[0]["generated_text"]
    except Exception:
        pass
    return textwrap.fill(
        "Across borders and bright screens, voices carried both worry and resolve. "
        "We leaned toward each other, sketching a softer horizon.", 80
    )


def target_date_from_news() -> str:
    """Use date from today_news.json or fallback to yesterday."""
    news_path = os.path.join(DATA_DIR, "today_news.json")
    if os.path.exists(news_path):
        try:
            with open(news_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            d = data.get("date")
            if d:
                return d
        except Exception:
            pass
    return (datetime.date.today() - datetime.timedelta(days=1)).isoformat()


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(os.path.join(SITE_DIR, "entries"), exist_ok=True)

    # Align with content date (yesterday in PT)
    target_date = target_date_from_news()

    news_path = os.path.join(DATA_DIR, "today_news.json")
    if os.path.exists(news_path):
        with open(news_path, "r", encoding="utf-8") as f:
            news_data = json.load(f)
    else:
        news_data = {"topics": {}}

    # Build a compact headline string from the topic structure
    titles = []
    for tkey in ["politics", "health", "entertainment", "sports", "technology"]:
        for item in news_data.get("topics", {}).get(tkey, [])[:1]:
            t = item.get("title")
            if t:
                titles.append(t)
    headlines = "; ".join(titles) or "Global headlines spanning health, politics, culture, sports, and technology."

    summary = hf_summarize(headlines)
    prompt = (
        f"Yesterday's news ({target_date}): {summary}. Write 3 sentences as a museum curator "
        f"describing how humanity felt, in an artistic tone."
    )
    note = hf_generate(prompt)

    md_path = os.path.join(SITE_DIR, "entries", f"{target_date}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# {target_date}\n\n**Summary:** {summary}\n\n{note}\n")

    print(f"Wrote curator note to {md_path}")


if __name__ == "__main__":
    main()


