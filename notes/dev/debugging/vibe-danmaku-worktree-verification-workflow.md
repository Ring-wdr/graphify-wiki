# Vibe Danmaku worktree와 검증 중심 Git 흐름

## 한 줄 요약

Vibe Danmaku는 생성 에셋과 실험 파일이 섞이기 쉬워서, 작은 수정도 worktree 격리, focused verification, narrow staging, merge cleanup 순서가 안전했다.

## 언제 쓰나

- 현재 작업트리에 다른 생성 에셋이나 임시 파일이 있을 때
- 캐릭터 밸런스, 보스 크기, UI 문구처럼 작은 수정을 안전하게 끝내고 싶을 때
- `local commit`, `local main merge`, `push origin main` 경계를 구분해야 할 때
- Windows에서 worktree cleanup이 실패했을 때

## 기본 원칙

작업 전에 `git status --short --branch`를 먼저 본다. 이 프로젝트는 `tmp/`, 생성 이미지, 진행 중 asset wire-up이 작업트리에 남아 있을 수 있다.

작은 수정이 현재 변경분과 섞일 가능성이 있으면 `.worktrees/` 아래 helper worktree를 만든다. 이 repo에서는 `.worktrees/`가 gitignore되어 있어서 격리 작업에 적합했다.

완료 후에는 helper branch를 `main`에 fast-forward merge하고, worktree와 branch를 정리한다. 최종 검증은 정리된 local `main`에서 다시 한다.

## 검증 순서

변경 파일에 맞는 focused test를 먼저 돌린다. 예를 들어 캐릭터 밸런스면 `characters.test.ts`, 보스 렌더링이면 `battleEntities.test.tsx`, 에셋 매핑이면 `assets.test.ts`와 `battleAssetPreload.test.ts`가 먼저다.

그다음 repo 전체 기준의 `npm test`, `npm run typecheck`, `npm run build`를 본다. 앱 셸, lint config, React Compiler 정책을 건드렸다면 `npm run lint`도 포함한다.

dependency-only 변경은 `git diff --check`가 추가 guard로 쓸 만했다. source edit가 없더라도 package metadata는 좁게 stage해야 한다.

## Windows cleanup 시행착오

`git worktree remove`가 Windows에서 `Invalid argument`로 실패한 적이 있었다. merge가 이미 끝난 상황이라면 실제 worktree path를 확인한 뒤 PowerShell의 `Remove-Item -LiteralPath <path> -Recurse -Force`로 삭제하고, `git branch -d <branch>`와 `git worktree prune`까지 확인한다.

루트 아래 `.worktrees`가 남아 있으면 Vitest가 중복 테스트를 발견할 수 있다. 그래서 최종 root verification 전에는 helper worktree가 남지 않았는지 보는 편이 좋다.

## commit과 push 경계

`local commit`은 push하지 않는다. 검증 후 의도한 파일만 stage해서 local commit을 만든다.

`local main merge`는 helper branch의 결과를 local `main`에 합치고 cleanup하는 흐름이다. PR이나 remote push를 뜻하지 않는다.

`push origin main`이나 `origin push`가 들어오면 실제 push까지 끝내야 한다. push 명령이 중간에 끊겼다면 remote가 업데이트되었다고 말하면 안 된다.

## 다음에 볼 곳

- `.gitignore`
- `package.json`
- `src/game/content/characters.test.ts`
- `src/game/ui/battleEntities.test.tsx`
- `src/game/assets.test.ts`
- `src/app/battleAssetPreload.test.ts`

## 관련 노트

- [Vibe Danmaku 트러블슈팅과 기술 판단 개요](vibe-danmaku-troubleshooting-and-technical-decisions.md)
- [코드 리뷰를 위한 커밋 크기](../tooling/code-review-commit-sizing.md)
- [KMP Compose 워크트리 로컬 실행 세팅](../tooling/kmp-compose-worktree-local-run-setup.md)
