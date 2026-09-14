# JSON SUMMARIZED ROLLUP

## JSON 경로와 문서 전체 집계

JSON 경로 ROLLUP은 지정 경로에서 숫자 값을 집계합니다. 문서 전체 ROLLUP은
JSON SUMMARIZED 컬럼의 숫자 경로별 통계를 유지합니다. 경로가 없는 값, JSON null,
SQL NULL과 배열을 같은 표본으로 해석하지 않습니다.

## 준비

```sql
CREATE TAG TABLE ch6_json (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value JSON SUMMARIZED
);
CREATE ROLLUP ch6_json_metric ON ch6_json(value.metric) INTERVAL 1 MIN;
CREATE ROLLUP ch6_json_whole ON ch6_json(value) INTERVAL 1 MIN;
INSERT INTO ch6_json VALUES ('S1', TO_DATE('2026-01-01 00:00:00'),
    '{"metric":10,"nested":{"x":2},"status":"OK","items":[1,2]}');
INSERT INTO ch6_json VALUES ('S1', TO_DATE('2026-01-01 00:00:10'),
    '{"metric":20,"nested":{"x":4},"status":"WARN","items":[3,4]}');
INSERT INTO ch6_json VALUES ('S1', TO_DATE('2026-01-01 00:00:20'),
    '{"metric":null,"status":false}');
INSERT INTO ch6_json VALUES ('S1', TO_DATE('2026-01-01 00:00:30'), NULL);
EXEC TABLE_FLUSH(ch6_json);
ALTER ROLLUP ch6_json_metric FORCE;
ALTER ROLLUP ch6_json_whole FORCE;
```

## 경로 집계 비교

```sql
SELECT DATE_TRUNC('minute', time) AS bucket,
       COUNT(JSON_EXTRACT_DOUBLE(value, '$.metric')),
       AVG(JSON_EXTRACT_DOUBLE(value, '$.metric'))
  FROM ch6_json WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;

SELECT /*+ ROLLUP_TABLE(ch6_json_metric) */
       rollup('min', 1, time) AS bucket,
       COUNT(value.metric), AVG(value.metric)
  FROM ch6_json WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;

SELECT /*+ ROLLUP_TABLE(ch6_json_metric) */
       rollup('min', 1, time) AS bucket, AVG(value->'$.metric')
  FROM ch6_json WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;
```

metric의 유효 숫자 표본은 2개이고 평균은 15입니다. dot과 arrow는 같은 경로를 표현합니다.
특정 배열 요소를 경로로 지정하는 것과 문서 전체 집계가 배열을 자동 전개하는 것은 다릅니다.
경로 선언의 예로 `value.items[0]."metric-id"`를 사용할 수 있지만 해당 JSON 구조와 숫자
표본이 실제로 있는지 먼저 확인해야 합니다.

## 문서 전체 집계와 COUNT

```sql
SELECT COUNT(*) AS raw_rows, COUNT(value) AS raw_documents FROM ch6_json;

SELECT /*+ ROLLUP_TABLE(ch6_json_whole) */
       rollup('min', 1, time) AS bucket,
       COUNT(value), AVG(value), MIN(value), MAX(value), SUM(value)
  FROM ch6_json WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;
```

원본 COUNT(*)는 4이고 COUNT(value)는 3입니다. 문서 전체 ROLLUP의 COUNT(value)는 저장된
문서 집계 건수를 합산합니다. 현재 이 집계의 건수는 원본 COUNT(*)로 만들어지므로 위처럼
숫자 경로를 가진 문서와 SQL NULL이 섞인 버킷에서는 4입니다. 일반 원본 COUNT(value)의
NULL 제외 규칙을 그대로 적용하면 안 됩니다.

AVG 결과의 metric은 15, nested.x는 3이며 각 경로의 유효 숫자 표본으로 계산합니다.
문자열·불리언·JSON null·배열은 숫자 집계에서 제외되고 비숫자 경로는 null 또는 생략으로
나타날 수 있습니다. JSON 직렬화의 키 순서를 고정된 문자열 결과로 비교하지 않습니다.
숫자 경로가 전혀 없는 문서나 SQL NULL만 있는 구간은 별도로 표본을 만들어 확인합니다.

JSON 경로 집계와 문서 전체 집계는 후보 모드가 다릅니다. 서로 다른 모드의 ROLLUP을
힌트로 강제해서 같은 결과가 된다고 가정하지 마십시오. 유효하지 않은 JSON은 입력 오류입니다.

## 정리

```sql
DROP ROLLUP ch6_json_whole;
DROP ROLLUP ch6_json_metric;
DROP TABLE ch6_json;
```
