'use client'

import type { OutputState } from '@/app/page'
import CopyButton from './CopyButton'

interface OutputCardProps {
  state: OutputState
  content: string
}

// ── Shared card base classes ──────────────────────────────────────────────
const cardBase = 'mt-4 bg-charcoal border border-slate rounded-md font-inter'

// ── Lightweight Markdown renderer ────────────────────────────────────────
// Handles: **bold**, *italic*, # headings, - bullets, blank lines

function renderInline(text: string): React.ReactNode[] {
  // Split on **bold** and *italic* (order matters — bold first)
  const tokens = text.split(/(\*\*.*?\*\*|\*.*?\*)/g)
  return tokens.map((token, i) => {
    if (token.startsWith('**') && token.endsWith('**'))
      return <strong key={i} className="text-paper font-semibold">{token.slice(2, -2)}</strong>
    if (token.startsWith('*') && token.endsWith('*'))
      return <em key={i} className="text-fog italic">{token.slice(1, -1)}</em>
    return token
  })
}

function renderMarkdown(text: string): React.ReactNode[] {
  return text.split('\n').map((line, i) => {
    if (line.startsWith('### '))
      return <h3 key={i} className="font-space-grotesk text-paper font-semibold text-base mt-4 mb-0.5">{renderInline(line.slice(4))}</h3>
    if (line.startsWith('## '))
      return <h2 key={i} className="font-space-grotesk text-paper font-semibold text-lg mt-5 mb-1">{renderInline(line.slice(3))}</h2>
    if (line.startsWith('# '))
      return <h1 key={i} className="font-space-grotesk text-paper font-bold text-xl mt-5 mb-1">{renderInline(line.slice(2))}</h1>
    if (line.match(/^[-•]\s/))
      return <li key={i} className="ml-5 text-fog leading-relaxed list-disc">{renderInline(line.slice(2))}</li>
    if (line.trim() === '')
      return <div key={i} className="h-3" />
    return <p key={i} className="text-fog leading-[1.75]">{renderInline(line)}</p>
  })
}

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
      {/* Rendered markdown content */}
      <div className="text-sm space-y-0.5">
        {renderMarkdown(content)}
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
