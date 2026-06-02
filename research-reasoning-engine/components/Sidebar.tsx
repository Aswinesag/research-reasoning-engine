"use client"

import { useState } from "react"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { runAnalysis } from "@/lib/api"
import { useAnalysisStore } from "@/lib/store"
import LoadingTimeline from "./LoadingTimeline"

export default function Sidebar() {
  const [query, setQuery] = useState("")
  const { setData, setLoading, loading } = useAnalysisStore()

  const handleRun = async () => {
    if (!query) return
    setLoading(true)
    try {
      const result = await runAnalysis(query)
      setData(result)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-full p-6 flex flex-col gap-6">
      <div>
        <h2 className="text-lg font-semibold tracking-tight">
          Research Reasoning Engine
        </h2>
        <p className="text-xs text-slate-500 mt-1">
          Graph-grounded hypothesis generation
        </p>
      </div>

      <div className="flex-1 flex flex-col gap-4">
        <Textarea
          className="min-h-[120px] resize-none rounded-xl"
          placeholder="Enter a research question..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />

        <Button className="w-full rounded-xl" onClick={handleRun} disabled={loading}>
          {loading ? "Analyzing..." : "Run Analysis"}
        </Button>

        {loading && <LoadingTimeline />}
      </div>
    </div>
  )
}
