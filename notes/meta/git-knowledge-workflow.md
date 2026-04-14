# Git Knowledge Workflow

이 저장소에서 Git은 지식 변화의 이력을 읽기 쉽게 남기는 도구다.

## 핵심 원칙

- `notes/`를 원본 자산으로 본다.
- `graphify-out/`는 파생 산출물로 취급한다.
- 구조 변경과 내용 변경을 같은 커밋에 섞지 않는다.
- 파일 이동이나 개명은 링크 수정과 같은 커밋에서 끝낸다.

## 권장 커밋 타입

- `notes:` 새 원자 노트 추가 또는 내용 수정
- `hubs:` 허브 문서 구조 조정
- `taxonomy:` 폴더 구조나 파일명 규칙 개편
- `meta:` 템플릿과 운영 문서 수정
- `graph:` 그래프 산출물 재생성

## 권장 작업 순서

1. 원자 노트 작성 또는 수정
2. 관련 허브와 연관 링크 갱신
3. `notes:` 또는 `hubs:` 커밋
4. `uv run python scripts/wiki_status.py`로 현재 상태 확인
5. `uv run python scripts/rebuild_wiki_graph.py` 실행
6. `uv run python scripts/wiki_status.py`로 그래프 산출물만 바뀌었는지 확인
7. `graph:` 커밋

## 빠른 점검 명령

```bash
uv run python scripts/wiki_status.py
```

이 명령은 아래를 짧게 보여 준다.

- `notes/` 변경 수
- `graphify-out/` 변경 수
- `README.md`, `scripts/` 같은 운영 변경 수
- 노트보다 그래프 산출물이 오래됐는지 여부

## 권장 커밋 분리 예시

1. 새 노트 작성 후 `notes:` 커밋
2. 그래프 재생성 후 `graph:` 커밋

이 순서를 지키면 Git log만 봐도 지식 자체의 변화와 파생 산출물 갱신을 구분하기 쉽다.

## 공개 저장소 규칙

- 회사명, 고객명, 내부 URL, 비밀 설정값은 기록하지 않는다.
- 실제 사례는 일반화된 패턴으로 정리한다.
- 공개 불가 메모는 별도 비공개 저장소나 로컬 저장소에서 관리한다.
