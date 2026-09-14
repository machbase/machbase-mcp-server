# 생성, 변경, 삭제

VOLATILE 테이블의 생성·삭제 방법과 다른 테이블 타입과의 영속성 차이를 다룹니다.

## Volatile 테이블 생성 및 관리

volatile 테이블의 생성 및 삭제 방법은 다음과 같습니다.

### 생성

```sql
create volatile table vtable (id1 integer, name varchar(20));
```

### Volatile 테이블 생성 및 관리 삭제

```sql
drop table vtable;
```

## 영속성 차이·DDL

VOLATILE 테이블은 다른 테이블 타입과 달리 메모리에만 존재합니다.

### 영속성 비교

| 항목 | VOLATILE | LOOKUP | TRANSACTION | TAG | LOG |
|------|----------|--------|-----|-----|-----|
| 저장 위치 | 메모리 | 디스크 | 디스크 | 디스크 | 디스크 |
| 서버 재시작 후 데이터 유지 | X | O | O | O | O |
| 테이블 구조(DDL) 유지 | O | O | O | O | O |

### DDL 특성

VOLATILE에서 사라지는 것은 데이터이고, 테이블 정의는 다른 테이블 타입과 마찬가지로
영속 저장됩니다. 재시작 후 필요한 작업은 재생성이 아니라 초기 적재입니다.

```sql
-- 테이블 정의는 한 번만 만들면 됩니다.
CREATE VOLATILE TABLE ch10_ddl (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    updated_at DATETIME
);
```

### 생성 문법

기본 구문은 `CREATE VOLATILE TABLE 테이블명 (컬럼 정의, ...)`입니다. 키 기반 갱신이나 삭제가
필요할 때 한 컬럼에 `PRIMARY KEY`를 지정합니다.

- `PRIMARY KEY`는 선택 사항입니다.
- PRIMARY KEY 컬럼은 하나만 지정합니다.

### AUTO_INCREMENT PRIMARY KEY

서버가 숫자 PRIMARY KEY를 생성해야 하면 단일 `LONG` 또는 `INT64` 컬럼에
`AUTO_INCREMENT`를 지정합니다.

```sql
CREATE VOLATILE TABLE ch10_ddl_seq (
    request_id LONG PRIMARY KEY AUTO_INCREMENT,
    payload    VARCHAR(256)
);

INSERT INTO ch10_ddl_seq(payload) VALUES('refresh');
```

PK 컬럼을 생략하거나 NULL로 지정하면 서버가 값을 생성합니다. 단일
`INSERT ... VALUES`에서 `0..INT64_MAX` 범위의 PK 값을 직접 지정할 수도 있습니다. 지정값이
현재 다음 자동값 이상이면 다음 자동값은 `지정값 + 1`로 진행하며, 작은 값을 지정해도
되감기지 않습니다.
AUTO_INCREMENT를 사용하는 VOLATILE 테이블에서는 `INSERT ... SELECT`와
`ON DUPLICATE KEY UPDATE`를 사용할 수 없습니다.

VOLATILE 테이블은 서버 재시작 시 데이터가 사라지므로 다음 자동값도 1부터 다시
시작합니다. 테이블 정의는 유지되므로 다시 만들 필요는 없습니다. SDK에서 INSERT 결과 ID를 받는 방법은
ROWID와 INSERT 결과 ID를 참고하십시오.

### 컬럼 추가와 삭제

Standard Edition에서는 VOLATILE 테이블에 고정 길이 숫자 ARRAY 컬럼을 추가하고 삭제할
수 있습니다.

```sql
ALTER TABLE ch10_ddl
    ADD COLUMN (thresholds DOUBLE[2] DEFAULT [10.0, 20.0]);

ALTER TABLE ch10_ddl
    DROP COLUMN (thresholds);
```

VOLATILE은 기존 scalar `ADD COLUMN`과 마찬가지로 ALTER 전에 존재한 row를 DEFAULT로 다시
쓰지 않습니다. ARRAY DEFAULT를 지정해도 기존 row의 새 컬럼은 whole NULL입니다. 이
동작은 LOG, LOOKUP, TRANSACTION과 TAG METADATA의 backfill 규칙과 다릅니다.

ARRAY의 지원 요소 타입, cardinality와 DEFAULT 규칙은
숫자 ARRAY 타입을 참고하십시오.

### 영속성 차이·DDL 삭제

```sql
DROP TABLE ch10_ddl;
DROP TABLE ch10_ddl_seq;
```

### 주의사항

- VOLATILE 테이블의 DDL(구조 정의)은 데이터베이스에 저장되며 서버 재시작 후에도 남습니다.
- 데이터는 재시작 후 자동 복원되지 않으므로, 초기 적재 스크립트(예: 시작 시 machsql 실행)를 구성해야 합니다.
