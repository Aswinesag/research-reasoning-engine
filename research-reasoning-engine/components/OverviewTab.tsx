import { useAnalysisStore } from "@/lib/store"
import { Card } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

export default function OverviewTab() {
  const data = useAnalysisStore((s) => s.data)
  if (!data) return null

  return (
    <div className="grid grid-cols-2 gap-4 mt-4">
      <Card className="p-6 rounded-2xl shadow-sm border bg-white">
        <p className="text-3xl font-semibold">Total Edges: {data.overview.total_edges}</p>
        <p className="text-3xl font-semibold">Conflicts: {data.overview.conflicts}</p>
      </Card>

      <Card className="p-6 rounded-2xl shadow-sm border bg-white">
        <div className="mt-6">
          <Progress value={data.overview.confidence} className="h-2" />
          <p className="text-xs text-slate-500 mt-1">
            Confidence Score: {data.overview.confidence}%
          </p>
        </div>
      </Card>

      <Card className="p-6 rounded-2xl shadow-sm border bg-white col-span-2">
        <p className="font-medium">Strongest Chain</p>
        <p>{data.overview.strongest_chain.join(" â†’ ")}</p>
      </Card>
    </div>
  )
}
