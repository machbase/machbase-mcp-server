# LOOKUP predicate UPDATE

LOOKUP 테이블의 `UPDATE`는 primary key equality 조건뿐 아니라 일반 predicate를
`WHERE` 절에 사용할 수 있습니다. 조건에 맞는 모든 row가 갱신됩니다.

## Syntax

```sql
UPDATE table_name
   SET column_name = expression [, column_name = expression ...]
 WHERE predicate;
```

## 지원하는 조건 예

```sql
-- 일반 컬럼 조건
UPDATE device_lookup
SET status = 'ACTIVE'
WHERE site = 'SEOUL' AND status = 'READY';

-- 범위와 문자열 조건
UPDATE device_lookup
SET score = score + 10
WHERE score BETWEEN 10 AND 80
  AND note LIKE 'sensor-%';

-- JSON path 조건
UPDATE device_lookup
SET meta = JSON_SET(meta, '$.state', 'active')
WHERE meta->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') >= 3;
```

`SET` 절의 오른쪽 표현식은 현재 row의 값을 참조할 수 있습니다.

```sql
UPDATE device_lookup
SET score = score + 1
WHERE group_name IN ('A', 'B');
```

## 지원 조건 범위

| 조건 | 지원 |
|------|:---:|
| `pk_col = value` | O |
| `non_pk_col = value` | O |
| `<`, `<=`, `>`, `>=`, `<>` | O |
| `BETWEEN` | O |
| `IN`, `NOT IN` | O |
| `LIKE`, `NOT LIKE` | O |
| `AND`, `OR`, `NOT` | O |
| `IS NULL`, `IS NOT NULL` | O |
| `TO_DATE(...)` 날짜 조건 | O |
| JSON `->`, `JSON_EXTRACT_*`, `JSON_IS_VALID` | O |

## 제약

- Primary key 컬럼 자체는 `SET` 절에서 변경할 수 없습니다.
- 조건에 맞는 row가 여러 개이면 여러 row가 갱신됩니다.
- JSON path 문자열은 작은따옴표(`'$.key'`)로 작성합니다. 큰따옴표는 SQL 식별자로 해석됩니다.
- 숫자 JSON 값을 비교할 때는 `JSON_EXTRACT_INTEGER`, `JSON_EXTRACT_DOUBLE` 같은 타입별 함수를 권장합니다.

## 관련 문서

- LOOKUP predicate DELETE syntax
- LOOKUP SQL/JSON 지원표
