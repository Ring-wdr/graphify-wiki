# Vibe Danmaku 전투 페이싱과 런타임 타이밍 디버깅

## 한 줄 요약

전투가 비어 보이거나 적이 늦게 공격하는 문제는 렌더링보다 런타임 타이밍과 스테이지 콘텐츠 간격을 먼저 의심해야 했다.

## 언제 쓰나

- 적이 화면에 보인 뒤 한참 지나서야 탄을 쏠 때
- 웨이브 사이 공백이 길어 게임이 늘어진다고 느껴질 때
- 스테이지 데이터와 런타임 계산 중 어느 쪽을 고칠지 판단해야 할 때
- 감각적인 페이싱 불만을 회귀 테스트로 바꾸고 싶을 때

## 적의 첫 공격이 늦던 문제

증상은 "적이 보이는데 공격하지 않는다"였다. 겉으로는 전투 연출 문제처럼 보였지만 실제로는 `battleRuntime.ts`의 첫 발사 지연 계산이 너무 보수적이었다.

해결 방향은 적이 완전히 정착한 뒤에만 공격하게 하지 않고, 화면 진입 중 특정 lead zone에 들어오면 첫 공격을 시작하게 하는 것이었다. 오프스크린에서 플레이어가 볼 수 없는 탄이 날아오면 불공정하므로, "보이기 시작한 뒤 곧 압박한다"는 중간 지점이 중요했다.

좋은 테스트는 특정 초까지 runtime을 advance했을 때 실제 enemy bullet이 나오는지 확인하는 것이다. 첫 시도에서 2초 부근에 탄이 없다는 테스트 실패가 나왔고, 그 실패가 수정 방향을 분명하게 만들었다.

## 웨이브 공백이 길던 문제

웨이브 간격이 길면 난이도 문제가 아니라 밀도 문제가 된다. 이 프로젝트에서는 `stage1.ts`의 wave count와 wave gap을 테스트로 고정했다.

처음에는 웨이브가 3개뿐이라는 테스트 실패가 나왔고, 이를 계기로 단순히 한두 출현 시점을 당기는 대신 전체 웨이브 수와 보스 전 공백을 함께 조정했다. 체감 품질을 "최소 웨이브 수"와 "최대 공백"으로 바꾼 점이 핵심이었다.

## 런타임과 콘텐츠의 책임 구분

런타임은 "주어진 이벤트를 언제 어떻게 실행하는가"를 책임진다. 적 entry, first shot delay, boss active 여부, victory result 같은 계산은 runtime 쪽이다.

콘텐츠는 "어떤 이벤트가 어떤 간격으로 배치되는가"를 책임진다. wave start time, midboss/final boss timing, stage duration, difficulty scaling은 stage definition 쪽이다.

이 둘을 섞으면 원인을 놓치기 쉽다. 공격 시작이 늦으면 runtime, 전투가 비면 stage content, 보스 이후 진행이 멈추면 event gate와 boss state를 같이 본다.

## 다음에 볼 곳

- `src/game/runtime/battleRuntime.ts`
- `src/game/runtime/battleRuntime.test.ts`
- `src/game/content/stage1.ts`
- `src/game/content/stage1.test.ts`
- `src/game/content/stage3.ts`
- `src/game/content/stageEvents.ts`

## 주의할 점

- 첫 공격을 당길 때 오프스크린 공격이 생기지 않는지 확인한다.
- 웨이브 간격 조정은 하나의 time value만 바꾸기보다 전체 stage rhythm을 본다.
- 감각적 불만은 가능한 한 테스트 가능한 숫자로 바꾼다.
- `BattleView.tsx`가 보이는 문제처럼 느껴져도, snapshot 생성은 runtime이 한다.

## 관련 노트

- [Vibe Danmaku 스테이지 이벤트 타임라인과 보스 FSM](vibe-danmaku-stage-events-and-boss-fsm.md)
- [Vibe Danmaku 트러블슈팅과 기술 판단 개요](vibe-danmaku-troubleshooting-and-technical-decisions.md)
- [재현 우선 디버깅](repro-first-debugging.md)
