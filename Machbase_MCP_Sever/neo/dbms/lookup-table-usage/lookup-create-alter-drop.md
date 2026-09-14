# 생성, 변경, 삭제

LOOKUP 테이블의 생성, 변경, 삭제 방법을 다룹니다.

## Lookup 테이블 생성 및 관리

참조 테이블을 생성하는 방법은 다음과 같습니다. LOOKUP 테이블은 반드시 `PRIMARY KEY`를 지정해야 합니다.

## LOOKUP 테이블 생성

```sql
CREATE LOOKUP TABLE ch9_ddl (id INTEGER PRIMARY KEY, name VARCHAR(20));
```

운영에서 사용하는 기준 정보는 의미 있는 컬럼명을 사용해 정의합니다.

```sql
CREATE LOOKUP TABLE ch9_ddl_equip (
    equip_id   LONG PRIMARY KEY,
    equip_name VARCHAR(128),
    location   VARCHAR(64),
    status     VARCHAR(16),
    updated_at DATETIME
);
```

`PRIMARY KEY`는 행을 고유하게 식별하고 UPDATE, DELETE, JOIN의 기준이 됩니다. 여러 컬럼 조합이 비즈니스 키라면 조합 문자열을 별도 키 컬럼으로 만들거나 SEQUENCE 기반 대리키를 사용합니다.

```sql
CREATE LOOKUP TABLE ch9_ddl_price (
    price_key  VARCHAR(64) PRIMARY KEY,
    product_id VARCHAR(32),
    region     VARCHAR(16),
    price      DOUBLE
);
```

## AUTO_INCREMENT PRIMARY KEY

서버가 숫자 PRIMARY KEY를 생성해야 하면 단일 `LONG` 또는 `INT64` 컬럼에
`AUTO_INCREMENT`를 지정합니다.

```sql
CREATE LOOKUP TABLE ch9_ddl_registry (
    equip_id   LONG PRIMARY KEY AUTO_INCREMENT,
    equip_name VARCHAR(128),
    location   VARCHAR(64)
);

INSERT INTO ch9_ddl_registry(equip_name, location)
VALUES ('compressor-01', 'SEOUL-A');
```

PK 컬럼을 생략하거나 NULL로 지정하면 서버가 값을 생성합니다. 단일
`INSERT ... VALUES`에서 `0..INT64_MAX` 범위의 PK 값을 직접 지정할 수도 있습니다. 지정값이
현재 다음 자동값 이상이면 다음 자동값은 `지정값 + 1`로 진행하며, 작은 값을 지정해도
되감기지 않습니다. 데이터와 다음 자동값은 정상 재시작 후 유지됩니다.

AUTO_INCREMENT를 사용하는 LOOKUP 테이블에서는 `INSERT ... SELECT`와
`ON DUPLICATE KEY UPDATE`를 사용할 수 없습니다. SDK에서 INSERT 결과 ID를 받는 방법은
ROWID와 INSERT 결과 ID를 참고하십시오.

## SEQUENCE 컬럼 사용

자동 증가 번호가 필요하면 `LONG PROPERTY(SEQUENCE=1)` 컬럼을 사용합니다. 입력 시에는 `NEXTVAL()` 함수로 다음 값을 가져옵니다.

```sql
CREATE LOOKUP TABLE ch9_ddl_alarm (
    seq         LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    sensor_id   VARCHAR(64),
    alarm_type  VARCHAR(32),
    occurred_at DATETIME,
    message     VARCHAR(256)
);

INSERT INTO ch9_ddl_alarm
VALUES (NEXTVAL(seq), 'TEMP-01', 'HIGH', NOW, '온도 초과');
```

SEQUENCE 컬럼의 세부 정책은 SEQUENCE 컬럼에서 다룹니다.
`PROPERTY(SEQUENCE)`와 `AUTO_INCREMENT`는 별개의 기능이며 같은 컬럼에 함께 지정하지
않습니다.

## 컬럼 추가와 삭제

Standard Edition에서는 LOOKUP 테이블에 고정 길이 숫자 ARRAY 컬럼을 추가하고 삭제할 수
있습니다.

```sql
ALTER TABLE ch9_ddl_equip
    ADD COLUMN (limits DECIMAL(12,4)[2] DEFAULT [0.0000, NULL]);

ALTER TABLE ch9_ddl_equip
    DROP COLUMN (limits);
```

DEFAULT가 없으면 기존 row의 새 ARRAY 컬럼은 whole NULL입니다. DEFAULT를 지정하면 기존
row에도 해당 값을 적용합니다. ARRAY DEFAULT의 요소 수는 선언 cardinality와 정확히
같아야 합니다. ARRAY 컬럼은 PRIMARY KEY나 index key로 사용할 수 없습니다.

지원 타입과 제약은
숫자 ARRAY 타입을 참고하십시오.

## 인덱스 추가

자주 조회하거나 JOIN 조건에 사용하는 컬럼에는 인덱스를 추가합니다.

```sql
CREATE INDEX ch9_ddl_loc_idx ON ch9_ddl_equip(location);
CREATE INDEX ch9_ddl_status_idx   ON ch9_ddl_equip(status);
```

PRIMARY KEY 컬럼에는 기본 인덱스가 생성되므로, 같은 컬럼에 별도 인덱스를 중복 생성하지 않습니다. 인덱스가 많으면 입력과 갱신 비용이 증가하므로 조회 조건이 명확한 컬럼에만 추가합니다.

## 데이터 삭제와 테이블 삭제

행을 삭제하려면 `DELETE` 문을 사용합니다. 단건 삭제는 PK 조건을 사용하는 것이 가장 명확합니다.

```sql
DELETE FROM ch9_ddl_equip
WHERE equip_id = 1001;
```

일괄 삭제는 일반 조건식을 사용할 수 있습니다. 운영 데이터에서는 먼저 같은 조건으로 대상 건수를 확인합니다.

```sql
SELECT COUNT(*)
FROM ch9_ddl_equip
WHERE status = 'RETIRED';

DELETE FROM ch9_ddl_equip
WHERE status = 'RETIRED';
```

테이블 자체를 삭제하려면 `DROP TABLE`을 사용합니다.

```sql
DROP TABLE ch9_ddl_alarm;
DROP TABLE ch9_ddl_registry;
DROP TABLE ch9_ddl_price;
DROP TABLE ch9_ddl_equip;
DROP TABLE ch9_ddl;
```

`DROP TABLE`은 테이블 정의와 데이터를 모두 삭제합니다. 필요한 경우 삭제 전에 백업 또는 내보내기 절차를 수행합니다.

## 주의사항

- LOOKUP 테이블은 `PRIMARY KEY`가 필수입니다.
- `PRIMARY KEY` 컬럼은 하나만 지정합니다.
- `PRIMARY KEY` 값을 변경해야 하면 기존 행을 삭제한 뒤 새 키로 삽입합니다.
- 기준 데이터가 커지고 조회·갱신 패턴이 복잡해지면 TRANSACTION 테이블을 검토합니다.
