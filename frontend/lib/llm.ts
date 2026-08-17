/**
 * lib/llm.ts — Server-side LLM provider abstraction for Loopwrite.
 *
 * Runs ONLY in Next.js API routes (server-side) — never in the browser.
 * Swap provider via LLM_PROVIDER env var: groq | gemini | openrouter
 */

export class LLMError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'LLMError'
  }
}

// ── Helpers ─────────────────────────────────────────────────────────────────

function raiseProviderError(provider: string, err: unknown): never {
  const msg = (err instanceof Error ? err.message : String(err)).toLowerCase()
  if (msg.includes('rate limit') || msg.includes('429'))
    throw new LLMError(`${provider} rate limit reached. Wait a moment and try again, or switch providers.`)
  if (msg.includes('auth') || msg.includes('401') || msg.includes('api_key') || msg.includes('invalid api key'))
    throw new LLMError(`${provider} authentication failed — check that your API key is correct.`)
  if (msg.includes('quota') || msg.includes('403'))
    throw new LLMError(`${provider} quota exceeded. Check your usage at the provider dashboard.`)
  if (msg.includes('timeout') || msg.includes('connect'))
    throw new LLMError(`${provider} request timed out. Check your connection and try again.`)
  throw new LLMError(`${provider} error: ${err instanceof Error ? err.message : String(err)}`)
}

// ── Provider implementations ─────────────────────────────────────────────────

async function generateGroq(prompt: string, system: string): Promise<string> {
  const apiKey = process.env.GROQ_API_KEY
  if (!apiKey)
    throw new LLMError('GROQ_API_KEY is not set. Get a free key at https://console.groq.com')
  try {
    const Groq = (await import('groq-sdk')).default
    const client = new Groq({ apiKey })
    const res = await client.chat.completions.create({
      model: process.env.GROQ_MODEL ?? 'llama-3.3-70b-versatile',
      messages: [
        { role: 'system', content: system },
        { role: 'user',   content: prompt },
      ],
      temperature: 0.85,
      max_tokens: 1500,
    })
    return res.choices[0].message.content?.trim() ?? ''
  } catch (err) {
    raiseProviderError('Groq', err)
  }
}

async function generateGemini(prompt: string, system: string): Promise<string> {
  const apiKey = process.env.GOOGLE_API_KEY
  if (!apiKey)
    throw new LLMError('GOOGLE_API_KEY is not set. Get a free key at https://aistudio.google.com')
  try {
    const { GoogleGenerativeAI } = await import('@google/generative-ai')
    const genai = new GoogleGenerativeAI(apiKey)
    const model = genai.getGenerativeModel({
      model: process.env.GEMINI_MODEL ?? 'gemini-1.5-flash',
      systemInstruction: system,
    })
    const result = await model.generateContent(prompt)
    return result.response.text().trim()
  } catch (err) {
    raiseProviderError('Gemini', err)
  }
}

async function generateOpenRouter(prompt: string, system: string): Promise<string> {
  const apiKey = process.env.OPENROUTER_API_KEY
  if (!apiKey)
    throw new LLMError('OPENROUTER_API_KEY is not set. Get a free key at https://openrouter.ai')
  try {
    const OpenAI = (await import('openai')).default
    const client = new OpenAI({ apiKey, baseURL: 'https://openrouter.ai/api/v1' })
    const res = await client.chat.completions.create({
      model: process.env.OPENROUTER_MODEL ?? 'meta-llama/llama-3.2-3b-instruct:free',
      messages: [
        { role: 'system', content: system },
        { role: 'user',   content: prompt },
      ],
      temperature: 0.85,
      max_tokens: 1500,
    })
    return res.choices[0].message.content?.trim() ?? ''
  } catch (err) {
    raiseProviderError('OpenRouter', err)
  }
}

// ── Public API ───────────────────────────────────────────────────────────────

const PROVIDERS: Record<string, (p: string, s: string) => Promise<string>> = {
  groq:       generateGroq,
  gemini:     generateGemini,
  openrouter: generateOpenRouter,
}

export async function generate(prompt: string, system: string): Promise<string> {
  const provider = (process.env.LLM_PROVIDER ?? 'groq').toLowerCase()
  const fn = PROVIDERS[provider]
  if (!fn)
    throw new Error(`Unsupported LLM_PROVIDER '${provider}'. Use: groq | gemini | openrouter`)
  return fn(prompt, system)
}
