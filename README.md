# humanity-through-ai
Humanity Through AI — a daily AI-curated art + reflection archive powered by free tooling: GitHub Pages (hosting) + GitHub Actions (automation) + RSS (news) + Pollinations.ai (art) + optional Hugging Face Inference API (text summaries/notes).

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

- `.github/workflows/daily.yml` — runs daily at 00:00 America/Los_Angeles (midnight Pacific), DST-aware, executes the pipeline and commits results
- `scripts/` — Python utilities for archiving, fetching news, summarizing, writing curator note, generating art (with graceful fallbacks), building the site, generating archive pages, and updating the sitemap/manifest
- `site/index.html` — the public site. It reads `site/manifest.json` to render the latest entry and archive
- `site/manifest.json` — append-only list of entries, most-recent first
- `site/entries/` — images and texts per day
- `data/` — ephemeral inputs (latest RSS headlines, etc.)

## Daily Flow

At 00:00 America/Los_Angeles daily (and on manual trigger):

1. `scripts/archive_previous_day.py` creates a static HTML snapshot of the prior day under `site/entries/<YYYY-MM-DD>.html`
2. `scripts/fetch_news.py` pulls top headlines via Google News RSS for Pacific “yesterday”
3. `scripts/curator_note.py`
   - Summarizes headlines (optional: Hugging Face `facebook/bart-large-cnn`, with graceful fallback)
   - Generates a short curator reflection (optional: Hugging Face `mistral-7b-instruct`, with graceful fallback)
   - Writes a markdown note for the day under `site/entries/<YYYY-MM-DD>.md`
4. `scripts/generate_art.py` generates AI art using Pollinations.ai (free, no token required), with retry and a seeded generative SVG fallback; if `HF_TOKEN` is present it may attempt HF image models as a last resort
5. `scripts/build_site.py` updates `site/manifest.json` (adds today’s record at the top) and refreshes `site/entries/latest.png` for social share
6. `scripts/generate_archive_pages.py` generates standalone archive pages at the site root: `/YYYY-MM-DD.html` (improves SEO and shareability)
7. `scripts/update_sitemap.py` refreshes `sitemap.xml`
8. Changes are committed and pushed by the workflow; GitHub Pages serves the updated site

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

- You can open the project in any editor and simply open `site/index.html` in a browser to preview. It loads the current `site/manifest.json` and renders entries.
- To run the full pipeline locally (mirrors CI order):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/archive_previous_day.py
python scripts/fetch_news.py
python scripts/curator_note.py
python scripts/generate_art.py
python scripts/build_site.py
python scripts/generate_archive_pages.py
python scripts/update_sitemap.py
```

This creates/updates today’s entry, refreshes `site/manifest.json`, generates `/YYYY-MM-DD.html` pages, and updates `sitemap.xml`.

## Next Steps (you)

1) Push this repo to GitHub
2) Enable GitHub Pages (Settings → Pages → Source: main / root)
3) Add custom domain in Pages; copy DNS records to GoDaddy and save
4) (Optional) Add Actions secret `HF_TOKEN` (from Hugging Face) for improved summaries/notes
5) Trigger the workflow once to generate the first entry immediately:
   - GitHub UI: Actions → “Daily Humanity Reflection” → Run workflow
   - Or CLI: `gh workflow run daily.yml` (requires `gh auth login`)
6) Visit your domain — the homepage shows the latest reflection; the archive links populate daily

## Requirements

- Python 3.9+ (CI uses 3.11)
- Dependencies listed in `requirements.txt`

## Schedule and Time Zone

- Runs at 12:00 AM America/Los_Angeles every day, across DST.
- Implementation uses dual UTC crons (07:00, 08:00) plus a PT midnight guard so it only executes at local midnight.

## Archive Pages

- Static snapshots in `site/entries/YYYY-MM-DD.html` (used by the site’s Archive UI today).
- Standalone SEO-friendly pages at the site root: `/YYYY-MM-DD.html` (generated by `scripts/generate_archive_pages.py`). These can be linked directly (e.g., https://ashwinirao.com/2025-10-05.html).

## Notes

- This project is intentionally lightweight and free-friendly. You can later swap models, styles, and hosting without changing the public interface (`site/manifest.json`).

