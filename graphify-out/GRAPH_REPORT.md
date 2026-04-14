# Graph Report - .  (2026-04-14)

## Corpus Check
- Corpus is ~91 words - fits in a single context window. You may not need a graph.

## Summary
- 10 nodes · 11 edges · 3 communities detected
- Extraction: 55% EXTRACTED · 45% INFERRED · 0% AMBIGUOUS · INFERRED: 5 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Workspace Purpose|Workspace Purpose]]
- [[_COMMUNITY_Graph Outputs|Graph Outputs]]
- [[_COMMUNITY_Note Growth|Note Growth]]

## God Nodes (most connected - your core abstractions)
1. `Graphify Wiki Overview` - 9 edges
2. `GRAPH_REPORT.md` - 2 edges
3. `graph.json` - 2 edges
4. `Notes Folder Initial State` - 2 edges
5. `Future Topic Notes` - 2 edges
6. `graphify` - 1 edges
7. `Knowledge Graph Workspace` - 1 edges
8. `Core Concepts and Connections` - 1 edges
9. `graph.html` - 1 edges
10. `Community Structure` - 1 edges

## Surprising Connections (you probably didn't know these)
- `Graphify Wiki Overview` --references--> `GRAPH_REPORT.md`  [EXTRACTED]
  notes/graphify-wiki-overview.md → notes/graphify-wiki-overview.md  _Bridges community 0 → community 1_
- `Graphify Wiki Overview` --references--> `Notes Folder Initial State`  [EXTRACTED]
  notes/graphify-wiki-overview.md → notes/graphify-wiki-overview.md  _Bridges community 0 → community 2_

## Hyperedges (group relationships)
- **Graphify Output Bundle** — graph_html, graph_report_md, graph_json [INFERRED 0.94]

## Communities

### Community 0 - "Workspace Purpose"
Cohesion: 0.33
Nodes (6): Community Structure, Core Concepts and Connections, graph.html, graphify, Graphify Wiki Overview, Knowledge Graph Workspace

### Community 1 - "Graph Outputs"
Cohesion: 1.0
Nodes (2): graph.json, GRAPH_REPORT.md

### Community 2 - "Note Growth"
Cohesion: 1.0
Nodes (2): Future Topic Notes, Notes Folder Initial State

## Knowledge Gaps
- **5 isolated node(s):** `graphify`, `Knowledge Graph Workspace`, `Core Concepts and Connections`, `graph.html`, `Community Structure`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Graph Outputs`** (2 nodes): `graph.json`, `GRAPH_REPORT.md`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Note Growth`** (2 nodes): `Future Topic Notes`, `Notes Folder Initial State`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Graphify Wiki Overview` connect `Workspace Purpose` to `Graph Outputs`, `Note Growth`?**
  _High betweenness centrality (0.944) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Graphify Wiki Overview` (e.g. with `Knowledge Graph Workspace` and `Core Concepts and Connections`) actually correct?**
  _`Graphify Wiki Overview` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify`, `Knowledge Graph Workspace`, `Core Concepts and Connections` to the rest of the system?**
  _5 weakly-connected nodes found - possible documentation gaps or missing edges._