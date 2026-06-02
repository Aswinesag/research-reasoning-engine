'use client'

import { Bar, BarChart, CartesianGrid, Cell, Line, LineChart, RadialBar, RadialBarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useResearchStore } from '@/store/research-store'

export function MetricsDashboard() {
  const metrics = useResearchStore((state) => state.result.metrics)
  const radial = [{ name: 'confidence', value: Math.round(metrics.confidence * 100), fill: '#22d3ee' }]
  const bars = [
    { name: 'Nodes', value: metrics.totalNodes }, { name: 'Edges', value: metrics.totalEdges }, { name: 'Conflicts', value: metrics.conflicts }, { name: 'Depth', value: metrics.reasoningDepth },
  ]
  const line = [
    { step: 'Retrieve', value: 62 }, { step: 'Entity', value: 71 }, { step: 'Graph', value: 78 }, { step: 'Conflict', value: 74 }, { step: 'Hypothesis', value: Math.round(metrics.confidence * 100) },
  ]
  return <div className="grid gap-4 xl:grid-cols-3"><Card className="border-white/10 bg-white/[0.05] text-slate-100"><CardHeader><CardTitle>Confidence</CardTitle></CardHeader><CardContent className="h-56"><ResponsiveContainer><RadialBarChart innerRadius="70%" outerRadius="100%" data={radial} startAngle={90} endAngle={-270}><RadialBar dataKey="value" cornerRadius={12} background /><text x="50%" y="50%" textAnchor="middle" dominantBaseline="middle" className="fill-cyan-100 text-3xl font-semibold">{radial[0].value}%</text></RadialBarChart></ResponsiveContainer></CardContent></Card><Card className="border-white/10 bg-white/[0.05] text-slate-100"><CardHeader><CardTitle>Graph Structure</CardTitle></CardHeader><CardContent className="h-56"><ResponsiveContainer><BarChart data={bars}><CartesianGrid strokeDasharray="3 3" stroke="#1e293b" /><XAxis dataKey="name" stroke="#94a3b8" fontSize={12} /><YAxis stroke="#94a3b8" fontSize={12} /><Tooltip contentStyle={{ background: '#020617', border: '1px solid #334155' }} /> <Bar dataKey="value" radius={[8,8,0,0]}>{bars.map((_, index) => <Cell key={index} fill={index === 2 ? '#fb7185' : '#22d3ee'} />)}</Bar></BarChart></ResponsiveContainer></CardContent></Card><Card className="border-white/10 bg-white/[0.05] text-slate-100"><CardHeader><CardTitle>Reasoning Quality</CardTitle></CardHeader><CardContent className="h-56"><ResponsiveContainer><LineChart data={line}><CartesianGrid strokeDasharray="3 3" stroke="#1e293b" /><XAxis dataKey="step" stroke="#94a3b8" fontSize={12} /><YAxis stroke="#94a3b8" fontSize={12} /><Tooltip contentStyle={{ background: '#020617', border: '1px solid #334155' }} /><Line dataKey="value" type="monotone" stroke="#a78bfa" strokeWidth={3} dot={{ fill: '#22d3ee' }} /></LineChart></ResponsiveContainer></CardContent></Card></div>
}

