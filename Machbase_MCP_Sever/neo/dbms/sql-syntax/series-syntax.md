# SERIES BY

`SERIES BY` 절은 정렬된 결과 집합에서 특정 조건을 만족하는 연속적인 행의 구간(series)을 추출합니다. 연속된 구간에서 시작/종료 시각과 패턴을 분석할 때 사용합니다.

## 문법

```sql
SELECT ...
  FROM table_name
 [WHERE ...]
 ORDER BY col [ASC | DESC]
 SERIES BY condition_expr
```

- `ORDER BY` 절이 없으면 `_ARRIVAL_TIME` 컬럼 기준으로 정렬됩니다.
- `GROUP BY`를 사용하거나 `_ARRIVAL_TIME` 컬럼이 없는 VOLATILE / LOOKUP 테이블에서는 반드시 `ORDER BY`를 명시해야 합니다.
- `SERIES BY` 조건을 연속으로 만족하는 같은 구간의 행들은 동일한 `SERIESNUM()` 반환값을 가집니다.

## 예시

### 기본 사용

```sql
CREATE LOG TABLE t1 (c1 INTEGER, c2 INTEGER);
INSERT INTO t1 VALUES (0, 1);
INSERT INTO t1 VALUES (1, 2);
INSERT INTO t1 VALUES (2, 3);
INSERT INTO t1 VALUES (3, 2);
INSERT INTO t1 VALUES (4, 1);
INSERT INTO t1 VALUES (5, 2);
INSERT INTO t1 VALUES (6, 3);
INSERT INTO t1 VALUES (7, 1);

SELECT c1, c2
  FROM t1
 ORDER BY c1
 SERIES BY c2 > 1;
```

결과:

```
C1          C2
---------------------------
1           2
2           3
3           2
5           2
6           3
```

### SERIESNUM()으로 구간 번호 확인

```sql
SELECT c1, c2, SERIESNUM() AS grp
  FROM t1
 ORDER BY c1
 SERIES BY c2 > 1;
```

결과:

```
C1          C2          GRP
-----------------------------------
1           2           1
2           3           1
3           2           1
5           2           2
6           3           2
```

### TAG 테이블에서 연속 구간 분석

내부 쿼리에서 연속 구간별 번호를 생성하고, 외부 쿼리에서 구간 번호를 기준으로 집계합니다.

```sql
-- 100을 초과하는 연속 구간별 시작/끝 시각과 최댓값 조회
SELECT MIN(time) AS start_time,
       MAX(time) AS end_time,
       MAX(value) AS peak_value,
       series_id
  FROM (
      SELECT time, value, SERIESNUM() AS series_id
        FROM tag
       WHERE name = 'PRESSURE-01'
         AND time >= TO_DATE('2024-01-01', 'YYYY-MM-DD')
       ORDER BY time
       SERIES BY value > 100.0
  )
 GROUP BY series_id
 ORDER BY series_id;
```

## SERIES BY와 INTERPOLATION 비교

| 항목 | SERIES BY | INTERPOLATION 힌트 |
|------|-----------|--------------------|
| 용도 | 조건 만족 연속 구간 추출 | 누락 시간 구간 보간 |
| 대상 | 모든 테이블 | TAG 테이블 |
| 결과 | 조건 만족 행만 반환 | 보간된 행을 자동 추가 |

## 관련 문서

- SELECT hint syntax — INTERPOLATION 힌트와의 조합
- window function / OVER syntax — 윈도우 기반 분석과의 차이
