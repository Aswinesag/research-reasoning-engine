import { ResearchResult } from '@/types/research'

export const mockResearchResult: ResearchResult = {
  id: 'session-ifnar1-cardiac-risk',
  query: 'How could influenza infection contribute to cardiomyocyte damage through immune signaling?',
  domain: 'biomedical',
  createdAt: '2026-06-02T17:30:00.000Z',
  hypothesis: {
    title: 'Immune-mediated cardiac injury pathway',
    mechanism: 'Influenza-associated inflammatory signaling may activate IFNAR1-linked interferon responses that amplify stress pathways in cardiomyocytes.',
    inference: 'Evidence chains connect viral immune activation, cytokine signaling, receptor-mediated stress, and downstream cardiac cell injury markers.',
    conclusion: 'The strongest hypothesis is an indirect causal mechanism where systemic antiviral response increases cardiomyocyte vulnerability rather than direct viral cytotoxicity alone.',
    falsifiability: 'Measure IFNAR1 pathway activation and cardiomyocyte injury markers under influenza exposure with pathway inhibition controls.',
    confidence: 0.82,
    simplified: 'The immune response triggered by influenza may damage heart cells through inflammatory signaling pathways.',
  },
  graphNodes: [
    { id: 'influenza', label: 'Influenza infection', type: 'entity', confidence: 0.95, summary: 'Primary exposure that initiates antiviral immune signaling.' },
    { id: 'cytokines', label: 'Cytokine activation', type: 'mechanism', confidence: 0.86, summary: 'Inflammatory mediator release observed across retrieved evidence.' },
    { id: 'ifnar1', label: 'IFNAR1 signaling', type: 'mechanism', confidence: 0.79, summary: 'Interferon receptor pathway linked to cellular stress response.' },
    { id: 'oxidative', label: 'Oxidative stress', type: 'mechanism', confidence: 0.74, summary: 'Intermediate damage mechanism inferred from pathway evidence.' },
    { id: 'damage', label: 'Cardiomyocyte damage', type: 'outcome', confidence: 0.81, summary: 'Outcome supported by injury marker and pathway studies.' },
    { id: 'counter', label: 'Direct viral injury uncertainty', type: 'conflict', confidence: 0.52, summary: 'Some sources favor direct infection rather than immune-mediated damage.' },
  ],
  graphEdges: [
    { id: 'e1', source: 'influenza', target: 'cytokines', label: 'triggers', confidence: 0.91, polarity: 'supports' },
    { id: 'e2', source: 'cytokines', target: 'ifnar1', label: 'activates', confidence: 0.84, polarity: 'supports' },
    { id: 'e3', source: 'ifnar1', target: 'oxidative', label: 'amplifies', confidence: 0.72, polarity: 'inferred' },
    { id: 'e4', source: 'oxidative', target: 'damage', label: 'contributes to', confidence: 0.78, polarity: 'supports' },
    { id: 'e5', source: 'counter', target: 'damage', label: 'alternative cause', confidence: 0.49, polarity: 'contradicts' },
  ],
  evidence: [
    { id: 'ev-1', excerpt: 'Influenza exposure is associated with elevated antiviral cytokine signaling and downstream cardiac stress markers.', similarity: 0.92, source: 'Virology Cardiac Review / 2024', relations: ['influenza -> cytokines'], nodeIds: ['influenza', 'cytokines'], conflict: false, type: 'evidence' },
    { id: 'ev-2', excerpt: 'Interferon receptor activation can alter mitochondrial function and increase oxidative injury in vulnerable cardiac tissue.', similarity: 0.87, source: 'Immunology Mechanisms / 2025', relations: ['IFNAR1 -> oxidative stress'], nodeIds: ['ifnar1', 'oxidative'], conflict: false, type: 'inference' },
    { id: 'ev-3', excerpt: 'Several studies report cardiac injury without direct myocardial viral replication, implying indirect immune-mediated effects.', similarity: 0.84, source: 'Clinical Meta-analysis / 2023', relations: ['cytokines -> damage'], nodeIds: ['cytokines', 'damage'], conflict: false, type: 'evidence' },
    { id: 'ev-4', excerpt: 'A subset of cases detected viral material in cardiac tissue, leaving direct cytotoxicity unresolved.', similarity: 0.71, source: 'Case Series / 2022', relations: ['direct viral injury -> damage'], nodeIds: ['counter', 'damage'], conflict: true, type: 'unresolved' },
  ],
  metrics: { confidence: 0.82, graphDensity: 0.31, totalNodes: 6, totalEdges: 5, conflicts: 1, evidenceUsage: 0.76, reasoningDepth: 4 },
  supportingChains: [
    { id: 'chain-1', title: 'Immune signaling chain', strength: 0.86, path: ['Influenza', 'Cytokine activation', 'IFNAR1', 'Oxidative stress', 'Cardiomyocyte damage'], explanation: 'Strongest pathway because each hop is supported by at least one retrieved source.', inferred: false },
    { id: 'chain-2', title: 'Indirect injury pathway', strength: 0.73, path: ['Influenza', 'Systemic inflammation', 'Cardiac vulnerability', 'Damage markers'], explanation: 'Partially inferred pathway that explains injury without direct viral replication.', inferred: true },
  ],
  conflicts: [
    { id: 'conflict-1', relation: 'Influenza -> Cardiomyocyte damage', evidence: 'Immune-mediated injury is supported by cytokine and receptor pathway studies.', contradiction: 'Some case reports suggest direct viral presence in cardiac tissue.', uncertainty: 0.43 },
  ],
}

export const savedSessions = [
  mockResearchResult,
  { ...mockResearchResult, id: 'climate-feedbacks', domain: 'climate' as const, query: 'Which aerosol-cloud pathways most strongly affect regional rainfall uncertainty?' },
  { ...mockResearchResult, id: 'cyber-lateral-movement', domain: 'cybersecurity' as const, query: 'What evidence supports credential replay as the cause of lateral movement?' },
]

