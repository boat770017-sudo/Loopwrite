import { NextRequest, NextResponse } from 'next/server'
import { generate, LLMError } from '@/lib/llm'
import { getPrompt } from '@/lib/prompts'

export async function POST(req: NextRequest) {
  try {
    const body = await req.json()
    const { topic, platform, content_type, tone, variation_seed } = body as {
      topic: string
      platform: string
      content_type: string
      tone: string
      variation_seed?: number
    }

    // Validate required fields
    if (!topic?.trim()) {
      return NextResponse.json({ detail: 'Topic cannot be empty.' }, { status: 422 })
    }
    if (!platform || !content_type || !tone) {
      return NextResponse.json(
        { detail: 'platform, content_type, and tone are required.' },
        { status: 422 },
      )
    }

    // Build prompt pair
    let [system, user] = getPrompt(platform, content_type, topic.trim(), tone)

    // Append variation seed so Regenerate produces different output
    if (variation_seed) {
      user += `\n\n<!-- variation: ${variation_seed} -->`
    }

    const content = await generate(user, system)
    return NextResponse.json({ content })

  } catch (err: unknown) {
    if (err instanceof LLMError) {
      return NextResponse.json({ detail: err.message }, { status: 500 })
    }
    if (err instanceof Error && err.message.startsWith('Unsupported')) {
      return NextResponse.json({ detail: err.message }, { status: 422 })
    }
    const message = err instanceof Error ? err.message : String(err)
    return NextResponse.json(
      { detail: `Unexpected error — please try again. ${message}` },
      { status: 500 },
    )
  }
}
