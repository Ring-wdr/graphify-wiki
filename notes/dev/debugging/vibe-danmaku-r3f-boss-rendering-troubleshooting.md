# Vibe Danmaku R3F 보스 렌더링 트러블슈팅

## 한 줄 요약

보스가 작거나 납작하거나 평면 카드처럼 보일 때는 Three.js 내부 DOM보다 stage, boss role, texture, scale, fallback geometry 계약을 검증하는 편이 오래갔다.

## 언제 쓰나

- 전투 화면에서 보스 존재감이 약할 때
- R3F 테스트가 `planeGeometry` 같은 내부 구조에 과하게 묶일 때
- stage별 boss texture가 잘못 나오거나 fallback으로 떨어질 때
- Stage 3 final boss처럼 2D 스프라이트와 저폴리 모델을 섞어야 할 때

## 보스 크기 조정에서 배운 점

보스 크기를 키우는 작업은 gameplay logic이 아니라 battle presentation 변경이었다. 따라서 hp, phase, collision 같은 규칙을 건드리지 않고 `BossSprite`의 표시 크기와 fallback radius를 조정하는 것이 맞았다.

처음 테스트는 R3F 내부 DOM shape를 직접 찌르는 방식이었고 깨지기 쉬웠다. 이후에는 `bossSpriteSize`, fallback radius, renderable boss 목록처럼 공개된 계약에 가까운 지점을 검증하는 편이 나았다.

## stage별 boss texture 선택

보스 texture는 현재 stage theme와 boss role을 함께 봐야 한다. Stage 3 midboss와 final boss는 서로 다른 core asset을 가져야 하고, Stage 1 기본 보스는 기존 boss core를 유지해야 한다.

`getBossDefinitionsByRole(stage, role)`는 stage event에서 boss definition을 추출해 role별로 판단하는 핵심 helper다. 이 helper를 통해 boss id와 event role을 맞춰야 midboss/final boss texture가 뒤섞이지 않는다.

## Stage 3 final boss 모델

Stage 3 final boss는 단일 plane sprite만으로는 abyssal biomech boss의 실루엣이 충분하지 않았다. 그래서 core texture를 중심으로 armor plate, side pod, appendage sprite를 조합한 저폴리 모델을 만들었다.

중요한 조건은 stage theme가 `abyssal-biomech`이고, boss id가 final boss definition에 포함될 때만 이 경로를 타는 것이다. 그렇지 않으면 Stage 2나 기본 boss까지 Stage 3 전용 모델이 침범한다.

appendage texture가 아직 로딩되지 않았을 때도 fallback geometry가 있어야 한다. 텍스처 로딩 전 빈 보스가 보이는 것보다 임시 cone/mesh라도 남는 편이 전투 가독성에 낫다.

## phase break effect

보스 phase break는 `boss.fsm.phase === 'Break'`와 `vulnerability === 'Invulnerable'`를 함께 보고 렌더링한다. 단순히 phase id만 바뀌었다고 effect를 띄우면 armor break와 일반 phase 전환의 의미가 섞인다.

이 effect는 보스 크기와 같이 움직여야 하므로 `bossPhaseBreakInnerRadius`, `bossPhaseBreakOuterRadius`가 boss scale과 어울리는지 같이 본다.

## 다음에 볼 곳

- `src/game/ui/battleEntities.tsx`
- `src/game/ui/battleEntities.test.tsx`
- `src/game/content/stage3.ts`
- `src/game/assets.ts`
- `src/game/runtime/fsm/bossFsm.ts`

## 주의할 점

- R3F 테스트는 내부 geometry tag보다 render contract를 우선한다.
- stage별 boss asset 선택은 stage theme만 보지 말고 boss role까지 본다.
- texture fallback은 단순 예외 처리가 아니라 전투 중 가독성 장치다.
- React Compiler memoization 정책을 `src/game/ui`에 무리하게 강제하지 않는다.

## 관련 노트

- [Vibe Danmaku 생성 에셋과 프리로드 파이프라인](vibe-danmaku-generated-assets-and-preload-pipeline.md)
- [Vibe Danmaku 스테이지 이벤트 타임라인과 보스 FSM](vibe-danmaku-stage-events-and-boss-fsm.md)
- [Vibe Danmaku 트러블슈팅과 기술 판단 개요](vibe-danmaku-troubleshooting-and-technical-decisions.md)
