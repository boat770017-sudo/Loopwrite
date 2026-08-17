'use client'

import type { OutputState } from '@/app/page'
import CopyButton from './CopyButton'

interface OutputCardProps {
  state: OutputState
  content: string
}

// ── Shared card base classes ──────────────────────────────────────────────
const cardBase = 'mt-4 bg-charcoal border border-slate rounded-md font-inter'

// ── Sub-components ────────────────────────────────────────────────────────

function EmptyState() {
  return (
    <div
      className="
        mt-4 border border-dashed border-slate rounded-md
        py-14 px-8 text-center
      "
    >
      <div className="text-2xl mb-3 opacity-40 text-fog select-none">✦</div>
      <p className="text-ash text-sm font-inter">
        Fill in a topic and hit{' '}
        <strong className="text-fog font-semibold">Generate</strong> to see
        your content here.
      </p>
    </div>
  )
}

function LoadingState() {
  return (
    <div className={`${cardBase} py-12 text-center`}>
      <p className="font-mono text-paper text-sm tracking-[0.1em] animate-pulse-opacity">
        GENERATING  ···
      </p>
    </div>
  )
}

function ErrorState({ content }: { content: string }) {
  return (
    <div
      className={`
        ${cardBase}
        border-l-2 border-l-paper
        px-7 py-6
      `}
    >
      <p className="text-fog text-sm font-semibold leading-relaxed">
        ! {content}
      </p>
    </div>
  )
}

function SuccessState({ content }: { content: string }) {
  const wordCount = content.trim().split(/\s+/).filter(Boolean).length
  const charCount = content.length

  return (
    <div
      className={`
        ${cardBase}
        border-l-2 border-l-paper
        px-7 py-6
      `}
    >
      {/* Content — preserve whitespace for multi-line output */}
      <div className="text-fog text-sm leading-[1.75] whitespace-pre-wrap break-words">
        {content}
      </div>

      {/* Footer row: copy button + word/char count */}
      <div className="mt-6 flex items-center justify-between">
        <CopyButton text={content} />
        <span className="font-mono text-ash text-[0.72rem] tracking-[0.06em]">
          {wordCount} words · {charCount} chars
        </span>
      </div>
    </div>
  )
}

// ── Main component ────────────────────────────────────────────────────────

export default function OutputCard({ state, content }: OutputCardProps) {
  switch (state) {
    case 'empty':   return <EmptyState />
    case 'loading': return <LoadingState />
    case 'error':   return <ErrorState content={content} />
    case 'success': return <SuccessState content={content} />
  }
}
