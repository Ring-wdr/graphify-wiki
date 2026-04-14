# Graph Output Lifecycle

현재 저장소는 `graphify-out/`를 버전 관리하고 GitHub Pages에 배포한다.

## 현재 단계

- `notes/`를 수정한 뒤 로컬에서 `graphify`를 실행한다.
- 생성된 `graph.html`, `graph.json`, `GRAPH_REPORT.md`를 확인한다.
- 노트 커밋과 분리해서 `graph:` 커밋으로 남긴다.

## 장기 방향

- 장기적으로는 CI에서 `graphify-out/`를 생성하도록 옮긴다.
- 그 전까지는 Pages 안정성을 위해 현재 산출물을 계속 유지한다.
- CI 전환 전에는 산출물과 원본 노트의 의미를 Git에서 구분해 읽을 수 있게 운영한다.
