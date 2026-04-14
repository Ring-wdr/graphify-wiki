# Graph Report - notes  (2026-04-15)

## Corpus Check
- Corpus is ~2,502 words - fits in a single context window. You may not need a graph.

## Summary
- 18 nodes · 46 edges · 4 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Debugging & Operations|Debugging & Operations]]
- [[_COMMUNITY_Version Control|Version Control]]
- [[_COMMUNITY_Wiki Operations|Wiki Operations]]
- [[_COMMUNITY_Inbox Notes|Inbox Notes]]

## God Nodes (most connected - your core abstractions)
1. `개발 위키 인덱스` - 16 edges
2. `재현 우선 디버깅` - 7 edges
3. `디버깅과 운영 허브` - 7 edges
4. `버전관리와 협업 허브` - 7 edges
5. `API 멱등성 기초` - 6 edges
6. `로그와 메트릭과 트레이싱` - 6 edges
7. `롤포워드와 롤백` - 6 edges
8. `Git 충돌 해결 체크리스트` - 6 edges
9. `Python asyncio 취소 처리` - 5 edges
10. `Postgres 인덱스 선택도` - 5 edges

## Surprising Connections (you probably didn't know these)
- `개발 위키 인덱스` --references--> `API 멱등성 기초`  [EXTRACTED]
  notes/hubs/development-wiki-index.md → notes/dev/architecture/api-idempotency-basics.md
- `개발 위키 인덱스` --references--> `Python asyncio 취소 처리`  [EXTRACTED]
  notes/hubs/development-wiki-index.md → notes/dev/backend-runtime/python-asyncio-cancellation.md
- `개발 위키 인덱스` --references--> `Postgres 인덱스 선택도`  [EXTRACTED]
  notes/hubs/development-wiki-index.md → notes/dev/database/postgres-index-selectivity.md
- `개발 위키 인덱스` --references--> `로그와 메트릭과 트레이싱`  [EXTRACTED]
  notes/hubs/development-wiki-index.md → notes/dev/debugging/logging-metrics-tracing.md
- `재현 우선 디버깅` --references--> `Git 충돌 해결 체크리스트`  [EXTRACTED]
  notes/dev/debugging/repro-first-debugging.md → notes/dev/version-control/git-conflict-resolution-checklist.md

## Communities

### Community 0 - "Debugging & Operations"
Cohesion: 0.76
Nodes (7): API 멱등성 기초, Python asyncio 취소 처리, Postgres 인덱스 선택도, 로그와 메트릭과 트레이싱, 재현 우선 디버깅, 롤포워드와 롤백, 디버깅과 운영 허브

### Community 1 - "Version Control"
Cohesion: 0.73
Nodes (6): 코드 리뷰를 위한 커밋 크기, Git 체리픽과 리버트, Git 충돌 해결 체크리스트, Git 리베이스 기초, 버전관리와 협업 허브, Git Knowledge Workflow

### Community 2 - "Wiki Operations"
Cohesion: 0.5
Nodes (4): 개발 위키 인덱스, Atomic Note Template, Graph Output Lifecycle, Graphify Wiki Overview

### Community 3 - "Inbox Notes"
Cohesion: 1.0
Nodes (1): Inbox

## Knowledge Gaps
- **4 isolated node(s):** `Inbox`, `Atomic Note Template`, `Graph Output Lifecycle`, `Graphify Wiki Overview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Inbox Notes`** (1 nodes): `Inbox`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `개발 위키 인덱스` connect `Wiki Operations` to `Debugging & Operations`, `Version Control`?**
  _High betweenness centrality (0.541) - this node is a cross-community bridge._
- **Why does `재현 우선 디버깅` connect `Debugging & Operations` to `Version Control`, `Wiki Operations`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `버전관리와 협업 허브` connect `Version Control` to `Debugging & Operations`, `Wiki Operations`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **What connects `Inbox`, `Atomic Note Template`, `Graph Output Lifecycle` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._