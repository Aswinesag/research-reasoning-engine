export default function LoadingTimeline() {
  const steps = [
    "Retrieving evidence",
    "Extracting causal relations",
    "Building causal graph",
    "Detecting conflicts",
    "Generating hypothesis",
  ]

  return (
    <div className="mt-6 space-y-3 text-sm text-slate-600">
      {steps.map((step) => (
        <div key={step} className="flex items-center gap-2">
          <div className="h-2 w-2 bg-blue-500 rounded-full animate-pulse" />
          <span>{step}...</span>
        </div>
      ))}
    </div>
  )
}
