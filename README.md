# Research Reasoning Engine

A grounded causal reasoning system that constructs evidence-backed knowledge graphs and generates testable hypotheses from unstructured scientific text.

This project is designed as a structured AI reasoning pipeline — not a chatbot, and not a simple retrieval wrapper. It focuses on controlled inference, graph construction, and explainable hypothesis generation.

---

## 1. Overview

The Research Reasoning Engine processes domain text collections and produces:

- A filtered evidence set  
- Extracted entities and relations  
- A sparse causal graph  
- A structured hypothesis  
- Reasoning metrics for transparency  

The system enforces grounding constraints to reduce speculative inference and maintain traceability between claims and source evidence.

---

## 2. System Architecture

The system follows a modular reasoning pipeline:

Query
↓
Embedding & Retrieval (FAISS)
↓
Evidence Filtering
↓
Entity Extraction
↓
Relation Extraction
↓
Graph Construction
↓
Hypothesis Generation
↓
Structured JSON Output


Each stage operates independently and can be replaced or extended without modifying the overall architecture.

---

## 3. Design Principles

### Grounded Inference
All relations must be traceable to retrieved evidence.  
No prior knowledge or external facts are injected into reasoning.

### Sparse Graph Construction
Edges are created only when supported by explicit relationships.  
Overconnected graphs are pruned using density and reinforcement constraints.

### Explicit Speculation Control
The hypothesis is separated into:
- Grounded mechanism (directly supported)
- Speculative extensions (clearly labeled)

### Traceability
Each inferred relation references supporting evidence IDs.

---

## 4. Core Components

### 4.1 Retrieval Layer

- Embedding-based similarity search  
- FAISS index for vector retrieval  
- Threshold-based relevance filtering  
- Optional reranking  

This layer retrieves candidate excerpts but does not perform reasoning.

---

### 4.2 Evidence Filtering

Removes:
- Irrelevant chunks  
- Low similarity matches  
- Excerpts lacking query entities  

This step reduces noise before reasoning begins.

---

### 4.3 Entity Extraction

Extracts explicitly mentioned domain entities from each excerpt.

No entities are fabricated.  
No entity is inferred unless it appears in text.

---

### 4.4 Relation Extraction

Identifies explicit causal or mechanistic statements.

Each relation includes:
- Source  
- Target  
- Polarity (+ / -)  
- Supporting excerpt reference  

Only text-supported relations are allowed.

---

### 4.5 Graph Builder

Constructs a directed graph with:

- Node frequency tracking  
- Weighted edges  
- Conflict detection  
- Density monitoring  

Constraints:
- Limited edges per node  
- Pruning of low-support connections  
- Re-evaluation if graph density exceeds threshold  

---

### 4.6 Hypothesis Generator

Generates structured output:

- Grounded mechanism  
- Supporting chains  
- Explicit evidence mapping  
- Confidence level  
- Optional speculative extensions  

No free-form narrative reasoning is allowed.

---

## 5. Output Format

The system returns structured JSON:

```json
{
  "filtered_evidence": [],
  "entities": [],
  "relations": [],
  "graph": {
    "nodes": [],
    "edges": []
  },
  "hypothesis": {
    "grounded_mechanism": "",
    "speculative_extensions": "",
    "confidence_level": ""
  },
  "metrics": {
    "total_nodes": 0,
    "total_edges": 0,
    "graph_density": 0.0
  }
}

### What This System Is Not

- Not a conversational chatbot
- Not a generic RAG wrapper
- Not a summarization engine
- Not a free-form generative model

The system performs structured reasoning under constraints.

### What This System Is Not

- Not a conversational chatbot
- Not a generic RAG wrapper
- Not a summarization engine
- Not a free-form generative model

The system performs structured reasoning under constraints.

### Limitations

- Dependent on retrieval quality
- Sensitive to noisy or incomplete text
- Does not replace domain expertise
- Speculative reasoning remains probabilistic

Grounding constraints reduce hallucination but do not eliminate uncertainty.