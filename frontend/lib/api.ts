/**
 * lib/api.ts — Fetch wrapper for the Loopwrite /api/generate route.
 *
 * Uses a relative URL (/api/generate) — works in local dev and on Render
 * without any environment variable configuration.
 */

export interface FormInputs {
  topic: string
  platform: string
  content_type: string
  tone: string
}

export async function generateContent(
  inputs: FormInputs,
  variationSeed?: number,
): Promise<string> {
  const payload = {
    topic:        inputs.topic,
    platform:     inputs.platform,
    content_type: inputs.content_type,
    tone:         inputs.tone,
    ...(variationSeed ? { variation_seed: variationSeed } : {}),
  }

  let res: Response
  try {
    res = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
  } catch {
    throw new Error('Network error — could not reach the API. Check your connection.')
  }

  if (!res.ok) {
    let detail = `Request failed (HTTP ${res.status})`
    try {
      const data = await res.json()
      if (data?.detail) detail = data.detail
    } catch { /* ignore */ }
    throw new Error(detail)
  }

  const data = await res.json()
  return data.content as string
}
