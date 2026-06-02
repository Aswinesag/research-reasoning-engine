import { create } from "zustand"
import { AnalysisResponse } from "@/types/analysis"

interface AnalysisState {
  data: AnalysisResponse | null
  loading: boolean
  setData: (data: AnalysisResponse | null) => void
  setLoading: (loading: boolean) => void
}

export const useAnalysisStore = create<AnalysisState>((set) => ({
  data: null,
  loading: false,
  setData: (data) => set({ data }),
  setLoading: (loading) => set({ loading }),
}))
