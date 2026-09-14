# Custom ROLLUP

<span class="badge-since">Standard Edition 전용</span>

## Custom과 일반 ROLLUP

Custom ROLLUP은 SELECT의 증분 집계 결과를 미리 만든 대상 TAG에 누적합니다.
일반 ROLLUP의 내부 통계를 `rollup()`으로 읽는 방식과 달리, 대상 TAG를 직접 조회하면서
부분 집계를 다시 합쳐야 합니다. Cluster Edition에서는 생성할 수 없습니다.

```text
CREATE ROLLUP [IF NOT EXISTS] name
  INTO (destination_tag)
  AS (SELECT ... FROM source_tag [WHERE ...] GROUP BY ...)
  INTERVAL n (SEC|MIN|HOUR)
  [WAKEUP INTERVAL m (SEC|MIN|HOUR)];
```

소스는 시간축 TAG 하나이며 JOIN·FROM 서브쿼리는 사용할 수 없습니다. 대상은 미리 만든
TAG이고 SELECT의 컬럼 순서·타입과 호환되어야 합니다. SELECT 내부 WHERE는 사용할 수
있지만 BASETIME 직접 조건은 허용되지 않습니다. 일반 ROLLUP처럼 INTERVAL 뒤에 외부
WHERE를 붙이지 않습니다.

생성 간격과 SELECT가 계산하는 시간 버킷을 일치시키십시오. 작업이 새 입력만 처리하므로
같은 버킷에 여러 결과 행이 있을 수 있습니다. 행 수를 버킷 수로 해석하지 않습니다.

## 1. 합계·유효 건수 실습

```sql
CREATE TAG TABLE ch6_custom_src (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE
);
CREATE TAG TABLE ch6_custom_dst (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME,
    sum_value DOUBLE, valid_count LONG, total_count LONG
);
CREATE ROLLUP ch6_custom_ru INTO (ch6_custom_dst)
AS (
    SELECT name, DATE_TRUNC('minute', time) AS time,
           SUM(value), COUNT(value), COUNT(*)
      FROM ch6_custom_src
     GROUP BY name, time
) INTERVAL 1 MIN;
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:05', 'YYYY-MM-DD HH24:MI:SS'), 10);
EXEC TABLE_FLUSH(ch6_custom_src);
ALTER ROLLUP ch6_custom_ru FORCE;
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:10', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:15', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:20', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:25', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:35', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:40', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:45', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:55', 'YYYY-MM-DD HH24:MI:SS'), NULL);
EXEC TABLE_FLUSH(ch6_custom_src);
ALTER ROLLUP ch6_custom_ru FORCE;

SELECT name, DATE_TRUNC('minute', time) AS bucket,
       SUM(value), COUNT(value), COUNT(*), AVG(value)
  FROM ch6_custom_src
 GROUP BY name, bucket ORDER BY name, bucket;

SELECT name, time, SUM(sum_value) AS sum_value,
       SUM(valid_count) AS valid_count, SUM(total_count) AS total_count,
       CASE WHEN SUM(valid_count) = 0 THEN NULL
            ELSE SUM(sum_value) / SUM(valid_count) END AS avg_value
  FROM ch6_custom_dst
 GROUP BY name, time ORDER BY name, time;
```

한 버킷의 합계는 180, 유효 값은 10개, 전체 행은 11개, 평균은 18입니다.
부분 평균 10과 20을 단순 평균한 15와 다릅니다. NULL을 평균의 분모에 넣지 않도록
COUNT(value)를 사용하고, NULL 포함 행 수는 COUNT(*)로 따로 보관합니다.
모든 값이 NULL인 버킷까지 처리하려면 유효 건수 0에서 나누지 않는 결과 정책도 정합니다.

### 표본 비율과 시간 가동률

조건을 만족한 표본 수를 전체 표본 수로 나눈 값은 표본 비율입니다. 시간 가동률로 해석하려면
관측 간격·결측 처리와 상태 지속 시간을 반영해야 합니다. 비율도 부분 비율끼리 평균하지
말고 분자와 분모를 각각 합산합니다.

## 2. OHLCV와 1분→10분 Custom 계층

별도 실습입니다. FIRST/LAST 재집계를 위해 원본의 첫·마지막 관측 시각도 저장합니다.

```sql
CREATE TAG TABLE ch6_ticks (
    code VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME,
    price DOUBLE, volume DOUBLE
);
CREATE TAG TABLE ch6_candle_min (
    code VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME,
    open_price DOUBLE, high_price DOUBLE, low_price DOUBLE, close_price DOUBLE,
    volume DOUBLE, cnt LONG, firsttime DATETIME, lasttime DATETIME
);
CREATE TAG TABLE ch6_candle_10m (
    code VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME,
    open_price DOUBLE, high_price DOUBLE, low_price DOUBLE, close_price DOUBLE,
    volume DOUBLE, cnt LONG, firsttime DATETIME, lasttime DATETIME
);
CREATE ROLLUP ch6_candle_ru_min INTO (ch6_candle_min)
AS (
    SELECT code, DATE_TRUNC('minute', time) AS time,
           FIRST(time, price), MAX(price), MIN(price), LAST(time, price),
           SUM(volume), COUNT(*), MIN(time), MAX(time)
      FROM ch6_ticks
     GROUP BY code, time
) INTERVAL 1 MIN;

CREATE ROLLUP ch6_candle_ru_10m INTO (ch6_candle_10m)
AS (
    SELECT code, DATE_BIN('min', 10, time, TO_DATE('2000-01-01 00:00:00')) AS time,
           FIRST(firsttime, open_price), MAX(high_price),
           MIN(low_price), LAST(lasttime, close_price),
           SUM(volume), SUM(cnt), MIN(firsttime), MAX(lasttime)
      FROM ch6_candle_min
     GROUP BY code, time
) INTERVAL 10 MIN;

INSERT INTO ch6_ticks VALUES ('AAPL', TO_DATE('2026-01-01 09:00:00'), 100, 2);
INSERT INTO ch6_ticks VALUES ('AAPL', TO_DATE('2026-01-01 09:00:30'), 105, 3);
INSERT INTO ch6_ticks VALUES ('AAPL', TO_DATE('2026-01-01 09:01:00'), 103, 1);
INSERT INTO ch6_ticks VALUES ('AAPL', TO_DATE('2026-01-01 09:01:30'), 99, 4);
EXEC TABLE_FLUSH(ch6_ticks);
ALTER ROLLUP ch6_candle_ru_min FORCE;
EXEC TABLE_FLUSH(ch6_candle_min);
ALTER ROLLUP ch6_candle_ru_10m FORCE;

SELECT code, time,
       FIRST(firsttime, open_price), MAX(high_price),
       MIN(low_price), LAST(lasttime, close_price), SUM(volume), SUM(cnt)
  FROM ch6_candle_10m
 GROUP BY code, time ORDER BY code, time;
```

09:00의 10분 버킷은 Open=100, High=105, Low=99, Close=99, volume=10, cnt=4입니다.
가격·거래량이 NULL인 경우에는 어떤 행의 시각과 값을 사용할지 별도 규칙과 테스트가 필요합니다.
동일 시각의 여러 거래도 업무상 순서가 있다면 추가 식별 기준을 설계합니다.

이 10분 Custom은 생성·조회 예제입니다. 현행 REBUILD의 Custom 시간 범위 처리에
지원되는 간격과 같다고 가정하지 마십시오. REBUILD 제한을 확인합니다.

## 상태와 정리

생성 후 자동 시작되므로 START를 즉시 반복하지 않습니다. STOP/START와 FORCE는 작업
상태에 맞춰 호출합니다. 작업이 존재하는 대상 TAG의 DROP은 차단됩니다.

```sql
SELECT DISTINCT ROLLUP_NAME, ROLLUP_TABLE, ROOT_TABLE, EXT_TYPE,
       INTERVAL_TIME, WAKEUP_INTERVAL
  FROM V$ROLLUP WHERE ROLLUP_NAME = 'CH6_CUSTOM_RU';

DROP ROLLUP ch6_candle_ru_10m;
DROP ROLLUP ch6_candle_ru_min;
DROP TABLE ch6_candle_10m;
DROP TABLE ch6_candle_min;
DROP TABLE ch6_ticks;
DROP ROLLUP ch6_custom_ru;
DROP TABLE ch6_custom_dst;
DROP TABLE ch6_custom_src;
```

EXT_TYPE=2는 Custom이며 PREDICATE에는 SELECT 본문이 기록됩니다.
정리할 때는 실행한 실습의 객체만 대상으로 합니다. 원본 보정과 상위 재집계의 재시도·완료
확인은 제어와 상태 및 REBUILD 절차를 따릅니다.
