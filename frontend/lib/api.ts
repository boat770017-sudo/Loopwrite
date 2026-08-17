/**
 * lib/api.ts — Fetch wrapper for the Loopwrite FastAPI backend.
 *
 * The backend URL is controlled by NEXT_PUBLIC_API_URL env var:
 *   - Local dev: http://localhost:8000  (set in .env.local)
 *   - Render:    https://loopwrite-backend.onrender.com  (set in Render dashboard)
 */

export interface FormInputs {
  topic: string
  platform: string
  content_type: string
  tone: string
}

const API_URL =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, '') ?? 'http://localhost:8000'

export async function generateContent(
  inputs: FormInputs,
  variationSeed?: number,
): Promise<string> {
  const payload = {
    topic: inputs.topic,
    platform: inputs.platform,
    content_type: inputs.content_type,
    tone: inputs.tone,
    ...(variationSeed ? { variation_seed: variationSeed } : {}),
  }

  let res: Response
  try {
    res = await fetch(`${API_URL}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
  } catch {
    throw new Error(
      'Could not reach the Loopwrite API. Make sure the backend is running at ' +
        API_URL,
    )
  }

  if (!res.ok) {
    let detail = `Request failed (HTTP ${res.status})`
    try {
      const data = await res.json()
      if (data?.detail) detail = data.detail
    } catch { /* ignore parse error */ }
    throw new Error(detail)
  }

  const data = await res.json()
  return data.content as string
}
