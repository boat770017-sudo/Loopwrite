import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './lib/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      // ── Monochrome palette — single source of truth ──────────────────
      colors: {
        onyx:    '#0E0E10',   // App background
        charcoal:'#1A1A1D',   // Card / input surfaces
        slate:   '#3A3A3F',   // Borders, dividers, disabled
        ash:     '#8B8B8F',   // Secondary/muted text
        fog:     '#E8E8EA',   // Primary body text
        paper:   '#FFFFFF',   // Headlines, primary buttons, emphasis
      },
      // ── Typography ───────────────────────────────────────────────────
      fontFamily: {
        'space-grotesk': ['var(--font-space-grotesk)', 'sans-serif'],
        'inter':         ['var(--font-inter)', 'sans-serif'],
        'mono':          ['var(--font-ibm-plex-mono)', 'monospace'],
      },
      // ── Animations ───────────────────────────────────────────────────
      animation: {
        'pulse-opacity': 'pulse-opacity 1.4s ease-in-out infinite',
      },
      keyframes: {
        'pulse-opacity': {
          '0%, 100%': { opacity: '1' },
          '50%':      { opacity: '0.35' },
        },
      },
      // ── Max border-radius cap at 6px per spec ────────────────────────
      borderRadius: {
        DEFAULT: '4px',
        md:      '6px',
      },
    },
  },
  plugins: [],
}

export default config
