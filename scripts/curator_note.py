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


def categorize_news(news_items):
    """Categorize news items into health, politics, entertainment"""
    categories = {
        "health": [],
        "politics": [],
        "entertainment": []
    }
    
    health_keywords = ["health", "medical", "vaccine", "disease", "hospital", "doctor", "treatment", "cure", "pandemic", "healthcare"]
    politics_keywords = ["election", "government", "president", "minister", "parliament", "congress", "policy", "law", "vote", "political"]
    entertainment_keywords = ["movie", "film", "music", "celebrity", "entertainment", "show", "game", "sport", "art", "culture"]
    
    for item in news_items:
        title = item.get("title", "").lower()
        link = item.get("link", "")
        source = item.get("source", "")
        
        # Categorize based on keywords
        if any(keyword in title for keyword in health_keywords):
            categories["health"].append({"title": item.get("title", ""), "url": link, "source": source})
        elif any(keyword in title for keyword in politics_keywords):
            categories["politics"].append({"title": item.get("title", ""), "url": link, "source": source})
        elif any(keyword in title for keyword in entertainment_keywords):
            categories["entertainment"].append({"title": item.get("title", ""), "url": link, "source": source})
        else:
            # Default to politics if no clear category
            categories["politics"].append({"title": item.get("title", ""), "url": link, "source": source})
    
    return categories

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(os.path.join(SITE_DIR, "entries"), exist_ok=True)
    today = datetime.date.today().isoformat()

    news_path = os.path.join(DATA_DIR, "today_news.json")
    if os.path.exists(news_path):
        with open(news_path, "r", encoding="utf-8") as f:
            news_data = json.load(f)
    else:
        news_data = {"items": []}

    headlines = "; ".join(i.get("title", "") for i in news_data.get("items", []) if i.get("title"))
    headlines = headlines or "Global headlines spanning health, politics, and culture."

    summary = hf_summarize(headlines)
    prompt = (
        f"Today's news: {summary}. Write 3 sentences as a museum curator describing "
        f"how humanity felt today, in an artistic tone."
    )
    note = hf_generate(prompt)
    
    # Categorize news items
    categorized_news = categorize_news(news_data.get("items", []))

    md_path = os.path.join(SITE_DIR, "entries", f"{today}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# {today}\n\n**Summary:** {summary}\n\n{note}\n")
    
    # Save categorized news for the build script
    news_categories_path = os.path.join(DATA_DIR, "categorized_news.json")
    with open(news_categories_path, "w", encoding="utf-8") as f:
        json.dump(categorized_news, f, ensure_ascii=False, indent=2)
    
    print(f"Wrote curator note to {md_path}")
    print(f"Wrote categorized news to {news_categories_path}")


if __name__ == "__main__":
    main()


