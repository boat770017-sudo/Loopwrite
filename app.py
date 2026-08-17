"""
app.py — Streamlit entrypoint for Loopwrite.

UI follows the monochrome black/white/gray theme spec:
  - All colors come from config.py constants (never hardcoded hex)
  - Fonts: Space Grotesk (headings), Inter (body), IBM Plex Mono (tags/code)
  - Status communicated via border weight + icon + copy — never color
"""

from __future__ import annotations

import random
import time

import streamlit as st

import config
from llm_client import LLMError, generate
from prompts import get_prompt

# ---------------------------------------------------------------------------
# Page config — must be first Streamlit call
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Google Fonts + Custom CSS injection
# ---------------------------------------------------------------------------

FONTS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Space+Grotesk:wght@400;500;600;700&"
    "family=Inter:wght@300;400;500;600&"
    "family=IBM+Plex+Mono:wght@400;500&"
    "display=swap"
)

st.markdown(
    f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="{FONTS_URL}" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <style>
    /* ── Base typography ── */
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: {config.ONYX};
        color: {config.FOG};
    }}

    h1, h2, h3 {{
        font-family: 'Space Grotesk', sans-serif;
        color: {config.PAPER};
        letter-spacing: -0.02em;
    }}

    /* ── Primary buttons (Generate / Regenerate) ── */
    .stButton > button {{
        background-color: {config.PAPER};
        color: {config.ONYX};
        border: none;
        border-radius: 4px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        padding: 0.6rem 1.4rem;
        width: 100%;
        transition: background-color 0.15s ease;
    }}
    .stButton > button:hover {{
        background-color: {config.FOG};
        color: {config.ONYX};
    }}
    .stButton > button:active {{
        background-color: {config.ASH};
        color: {config.ONYX};
    }}

    /* ── Form inputs ── */
    .stTextInput input,
    .stTextArea textarea {{
        background-color: {config.CHARCOAL} !important;
        color: {config.FOG} !important;
        border: 1px solid {config.SLATE} !important;
        border-radius: 4px !important;
        font-family: 'Inter', sans-serif;
    }}
    .stTextInput input:focus,
    .stTextArea textarea:focus {{
        border-color: {config.ASH} !important;
        box-shadow: none !important;
    }}

    /* ── Selectbox ── */
    .stSelectbox > div > div {{
        background-color: {config.CHARCOAL} !important;
        color: {config.FOG} !important;
        border: 1px solid {config.SLATE} !important;
        border-radius: 4px !important;
    }}

    /* ── Labels ── */
    label, .stSelectbox label, .stTextInput label, .stTextArea label {{
        color: {config.ASH} !important;
        font-family: 'Inter', sans-serif;
        font-size: 0.82rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}

    /* ── Markdown text ── */
    [data-testid="stMarkdownContainer"] p {{
        color: {config.FOG};
        font-family: 'Inter', sans-serif;
        line-height: 1.65;
    }}

    /* ── Divider ── */
    hr {{
        border: none;
        border-top: 1px solid {config.SLATE};
        margin: 1.5rem 0;
    }}

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header {{visibility: hidden;}}
    .block-container {{
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 780px;
    }}

    /* ── Output card — base ── */
    .output-card {{
        background-color: {config.CHARCOAL};
        border: 1px solid {config.SLATE};
        border-radius: 6px;
        padding: 1.75rem 2rem;
        margin-top: 1.25rem;
        font-family: 'Inter', sans-serif;
        line-height: 1.7;
        color: {config.FOG};
        white-space: pre-wrap;
        word-break: break-word;
    }}
    /* Success state — 2px paper left border */
    .output-card.is-success {{
        border-left: 2px solid {config.PAPER};
    }}
    /* Error state — 2px paper left border */
    .output-card.is-error {{
        border-left: 2px solid {config.PAPER};
        color: {config.FOG};
        font-weight: 600;
    }}
    /* Empty state — dashed slate border, centred ash text */
    .output-card.is-empty {{
        border: 1px dashed {config.SLATE};
        color: {config.ASH};
        text-align: center;
        padding: 3rem 2rem;
    }}

    /* ── Mono tag (platform / content type labels) ── */
    .mono-tag {{
        font-family: 'IBM Plex Mono', monospace;
        color: {config.ASH};
        font-size: 0.78rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }}

    /* ── Copy button (secondary style) ── */
    .copy-btn button {{
        background-color: transparent !important;
        color: {config.ASH} !important;
        border: 1px solid {config.SLATE} !important;
        font-size: 0.82rem;
        padding: 0.35rem 1rem;
        width: auto !important;
    }}
    .copy-btn button:hover {{
        border-color: {config.FOG} !important;
        color: {config.FOG} !important;
    }}

    /* ── Spinner pulse animation ── */
    @keyframes pulse-opacity {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.4; }}
    }}
    .loading-pulse {{
        animation: pulse-opacity 1.4s ease-in-out infinite;
        color: {config.PAPER};
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.85rem;
        letter-spacing: 0.08em;
        text-align: center;
        padding: 2.5rem 0;
    }}

    /* ── Section header separator ── */
    .section-label {{
        font-family: 'IBM Plex Mono', monospace;
        color: {config.ASH};
        font-size: 0.72rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------------

if "output" not in st.session_state:
    st.session_state.output = None          # str | None
if "output_state" not in st.session_state:
    st.session_state.output_state = "empty" # "empty" | "loading" | "success" | "error"
if "last_inputs" not in st.session_state:
    st.session_state.last_inputs = {}
if "copied" not in st.session_state:
    st.session_state.copied = False


# ---------------------------------------------------------------------------
# Helper: copy to clipboard via JS bridge
# ---------------------------------------------------------------------------

def _copy_js(text: str) -> None:
    """Inject a JS snippet that writes text to the clipboard."""
    escaped = text.replace("`", "\\`").replace("\\", "\\\\").replace("$", "\\$")
    st.components.v1.html(
        f"""
        <script>
        navigator.clipboard.writeText(`{escaped}`)
          .then(() => {{
            const el = window.parent.document.getElementById('copy-flash');
            if (el) {{ el.style.opacity = '1'; setTimeout(() => el.style.opacity = '0', 1800); }}
          }})
          .catch(() => {{}});
        </script>
        <div id="copy-flash" style="
          opacity: 0;
          transition: opacity 0.3s;
          font-family: 'IBM Plex Mono', monospace;
          font-size: 0.75rem;
          color: {config.ASH};
          text-align: right;
          margin-top: 0.25rem;
        ">Copied ✓</div>
        """,
        height=24,
    )


# ---------------------------------------------------------------------------
# UI — Header
# ---------------------------------------------------------------------------

st.markdown(
    f"""
    <div style="margin-bottom: 0.25rem;">
      <span style="
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.18em;
        color: {config.ASH};
        text-transform: uppercase;
      ">AI Content Generator</span>
    </div>
    <h1 style="margin-top: 0; margin-bottom: 0.2rem; font-size: 2.2rem;">
      {config.APP_TITLE}
    </h1>
    <p style="color: {config.ASH}; margin-top: 0; font-size: 0.95rem;">
      {config.APP_SUBTITLE}
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown(f'<hr style="border-top: 1px solid {config.SLATE}; margin: 1.2rem 0 1.8rem;">', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# UI — Input form
# ---------------------------------------------------------------------------

st.markdown('<p class="section-label">Content Inputs</p>', unsafe_allow_html=True)

topic = st.text_area(
    "Topic",
    placeholder="e.g. 'Morning routines that boost productivity' or 'My new sustainable skincare line'",
    height=90,
    key="topic_input",
)

col1, col2, col3 = st.columns(3)

with col1:
    platform = st.selectbox("Platform", config.PLATFORMS, key="platform_select")

with col2:
    content_type = st.selectbox("Content Type", config.CONTENT_TYPES, key="content_type_select")

with col3:
    tone = st.selectbox("Tone / Style", config.TONES, key="tone_select")

st.markdown("<br>", unsafe_allow_html=True)

# Platform + content type meta tags
st.markdown(
    f"""
    <div style="margin-bottom: 1rem;">
      <span class="mono-tag">▸ {platform.upper()}</span>
      &nbsp;&nbsp;
      <span class="mono-tag">/ {content_type.upper()}</span>
      &nbsp;&nbsp;
      <span class="mono-tag">/ {tone.upper()}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# UI — Action buttons
# ---------------------------------------------------------------------------

btn_col1, btn_col2 = st.columns([3, 1])

with btn_col1:
    generate_clicked = st.button("✦  Generate", key="generate_btn", use_container_width=True)

with btn_col2:
    has_output = st.session_state.output_state == "success"
    regenerate_clicked = st.button(
        "↻",
        key="regenerate_btn",
        use_container_width=True,
        disabled=not has_output,
    )

# ---------------------------------------------------------------------------
# Generation logic
# ---------------------------------------------------------------------------

def _run_generation(topic: str, platform: str, content_type: str, tone: str, seed: int = 0) -> None:
    """Call the LLM and update session state."""
    if not topic.strip():
        st.session_state.output = "**Please enter a topic** before generating content."
        st.session_state.output_state = "error"
        return

    st.session_state.output_state = "loading"
    st.session_state.output = None
    st.session_state.last_inputs = {
        "topic": topic,
        "platform": platform,
        "content_type": content_type,
        "tone": tone,
    }

    try:
        sys_prompt, user_prompt = get_prompt(platform, content_type, topic, tone)
        # Append a small random seed comment to guarantee variation on Regenerate
        if seed:
            user_prompt += f"\n\n<!-- variation seed: {seed} -->"
        result = generate(user_prompt, sys_prompt)
        st.session_state.output = result
        st.session_state.output_state = "success"
    except LLMError as exc:
        st.session_state.output = f"**! Generation failed**\n\n{exc}"
        st.session_state.output_state = "error"
    except ValueError as exc:
        st.session_state.output = f"**! Configuration error**\n\n{exc}"
        st.session_state.output_state = "error"
    except Exception as exc:
        st.session_state.output = (
            f"**! Unexpected error**\n\n"
            f"Something went wrong on our end. Details: {exc}"
        )
        st.session_state.output_state = "error"


if generate_clicked:
    _run_generation(topic, platform, content_type, tone)
    st.rerun()

if regenerate_clicked and has_output:
    last = st.session_state.last_inputs
    _run_generation(
        last.get("topic", topic),
        last.get("platform", platform),
        last.get("content_type", content_type),
        last.get("tone", tone),
        seed=random.randint(1000, 9999),
    )
    st.rerun()

# ---------------------------------------------------------------------------
# UI — Output panel
# ---------------------------------------------------------------------------

st.markdown(f'<hr style="border-top: 1px solid {config.SLATE}; margin: 1.5rem 0 0.5rem;">', unsafe_allow_html=True)
st.markdown('<p class="section-label">Generated Output</p>', unsafe_allow_html=True)

output_state = st.session_state.output_state
output_text = st.session_state.output or ""

if output_state == "empty":
    st.markdown(
        """
        <div class="output-card is-empty">
            <div style="font-size: 1.5rem; margin-bottom: 0.75rem; opacity: 0.5;">✦</div>
            Fill in a topic and hit <strong>Generate</strong> to see your content here.
        </div>
        """,
        unsafe_allow_html=True,
    )

elif output_state == "loading":
    st.markdown(
        """
        <div class="output-card" style="border: 1px solid #3A3A3F;">
            <div class="loading-pulse">GENERATING  ···</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

elif output_state == "success":
    # Render content
    st.markdown(
        f'<div class="output-card is-success">',
        unsafe_allow_html=True,
    )
    st.markdown(output_text)
    st.markdown("</div>", unsafe_allow_html=True)

    # Copy to clipboard
    st.markdown("<div style='margin-top: 0.75rem;'>", unsafe_allow_html=True)
    copy_col, _, char_col = st.columns([2, 4, 2])
    with copy_col:
        st.markdown('<div class="copy-btn">', unsafe_allow_html=True)
        if st.button("⎘  Copy", key="copy_btn"):
            _copy_js(output_text)
        st.markdown("</div>", unsafe_allow_html=True)
    with char_col:
        char_count = len(output_text)
        word_count = len(output_text.split())
        st.markdown(
            f'<p class="mono-tag" style="text-align:right; padding-top: 0.5rem;">'
            f'{word_count} words · {char_count} chars</p>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

elif output_state == "error":
    st.markdown(
        f"""
        <div class="output-card is-error">
            {output_text}
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="text-align: center;">
      <span class="mono-tag" style="font-size: 0.7rem;">
        Loopwrite · powered by {config.LLM_PROVIDER.upper()} ·
        <a href="https://github.com" style="color: {config.ASH}; text-decoration: none;">GitHub</a>
      </span>
    </div>
    """,
    unsafe_allow_html=True,
)
