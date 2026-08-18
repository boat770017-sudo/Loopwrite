"""
config.py — App-wide constants and environment config for Loopwrite.

Color tokens are defined here and referenced by app.py via CSS template strings.
Never hardcode hex values in the UI layer — always import from this module.
"""

from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Colour palette — monochrome only, no colour accents
# ---------------------------------------------------------------------------

ONYX = "#0E0E10"       # App background
CHARCOAL = "#1A1A1D"   # Card / input / container surfaces
SLATE = "#3A3A3F"      # Borders, dividers, disabled states
ASH = "#8B8B8F"        # Secondary / muted text, placeholders
FOG = "#E8E8EA"        # Primary body text
PAPER = "#FFFFFF"      # Headlines, primary buttons, active states

# ---------------------------------------------------------------------------
# LLM provider config
# ---------------------------------------------------------------------------

LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq").lower()

# Groq
GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# Google Gemini
GOOGLE_API_KEY: str | None = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# OpenRouter
OPENROUTER_API_KEY: str | None = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.2-3b-instruct:free")
OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

# ---------------------------------------------------------------------------
# App meta
# ---------------------------------------------------------------------------

APP_TITLE = "Loopwrite"
APP_SUBTITLE = "AI content for creators — captions, scripts, hashtags & more."

PLATFORMS: list[str] = ["Instagram", "YouTube", "LinkedIn", "X (Twitter)"]

CONTENT_TYPES: list[str] = [
    "Caption",
    "Video Script",
    "Hashtags",
    "Blog Idea",
    "Marketing Copy",
]

TONES: list[str] = [
    "Casual",
    "Professional",
    "Funny",
    "Inspirational",
    "Bold",
    "Expert",
]
