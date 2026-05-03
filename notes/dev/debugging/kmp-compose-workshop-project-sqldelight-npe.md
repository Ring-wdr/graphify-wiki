# KMP Compose Workshop 프로젝트 생성 시 SQLDelight NPE 트러블슈팅

## 한 줄 요약

Desktop 앱 시작 직후 `ResultSet returned null for Project.sq:selectProjectById`가 터지면, 대개 프로젝트 생성 직후 재조회 경로가 안전하지 않아 insert 결과와 readback이 어긋난 경우다.

## 언제 쓰나

- Compose Desktop 앱이 첫 화면 렌더링 중 바로 죽을 때
- SQLDelight `executeAsOne()`가 `null` 결과로 `NullPointerException`을 던질 때
- 새 프로젝트나 숨김 초기 프로젝트를 앱 시작 시 자동 생성하는 흐름이 있을 때
- insert 후 즉시 select 하는 초기화 코드를 의심해야 할 때

## 핵심 개념

- `executeAsOne()`은 결과가 반드시 있다고 가정하므로, 초기화 경로에서는 생각보다 공격적이다.
- 앱 시작 시 숨김 `Workshop` 프로젝트를 만들고 곧바로 다시 읽는 흐름은 transaction 경계가 불명확하면 깨질 수 있다.
- 생성 직후 조회는 `executeAsOneOrNull()`과 fallback lookup으로 방어하는 편이 안전하다.
- 저장 계층과 화면 부트스트랩 계층 양쪽에 같은 취약 패턴이 있으면 한쪽만 고쳐서는 재발할 수 있다.

## 실전 예시

이 세션에서 실제로 나온 에러는 아래와 같았다.

```text
java.lang.NullPointerException: ResultSet returned null for Project.sq:selectProjectById
    at app.cash.sqldelight.ExecutableQuery.executeAsOne(Query.kt:189)
    at io.github.ringwdr.novelignite.features.workshop.WorkshopViewModelFactory_jvmKt.ensureWorkshopProject(WorkshopViewModelFactory.jvm.kt:67)
```

문제 지점은 Desktop 시작 경로의 `ensureWorkshopProject()`와 공용 저장 계층 `ProjectRepositoryImpl.createProject()`였다. 두 곳 모두 `insert -> lastInsertedRowId -> selectProjectById(...).executeAsOne()` 패턴을 쓰고 있었고, 읽기 결과가 비는 순간 앱이 바로 죽었다.

수정 방향은 아래와 같았다.

- insert와 readback을 같은 transaction 안에서 처리한다.
- `executeAsOne()` 대신 `executeAsOneOrNull()`로 1차 방어를 둔다.
- readback이 비면 같은 생성 조건의 row를 한 번 더 fallback lookup 한다.
- 화면 부트스트랩 코드와 repository 코드 둘 다 같은 방식으로 맞춘다.

이후 `:composeApp:jvmTest --tests "io.github.ringwdr.novelignite.data.local.ProjectRepositoryImplTest"`와 `:composeApp:compileKotlinJvm`를 다시 돌려 검증했고, `:composeApp:run` 캡처에서도 같은 예외는 재발하지 않았다.

## 주의할 점

- Compose Desktop에서는 composition 에러 로그가 길게 반복될 수 있으니, 첫 번째 `Exception in thread "main"`과 첫 번째 `Caused by`를 우선 본다.
- `Error was captured in composition.`가 여러 번 찍혀도 근본 원인은 보통 첫 번째 DB 예외 하나인 경우가 많다.
- 앱 시작 시 자동 생성되는 숨김 프로젝트나 세션은 id 재조회 경로를 특히 조심해야 한다.
- 테스트가 통과해도 실제 `:composeApp:run`으로 화면 부트스트랩을 한 번 더 확인하는 편이 좋다.

## 관련 노트

- [재현 우선 디버깅](repro-first-debugging.md)
- [KMP Compose 워크트리 로컬 실행 세팅](../tooling/kmp-compose-worktree-local-run-setup.md)
- [디버깅과 운영 허브](../../hubs/debugging-operations-hub.md)
