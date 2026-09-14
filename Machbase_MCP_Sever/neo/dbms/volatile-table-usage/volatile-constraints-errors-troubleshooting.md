# 제약, 오류, 문제 해결

VOLATILE 테이블의 제약 사항, 발생 가능한 오류, 문제 해결 방법을 다룹니다. 대부분의 문제는 메모리 한도, PRIMARY KEY 설계, 지원하지 않는 컬럼 타입, 재시작 후 데이터 소실에서 발생합니다.

## 제약 사항

VOLATILE 테이블 사용 시 다음 제약을 고려합니다.

| 항목 | 제약 |
|------|------|
| 저장 위치 | 메모리 |
| 재시작 후 데이터 | 소멸 |
| 백업·마운트 | 지원하지 않음 |
| JSON 컬럼 | 지원하지 않음 |
| PRIMARY KEY | 선택 사항, 하나만 지정 |
| UPDATE/DELETE | `PRIMARY KEY = 값` 조건만 지원 |
| 메모리 한도 | Volatile/Lookup 테이블 전체 메모리 한도 영향 |

```sql
-- 실패 예: VOLATILE 테이블에는 JSON 컬럼을 사용하지 않습니다.
CREATE VOLATILE TABLE ch10_err_json (
    session_id VARCHAR(64) PRIMARY KEY,
    payload    JSON
);
```

유동 속성이 필요하면 자주 조회하는 값을 일반 컬럼으로 분리하거나, 영속 JSON 컬럼이 필요한 경우 TRANSACTION 또는 TAG 테이블을 검토합니다.

## 메모리 부족

VOLATILE 테이블의 데이터와 인덱스는 메모리를 사용합니다. 행 수가 증가하거나 인덱스가 많으면 메모리 한도에 도달할 수 있습니다.

진단은 다음 순서로 수행합니다. 아래 실습 테이블은 이 페이지 끝에서 정리합니다.

```sql
-- 진단 예제용 실습 테이블입니다.
CREATE VOLATILE TABLE ch10_diag (
    device_id VARCHAR(64) PRIMARY KEY,
    value     DOUBLE
);
INSERT INTO ch10_diag VALUES ('DEV-01', 10.0);

-- 1. 대상 테이블의 행 수를 확인합니다.
SELECT COUNT(*) FROM ch10_diag;
```

```sql
-- 2. VOLATILE 테이블 전체의 메모리 사용을 확인합니다.
SELECT *
FROM V$STORAGE_DC_VOLATILE_TABLE;
```

필요하면 설정의 `VOLATILE_TABLESPACE_MEMORY_MAX_SIZE` 값을 확인합니다.

```sql
SELECT NAME, VALUE
FROM V$PROPERTY
WHERE NAME = 'VOLATILE_TABLESPACE_MEMORY_MAX_SIZE';
```

해결 방법은 다음과 같습니다.

- 불필요한 행을 삭제합니다.
- 캐시 보관 범위를 줄입니다.
- 사용하지 않는 인덱스를 제거합니다.
- 중요한 데이터는 영속 테이블로 옮긴 뒤 VOLATILE 테이블을 재구성합니다.
- 운영 정책에 맞게 메모리 한도 조정을 검토합니다.

## PRIMARY KEY 관련 오류

`ON DUPLICATE KEY UPDATE`, PK 기반 UPDATE, PK 기반 DELETE를 사용하려면 PRIMARY KEY가 필요합니다.

```sql
CREATE VOLATILE TABLE ch10_err_device (
    device_id  VARCHAR(64) PRIMARY KEY,
    status     VARCHAR(16),
    updated_at DATETIME
);
```

PRIMARY KEY 값은 중복될 수 없습니다. 중복 입력을 갱신으로 처리하려면 `ON DUPLICATE KEY UPDATE`를 사용합니다.

```sql
INSERT INTO ch10_err_device VALUES ('DEV-01', 'ONLINE', NOW)
ON DUPLICATE KEY UPDATE SET status = 'ONLINE', updated_at = NOW;
```

PRIMARY KEY 컬럼 자체는 UPDATE할 수 없습니다. 키를 변경해야 하는 경우 기존 행을 삭제하고
새 키로 삽입합니다.

## 재시작 후 데이터 소실

서버가 정상 종료, 비정상 종료, 재시작되면 VOLATILE 테이블 데이터는 소멸합니다. 이는 오류가 아니라 테이블 타입의 특성입니다.

문제가 발생했을 때는 다음을 확인합니다.

1. 서버 재시작 이력이 있는지 확인합니다.
2. VOLATILE 테이블 생성 스크립트가 실행되었는지 확인합니다.
3. 초기 적재 쿼리가 정상 실행되었는지 확인합니다.
4. 원본 TAG/LOG/TRANSACTION 테이블에서 캐시를 재구성합니다.

```sql
SELECT COUNT(*) FROM ch10_diag;
```

결과가 0이면 초기 적재 절차를 다시 실행합니다.

이 페이지의 실습 테이블은 다음과 같이 정리합니다.

```sql
DROP TABLE ch10_diag;
DROP TABLE ch10_err_device;
```

## 문제 해결 체크리스트

- 테이블에 저장한 데이터가 재생성 가능한지 확인합니다.
- PRIMARY KEY가 필요한 작업인지 확인합니다.
- `COUNT(*)`와 `V$STORAGE_DC_VOLATILE_TABLE`로 규모와 메모리 사용을 확인합니다.
- 재시작 후에는 초기 적재 SQL을 다시 실행합니다. 테이블은 다시 만들지 않아도 됩니다.
- 영속 보존이 필요하면 VOLATILE이 아니라 TAG, LOG, LOOKUP, TRANSACTION 테이블을 사용합니다.
