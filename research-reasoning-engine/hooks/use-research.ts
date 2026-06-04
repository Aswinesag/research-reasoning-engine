import { useMutation, useQuery } from '@tanstack/react-query'
import { getResearchResult, getSystemMetrics, runResearch } from '@/services/api'
import { ResearchRequest } from '@/types/research'

export function useRunResearch() {
  return useMutation({
    mutationFn: (request: ResearchRequest) => runResearch(request),
  })
}

export function useResearchResult(id: string) {
  return useQuery({
    queryKey: ['research-result', id],
    queryFn: () => getResearchResult(id),
    enabled: Boolean(id),
    refetchInterval: (query) => {
      const status = query.state.data?.status
      return status === 'complete' || status === 'failed' ? false : 2000
    },
  })
}

export function useSystemMetrics() {
  return useQuery({ queryKey: ['system-metrics'], queryFn: getSystemMetrics })
}

