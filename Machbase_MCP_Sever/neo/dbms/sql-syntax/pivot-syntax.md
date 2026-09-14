# PIVOT

`PIVOT`은 행(row) 방향 데이터를 열(column) 방향으로 변환하는 구문입니다. GROUP BY 집계 결과를 컬럼으로 재배열해 가독성 높은 리포트 형태로 표현할 때 사용합니다.

> PIVOT 구문은 Machbase 5.6 버전부터 지원됩니다.

## 문법

```sql
SELECT *
  FROM (inline_view)
 PIVOT (aggregate_function(value_col) FOR category_col IN ('val1', 'val2', ...))
[WHERE ...]
```

- `inline_view`에서 PIVOT 절에 사용되지 않은 컬럼에 대해 GROUP BY를 수행합니다.
- `FOR category_col IN (...)`: 피벗 기준 컬럼과 열로 변환할 값 목록을 지정합니다.
- 결과 컬럼명은 IN 절에 지정한 문자열 값이 됩니다.

## 예시

### 센서별 집계를 열로 변환

```sql
-- 인라인 뷰를 사용한 PIVOT
SELECT * FROM (
    SELECT regtime, tagid, dvalue FROM result_d
     WHERE regtime BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                       AND TO_DATE('2024-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
) PIVOT (
    SUM(dvalue) FOR tagid IN ('FRONT_AXIS_TORQUE', 'REAR_AXIS_TORQUE', 'HOIST_AXIS_TORQUE', 'SLIDE_AXIS_TORQUE')
)
WHERE FRONT_AXIS_TORQUE >= 40 AND REAR_AXIS_TORQUE >= 20;
```

### CASE 문 대비 간결한 표현

```sql
-- PIVOT 없이 CASE 사용
SELECT regtime,
       SUM(CASE WHEN tagid = 'SENSOR_A' THEN dvalue ELSE 0 END) AS sensor_a,
       SUM(CASE WHEN tagid = 'SENSOR_B' THEN dvalue ELSE 0 END) AS sensor_b
  FROM result_d
 GROUP BY regtime;

-- PIVOT으로 간결하게 표현
SELECT * FROM (
    SELECT regtime, tagid, dvalue FROM result_d
) PIVOT (SUM(dvalue) FOR tagid IN ('SENSOR_A', 'SENSOR_B'));
```

### TAG 테이블과 PIVOT 조합

```sql
SELECT * FROM (
    SELECT name, time, value
      FROM sensor_tag
     WHERE time BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                    AND TO_DATE('2024-01-01 01:00:00', 'YYYY-MM-DD HH24:MI:SS')
) PIVOT (
    AVG(value) FOR name IN ('sensor-01', 'sensor-02', 'sensor-03')
);
```

### INTERPOLATION 힌트와 조합

```sql
SELECT * FROM (
    SELECT /*+ INTERPOLATION(time) */ name, time, value
      FROM sensor_tag
     WHERE time BETWEEN NOW - 1h AND NOW
) PIVOT (AVG(value) FOR name IN ('TEMP-01', 'TEMP-02', 'PRESS-01'));
```

## 제약사항

- PIVOT은 반드시 인라인 뷰(서브쿼리)와 함께 사용해야 합니다.
- 인라인 뷰에서 PIVOT 집계 컬럼(`value_col`)과 기준 컬럼(`category_col`) 외의 모든 컬럼이 자동 GROUP BY 대상이 됩니다.
- IN 절에 나열하는 값은 컴파일 시점에 확정된 리터럴이어야 합니다 (동적 컬럼 목록 불가).

## 관련 문서

- SELECT hint syntax — INTERPOLATION 힌트와 PIVOT 조합
