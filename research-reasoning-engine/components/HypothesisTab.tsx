import { useAnalysisStore } from "@/lib/store"
import { Card } from "@/components/ui/card"

export default function HypothesisTab() {
  const data = useAnalysisStore((s) => s.data)
  if (!data) return null

  return (
    <div className="space-y-6 mt-4">
      <Card className="p-6 rounded-2xl border bg-white shadow-sm">
        <h3 className="text-lg font-semibold tracking-tight">Mechanistic Hypothesis</h3>
        <p className="mt-3 text-slate-700 leading-relaxed">{data.hypothesis.mechanism}</p>
      </Card>

      <Card className="p-6 rounded-2xl border bg-white shadow-sm">
        <h3 className="text-lg font-semibold tracking-tight">Supporting Chains</h3>
        <div className="mt-4 space-y-2 text-sm">
          {data.hypothesis.supporting_chains.map((chain, i) => (
            <p key={i}>{chain.join(" â†’ ")}</p>
          ))}
        </div>
      </Card>

      <Card className="p-6 rounded-2xl border bg-white shadow-sm">
        <h3 className="text-lg font-semibold tracking-tight">Testable Predictions</h3>
        <ul className="list-disc pl-6">
          {data.hypothesis.testable_predictions.map((p, i) => (
            <li key={i}>{p}</li>
          ))}
        </ul>
      </Card>
    </div>
  )
}
