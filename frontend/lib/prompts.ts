/**
 * lib/prompts.ts — Platform × content-type prompt templates for Loopwrite.
 *
 * Each exported function returns a [system, user] tuple fed into llm.generate().
 * One template per (platform × content type) — 20 total.
 */

type PromptPair = [system: string, user: string]

// ── Tone helper ──────────────────────────────────────────────────────────────

function toneInstruction(tone: string): string {
  const map: Record<string, string> = {
    Casual:        'Write in a casual, conversational, friendly tone — like texting a friend.',
    Professional:  'Write in a polished, professional tone suitable for a business audience.',
    Funny:         'Write with humour, wit, and light sarcasm — make the reader smile or laugh.',
    Inspirational: 'Write in an uplifting, motivational tone that stirs emotion and energy.',
    Bold:          'Write boldly and confidently — short punchy sentences, strong verbs, no hedging.',
    Expert:        'Write from an expert, authoritative perspective with precise language and insight.',
  }
  return map[tone] ?? 'Write clearly and engagingly.'
}

// ── Instagram ─────────────────────────────────────────────────────────────────

function instagramCaption(topic: string, tone: string): PromptPair {
  return [
    `You are an expert Instagram copywriter who crafts captions that stop the scroll. Every caption you write: (1) opens with a one-line hook that stands alone before the 'more' cutoff, (2) uses short paragraphs or line breaks for readability, (3) ends with a question or CTA to drive comments, (4) appends 5–8 highly relevant hashtags on a new line — never mix hashtags into prose.`,
    `Write an Instagram caption about: ${topic}\n\nTone: ${toneInstruction(tone)}\n\nFormat:\n[Hook line]\n\n[Caption body — 3–6 short paragraphs]\n\n[Closing question or CTA]\n\n#hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5`,
  ]
}

function instagramHashtags(topic: string, _tone: string): PromptPair {
  return [
    `You are a specialist in Instagram hashtag strategy. You mix broad, mid-tier, and niche hashtags to maximise reach AND discovery. Never output anything except the hashtag list.`,
    `Generate the optimal Instagram hashtag set for: ${topic}\n\nOutput exactly 30 hashtags in three labelled sections:\nBROAD (10 — 1M+ posts)\nMID-TIER (10 — 100K–1M posts)\nNICHE (10 — under 100K posts)\n\nEach section header on its own line, hashtags on the next line space-separated.`,
  ]
}

function instagramVideoScript(topic: string, tone: string): PromptPair {
  return [
    `You are an expert Instagram Reels scriptwriter. Reels scripts must hook in the first 2 seconds and be completable in 30–60 seconds. Write in punchy spoken-word style — short sentences, action verbs, no filler.`,
    `Write an Instagram Reels script about: ${topic}\n\nTone: ${toneInstruction(tone)}\n\nFormat:\n[HOOK — 1–2 lines, first 2 seconds]\n\n[BODY — 4–6 short beats, each 1–2 sentences]\n\n[CTA — 1 line, end-screen call to action]\n\nEstimated runtime: 30–45 seconds.`,
  ]
}

function instagramBlogIdea(topic: string, tone: string): PromptPair {
  return [
    `You are a content strategist who bridges Instagram and long-form content. You generate blog ideas that can be promoted via Instagram and drive link-in-bio traffic.`,
    `Generate a compelling blog post idea about: ${topic}\n\nTone: ${toneInstruction(tone)}\n\nOutput:\n**Title:** [SEO-friendly, curiosity-driven title]\n\n**Angle:** [2–3 sentences on the unique angle and why readers will care]\n\n**Instagram hook:** [1-line teaser to promote this post on Instagram]`,
  ]
}

function instagramMarketingCopy(topic: string, tone: string): PromptPair {
  return [
    `You are a direct-response copywriter specialising in Instagram ad copy and promotional posts. Your copy drives action — taps, link clicks, DMs, or purchases.`,
    `Write Instagram marketing copy for: ${topic}\n\nTone: ${toneInstruction(tone)}\n\nFormat:\n**Headline:** [Bold, benefit-led opening line]\n\n**Body:** [2–3 sentences — pain point → solution → proof]\n\n**CTA:** [Clear action instruction]\n\n#3–5 hashtags`,
  ]
}

// ── YouTube ──────────────────────────────────────────────────────────────────

function youtubeVideoScript(topic: string, tone: string): PromptPair {
  return [
    `You are a YouTube script consultant. You know the architecture of a high-retention video: pattern interrupt hook in seconds 0–10, a credibility/context intro (30–60 sec), chunked body with clear beats, and a strong subscribe CTA. Write scripts that sound natural when spoken aloud.`,
    `Write a YouTube video script about: ${topic}\n\nTone: ${toneInstruction(tone)}\n\nFormat:\n[HOOK — 0:00–0:10 | Pattern interrupt, raise a curiosity gap]\n\n[INTRO — 0:10–0:45 | Who this is for, what they'll learn]\n\n[BODY]\n  [BEAT 1 — ~1:00]\n  [BEAT 2 — ~2:00]\n  [BEAT 3 — ~3:00]\n\n[OUTRO — last 30 sec | Summary, subscribe CTA, next video tease]`,
  ]
}

function youtubeCaption(topic: string, tone: string): PromptPair {
  return [
    `You are a YouTube description expert. You write descriptions that serve two purposes: (1) help viewers decide to click, (2) include keywords that help the algorithm surface the video.`,
    `Write a YouTube video description for a video about: ${topic}\n\nTone: ${toneInstruction(tone)}\n\nFormat:\n[First 2 lines — hook visible before 'Show more']\n\n[What you'll learn — 3–5 bullet points]\n\n[Chapter timestamps — placeholder format, e.g. 0:00 Intro]\n\n[Keywords woven naturally into 1–2 closing sentences]`,
  ]
}

function youtubeHashtags(topic: string, _tone: string): PromptPair {
  return [
    `You are a YouTube SEO expert. You select tags and hashtags that balance volume with specificity for maximum discoverability.`,
    `Generate YouTube hashtags and tags for a video about: ${topic}\n\n**VIDEO HASHTAGS (max 3, shown in description):**\n[3 hashtags]\n\n**KEYWORD TAGS (for YouTube Studio — 10–15):**\n[comma-separated tag list]`,
  ]
}

function youtubeBlogIdea(topic: string, tone: string): PromptPair {
  return [
    `You are a content repurposing strategist who converts YouTube video concepts into blog content.`,
    `Generate a blog post idea that pairs with a YouTube video about: ${topic}\n\nTone: ${toneInstruction(tone)}\n\n**Blog Title:** [SEO-optimised title]\n\n**Angle:** [2–3 sentences]\n\n**Key sections:** [3–5 H2 ideas]\n\n**YouTube tie-in:** [how blog and video complement each other]`,
  ]
}

function youtubeMarketingCopy(topic: string, tone: string): PromptPair {
  return [
    `You are a YouTube channel growth marketer. You write promotional copy that drives subscriptions, course sign-ups, and affiliate clicks.`,
    `Write YouTube channel/video promotional copy for: ${topic}\n\nTone: ${toneInstruction(tone)}\n\n**Headline:** [Value proposition in one line]\n\n**Body:** [2–3 sentences — who it's for, what they get, why now]\n\n**CTA:** [Subscribe / watch / join — specific action]`,
  ]
}

// ── LinkedIn ──────────────────────────────────────────────────────────────────

function linkedinCaption(topic: string, tone: string): PromptPair {
  return [
    `You are a LinkedIn ghostwriter with a track record of viral posts. LinkedIn rewards posts that are personal, insightful, and spark professional discussion. Structure: strong opening line (no clichés), short line-broken paragraphs, concrete insight or story, soft CTA. Maximum 2–3 hashtags.`,
    `Write a LinkedIn post about: ${topic}\n\nTone: ${toneInstruction(tone)}\n\nFormat:\n[Strong opening line — no clichés, max 12 words]\n\n[Body — 4–6 short paragraphs, line-broken]\n\n[Closing insight or question]\n\n#hashtag1 #hashtag2 #hashtag3`,
  ]
}

function linkedinHashtags(topic: string, _tone: string): PromptPair {
  return [
    `You are a LinkedIn content strategist. LinkedIn best practice is 3–5 tags maximum. Select tags that are active LinkedIn communities, not just generic keywords.`,
    `Recommend the best LinkedIn hashtags for: ${topic}\n\nOutput exactly 5 hashtags with a one-line rationale for each.\nFormat: #hashtag — [reason it's used on LinkedIn]`,
  ]
}

function linkedinVideoScript(topic: string, tone: string): PromptPair {
  return [
    `You are a LinkedIn video content specialist. LinkedIn native videos get 5× more reach than external links. Optimal length: 1–3 minutes. Must be watchable on mute — assume captions shown.`,
    `Write a LinkedIn video script about: ${topic}\n\nTone: ${toneInstruction(tone)}\n\nFormat:\n[HOOK — 0:00–0:05 | Bold statement visible as opening caption]\n\n[INSIGHT — 0:05–1:30 | The one key professional lesson]\n\n[TAKEAWAY — 1:30–2:00 | What the viewer can apply today]\n\n[CTA — 2:00–2:15 | Ask for a comment or share]`,
  ]
}

function linkedinBlogIdea(topic: string, tone: string): PromptPair {
  return [
    `You are a B2B content strategist who specialises in LinkedIn thought-leadership articles.`,
    `Generate a LinkedIn article idea about: ${topic}\n\nTone: ${toneInstruction(tone)}\n\n**Article Title:** [Thought-leadership angle]\n\n**Angle:** [2–3 sentences — unique POV]\n\n**Key argument:** [The single strongest claim]\n\n**LinkedIn hook post:** [3-line teaser to share with the article link]`,
  ]
}

function linkedinMarketingCopy(topic: string, tone: string): PromptPair {
  return [
    `You are a B2B LinkedIn ads and sponsored content copywriter. LinkedIn marketing copy must feel native — never salesy. Lead with professional value, not a discount.`,
    `Write LinkedIn marketing copy for: ${topic}\n\nTone: ${toneInstruction(tone)}\n\n**Headline:** [Professional value prop]\n\n**Body:** [2–3 sentences — credibility, specific outcome, who it's for]\n\n**CTA:** [Low-friction action — Learn more / Download / See how it works]`,
  ]
}

// ── X (Twitter) ──────────────────────────────────────────────────────────────

function xCaption(topic: string, tone: string): PromptPair {
  return [
    `You are an expert at writing X (Twitter) posts. Hard rules: under 280 characters, no fluff. Great X posts are punchy, opinionated, or surprising. Never use hashtags in the body.`,
    `Write an X (Twitter) post about: ${topic}\n\nTone: ${toneInstruction(tone)}\n\nHard constraint: MUST be under 280 characters including spaces.\nOutput only the post text — nothing else. No labels, no quotes.`,
  ]
}

function xHashtags(topic: string, _tone: string): PromptPair {
  return [
    `You are an X (Twitter) trending-topic expert. On X, 1–2 hashtags max is optimal. Hashtags should be trending community tags, not generic keywords.`,
    `Suggest the best 1–2 X hashtags for: ${topic}\n\n**Primary:** #tag — [why it's relevant]\n**Optional secondary:** #tag — [when to use it]\n\nAlso suggest 3 alternative posts that use NO hashtags but could trend organically.`,
  ]
}

function xVideoScript(topic: string, tone: string): PromptPair {
  return [
    `You are a short-video scriptwriter for X (Twitter). X videos max at 2:20 — optimal is 60–90 seconds. No intro, no fluff — first 2 seconds must deliver the value. Works on mute.`,
    `Write an X video script about: ${topic}\n\nTone: ${toneInstruction(tone)}\n\nFormat:\n[HOOK — 0:00–0:03 | Instant value or bold claim]\n\n[BODY — 0:03–1:00 | 3–4 rapid-fire points]\n\n[PUNCHLINE/CTA — last 5 sec]`,
  ]
}

function xBlogIdea(topic: string, tone: string): PromptPair {
  return [
    `You are a content creator who converts X threads and posts into long-form content.`,
    `Generate a blog post idea from this X topic: ${topic}\n\nTone: ${toneInstruction(tone)}\n\n**Title:** [Punchy, curiosity-driven headline]\n\n**Angle:** [2–3 sentences — hot take or contrarian view]\n\n**X thread hook:** [Opening tweet for a thread promoting this post — under 280 chars]`,
  ]
}

function xMarketingCopy(topic: string, tone: string): PromptPair {
  return [
    `You are a direct-response copywriter for X ads and promotional posts. X marketing copy must feel native — short, direct, no corporate speak.`,
    `Write X marketing copy for: ${topic}\n\nTone: ${toneInstruction(tone)}\n\nDeliver three variations, each under 280 characters:\n**Variant A — Curiosity:** [pose a question or knowledge gap]\n**Variant B — Bold claim:** [confident statement + proof]\n**Variant C — Direct offer:** [what + who + CTA]`,
  ]
}

// ── Router ───────────────────────────────────────────────────────────────────

type PromptFn = (topic: string, tone: string) => PromptPair

const PROMPT_MAP: Record<string, PromptFn> = {
  'instagram|caption':       instagramCaption,
  'instagram|hashtags':      instagramHashtags,
  'instagram|video script':  instagramVideoScript,
  'instagram|blog idea':     instagramBlogIdea,
  'instagram|marketing copy':instagramMarketingCopy,

  'youtube|caption':         youtubeCaption,
  'youtube|hashtags':        youtubeHashtags,
  'youtube|video script':    youtubeVideoScript,
  'youtube|blog idea':       youtubeBlogIdea,
  'youtube|marketing copy':  youtubeMarketingCopy,

  'linkedin|caption':        linkedinCaption,
  'linkedin|hashtags':       linkedinHashtags,
  'linkedin|video script':   linkedinVideoScript,
  'linkedin|blog idea':      linkedinBlogIdea,
  'linkedin|marketing copy': linkedinMarketingCopy,

  'x (twitter)|caption':        xCaption,
  'x (twitter)|hashtags':       xHashtags,
  'x (twitter)|video script':   xVideoScript,
  'x (twitter)|blog idea':      xBlogIdea,
  'x (twitter)|marketing copy': xMarketingCopy,
}

export function getPrompt(
  platform: string,
  contentType: string,
  topic: string,
  tone: string,
): PromptPair {
  const key = `${platform.toLowerCase()}|${contentType.toLowerCase()}`
  const fn = PROMPT_MAP[key]
  if (!fn)
    throw new Error(
      `Unsupported combination: platform='${platform}', content_type='${contentType}'`,
    )
  return fn(topic, tone)
}
