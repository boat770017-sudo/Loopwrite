"""
backend/main.py — FastAPI REST API for Loopwrite.

Exposes a single endpoint:
  POST /api/generate  →  { content: str }

The LLM provider is swapped entirely via the LLM_PROVIDER env var;
no changes to this file are needed when switching providers.
"""

from __future__ import annotations

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

from llm_client import generate, LLMError
from prompts import get_prompt

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Loopwrite API",
    description="AI content generation for creators",
    version="1.0.0",
)

# CORS — restrict to your frontend URL in production via ALLOWED_ORIGINS env var
_raw_origins = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = [o.strip() for o in _raw_origins.split(",")] if _raw_origins != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------

class GenerateRequest(BaseModel):
    topic: str
    platform: str
    content_type: str
    tone: str
    variation_seed: int | None = None  # optional — ensures different output on Regenerate

    @field_validator("topic")
    @classmethod
    def topic_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Topic cannot be empty.")
        return v.strip()


class GenerateResponse(BaseModel):
    content: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health")
def health() -> dict:
    """Health check — used by Render's health check path."""
    return {"status": "ok", "service": "loopwrite-api"}


@app.post("/api/generate", response_model=GenerateResponse)
def generate_content(req: GenerateRequest) -> GenerateResponse:
    """
    Generate platform-specific content using the configured LLM provider.
    """
    try:
        system_prompt, user_prompt = get_prompt(
            req.platform,
            req.content_type,
            req.topic,
            req.tone,
        )
        # Append a hidden seed comment when regenerating to guarantee variation
        if req.variation_seed:
            user_prompt += f"\n\n<!-- variation: {req.variation_seed} -->"

        result = generate(user_prompt, system_prompt)
        return GenerateResponse(content=result)

    except LLMError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error — please try again. Details: {exc}",
        )
