import axios from "axios"
import { AnalysisResponse } from "@/types/analysis"

export const runAnalysis = async (
  query: string
): Promise<AnalysisResponse> => {
  const response = await axios.post(
    "http://localhost:8000/analyze",
    { query }
  )
  return response.data
}
