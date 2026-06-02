'use client'

import { motion } from 'framer-motion'
import { Clipboard, Download, FileText } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { useResearchStore } from '@/store/research-store'

export function HypothesisPanel() {
  const { result, viewMode } = useResearchStore()
  const hypothesis = result.hypothesis
  const rows = viewMode === 'simplified'
    ? [['Plain English', hypothesis.simplified], ['What it means', hypothesis.conclusion], ['How to test it', hypothesis.falsifiability]]
    : [['Generated mechanism', hypothesis.mechanism], ['Inference', hypothesis.inference], ['Conclusion', hypothesis.conclusion], ['Falsifiability', hypothesis.falsifiability]]

  return <Card className="border-white/10 bg-white/[0.05] text-slate-100 backdrop-blur-xl"><CardHeader className="flex flex-row items-start justify-between gap-4"><div><CardTitle className="text-xl">{hypothesis.title}</CardTitle><p className="mt-2 text-sm text-slate-400">Structured hypothesis generated from graph-linked evidence.</p></div><div className="flex gap-2"><Button size="sm" variant="outline" className="border-white/10 bg-white/5"><Clipboard className="h-4 w-4" /></Button><Button size="sm" variant="outline" className="border-white/10 bg-white/5"><FileText className="h-4 w-4" /></Button><Button size="sm" variant="outline" className="border-white/10 bg-white/5"><Download className="h-4 w-4" /></Button></div></CardHeader><CardContent className="space-y-5"><div><div className="mb-2 flex justify-between text-sm"><span className="text-slate-400">Confidence score</span><span className="text-cyan-200">{Math.round(hypothesis.confidence * 100)}%</span></div><Progress value={hypothesis.confidence * 100} /></div>{rows.map(([label, text], index) => <motion.details key={label} open={index < 2} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: index * 0.05 }} className="rounded-2xl border border-white/10 bg-slate-950/60 p-4"><summary className="cursor-pointer text-sm font-medium text-cyan-100">{label}</summary><p className="mt-3 text-sm leading-7 text-slate-300">{text}</p></motion.details>)}</CardContent></Card>
}

