import { useAnalysisStore } from "@/lib/store"
import { Card } from "@/components/ui/card"

export default function MetricsTab() {
  const data = useAnalysisStore((s) => s.data)
  if (!data) return null

  return (
    <div className="grid grid-cols-3 gap-6 mt-6">
      <Card className="p-6 rounded-2xl border bg-white shadow-sm">
        <p className="text-xs text-slate-500 uppercase tracking-wide">
          Mean Weight
        </p>
        <p className="text-2xl font-semibold mt-2">
          {data.metrics.mean_weight}
        </p>
      </Card>
      <Card className="p-4">
        Reinforcement Factor: {data.metrics.reinforcement_factor}
      </Card>
      <Card className="p-4">
        Graph Density: {data.metrics.graph_density}
      </Card>
    </div>
  )
}
