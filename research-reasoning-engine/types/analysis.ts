export interface AnalysisResponse {
  overview: {
    total_edges: number
    conflicts: number
    confidence: number
    strongest_chain: string[]
  }
  evidence: EvidenceItem[]
  graph: {
    nodes: GraphNode[]
    edges: GraphEdge[]
  }
  hypothesis: {
    mechanism: string
    supporting_chains: string[][]
    conflicts: string[]
    testable_predictions: string[]
  }
  metrics: {
    mean_weight: number
    reinforcement_factor: number
    graph_density: number
  }
}

export interface EvidenceItem {
  id: string
  doc_id: string
  score: number
  excerpt: string
  entities: string[]
  relations_count: number
  used: boolean
  conflict: boolean
}

export interface GraphNode {
  id: string
  label: string
  frequency: number
}

export interface GraphEdge {
  id: string
  source: string
  target: string
  polarity: "+" | "-"
  weight: number
  conflict: boolean
}
