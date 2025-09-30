#!/bin/bash
# Test script for AI art generation

echo "🎨 Testing Humanity Through AI - Art Generation"
echo "================================================"
echo ""

# Check if HF_TOKEN is set
if [ -z "$HF_TOKEN" ]; then
    echo "⚠️  HF_TOKEN is not set!"
    echo ""
    echo "Please set your Hugging Face token:"
    echo "  export HF_TOKEN='your_token_here'"
    echo ""
    echo "You can get a token from: https://huggingface.co/settings/tokens"
    exit 1
fi

echo "✅ HF_TOKEN is set (${#HF_TOKEN} characters)"
echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    echo "⚠️  No virtual environment found. Run:"
    echo "  python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "Running art generation script..."
echo "================================"
python scripts/generate_art.py

echo ""
echo "✅ Done! Check site/entries/ for the generated image."