# Python asyncio 취소 처리

## 한 줄 요약

`asyncio`의 취소는 예외처럼 보이지만 사실상 제어 흐름이므로, 정리 작업과 타임아웃 설계를 함께 생각해야 한다.

## 언제 쓰나

- 비동기 작업이 타임아웃으로 중단될 때 어떤 정리가 필요한지 볼 때
- 백그라운드 태스크가 중간에 취소돼 상태가 꼬이는 문제를 다룰 때
- 재시도, 셧다운, 요청 취소가 섞인 시스템을 이해할 때

## 핵심 개념

- 취소는 보통 `CancelledError`로 전달되며, 무시하면 상위 제어 흐름이 깨질 수 있다.
- 취소 가능한 경계와 취소되면 안 되는 정리 구간을 구분해야 한다.
- 타임아웃은 기능이 아니라 예산 배분 문제라서 상위 호출 체인과 함께 설계해야 한다.

## 실전 예시

```python
try:
    await worker()
except asyncio.CancelledError:
    await cleanup()
    raise
```

## 주의할 점

- 취소 예외를 삼켜 버리면 셧다운이나 타임아웃 동작이 이상해진다.
- 정리 작업이 너무 오래 걸리면 취소의 의미가 약해진다.
- 네트워크와 데이터베이스 호출은 취소 이후 상태 일관성을 따로 점검해야 한다.

## 관련 노트

- [재현 우선 디버깅](../debugging/repro-first-debugging.md)
- [API 멱등성 기초](../architecture/api-idempotency-basics.md)
- [롤포워드와 롤백](../tooling/deployment-rollforward-vs-rollback.md)
