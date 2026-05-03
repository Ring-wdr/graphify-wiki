# Vibe Danmaku 생성 에셋과 프리로드 파이프라인

## 한 줄 요약

생성형 게임 에셋은 파일을 만드는 것으로 끝나지 않고, 투명도 품질, WebP 최적화, runtime registry, preload, 렌더링 테스트까지 연결해야 안전하다.

## 언제 쓰나

- 새 캐릭터, 보스, 배경, UI ornament 에셋을 추가할 때
- PNG에서 WebP로 최적화한 뒤 화면이 깨질 때
- 배경 제거가 과하거나 부족해서 boss cutout이 어색할 때
- battle loading에서 특정 texture가 늦게 뜰 때

## 에셋 추가의 실제 흐름

Vibe Danmaku의 생성 에셋은 보통 `src/assets/generated` 아래에 원본 PNG와 런타임 WebP가 함께 놓인다. 런타임은 `src/game/assets.ts`의 `gameAssets` registry를 통해 URL을 받는다.

전투에서 쓰는 에셋은 registry에만 추가해서는 부족하다. `battleAssetPreload.ts`에도 포함해야 battle loading 단계에서 texture가 준비된다. 렌더링 컴포넌트는 이 URL을 `useLoadedTexture`나 material helper로 소비한다.

## Stage 3 boss 투명도 문제

Stage 3 boss core와 midboss core는 배경이 남으면 카드판처럼 보였다. 반대로 chroma key나 edge removal이 너무 세면 어두운 장갑 디테일까지 사라졌다.

그래서 `assets.test.ts`는 단순히 파일이 존재하는지보다 투명 픽셀 비율과 어두운 디테일 보존을 같이 본다. 이 테스트는 "배경은 투명해야 하지만 디자인의 어두운 부분은 남아야 한다"는 애매한 요구를 코드로 고정한다.

Stage 3 final boss appendage는 core와 별도 파일로 분리했다. appendage sprite는 final boss 저폴리 모델을 구성하는 부품이므로, `stage3-boss-appendages.webp`가 registry와 preload에 모두 들어가야 한다.

## WebP 최적화에서 볼 점

`scripts/optimize-runtime-assets.mjs`는 runtime asset의 크기와 품질을 조정한다. 이미지가 작아지는 것만 보면 안 되고, alpha quality와 edge removal 때문에 전투 중 실루엣이 망가지지 않는지도 봐야 한다.

`npm run assets:optimize`는 enemy atlas packing, player sprite normalization, runtime asset optimization을 이어서 실행한다. 새 asset 종류가 생기면 이 스크립트와 tests 둘 다 업데이트해야 한다.

## 프리로드 계약

Stage 3 전투 전에는 abyssal background, pressure layer, enemy atlas, midboss core, final boss core, appendage texture가 준비되어야 한다. 하나라도 빠지면 battle screen 첫 렌더에서 blank나 fallback이 보일 수 있다.

프리로드 테스트는 포함과 제외를 같이 봐야 한다. Stage 3에는 Stage 3 전용 에셋이 들어가야 하지만, Stage 1 진입 전에 Stage 2/3 boss asset을 불필요하게 당겨오면 초기 로딩이 커진다.

## 다음에 볼 곳

- `src/assets/generated`
- `src/game/assets.ts`
- `src/game/assets.test.ts`
- `src/app/battleAssetPreload.ts`
- `src/app/battleAssetPreload.test.ts`
- `scripts/pack-enemy-atlas.mjs`
- `scripts/normalize-player-sprite-sheets.mjs`
- `scripts/optimize-runtime-assets.mjs`

## 체크리스트

1. PNG 원본과 WebP 런타임 파일을 같은 역할 기준으로 배치한다.
2. `gameAssets`에 URL을 등록한다.
3. 필요한 stage preload 목록에 추가한다.
4. 렌더링 컴포넌트에서 stage theme와 role을 기준으로 소비한다.
5. 파일 존재, runtime URL, 투명도 품질, preload 포함 여부를 테스트한다.
6. 최종적으로 `npm run assets:optimize`, `npm test`, `npm run build`를 확인한다.

## 관련 노트

- [Vibe Danmaku R3F 보스 렌더링 트러블슈팅](vibe-danmaku-r3f-boss-rendering-troubleshooting.md)
- [Vibe Danmaku 트러블슈팅과 기술 판단 개요](vibe-danmaku-troubleshooting-and-technical-decisions.md)
- [로그와 메트릭과 트레이싱](logging-metrics-tracing.md)
