'use client'

import { FormEvent } from 'react'
import { Search, SlidersHorizontal } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useRunResearch } from '@/hooks/use-research'
import { useResearchStore } from '@/store/research-store'
import { Domain } from '@/types/research'
import { toResearchResult } from '@/services/api'

const domains: Domain[] = ['biomedical', 'legal', 'climate', 'cybersecurity', 'finance', 'general']

export function QueryBar() {
  const {
    activeQuery,
    domain,
    depth,
    viewMode,
    setQuery,
    setDomain,
    setDepth,
    setViewMode,
    setResult,
    setAnalysisStatus,
    setCurrentJobId,
  } = useResearchStore()
  const mutation = useRunResearch()

  async function submit(event: FormEvent) {
    event.preventDefault()
    setAnalysisStatus('processing')
    setCurrentJobId(undefined)
    const response = await mutation.mutateAsync({ query: activeQuery, domain, depth, simplified: viewMode === 'simplified' })
    if (response.status === 'processing' && response.job_id) {
      setCurrentJobId(response.job_id)
    }
    setResult(toResearchResult(response, { query: activeQuery, domain, depth, simplified: viewMode === 'simplified' }))
    setAnalysisStatus(response.status)
  }

  return <form onSubmit={submit} className="rounded-3xl border border-white/10 bg-white/[0.05] p-4 shadow-2xl backdrop-blur-xl"><div className="grid gap-3 xl:grid-cols-[1fr_160px_160px_210px_auto]"><label className="relative"><Search className="absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" /><input value={activeQuery} onChange={(event) => setQuery(event.target.value)} placeholder="Ask a research reasoning question..." className="h-12 w-full rounded-2xl border border-white/10 bg-slate-950/70 pl-11 pr-4 text-sm text-white outline-none transition focus:border-cyan-300/50" /></label><select value={domain} onChange={(event) => setDomain(event.target.value as Domain)} className="h-12 rounded-2xl border border-white/10 bg-slate-950/70 px-4 text-sm text-white outline-none">{domains.map((item) => <option key={item}>{item}</option>)}</select><select value={depth} onChange={(event) => setDepth(Number(event.target.value))} className="h-12 rounded-2xl border border-white/10 bg-slate-950/70 px-4 text-sm text-white outline-none"><option value="2">Depth 2</option><option value="3">Depth 3</option><option value="4">Depth 4</option><option value="5">Depth 5</option></select><div className="grid grid-cols-2 rounded-2xl border border-white/10 bg-slate-950/70 p-1 text-xs"><button type="button" onClick={() => setViewMode('research')} className={`rounded-xl px-3 ${viewMode === 'research' ? 'bg-cyan-300 text-slate-950' : 'text-slate-400'}`}>Research</button><button type="button" onClick={() => setViewMode('simplified')} className={`rounded-xl px-3 ${viewMode === 'simplified' ? 'bg-cyan-300 text-slate-950' : 'text-slate-400'}`}>Simplified</button></div><Button disabled={mutation.isPending} className="h-12 rounded-2xl bg-cyan-300 text-slate-950 hover:bg-cyan-200"><SlidersHorizontal className="mr-2 h-4 w-4" />Analyze</Button></div></form>
}

