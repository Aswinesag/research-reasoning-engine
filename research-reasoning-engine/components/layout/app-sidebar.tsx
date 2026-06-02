'use client'

import Link from 'next/link'
import { BarChart3, BookMarked, Download, FlaskConical, GitBranch, History, Home, Save } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useResearchStore } from '@/store/research-store'

const nav = [
  [Home, 'Landing', '/'], [FlaskConical, 'Workspace', '/workspace'], [GitBranch, 'Results', '/results'], [BookMarked, 'Saved Sessions', '/sessions'], [BarChart3, 'System Metrics', '/metrics'],
]

export function AppSidebar() {
  const sessions = useResearchStore((state) => state.sessions)
  return (
    <aside className="flex h-full w-full flex-col border-r border-white/10 bg-slate-950/80 p-5 backdrop-blur-xl">
      <div className="mb-8">
        <div className="text-lg font-semibold text-white">Reasoning Engine</div>
        <div className="text-xs text-slate-500">Explainable AI research workspace</div>
      </div>
      <nav className="space-y-2">
        {nav.map(([Icon, label, href]) => {
          const TypedIcon = Icon as typeof Home
          return <Button key={href as string} asChild variant="ghost" className="w-full justify-start text-slate-300 hover:bg-white/10 hover:text-white"><Link href={href as string}><TypedIcon className="mr-3 h-4 w-4" />{label as string}</Link></Button>
        })}
      </nav>
      <div className="mt-8 space-y-3">
        <div className="flex items-center gap-2 text-xs uppercase tracking-widest text-slate-500"><History className="h-3.5 w-3.5" /> Recent analyses</div>
        {sessions.slice(0, 4).map((session) => <div key={session.id} className="rounded-xl border border-white/10 bg-white/[0.04] p-3 text-xs text-slate-300"><div className="line-clamp-2">{session.query}</div><div className="mt-2 text-slate-500">{session.domain}</div></div>)}
      </div>
      <div className="mt-auto grid grid-cols-2 gap-2 pt-6">
        <Button variant="outline" className="border-white/10 bg-white/5 text-slate-300"><Save className="mr-2 h-4 w-4" />Save</Button>
        <Button variant="outline" className="border-white/10 bg-white/5 text-slate-300"><Download className="mr-2 h-4 w-4" />Export</Button>
      </div>
    </aside>
  )
}

