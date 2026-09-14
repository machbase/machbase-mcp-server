# JSON 타입의 테이블 타입별 지원 범위

JSON 타입 컬럼을 각 테이블 타입에서 사용할 때의 지원 범위를 정리합니다.

## 지원 범위 요약

| 테이블 타입 | JSON 컬럼 생성 | JSON path query | JSON PK | 비고 |
|------------|:-------------:|:---------------:|:-------:|------|
| TAG | O | O | X | JSON 컬럼과 JSON 함수 지원, PK는 미지원 |
| LOG | O | O | X | JSON 컬럼과 JSON 함수 지원 |
| LOOKUP | O | O | X | 일반 컬럼으로 지원, JSON path index는 미지원 |
| VOLATILE | X | X | X | JSON 컬럼 생성 불가 |
| TRANSACTION | O | O | X | JSON 컬럼과 JSON 함수 지원 |

## LOOKUP 테이블

LOOKUP 테이블은 JSON 타입 컬럼을 일반 컬럼으로 지원합니다.

```sql
CREATE LOOKUP TABLE config_lookup (
    key    VARCHAR(64) PRIMARY KEY,
    site   VARCHAR(32),
    config JSON
);

INSERT INTO config_lookup VALUES (
    'device-001',
    'SEOUL',
    '{"region":"kr","level":3,"state":"ready"}'
);

SELECT key
FROM config_lookup
WHERE config->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(config, '$.level') >= 3;
```

JSON 컬럼은 `JSON_SET`, `JSON_SET_JSON`, `JSON_REMOVE` 등 JSON 함수로 갱신할 수 있습니다.

```sql
UPDATE config_lookup
SET config = JSON_SET(config, '$.state', 'active')
WHERE site = 'SEOUL';
```

단, JSON 컬럼은 primary key로 선언할 수 없습니다.

```sql
-- 오류
CREATE LOOKUP TABLE invalid_lookup (
    config JSON PRIMARY KEY
);
```

## VOLATILE 테이블

VOLATILE 테이블은 JSON 타입 컬럼 생성을 지원하지 않습니다.

```sql
CREATE VOLATILE TABLE session_data (
    session_id VARCHAR(64) PRIMARY KEY,
    payload    JSON
);
```

## JSON 관련 함수 테이블 타입별 지원

| 함수/연산자 | TAG | LOG | LOOKUP | VOLATILE | TRANSACTION |
|-------------|:---:|:---:|:------:|:--------:|:---:|
| `->` 연산자 | O | O | O | X | O |
| `JSON_EXTRACT*` | O | O | O | X | O |
| `JSON_TYPEOF` | O | O | O | X | O |
| `JSON_IS_VALID` | O | O | O | O | O |
| `JSON_SET` | O | O | O | X | O |
| `JSON_SET_JSON` | O | O | O | X | O |
| `JSON_REMOVE` | O | O | O | X | O |

## 사용 주의사항

- JSON path 문자열은 작은따옴표(`'$.key'`)로 작성합니다.
- 숫자 비교에는 `JSON_EXTRACT_INTEGER`, `JSON_EXTRACT_DOUBLE` 같은 타입별 함수를 사용합니다.
- LOOKUP 테이블은 JSON path별 전용 인덱스를 지원하지 않으므로 고빈도 검색 값은 별도 컬럼으로 분리합니다.
