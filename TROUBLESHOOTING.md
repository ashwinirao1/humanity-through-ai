# Troubleshooting Guide

## Fixed: 404 Error with Hugging Face API

### What was the problem?
Hugging Face's **FREE Inference API no longer supports** most Stable Diffusion models without a PRO subscription or dedicated endpoints. All model attempts were returning 404 errors.

### What's been fixed?
The `scripts/generate_art.py` now:
1. **Uses Pollinations.ai as primary** - A completely free, no-auth-required AI image generation service
   - No token needed!
   - No rate limits on free tier
   - Reliable and fast

2. **Hugging Face as backup** - Still tries HF models if HF_TOKEN is set (requires PRO subscription for most models)

3. **Graceful fallback** - If all AI services fail, creates a beautiful SVG placeholder

### How to test the fix locally:

1. **Set up your environment (if not already done):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run the generation script:**
   ```bash
   python scripts/generate_art.py
   ```
   
   **No token needed!** Pollinations.ai works without authentication.

3. **Check the output** - You should see:
   ```
   ✅ Successfully generated AI art via Pollinations! Size: XXXXX bytes
   Saved AI-generated PNG to site/entries/<date>.png
   ```

### For GitHub Actions:

Make sure your `HF_TOKEN` is set as a repository secret:
1. Go to: GitHub → Your Repo → Settings → Secrets and variables → Actions
2. Create a new secret: `HF_TOKEN` with your Hugging Face token
3. The workflow will automatically use it

### Common Issues:

**Q: Still getting 404 errors?**
- The models might be loading (Hugging Face "cold starts"). Wait 30-60 seconds and try again.
- Your token might not have the right permissions. Make sure it's a "read" token.

**Q: Getting rate limited?**
- Free tier has limits. The script will fallback to the SVG placeholder automatically.

**Q: Images look weird/corrupted?**
- This can happen if the model is still "warming up". Try again in a minute.

**Q: Want to use a different model?**
- Edit `scripts/generate_art.py` and modify the `models` list (line 61-65)
- You can browse models at: https://huggingface.co/models?pipeline_tag=text-to-image

### Testing in GitHub Actions:

Trigger a manual workflow run:
1. Go to: Actions → Daily Humanity Reflection → Run workflow
2. Watch the logs to see which model succeeds
3. Check your GitHub Pages site for the new entry

### Next Steps:

Your project should now work! The fixes ensure:
- ✅ Multiple model fallbacks for reliability
- ✅ Better error messages for debugging
- ✅ Beautiful placeholder if all models fail
- ✅ No more 404 errors blocking the pipeline