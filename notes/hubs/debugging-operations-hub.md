# 디버깅과 운영 허브

이 허브는 장애를 재현하고 원인을 좁히며 배포 후 대응을 정리하는 노트를 묶는다.

## 자주 보는 노트

- [재현 우선 디버깅](../dev/debugging/repro-first-debugging.md)
- [로그와 메트릭과 트레이싱](../dev/debugging/logging-metrics-tracing.md)
- [Vibe Danmaku 트러블슈팅과 기술 판단 개요](../dev/debugging/vibe-danmaku-troubleshooting-and-technical-decisions.md)
- [Vibe Danmaku 세션 상태 경계와 XState 전환](../dev/debugging/vibe-danmaku-session-state-boundary.md)
- [Vibe Danmaku 전투 페이싱과 런타임 타이밍 디버깅](../dev/debugging/vibe-danmaku-battle-pacing-runtime-debugging.md)
- [Vibe Danmaku 스테이지 이벤트 타임라인과 보스 FSM](../dev/debugging/vibe-danmaku-stage-events-and-boss-fsm.md)
- [Vibe Danmaku R3F 보스 렌더링 트러블슈팅](../dev/debugging/vibe-danmaku-r3f-boss-rendering-troubleshooting.md)
- [Vibe Danmaku 생성 에셋과 프리로드 파이프라인](../dev/debugging/vibe-danmaku-generated-assets-and-preload-pipeline.md)
- [Vibe Danmaku 짧은 세로 화면과 메뉴 UX](../dev/debugging/vibe-danmaku-responsive-menu-ux.md)
- [Vibe Danmaku worktree와 검증 중심 Git 흐름](../dev/debugging/vibe-danmaku-worktree-verification-workflow.md)
- [KMP Compose Workshop 프로젝트 생성 시 SQLDelight NPE 트러블슈팅](../dev/debugging/kmp-compose-workshop-project-sqldelight-npe.md)
- [Python asyncio 취소 처리](../dev/backend-runtime/python-asyncio-cancellation.md)
- [롤포워드와 롤백](../dev/tooling/deployment-rollforward-vs-rollback.md)

## 언제 이 허브를 보나

- 버그를 재현 가능한 형태로 줄이고 싶을 때
- 운영 신호를 무엇으로 봐야 할지 정리하고 싶을 때
- 비동기 작업 취소나 타임아웃 문제를 이해하고 싶을 때
- 배포 사고 대응에서 되돌릴지 앞으로 고칠지 판단해야 할 때

## 함께 보면 좋은 노트

- [API 멱등성 기초](../dev/architecture/api-idempotency-basics.md)
- [Postgres 인덱스 선택도](../dev/database/postgres-index-selectivity.md)
