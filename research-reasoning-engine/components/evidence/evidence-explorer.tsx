'use client'

import { useMemo, useState } from 'react'
import { AlertTriangle, Filter, Link2 } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'
import { useResearchStore } from '@/store/research-store'

export function EvidenceExplorer() {
  const { result, selectedEvidence, selectEvidence } = useResearchStore()
  const [filter, setFilter] = useState('all')
  const evidence = useMemo(() => result.evidence.filter((item) => filter === 'all' || (filter === 'conflict' ? item.conflict : item.type === filter)), [result.evidence, filter])
  return <div className="space-y-4"><div className="flex flex-wrap items-center justify-between gap-3"><div><h2 className="text-lg font-semibold">Evidence Explorer</h2><p className="text-sm text-slate-400">Expandable snippets linked to causal graph nodes.</p></div><div className="flex items-center gap-2 rounded-2xl border border-white/10 bg-white/[0.04] px-3 py-2"><Filter className="h-4 w-4 text-slate-500" /><select value={filter} onChange={(event) => setFilter(event.target.value)} className="bg-transparent text-sm text-slate-200 outline-none"><option value="all">All evidence</option><option value="evidence">Evidence</option><option value="inference">Inference</option><option value="unresolved">Unresolved</option><option value="conflict">Conflicts</option></select></div></div><div className="grid gap-3">{evidence.map((item) => <Card key={item.id} onClick={() => selectEvidence(item)} className={`cursor-pointer border-white/10 bg-white/[0.05] text-slate-100 transition hover:border-cyan-300/40 ${selectedEvidence?.id === item.id ? 'ring-1 ring-cyan-300' : ''}`}><CardContent className="p-4"><div className="mb-3 flex items-center justify-between gap-3"><span className="rounded-full bg-cyan-300/10 px-3 py-1 text-xs text-cyan-200">Similarity {Math.round(item.similarity * 100)}%</span>{item.conflict && <span className="flex items-center gap-1 text-xs text-rose-300"><AlertTriangle className="h-3.5 w-3.5" />Conflict</span>}</div><p className="text-sm leading-6 text-slate-300">{item.excerpt}</p><div className="mt-4 flex flex-wrap gap-2 text-xs text-slate-500"><span>{item.source}</span>{item.relations.map((relation) => <span key={relation} className="flex items-center gap-1"><Link2 className="h-3 w-3" />{relation}</span>)}</div></CardContent></Card>)}</div></div>
}

