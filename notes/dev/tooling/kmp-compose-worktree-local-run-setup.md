# KMP Compose 워크트리 로컬 실행 세팅

## 한 줄 요약

Windows에서 KMP Compose 데스크톱 앱을 로컬 테스트할 때는 저장소 루트가 아니라 실제 워크트리 경로에서 `gradlew.bat`를 실행하고, JDK 21과 Ollama 연결값을 함께 맞추는 것이 가장 안정적이다.

## 언제 쓰나

- `.\gradlew.bat`를 쳤는데 명령을 찾지 못한다고 나올 때
- KMP Compose 프로젝트가 루트 저장소와 별도 git worktree를 함께 쓰고 있을 때
- Desktop 앱을 Ollama와 붙여서 빠르게 smoke test 하고 싶을 때
- `:composeApp:run`이 오래 걸리거나 멈춘 것처럼 보여 정상 동작인지 헷갈릴 때

## 핵심 개념

- KMP Compose 프로젝트는 git worktree 안에 실제 `gradlew.bat`와 Gradle 설정이 들어갈 수 있으므로 현재 셸 위치가 중요하다.
- 실행 루트는 저장소 루트가 아니라 실제 앱이 들어 있는 worktree 경로여야 한다.
- Windows KMP Compose는 JDK 21 기준으로 맞춰 두는 편이 안정적이다.
- Desktop 앱의 `:composeApp:run`은 앱 창이 떠 있는 동안 Gradle 작업이 종료되지 않으므로 `95% EXECUTING` 상태가 곧 에러를 뜻하지는 않는다.
- 로컬 AI smoke test는 `OLLAMA_BASE_URL`과 `OLLAMA_MODEL`만 맞추면 빠르게 검증할 수 있다.

## 실전 예시

저장소 루트 `<repo-root>`에서는 `gradlew.bat`가 없어 아래처럼 실패할 수 있다.

```powershell
PS <repo-root>> .\gradlew.bat :composeApp:run
.\gradlew.bat: The term '.\gradlew.bat' is not recognized ...
```

이 경우 실제 워크트리 경로로 이동해서 실행한다.

```powershell
cd <repo-root>\.worktrees\<app-worktree>
.\gradlew.bat :composeApp:run
```

Ollama까지 함께 붙여서 Desktop 앱을 확인할 때는 아래처럼 환경변수를 맞춘다.

```powershell
$env:OLLAMA_BASE_URL="<ollama-base-url>"
$env:OLLAMA_MODEL="<local-model-name>"
.\gradlew.bat :composeApp:run
```

자동 검증은 아래 조합이 가장 단순했다.

```powershell
.\gradlew.bat :composeApp:jvmTest
.\gradlew.bat :composeApp:compileKotlinJvm
```

## 주의할 점

- `:composeApp:run`은 앱을 닫기 전까지 끝나지 않으므로 실행 중인 상태와 실패를 구분해서 봐야 한다.
- `95% EXECUTING` 표시는 Desktop 앱 프로세스가 살아 있는 동안 정상적으로 보일 수 있다.
- 루트 저장소와 worktree를 함께 쓸 때는 어떤 디렉터리가 실제 앱 루트인지 먼저 확인하는 편이 빠르다.
- JDK 25 같은 최신 시스템 Java가 있어도 프로젝트 빌드는 JDK 21로 고정하는 편이 안전하다.
- Kotlin daemon 경고가 보여도 Gradle이 non-daemon compile로 fallback 하며 성공할 수 있으니, 경고와 실패를 바로 같은 것으로 보지 않는다.

## 관련 노트

- [Windows에서 KMP Compose용 JDK 21 운영](windows-jdk-21-for-kmp-compose.md)
- [KMP Compose Workshop 프로젝트 생성 시 SQLDelight NPE 트러블슈팅](../debugging/kmp-compose-workshop-project-sqldelight-npe.md)
- [개발 위키 인덱스](../../hubs/development-wiki-index.md)
