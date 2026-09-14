# 데이터 보존 정책

Retention Policy는 TAG, KV, LOG 테이블에서 기준 시각보다 오래된 데이터를 주기적으로
삭제합니다. `DURATION`은 보존 기간이고 `INTERVAL`은 삭제 작업의 실행 주기입니다.
TRANSACTION, VOLATILE, LOOKUP 테이블에는 적용할 수 없습니다.

```text
정책 생성 → 테이블 적용 → 실행 상태 확인 → 테이블에서 해제 → 정책 삭제
```

## Retention Policy

운영 정책을 만들기 전에 법적 보관 의무, 복구 요구사항, 시간당 유입량과 삭제 부하를 함께
검토합니다. 고정 비율로 `INTERVAL`을 정하지 말고 운영 환경에서 측정한 삭제 시간보다 충분히
긴 주기를 사용하십시오.

정책과 적용 상태는 다음 뷰에서 확인합니다.

```sql
SELECT * FROM M$RETENTION;
SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE, LAST_DELETED_TIME
  FROM V$RETENTION_JOB;
```

### Retention Policy 생성

```sql
CREATE RETENTION policy_name
    DURATION duration_value {MONTH|DAY|HOUR|MIN|SEC}
    INTERVAL interval_value {DAY|HOUR|MIN|SEC};
```

`DURATION`은 월부터 초까지, `INTERVAL`은 `DAY`부터 `SEC`까지 지정할 수 있습니다. `MONTH`는 달력
월이 아니라 고정 30일이므로 법적 보관처럼 달력 경계가 중요한 정책은 `DAY` 단위로 환산하고
실제 삭제 기준을 검증합니다. 정확한 파서 문법과 적용 가능한 테이블 타입은
RETENTION 문법을 참고합니다.

예를 들어 30일을 보존하고 하루마다 삭제 대상을 처리하는 정책은 다음과 같습니다.

```sql
CREATE RETENTION policy_30d DURATION 30 DAY INTERVAL 1 DAY;
SELECT * FROM M$RETENTION WHERE POLICY_NAME = 'POLICY_30D';
```

정책 생성과 삭제에는 필요한 관리 권한이 있어야 합니다. 운영 계정으로 실행하기 전에 권한과
변경 승인 범위를 확인하십시오.

### 테이블에 적용

```sql
ALTER TABLE sensor_tag ADD RETENTION policy_30d;

SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE
  FROM V$RETENTION_JOB
 WHERE TABLE_NAME = 'SENSOR_TAG';
```

한 테이블에는 하나의 정책만 적용할 수 있습니다. TAG 테이블은 `BASETIME`, LOG 테이블은
`_ARRIVAL_TIME`을 기준으로 오래된 데이터를 판정합니다. 적용 직후 삭제되는 것이 아니라
설정한 주기에 따라 작업이 실행됩니다.

### 테이블에서 해제

```sql
ALTER TABLE sensor_tag DROP RETENTION;
```

해제하면 자동 삭제가 중단되지만 이미 삭제된 데이터는 복구되지 않습니다. 해제 후
`V$RETENTION_JOB`에서 대상 테이블이 사라졌는지 확인합니다.

### Retention Policy 삭제

정책을 사용하는 모든 테이블에서 먼저 해제한 뒤 정책 객체를 삭제합니다.

```sql
SELECT USER_NAME, TABLE_NAME
  FROM V$RETENTION_JOB
 WHERE POLICY_NAME = 'POLICY_30D';

-- 조회된 각 테이블에서 정책을 해제한 뒤 실행
DROP RETENTION policy_30d;
```

`ALTER TABLE ... DROP RETENTION`은 테이블과 정책의 연결을 해제하고, `DROP RETENTION`은
정책 객체를 삭제합니다. 적용 중인 정책은 삭제할 수 없습니다.

### 적용 범위와 권한

| 테이블 타입 | 적용 가능 |
|---|---|
| TAG, KV, LOG | 예 |
| TRANSACTION, VOLATILE, LOOKUP | 아니요 |

정책을 만들거나 삭제할 계정과 테이블 소유 계정이 다르면 운영 전에 실제 권한 구성을
검증하십시오. 다른 소유자의 테이블을 대상으로 할 때는 명시적으로 필요한 권한만 부여합니다.

### 실행 상태 확인

```sql
SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE, LAST_DELETED_TIME
  FROM V$RETENTION_JOB
 ORDER BY USER_NAME, TABLE_NAME;
```

`STATE`는 작업의 현재 상태이고, `LAST_DELETED_TIME`은 마지막 삭제 작업에 사용한 기준
시각입니다. 벽시계 기준의 작업 완료 시각으로 해석하지 마십시오. 실제 삭제 여부는 대상
테이블의 가장 오래된 시간과 행 수 추세를 함께 확인합니다.
