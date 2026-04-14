# Git 리베이스 기초

## 한 줄 요약

리베이스는 내 커밋을 다른 기준 커밋 위에 다시 적용해 히스토리를 더 직선적으로 정리하는 방법이다.

## 언제 쓰나

- 오래 작업한 브랜치를 최신 `main` 위로 다시 올리고 싶을 때
- merge commit 없이 리뷰 흐름을 단순하게 유지하고 싶을 때
- 내 커밋 순서를 정리하거나 불필요한 커밋을 합치고 싶을 때

## 핵심 개념

- 리베이스는 기존 커밋을 그대로 옮기는 것이 아니라 새 위치에서 다시 만든다.
- 공유된 브랜치에 리베이스하면 원격 히스토리와 충돌할 수 있다.
- interactive rebase를 쓰면 커밋 순서 변경, squash, reword가 가능하다.

## 실전 예시

```bash
git fetch origin
git rebase origin/main
git rebase -i HEAD~3
```

## 주의할 점

- 이미 다른 사람이 쓰는 브랜치에서는 강제 push가 필요할 수 있다.
- 충돌이 나면 각 커밋 단위로 해결해야 하므로 변경 의도를 이해하고 진행해야 한다.
- 히스토리를 예쁘게 만드는 목적이 실제 협업 안정성보다 앞서면 안 된다.

## 관련 노트

- [Git 체리픽과 리버트](git-cherry-pick-vs-revert.md)
- [Git 충돌 해결 체크리스트](git-conflict-resolution-checklist.md)
- [코드 리뷰를 위한 커밋 크기](../tooling/code-review-commit-sizing.md)
