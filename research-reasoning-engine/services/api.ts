import axios from 'axios'
import { mockResearchResult } from '@/lib/mock-data'
import { ResearchRequest, ResearchResult } from '@/types/research'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000',
  timeout: 120_000,
})

function normalizeBackendResult(data: any, request: ResearchRequest): ResearchResult {
  if (data?.hypothesis?.title && data?.graphNodes) return data as ResearchResult

  const graphNodes = (data?.graph?.nodes ?? []).map((node: any) => ({
    id: String(node.id),
    label: String(node.label ?? node.id),
    type: 'entity' as const,
    confidence: Math.min(Number(node.frequency ?? 1) / 5, 1),
    summary: `Referenced ${node.frequency ?? 1} time(s) in extracted relations.`,
  }))

  const graphEdges = (data?.graph?.edges ?? []).map((edge: any) => ({
    id: String(edge.id),
    source: String(edge.source),
    target: String(edge.target),
    label: String(edge.polarity ?? 'relates to'),
    confidence: Number(edge.weight ?? 0.5),
    polarity: edge.conflict ? 'contradicts' : 'supports',
  }))

  const evidence = (data?.evidence ?? []).map((item: any) => ({
    id: String(item.id),
    excerpt: String(item.excerpt ?? ''),
    similarity: Number(item.score ?? 0),
    source: String(item.doc_id ?? 'retrieved document'),
    supportingRelations: [],
    relations: (item.entities ?? []).slice(0, 3),
    nodeIds: (item.entities ?? []).map(String),
    conflict: Boolean(item.conflict),
    type: item.conflict ? 'unresolved' : 'evidence',
  }))

  const chains = data?.hypothesis?.supporting_chains ?? []
  const confidence = Number(data?.overview?.confidence ?? 0) > 1 ? Number(data?.overview?.confidence ?? 0) / 100 : Number(data?.overview?.confidence ?? 0.5)

  return {
    id: `session-${Date.now()}`,
    query: request.query,
    domain: request.domain,
    createdAt: new Date().toISOString(),
    hypothesis: {
      title: 'Evidence-backed reasoning hypothesis',
      mechanism: String(data?.hypothesis?.mechanism ?? 'No mechanism returned.'),
      inference: chains.length ? `Strongest chain: ${chains[0].join(' -> ')}` : 'No supporting chain was returned by the backend.',
      conclusion: String(data?.hypothesis?.mechanism ?? 'Insufficient structured evidence retrieved.'),
      falsifiability: 'Test the strongest extracted relation with targeted intervention and disconfirming evidence checks.',
      confidence,
      simplified: String(data?.hypothesis?.mechanism ?? 'The system found limited evidence for this question.'),
    },
    evidence,
    graphNodes,
    graphEdges,
    metrics: {
      confidence,
      graphDensity: Number(data?.metrics?.graph_density ?? 0),
      totalNodes: graphNodes.length,
      totalEdges: graphEdges.length,
      conflicts: Number(data?.overview?.conflicts ?? 0),
      evidenceUsage: evidence.length ? evidence.filter((item: any) => item.type === 'evidence').length / evidence.length : 0,
      reasoningDepth: Math.max(...chains.map((chain: string[]) => chain.length), 1),
    },
    conflicts: (data?.hypothesis?.conflicts ?? []).map((conflict: string, index: number) => ({
      id: `conflict-${index}`,
      relation: 'Contradictory extracted relation',
      evidence: 'Backend flagged a conflict in generated reasoning.',
      contradiction: conflict,
      uncertainty: 0.5,
    })),
    supportingChains: chains.map((chain: string[], index: number) => ({
      id: `chain-${index}`,
      title: `Supporting chain ${index + 1}`,
      strength: Math.max(0.5, confidence - index * 0.08),
      path: chain,
      explanation: 'Extracted from backend graph traversal over retrieved evidence.',
      inferred: index > 0,
    })),
  }
}

export async function runResearch(request: ResearchRequest): Promise<ResearchResult> {
  try {
    const { data } = await api.post('/analyze', { query: request.query })
    return normalizeBackendResult(data, request)
  } catch (error) {
    if (axios.isAxiosError(error) && error.code === 'ECONNABORTED') {
      throw new Error('The backend took longer than 120 seconds to respond.')
    }
    if (process.env.NODE_ENV === 'production') throw error
    return { ...mockResearchResult, query: request.query, domain: request.domain }
  }
}

export async function getResearchResult(id: string): Promise<ResearchResult> {
  try {
    const { data } = await api.get(`/research/results/${id}`)
    return data
  } catch (error) {
    if (process.env.NODE_ENV === 'production') throw error
    return { ...mockResearchResult, id }
  }
}

export async function getSystemMetrics() {
  try {
    const { data } = await api.get('/system/metrics')
    return data
  } catch {
    return {
      latency: [120, 138, 101, 156, 132, 118],
      throughput: [32, 41, 38, 46, 51, 48],
      retrievalQuality: 0.84,
      graphCompleteness: 0.78,
      conflictPrecision: 0.71,
    }
  }
}
