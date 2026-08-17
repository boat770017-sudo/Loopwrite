'use client'

import { useState } from 'react'

// ── Constants (mirrored from backend/config.py) ───────────────────────────

const PLATFORMS = ['Instagram', 'YouTube', 'LinkedIn', 'X (Twitter)'] as const
const CONTENT_TYPES = [
  'Caption',
  'Video Script',
  'Hashtags',
  'Blog Idea',
  'Marketing Copy',
] as const
const TONES = [
  'Casual',
  'Professional',
  'Funny',
  'Inspirational',
  'Bold',
  'Expert',
] as const

// ── Types ─────────────────────────────────────────────────────────────────

export interface FormInputs {
  topic: string
  platform: string
  content_type: string
  tone: string
}

interface GenerateFormProps {
  onGenerate: (inputs: FormInputs) => void
  onRegenerate: () => void
  hasOutput: boolean
  isLoading: boolean
}

// ── Shared input class strings ────────────────────────────────────────────

const inputBase =
  'w-full bg-charcoal border border-slate rounded text-fog text-sm font-inter ' +
  'px-3 py-2.5 focus:outline-none focus:border-ash transition-colors'

const labelBase =
  'block text-[0.72rem] font-inter font-medium tracking-[0.1em] uppercase text-ash mb-1.5'

// ── Component ─────────────────────────────────────────────────────────────

export default function GenerateForm({
  onGenerate,
  onRegenerate,
  hasOutput,
  isLoading,
}: GenerateFormProps) {
  const [topic, setTopic] = useState('')
  const [platform, setPlatform] = useState<string>(PLATFORMS[0])
  const [contentType, setContentType] = useState<string>(CONTENT_TYPES[0])
  const [tone, setTone] = useState<string>(TONES[0])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onGenerate({
      topic,
      platform,
      content_type: contentType,
      tone,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">

      {/* Topic textarea */}
      <div>
        <label htmlFor="topic" className={labelBase}>
          Topic
        </label>
        <textarea
          id="topic"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="e.g. 'Morning routines that boost productivity' or 'My new sustainable skincare line'"
          rows={3}
          className={`${inputBase} resize-none placeholder:text-ash/50`}
        />
      </div>

      {/* Three selects */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div>
          <label htmlFor="platform" className={labelBase}>
            Platform
          </label>
          <select
            id="platform"
            value={platform}
            onChange={(e) => setPlatform(e.target.value)}
            className={inputBase}
          >
            {PLATFORMS.map((p) => (
              <option key={p} value={p}>
                {p}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="content-type" className={labelBase}>
            Content Type
          </label>
          <select
            id="content-type"
            value={contentType}
            onChange={(e) => setContentType(e.target.value)}
            className={inputBase}
          >
            {CONTENT_TYPES.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="tone" className={labelBase}>
            Tone / Style
          </label>
          <select
            id="tone"
            value={tone}
            onChange={(e) => setTone(e.target.value)}
            className={inputBase}
          >
            {TONES.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Meta tags — mono font, ash color, uppercase */}
      <div className="flex flex-wrap gap-x-4 gap-y-1">
        <span className="font-mono text-ash text-[0.72rem] tracking-[0.1em] uppercase">
          ▸ {platform.toUpperCase()}
        </span>
        <span className="font-mono text-ash text-[0.72rem] tracking-[0.1em] uppercase">
          / {contentType.toUpperCase()}
        </span>
        <span className="font-mono text-ash text-[0.72rem] tracking-[0.1em] uppercase">
          / {tone.toUpperCase()}
        </span>
      </div>

      {/* Action buttons */}
      <div className="flex gap-3 pt-1">
        {/* Generate — paper bg, primary emphasis */}
        <button
          type="submit"
          disabled={isLoading}
          className="
            flex-1 bg-paper text-onyx font-inter font-semibold text-sm
            py-3 px-5 rounded
            hover:bg-fog
            active:bg-ash
            transition-colors
            disabled:opacity-50 disabled:cursor-not-allowed
          "
        >
          {isLoading ? 'Generating…' : '✦  Generate'}
        </button>

        {/* Regenerate — secondary, border only */}
        <button
          type="button"
          onClick={onRegenerate}
          disabled={!hasOutput || isLoading}
          title="Regenerate with same inputs"
          className="
            px-4 py-3 border border-slate text-ash text-sm font-mono rounded
            hover:border-fog hover:text-fog
            transition-colors
            disabled:opacity-30 disabled:cursor-not-allowed
          "
        >
          ↻
        </button>
      </div>

    </form>
  )
}
