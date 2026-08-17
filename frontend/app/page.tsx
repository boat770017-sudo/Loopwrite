'use client'

import { useState } from 'react'
import GenerateForm, { type FormInputs } from '@/components/GenerateForm'
import OutputCard from '@/components/OutputCard'
import { generateContent } from '@/lib/api'

export type OutputState = 'empty' | 'loading' | 'success' | 'error'

export default function Home() {
  const [output, setOutput] = useState('')
  const [outputState, setOutputState] = useState<OutputState>('empty')
  const [lastInputs, setLastInputs] = useState<FormInputs | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  // ── Core generation handler ────────────────────────────────────────────────
  const handleGenerate = async (inputs: FormInputs, variationSeed?: number) => {
    setIsLoading(true)
    setOutputState('loading')
    setLastInputs(inputs)

    try {
      const result = await generateContent(inputs, variationSeed)
      setOutput(result)
      setOutputState('success')
    } catch (err: unknown) {
      const message =
        err instanceof Error
          ? err.message
          : 'Generation failed — check your API key and try again.'
      setOutput(message)
      setOutputState('error')
    } finally {
      setIsLoading(false)
    }
  }

  // ── Regenerate — same inputs, different variation seed ─────────────────────
  const handleRegenerate = () => {
    if (!lastInputs) return
    const seed = Math.floor(Math.random() * 9000) + 1000
    handleGenerate(lastInputs, seed)
  }

  return (
    <main className="min-h-screen bg-onyx py-10 px-5">
      <div className="max-w-[780px] mx-auto">

        {/* ── Header ─────────────────────────────────────────────────── */}
        <header className="mb-8">
          <p className="font-mono text-ash text-[0.72rem] tracking-[0.18em] uppercase mb-1.5">
            AI Content Generator
          </p>
          <h1 className="font-space-grotesk text-paper text-[2.4rem] font-bold tracking-[-0.02em] leading-none mb-2">
            Loopwrite
          </h1>
          <p className="text-ash text-sm font-inter leading-relaxed">
            AI content for creators — captions, scripts, hashtags &amp; more.
          </p>
        </header>

        <div className="border-t border-slate mb-8" />

        {/* ── Input form ─────────────────────────────────────────────── */}
        <section aria-label="Content inputs">
          <p className="font-mono text-ash text-[0.72rem] tracking-[0.14em] uppercase mb-4">
            Content Inputs
          </p>
          <GenerateForm
            onGenerate={handleGenerate}
            onRegenerate={handleRegenerate}
            hasOutput={outputState === 'success'}
            isLoading={isLoading}
          />
        </section>

        <div className="border-t border-slate mt-8 mb-5" />

        {/* ── Output panel ────────────────────────────────────────────── */}
        <section aria-label="Generated output">
          <p className="font-mono text-ash text-[0.72rem] tracking-[0.14em] uppercase mb-1">
            Generated Output
          </p>
          <OutputCard state={outputState} content={output} />
        </section>

        {/* ── Footer ──────────────────────────────────────────────────── */}
        <footer className="mt-20 text-center">
          <span className="font-mono text-ash text-[0.68rem] tracking-[0.08em]">
            Loopwrite · AI Content Generator
          </span>
        </footer>

      </div>
    </main>
  )
}
