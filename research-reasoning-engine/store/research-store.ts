import { create } from 'zustand'
import { mockResearchResult, savedSessions } from '@/lib/mock-data'
import { Domain, EvidenceSnippet, ResearchResult, ViewMode } from '@/types/research'

interface ResearchState {
  activeQuery: string
  domain: Domain
  depth: number
  viewMode: ViewMode
  result: ResearchResult
  selectedEvidence?: EvidenceSnippet
  sessions: ResearchResult[]
  setQuery: (query: string) => void
  setDomain: (domain: Domain) => void
  setDepth: (depth: number) => void
  setViewMode: (viewMode: ViewMode) => void
  setResult: (result: ResearchResult) => void
  selectEvidence: (evidence?: EvidenceSnippet) => void
  saveSession: (result: ResearchResult) => void
}

export const useResearchStore = create<ResearchState>((set) => ({
  activeQuery: mockResearchResult.query,
  domain: 'biomedical',
  depth: 4,
  viewMode: 'research',
  result: mockResearchResult,
  sessions: savedSessions,
  setQuery: (activeQuery) => set({ activeQuery }),
  setDomain: (domain) => set({ domain }),
  setDepth: (depth) => set({ depth }),
  setViewMode: (viewMode) => set({ viewMode }),
  setResult: (result) => set((state) => ({ result, sessions: [result, ...state.sessions.filter((session) => session.id !== result.id)] })),
  selectEvidence: (selectedEvidence) => set({ selectedEvidence }),
  saveSession: (result) => set((state) => ({ sessions: [result, ...state.sessions.filter((session) => session.id !== result.id)] })),
}))

