'use client'

import { ArrowDown, Sparkles } from 'lucide-react'
import { useResearchStore } from '@/store/research-store'

export function SupportingChains() {
  const chains = useResearchStore((state) => state.result.supportingChains)
  return <div className="space-y-4"><div><h2 className="text-lg font-semibold">Supporting Chains</h2><p className="text-sm text-slate-400">Strongest causal pathways and inferred relationships.</p></div><div className="grid gap-4 lg:grid-cols-2">{chains.map((chain) => <div key={chain.id} className="rounded-3xl border border-white/10 bg-white/[0.05] p-5"><div className="mb-4 flex items-center justify-between"><div className="font-medium text-white">{chain.title}</div><div className="rounded-full bg-purple-300/10 px-3 py-1 text-xs text-purple-200">{Math.round(chain.strength * 100)}% strength</div></div><div className="space-y-2">{chain.path.map((item, index) => <div key={`${chain.id}-${item}`} className="flex flex-col items-center rounded-xl border border-white/10 bg-slate-950/50 p-3 text-sm text-slate-200">{item}{index < chain.path.length - 1 && <ArrowDown className="mt-2 h-4 w-4 text-cyan-300" />}</div>)}</div><p className="mt-4 text-sm leading-6 text-slate-400">{chain.explanation}</p>{chain.inferred && <div className="mt-3 flex items-center gap-2 text-xs text-purple-200"><Sparkles className="h-3.5 w-3.5" />Contains inferred relationship</div>}</div>)}</div></div>
}

