'use client'

import { motion } from 'framer-motion'
import { CheckCircle2, CircleDashed } from 'lucide-react'
import { Progress } from '@/components/ui/progress'

const stages = [
  'Retrieving Evidence',
  'Extracting Entities',
  'Building Causal Graph',
  'Detecting Conflicts',
  'Generating Hypothesis',
]

export function ReasoningPipeline({
  active = false,
  progress = 0,
  stage = 'idle',
}: {
  active?: boolean
  progress?: number
  stage?: string
}) {
  const normalizedProgress = Math.max(0, Math.min(progress, 100))

  return (
    <div className="rounded-2xl border border-cyan-300/15 bg-slate-950/70 p-5">
      <div className="mb-4 flex items-center justify-between gap-4">
        <div className="text-sm font-medium text-cyan-200">Reasoning pipeline</div>
        <div className="text-xs text-slate-400">{stage}</div>
      </div>
      <div className="mb-4">
        <Progress value={normalizedProgress} />
        <div className="mt-2 text-xs text-slate-400">{normalizedProgress}% complete</div>
      </div>
      <div className="grid gap-3 md:grid-cols-5">
        {stages.map((item, index) => {
          const completed = normalizedProgress >= (index + 1) * 20
          const current = stage.toLowerCase().includes(item.toLowerCase().split(' ')[0])
          return (
            <motion.div
              key={item}
              initial={{ opacity: 0.4 }}
              animate={{ opacity: active ? [0.55, 1, 0.75] : 1 }}
              transition={{ duration: 1.2, repeat: active ? Infinity : 0, delay: index * 0.15 }}
              className={`rounded-xl border p-3 text-xs ${
                current ? 'border-cyan-300/50 bg-cyan-300/10 text-white' : 'border-white/10 bg-white/[0.04] text-slate-300'
              }`}
            >
              {completed ? (
                <CheckCircle2 className="mb-2 h-4 w-4 text-emerald-300" />
              ) : (
                <CircleDashed className="mb-2 h-4 w-4 animate-spin text-cyan-300" />
              )}
              {item}
            </motion.div>
          )
        })}
      </div>
    </div>
  )
}

