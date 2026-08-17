"""
llm_client.py — Provider-agnostic LLM abstraction for Loopwrite.

Public API:
    generate(prompt: str, system: str) -> str

Swap provider by setting the LLM_PROVIDER environment variable:
    groq        → Groq API (default, free tier, very fast)
    gemini      → Google Gemini API (free tier via AI Studio)
    openrouter  → OpenRouter free model pool (OpenAI-compatible)

No other file in this project knows which provider is active.
"""

from __future__ import annotations

import os
from typing import Optional

import config


class LLMError(Exception):
    """Raised when the LLM call fails for any reason."""


# ---------------------------------------------------------------------------
# Provider implementations
# ---------------------------------------------------------------------------

def _generate_groq(prompt: str, system: str) -> str:
    """Call the Groq API using the official groq Python SDK."""
    if not config.GROQ_API_KEY:
        raise LLMError(
            "GROQ_API_KEY is not set. "
            "Get a free key at https://console.groq.com and add it to your .env file."
        )
    try:
        from groq import Groq  # type: ignore
    except ImportError:
        raise LLMError("The 'groq' package is not installed. Run: pip install groq")

    try:
        client = Groq(api_key=config.GROQ_API_KEY)
        response = client.chat.completions.create(
            model=config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=0.85,
            max_tokens=1500,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        _raise_provider_error("Groq", exc)


def _generate_gemini(prompt: str, system: str) -> str:
    """Call the Google Gemini API using the google-generativeai SDK."""
    if not config.GOOGLE_API_KEY:
        raise LLMError(
            "GOOGLE_API_KEY is not set. "
            "Get a free key at https://aistudio.google.com and add it to your .env file."
        )
    try:
        import google.generativeai as genai  # type: ignore
    except ImportError:
        raise LLMError(
            "The 'google-generativeai' package is not installed. "
            "Run: pip install google-generativeai"
        )

    try:
        genai.configure(api_key=config.GOOGLE_API_KEY)
        model = genai.GenerativeModel(
            model_name=config.GEMINI_MODEL,
            system_instruction=system,
        )
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.85,
                max_output_tokens=1500,
            ),
        )
        return response.text.strip()
    except Exception as exc:
        _raise_provider_error("Gemini", exc)


def _generate_openrouter(prompt: str, system: str) -> str:
    """Call OpenRouter using the openai-compatible SDK."""
    if not config.OPENROUTER_API_KEY:
        raise LLMError(
            "OPENROUTER_API_KEY is not set. "
            "Get a free key at https://openrouter.ai and add it to your .env file."
        )
    try:
        from openai import OpenAI  # type: ignore
    except ImportError:
        raise LLMError("The 'openai' package is not installed. Run: pip install openai")

    try:
        client = OpenAI(
            api_key=config.OPENROUTER_API_KEY,
            base_url=config.OPENROUTER_BASE_URL,
        )
        response = client.chat.completions.create(
            model=config.OPENROUTER_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=0.85,
            max_tokens=1500,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        _raise_provider_error("OpenRouter", exc)


# ---------------------------------------------------------------------------
# Error normalisation
# ---------------------------------------------------------------------------

def _raise_provider_error(provider: str, exc: Exception) -> None:
    """Translate raw provider exceptions into user-friendly LLMError messages."""
    msg = str(exc).lower()
    if "rate limit" in msg or "429" in msg:
        raise LLMError(
            f"{provider} rate limit reached. Wait a moment and try again, "
            "or switch LLM_PROVIDER in your .env file."
        )
    if "auth" in msg or "401" in msg or "invalid api key" in msg or "api_key" in msg:
        raise LLMError(
            f"{provider} authentication failed — check that your API key is correct in .env."
        )
    if "quota" in msg or "403" in msg:
        raise LLMError(
            f"{provider} quota exceeded. Check your usage at the provider dashboard "
            "or switch to another provider via LLM_PROVIDER."
        )
    if "timeout" in msg or "connection" in msg:
        raise LLMError(
            f"{provider} request timed out or lost connection. Check your internet and try again."
        )
    # Generic fallback — include the raw message for debugging
    raise LLMError(f"{provider} error: {exc}")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

_PROVIDERS: dict[str, callable] = {
    "groq": _generate_groq,
    "gemini": _generate_gemini,
    "openrouter": _generate_openrouter,
}


def generate(prompt: str, system: str) -> str:
    """
    Generate text from the configured LLM provider.

    Args:
        prompt: The user-facing instruction (content of the user turn).
        system: The system / role instruction that shapes model behaviour.

    Returns:
        The generated text as a plain string.

    Raises:
        LLMError: On any provider error (missing key, rate limit, network, etc.)
        ValueError: If LLM_PROVIDER is set to an unsupported value.
    """
    provider = config.LLM_PROVIDER
    fn = _PROVIDERS.get(provider)
    if fn is None:
        supported = ", ".join(_PROVIDERS.keys())
        raise ValueError(
            f"Unsupported LLM_PROVIDER '{provider}'. "
            f"Supported values: {supported}"
        )
    return fn(prompt, system)
