# 확장 ROLLUP과 FIRST/LAST

## EXTENSION과 원본 FIRST/LAST의 차이

EXTENSION은 ROLLUP에 첫·마지막 값과 관련 시각 정보를 추가합니다.
일반 원본 GROUP BY에서 FIRST/LAST를 사용하는 것과, 저장된 ROLLUP에서 FIRST/LAST를
조회하는 것은 다릅니다. 후자에는 적용 가능한 확장 ROLLUP이 필요합니다.

EXTENSION이 추가하는 것은 첫·마지막 값과 시각뿐입니다. MIN, MAX, SUM, COUNT와
제곱합인 SUMSQ는 일반 ROLLUP에도 함께 저장됩니다. SUMSQ로 분산과 표준편차를
계산하는 방법은 SUMSQ와 분산·표준편차를
참고합니다.

## 준비와 입력

```sql
CREATE TAG TABLE ch6_ext (
    code VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    price DOUBLE
);
CREATE ROLLUP ch6_ext_first
  ON ch6_ext(price) INTERVAL 1 MIN EXTENSION;
CREATE ROLLUP ch6_ext_plain
  ON ch6_ext(price) INTERVAL 1 MIN;
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100);
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:10', 'YYYY-MM-DD HH24:MI:SS'), 105);
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:20', 'YYYY-MM-DD HH24:MI:SS'), 99);
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:30', 'YYYY-MM-DD HH24:MI:SS'), 103);
EXEC TABLE_FLUSH(ch6_ext);
ALTER ROLLUP ch6_ext_first FORCE;
ALTER ROLLUP ch6_ext_plain FORCE;
```

## 원본과 OHLC 비교

```sql
SELECT DATE_TRUNC('minute', time) AS bucket,
       FIRST(time, price) AS open_price, MAX(price) AS high_price,
       MIN(price) AS low_price, LAST(time, price) AS close_price
  FROM ch6_ext WHERE code = 'AAPL'
 GROUP BY bucket ORDER BY bucket;

SELECT /*+ ROLLUP_TABLE(ch6_ext_first) */
       rollup('min', 1, time) AS bucket,
       FIRST(time, price) AS open_price, MAX(price) AS high_price,
       MIN(price) AS low_price, LAST(time, price) AS close_price
  FROM ch6_ext WHERE code = 'AAPL'
 GROUP BY bucket ORDER BY bucket;
```

두 쿼리는 09:00 버킷에 Open=100, High=105, Low=99, Close=103을 반환합니다.
ROLLUP의 FIRST/LAST 첫 인자는 BASETIME, 두 번째는 집계 대상 컬럼을 사용합니다.
같은 시각의 여러 값은 추가적인 업무 순서가 필요한 경우를 별도로 설계합니다.

## 일반 후보와 확장 후보가 함께 있을 때

일반 ROLLUP이 확장 ROLLUP보다 무조건 우선하는 것은 아닙니다. 같은 조건·간격의 후보는
등록 순서의 영향을 받습니다. 이 예제는 확장을 먼저 만들었지만, 결과가 특정 후보에
의존해야 한다면 위처럼 명시합니다. 확장만 적용 가능한 환경에서는 힌트 없이 선택될 수도 있습니다.

다음은 일반 ROLLUP을 강제하므로 의도적으로 실패하는 조회입니다.

```sql
SELECT /*+ ROLLUP_TABLE(ch6_ext_plain) */
       rollup('min', 1, time) AS bucket, FIRST(time, price)
  FROM ch6_ext WHERE code = 'AAPL'
 GROUP BY bucket;
```

자동 계층에 확장이 필요하면 별도 테이블의 CREATE에서
`WITH ROLLUP (SEC) EXTENSION`을 사용합니다. FROM으로 계층을 만들 때도 확장 속성을
일치시켜야 합니다. Custom OHLCV 재집계는 Custom 실습을 참고합니다.

## 정리

```sql
DROP ROLLUP ch6_ext_plain;
DROP ROLLUP ch6_ext_first;
DROP TABLE ch6_ext;
```
