# Vibe Danmaku 스테이지 이벤트 타임라인과 보스 FSM

## 한 줄 요약

스테이지 진행은 암묵적 런타임 흐름보다 명시적인 이벤트 타임라인으로 두고, 보스의 phase, movement, fire pattern, vulnerability는 FSM snapshot으로 분리하는 편이 확장에 강했다.

## 언제 쓰나

- Stage 3처럼 midboss, final boss, phase break, victory condition이 많아질 때
- 보스 처치 후 다음 이벤트가 너무 빨리 오거나 멈추는 문제를 볼 때
- boss FSM이 실제 spawn time과 어긋나는지 의심될 때
- 탄막 패턴을 rank 기반으로 조정해야 할 때

## 이벤트 타임라인으로 옮긴 이유

스테이지가 단순할 때는 runtime에 "이 시점쯤 보스를 낸다"는 흐름이 숨어 있어도 버틸 수 있다. 하지만 Stage 3처럼 midboss gate, final boss, phase break, victory event가 늘어나면 암묵적 흐름은 금방 추적하기 어려워진다.

명시적 `StageEvent` 타임라인은 stage authoring을 데이터 중심으로 만든다. `time`, `afterDefeated`, `spawnBoss`, `victory` 같은 이벤트가 보이면, 디자이너가 어떤 리듬을 의도했는지 코드만 보고도 따라갈 수 있다.

## Stage 3의 패턴

Stage 3는 abyssal biomech 테마를 기준으로 배경, enemy atlas, midboss, final boss를 가진다. `midbossAt`, `finalBossAt`, `fastStageMultiplier` 같은 값은 기본 타이밍과 빠른 테스트/디버그 흐름을 분리하는 데 도움이 된다.

탄막은 BulletML 스타일 설정으로 작성된다. `rankExpression`, `rankScale`, `rankWait`처럼 난이도 rank에 따라 반복 횟수, 탄속, wait를 조절하는 helper를 둔 것이 포인트다.

이 구조는 "패턴이 멋있다"보다 "패턴이 데이터로 읽힌다"가 중요하다. 반복, 발사 방향, speed change, direction change, wait가 모두 stage content 안에서 드러난다.

## 보스 FSM의 역할

보스 FSM은 하나의 거대한 상태값이 아니라 네 영역으로 읽는 편이 좋았다.

- `phase`: Intro, active phase, Break 같은 전투 단계
- `movement`: EnterScreen, center hold 같은 위치 행동
- `firePattern`: Idle 또는 현재 phase의 발사 패턴
- `vulnerability`: Invulnerable, Vulnerable, ArmorBreak 같은 피격 가능 상태

`bossFsm.ts`는 내부적으로 다음 snapshot을 계산한 뒤 각 region actor에 같은 tick을 반영한다. 이 덕분에 UI는 `boss.fsm` snapshot을 보고 phase break effect나 damageable 상태를 판단할 수 있다.

## 시행착오

보스 FSM intro는 실제 spawn 기준 시간과 맞아야 한다. late spawn boss가 runtime elapsed 전체를 기준으로 intro를 계산하면, 등장하자마자 phase가 건너뛰는 문제가 생길 수 있다.

midboss defeat는 victory가 아니다. midboss gate 이후 wave를 재개해야 하지만 결과 화면으로 가면 안 된다. victory는 final boss defeat나 명시적인 victory event에 묶는 편이 안전했다.

phase break 중에는 vulnerability와 fire pattern이 함께 바뀐다. 무적 상태인데 발사 패턴이 계속 돌면 시각적으로도 규칙적으로도 어색하다.

## 다음에 볼 곳

- `src/game/content/stageEvents.ts`
- `src/game/content/stage3.ts`
- `src/game/runtime/battleRuntime.ts`
- `src/game/runtime/fsm/bossFsm.ts`
- `src/game/runtime/fsm/phaseFsm.ts`
- `src/game/runtime/fsm/movementFsm.ts`
- `src/game/runtime/fsm/firePatternFsm.ts`
- `src/game/runtime/fsm/vulnerabilityFsm.ts`
- `src/game/runtime/battleRuntime.test.ts`

## 관련 노트

- [Vibe Danmaku 전투 페이싱과 런타임 타이밍 디버깅](vibe-danmaku-battle-pacing-runtime-debugging.md)
- [Vibe Danmaku R3F 보스 렌더링 트러블슈팅](vibe-danmaku-r3f-boss-rendering-troubleshooting.md)
- [Vibe Danmaku 트러블슈팅과 기술 판단 개요](vibe-danmaku-troubleshooting-and-technical-decisions.md)
