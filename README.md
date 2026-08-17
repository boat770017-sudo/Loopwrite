# Loopwrite — AI Content Generator for Creators

> Generate captions, video scripts, hashtags, blog ideas, and marketing copy
> for Instagram, YouTube, LinkedIn, and X — powered by free LLM APIs.

**Stack:** Next.js 14 (frontend) · FastAPI Python (backend) · Groq / Gemini / OpenRouter (LLM)

---

## Features

- **4 platforms** — Instagram · YouTube · LinkedIn · X (Twitter)
- **5 content types** — Caption · Video Script · Hashtags · Blog Idea · Marketing Copy
- **6 tones** — Casual · Professional · Funny · Inspirational · Bold · Expert
- **3 free LLM providers** — swap with one env var, no code change
- Copy-to-clipboard · word & character counter · Regenerate button
- Monochrome UI (black / white / gray — no color accents)
- Deploy-ready for **Render** (two services)

---

## Getting a Free API Key

| Provider | Sign-up | Free Tier |
|----------|---------|-----------|
| **Groq** (recommended) | https://console.groq.com | Fast inference, generous limits |
| **Google Gemini** | https://aistudio.google.com | Free via AI Studio |
| **OpenRouter** | https://openrouter.ai | Pool of `:free` tagged models |

---

## Local Setup

### 1 — Backend (FastAPI)

```bash
cd backend

python3 -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Open backend/.env and fill in your API key:
#   LLM_PROVIDER=groq
#   GROQ_API_KEY=gsk_xxxxxxxxxxxx

uvicorn main:app --reload   # runs on http://localhost:8000
```

### 2 — Frontend (Next.js)

```bash
cd frontend

npm install

cp .env.example .env.local
# .env.local already points to http://localhost:8000 — no change needed locally

npm run dev                 # runs on http://localhost:3000
```

Open **http://localhost:3000** in your browser.

---

## Switching Providers

Edit `backend/.env` — no code change needed:

```bash
# Groq (default)
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_...

# Gemini
LLM_PROVIDER=gemini
GOOGLE_API_KEY=AIza...

# OpenRouter
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-...
```

---

## Deploy to Render

### Step 1 — Push to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2 — Deploy with Blueprint

1. Go to [render.com](https://render.com) → **New → Blueprint**
2. Connect your GitHub repo — Render detects `render.yaml` automatically
3. Two services are created: `loopwrite-backend` and `loopwrite-frontend`

### Step 3 — Set environment variables

In the **`loopwrite-backend`** service dashboard → **Environment**:
| Variable | Value |
|----------|-------|
| `GROQ_API_KEY` | `gsk_xxxxxxxxxxxx` |
| `ALLOWED_ORIGINS` | `https://loopwrite-frontend.onrender.com` |

In the **`loopwrite-frontend`** service dashboard → **Environment**:
| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_API_URL` | `https://loopwrite-backend.onrender.com` |

### Step 4 — Redeploy

After setting env vars, trigger a manual redeploy on the frontend service
so `NEXT_PUBLIC_API_URL` is baked into the Next.js build.

> **Never commit `.env` files** — they're in `.gitignore`.
> Only `.env.example` files (with empty values) are committed.

---

## Project Structure

```
Loopwrite/
├── backend/                  # FastAPI Python API
│   ├── main.py               # /api/generate endpoint
│   ├── llm_client.py         # Provider abstraction (Groq/Gemini/OpenRouter)
│   ├── prompts.py            # 20 prompt templates (4 platforms × 5 content types)
│   ├── config.py             # Env vars, model names, constants
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                 # Next.js 14 app
│   ├── app/
│   │   ├── layout.tsx        # Google Fonts, global metadata
│   │   ├── page.tsx          # Main page — form + output panel
│   │   └── globals.css       # Tailwind directives + base styles
│   ├── components/
│   │   ├── GenerateForm.tsx  # Input form component
│   │   ├── OutputCard.tsx    # Output panel (empty/loading/success/error)
│   │   └── CopyButton.tsx    # Clipboard copy with feedback
│   ├── lib/
│   │   └── api.ts            # fetch wrapper → FastAPI backend
│   ├── tailwind.config.ts    # Monochrome color tokens
│   ├── .env.example
│   └── package.json
│
├── render.yaml               # Render Blueprint — two services
├── .gitignore
└── README.md
```

---

## API Reference

```
POST /api/generate
Content-Type: application/json

{
  "topic": "string",
  "platform": "Instagram | YouTube | LinkedIn | X (Twitter)",
  "content_type": "Caption | Video Script | Hashtags | Blog Idea | Marketing Copy",
  "tone": "Casual | Professional | Funny | Inspirational | Bold | Expert",
  "variation_seed": 1234   // optional — ensures variation on Regenerate
}

200 OK:  { "content": "string" }
422:     { "detail": "validation error message" }
500:     { "detail": "LLM error message" }
```

---

## License

MIT
