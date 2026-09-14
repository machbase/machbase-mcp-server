# ROLLUP 성능 튜닝

## 같은 결과를 만든 뒤 비용 비교

ROLLUP의 효과는 읽는 원시 행을 줄이는 데 있습니다. 먼저 태그, 시간 구간, NULL 처리와
집계 기준이 같은 결과인지 확인한 뒤 실행 시간·CPU·I/O·메모리를 비교합니다.
작은 예제의 실행 시간이 운영 성능을 보장하지는 않습니다.

## 비교 실습

```sql
CREATE TAG TABLE ch6_perf (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP ch6_perf_ru ON ch6_perf(value) INTERVAL 1 MIN;
INSERT INTO ch6_perf VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_perf VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_perf VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_perf VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
EXEC TABLE_FLUSH(ch6_perf);
ALTER ROLLUP ch6_perf_ru FORCE;

SELECT DATE_TRUNC('minute', time) AS bucket,
       SUM(value), COUNT(value), AVG(value), MIN(value), MAX(value)
  FROM ch6_perf
 WHERE name = 'TEMP_01'
   AND time >= TO_DATE('2026-01-01 00:00:00')
   AND time < TO_DATE('2026-01-01 00:02:00')
 GROUP BY bucket ORDER BY bucket;

SELECT rollup('min', 1, time) AS bucket,
       SUM(value), COUNT(value), AVG(value), MIN(value), MAX(value)
  FROM ch6_perf
 WHERE name = 'TEMP_01'
   AND time >= TO_DATE('2026-01-01 00:00:00')
   AND time < TO_DATE('2026-01-01 00:02:00')
 GROUP BY bucket ORDER BY bucket;

EXPLAIN SELECT rollup('min', 1, time) AS bucket, AVG(value)
  FROM ch6_perf WHERE name = 'TEMP_01'
 GROUP BY bucket;
```

두 결과는 00:00의 합계 30·건수 2·평균 15·최솟값 10·최댓값 20과,
00:01의 합계 30·건수 1·평균 30·최솟값 30·최댓값 30입니다.
원본 DATE_TRUNC 쿼리의 실행 계획도 같은 방식으로 확인합니다.

## 운영 부하 측정

| 항목 | 함께 기록할 조건 |
|---|---|
| 입력 처리량 | 태그 수·입력률·행 폭·동시 입력자 |
| 조회 지연 | 태그 범위·버킷·동시 쿼리·캐시가 차갑거나 준비된 상태 |
| 집계 지연 | 계층별 gap·작업 상태·처리 시간 |
| 저장량 | 원본·집계·인덱스·압축·복제본 |
| 변경 영향 | WAKEUP 주기와 계층 변경 전후의 입력·조회 비용 |

WAKEUP을 짧게 하면 같은 버킷에 더 자주 부분 집계가 생길 수 있습니다. 집계 버킷을
작게 하면 저장·재집계 양이 늘어납니다. 두 간격을 같은 튜닝 항목으로 취급하지 않습니다.
단일 실행뿐 아니라 입력과 조회가 동시에 진행되는 상황을 측정합니다.

## 계층 크기의 의미

태그 하나가 30일 동안 모든 구간에 데이터를 가진다는 가정의 논리 버킷 수입니다.

| 조회 구간 | 버킷 수 |
|---|---:|
| 1초 | 2,592,000 |
| 1분 | 43,200 |
| 1시간 | 720 |
| 1일 | 30 |

이는 물리 저장 행 수가 아닙니다. 여러 부분 집계, 빈 구간, NULL과 조건 필터를 포함한
실제 저장량은 표본 적재로 측정합니다. 가장 거친 후보가 항상 올바른 결과를 만드는 것도
아니므로 필요한 해상도·origin·후보 선택 제약을 함께 확인합니다.

일 단위 결과에는 적용 가능한 HOUR/MIN/SEC 집계를 재집계합니다.
24 HOUR ROLLUP을 `rollup('day', 1, ...)`의 대체 저장 계층으로 권장하지 않습니다.
조회 후보 규칙과 실제 EXPLAIN을 기준으로 합니다.

## 지연·불일치의 분리

gap=0은 처리 위치를 따라잡았다는 뜻이지 원본 보정이 이미 반영됐다는 뜻은 아닙니다.
성능 비교 전에는 집계 진행과 과거 정정 상태를 구분하고, 정의·필터가 같은지 확인합니다.
적용 가능한 ROLLUP이 없는 `rollup()` 쿼리를 원본 성능 측정용으로 사용하지 않습니다.

## 정리

```sql
DROP ROLLUP ch6_perf_ru;
DROP TABLE ch6_perf;
```

제어와 상태, 계층 설계,
문제 해결에서 다음 조정을 선택합니다.
