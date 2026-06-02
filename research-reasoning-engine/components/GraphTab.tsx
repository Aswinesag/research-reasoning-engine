"use client"

import ReactFlow, {
  Background,
  Controls,
} from "reactflow"
import "reactflow/dist/style.css"
import { useAnalysisStore } from "@/lib/store"

export default function GraphTab() {
  const data = useAnalysisStore((s) => s.data)
  if (!data) return null

  const nodes = data.graph.nodes.map((n) => ({
    id: n.id,
    data: { label: n.label },
    position: {
      x: Math.random() * 400,
      y: Math.random() * 400,
    },
    style: {
      padding: 12,
      borderRadius: 16,
      border: "1px solid #e2e8f0",
      background: "#f8fafc",
      fontSize: 12,
    },
  }))

  const edges = data.graph.edges.map((e) => ({
    id: e.id,
    source: e.source,
    target: e.target,
    style: {
      stroke: e.conflict
        ? "#f59e0b"
        : e.polarity === "+"
        ? "#16a34a"
        : "#dc2626",
      strokeWidth: 2,
    },
  }))

  return (
    <div className="h-[650px] rounded-2xl border bg-white shadow-sm mt-6">
      <div className="mb-4 p-4">
        <h3 className="text-lg font-semibold">Causal Structure</h3>
        <p className="text-sm text-slate-500">
          Extracted relationships across evidence sources
        </p>
      </div>
      <ReactFlow nodes={nodes} edges={edges} fitView>
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  )
}
