'use client'

import { useEffect } from 'react'
import { FlaskConical } from 'lucide-react'
import { WorkspaceShell } from '@/components/layout/workspace-shell'
import { QueryBar } from '@/components/workspace/query-bar'
import { HypothesisPanel } from '@/components/hypothesis/hypothesis-panel'
import { ReasoningGraph } from '@/components/graph/reasoning-graph'
import { EvidenceExplorer } from '@/components/evidence/evidence-explorer'
import { MetricsDashboard } from '@/components/metrics/metrics-dashboard'
import { SupportingChains } from '@/components/chains/supporting-chains'
import { ConflictAnalysis } from '@/components/conflicts/conflict-analysis'
import { ReasoningPipeline } from '@/components/loading/reasoning-pipeline'
import { useResearchResult } from '@/hooks/use-research'
import { useResearchStore } from '@/store/research-store'

export function ResearchWorkspace() {
  const { currentJobId, analysisStatus, setResult, setAnalysisStatus } = useResearchStore()
  const jobQuery = useResearchResult(currentJobId ?? '')
  const jobProgress = jobQuery.data?.progress ?? (analysisStatus === 'processing' ? 0 : 100)
  const jobStage = jobQuery.data?.stage ?? analysisStatus

  useEffect(() => {
    if (!jobQuery.data) return

    if (jobQuery.data.status === 'complete' && jobQuery.data.result) {
      setResult(jobQuery.data.result)
      setAnalysisStatus('complete')
    }

    if (jobQuery.data.status === 'failed') {
      setAnalysisStatus('failed')
    }
  }, [jobQuery.data, setAnalysisStatus, setResult])

  return (
    <WorkspaceShell>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 text-cyan-200">
            <FlaskConical className="h-5 w-5" /> Research Workspace
          </div>
          <h1 className="mt-2 text-3xl font-semibold text-white">Structured reasoning over evidence</h1>
        </div>
        {currentJobId ? (
          <div className="rounded-2xl border border-cyan-300/15 bg-cyan-300/10 px-4 py-2 text-right text-xs text-cyan-100">
            <div className="font-medium uppercase tracking-widest">Job</div>
            <div>{jobStage}</div>
            <div>{jobProgress}%</div>
          </div>
        ) : null}
      </div>

      <div className="space-y-6">
        <QueryBar />
        <ReasoningPipeline
          active={analysisStatus === 'processing' || jobQuery.isFetching}
          progress={jobProgress}
          stage={jobStage}
        />
        <div className="grid gap-6 xl:grid-cols-[.95fr_1.05fr]">
          <HypothesisPanel />
          <ReasoningGraph />
        </div>
        <MetricsDashboard />
        <div className="grid gap-6 xl:grid-cols-[1fr_.9fr]">
          <EvidenceExplorer />
          <SupportingChains />
        </div>
        <ConflictAnalysis />
        <section className="rounded-3xl border border-white/10 bg-white/[0.05] p-5">
          <h2 className="text-lg font-semibold">Testability Section</h2>
          <p className="mt-2 text-sm leading-6 text-slate-400">
            Convert the hypothesis into measurable experiments: define intervention, expected pathway suppression,
            observable markers, and disconfirming evidence. This keeps the reasoning output falsifiable instead of
            merely plausible.
          </p>
        </section>
      </div>
    </WorkspaceShell>
  )
}
