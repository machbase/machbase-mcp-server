# ROLLUP 개요와 사용 기준

ROLLUP은 원시 행에서 같은 집계를 반복하는 비용을 줄입니다. 원본 보관 정책이나 임의
쿼리 결과 캐시가 아니며, 집계에 저장하지 않은 원본 정보까지 복원할 수는 없습니다.

## 사용 기준

| 요구 | 검토할 방식 |
|---|---|
| 한 숫자 컬럼의 반복 구간 통계 | 일반 ROLLUP |
| 특정 품질 조건을 통과한 표본만 집계 | 조건 ROLLUP |
| 구간의 첫 값·마지막 값 필요 | EXTENSION ROLLUP |
| 여러 집계식을 별도 TAG에 저장 | Custom ROLLUP(Standard Edition 전용) |
| JSON 경로나 문서의 숫자 값 집계 | JSON 경로 또는 문서 전체 ROLLUP |
| 거리축 TAG | 일반 숫자 구간 집계; ROLLUP은 미지원 |

일반 숫자 컬럼을 명시해 만드는 ROLLUP에는 SUMMARIZED가 필수가 아닙니다.
WITH ROLLUP 자동 생성과 JSON 문서 전체 집계에는 별도의 SUMMARIZED 조건이 있습니다.
자세한 차이는 생성 문법을 참고합니다.

## 기본 실습

### 1. 생성과 입력

```sql
CREATE TAG TABLE ch6_basic (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP ch6_basic_ru ON ch6_basic(value) INTERVAL 1 MIN;
INSERT INTO ch6_basic VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_basic VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_basic VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_basic VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
```

### 2. 집계 완료 범위 확인

```sql
EXEC TABLE_FLUSH(ch6_basic);
ALTER ROLLUP ch6_basic_ru FORCE;
SHOW ROLLUPGAP;
```

SHOW ROLLUPGAP은 machsql 명령입니다. SDK에서는 V$ROLLUP 등 지원되는 SQL 조회를
사용합니다. TABLE_FLUSH는 저장 버퍼 처리이고 FORCE는 해당 ROLLUP의 처리 범위를
따라잡는 작업입니다. 지속 입력 중 미래에 들어올 행까지 완료시킨다는 뜻은 아닙니다.

### 3. 원본과 비교

```sql
SELECT DATE_TRUNC('minute', time) AS bucket,
       COUNT(value), MIN(value), MAX(value), AVG(value)
  FROM ch6_basic
 WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;

SELECT rollup('min', 1, time) AS bucket,
       COUNT(value), MIN(value), MAX(value), AVG(value)
  FROM ch6_basic
 WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

| 버킷 | COUNT(value) | MIN | MAX | AVG |
|---|---:|---:|---:|---:|
| 2026-01-01 00:00:00 | 2 | 10 | 20 | 15 |
| 2026-01-01 00:01:00 | 1 | 30 | 30 | 30 |

두 쿼리는 같은 결과를 반환해야 합니다. DATE_TRUNC의 원본 집계가 단지 ROLLUP이 존재한다는
이유로 자동 전환되는 것으로 설명하지 않습니다. ROLLUP 조회에서는 `rollup()`을 명시합니다.

### 4. 정리

```sql
DROP ROLLUP ch6_basic_ru;
DROP TABLE ch6_basic;
```

## 도입 전 확인

대표 태그 수, 입력량, 조회 빈도와 허용 집계 지연을 정합니다. 필요한 가장 세밀한 구간과
원본 보존 기간을 먼저 결정하고 계층 설계로 이어갑니다.
긴 기간의 성능은 운영과 유사한 데이터로 측정하며 이 작은 표본의 시간으로 추정하지 않습니다.
