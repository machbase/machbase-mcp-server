# LOOKUP predicate DELETE

LOOKUP 테이블의 `DELETE`는 primary key equality 조건뿐 아니라 일반 predicate를
`WHERE` 절에 사용할 수 있습니다. 조건에 맞는 모든 row가 삭제됩니다.

## Syntax

```sql
DELETE FROM table_name
 WHERE predicate;
```

`WHERE` 절 없이 실행하면 LOOKUP 테이블의 모든 row가 삭제됩니다.

## 지원하는 조건 예

```sql
-- 일반 컬럼 조건
DELETE FROM device_lookup
WHERE status = 'EXPIRED';

-- 날짜와 범위 조건
DELETE FROM device_lookup
WHERE updated_at < TO_DATE('2026-01-01 00:00:00')
   OR score < 10;

-- JSON path 조건
DELETE FROM device_lookup
WHERE meta->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') < 2;
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
| WHERE 절 없는 전체 삭제 | O |

## 운영 주의사항

일반 predicate `DELETE`는 조건에 맞는 모든 row를 삭제합니다. 운영 데이터에서는 먼저 같은
조건으로 대상 범위를 확인한 뒤 실행합니다.

```sql
SELECT COUNT(*)
FROM device_lookup
WHERE status = 'EXPIRED';

DELETE FROM device_lookup
WHERE status = 'EXPIRED';
```

## 관련 문서

- LOOKUP predicate UPDATE syntax
- LOOKUP SQL/JSON 지원표
