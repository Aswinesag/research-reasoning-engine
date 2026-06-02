'use client'

import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid } from 'recharts'
import { WorkspaceShell } from '@/components/layout/workspace-shell'
import { useSystemMetrics } from '@/hooks/use-research'

export function SystemMetricsView() {
  const { data } = useSystemMetrics()
  const latency = (data?.latency ?? [120, 138, 101, 156, 132, 118]).map((value: number, index: number) => ({ index: index + 1, value }))
  return <WorkspaceShell><div className="mb-6"><div className="text-sm text-cyan-200">System Metrics View</div><h1 className="mt-2 text-3xl font-semibold text-white">Reasoning system telemetry</h1></div><div className="grid gap-4 md:grid-cols-3">{[['Retrieval quality', data?.retrievalQuality ?? .84], ['Graph completeness', data?.graphCompleteness ?? .78], ['Conflict precision', data?.conflictPrecision ?? .71]].map(([label, value]) => <div key={label as string} className="rounded-3xl border border-white/10 bg-white/[0.05] p-6"><div className="text-sm text-slate-400">{label as string}</div><div className="mt-3 text-4xl font-semibold text-cyan-200">{Math.round((value as number) * 100)}%</div></div>)}</div><div className="mt-6 rounded-3xl border border-white/10 bg-white/[0.05] p-6"><h2 className="mb-4 text-lg font-semibold">API latency trend</h2><div className="h-80"><ResponsiveContainer><LineChart data={latency}><CartesianGrid strokeDasharray="3 3" stroke="#1e293b" /><XAxis dataKey="index" stroke="#94a3b8" /><YAxis stroke="#94a3b8" /><Tooltip contentStyle={{ background: '#020617', border: '1px solid #334155' }} /><Line dataKey="value" stroke="#22d3ee" strokeWidth={3} dot={{ fill: '#a78bfa' }} /></LineChart></ResponsiveContainer></div></div></WorkspaceShell>
}

