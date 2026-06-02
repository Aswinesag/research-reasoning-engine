'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { ArrowRight, BrainCircuit, GitBranch, Microscope, ShieldCheck, Workflow } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { GraphPreview } from '@/components/landing/graph-preview'

const features = [
  ['Evidence traceability', 'Every claim is linked to retrieved snippets, graph nodes, and confidence weights.'],
  ['Causal graph reasoning', 'Directed pathways expose mechanisms, indirect chains, and uncertainty.'],
  ['Conflict-aware inference', 'Contradictory evidence is separated from unresolved inferred relations.'],
  ['Domain agnostic analysis', 'Designed for biomedical, legal, climate, cyber, finance, and research teams.'],
]

export function LandingPage() {
  return (
    <main className="min-h-screen overflow-hidden bg-[radial-gradient(circle_at_top_left,#1e3a8a55,transparent_34%),linear-gradient(135deg,#020617,#0f172a_55%,#111827)] text-slate-100">
      <section className="relative mx-auto grid max-w-7xl gap-12 px-6 py-20 lg:grid-cols-[1.05fr_.95fr] lg:px-8 lg:py-28">
        <div className="absolute inset-0 -z-0 opacity-30 [background-image:linear-gradient(#ffffff12_1px,transparent_1px),linear-gradient(90deg,#ffffff12_1px,transparent_1px)] [background-size:48px_48px]" />
        <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7 }} className="relative z-10 space-y-8">
          <div className="inline-flex items-center gap-2 rounded-full border border-cyan-400/30 bg-cyan-400/10 px-4 py-2 text-sm text-cyan-200">
            <Microscope className="h-4 w-4" /> Computational research dashboard
          </div>
          <div className="space-y-5">
            <h1 className="max-w-4xl text-5xl font-semibold tracking-tight text-white md:text-7xl">Evidence-backed AI reasoning</h1>
            <p className="max-w-2xl text-lg leading-8 text-slate-300">Transform retrieval outputs into visual causal reasoning, evidence traceability, explainable inference, and structured scientific analysis.</p>
          </div>
          <div className="flex flex-col gap-3 sm:flex-row">
            <Button asChild size="lg" className="bg-cyan-300 text-slate-950 hover:bg-cyan-200">
              <Link href="/workspace">Open Research Workspace <ArrowRight className="ml-2 h-4 w-4" /></Link>
            </Button>
            <Button asChild variant="outline" size="lg" className="border-white/20 bg-white/5 text-white hover:bg-white/10">
              <Link href="/metrics">View System Metrics</Link>
            </Button>
          </div>
          <div className="grid gap-3 sm:grid-cols-3">
            {['Causal graphs', 'Conflict detection', 'Plain English mode'].map((label) => (
              <div key={label} className="rounded-2xl border border-white/10 bg-white/[0.06] p-4 text-sm text-slate-300 shadow-2xl backdrop-blur">{label}</div>
            ))}
          </div>
        </motion.div>
        <motion.div initial={{ opacity: 0, scale: 0.96 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.8, delay: 0.1 }} className="relative z-10">
          <GraphPreview />
        </motion.div>
      </section>

      <section className="mx-auto max-w-7xl px-6 pb-24 lg:px-8">
        <div className="grid gap-5 md:grid-cols-4">
          {features.map(([title, body], index) => (
            <motion.div key={title} initial={{ opacity: 0, y: 18 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: index * 0.08 }}>
              <Card className="h-full border-white/10 bg-white/[0.05] text-slate-100 backdrop-blur-xl">
                <CardHeader><CardTitle className="text-base">{title}</CardTitle></CardHeader>
                <CardContent className="text-sm leading-6 text-slate-400">{body}</CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </section>

      <section className="mx-auto grid max-w-7xl gap-6 px-6 pb-24 lg:grid-cols-3 lg:px-8">
        {[
          [BrainCircuit, 'Retrieve and score evidence', 'Semantic retrieval surfaces the highest-signal snippets across heterogeneous sources.'],
          [GitBranch, 'Build causal structure', 'Entities, mechanisms, outcomes, and conflicts become an inspectable reasoning graph.'],
          [ShieldCheck, 'Explain and test', 'The system reports confidence, falsifiability, support chains, and unresolved contradictions.'],
        ].map(([Icon, title, body]) => {
          const TypedIcon = Icon as typeof BrainCircuit
          return <Card key={title as string} className="border-cyan-300/10 bg-slate-900/70 text-slate-100"><CardHeader><TypedIcon className="mb-4 h-8 w-8 text-cyan-300" /><CardTitle>{title as string}</CardTitle></CardHeader><CardContent className="text-slate-400">{body as string}</CardContent></Card>
        })}
      </section>

      <section className="mx-auto max-w-7xl px-6 pb-24 lg:px-8">
        <div className="rounded-3xl border border-purple-300/20 bg-gradient-to-r from-purple-500/10 to-cyan-500/10 p-8 backdrop-blur-xl md:p-12">
          <div className="mb-8 flex items-center gap-3 text-purple-200"><Workflow className="h-5 w-5" /> Research workflow visualization</div>
          <div className="grid gap-4 md:grid-cols-5">
            {['Query', 'Evidence', 'Graph', 'Conflicts', 'Hypothesis'].map((step, index) => <div key={step} className="rounded-2xl border border-white/10 bg-black/20 p-5"><div className="text-3xl font-semibold text-cyan-200">0{index + 1}</div><div className="mt-3 text-sm text-slate-300">{step}</div></div>)}
          </div>
        </div>
      </section>
    </main>
  )
}

