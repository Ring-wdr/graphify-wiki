# Vibe Danmaku 세션 상태 경계와 XState 전환

## 한 줄 요약

전투 계산 전체가 아니라 타이틀에서 결과 화면까지의 앱 세션 흐름만 XState로 옮긴 것이 Vibe Danmaku의 첫 안정화 지점이었다.

## 언제 쓰나

- 화면 전환이 꼬이거나 retry, next stage, return title 흐름이 이상할 때
- `App.tsx`의 상태가 너무 많은 책임을 갖는다고 느껴질 때
- 페이지별로 필요한 값만 구독하도록 구조를 다시 보고 싶을 때
- React Compiler와 memoization 제거 범위를 판단해야 할 때

## 문제의 모양

초기 앱 흐름은 `App.tsx`의 여러 `useState`가 화면, 난이도, 선택 캐릭터, 현재 스테이지, 전투 시드, 결과를 함께 들고 있었다. 값이 많아질수록 화면 전환 테스트가 복잡해졌고, battle loading, stage intro, battle view, result 사이의 계약이 흐릿해졌다.

하지만 전투 런타임까지 한 번에 상태머신으로 바꾸면 범위가 지나치게 커진다. 이 프로젝트에서는 먼저 앱 세션만 기계로 만들고, 실제 충돌, 탄막, boss update, item 처리 같은 전투 계산은 기존 imperative runtime에 남겼다.

## 결정한 경계

`battleSessionMachine.ts`는 앱 흐름을 책임진다. 컨텍스트에는 난이도, 선택 캐릭터, 현재 스테이지 번호, 전투 시드, 결과처럼 화면 전환에 필요한 값만 둔다.

`App.tsx`는 `useMachine(battleSessionMachine, { input })`의 반환값인 `snapshot`, `send`, `actorRef`를 유지한다. `snapshot.matches(...)`는 어떤 화면을 보여 줄지 결정하는 데 쓰고, `send`는 화면 이벤트를 상태머신 이벤트로 전달한다.

각 화면은 필요한 값만 `useSelector`로 구독한다. 예를 들어 캐릭터 선택 화면은 난이도와 선택 이벤트만 필요하고, 로딩 화면은 현재 스테이지와 캐릭터, 전투 시드가 필요하다.

## 시행착오

`App` 자체를 과도하게 selector 기반으로 바꾸면 오히려 라우터 역할이 흐릿해졌다. `App`은 세션 actor의 router에 가깝고, 페이지 컴포넌트가 세부 값을 선택하는 편이 낫다.

retry 테스트는 실제 전환 경로를 따라야 한다. stage 2 defeat를 테스트한다고 해서 중간 상태를 건너뛰고 결과만 주입하면, machine contract를 검증하지 못한다.

스테이지 수가 늘어나면서 retry stage clamp가 `1 | 2` 중심으로 남아 있던 부분은 별도 확장 포인트가 되었다. Stage 3 이후를 고려할 때는 stage model을 더 일반화해야 한다.

## React Compiler와 lint 정책

앱 레이어에서는 React Compiler를 믿고 평범한 `useMemo`, `useCallback`을 제거하는 편이 좋았다. 반대로 `src/game/ui`는 texture, geometry, material, refs 같은 특수 객체를 다루므로 같은 규칙을 그대로 적용하면 거짓 양성이 많이 나온다.

그래서 `eslint-plugin-react-hooks`의 최신 권장 규칙은 `src/app/**/*.{ts,tsx}`에만 적용했다. 이 결정은 "React Compiler를 쓰니 memo를 전부 지운다"가 아니라 "앱 상태 레이어와 렌더링 객체 레이어를 분리한다"에 가깝다.

## 다음에 볼 곳

- `src/app/battleSessionMachine.ts`
- `src/app/battleSessionMachine.test.ts`
- `src/app/App.tsx`
- `src/app/BattlePhase.tsx`
- `src/app/BattleLoadingScreen.tsx`
- `src/app/screens/CharacterSelectScreen.tsx`
- `eslint.config.js`

## 관련 노트

- [Vibe Danmaku 트러블슈팅과 기술 판단 개요](vibe-danmaku-troubleshooting-and-technical-decisions.md)
- [Vibe Danmaku worktree와 검증 중심 Git 흐름](vibe-danmaku-worktree-verification-workflow.md)
- [코드 리뷰를 위한 커밋 크기](../tooling/code-review-commit-sizing.md)
