# SELECT

`SELECT`는 Machbase의 다양한 테이블에서 데이터를 조회·필터링·집계하는 구문입니다.

## SELECT 전체 문법

```sql
query_stmt ::=
    [ with_clause ]
    select_stmt

select_stmt ::=
    'SELECT' [ hint_clause ] target_list
    [ 'FROM' table_reference_list ]
    [ 'WHERE' condition_expr ]
    [ 'DURATION' duration_expr ]
    [ 'GROUP BY' expr_list [ 'HAVING' condition_expr ] ]
    [ 'ORDER BY' expr_list [ 'ASC' | 'DESC' ] ]
    [ 'SERIES BY' condition_expr ]
    [ 'LIMIT' [ offset ',' ] row_count ]

-- 집합 연산자
select_stmt 'UNION ALL' select_stmt
```

`DURATION`은 `WHERE` 뒤, `GROUP BY`·`HAVING`·`ORDER BY`·`SERIES BY`·`LIMIT`보다 앞에 작성합니다.
위 문법에 나열된 순서는 SQL 절의 작성 순서이며, 내부 실행 순서를 의미하지 않습니다.

`with_clause`는 Standard Edition에서 비재귀 CTE를 선언합니다. 전체 문법과 제한은
WITH / CTE syntax를 참고하십시오.

### 대상 목록 (target_list)

```sql
target_list ::=
    '*'
  | target_expr ( ',' target_expr )*

target_expr ::=
    column_name [ 'AS' alias ]
  | expr [ 'AS' alias ]
  | '(' subquery ')' [ 'AS' alias ]
```

### FROM 절

```sql
table_reference_list ::=
    table_reference ( ',' table_reference )*

table_reference ::=
    table_name [ alias ]
  | '(' subquery ')' [ alias ]
  | table_name [ alias ] join_clause
  | view_name [ alias ]

join_clause ::=
    [ 'INNER' | 'LEFT OUTER' | 'RIGHT OUTER' ] 'JOIN' table_reference 'ON' condition_expr
  | 'CROSS JOIN' table_reference
```

---

## FROM 절 없는 SELECT

테이블 조회 없이 상수, 산술식, 단순 함수 결과를 1행으로 반환합니다.

```sql
SELECT 1;
SELECT 'alive';
SELECT 1 + 2;
SELECT ABS(-7);
SELECT SYSDATE;
```

---

## WHERE 절

```sql
condition_expr ::=
    expr comparison_op expr
  | expr [ 'NOT' ] 'BETWEEN' expr 'AND' expr
  | column_name [ 'NOT' ] 'IN' '(' value_list | subquery ')'
  | column_name 'RANGE' duration_spec
  | column_name [ 'NOT' ] 'SEARCH' string_literal
  | column_name 'ESEARCH' pattern_literal
  | column_name [ 'NOT' ] 'REGEXP' pattern_literal
  | expr 'IS' [ 'NOT' ] 'NULL'
  | condition_expr ( 'AND' | 'OR' ) condition_expr
  | 'NOT' condition_expr
  | '(' condition_expr ')'
  | '(' subquery ')'
```

### 주요 WHERE 연산자

| 연산자 | 설명 |
|--------|------|
| `=`, `<>`, `<`, `<=`, `>`, `>=` | 비교 연산자 |
| `BETWEEN value1 AND value2` | 범위 조건 |
| `IN (value_list)` | 값 목록 조건 |
| `IN (subquery)` | 서브쿼리 IN |
| `RANGE n unit` | 현재 시각 기준 시간 범위 조건 |
| `SEARCH 'keyword'` | 키워드 인덱스 기반 텍스트 검색 |
| `ESEARCH 'pattern%'` | 확장 텍스트 검색 (% 와일드카드) |
| `REGEXP 'pattern'` | 정규 표현식 검색 (인덱스 미사용) |
| `IS NULL` / `IS NOT NULL` | NULL 조건 |

```sql
-- BETWEEN
SELECT * FROM sensor_log WHERE value BETWEEN 10.0 AND 20.0;

-- IN
SELECT * FROM sensor_log WHERE status IN ('OK', 'WARN');

-- RANGE (현재 시각 기준 최근 1시간)
SELECT * FROM sensor_log WHERE _arrival_time RANGE 1 HOUR;

-- SEARCH (키워드 인덱스 사용)
SELECT * FROM log_table WHERE message SEARCH 'error';

-- ESEARCH (와일드카드 패턴)
SELECT * FROM log_table WHERE message ESEARCH 'timeout%';

-- REGEXP (정규식)
SELECT * FROM log_table WHERE message REGEXP 'error[0-9]+';
```

---

## GROUP BY / HAVING

```sql
'GROUP BY' expr_list [ 'HAVING' condition_expr ]
```

```sql
SELECT name, AVG(value), MAX(value), COUNT(*)
  FROM sensor_log
 GROUP BY name
HAVING AVG(value) > 50.0;
```

---

## ORDER BY

```sql
'ORDER BY' expr_list [ 'ASC' | 'DESC' ]
```

```sql
SELECT name, value FROM sensor_log ORDER BY value DESC;
SELECT name, value FROM sensor_log ORDER BY name ASC, value DESC;
```

---

## LIMIT

```sql
'LIMIT' [ offset ',' ] row_count
```

```sql
-- 처음 10건만 조회
SELECT * FROM sensor_log LIMIT 10;

-- 11번째부터 10건 조회
SELECT * FROM sensor_log LIMIT 10, 10;
```

---

## DURATION

`_arrival_time` 컬럼을 기준으로 조회 시간 범위를 지정합니다.

```sql
duration_expr ::=
    number time_unit [ ( 'BEFORE' | 'AFTER' ) number time_unit ]
  | 'FROM' datetime_expr 'TO' datetime_expr

time_unit ::= 'YEAR' | 'MONTH' | 'WEEK' | 'DAY' | 'HOUR' | 'MINUTE' | 'SECOND'
```

```sql
-- 최근 1시간 데이터
SELECT * FROM sensor_log DURATION 1 HOUR;

-- 1일 전부터 1시간 범위
SELECT * FROM sensor_log DURATION 1 HOUR BEFORE 1 DAY;

-- 명시적 범위
SELECT * FROM sensor_log
DURATION FROM TO_DATE('2024-01-01','YYYY-MM-DD')
         TO TO_DATE('2024-01-31','YYYY-MM-DD');
```

---

## JOIN

### INNER JOIN (쉼표 방식)

```sql
SELECT t1.id, t2.name
  FROM sensor_log t1, devices t2
 WHERE t1.id = t2.device_id AND t1.value > 50;
```

### ANSI JOIN

```sql
-- INNER JOIN
SELECT t1.id, t2.name
  FROM sensor_log t1
  INNER JOIN devices t2 ON (t1.id = t2.device_id)
 WHERE t1.value > 50;

-- LEFT OUTER JOIN
SELECT t1.id, t2.location
  FROM sensor_log t1
  LEFT OUTER JOIN devices t2 ON (t1.name = t2.name);

-- RIGHT OUTER JOIN
SELECT t1.value, t2.name
  FROM sensor_log t1
  RIGHT OUTER JOIN devices t2 ON (t1.name = t2.name);
```

> FULL OUTER JOIN은 지원하지 않습니다.

---

## SERIES BY

정렬된 결과에서 조건을 연속으로 만족하는 레코드 그룹을 추출합니다.

```sql
'ORDER BY' expr 'SERIES BY' condition_expr
```

```sql
-- C2 > 1을 연속으로 만족하는 레코드 그룹 조회
SELECT c1, c2, SERIESNUM() AS grp
  FROM t1
 ORDER BY c1
 SERIES BY c2 > 1;
```

---

## SUBQUERY

```sql
-- FROM 절 서브쿼리 (인라인 뷰)
SELECT a.name, a.avg_val
  FROM (SELECT name, AVG(value) AS avg_val FROM sensor_log GROUP BY name) a
 WHERE a.avg_val > 50;

-- WHERE 절 서브쿼리
SELECT * FROM sensor_log
 WHERE value > (SELECT AVG(value) FROM sensor_log);

-- IN 절 서브쿼리
SELECT * FROM sensor_log
 WHERE name IN (SELECT name FROM devices WHERE status = 'ACTIVE');
```

> 상관 서브쿼리(외부 쿼리 컬럼을 참조하는 서브쿼리)는 지원하지 않습니다.

---

## CASE 문

```sql
-- simple CASE
CASE expr
    WHEN value1 THEN result1
    [ WHEN value2 THEN result2 ... ]
    [ ELSE default_result ]
END

-- searched CASE
CASE
    WHEN condition1 THEN result1
    [ WHEN condition2 THEN result2 ... ]
    [ ELSE default_result ]
END
```

```sql
SELECT name,
       value,
       CASE
           WHEN value >= 80 THEN 'HIGH'
           WHEN value >= 40 THEN 'MID'
           ELSE 'LOW'
       END AS level
  FROM sensor_log;
```

---

## PIVOT

인라인 뷰의 집계 결과를 행에서 열로 변환합니다.

```sql
'PIVOT' '(' aggregate_func '(' column ')' 'FOR' pivot_column 'IN' '(' value_list ')' ')'
```

```sql
SELECT *
  FROM (SELECT regtime, tagid, dvalue FROM result_d)
 PIVOT (SUM(dvalue) FOR tagid IN ('AXIS_X', 'AXIS_Y', 'AXIS_Z'));
```

---

## UNION ALL

```sql
select_stmt 'UNION ALL' select_stmt
```

두 SELECT 결과를 합칩니다. 컬럼 수와 타입이 호환되어야 합니다. `UNION` (중복 제거), `INTERSECT`, `EXCEPT`는 지원하지 않습니다.

```sql
SELECT id, name FROM table_a
UNION ALL
SELECT id, name FROM table_b;
```

---

## SAVE DATA INTO

SELECT 결과를 CSV 파일로 저장합니다.

```sql
'SAVE DATA INTO' 'file_path'
    [ 'HEADER' ( 'ON' | 'OFF' ) ]
    [ ( 'FIELDS' | 'COLUMNS' )
        [ 'TERMINATED BY' char ]
        [ 'ENCLOSED BY' char ] ]
    [ 'ENCODED BY' encoding ]
    'AS' select_stmt
```

```sql
SAVE DATA INTO '/tmp/sensor_data.csv' HEADER ON AS SELECT * FROM sensor_log;
```

---

## 관련 문서

- WITH / CTE syntax - 비재귀 공통 테이블 표현식
- 힌트 사전 - SELECT 쿼리 성능 최적화 힌트
- SERIES BY - 연속 조건 그룹화 상세 설명
- PIVOT - 행-열 변환 상세 예시
- SEARCH/ESEARCH/REGEXP - 텍스트 검색 상세
- DURATION 상대 시간 표현 - 시간 범위 표현 전체 목록
