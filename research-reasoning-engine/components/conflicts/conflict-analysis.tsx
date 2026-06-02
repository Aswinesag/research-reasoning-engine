'use client'

import { AlertTriangle, HelpCircle, Scale } from 'lucide-react'
import { useResearchStore } from '@/store/research-store'

export function ConflictAnalysis() {
  const conflicts = useResearchStore((state) => state.result.conflicts)
  return <div className="space-y-4"><div><h2 className="text-lg font-semibold">Conflict Analysis</h2><p className="text-sm text-slate-400">Contradictory relations and unresolved uncertainty indicators.</p></div>{conflicts.map((conflict) => <div key={conflict.id} className="rounded-3xl border border-rose-300/20 bg-rose-950/20 p-5"><div className="mb-4 flex items-center gap-2 text-rose-200"><AlertTriangle className="h-5 w-5" />{conflict.relation}</div><div className="grid gap-4 md:grid-cols-3"><div className="rounded-2xl border border-emerald-300/15 bg-emerald-300/5 p-4"><Scale className="mb-2 h-4 w-4 text-emerald-300" /><div className="text-xs uppercase text-emerald-200">Evidence</div><p className="mt-2 text-sm text-slate-300">{conflict.evidence}</p></div><div className="rounded-2xl border border-rose-300/15 bg-rose-300/5 p-4"><AlertTriangle className="mb-2 h-4 w-4 text-rose-300" /><div className="text-xs uppercase text-rose-200">Contradiction</div><p className="mt-2 text-sm text-slate-300">{conflict.contradiction}</p></div><div className="rounded-2xl border border-purple-300/15 bg-purple-300/5 p-4"><HelpCircle className="mb-2 h-4 w-4 text-purple-300" /><div className="text-xs uppercase text-purple-200">Uncertainty</div><p className="mt-2 text-3xl font-semibold text-white">{Math.round(conflict.uncertainty * 100)}%</p></div></div></div>)}</div>
}

