'use client'

import ReactFlow, { Background, Controls, Edge, MarkerType, MiniMap, Node, Position } from 'reactflow'
import 'reactflow/dist/style.css'
import { useMemo } from 'react'
import { useResearchStore } from '@/store/research-store'

const colors = { supports: '#22d3ee', contradicts: '#fb7185', inferred: '#a78bfa', neutral: '#94a3b8' }

export function ReasoningGraph() {
  const { result, selectEvidence } = useResearchStore()
  const nodes: Node[] = useMemo(() => result.graphNodes.map((node, index) => ({
    id: node.id,
    position: { x: (index % 3) * 250, y: Math.floor(index / 3) * 180 },
    sourcePosition: Position.Right,
    targetPosition: Position.Left,
    data: { label: <div className="min-w-36"><div className="text-sm font-semibold text-white">{node.label}</div><div className="mt-1 text-xs text-slate-400">{Math.round(node.confidence * 100)}% confidence</div></div> },
    style: { border: node.type === 'conflict' ? '1px solid #fb7185' : '1px solid rgba(34,211,238,.35)', background: 'rgba(15,23,42,.92)', borderRadius: 16, padding: 12, color: 'white', boxShadow: '0 20px 50px rgba(0,0,0,.35)' },
  })), [result.graphNodes])

  const edges: Edge[] = useMemo(() => result.graphEdges.map((edge) => ({
    id: edge.id, source: edge.source, target: edge.target, label: `${edge.label} ${Math.round(edge.confidence * 100)}%`, animated: true, type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed, color: colors[edge.polarity] }, style: { stroke: colors[edge.polarity], strokeWidth: 2 }, labelStyle: { fill: '#cbd5e1', fontSize: 11 },
  })), [result.graphEdges])

  return <div className="h-[560px] overflow-hidden rounded-3xl border border-white/10 bg-slate-950/80"><ReactFlow nodes={nodes} edges={edges} fitView onNodeClick={(_, node) => selectEvidence(result.evidence.find((item) => item.nodeIds.includes(node.id)))}><Background color="#334155" gap={24} /><MiniMap nodeColor="#22d3ee" maskColor="rgba(2,6,23,.75)" /><Controls /></ReactFlow></div>
}

