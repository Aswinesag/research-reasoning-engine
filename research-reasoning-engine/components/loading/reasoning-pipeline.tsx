'use client'

import { motion } from 'framer-motion'
import { CheckCircle2, CircleDashed } from 'lucide-react'

const stages = ['Retrieving Evidence', 'Extracting Entities', 'Building Causal Graph', 'Detecting Conflicts', 'Generating Hypothesis']

export function ReasoningPipeline({ active = false }: { active?: boolean }) {
  return <div className="rounded-2xl border border-cyan-300/15 bg-slate-950/70 p-5"><div className="mb-4 text-sm font-medium text-cyan-200">Reasoning pipeline</div><div className="grid gap-3 md:grid-cols-5">{stages.map((stage, index) => <motion.div key={stage} initial={{ opacity: 0.4 }} animate={{ opacity: active ? [0.55, 1, 0.75] : 1 }} transition={{ duration: 1.2, repeat: active ? Infinity : 0, delay: index * 0.15 }} className="rounded-xl border border-white/10 bg-white/[0.04] p-3 text-xs text-slate-300">{active ? <CircleDashed className="mb-2 h-4 w-4 animate-spin text-cyan-300" /> : <CheckCircle2 className="mb-2 h-4 w-4 text-emerald-300" />}{stage}</motion.div>)}</div></div>
}

