# 잠금, 충돌, busy timeout

서로 다른 행을 바꾸는데도 Resource busy가 발생하면 행 잠금만 떠올려서는 원인을 찾기
어렵습니다. TRANSACTION의 쓰기 충돌은 같은 테이블의 다른 행 사이에서도 발생할 수
있습니다. 기다리면 풀리는 충돌과 트랜잭션을 새로 시작해야 하는 충돌을 구분해 보겠습니다.

## 실습 환경

이 실습은 기본 WAL 설정인 검증용 Standard 환경을 기준으로 합니다.
A·B는 같은 계정·데이터베이스에 접속한 서로 다른 연결입니다.
각 코드 블록을 표시된 순서대로 실행하고, SELECT 결과는 끝까지 읽어 커서를 닫으세요.
스냅샷 실습을 위해 운영 서버의 저널 모드를 바꾸지는 마세요.

A에서 준비합니다.

```sql
SELECT NAME, VALUE FROM V$PROPERTY WHERE NAME = 'TRANSACTION_JOURNAL_MODE';

CREATE TRANSACTION TABLE ch8_lock (id INTEGER PRIMARY KEY, val INTEGER);
INSERT INTO ch8_lock VALUES (1, 10);
INSERT INTO ch8_lock VALUES (2, 20);
```

TRANSACTION_JOURNAL_MODE=4가 WAL입니다.
다른 값이면 아래 WAL 스냅샷 실습의 결과를 그대로 기대하지 말고 환경부터 확인하세요.

## 동시 쓰기 충돌

A에서 트랜잭션을 열고 종료하지 않은 채 기다립니다.

```sql
BEGIN;
UPDATE ch8_lock SET val = 11 WHERE id = 1;
```

이어서 B에서 조회합니다. 실습용 B 연결만 대기 시간을 0으로 바꿉니다.

```sql
ALTER SESSION SET TRANSACTION_BUSY_TIMEOUT_MS = 0;
SELECT id, val FROM ch8_lock ORDER BY id;
```

B는 아직 커밋되지 않은 A의 11이 아니라 기존 값 10·20을 봅니다.
다음 B의 UPDATE는 의도적으로 Resource busy 오류가 나는 단계입니다.

```sql
-- B: A와 다른 행이지만 같은 테이블 쓰기이므로 실패가 예상됩니다.
UPDATE ch8_lock SET val = val + 1 WHERE id = 2;
```

A에서 COMMIT한 다음 B의 UPDATE를 다시 실행합니다.

```sql
-- A
COMMIT;
```

```sql
-- B
UPDATE ch8_lock SET val = val + 1 WHERE id = 2;
SELECT id, val FROM ch8_lock ORDER BY id;
```

이제 값은 11·21입니다.
같은 테이블의 쓰기 충돌을 일반적인 행 단위 잠금으로 해석하면 안 된다는 것을 보여 줍니다.

## WAL 스냅샷 충돌

이전 단계가 모두 끝난 뒤 A에서 읽기 트랜잭션을 엽니다.

```sql
-- A
BEGIN;
SELECT val FROM ch8_lock WHERE id = 1;
```

A가 11을 읽은 뒤 B에서 값을 변경합니다. B는 명시적 트랜잭션이 없는 상태입니다.

```sql
-- B
UPDATE ch8_lock SET val = val + 10 WHERE id = 1;
```

이어서 A에서 쓰기로 전환하면 스냅샷 충돌이 예상됩니다.

```sql
-- A: 의도적으로 실패하는 단계
UPDATE ch8_lock SET val = val + 1 WHERE id = 1;
```

다른 연결이 이미 커밋했으므로 A의 오래된 읽기 스냅샷을 그대로 쓰기로 전환할 수 없습니다.
현재 이 충돌은 busy timeout을 늘리거나 -1로 설정해도 기다려서 해결되지 않습니다.
같은 UPDATE만 반복하지 말고 A의 트랜잭션을 종료한 뒤 새 상태에서 다시 판단합니다.

```sql
-- A
ROLLBACK;
BEGIN;
UPDATE ch8_lock SET val = val + 1 WHERE id = 1;
COMMIT;
SELECT id, val FROM ch8_lock ORDER BY id;
```

최종 값은 22·21입니다.
업무에서 읽은 값으로 다음 변경을 계산했다면 새로운 트랜잭션에서 읽기와 판단부터
다시 해야 합니다.

## busy timeout

서버 기본 TRANSACTION_BUSY_TIMEOUT_MS는 30000ms이고 새 세션에 복사됩니다.
현재 세션은 ALTER SESSION으로 바꿀 수 있습니다.

| 값 | 일시적인 잠금 충돌 처리 |
|---|---|
| -1 | 취소·연결 종료 또는 잠금 해제까지 대기 |
| 0 | 대기 없이 busy 반환 |
| 양수 | 해당 밀리초 범위 내 대기 후 처리 또는 busy 반환 |

스냅샷 전환 충돌처럼 재시도로 풀리지 않는 경우는 이 정책의 예외입니다.
-1을 모든 충돌에 대한 무한 재시도라고 해석하지 마세요.
DDL_LOCK_TIMEOUT은 별도의 DDL 잠금 대기 설정이며 이를 바꾼다고 스냅샷 충돌이
해결되지는 않습니다.

## 오류와 재시도

메시지에 TRANSACTION이 있다는 이유만으로 재시도하면 타입·제약·권한 오류까지 반복하게
됩니다. 드라이버의 오류 코드와 전체 진단, 작업 종류를 함께 보고 재시도 가능한 잠금
충돌인지 구분하세요.

명시적 트랜잭션에서 재시도하려면 열린 결과 집합을 닫고 ROLLBACK한 뒤,
제한된 횟수·전체 요청 시간 안에서 새 트랜잭션으로 재실행합니다.
연결 유실이나 COMMIT 응답 유실은 별도 경우입니다. 이미 처리되었는지 업무 키로 확인하지
않고 카운터 증가나 주문 처리를 다시 실행하면 중복 반영될 수 있습니다.

## 충돌 진단

```sql
SELECT id, user_name, user_ip, transaction_busy_timeout_ms
  FROM V$SESSION WHERE closed = 0 ORDER BY id;

SELECT id, sess_id, state, query FROM V$STMT
 WHERE state LIKE 'Execute in progress%'
    OR state LIKE 'Fetch in progress%';
```

이 조회가 잠금 소유자를 직접 매핑해 주는 것은 아닙니다.
V$MUTEX도 서버 내부 뮤텍스 통계이지 업무 행 잠금 목록은 아닙니다.
접속 정보와 애플리케이션의 BEGIN·종료 기록을 함께 확인하세요.
세션 강제 종료는 미커밋 업무를 취소할 수 있으므로 첫 조치로 사용하지 마세요.

두 연결에 열린 트랜잭션이 없는지 확인한 뒤 A에서 정리합니다.

```sql
DROP TABLE ch8_lock;
```

실습용 연결 A·B를 종료하면 B에 지정한 세션별 timeout도 더 이상 영향을 주지 않습니다.
운영에서는 외부 API 호출·긴 계산을 BEGIN 밖으로 옮기는 것만으로도 대기 원인을 줄일 수
있습니다.
