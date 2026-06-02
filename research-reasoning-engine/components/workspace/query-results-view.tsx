'use client'

import { WorkspaceShell } from '@/components/layout/workspace-shell'
import { HypothesisPanel } from '@/components/hypothesis/hypothesis-panel'
import { ReasoningGraph } from '@/components/graph/reasoning-graph'
import { EvidenceExplorer } from '@/components/evidence/evidence-explorer'
import { MetricsDashboard } from '@/components/metrics/metrics-dashboard'
import { SupportingChains } from '@/components/chains/supporting-chains'
import { ConflictAnalysis } from '@/components/conflicts/conflict-analysis'

export function QueryResultsView() {
  return <WorkspaceShell><div className="mb-6"><div className="text-sm text-cyan-200">Query Results View</div><h1 className="mt-2 text-3xl font-semibold text-white">Explainable inference report</h1></div><div className="space-y-6"><HypothesisPanel /><ReasoningGraph /><MetricsDashboard /><EvidenceExplorer /><SupportingChains /><ConflictAnalysis /></div></WorkspaceShell>
}

