# Loopwrite — AI Content Generator for Creators

> Generate captions, video scripts, hashtags, blog ideas, and marketing copy
> for Instagram, YouTube, LinkedIn, and X — powered by free LLM APIs.

---

## Features

- **4 platforms** — Instagram · YouTube · LinkedIn · X (Twitter)
- **5 content types** — Caption · Video Script · Hashtags · Blog Idea · Marketing Copy
- **6 tones** — Casual · Professional · Funny · Inspirational · Bold · Expert
- **3 free LLM providers** — Groq · Gemini · OpenRouter (swap via one env var)
- Copy-to-clipboard, word & character counter, Regenerate button
- Monochrome UI (black / white / gray — no color accents)
- One-click deploy to **Render**

---

## Getting a Free API Key

Pick one provider and grab a free key:

| Provider | Sign-up | Free Tier |
|----------|---------|-----------|
| **Groq** (recommended — fastest) | https://console.groq.com | Generous RPM/TPM limits on Llama 3 |
| **Google Gemini** | https://aistudio.google.com | Free tier via AI Studio |
| **OpenRouter** | https://openrouter.ai | Pool of `:free` tagged models |

---

## Local Setup

```bash
# 1. Clone
git clone https://github.com/your-username/loopwrite.git
cd loopwrite

# 2. Virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Dependencies
pip install -r requirements.txt

# 4. Configure env vars
cp .env.example .env
# Open .env and fill in your chosen API key, e.g.:
#   LLM_PROVIDER=groq
#   GROQ_API_KEY=gsk_xxxxxxxxxxxx

# 5. Run
streamlit run app.py
```

The app opens at **http://localhost:8501** by default.

---

## Switching Providers

Edit `.env` — no code changes needed:

```bash
# Use Groq (default)
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_...

# Use Gemini
LLM_PROVIDER=gemini
GOOGLE_API_KEY=AIza...

# Use OpenRouter
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-...
```

---

## Deploy to Render

1. Push this repo to GitHub.
2. Go to [render.com](https://render.com) → **New → Blueprint** → connect your repo.
   Render will detect `render.yaml` automatically.
3. In the **Environment** tab of your Render service, add your API key:
   - `GROQ_API_KEY` (or `GOOGLE_API_KEY` / `OPENROUTER_API_KEY`)
4. Hit **Deploy** — the app will be live at your `.onrender.com` URL.

> **Never commit `.env`** — it's in `.gitignore`. Add secrets directly in the
> Render dashboard under **Environment → Secret Files** or **Environment Variables**.

---

## Project Structure

```
loopwrite/
├── app.py              # Streamlit UI entrypoint
├── llm_client.py       # Provider abstraction (Groq / Gemini / OpenRouter)
├── prompts.py          # Prompt templates per platform × content type
├── config.py           # Color tokens, env vars, constants
├── requirements.txt
├── render.yaml         # Render deployment manifest
├── .env.example        # Template — copy to .env and fill in keys
├── .gitignore
├── .streamlit/
│   └── config.toml     # Streamlit theme (monochrome dark)
└── README.md
```

---

## Env Var Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `groq` | Active provider: `groq` \| `gemini` \| `openrouter` |
| `GROQ_API_KEY` | — | Groq API key |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Override Groq model |
| `GOOGLE_API_KEY` | — | Gemini API key |
| `GEMINI_MODEL` | `gemini-1.5-flash` | Override Gemini model |
| `OPENROUTER_API_KEY` | — | OpenRouter API key |
| `OPENROUTER_MODEL` | `meta-llama/llama-3.2-3b-instruct:free` | Override OpenRouter model |

---

## License

MIT
