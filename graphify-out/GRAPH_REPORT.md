# Graph Report - notes  (2026-05-03)

## Corpus Check
- Corpus is ~7,211 words - fits in a single context window. You may not need a graph.

## Summary
- 30 nodes · 85 edges · 5 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Debugging & Operations|Debugging & Operations]]
- [[_COMMUNITY_Wiki Operations|Wiki Operations]]
- [[_COMMUNITY_Debugging & Operations|Debugging & Operations]]
- [[_COMMUNITY_Version Control|Version Control]]
- [[_COMMUNITY_Inbox Notes|Inbox Notes]]

## God Nodes (most connected - your core abstractions)
1. `개발 위키 인덱스` - 18 edges
2. `디버깅과 운영 허브` - 16 edges
3. `재현 우선 디버깅` - 12 edges
4. `Vibe Danmaku 트러블슈팅과 기술 판단 개요` - 11 edges
5. `로그와 메트릭과 트레이싱` - 9 edges
6. `코드 리뷰를 위한 커밋 크기` - 8 edges
7. `버전관리와 협업 허브` - 7 edges
8. `API 멱등성 기초` - 6 edges
9. `롤포워드와 롤백` - 6 edges
10. `Git 충돌 해결 체크리스트` - 6 edges

## Surprising Connections (you probably didn't know these)
- `디버깅과 운영 허브` --references--> `API 멱등성 기초`  [EXTRACTED]
  notes/hubs/debugging-operations-hub.md → notes/dev/architecture/api-idempotency-basics.md
- `개발 위키 인덱스` --references--> `API 멱등성 기초`  [EXTRACTED]
  notes/hubs/development-wiki-index.md → notes/dev/architecture/api-idempotency-basics.md
- `디버깅과 운영 허브` --references--> `Python asyncio 취소 처리`  [EXTRACTED]
  notes/hubs/debugging-operations-hub.md → notes/dev/backend-runtime/python-asyncio-cancellation.md
- `개발 위키 인덱스` --references--> `Python asyncio 취소 처리`  [EXTRACTED]
  notes/hubs/development-wiki-index.md → notes/dev/backend-runtime/python-asyncio-cancellation.md
- `디버깅과 운영 허브` --references--> `Postgres 인덱스 선택도`  [EXTRACTED]
  notes/hubs/debugging-operations-hub.md → notes/dev/database/postgres-index-selectivity.md

## Communities

### Community 0 - "Debugging & Operations"
Cohesion: 0.56
Nodes (9): Vibe Danmaku 전투 페이싱과 런타임 타이밍 디버깅, Vibe Danmaku 생성 에셋과 프리로드 파이프라인, Vibe Danmaku R3F 보스 렌더링 트러블슈팅, Vibe Danmaku 짧은 세로 화면과 메뉴 UX, Vibe Danmaku 세션 상태 경계와 XState 전환, Vibe Danmaku 스테이지 이벤트 타임라인과 보스 FSM, Vibe Danmaku 트러블슈팅과 기술 판단 개요, Vibe Danmaku worktree와 검증 중심 Git 흐름 (+1 more)

### Community 1 - "Wiki Operations"
Cohesion: 0.36
Nodes (8): KMP Compose Workshop 프로젝트 생성 시 SQLDelight NPE 트러블슈팅, KMP Compose 워크트리 로컬 실행 세팅, Windows에서 KMP Compose용 JDK 21 운영, 개발 위키 인덱스, Atomic Note Template, Git Knowledge Workflow, Graph Output Lifecycle, Graphify Wiki Overview

### Community 2 - "Debugging & Operations"
Cohesion: 0.57
Nodes (7): API 멱등성 기초, Python asyncio 취소 처리, Postgres 인덱스 선택도, 로컬 노트 코파일럿 RN Expo 트러블슈팅, 로그와 메트릭과 트레이싱, 재현 우선 디버깅, 롤포워드와 롤백

### Community 3 - "Version Control"
Cohesion: 0.9
Nodes (5): 코드 리뷰를 위한 커밋 크기, Git 체리픽과 리버트, Git 충돌 해결 체크리스트, Git 리베이스 기초, 버전관리와 협업 허브

### Community 4 - "Inbox Notes"
Cohesion: 1.0
Nodes (1): Inbox

## Knowledge Gaps
- **3 isolated node(s):** `Inbox`, `Atomic Note Template`, `Graph Output Lifecycle`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Inbox Notes`** (1 nodes): `Inbox`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `개발 위키 인덱스` connect `Wiki Operations` to `Debugging & Operations`, `Debugging & Operations`, `Version Control`?**
  _High betweenness centrality (0.371) - this node is a cross-community bridge._
- **Why does `디버깅과 운영 허브` connect `Debugging & Operations` to `Wiki Operations`, `Debugging & Operations`?**
  _High betweenness centrality (0.217) - this node is a cross-community bridge._
- **Why does `재현 우선 디버깅` connect `Debugging & Operations` to `Debugging & Operations`, `Wiki Operations`, `Version Control`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **What connects `Inbox`, `Atomic Note Template`, `Graph Output Lifecycle` to the rest of the system?**
  _3 weakly-connected nodes found - possible documentation gaps or missing edges._