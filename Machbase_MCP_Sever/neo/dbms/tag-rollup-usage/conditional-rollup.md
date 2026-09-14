# 조건 ROLLUP

## 원본을 필터한 뒤 집계

조건 ROLLUP은 원본의 품질·상태 조건을 적용한 통계를 유지합니다. 이미 계산한 평균에서
불량 표본만 나중에 제거하는 것과 다릅니다. 조건에 사용한 quality 컬럼 자체가 집계 결과에
보존되는 것도 아닙니다.

## 1. 테이블과 두 ROLLUP 준비

```sql
CREATE TAG TABLE ch6_condition (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP ch6_condition_all
  ON ch6_condition(value) INTERVAL 1 MIN EXTENSION;
CREATE ROLLUP ch6_condition_good
  ON ch6_condition(value) INTERVAL 1 MIN EXTENSION WHERE quality = 1;
INSERT INTO ch6_condition VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_condition VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_condition VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_condition VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
INSERT INTO ch6_condition VALUES
    ('TEMP_01', TO_DATE('2026-01-01 00:00:50', 'YYYY-MM-DD HH24:MI:SS'), 90.0, 0);
EXEC TABLE_FLUSH(ch6_condition);
ALTER ROLLUP ch6_condition_all FORCE;
ALTER ROLLUP ch6_condition_good FORCE;
```

## 2. 원본 조건과 ROLLUP 비교

```sql
SELECT DATE_TRUNC('minute', time) AS bucket, COUNT(value), AVG(value),
       MIN(value), MAX(value), FIRST(time, value), LAST(time, value)
  FROM ch6_condition
 WHERE name = 'TEMP_01' AND quality = 1
 GROUP BY bucket ORDER BY bucket;

SELECT /*+ ROLLUP_TABLE(ch6_condition_good) */
       rollup('min', 1, time) AS bucket, COUNT(value), AVG(value),
       MIN(value), MAX(value), FIRST(time, value), LAST(time, value)
  FROM ch6_condition WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;

SELECT /*+ ROLLUP_TABLE(ch6_condition_all) */
       rollup('min', 1, time) AS bucket, COUNT(value), AVG(value),
       MIN(value), MAX(value), FIRST(time, value), LAST(time, value)
  FROM ch6_condition WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

| 버킷·집합 | COUNT | AVG | MIN | MAX | FIRST | LAST |
|---|---:|---:|---:|---:|---:|---:|
| 00:00 전체 | 3 | 40 | 10 | 90 | 10 | 90 |
| 00:00 quality=1 | 2 | 15 | 10 | 20 | 10 | 20 |
| 00:01 두 집합 공통 | 1 | 30 | 30 | 30 | 30 | 30 |

이 표본은 불량값이 구간의 마지막에 있으므로 LAST도 달라집니다.
FIRST/LAST는 시각·값 쌍이 아니라 선택한 value를 반환합니다.

## 명시적인 후보 선택

이 예제는 전체 통계와 정상 통계의 결과 집합을 고정하기 위해 힌트를 사용합니다.
자동 선택은 조건 없는 후보를 우선하지만 조건 후보만 있을 때는 필터된 통계를 선택할 수
있습니다. “조건 ROLLUP은 항상 무시된다”거나 “EXTENSION에는 항상 힌트가 필수”라는
규칙으로 해석하지 않습니다.

## 문법과 제약

일반 ROLLUP의 필터는 INTERVAL·EXTENSION 뒤의 WHERE에 작성합니다.
비교, BETWEEN, IN, LIKE, 논리 연산과 지원 스칼라 함수를 사용할 수 있지만 서브쿼리,
집계 함수와 태그 이름 PRIMARY KEY 조건은 지원하지 않습니다.
Custom은 SELECT 내부 WHERE를 사용하므로 구문을 섞지 않습니다.

## 상태 확인과 정리

```sql
SELECT DISTINCT ROLLUP_NAME, PREDICATE, ENABLED
  FROM V$ROLLUP WHERE ROOT_TABLE = 'CH6_CONDITION';
DROP ROLLUP ch6_condition_good;
DROP ROLLUP ch6_condition_all;
DROP TABLE ch6_condition;
```

업무 품질 기준이 바뀌면 조건과 재집계 계획도 갱신합니다. 기존 집계가 새로운 조건으로
자동 전환되지는 않습니다. 제어와
재구성 범위를 확인합니다.
