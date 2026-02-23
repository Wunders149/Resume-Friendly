# 🤖 CV Forge - Free AI Setup Guide

## Quick Start: Use FREE AI for Resume Parsing

CV Forge supports multiple **FREE** AI options for intelligent resume parsing:

---

## Option 1: Google Gemini (Recommended - Free Tier)

**Best for:** Most users, easy setup, good accuracy

### Setup Steps:
1. **Get Free API Key:**
   - Go to: https://makersuite.google.com/app/apikey
   - Sign in with Google account
   - Click "Create API Key"
   - Copy the key

2. **Configure CV Forge:**
   - Run CV Forge
   - Upload a resume
   - When asked about AI parsing, click "Yes"
   - Enter your Gemini API key when prompted

### Limits:
- **Free:** 1,500 requests/day
- **Model:** gemini-1.5-flash (fast, efficient)

---

## Option 2: Hugging Face (Free)

**Best for:** Open-source models, no installation

### Setup Steps:
1. **Get Free API Key:**
   - Go to: https://huggingface.co/settings/tokens
   - Sign up/login
   - Click "New Token"
   - Name it "CV Forge"
   - Select "Read" permission
   - Copy the token

2. **Configure CV Forge:**
   - Set environment variable:
     ```
     set AI_API_KEY=your_token_here
     set AI_PROVIDER=huggingface
     ```
   - Or configure in app settings

### Limits:
- Free tier has rate limits
- Model: Mistral-7B-Instruct (good quality)

---

## Option 3: Ollama (Local/Free - Best Privacy)

**Best for:** Privacy, unlimited use, offline

### Setup Steps:
1. **Install Ollama:**
   - Download from: https://ollama.ai/
   - Install on your computer

2. **Download Model:**
   ```bash
   ollama pull llama3.2
   ```

3. **Run CV Forge:**
   - AI parsing will auto-detect Ollama
   - No API key needed!

### Limits:
- **None!** Completely free and unlimited
- Runs on your computer (needs 4GB+ RAM)

---

## Option 4: LM Studio (Local/Free)

**Best for:** Trying different models locally

### Setup Steps:
1. **Install LM Studio:**
   - Download from: https://lmstudio.ai/
   - Install and open

2. **Download a Model:**
   - Search for "llama" or "mistral"
   - Download a 7B model

3. **Start Local Server:**
   - Click "Start Server" in LM Studio

4. **Run CV Forge:**
   - Will auto-detect LM Studio

---

## Comparison Table

| Provider | Cost | Setup | Quality | Limits |
|----------|------|-------|---------|--------|
| **Gemini** | Free | Easy (2 min) | ⭐⭐⭐⭐ | 1500/day |
| **Hugging Face** | Free | Easy (3 min) | ⭐⭐⭐ | Rate limited |
| **Ollama** | Free | Medium (10 min) | ⭐⭐⭐⭐ | None |
| **LM Studio** | Free | Medium (15 min) | ⭐⭐⭐⭐ | None |
| **OpenAI** | Paid | Easy | ⭐⭐⭐⭐⭐ | Paid |

---

## Quick Test

After setup, test AI parsing:

1. Open CV Forge
2. Click "📁 Choose Document"
3. Select your resume (PDF/Word)
4. Click "Yes" for AI parsing
5. Review extracted information!

---

## Troubleshooting

### "AI not available" message:
- Check internet connection (for cloud APIs)
- Verify API key is correct
- For local AI: ensure Ollama/LM Studio is running

### "Rate limit exceeded":
- Wait a few minutes and try again
- Switch to local AI (Ollama) for unlimited use

### "Invalid API key":
- Double-check you copied the full key
- For Gemini: make sure API is enabled
- For Hugging Face: ensure token has "Read" permission

---

## Recommended Setup

**For most users:** Use **Google Gemini** (free tier)
- Easy setup
- Good accuracy  
- 1500 free requests/day is plenty for personal use

**For privacy/advanced users:** Use **Ollama** (local)
- Completely private
- Unlimited use
- Works offline

---

## Need Help?

1. Check this guide first
2. Try a different AI provider
3. Fall back to standard (non-AI) parsing - still works great!
