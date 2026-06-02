'use client'

import { WorkspaceShell } from '@/components/layout/workspace-shell'
import { useResearchStore } from '@/store/research-store'

export function SavedSessionsView() {
  const sessions = useResearchStore((state) => state.sessions)
  const setResult = useResearchStore((state) => state.setResult)
  return <WorkspaceShell><div className="mb-6"><div className="text-sm text-cyan-200">Saved Sessions View</div><h1 className="mt-2 text-3xl font-semibold text-white">Research memory</h1></div><div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">{sessions.map((session) => <button key={session.id} onClick={() => setResult(session)} className="rounded-3xl border border-white/10 bg-white/[0.05] p-5 text-left transition hover:border-cyan-300/40"><div className="mb-3 inline-flex rounded-full bg-cyan-300/10 px-3 py-1 text-xs text-cyan-200">{session.domain}</div><div className="font-medium text-white">{session.query}</div><div className="mt-4 text-sm text-slate-400">Confidence {Math.round(session.metrics.confidence * 100)}% · {session.metrics.totalNodes} nodes · {session.metrics.conflicts} conflicts</div></button>)}</div></WorkspaceShell>
}

