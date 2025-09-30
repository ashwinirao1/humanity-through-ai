# humanity-through-ai
Humanity Through AI — a daily AI-curated art + reflection archive powered by free tooling: GitHub Pages (hosting) + GitHub Actions (automation) + RSS (news) + Hugging Face Inference API (summaries, reflection, art).

## Quick Start (10–15 min)

1) Create a GitHub repo named `humanity-through-ai` (or any name)
2) Copy all files from this folder into your repo root
3) Enable GitHub Pages
   - Repo → Settings → Pages → Source: `main` branch, folder: `/` (root)
4) Visit `https://<your-username>.github.io/<repo-name>/` — the demo page loads immediately

Optional (for AI text summaries):
- Create a Hugging Face token and add it as a Repo Secret named `HF_TOKEN` (only needed for text summarization, NOT for image generation)
- GitHub → Repo → Settings → Secrets and variables → Actions → New repository secret → Name: `HF_TOKEN`, Value: your token
- **Note:** Image generation now uses Pollinations.ai (free, no token required)

## What’s Included

- `.github/workflows/daily.yml` — runs daily at 23:59 UTC, executes the pipeline and commits results
- `scripts/` — Python utilities for fetching news, summarizing, writing curator note, generating art (with graceful fallbacks), and updating the manifest
- `site/index.html` — the public site. It reads `site/manifest.json` to render the latest entry and archive
- `site/manifest.json` — append-only list of entries, most-recent first
- `site/entries/` — images and texts per day
- `data/` — ephemeral inputs (latest RSS headlines, etc.)

## Daily Flow

At 23:59 UTC daily (and on manual trigger):

1. `scripts/fetch_news.py` pulls top headlines via Google News RSS
2. `scripts/curator_note.py`
   - Summarizes headlines (Hugging Face `facebook/bart-large-cnn`, with fallback)
   - Generates a short curator reflection (Hugging Face `mistral-7b-instruct`, with fallback)
   - Writes a markdown note for the day under `site/entries/<YYYY-MM-DD>.md`
3. `scripts/generate_art.py` generates AI art using Pollinations.ai (free, no token required), with fallback to Hugging Face models if HF_TOKEN is set, and ultimately falls back to a beautiful SVG placeholder
4. `scripts/build_site.py` updates `site/manifest.json` (adds today’s record at the top)
5. Changes are committed and pushed by the workflow; GitHub Pages serves the updated site

If the `HF_TOKEN` is not present or the remote calls throttle/fail, the pipeline gracefully falls back to on-device summaries and a generated placeholder image, ensuring the site still updates daily.

### Paths: no hardcoded locals

All scripts compute paths relative to the repo root at runtime (no absolute paths). This makes them work in GitHub Actions and on any local machine.

## Configure Your Custom Domain (GoDaddy)

1. In your GitHub repo → Settings → Pages → add your custom domain (e.g., `example.com`)
2. GitHub will display DNS records to add:
   - A records (4 IPv4 entries) for apex domain (e.g., `@`)
   - CNAME for `www` pointing to `<username>.github.io`
3. In GoDaddy → Domain → DNS → add/verify these records
4. Wait for DNS propagation (typically minutes to a couple hours). GitHub will automatically provision HTTPS once records resolve

## Local Development

- You can open the project in Cursor (or any editor) and simply open `site/index.html` in a browser to preview. It loads the current `site/manifest.json` and renders entries.
- To run the pipeline locally:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/fetch_news.py && python scripts/curator_note.py && python scripts/generate_art.py && python scripts/build_site.py
```

This will create/update today’s entry and refresh `site/manifest.json`.

## Next Steps (you)

1) Push this repo to GitHub
2) Enable GitHub Pages (Settings → Pages → Source: main / root)
3) Add custom domain in Pages; copy DNS records to GoDaddy and save
4) Add Actions secret `HF_TOKEN` (from Hugging Face)
5) Trigger the workflow once (Actions → Daily Humanity Reflection → Run workflow) to generate the first real entry immediately
6) Visit your domain — the homepage should show today’s art/headline; the archive will grow daily

## Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`

## Notes

- This project is intentionally lightweight and free-friendly. You can later swap models, styles, and hosting without changing the public interface (`site/manifest.json`).

