"""
prompts.py — Platform × content-type prompt templates for Loopwrite.

Each public function returns a (system_prompt, user_prompt) tuple that is
passed directly to llm_client.generate(). Templates are intentionally
specific so output matches each platform's native format.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _tone_instruction(tone: str) -> str:
    """Return a one-line tone modifier to embed in every prompt."""
    mapping = {
        "Casual": "Write in a casual, conversational, friendly tone — like texting a friend.",
        "Professional": "Write in a polished, professional tone suitable for a business audience.",
        "Funny": "Write with humour, wit, and light sarcasm — make the reader smile or laugh.",
        "Inspirational": "Write in an uplifting, motivational tone that stirs emotion and energy.",
        "Bold": "Write boldly and confidently — short punchy sentences, strong verbs, no hedging.",
        "Expert": "Write from an expert, authoritative perspective with precise language and insight.",
    }
    return mapping.get(tone, "Write clearly and engagingly.")


# ---------------------------------------------------------------------------
# Instagram
# ---------------------------------------------------------------------------

def instagram_caption(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are an expert Instagram copywriter who crafts captions that stop the scroll. "
        "You know Instagram's algorithm rewards saves and comments over likes. "
        "Every caption you write: (1) opens with a one-line hook that stands alone before the 'more' cutoff, "
        "(2) uses short paragraphs or line breaks for readability, "
        "(3) ends with a question or call-to-action to drive comments, "
        "(4) appends 5–8 highly relevant hashtags on a new line after the body — never mix hashtags into prose."
    )
    user = (
        f"Write an Instagram caption about: {topic}\n\n"
        f"Tone: {_tone_instruction(tone)}\n\n"
        "Format strictly:\n"
        "[Hook line]\n\n"
        "[Caption body — 3–6 short paragraphs]\n\n"
        "[Closing question or CTA]\n\n"
        "#hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5"
    )
    return system, user


def instagram_hashtags(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are a specialist in Instagram hashtag strategy. "
        "You mix broad, mid-tier, and niche hashtags to maximise reach AND discovery in a specific community. "
        "Never output anything except the hashtag list."
    )
    user = (
        f"Generate the optimal Instagram hashtag set for this topic: {topic}\n\n"
        "Output exactly 30 hashtags grouped into three labelled sections:\n"
        "• BROAD (10 hashtags — 1M+ posts)\n"
        "• MID-TIER (10 hashtags — 100K–1M posts)\n"
        "• NICHE (10 hashtags — under 100K posts)\n\n"
        "Format: each section header on its own line, hashtags on the next line space-separated."
    )
    return system, user


def instagram_video_script(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are an expert Instagram Reels scriptwriter. "
        "Reels scripts must hook in the first 2 seconds and be completable in 30–60 seconds. "
        "Write in punchy, spoken-word style — short sentences, action verbs, no filler."
    )
    user = (
        f"Write an Instagram Reels script about: {topic}\n\n"
        f"Tone: {_tone_instruction(tone)}\n\n"
        "Format:\n"
        "[HOOK — 1–2 lines, first 2 seconds on screen]\n\n"
        "[BODY — 4–6 short beats, each 1–2 sentences]\n\n"
        "[CTA — 1 line, end-screen call to action]\n\n"
        "Estimated runtime: 30–45 seconds."
    )
    return system, user


def instagram_blog_idea(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are a content strategist who bridges Instagram and long-form content. "
        "You generate blog ideas that can be promoted via Instagram and drive link-in-bio traffic."
    )
    user = (
        f"Generate a compelling blog post idea about: {topic}\n\n"
        f"Tone: {_tone_instruction(tone)}\n\n"
        "Output:\n"
        "**Title:** [SEO-friendly, curiosity-driven title]\n\n"
        "**Angle:** [2–3 sentences on the unique angle and why readers will care]\n\n"
        "**Instagram hook:** [1-line teaser to promote this post on Instagram]"
    )
    return system, user


def instagram_marketing_copy(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are a direct-response copywriter specialising in Instagram ad copy and promotional posts. "
        "Your copy drives action — taps, link clicks, DMs, or purchases."
    )
    user = (
        f"Write Instagram marketing copy for: {topic}\n\n"
        f"Tone: {_tone_instruction(tone)}\n\n"
        "Format:\n"
        "**Headline:** [Bold, benefit-led opening line]\n\n"
        "**Body:** [2–3 sentences — pain point → solution → proof]\n\n"
        "**CTA:** [Clear action instruction, e.g. 'DM us START' or 'Link in bio']\n\n"
        "#3–5 hashtags"
    )
    return system, user


# ---------------------------------------------------------------------------
# YouTube
# ---------------------------------------------------------------------------

def youtube_video_script(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are a YouTube script consultant who has studied 10,000+ successful videos. "
        "You know the architecture of a high-retention video: pattern interrupt hook in seconds 0–10, "
        "a credibility/context intro (30–60 sec), chunked body with clear beats, and a strong subscribe CTA. "
        "Write scripts that sound natural when spoken aloud — no robotic lists, use conversational transitions."
    )
    user = (
        f"Write a YouTube video script about: {topic}\n\n"
        f"Tone: {_tone_instruction(tone)}\n\n"
        "Format:\n"
        "[HOOK — 0:00–0:10 | Pattern interrupt opening, raise a curiosity gap]\n\n"
        "[INTRO — 0:10–0:45 | Who this is for, what they'll learn, quick credibility]\n\n"
        "[BODY]\n"
        "  [BEAT 1 — ~1:00 | ...]\n"
        "  [BEAT 2 — ~2:00 | ...]\n"
        "  [BEAT 3 — ~3:00 | ...]\n"
        "  (add beats as needed)\n\n"
        "[OUTRO — last 30 sec | Summary, subscribe CTA, suggested next video tease]"
    )
    return system, user


def youtube_caption(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are a YouTube community-post and video-description expert. "
        "You write descriptions that serve two purposes: (1) help viewers decide to click, "
        "(2) include keywords that help the YouTube algorithm surface the video."
    )
    user = (
        f"Write a YouTube video description for a video about: {topic}\n\n"
        f"Tone: {_tone_instruction(tone)}\n\n"
        "Format:\n"
        "[First 2 lines — hook visible before 'Show more' cutoff]\n\n"
        "[What you'll learn — 3–5 bullet points]\n\n"
        "[Chapter timestamps — placeholder format, e.g. 0:00 Intro]\n\n"
        "[Relevant keywords woven naturally into 1–2 closing sentences]"
    )
    return system, user


def youtube_hashtags(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are a YouTube SEO expert. "
        "You select tags and hashtags that balance volume with specificity for maximum discoverability."
    )
    user = (
        f"Generate YouTube hashtags and tags for a video about: {topic}\n\n"
        "Output two sections:\n"
        "**VIDEO HASHTAGS (show in description — max 3):**\n"
        "[3 hashtags]\n\n"
        "**KEYWORD TAGS (for YouTube Studio tags field — 10–15):**\n"
        "[comma-separated tag list]"
    )
    return system, user


def youtube_blog_idea(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are a content repurposing strategist who converts YouTube video concepts into blog content."
    )
    user = (
        f"Generate a blog post idea that pairs with a YouTube video about: {topic}\n\n"
        f"Tone: {_tone_instruction(tone)}\n\n"
        "Output:\n"
        "**Blog Title:** [SEO-optimised title]\n\n"
        "**Angle:** [2–3 sentences — unique perspective or hook]\n\n"
        "**Key sections to cover:** [3–5 H2 section ideas]\n\n"
        "**YouTube tie-in:** [1 sentence — how the blog and video complement each other]"
    )
    return system, user


def youtube_marketing_copy(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are a YouTube channel growth marketer. "
        "You write promotional copy that drives subscriptions, course sign-ups, and affiliate clicks."
    )
    user = (
        f"Write YouTube channel / video promotional copy for: {topic}\n\n"
        f"Tone: {_tone_instruction(tone)}\n\n"
        "Format:\n"
        "**Headline:** [Value proposition in one line]\n\n"
        "**Body:** [2–3 sentences — who it's for, what they get, why now]\n\n"
        "**CTA:** [Subscribe / watch / join — specific action]"
    )
    return system, user


# ---------------------------------------------------------------------------
# LinkedIn
# ---------------------------------------------------------------------------

def linkedin_caption(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are a LinkedIn ghostwriter with a track record of viral posts. "
        "LinkedIn rewards posts that are personal, insightful, and spark professional discussion. "
        "Structure: strong opening line (no 'I am excited to share' clichés), "
        "short line-broken paragraphs, concrete insight or story, soft CTA at the end. "
        "Maximum 2–3 hashtags — hashtag stuffing kills reach on LinkedIn."
    )
    user = (
        f"Write a LinkedIn post about: {topic}\n\n"
        f"Tone: {_tone_instruction(tone)}\n\n"
        "Format:\n"
        "[Strong opening line — no clichés, max 12 words]\n\n"
        "[Body — 4–6 short paragraphs, line-broken for mobile readability]\n\n"
        "[Closing insight or question to drive comments]\n\n"
        "#hashtag1 #hashtag2 #hashtag3"
    )
    return system, user


def linkedin_hashtags(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are a LinkedIn content strategist. "
        "LinkedIn hashtag best practice is 3–5 tags maximum — more dilutes reach. "
        "Select tags that are active LinkedIn communities, not just generic keywords."
    )
    user = (
        f"Recommend the best LinkedIn hashtags for this topic: {topic}\n\n"
        "Output exactly 5 hashtags with a one-line rationale for each.\n"
        "Format: #hashtag — [reason it's used on LinkedIn]"
    )
    return system, user


def linkedin_video_script(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are a LinkedIn video content specialist. "
        "LinkedIn native videos get 5× more reach than external links. "
        "Optimal length: 1–3 minutes. Must be watchable on mute — assume captions shown. "
        "Structure: hook (0–5 sec), clear single insight, practical takeaway, CTA to comment."
    )
    user = (
        f"Write a LinkedIn video script about: {topic}\n\n"
        f"Tone: {_tone_instruction(tone)}\n\n"
        "Format:\n"
        "[HOOK — 0:00–0:05 | Bold statement or question visible as opening caption]\n\n"
        "[INSIGHT — 0:05–1:30 | The one key professional lesson or observation]\n\n"
        "[PRACTICAL TAKEAWAY — 1:30–2:00 | What the viewer can apply today]\n\n"
        "[CTA — 2:00–2:15 | Ask for a comment or share]"
    )
    return system, user


def linkedin_blog_idea(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are a B2B content strategist who specialises in LinkedIn thought-leadership articles."
    )
    user = (
        f"Generate a LinkedIn article idea about: {topic}\n\n"
        f"Tone: {_tone_instruction(tone)}\n\n"
        "Output:\n"
        "**Article Title:** [Thought-leadership angle, professional audience]\n\n"
        "**Angle:** [2–3 sentences — unique POV, why professionals should read this]\n\n"
        "**Key argument:** [The single strongest claim the article will make]\n\n"
        "**LinkedIn hook post:** [3-line teaser post to share with the article link]"
    )
    return system, user


def linkedin_marketing_copy(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are a B2B LinkedIn ads and sponsored content copywriter. "
        "LinkedIn marketing copy must feel native — never salesy or pushy. "
        "Lead with professional value, not a discount."
    )
    user = (
        f"Write LinkedIn marketing copy for: {topic}\n\n"
        f"Tone: {_tone_instruction(tone)}\n\n"
        "Format:\n"
        "**Headline:** [Professional value prop — what problem does this solve?]\n\n"
        "**Body:** [2–3 sentences — credibility, specific outcome, who it's for]\n\n"
        "**CTA:** [Low-friction action — Learn more / Download / See how it works]"
    )
    return system, user


# ---------------------------------------------------------------------------
# X (Twitter)
# ---------------------------------------------------------------------------

def x_caption(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are an expert at writing X (Twitter) posts. "
        "The hard rules: under 280 characters, no fluff, no filler phrases. "
        "Great X posts are: punchy, opinionated, or surprising. "
        "They spark replies — either agreement, disagreement, or curiosity. "
        "Never use hashtags in the body — they read as spam on X."
    )
    user = (
        f"Write an X (Twitter) post about: {topic}\n\n"
        f"Tone: {_tone_instruction(tone)}\n\n"
        "Hard constraint: MUST be under 280 characters including spaces.\n"
        "Output only the post text — nothing else. No labels, no quotes."
    )
    return system, user


def x_hashtags(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are an X (Twitter) trending-topic expert. "
        "On X, 1–2 hashtags max per post is optimal — more hurts engagement. "
        "Hashtags on X should be trending community tags, not generic keywords."
    )
    user = (
        f"Suggest the best 1–2 X (Twitter) hashtags for this topic: {topic}\n\n"
        "Output:\n"
        "**Primary hashtag:** #tag — [why it's trending / relevant]\n"
        "**Optional secondary:** #tag — [when to use it]\n\n"
        "Also suggest 3 alternative posts that use NO hashtags but could trend organically."
    )
    return system, user


def x_video_script(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are a short-video scriptwriter for X (Twitter). "
        "X videos max out at 2:20 — optimal is 60–90 seconds. "
        "No intro, no fluff — first 2 seconds must deliver the value. "
        "Works on mute: assume captions."
    )
    user = (
        f"Write an X (Twitter) video script about: {topic}\n\n"
        f"Tone: {_tone_instruction(tone)}\n\n"
        "Format:\n"
        "[HOOK — 0:00–0:03 | Instant value or bold claim]\n\n"
        "[BODY — 0:03–1:00 | 3–4 rapid-fire points, no padding]\n\n"
        "[PUNCHLINE / CTA — last 5 sec | What to do next or memorable closer]"
    )
    return system, user


def x_blog_idea(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are a content creator who converts X threads and posts into long-form content."
    )
    user = (
        f"Generate a blog post idea that originated from this X topic: {topic}\n\n"
        f"Tone: {_tone_instruction(tone)}\n\n"
        "Output:\n"
        "**Title:** [Punchy, curiosity-driven, shareable headline]\n\n"
        "**Angle:** [2–3 sentences — hot take or contrarian view]\n\n"
        "**X thread hook:** [Opening tweet for a thread promoting this post — under 280 chars]"
    )
    return system, user


def x_marketing_copy(topic: str, tone: str) -> tuple[str, str]:
    system = (
        "You are a direct-response copywriter for X (Twitter) ads and promotional posts. "
        "X marketing copy must feel native and not like an ad — short, direct, no corporate speak."
    )
    user = (
        f"Write X (Twitter) marketing copy for: {topic}\n\n"
        f"Tone: {_tone_instruction(tone)}\n\n"
        "Deliver three variations, each under 280 characters:\n"
        "**Variant A — Curiosity:** [pose a question or knowledge gap]\n"
        "**Variant B — Bold claim:** [confident statement + proof]\n"
        "**Variant C — Direct offer:** [what + who + CTA]"
    )
    return system, user


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

# Map (platform_key, content_type_key) → prompt function
_PROMPT_MAP: dict[tuple[str, str], callable] = {
    ("instagram", "caption"): instagram_caption,
    ("instagram", "hashtags"): instagram_hashtags,
    ("instagram", "video script"): instagram_video_script,
    ("instagram", "blog idea"): instagram_blog_idea,
    ("instagram", "marketing copy"): instagram_marketing_copy,

    ("youtube", "caption"): youtube_caption,
    ("youtube", "hashtags"): youtube_hashtags,
    ("youtube", "video script"): youtube_video_script,
    ("youtube", "blog idea"): youtube_blog_idea,
    ("youtube", "marketing copy"): youtube_marketing_copy,

    ("linkedin", "caption"): linkedin_caption,
    ("linkedin", "hashtags"): linkedin_hashtags,
    ("linkedin", "video script"): linkedin_video_script,
    ("linkedin", "blog idea"): linkedin_blog_idea,
    ("linkedin", "marketing copy"): linkedin_marketing_copy,

    ("x (twitter)", "caption"): x_caption,
    ("x (twitter)", "hashtags"): x_hashtags,
    ("x (twitter)", "video script"): x_video_script,
    ("x (twitter)", "blog idea"): x_blog_idea,
    ("x (twitter)", "marketing copy"): x_marketing_copy,
}


def get_prompt(platform: str, content_type: str, topic: str, tone: str) -> tuple[str, str]:
    """
    Return (system_prompt, user_prompt) for the given platform/content_type combo.

    Args:
        platform: e.g. "Instagram", "YouTube", "LinkedIn", "X (Twitter)"
        content_type: e.g. "Caption", "Video Script", "Hashtags", "Blog Idea", "Marketing Copy"
        topic: free-text topic entered by the user
        tone: one of the TONES constants from config.py

    Returns:
        Tuple[system_prompt, user_prompt] ready for llm_client.generate()

    Raises:
        ValueError: if the (platform, content_type) combination is not supported
    """
    key = (platform.lower(), content_type.lower())
    fn = _PROMPT_MAP.get(key)
    if fn is None:
        raise ValueError(
            f"Unsupported combination: platform='{platform}', content_type='{content_type}'"
        )
    return fn(topic, tone)
