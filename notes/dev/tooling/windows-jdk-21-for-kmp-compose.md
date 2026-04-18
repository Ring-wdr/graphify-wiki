# Windows에서 KMP Compose용 JDK 21 운영

## 한 줄 요약

Windows에서 Kotlin Multiplatform과 Compose Multiplatform을 안정적으로 돌리려면 기존 JDK 25를 지우기보다 JDK 21을 추가 설치하고 Gradle toolchain으로 21을 고정하는 편이 가장 단순하다.

## 언제 쓰나

- Windows PowerShell 환경에서 KMP + Compose 프로젝트를 시작할 때
- 시스템에 JDK 25 같은 최신 버전만 깔려 있어 Gradle 호환성이 불안할 때
- `kotlinc` 같은 별도 Kotlin CLI가 필요한지 헷갈릴 때
- `jabba` 같은 Java 버전 매니저 도입 여부를 판단할 때

## 핵심 개념

- KMP 프로젝트는 보통 `gradlew`가 Kotlin 컴파일과 테스트를 처리하므로 별도 `kotlinc` 설치가 필수는 아니다.
- Android + Desktop 타깃의 KMP/Compose에서는 JDK 21이 현재 가장 안전한 기본값이다.
- 기존 시스템 JDK 25는 남겨 두고, 프로젝트 빌드만 Gradle toolchain으로 21을 쓰게 하면 공존이 가능하다.
- Windows에서는 `jabba`보다 `winget + Gradle toolchain` 조합이 단순한 경우가 많다.
- 특히 오래된 `jabba`는 원격 목록이 JDK 17까지만 보이는 경우가 있어 JDK 21 관리에 바로 쓰기 어렵다.

## 실전 예시

JDK 21을 `winget`으로 추가 설치한다.

```powershell
winget install --id Microsoft.OpenJDK.21 -e
```

Temurin 다운로드가 GitHub에서 멈추면 아래 대안도 사용할 수 있다.

```powershell
winget install --id Amazon.Corretto.21.JDK -e
winget install --id Azul.Zulu.21.JDK -e
```

KMP 모듈의 `build.gradle.kts`에서는 toolchain을 21로 고정한다.

```kotlin
kotlin {
    jvmToolchain(21)
}
```

이 방식이면 시스템 기본 `java`가 25를 가리켜도 프로젝트 빌드는 21 기준으로 맞출 수 있다.

## 주의할 점

- JDK 배포판보다 더 중요한 것은 프로젝트가 실제로 JDK 21로 빌드되도록 고정하는 것이다.
- 시스템 Java를 무조건 삭제할 필요는 없고, 혼란이 생길 때만 PATH와 `JAVA_HOME`을 정리하면 된다.
- `jabba`를 이미 설치했다면 Windows 셸 함수와 폴더 흔적이 남을 수 있으니 제거 여부를 새 셸에서 다시 확인하는 편이 안전하다.
- 위저드가 생성한 Gradle, Kotlin, AGP 버전은 초기에 임의로 크게 올리지 않는 편이 안정적이다.

## 관련 노트

- [개발 위키 인덱스](../../hubs/development-wiki-index.md)
- [Graphify Wiki Overview](../../meta/graphify-wiki-overview.md)
- [Git Knowledge Workflow](../../meta/git-knowledge-workflow.md)
