# Vibe Danmaku 트러블슈팅과 기술 판단 개요

## 한 줄 요약

Vibe Danmaku에서 반복해서 나온 문제는 상태 소유권, 전투 런타임 타이밍, 스테이지 이벤트, R3F 렌더링, 생성 에셋, 좁은 화면 UX, Git 검증 흐름으로 나눠 기록하는 편이 가장 덜 새어 나간다.

## 언제 쓰나

- Vibe Danmaku 작업을 다시 시작하기 전에 과거 시행착오를 훑고 싶을 때
- 특정 증상이 앱 상태, 런타임, 렌더링, 에셋 중 어디서 온 것인지 먼저 분류하고 싶을 때
- 작은 수정도 어떻게 검증하고 `main`에 합쳤는지 확인하고 싶을 때

## 노트 지도

- [Vibe Danmaku 세션 상태 경계와 XState 전환](vibe-danmaku-session-state-boundary.md)
- [Vibe Danmaku 전투 페이싱과 런타임 타이밍 디버깅](vibe-danmaku-battle-pacing-runtime-debugging.md)
- [Vibe Danmaku 스테이지 이벤트 타임라인과 보스 FSM](vibe-danmaku-stage-events-and-boss-fsm.md)
- [Vibe Danmaku R3F 보스 렌더링 트러블슈팅](vibe-danmaku-r3f-boss-rendering-troubleshooting.md)
- [Vibe Danmaku 생성 에셋과 프리로드 파이프라인](vibe-danmaku-generated-assets-and-preload-pipeline.md)
- [Vibe Danmaku 짧은 세로 화면과 메뉴 UX](vibe-danmaku-responsive-menu-ux.md)
- [Vibe Danmaku worktree와 검증 중심 Git 흐름](vibe-danmaku-worktree-verification-workflow.md)

## 문제를 먼저 분류하는 법

상태가 꼬였으면 `src/app`부터 본다. 화면 전환, 선택 캐릭터, 현재 스테이지, 결과, 리더보드 기록처럼 앱 흐름에 가까운 값은 세션 상태 경계 문제일 확률이 높다.

전투가 비어 보이거나 적이 늦게 행동하면 `src/game/runtime`과 `src/game/content`를 같이 본다. 런타임 계산이 늦은 것인지, 콘텐츠 이벤트 간격이 넓은 것인지 분리해야 한다.

보스가 작거나 납작하거나 카드판처럼 보이면 `src/game/ui`와 `src/assets/generated`를 같이 본다. R3F 렌더링 문제가 에셋 투명도 문제처럼 보일 수도 있고, 반대도 가능하다.

화면이 짧은 모바일에서 잘리면 `src/style.css`와 화면별 CSS module을 본다. 이 프로젝트에서는 첫 타이틀 화면과 일반 메뉴 화면의 스크롤 정책이 다르다.

작업트리에 생성 에셋이나 임시 파일이 섞여 있으면 Git부터 정리한다. 작은 수정은 worktree로 분리하고, 검증 뒤 좁게 stage하는 편이 비용이 적었다.

## 공통 체크리스트

1. 증상을 상태, 런타임, 콘텐츠, 렌더링, 에셋, CSS, Git 흐름 중 하나 이상으로 분류한다.
2. 감각적 요구를 테스트 가능한 숫자나 데이터 계약으로 바꾼다.
3. R3F 테스트는 내부 DOM 모양보다 렌더링 계약과 데이터 경로를 검증한다.
4. 생성 에셋은 파일 존재, WebP 매핑, 투명도, 프리로드 포함 여부를 함께 본다.
5. `npm test`, `npm run typecheck`, `npm run build`를 기본 검증으로 두고, 앱 셸이나 lint 정책 변경 시 `npm run lint`를 추가한다.
6. 커밋할 때는 의도한 파일만 명시적으로 stage한다.

## 관련 노트

- [재현 우선 디버깅](repro-first-debugging.md)
- [로그와 메트릭과 트레이싱](logging-metrics-tracing.md)
- [코드 리뷰를 위한 커밋 크기](../tooling/code-review-commit-sizing.md)
