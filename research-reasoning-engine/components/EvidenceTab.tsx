import { useAnalysisStore } from "@/lib/store"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

export default function EvidenceTab() {
  const data = useAnalysisStore((s) => s.data)
  if (!data) return null

  return (
    <div className="space-y-4 mt-4">
      {data.evidence.map((item) => (
        <Card className="p-6 rounded-2xl border bg-white hover:shadow-md transition-shadow duration-200" key={item.id}>
          <div className="flex justify-between items-center mb-4">
            <span className="font-medium text-slate-800">
              {item.doc_id}
            </span>
            <Badge variant="outline">
              Score {item.score.toFixed(2)}
            </Badge>
          </div>

          <p className="text-sm text-slate-600 leading-relaxed mt-3">
            {item.excerpt}
          </p>

          <div className="flex gap-2 mt-4 flex-wrap">
            {item.entities.map((e) => (
              <Badge key={e} variant="secondary" className="bg-slate-100 text-slate-700 border border-slate-200">
                {e}
              </Badge>
            ))}
          </div>
        </Card>
      ))}
    </div>
  )
}
