# ROLLUP 조회 문법

## 명시적인 ROLLUP 조회

```text
rollup(time_unit, period, basetime_column [, origin])
```

| 인자 | 계약 |
|---|---|
| time_unit | SECOND/SEC, MINUTE/MIN, HOUR, DAY, WEEK, MONTH, YEAR; 대소문자 무관 |
| period | 양의 정수 리터럴; 컬럼이나 매개변수 자리표시자가 아님 |
| basetime_column | 원본 시간축 TAG의 BASETIME 컬럼 |
| origin | 생략 시 시간대 오프셋을 반영한 기본 기준점; 명시 시 단위별 제약 확인 |

반환값은 DATETIME 버킷입니다. 저장된 집계의 최소 간격보다 세밀한 결과를 복원할 수는
없습니다. 적용 가능한 ROLLUP이 없으면 원시 스캔으로 자동 전환하지 않고 오류가 발생합니다.
원본 집계가 필요하면 별도의 DATE_TRUNC/DATE_BIN + GROUP BY 쿼리를 작성합니다.

## 준비와 기본 조회

```sql
CREATE TAG TABLE ch6_query (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP ch6_query_sec ON ch6_query(value) INTERVAL 1 SEC;
INSERT INTO ch6_query VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_query VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_query VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_query VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
EXEC TABLE_FLUSH(ch6_query);
ALTER ROLLUP ch6_query_sec FORCE;

SELECT name, rollup('min', 1, time) AS bucket,
       COUNT(value), SUM(value), MIN(value), MAX(value), AVG(value)
  FROM ch6_query
 WHERE time >= TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time < TO_DATE('2026-01-01 00:02:00', 'YYYY-MM-DD HH24:MI:SS')
 GROUP BY name, bucket ORDER BY name, bucket;
```

TEMP_01의 00:00은 COUNT=2, SUM=30, AVG=15이고 00:01은 1, 30, 30입니다.
TEMP_02는 00:00의 1, 100, 100입니다. SELECT에서 name을 반환한다면 GROUP BY에도
name을 넣습니다. name을 빼면 여러 태그를 합친 집계이므로 단위가 다른 센서를 섞지 않습니다.

## 후보 선택과 힌트

1. ROLLUP_TABLE 힌트가 있으면 해당 후보의 호환성을 검사합니다.
2. 자동 선택은 집계 컬럼·JSON 경로·모드와 요청 간격이 맞는 후보를 찾습니다.
3. 조건 없는 후보를 먼저 찾고, 없을 때 조건 후보를 포함해 탐색합니다.
4. 적용 가능한 가장 큰 간격을 선택하며 같은 간격에서는 먼저 등록된 후보가 유지됩니다.

일반/확장 여부만으로 “일반이 항상 우선”이라고 단정하지 않습니다.
조건 ROLLUP만 있을 때는 필터된 데이터가 자동 선택될 수 있으므로 결과가 나타내는
표본 집합을 확인합니다. 반드시 특정 집계를 사용해야 하면 힌트를 명시합니다.

```sql
SELECT /*+ ROLLUP_TABLE(ch6_query_sec) */
       rollup('min', 1, time) AS bucket, AVG(value)
  FROM ch6_query WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

### 저장 후보의 간격과 조회 버킷

현재 후보 간격 검사는 SEC 요청을 period초, MIN 요청을 period분으로 계산합니다.
HOUR와 DAY/WEEK/MONTH/YEAR 요청은 후보 선택 단계에서 period시간을 기준으로 검사하고,
선택된 통계를 요청한 달력·시간 버킷으로 다시 합칩니다.

따라서 `rollup('day', 1, time)`을 위해 24 HOUR ROLLUP을 만들면 자동으로 사용할 수
있다고 가정하면 안 됩니다. 해당 요청은 1시간 기준에 맞는 HOUR/MIN/SEC 후보를 검토합니다.
생성 INTERVAL과 결과 버킷의 의미를 구분하고 실제 실행 계획을 확인합니다.

## 집계 함수와 표본

일반 숫자 ROLLUP은 MIN, MAX, SUM, COUNT, AVG, SUMSQ를 지원합니다.
ROLLUP 조회의 FIRST/LAST에는 EXTENSION이 필요합니다. Custom 결과는 일반 TAG에
저장되므로 Custom 재집계의 합계·건수 규칙을 사용합니다.
JSON 문서 전체 집계의 COUNT도 JSON 절에서 별도로 설명합니다.

### SUMSQ와 분산·표준편차

ROLLUP 조회는 STDDEV, STDDEV_POP, VARIANCE, VAR_POP을 직접 지원하지 않습니다.
`rollup()` 조회에서 이 함수들을 사용하면
`ERR-02816: Only rollup column with aggregate function can be referenced in ROLLUP SELECT query.`
가 발생합니다. 표준편차와 분산은 구간별 결과를 다시 더할 수 없기 때문입니다.
두 구간의 표준편차를 평균해도 전체 구간의 표준편차가 되지 않습니다.

대신 ROLLUP은 값의 제곱합인 SUMSQ를 COUNT, SUM과 함께 저장합니다. 이 세 값은 모두
더할 수 있으므로 저장 간격보다 큰 버킷으로 다시 합쳐도 유효하며, 조회 시점에 분산과
표준편차를 계산할 수 있습니다. SUMSQ는 일반 ROLLUP과 EXTENSION ROLLUP 모두에
포함됩니다.

| 값 | 계산식 |
|---|---|
| 모분산 | `SUMSQ/N - (SUM/N)^2` |
| 모표준편차 | 모분산의 제곱근 |
| 표본분산 | `(SUMSQ - SUM^2/N) / (N-1)` |
| 표본표준편차 | 표본분산의 제곱근 |

N은 `COUNT(value)`이며 NULL을 제외한 유효 값의 개수입니다.

ROLLUP 조회 블록에는 지원되는 집계만 두고, 분산과 표준편차는 인라인 뷰 밖에서
계산합니다. COUNT, SUM, SUMSQ를 한 번만 읽고 파생 계산을 분리하므로 계산식을
바꿔도 ROLLUP 조회 부분은 그대로 사용할 수 있습니다.

```sql
SELECT bucket, n, s, sq,
       sq/n - POWER(s/n, 2)       AS var_pop,
       SQRT(sq/n - POWER(s/n, 2)) AS stddev_pop
  FROM (
      SELECT rollup('min', 1, time) AS bucket,
             COUNT(value)           AS n,
             SUM(value)             AS s,
             SUMSQ(value)           AS sq
        FROM ch6_query WHERE name = 'TEMP_01'
       GROUP BY bucket
  ) t
 ORDER BY bucket;
```

00:00 버킷은 값 10과 20이므로 n=2, s=30, sq=500이고 모분산 25, 모표준편차 5입니다.
00:01 버킷은 값이 하나이므로 모분산과 모표준편차가 0입니다.

표본분산은 분모가 `N-1`이므로 값이 하나인 버킷을 먼저 걸러야 합니다. 이 판단도
인라인 뷰 밖에서 수행합니다. `ELSE NULL`을 명시하면 `ERR-02042`가 발생하므로
`ELSE`를 생략합니다.

```sql
SELECT bucket, n,
       CASE WHEN n > 1
            THEN (sq - POWER(s, 2)/n) / (n - 1)
            END AS var_samp
  FROM (
      SELECT rollup('min', 1, time) AS bucket,
             COUNT(value)           AS n,
             SUM(value)             AS s,
             SUMSQ(value)           AS sq
        FROM ch6_query WHERE name = 'TEMP_01'
       GROUP BY bucket
  ) t
 ORDER BY bucket;
```

00:00 버킷의 표본분산은 50이고, 값이 하나인 00:01 버킷은 NULL입니다.
값이 하나인 구간을 결과에서 빼려면 인라인 뷰 밖에 `WHERE n > 1`을 사용합니다.
원본 테이블의 `VARIANCE`와 `STDDEV`는 같은 구간에서 NULL이 아니라 0을 반환하므로,
두 결과를 함께 사용할 때는 표시 정책을 맞춥니다.

위 예제의 값에서는 원본 테이블에 `VAR_POP`, `STDDEV_POP`, `VARIANCE`, `STDDEV`를
직접 사용한 결과와 같습니다. 다만 두 계산식은 평균이 크고 편차가 작을수록 자리수가
손실됩니다. 예를 들어 값이 100000 부근에서 소수점 이하로만 흔들리면 `SUMSQ/N`과
`(SUM/N)^2`가 거의 같은 크기여서 뺄셈 결과의 유효 자리수가 줄어듭니다. 부동소수
오차로 분산이 아주 작은 음수가 되면 `SQRT`의 결과도 유효하지 않습니다. 정밀도가
중요한 구간에서는 원본 테이블의 `STDDEV`, `VAR_POP` 결과와 비교해 사용할 수 있는
범위를 확인합니다.

## 달력 단위와 origin

같은 준비 데이터를 사용해 월 단위 결과와 월요일 기준 주 단위를 확인합니다.

```sql
SELECT rollup('month', 1, time, '2000-01-01 00:00:00') AS bucket,
       SUM(value), COUNT(value), AVG(value)
  FROM ch6_query WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;

SELECT rollup('week', 1, time, '1970-01-05 00:00:00') AS bucket, AVG(value)
  FROM ch6_query WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

월 조회는 2026-01-01 버킷에 SUM=60, COUNT=3, AVG=20을 반환합니다.
월·년 origin은 시간대 해석 후 월의 1일이어야 하며 결과는 해당 월 경계의 자정입니다.
임의 날짜나 시각 오프셋으로 월간 업무 시작 시각을 옮기는 기능으로 해석하지 않습니다.
일·주 같은 고정 간격의 origin과 월·년의 달력 계산을 구분합니다.

문자열의 의미는 접속 시간대와 함께 확인합니다. DST를 자동으로 원하는 업무 달력에
맞춰 준다고 가정하지 말고 경계 전후의 원본 DATE_BIN 집계와 비교합니다. 저장 집계를
쪼개야 하는 origin이나 조회 경계에는 원본과 동일한 결과를 기대할 수 있는지 검증합니다.

## 정리

```sql
DROP ROLLUP ch6_query_sec;
DROP TABLE ch6_query;
```
