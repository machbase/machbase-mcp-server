# 집계 함수

집계 함수는 여러 행의 값을 하나의 결과로 계산합니다. `GROUP BY` 절과 함께 사용하면 그룹별 집계 결과를 얻을 수 있습니다. `NULL` 값은 집계에서 무시됩니다 (COUNT(*) 제외).

## 빠른 참조

| 함수 | 문법 | 설명 |
|------|------|------|
| COUNT | `COUNT(*) / COUNT(col)` | 전체 행 수 또는 NULL이 아닌 행 수 |
| SUM | `SUM(col)` | 합계 |
| AVG | `AVG(col)` | 평균 |
| MIN | `MIN(col)` | 최솟값 |
| MAX | `MAX(col)` | 최댓값 |
| STDDEV | `STDDEV(col)` | 표본 표준편차 |
| STDDEV_POP | `STDDEV_POP(col)` | 모표준편차 |
| VARIANCE | `VARIANCE(col)` | 표본 분산 |
| VAR_POP | `VAR_POP(col)` | 모분산 |
| FIRST | `FIRST(sort_expr, return_expr)` | 정렬 기준 첫 번째 레코드 값 |
| LAST | `LAST(sort_expr, return_expr)` | 정렬 기준 마지막 레코드 값 |
| SUMSQ | `SUMSQ(col)` | 제곱합 |
| MEDIAN | `MEDIAN(col)` | 중앙값 |
| MODE | `MODE(col)` | 최빈값 |
| AREA | `AREA(y, x)` | 곡선 아래 면적 (사다리꼴 적분) |
| SLOPE | `SLOPE(y, x)` | 선형 회귀 기울기 |
| GROUP_CONCAT | `GROUP_CONCAT(col ...)` | 그룹 내 값을 문자열로 연결 |
| TS_CHANGE_COUNT | `TS_CHANGE_COUNT(col)` | 값 변경 횟수 |
| TOP_K | `TOP_K(col, k)` | 상위 k개 빈도 값 |
| PERCENTILE_CONT | `PERCENTILE_CONT(col, ratio)` | 연속 분위수 |
| PERCENTILE_DISC | `PERCENTILE_DISC(col, ratio)` | 이산 분위수 |
| APPROX_PERCENTILE | `APPROX_PERCENTILE(col, ratio)` | 근사 분위수 |
| CUME_DIST | `CUME_DIST(value, threshold)` | 누적 분포 비율 |

---

## COUNT

주어진 컬럼의 레코드 개수를 구합니다. `COUNT(*)`는 NULL을 포함한 전체 행 수를, `COUNT(col)`은 NULL이 아닌 행 수를 반환합니다.

```sql
COUNT(*)
COUNT(column_name)
```

```sql
Mach> CREATE LOG TABLE count_table (id1 INTEGER, id2 INTEGER);
Mach> INSERT INTO count_table VALUES(1, 1);
Mach> INSERT INTO count_table VALUES(2, 2);
Mach> INSERT INTO count_table VALUES(null, 4);

Mach> SELECT COUNT(*) FROM count_table;
COUNT(*)
---------
3

Mach> SELECT COUNT(id1) FROM count_table;
COUNT(id1)
-----------
2
```

---

## SUM

숫자 컬럼의 합계를 반환합니다.

```sql
SUM(column_name)
```

```sql
Mach> SELECT c1, SUM(c2) FROM sum_table GROUP BY c1;
c1          SUM(c2)
--------------------
1           6
2           6
3           4
```

---

## AVG

숫자형 컬럼의 평균값을 반환합니다.

```sql
AVG(column_name)
```

```sql
Mach> SELECT id1, AVG(id2) FROM avg_table GROUP BY id1;
id1         AVG(id2)
---------------------
1           2
2           2
NULL        4
```

---

## MIN

지정한 숫자 컬럼의 최솟값을 반환합니다.

```sql
MIN(column_name)
```

```sql
Mach> SELECT MIN(c1) FROM min_table;
MIN(c1)
--------
1
```

---

## MAX

지정한 숫자 컬럼의 최댓값을 반환합니다.

```sql
MAX(column_name)
```

```sql
Mach> SELECT MAX(c) FROM max_table;
MAX(c)
-------
30
```

---

## STDDEV / STDDEV_POP

입력 컬럼의 표본 표준편차(STDDEV)와 모표준편차(STDDEV_POP)를 반환합니다.

```sql
STDDEV(column)
STDDEV_POP(column)
```

```sql
Mach> SELECT c2, STDDEV(c1) FROM stddev_table GROUP BY c2;
c2          STDDEV(c1)
-----------------------
1           0.707107
2           0.707107

Mach> SELECT c2, STDDEV_POP(c1) FROM stddev_table GROUP BY c2;
c2          STDDEV_POP(c1)
---------------------------
1           0.5
2           0.5
```

---

## VARIANCE / VAR_POP

표본 분산(VARIANCE)과 모분산(VAR_POP)을 반환합니다.

```sql
VARIANCE(column_name)
VAR_POP(column_name)
```

```sql
Mach> SELECT VARIANCE(c1) FROM var_table;
VARIANCE(c1)
--------------
0.333333

Mach> SELECT VAR_POP(c1) FROM var_table;
VAR_POP(c1)
-------------
0.25
```

---

## FIRST / LAST

각 그룹에서 `sort_expr` 기준으로 정렬했을 때 가장 앞(FIRST) 또는 마지막(LAST) 레코드의 `return_expr` 값을 반환합니다. 시계열 데이터에서 특정 시점의 값을 가져올 때 유용합니다.

```sql
FIRST(sort_expr, return_expr)
LAST(sort_expr, return_expr)
```

```sql
Mach> SELECT group_no, FIRST(id, name) FROM firstlast_table GROUP BY group_no;
group_no    first(id, name)
----------------------------
0           John
1           Grey

Mach> SELECT group_no, LAST(id, name) FROM firstlast_table GROUP BY group_no;
group_no    last(id, name)
---------------------------
0           Ryan
1           Kyle
```

---

## SUMSQ

숫자 값들의 제곱합을 반환합니다.

```sql
SUMSQ(value)
```

```sql
Mach> SELECT c1, SUMSQ(c2) FROM sumsq_table GROUP BY c1;
c1          SUMSQ(c2)
----------------------
1           14
2           41
```

---

## MEDIAN

숫자식의 정확한 중앙값을 반환합니다.

```sql
MEDIAN(value)
```

```sql
SELECT MEDIAN(temp_c) FROM sensor_log;
```

---

## MODE

입력 집합에서 가장 자주 나타나는 숫자 값(최빈값)을 반환합니다. 최빈값이 여러 개면 더 작은 값을 반환합니다.

```sql
MODE(value)
```

```sql
SELECT MODE(alarm_code) FROM event_log;
```

---

## AREA

숫자형 `(x, y)` 점들로 이루어진 곡선 아래 면적을 사다리꼴 적분으로 계산합니다. 유효한 점이 2개 미만이면 NULL을 반환합니다.

```sql
AREA(y, x)
```

```sql
SELECT AREA(power_kw, sample_sec) FROM power_log;
```

---

## SLOPE

숫자형 `(x, y)` 점들에 대한 선형 회귀 직선의 기울기를 계산합니다. `x` 분산이 0이거나 유효 데이터가 부족하면 NULL을 반환합니다.

```sql
SLOPE(y, x)
```

```sql
SELECT SLOPE(temp_c, sample_sec) FROM sensor_log;
```

---

## GROUP_CONCAT

그룹 내 컬럼 값들을 문자열로 이어 붙여 반환합니다.

> **주의**
> Cluster Edition에서는 사용할 수 없습니다.

```sql
GROUP_CONCAT(
    [DISTINCT] column
    [ORDER BY column [ASC | DESC] [, ...]]
    [SEPARATOR str_val]
)
```

```sql
Mach> SELECT GROUP_CONCAT(name) FROM concat_table GROUP BY id2;
G_NAMES
---------
Jack,Jack,Ram
Jill,Zara,John

Mach> SELECT GROUP_CONCAT(DISTINCT name SEPARATOR '.') FROM concat_table GROUP BY id2;
G_NAMES
---------
Jack.Ram
Jill.Zara.John
```

---

## TS_CHANGE_COUNT

시간순으로 입력된 컬럼 값의 변경 횟수를 반환합니다. VARCHAR 타입은 지원하지 않습니다.

> **주의**
> Cluster Edition에서는 사용할 수 없습니다.

```sql
TS_CHANGE_COUNT(column)
```

```sql
Mach> SELECT id, TS_CHANGE_COUNT(ip) FROM ipcount_table GROUP BY id;
id          TS_CHANGE_COUNT(ip)
--------------------------------
1           4
2           2
```

---

## TOP_K

가장 자주 등장한 `k`개의 숫자 값을 `value:count` 형식의 문자열로 반환합니다. 빈도 내림차순, 동일 빈도 시 값 오름차순으로 정렬됩니다.

```sql
TOP_K(value, k)
```

```sql
SELECT TOP_K(alarm_code, 3) FROM event_log;
-- 결과 예: 101:532,205:317,301:90
```

---

## PERCENTILE_CONT / PERCENTILE_DISC

정확한 분위값을 계산하는 집계 함수입니다. `ratio`는 0.0 이상 1.0 이하의 상수여야 합니다.

- `PERCENTILE_CONT`: 인접한 정렬 값 사이를 보간합니다.
- `PERCENTILE_DISC`: 실제 관측값 중 하나를 선택합니다.

```sql
PERCENTILE_CONT(value, ratio)
PERCENTILE_DISC(value, ratio)
```

축약형으로 `P05`, `P10`, `P90`, `P95` 함수도 제공합니다.

```sql
SELECT PERCENTILE_CONT(latency_ms, 0.95) AS p95,
       PERCENTILE_DISC(latency_ms, 0.50) AS p50
FROM api_log;

-- 축약형
SELECT P05(response_ms), P95(response_ms) FROM web_log;
```

---

## APPROX_PERCENTILE

근사 분위수 함수입니다. 데이터가 매우 크고 작은 오차를 허용할 때 유용합니다. `APPROX_MEDIAN`, `APPROX_P05`, `APPROX_P10`, `APPROX_P90`, `APPROX_P95` 축약형도 있습니다.

```sql
APPROX_PERCENTILE(value, ratio)
APPROX_MEDIAN(value)
APPROX_P95(value)
```

```sql
SELECT APPROX_PERCENTILE(latency_ms, 0.95) AS ap95,
       APPROX_MEDIAN(latency_ms)            AS amedian
FROM api_log;
```

---

## CUME_DIST

`value`가 `threshold` 이하인 행의 누적 비율(0.0 ~ 1.0)을 반환합니다. 윈도우 함수가 아닌 집계 함수입니다.

```sql
CUME_DIST(value, threshold)
```

```sql
SELECT CUME_DIST(latency_ms, 100) FROM api_log;
```
