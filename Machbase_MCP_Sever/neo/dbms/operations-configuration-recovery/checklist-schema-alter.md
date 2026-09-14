# 스키마 변경 체크리스트

운영 중 스키마 변경 전에 아래 항목을 순서대로 확인합니다.

## 변경 전 점검

### 1. 테이블 타입 확인

```sql
SELECT NAME AS TABLE_NAME, TYPE AS TABLE_TYPE
  FROM M$SYS_TABLES
 WHERE NAME = 'TARGET_TABLE';
```

테이블 타입별 ALTER TABLE 지원 범위가 다릅니다. 테이블 타입별 관리 가능 범위를 미리 확인하십시오.

### 2. 현재 스키마 확인

```sql
-- 컬럼 정보 확인
DESC target_table;

-- 인덱스 확인
SELECT i.NAME AS INDEX_NAME, i.TYPE AS INDEX_TYPE
  FROM M$SYS_INDEXES i
  JOIN M$SYS_TABLES t
    ON i.DATABASE_ID = t.DATABASE_ID
   AND i.TABLE_ID = t.ID
 WHERE t.NAME = 'TARGET_TABLE';
```

### 3. 데이터 볼륨 확인

```sql
SELECT COUNT(*) FROM target_table;
```

대용량 테이블의 스키마 변경은 시간이 걸릴 수 있습니다. 테스트 환경에서 소요 시간과 잠금
영향을 측정한 뒤 서비스의 유지보수 시간에 실행하십시오.

### 4. Retention Policy 적용 여부

```sql
SELECT * FROM V$RETENTION_JOB WHERE TABLE_NAME = 'TARGET_TABLE';
```

스키마 변경 전 Retention Policy가 실행 중이라면 완료 후 작업하십시오.

### 5. DDL 충돌 정책 설정

Standard Edition은 서로 다른 객체의 DDL을 동시에 수행할 수 있습니다. 같은 객체나 직접
관련된 객체의 DDL은 충돌하므로 운영 배포 세션에서 허용할 대기 시간을 먼저 설정합니다.

```sql
-- 충돌한 DDL 잠금을 최대 10초 동안 대기
ALTER SESSION SET DDL_LOCK_TIMEOUT = 10;

-- 세션별 설정값 확인
SELECT id, user_name, ddl_lock_timeout
  FROM v$session
 WHERE closed = 0
 ORDER BY id;
```

| 동시 실행 대상 | 판단 |
|----------------|------|
| 이름이 서로 다른 독립 테이블 | 병렬 실행 가능 |
| 동일 객체 또는 동일 이름 | 충돌 |
| 테이블 변경·삭제 DDL과 해당 테이블의 인덱스 DDL | 충돌 |
| 뷰 DDL과 원본 테이블의 변경·삭제 DDL | 충돌 |
| TAG 테이블 변경·삭제 DDL과 해당 Rollup 또는 Retention DDL | 충돌 |

Cluster Edition에는 `DDL_LOCK_TIMEOUT`이 없으며 기존 DDL 직렬화 정책을 사용합니다. 자세한
동작은 DDL 동시성과 잠금을
참고하십시오.

---

## 컬럼 추가 체크리스트

- [ ] 추가할 컬럼의 데이터 타입이 해당 테이블 타입에서 지원되는가?
- [ ] LOG/TRANSACTION 테이블 컬럼 추가 시 기존 데이터의 새 컬럼 값은 NULL로 채워짐을 인지하고 있는가?
- [ ] 컬럼명 중복 여부 확인

```sql
ALTER TABLE sensor_log ADD COLUMN (new_col DOUBLE);
```

---

## 컬럼 삭제 체크리스트

- [ ] 삭제할 컬럼이 인덱스에 포함되어 있는가? (인덱스 먼저 삭제 필요)
- [ ] 애플리케이션에서 해당 컬럼을 참조하는 쿼리가 있는가?
- [ ] 컬럼 삭제 후 데이터는 복구 불가

```sql
ALTER TABLE sensor_log DROP COLUMN (old_col);
```

---

## 인덱스 변경 체크리스트

- [ ] 인덱스 생성/삭제는 쿼리 성능에 직접 영향
- [ ] 인덱스 생성 작업은 기존 데이터에 대한 인덱싱을 포함하므로, 대용량 테이블에서는 시간이 소요됨
- [ ] 사용하지 않는 인덱스는 INSERT 성능을 저하시키므로 삭제 고려
- [ ] `IF NOT EXISTS` 사용 시 같은 이름의 기존 인덱스 정의를 별도로 확인

```sql
-- 반복 배포에서 조건부 생성
CREATE INDEX IF NOT EXISTS idx_new ON sensor_log (sensor_id);

-- name-only no-op일 수 있으므로 실제 mapping 확인
SHOW INDEX idx_new;

-- 불필요한 인덱스 삭제
DROP INDEX idx_old;
```

`IF NOT EXISTS`는 같은 데이터베이스와 소유자의 인덱스 이름만 확인합니다. 기존 인덱스의 테이블,
컬럼, 타입과 설정 속성이 배포 의도와 일치하는지는
INDEX 문법의
규칙에 따라 별도로 검증합니다.

---

## Retention Policy 변경 체크리스트

- [ ] 정책 변경 필요 시: 기존 정책 해제 → 새 정책 생성/적용
- [ ] 보존 기간 단축 시: 다음 삭제 작업에서 대상이 늘어날 수 있으므로 데이터 손실 가능성 검토

```sql
-- 기존 정책 해제
ALTER TABLE sensor_tag DROP RETENTION;

-- 새 정책 적용
ALTER TABLE sensor_tag ADD RETENTION new_policy;
```

---

## DDL 충돌 처리

기본 `DDL_LOCK_TIMEOUT=0`에서는 충돌 시
`ERR-02031: Resource busy (<object>)`가 즉시 반환됩니다.

1. `ERR-02031`만 제한된 횟수와 대기 간격을 두고 재시도합니다.
2. 재시도하기 전에 대상 객체와 의존 객체의 현재 상태를 다시 조회합니다.
3. 대기 후에는 선행 DDL의 결과에 따라 `already exists`나 `table not found`가 반환될 수 있습니다.
4. 문법 오류, 권한 오류, `already exists`, `table not found`는 같은 SQL로 반복 재시도하지 않습니다.
5. `machsql`을 사용하는 자동화는 프로세스 종료 코드뿐 아니라 출력의 `ERR-`도 확인합니다.

DDL 대기 시간이 끝나거나 작업이 취소된 뒤에는 다시 실행할 수 있지만, 선행 작업의 반영 여부를
확인한 다음 재시도해야 합니다.

---

## 변경 후 검증

```sql
-- 스키마 변경 확인
DESC target_table;

-- 데이터 정합성 확인
SELECT COUNT(*) FROM target_table;

-- 인덱스 상태 확인
SELECT i.NAME AS INDEX_NAME, i.TYPE AS INDEX_TYPE
  FROM M$SYS_INDEXES i
  JOIN M$SYS_TABLES t
    ON i.DATABASE_ID = t.DATABASE_ID
   AND i.TABLE_ID = t.ID
 WHERE t.NAME = 'TARGET_TABLE';
```

---

**다음으로 읽을 내용:**
- 데이터 보존 정책
- 운영 및 구성
