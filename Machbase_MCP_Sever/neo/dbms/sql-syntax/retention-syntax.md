# RETENTION

RETENTION 정책은 TAG, KV, LOG 테이블에서 보존 기간을 지난 데이터를 주기적으로 삭제합니다.
TRANSACTION, LOOKUP, VOLATILE에는 적용할 수 없습니다.

## RETENTION 정책 생성

```sql
create_retention_stmt ::=
    'CREATE RETENTION' policy_name
    'DURATION' positive_integer ( 'MONTH' | 'DAY' | 'HOUR' | 'MIN' | 'SEC' )
    'INTERVAL' positive_integer ( 'DAY' | 'HOUR' | 'MIN' | 'SEC' )
```

| 매개변수 | 설명 |
|----------|------|
| `policy_name` | 정책 이름 |
| `DURATION duration MONTH\|DAY\|HOUR\|MIN\|SEC` | 데이터 보존 기간 (`MONTH`는 고정 30일) |
| `INTERVAL interval DAY\|HOUR\|MIN\|SEC` | 삭제 실행 주기 |

```sql
-- 1일 보존, 1시간마다 삭제 실행
CREATE RETENTION policy_1d_1h DURATION 1 DAY INTERVAL 1 HOUR;

-- 30일 보존, 1일마다 삭제 실행
CREATE RETENTION policy_30d_1d DURATION 30 DAY INTERVAL 1 DAY;

-- 3개월 보존, 1일마다 삭제 실행
CREATE RETENTION policy_3m_1d DURATION 3 MONTH INTERVAL 1 DAY;
```

## RETENTION 정책 삭제

```sql
drop_retention_stmt ::= 'DROP RETENTION' policy_name
```

```sql
DROP RETENTION policy_1d_1h;
```

## 테이블에 RETENTION 정책 적용

```sql
alter_table_add_retention_stmt ::=
    'ALTER TABLE' table_name 'ADD RETENTION' policy_name
```

```sql
ALTER TABLE sensor_tag ADD RETENTION policy_1d_1h;
```

## 테이블에서 RETENTION 정책 해제

```sql
alter_table_drop_retention_stmt ::=
    'ALTER TABLE' table_name 'DROP RETENTION'
```

```sql
ALTER TABLE sensor_tag DROP RETENTION;
```

## RETENTION 정책 목록 조회

시스템 테이블에서 등록된 RETENTION 정책과 적용 현황을 조회합니다.

```sql
-- 모든 RETENTION 정책 조회
SELECT * FROM M$RETENTION;

-- 테이블별 적용 작업과 마지막 삭제 기준 확인
SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE, LAST_DELETED_TIME
  FROM V$RETENTION_JOB
 ORDER BY USER_NAME, TABLE_NAME;
```

## 전체 예시

```sql
-- 1. RETENTION 정책 생성 (1일 보존, 1시간마다 삭제)
CREATE RETENTION ret_1d DURATION 1 DAY INTERVAL 1 HOUR;

-- 2. TAG 테이블 생성
CREATE TAG TABLE sensor_tag (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- 3. 테이블에 RETENTION 정책 적용
ALTER TABLE sensor_tag ADD RETENTION ret_1d;

-- 4. 정책 적용 확인
SELECT * FROM M$RETENTION;

-- 5. 정책 해제
ALTER TABLE sensor_tag DROP RETENTION;

-- 6. 정책 삭제
DROP RETENTION ret_1d;
```

## 주의사항

- RETENTION 정책은 LOG 테이블과 TAG 테이블에 적용할 수 있습니다.
- KV 테이블에도 적용할 수 있습니다.
- 한 테이블에는 하나의 RETENTION 정책만 적용할 수 있습니다.
- `MONTH`는 달력 월이 아니라 고정 30일로 계산됩니다. 달력 경계가 중요한 정책은 `DAY` 단위로
  환산하고 실제 삭제 기준을 검증합니다.
- RETENTION 작업이 삭제한 row는 되돌릴 수 없으므로 보존 기간과 실행 주기를 신중하게
  설정합니다. `DROP RETENTION`은 table에서 정책을 모두 해제한 뒤 정책 객체만 삭제합니다.
- `INTERVAL`은 삭제 작업 실행 주기이며, 실제 삭제 시각은 약간 지연될 수 있습니다.
- 존재하지 않는 정책, 지원하지 않는 테이블 타입, 한 테이블의 중복 정책 적용은 오류입니다.
- 적용 중인 정책 객체는 모든 테이블에서 해제한 뒤 삭제합니다.

## 관련 문서

- Retention Policy 역할 — 자동 데이터 삭제 정책 개념
