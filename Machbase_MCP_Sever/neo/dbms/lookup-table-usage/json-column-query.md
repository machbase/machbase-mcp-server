# JSON 컬럼과 JSON 조회

LOOKUP 테이블의 JSON 컬럼 지원 범위와 JSON 조건 조회를 다룹니다.

## LOOKUP JSON 조건 조회

LOOKUP 테이블은 `JSON` 컬럼을 일반 컬럼으로 지원합니다. JSON 컬럼은 유동적인 속성 값을 참조 데이터와 함께 저장할 때 사용할 수 있습니다.

```sql
CREATE LOOKUP TABLE ch9_json (
    sensor_id VARCHAR(80) PRIMARY KEY,
    location  VARCHAR(200),
    config    JSON
);

INSERT INTO ch9_json VALUES (
    'TEMP-01',
    'factory1',
    '{"unit":"celsius","level":3,"threshold":{"high":90.0}}'
);

SELECT sensor_id, config
FROM ch9_json
WHERE config->'$.unit' = 'celsius';
```

## 타입별 JSON 조건

숫자 값을 숫자로 비교할 때는 타입별 JSON 추출 함수를 사용합니다.

```sql
SELECT sensor_id
FROM ch9_json
WHERE JSON_EXTRACT_INTEGER(config, '$.level') >= 3
  AND JSON_EXTRACT_DOUBLE(config, '$.threshold.high') > 80.0;
```

JSON 구조 자체를 확인할 수도 있습니다.

```sql
SELECT sensor_id
FROM ch9_json
WHERE JSON_IS_VALID(config) = 1
  AND JSON_TYPEOF(config, '$.threshold') = 'Object';
```

## PRIMARY KEY 제약

LOOKUP 테이블은 JSON 컬럼을 저장할 수 있지만, JSON 컬럼을 `PRIMARY KEY`로 사용할 수 없습니다. 행 식별자는 `INTEGER`, `LONG`, `VARCHAR` 등 안정적인 일반 타입으로 둡니다.

```sql
-- 실패: JSON 컬럼은 primary key로 사용하지 않습니다.
CREATE LOOKUP TABLE ch9_json_bad (
    config JSON PRIMARY KEY,
    note   VARCHAR(80)
);
```

```sql
-- 권장: 별도 식별자를 primary key로 사용합니다.
CREATE LOOKUP TABLE ch9_json_ok (
    sensor_id VARCHAR(80) PRIMARY KEY,
    config    JSON,
    note      VARCHAR(80)
);
```

## 설계 기준

| 상황 | 권장 접근 |
|------|----------|
| 조인/검색에 자주 쓰는 값 | 별도 컬럼 |
| 장비별로 다른 유동 속성 | JSON 컬럼 |
| 숫자 조건 검색 | 일반 숫자 컬럼으로 분리 |
| primary key | 안정적인 식별자 컬럼 사용 |
| 고빈도 path 검색 | 별도 컬럼으로 추출 |

JSON path별 전용 인덱스는 지원하지 않습니다. 고빈도 검색 조건은 별도 컬럼으로 분리하고, 해당 컬럼에 인덱스를 적용하는 설계를 우선 검토합니다.

```sql
CREATE LOOKUP TABLE ch9_json_fast (
    sensor_id VARCHAR(80) PRIMARY KEY,
    unit      VARCHAR(16),
    level     INTEGER,
    config    JSON
);

CREATE INDEX ch9_json_unit_idx ON ch9_json_fast(unit);
```

## UPDATE·DELETE 조건

```sql
UPDATE ch9_json
SET location = 'factory2'
WHERE config->'$.unit' = 'celsius';

DELETE FROM ch9_json
WHERE JSON_EXTRACT_INTEGER(config, '$.level') < 2;
```

대상 범위가 넓을 수 있으므로 UPDATE/DELETE 전에는 같은 조건으로 건수를 확인합니다.

이 페이지의 실습 객체는 다음과 같이 정리합니다. `ch9_json_bad`는 생성에 실패하는
예제이므로 정리 대상이 아닙니다.

```sql
DROP TABLE ch9_json_fast;
DROP TABLE ch9_json_ok;
DROP TABLE ch9_json;
```

## 주의사항

- LOOKUP 테이블은 JSON 컬럼을 일반 컬럼으로 지원합니다.
- JSON 컬럼은 primary key로 사용할 수 없습니다.
- JSON path별 전용 인덱스는 지원하지 않습니다.
- 자주 검색하는 값은 LOOKUP 일반 컬럼으로 분리합니다.
- JSON path 인덱스가 필요하면 TRANSACTION 또는 TAG 테이블을 검토합니다.
