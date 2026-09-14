# set operator

집합 연산자는 두 개 이상의 `SELECT` 쿼리 결과를 합치거나 교집합/차집합을 구하는 연산자입니다.

> Machbase는 현재 `UNION ALL` 집합 연산자만 지원합니다. `UNION` (중복 제거),
> `INTERSECT`, `EXCEPT`는 지원하지 않습니다.

## UNION ALL

두 쿼리의 결과를 중복 제거 없이 합칩니다.

```sql
select_stmt UNION ALL select_stmt
```

```sql
SELECT i1, i2 FROM table_1
UNION ALL
SELECT c1, c2 FROM table_2;
```

## 사용 조건

두 `SELECT` 문은 다음 조건을 모두 만족해야 합니다.

1. **컬럼 수가 동일**해야 합니다.
2. **컬럼 타입이 같거나 호환 가능**해야 합니다.

조건 중 하나라도 불일치하면 오류가 반환됩니다.

### 타입 호환 규칙

| 조합 | 호환 여부 | 결과 타입 |
|------|-----------|-----------|
| 부호 있는 정수 ↔ 부호 없는 정수 | X | 오류 |
| 정수 ↔ 실수 | O | 실수 타입 |
| 문자 타입 (다른 길이) | O | 처리됨 |
| IPv6 ↔ IPv4 | X | 오류 |

- 결과 컬럼명은 좌측 쿼리의 컬럼명을 따릅니다.

## 예시

```sql
-- 두 테이블의 데이터를 합치기
SELECT id, name FROM active_devices
UNION ALL
SELECT id, name FROM inactive_devices;

-- 서로 다른 기간의 통계를 합치기
SELECT 'Q1' AS quarter, SUM(value) AS total FROM sales WHERE month BETWEEN 1 AND 3
UNION ALL
SELECT 'Q2' AS quarter, SUM(value) AS total FROM sales WHERE month BETWEEN 4 AND 6;

-- 세 쿼리 결합
SELECT name, time, value FROM sensor_a WHERE time > TO_DATE('2024-01-01', 'YYYY-MM-DD')
UNION ALL
SELECT name, time, value FROM sensor_b WHERE time > TO_DATE('2024-01-01', 'YYYY-MM-DD')
UNION ALL
SELECT name, time, value FROM sensor_c WHERE time > TO_DATE('2024-01-01', 'YYYY-MM-DD');
```

## 주의사항

- `UNION ALL`은 중복 행을 제거하지 않습니다. 중복 제거가 필요하면 `UNION ALL` 결과를 서브쿼리로 감싸고 `DISTINCT`나 `GROUP BY`를 적용합니다.
- `FROM` 절 없는 리터럴 `SELECT`끼리의 `UNION ALL`은 지원하지 않습니다.
- 결과 행 순서는 보장되지 않습니다. 정렬이 필요하면 전체를 인라인 뷰로 감싸고 외부에서 `ORDER BY`를 적용합니다.

```sql
-- 정렬이 필요한 경우
SELECT * FROM (
    SELECT id, name, time FROM log_a
    UNION ALL
    SELECT id, name, time FROM log_b
) ORDER BY time DESC;
```

## 관련 문서

- SELECT syntax — SELECT 기본 문법
- WITH / CTE syntax — CTE에서 UNION ALL 사용
- VIEW syntax — UNION ALL을 포함한 VIEW 생성
