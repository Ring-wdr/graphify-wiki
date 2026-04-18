# 로컬 노트 코파일럿 RN Expo 트러블슈팅

## 한 줄 요약

Expo Router, SQLite, 로컬 서버, 앱 테마가 한 화면에서 동시에 얽히기 시작하면 문제는 대개 상태 동기화 경계에서 나온다.

## 언제 쓰나

- Expo Router 기반 앱에서 화면 진입 시점 데이터 갱신이 자꾸 어긋날 때
- `light` `dark` `system` 테마를 앱 설정과 시스템 설정에 함께 물려야 할 때
- `expo-sqlite` 초기화 이전에 화면이 먼저 떠서 데이터나 설정이 비어 보일 때
- 에뮬레이터에서는 되는데 실제 기기에서 로컬 서버 호출이 실패할 때

## 이 프로젝트에서 실제로 보인 포인트

### 1. 시스템 테마만으로는 앱 테마 요구사항을 못 덮는다

- 이 프로젝트는 `useColorScheme()`를 직접 각 화면에서 쓰지 않고 `AppThemeProvider` 안에서 감싼다.
- 이유는 시스템 테마만 읽는 것으로 끝나지 않고, 사용자 설정값 `light | dark | system`을 SQLite에 저장하고 다시 불러와야 하기 때문이다.
- 현재 구현은 `apps/mobile/src/lib/theme.tsx`에서 시스템 테마를 읽고, 저장된 `themeMode`가 `system`일 때만 최종 `resolvedTheme`를 계산한다.
- 이 구조 덕분에 설정 화면에서 앱 강제 라이트 모드나 강제 다크 모드를 선택해도 시스템 설정과 분리해서 유지할 수 있다.

### 2. 테마 색상은 중앙에서 고르고 스타일은 화면에서 조립하는 편이 안전하다

- `apps/mobile/src/constants/ui.ts`에 라이트 다크 토큰이 모여 있고, 각 화면은 `useAppTheme()`로 `colors`를 받아 `createStyles(colors)`를 호출한다.
- 이 패턴은 화면별 커스텀 레이아웃을 유지하면서도 토큰 출처를 한 군데로 묶어 준다.
- 다만 이 레포에는 Expo 기본 스캐폴드에서 온 `constants/theme.ts`, `hooks/use-theme.ts`, `ThemedText`, `ThemedView`도 아직 남아 있다.
- 테마 소스가 둘로 갈라지면 일부 화면은 새 테마 컨텍스트를 따르고 일부 컴포넌트는 예전 `useColorScheme` 경로를 타게 된다.
- 새 구조를 계속 밀고 갈 거라면 결국 한쪽으로 수렴시키는 정리가 필요하다.

### 3. SQLite는 앱 셸보다 먼저 준비되어야 한다

- `apps/mobile/src/app/_layout.tsx`는 앱 시작 시 `bootstrapDatabase()`를 먼저 호출하고, 설정을 읽은 뒤에야 `AppThemeProvider`와 라우터를 렌더링한다.
- 이 순서가 중요한 이유는 `themeMode`, `llmBaseUrl`, `requestTimeoutMs` 같은 설정이 화면 첫 렌더 전에 필요하기 때문이다.
- 초기화 전에 화면을 먼저 띄우면 기본값 깜빡임, 잘못된 테마, 빈 설정 화면 같은 증상이 생기기 쉽다.
- `db/client.ts`에서 `databasePromise`를 모듈 스코프에 캐시하는 것도 중복 오픈을 줄이는 데 도움이 된다.

### 4. Expo Router에서는 화면 복귀 시점 새로고침을 별도로 챙겨야 한다

- 노트 목록, 기록, 설정 화면은 `useFocusEffect`로 포커스 시점에 데이터를 다시 읽는다.
- 한 번 `useEffect`로만 불러오면 하위 화면에서 저장한 값이 상위 화면에 늦게 반영될 수 있다.
- 설정 상세 화면에서 서버 주소, 모델, 테마를 바꾼 뒤 뒤로 돌아왔을 때 목록이 바로 갱신되는 이유도 이 패턴 덕분이다.

### 5. 커스텀 헤더를 두면 라우팅 메타를 중앙화하는 편이 덜 아프다

- 이 프로젝트는 Expo Router 기본 헤더를 끄고 `GlobalRouteBar`를 별도로 둔다.
- 그러면 제목, 뒤로 가기 노출 여부, fallback route를 각 화면이 제각각 계산하지 않도록 `lib/route-header.ts` 같은 중앙 매핑이 필요해진다.
- 실제로 `/settings/theme`, `/settings/server`, `/settings/model`, `/notes/[id]`가 모두 여기서 타이틀과 뒤로 가기 동작을 정한다.
- 이 매핑이 없으면 파일 구조는 맞는데 헤더 제목이나 뒤로 가기 목적지가 틀리는 식의 버그가 자주 난다.

### 6. 로컬 서버 주소는 에뮬레이터 성공과 실제 기기 성공이 다르다

- 기본 `llmBaseUrl`은 `http://127.0.0.1:8787`로 저장된다.
- 이 값은 호스트 머신이나 같은 환경의 시뮬레이터에서는 맞을 수 있지만, 실제 기기에서는 기기 자신의 루프백을 가리키므로 실패한다.
- README에도 실제 기기 테스트 시에는 호스트 머신의 LAN IP로 바꾸라고 적혀 있다.
- 이런 류의 이슈는 코드 버그처럼 보이지만 네트워크 경계 문제인 경우가 많다.

### 7. 요청 타임아웃은 fetch 실패를 디버깅 가능한 실패로 바꿔 준다

- `apps/mobile/src/api/client.ts`는 `AbortController`로 요청 타임아웃을 강제한다.
- 로컬 LLM 호출은 모델 상태와 시스템 부하에 따라 응답 시간이 흔들리기 쉬워서 타임아웃이 없으면 사용자는 그냥 멈춘 것으로 느낀다.
- 타임아웃 값을 설정으로 저장해 둔 것도 실험 단계에서는 유용하다.

## 자주 부딪히는 증상과 먼저 볼 위치

- 앱이 첫 진입에서 이상한 배경색으로 뜬다
  `apps/mobile/src/lib/theme.tsx`, `apps/mobile/src/app/_layout.tsx`, `apps/mobile/src/constants/ui.ts`
- 테마 설정 저장 후 일부 컴포넌트만 색이 안 바뀐다
  `AppThemeProvider` 경로와 `ThemedText` `ThemedView` 같은 레거시 테마 경로가 섞였는지 본다.
- 설정 화면에서 바꾼 값이 이전 화면에 바로 반영되지 않는다
  `useFocusEffect`가 빠졌는지 본다.
- 실제 기기에서 서버 헬스체크가 실패한다
  `llmBaseUrl`이 `127.0.0.1`인지 먼저 본다.
- 노트나 설정이 비어 있는 채로 잠깐 보였다가 다시 채워진다
  DB 부트스트랩 이전 렌더가 있었는지 본다.

## 현재 기준 권장 정리 방향

- 테마 진입점은 `useAppTheme()` 하나로 정리한다.
- Expo 기본 스캐폴드에서 남은 `ThemedText`, `ThemedView`, `constants/theme.ts`는 계속 쓸지 제거할지 빠르게 결정한다.
- 화면 복귀 후 최신 데이터가 필요한 곳은 `useEffect`보다 `useFocusEffect`를 우선 검토한다.
- 앱 시작 의존성이 설정값에 걸려 있으면 루트 레이아웃에서 부트스트랩을 끝낸 뒤 화면을 렌더한다.
- 로컬 서버 연결 설정 화면에는 실제 기기용 안내를 더 분명히 둔다.

## 관련 노트

- [로그와 메트릭과 트레이싱](logging-metrics-tracing.md)
- [재현 우선 디버깅](repro-first-debugging.md)
