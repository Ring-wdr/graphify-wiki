# Vibe Danmaku 짧은 세로 화면과 메뉴 UX

## 한 줄 요약

짧은 세로 viewport에서 메뉴가 잘리는 문제는 단순 모바일 CSS가 아니라 앱 셸 높이, 화면별 overflow, 타이틀 화면 예외를 함께 다뤄야 했다.

## 언제 쓰나

- 모바일 또는 작은 높이의 브라우저에서 메뉴 버튼이 잘릴 때
- 첫 타이틀 화면에는 스크롤이 생기면 안 되지만 다른 메뉴는 스크롤이 필요할 때
- battle loading, result, character select 같은 화면의 세로 밀도를 조정해야 할 때
- UI 문제를 실제 viewport 조건으로 검증해야 할 때

## 문제의 뿌리

앱 셸은 게임 화면을 phone frame처럼 보여 주기 때문에 frame level overflow가 강하다. 이때 내부 화면이 `min-height` 중심으로만 잡히면 세로가 짧은 viewport에서 하단 버튼이나 카드가 잘린다.

해결은 전체 shell을 `100dvh` 기준으로 잡고, phone frame과 screen stack이 실제 available height 안에서 계산되도록 하는 쪽이었다. 일반 menu screen은 내부 스크롤을 허용해야 하지만, title hero는 의도적으로 스크롤을 막아야 했다.

## title screen은 예외다

사용자는 첫 타이틀 화면에 스크롤이 생기지 않기를 원했다. 따라서 모든 `.screen`에 같은 overflow 정책을 주면 안 된다.

`screen--hero`는 별도 no-scroll 예외를 유지한다. 아주 낮은 높이에서는 hero art를 줄이거나 secondary decoration을 숨겨 버튼과 겹치지 않게 한다. 타이틀 화면을 스크롤 가능하게 만드는 것은 쉬운 해결처럼 보이지만, 이 프로젝트의 의도와 맞지 않았다.

## 짧은 높이용 밀도 조정

짧은 viewport에서는 heading, top bar gap, card padding, button height, result summary 간격을 함께 줄여야 한다. 하나만 줄이면 다른 영역이 다시 밀려 내려간다.

좋았던 방식은 `@media (max-height: 620px)` 같은 전용 경로를 두고 화면별 핵심 요소의 밀도를 조정하는 것이다. 작은 화면용 규칙이 일반 desktop 레이아웃을 침범하지 않는지도 같이 본다.

## 검증 포인트

CSS만 읽으면 실제 잘림을 놓치기 쉽다. Playwright나 브라우저 확인으로 짧은 세로 viewport에서 버튼, heading, 주요 CTA가 보이는지 확인해야 한다.

테스트에서는 generic menu screen은 내부 스크롤 가능, hero screen은 non-scrollable이라는 계약을 분리해서 고정하는 편이 좋았다.

## 다음에 볼 곳

- `src/style.css`
- `src/app/menuLayout.test.ts`
- `src/app/screens/TitleScreen.tsx`
- `src/app/screens/TitleScreen.module.css`
- `src/app/screens/CharacterSelectScreen.tsx`
- `src/app/screens/ResultScreen.tsx`
- `src/app/BattleLoadingScreen.tsx`

## 관련 노트

- [Vibe Danmaku 세션 상태 경계와 XState 전환](vibe-danmaku-session-state-boundary.md)
- [Vibe Danmaku 트러블슈팅과 기술 판단 개요](vibe-danmaku-troubleshooting-and-technical-decisions.md)
- [재현 우선 디버깅](repro-first-debugging.md)
