'use client'

import { motion } from 'framer-motion'

const nodes = [
  { x: 16, y: 28, label: 'Evidence' }, { x: 48, y: 18, label: 'Mechanism' }, { x: 78, y: 34, label: 'Outcome' },
  { x: 34, y: 64, label: 'Conflict' }, { x: 68, y: 72, label: 'Hypothesis' },
]

export function GraphPreview() {
  return (
    <div className="relative h-[520px] overflow-hidden rounded-[2rem] border border-white/10 bg-slate-950/70 p-6 shadow-2xl backdrop-blur-xl">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_20%,#22d3ee22,transparent_28%),radial-gradient(circle_at_70%_80%,#a855f722,transparent_30%)]" />
      <svg className="absolute inset-0 h-full w-full">
        {[[0,1],[1,2],[0,3],[3,4],[1,4],[2,4]].map(([a,b]) => <motion.line key={`${a}-${b}`} x1={`${nodes[a].x}%`} y1={`${nodes[a].y}%`} x2={`${nodes[b].x}%`} y2={`${nodes[b].y}%`} stroke={b===3?'#fb7185':'#22d3ee'} strokeWidth="2" strokeDasharray="8 8" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1.5, delay: 0.3 }} />)}
      </svg>
      {nodes.map((node, index) => (
        <motion.div key={node.label} initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: index * 0.12 }} className="absolute -translate-x-1/2 -translate-y-1/2 rounded-2xl border border-cyan-300/20 bg-white/10 px-5 py-4 text-sm shadow-xl backdrop-blur" style={{ left: `${node.x}%`, top: `${node.y}%` }}>
          <div className="mb-2 h-2 w-14 rounded-full bg-gradient-to-r from-cyan-300 to-purple-300" />
          {node.label}
        </motion.div>
      ))}
      <div className="absolute bottom-6 left-6 right-6 rounded-2xl border border-white/10 bg-black/30 p-5 text-sm text-slate-300">
        <div className="mb-2 text-cyan-200">Explainability layer</div>
        Confidence, evidence links, contradictory relations, and falsifiability are surfaced with the graph.
      </div>
    </div>
  )
}

