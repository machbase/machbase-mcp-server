# window function / OVER

Machbase의 `LAG()`와 `LEAD()`는 조회 결과의 각 행에서 이전 또는 다음 행의 값을 참조합니다.
예를 들어 센서별 측정값을 시간순으로 비교해 직전 측정값과의 차이를 구할 수 있습니다.
`GROUP BY` 집계와 달리 여러 행을 하나로 줄이지 않습니다.

## 문법

```sql
LAG(value_expression, offset) OVER (
    [PARTITION BY partition_expression]
    [ORDER BY order_expression]
)

LEAD(value_expression, offset) OVER (
    [PARTITION BY partition_expression]
    [ORDER BY order_expression]
)
```

| 요소 | 설명 |
|------|------|
| `value_expression` | 이전 또는 다음 행에서 가져올 값 |
| `offset` | 현재 행에서 떨어진 행 수. 1 이상의 정수를 지정 |
| `PARTITION BY` | 비교할 행을 그룹으로 나누는 단일 식. 생략하면 전체 결과를 한 그룹으로 처리 |
| `ORDER BY` | 그룹 안에서 비교 순서를 정하는 단일 식 |

`OVER`는 필수이며, 괄호 안의 `PARTITION BY`와 `ORDER BY`는 생략할 수 있습니다.
시간순 비교에는 `ORDER BY time`처럼 기준을 명시하십시오. 정렬 기준 값이 같은 행 사이의
순서는 이 식만으로 구분할 수 없습니다. 최종 결과의 출력 순서가 필요하면 SELECT 문 끝에도
`ORDER BY`를 지정합니다.

## 지원 윈도우 함수

| 함수 | 설명 |
|------|------|
| `LAG(value, n)` | 같은 그룹에서 현재 행보다 n행 앞의 값 |
| `LEAD(value, n)` | 같은 그룹에서 현재 행보다 n행 뒤의 값 |

참조할 행이 없으면 NULL을 반환합니다. `offset`은 시간 간격이 아니라 행 수입니다.
측정 간격이 불규칙하면 직전 행이 반드시 1초 전이나 1분 전 측정값인 것은 아닙니다.

### 다른 DBMS의 윈도우 문법과 구분

다음 문법을 Machbase의 `LAG`/`LEAD` 문법과 혼동하지 마십시오.

- `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `FIRST_VALUE()`, `LAST_VALUE()`는 지원하지 않습니다.
- `SUM(...) OVER (...)`, `AVG(...) OVER (...)` 등의 집계 윈도우 함수는 지원하지 않습니다.
- `ROWS`/`RANGE` 프레임과 `UNBOUNDED PRECEDING`, `CURRENT ROW` 같은 프레임 경계를
  지정할 수 없습니다.
- `OVER` 안의 `PARTITION BY`와 `ORDER BY`에는 각각 하나의 식만 지정할 수 있습니다.
  `ORDER BY` 뒤에 `ASC`/`DESC`를 지정하는 문법도 지원하지 않습니다.

결과 행에 번호를 붙이는 `ROWNUM()`과 연속 구간 번호를 구하는 `SERIESNUM()`은
윈도우/시리즈 함수에서 설명합니다.

## 예시

### LAG / LEAD: 이전/이후 값 비교

다음 예제는 `name`, `time`, `value` 컬럼이 있는 `sensor_tag` 테이블을 사용합니다.

```sql
SELECT name, time, value,
       LAG(value, 1) OVER (PARTITION BY name ORDER BY time) AS prev_value,
       LEAD(value, 1) OVER (PARTITION BY name ORDER BY time) AS next_value,
       value - LAG(value, 1) OVER (PARTITION BY name ORDER BY time) AS delta
  FROM sensor_tag
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2024-01-01', 'YYYY-MM-DD')
 ORDER BY name, time;
```

`prev_value`와 `next_value`는 조회 범위 안의 이전·다음 값을 나타냅니다. 첫 행의
`prev_value`와 마지막 행의 `next_value`는 NULL입니다. `WHERE`로 제외한 과거 행은
비교 대상에 포함되지 않으므로 첫 행의 차이까지 필요하면 조회 범위를 앞쪽으로 넓힙니다.

### 집계 결과의 이전 값 비교

태그별 시간 구간을 먼저 집계한 뒤 집계값 사이의 변화를 비교할 수 있습니다. 다음 예제는
시간 단위 ROLLUP을 조회할 수 있는 `sensor_tag` 테이블을 전제로 합니다.

```sql
SELECT name, bucket, avg_val,
       LAG(avg_val, 1) OVER (PARTITION BY name ORDER BY bucket) AS prev_avg
  FROM (
      SELECT name,
             rollup('hour', 1, time) AS bucket,
             AVG(value)              AS avg_val
        FROM sensor_tag
       WHERE time BETWEEN TO_DATE('2024-01-01', 'YYYY-MM-DD')
                      AND TO_DATE('2024-07-01', 'YYYY-MM-DD')
       GROUP BY name, bucket
  ) t
 ORDER BY name, bucket;
```

이 쿼리는 구간별 평균과 직전 구간의 평균을 비교합니다. 이동 평균이나 누적 합계를
계산하는 쿼리는 아닙니다. 데이터가 없는 구간은 자동으로 채워지지 않습니다.

## 성능 주의사항

윈도우 계산에는 그룹 구분, 정렬과 이전·다음 행의 값을 유지하는 작업이 필요합니다.
시간 범위와 태그 조건으로 대상 행을 줄이고, 장기 추세 비교는 집계 결과에 적용하면
처리해야 할 행 수를 줄일 수 있습니다.

`LAG`/`LEAD`는 SELECT 결과 식에서 사용합니다. `WHERE`, `HAVING`, `GROUP BY`,
`ORDER BY`, JOIN의 `ON` 조건에 직접 호출하지 마십시오. 계산한 값으로 필터링하려면
인라인 뷰의 결과 컬럼을 바깥 SELECT에서 참조합니다.

## 관련 문서

- 윈도우/시리즈 함수 — `ROWNUM()`과 `SERIESNUM()`
- PIVOT syntax — 행을 열로 변환
- SERIES BY syntax — 연속 구간 추출
