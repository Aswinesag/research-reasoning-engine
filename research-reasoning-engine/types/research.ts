export type Domain = 'biomedical' | 'legal' | 'climate' | 'cybersecurity' | 'finance' | 'general'
export type ViewMode = 'research' | 'simplified'
export type RelationPolarity = 'supports' | 'contradicts' | 'inferred' | 'neutral'

export interface Hypothesis {
  title: string
  mechanism: string
  inference: string
  conclusion: string
  falsifiability: string
  confidence: number
  simplified: string
}

export interface EvidenceSnippet {
  id: string
  excerpt: string
  similarity: number
  source: string
  relations: string[]
  nodeIds: string[]
  conflict: boolean
  type: 'evidence' | 'inference' | 'unresolved'
}

export interface ReasoningNode {
  id: string
  label: string
  type: 'entity' | 'mechanism' | 'outcome' | 'evidence' | 'conflict'
  confidence: number
  summary: string
}

export interface ReasoningEdge {
  id: string
  source: string
  target: string
  label: string
  confidence: number
  polarity: RelationPolarity
}

export interface Metrics {
  confidence: number
  graphDensity: number
  totalNodes: number
  totalEdges: number
  conflicts: number
  evidenceUsage: number
  reasoningDepth: number
}

export interface SupportingChain {
  id: string
  title: string
  strength: number
  path: string[]
  explanation: string
  inferred: boolean
}

export interface ConflictItem {
  id: string
  relation: string
  evidence: string
  contradiction: string
  uncertainty: number
}

export interface ResearchResult {
  id: string
  query: string
  domain: Domain
  createdAt: string
  hypothesis: Hypothesis
  evidence: EvidenceSnippet[]
  graphNodes: ReasoningNode[]
  graphEdges: ReasoningEdge[]
  metrics: Metrics
  conflicts: ConflictItem[]
  supportingChains: SupportingChain[]
}

export interface ResearchRequest {
  query: string
  domain: Domain
  depth: number
  simplified: boolean
}

export interface AnalysisJobResponse {
  job_id: string
  status: 'processing' | 'complete' | 'failed'
  result?: ResearchResult
  overview?: {
    total_edges: number
    conflicts: number
    confidence: number
    strongest_chain: string[]
  }
  evidence?: EvidenceSnippet[]
  graph?: {
    nodes: ReasoningNode[]
    edges: ReasoningEdge[]
  }
  hypothesis?: Hypothesis
  metrics?: Metrics
  error?: string
}

