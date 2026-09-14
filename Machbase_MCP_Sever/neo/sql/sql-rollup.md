# Machbase Neo SQL Rollup

## 소개

대규모 시계열 데이터셋에서 통계 집계를 조회하는 일은 성능 면에서 큰 부담입니다. 넓은 시간 범위나 전체 데이터셋에 대한 집계는 계산 비용이 크고 시간이 오래 걸립니다. Machbase는 TAG 테이블에 저장된 시계열 데이터의 통계 분석을 최적화하도록 설계된 롤업(Rollup) 기능으로 이 문제를 해결합니다. 롤업 테이블은 정해진 시간 단위로 데이터를 미리 집계해 두어 자주 쓰는 통계 지표를 빠르게 조회할 수 있게 합니다.

## 핵심 개념

Machbase의 **롤업 테이블**은 원본 TAG 테이블이나 다른 롤업 테이블로부터 미리 계산한 집계 데이터를 저장하는 파생 테이블입니다. 이 사전 집계 과정은 Machbase가 내부적으로 관리하므로, 질의 실행 시 실시간으로 통계를 계산하는 부담을 크게 줄여 줍니다.

### 지원하는 집계 함수

롤업 테이블은 기본적으로 다음 표준 집계 함수를 지원합니다:
*   `MIN()`: 구간 내 최솟값입니다.
*   `MAX()`: 구간 내 최댓값입니다.
*   `SUM()`: 구간 내 값의 합입니다.
*   `COUNT()`: 구간 내 데이터 포인트 수입니다.
*   `AVG()`: 구간 내 값의 평균입니다.
*   `SUMSQ()`: 구간 내 값의 제곱합입니다.

### 확장 집계 함수(선택)

생성 시 `EXTENSION` 키워드를 사용하면 롤업 테이블이 다음도 지원합니다:
*   `FIRST()`: 구간 내에 기록된 첫 번째 값입니다.
*   `LAST()`: 구간 내에 기록된 마지막 값입니다.

### 시간 단위

롤업 집계는 다음의 고정된 시간 구간을 기준으로 동작합니다:
*   Seconds (`SEC`)
*   Minutes (`MIN`)
*   Hours (`HOUR`)

롤업을 사용하는 질의는 이 기본 단위나 그 배수를 기준으로 집계를 요청할 수 있습니다. 일·주·월·년처럼 더 큰 개념 단위도 사용할 수 있으며, 내부적으로 적절한 기본 롤업 테이블에 대응됩니다(1일 이상 구간은 보통 HOUR 기반).

## 롤업 테이블 종류

Machbase는 롤업 테이블을 만들고 관리하는 두 가지 방법을 제공합니다:

### 기본 롤업(Default Rollup)

*   `WITH ROLLUP` 절로 TAG 테이블을 만들 때 자동으로 생성됩니다.
*   지정한 최소 단위에 따라 표준 롤업 계층(초·분·시)을 만듭니다. 예를 들어 `WITH ROLLUP (MIN)`은 분·시 롤업을, `WITH ROLLUP` 또는 `WITH ROLLUP (SEC)`은 초·분·시 롤업을 만듭니다.
*   롤업 테이블 이름은 원본 TAG 테이블 이름에서 자동으로 파생됩니다(예: `_mytag_ROLLUP_SEC`).
*   TAG 테이블 하나당 기본 롤업 테이블 세트는 하나만 존재할 수 있습니다.

### 사용자 정의 롤업(Custom Rollup)

*   사용자가 `CREATE ROLLUP` 문으로 직접 만듭니다.
*   집계 구간을 원하는 대로 지정할 수 있습니다(예: 10초, 5분).
*   TAG 테이블이나 다른 사용자 정의 롤업 테이블을 기반으로 만들 수 있어 다단계 집계 계층을 구성할 수 있습니다.
*   기본 단위를 넘어서는 집계 요구를 유연하게 정의할 수 있습니다.

## 롤업 테이블 생성

### 기본 롤업 생성

기본 롤업 테이블은 TAG 테이블을 정의할 때 암묵적으로 생성됩니다.

중요: TAG 테이블은 정확히 name, time, value 세 컬럼으로 구성되어야 합니다.
- name: 태그 식별자 (VARCHAR, PRIMARY KEY)
- time: 타임스탬프 (DATETIME BASETIME)  
- value: 측정값 (숫자 타입, SUMMARIZED - 롤업 집계 대상)

추가 컬럼은 허용되지 않습니다. 여러 종류의 센서 값을 저장하려면 
값 종류마다 별도의 TAG 테이블을 만들어야 합니다.

**Syntax:**

```sql
CREATE TAG TABLE table_name (
    name datatype PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE [SUMMARIZED]
    [, additional_columns...]
)
WITH ROLLUP [ ( SEC | MIN | HOUR ) ] [ EXTENSION ];
```

*   `SEC | MIN | HOUR`: 필요한 가장 세밀한 단위를 지정합니다. 생략하면 `SEC`으로 간주합니다. 지정한 단위보다 큰 단위(MIN, HOUR)는 자동으로 포함됩니다(예: `MIN`은 `HOUR`를 포함).
*   `EXTENSION`: `FIRST()`와 `LAST()` 집계 함수를 활성화하는 선택 키워드입니다.

**Examples:**

SEC, MIN, HOUR 롤업을 만듭니다:

```sql
CREATE TAG TABLE sensor_data (...) WITH ROLLUP;
```

MIN, HOUR 롤업을 만듭니다:

```sql
CREATE TAG TABLE hourly_stats (...) WITH ROLLUP (MIN);
```

HOUR 롤업만 만듭니다:

```sql
CREATE TAG TABLE daily_summary (...) WITH ROLLUP (HOUR);
```

FIRST/LAST를 지원하는 SEC, MIN, HOUR 롤업을 만듭니다:

```sql
CREATE TAG TABLE detailed_sensor_data (...) WITH ROLLUP EXTENSION;
```

### 사용자 정의 롤업 생성

사용자 정의 롤업 테이블은 전용 DDL 문으로 명시적으로 만듭니다.

**Syntax:**

```sql
CREATE ROLLUP rollup_name
ON source_table_or_rollup_name ( source_value_column )
INTERVAL interval_value ( SEC | MIN | HOUR )
[ EXTENSION ];
```

*   `rollup_name`: 새 롤업 테이블에 사용자가 붙이는 이름입니다.
*   `source_table_or_rollup_name`: 원본 TAG 테이블 또는 기존 롤업 테이블의 이름입니다.
*   `source_value_column`: 원본 테이블에서 집계할 숫자 컬럼입니다. (원본이 다른 롤업 테이블이면 생략합니다.)
*   `interval_value`: 집계 주기를 정하는 숫자 값입니다(예: 10, 30).
*   `SEC | MIN | HOUR`: 구간의 시간 단위입니다.
*   `EXTENSION`: `FIRST()`와 `LAST()` 집계 함수를 활성화하는 선택 키워드입니다.

**제약 사항:**

*   원본은 TAG 테이블이거나 다른 롤업 테이블이어야 합니다.
*   원본이 롤업 테이블이면 새 `INTERVAL`은 원본 롤업 구간의 배수여야 하며 더 큰 단위여야 합니다.

**Examples:**

'tag_data' 테이블의 'value' 컬럼을 기준으로 30초 롤업을 만듭니다:

```sql
CREATE ROLLUP _tag_data_rollup_30sec ON tag_data(value) INTERVAL 30 SEC;
```

앞서 만든 30초 롤업을 기준으로 10분 롤업을 만듭니다:

```sql
CREATE ROLLUP _tag_data_rollup_10min ON _tag_data_rollup_30sec INTERVAL 10 MIN;
```

FIRST/LAST를 지원하는 15분 롤업을 만듭니다:

```sql
CREATE ROLLUP _tag_data_rollup_15min_ext ON tag_data(value) INTERVAL 15 MIN EXTENSION;
```

## 롤업과 일반 집계 비교

TAG 테이블에 롤업 테이블이 있으면(`WITH ROLLUP` 또는 `CREATE ROLLUP`으로 생성) 사전 집계 데이터를 활용하기 위해 `ROLLUP()` 함수를 사용해야 합니다. `ROLLUP()` 없이 일반 SQL 집계 함수를 쓰면 원본 데이터를 전부 훑게 되어 성능이 크게 떨어집니다.

### 성능 Comparison

수백만 행이 있고 WITH ROLLUP이 활성화된 TAG 테이블을 가정합니다:

느림 — 일반 집계는 원본 데이터를 전부 훑습니다(수백만 건 스캔):

```sql
SELECT
    DATE_TRUNC('hour', time) as hour_time,
    AVG(value) as avg_value
FROM sensor_data
WHERE name = 'SENSOR_A'
  AND time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-12-31')
GROUP BY DATE_TRUNC('hour', time)
ORDER BY hour_time;
```

빠름 — ROLLUP() 함수는 사전 집계 데이터를 사용합니다(100배 이상 빠름):

```sql
SELECT
    ROLLUP('hour', 1, time) AS hour_time,
    AVG(value) AS avg_value
FROM sensor_data
WHERE name = 'SENSOR_A'
  AND time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-12-31')
GROUP BY hour_time
ORDER BY hour_time;
```

### Key Rules

1. **롤업 테이블이 있으면 시간 기준 집계에는 항상 `ROLLUP()` 함수를 사용하세요**
2. 일반 `GROUP BY` 집계는 다음 경우에만 사용하세요:
   - 해당 TAG 테이블에 롤업 테이블이 없을 때
   - 롤업이 지원하지 않는 집계가 필요할 때(예: STDDEV, PERCENTILE)
   - 시간이 아닌 기준으로 그룹화해야 할 때

## 롤업 데이터 조회

사전 집계 데이터의 성능 이점을 얻으려면 질의에서 `ROLLUP()` 함수(또는 더 이상 권장되지 않는 `ROLLUP` 키워드 문법)를 사용해야 합니다. Machbase는 요청한 구간과 단위에 따라 가장 적합한 롤업 테이블을 자동으로 선택합니다.

**문법(권장):**

```sql
SELECT
    ROLLUP( time_unit, period, basetime_column [, origin ] ) AS rollup_time,
    AGGREGATE_FUNCTION( value_column ) AS aggregate_result
    [, other_aggregates... ]
FROM
    source_tag_table
WHERE
    [ time_range_predicate ]
    [ AND name_predicate ]
    [ AND other_predicates... ]
GROUP BY
    rollup_time -- Or GROUP BY ROLLUP(...) expression directly
ORDER BY
    rollup_time;
```

*   `time_unit`: 집계 구간의 단위입니다('sec', 'min', 'hour', 'day', 'week', 'month', 'year' 등).
*   `period`: `time_unit` 기준 집계 구간의 숫자 값입니다. 기반이 되는 롤업 테이블 구간의 배수여야 합니다.
*   `basetime_column`: TAG 테이블에서 `BASETIME` 속성이 지정된 DATETIME 컬럼입니다.
*   `origin`: (선택) 시간 버킷의 정렬 기준점을 지정하는 DATETIME 리터럴입니다. 기본값은 '1970-01-01 00:00:00'입니다. 주·월·년 정렬에서 특히 중요합니다.
*   `AGGREGATE_FUNCTION`: 지원되는 함수 중 하나입니다(MIN, MAX, AVG, SUM, COUNT, SUMSQ, 그리고 `EXTENSION`을 사용했다면 FIRST/LAST).

**중요 고려 사항:**

*   질의에는 `ROLLUP()` 표현식(또는 그 별칭)을 참조하는 `GROUP BY` 절이 있어야 합니다.
*   `ROLLUP()`을 사용할 때 값 컬럼에는 지원되는 집계 함수만 적용할 수 있습니다.

**질의 예제:**

특정 월에 대한 TAG_00001의 시간별 MIN·MAX 값:

```sql
SELECT
    ROLLUP('hour', 1, time) as mtime,
    MIN(value),
    MAX(value)
FROM TAG
WHERE name = 'TAG_00001'
  AND time BETWEEN TO_DATE('2023-01-01 00:00:00') AND TO_DATE('2023-01-31 23:59:59')
GROUP BY mtime
ORDER BY mtime;
```

MIN 또는 SEC 단위 롤업이 있다고 가정한 15분 평균값:

```sql
SELECT
    ROLLUP('min', 15, time) AS rollup_interval,
    AVG(value)
FROM TAG
WHERE name = 'SENSOR_A'
GROUP BY rollup_interval
ORDER BY rollup_interval;
```

Extension 롤업으로 일별 FIRST·LAST 값을 구하고 버킷을 2024년 1월 1일에 맞춥니다:

```sql
SELECT
    ROLLUP('day', 1, time, '2024-01-01') as day_interval,
    FIRST(time, value),
    LAST(time, value)
FROM TAG_WITH_EXTENSION
WHERE name = 'SENSOR_B'
GROUP BY day_interval
ORDER BY day_interval;
```

월요일 기준으로 정렬한 주별 평균('2024-01-01'이 월요일이라고 가정):

```sql
SELECT
    ROLLUP('week', 1, time, '2024-01-01') AS week_start,
    AVG(value)
FROM TAG
WHERE name = 'SENSOR_C'
GROUP BY week_start
ORDER BY week_start;
```

## 롤업 테이블 관리

### 수명 주기 제어

롤업 스레드가 수행하는 집계 과정을 직접 제어할 수 있습니다.

**Commands:**

특정 롤업의 집계 스레드를 시작합니다:

```sql
EXEC ROLLUP_START('rollup_name');
```

특정 롤업의 집계 스레드를 정지합니다:

```sql
EXEC ROLLUP_STOP('rollup_name');
```

일반적인 주기 대기를 건너뛰고 특정 롤업의 집계를 즉시 수행합니다:

```sql
EXEC ROLLUP_FORCE('rollup_name');
```

**Examples:**

```sql
EXEC ROLLUP_START('_tag_data_rollup_30sec');
```

```sql
EXEC ROLLUP_STOP('_tag_data_rollup_10min');
```

시간 단위 롤업의 대기 중인 데이터를 지금 처리합니다:

```sql
EXEC ROLLUP_FORCE('_tag_rollup_hour');
```

### 롤업 데이터 삭제

원본 TAG 테이블에서 데이터를 삭제해도 롤업 테이블의 해당 집계 데이터가 자동으로 지워지지는 **않습니다**. 롤업 데이터는 명시적으로 삭제해야 합니다.

**Syntax:**

지정한 테이블의 모든 롤업 데이터를 삭제합니다:

```sql
DELETE FROM table_name ROLLUP;
```

지정한 테이블에서 특정 시각 이전의 롤업 데이터를 삭제합니다:

```sql
DELETE FROM table_name ROLLUP BEFORE TO_DATE('YYYY-MM-DD HH24:MI:SS');
```

테이블 안 특정 태그의 모든 롤업 데이터를 삭제합니다:

```sql
DELETE FROM table_name ROLLUP WHERE name = 'specific_tag_id';
```

특정 태그의 특정 시각 이전 롤업 데이터를 삭제합니다:

```sql
DELETE FROM table_name ROLLUP WHERE name = 'specific_tag_id' AND time <= TO_DATE('YYYY-MM-DD HH24:MI:SS');
``` 

**Examples:**

'TAG' 테이블의 2024년 1월 15일 이전 롤업 데이터를 모두 삭제합니다:

```sql
DELETE FROM TAG ROLLUP BEFORE TO_DATE('2024-01-15 00:00:00');
```

'TAG' 테이블에서 'TAG01'의 모든 롤업 데이터를 삭제합니다:

```sql
DELETE FROM TAG ROLLUP WHERE name = 'TAG01';
```

### 롤업 테이블 삭제

사용자 정의 롤업 테이블은 개별적으로 삭제할 수 있습니다. 기본 롤업 테이블은 보통 상위 TAG 테이블을 삭제할 때 함께 제거됩니다.

**Syntax:**

특정 사용자 정의 롤업 테이블을 삭제합니다:

```sql
DROP ROLLUP rollup_name;
```

TAG 테이블과 그에 종속된 모든 롤업 테이블(기본·사용자 정의)을 삭제합니다:

```sql
DROP TABLE tag_table_name CASCADE;
```

**제약:** 다른 롤업 테이블이 의존하고 있는 롤업 테이블은 삭제할 수 없습니다. 의존하는 롤업을 먼저(생성의 역순으로) 삭제해야 합니다.

**Example:**

_rollup_min이 _rollup_sec에 의존한다고 할 때 역순으로 삭제합니다:

```sql
DROP ROLLUP _rollup_min;
```

```sql
DROP ROLLUP _rollup_sec;
```

'sensor_data' TAG 테이블과 연결된 모든 롤업을 삭제합니다:

```sql
DROP TABLE sensor_data CASCADE;
```

## Rollup Gap

**롤업 갭(Rollup Gap)** 은 원본 TAG 테이블에 입력된 최신 데이터와 롤업 테이블에 처리·반영된 최신 데이터 사이의 시간 차이를 말합니다. 집계가 주기적으로 이뤄지므로 약간의 갭은 정상입니다. 다만 갭이 크거나 계속 늘어난다면 성능 병목의 신호일 수 있습니다.

### 롤업 갭 확인

갭을 포함한 롤업 처리 현황을 확인할 수 있습니다.

**Command:**

```sql
SHOW ROLLUPGAP;
```

이 명령은 활성 롤업 프로세스별 정보를 보여 주며, 갭을 유발하는 대기 데이터 포인트 수도 함께 표시합니다. `GAP`이 0이면 롤업이 최신 상태라는 뜻입니다.

### 롤업 갭 해소

갭이 크게 벌어지면 다음 조치를 고려할 수 있습니다:

1.  **강제 집계:** `EXEC ROLLUP_FORCE('rollup_name');`으로 특정 롤업의 대기 데이터를 즉시 처리합니다.
2.  **병렬성 확대:** 원본 TAG 테이블의 `TAG_PARTITION_COUNT` 속성을 늘립니다. 더 많은 롤업 스레드가 병렬로 동작할 수 있지만 메모리 사용량이 늘어납니다.
3.  **하드웨어 자원:** 서버 자원, 특히 CPU 속도·코어 수와 디스크 I/O 성능을 개선합니다.
4.  **적재 속도 관리:** 데이터 적재 속도가 시스템 처리 용량을 지속적으로 넘어선다면 입력 흐름을 조절하거나 하드웨어를 더 확장하는 방안을 검토하세요.

갭이 계속 남아 있다면 대개 데이터 적재와 롤업 집계를 함께 감당하기에 시스템 자원이 부족하다는 뜻입니다.

## 제약 사항

Machbase 롤업 기능은 강력하지만 다음과 같은 제약이 있습니다:

*   **고정된 집계 함수:** 내장 집계 함수(MIN, MAX, AVG, SUM, COUNT, SUMSQ, 선택적으로 FIRST/LAST)만 지원합니다. 사용자 정의 집계 로직에는 다른 방법이 필요합니다.
*   **원본 데이터 품질:** 원본 TAG 테이블에 적재된 잘못된 데이터나 이상치는 롤업 집계에 그대로 반영됩니다. 적재 전이나 적재 중에 데이터 품질 관리를 적용해야 합니다.
*   **자원 소모:** 롤업 과정은 원본을 읽고 롤업 테이블에 쓰는 데 CPU와 I/O 자원을 사용합니다. 적재 부하가 높은데 자원이 부족하면 자원 경합이 생기고 롤업 갭이 커질 수 있습니다.
*   **지연:** TAG 테이블에 데이터가 도착한 시점과 롤업 테이블에 반영되는 시점 사이에는 집계 주기와 처리 시간만큼의 지연(롤업 갭)이 있습니다. 집계에 마이크로초 정밀도가 필요한 준실시간 질의라면 원본 TAG 데이터를 직접 조회해야 할 수 있습니다.

## 롤업 예제

이 절에서는 Machbase 롤업 테이블의 생성·관리·조회를 보여 주는 실전 예제를 다룹니다.

### 예제 1: 기본 롤업 생성과 조회

기본 롤업 테이블(SEC, MIN, HOUR)이 포함된 TAG 테이블을 만들고 시간별 집계를 조회하는 예제입니다.

**1단계.** 기본 롤업을 활성화한 TAG 테이블을 만듭니다(_iot_sensors_ROLLUP_SEC, _iot_sensors_ROLLUP_MIN, _iot_sensors_ROLLUP_HOUR 생성):

```sql
CREATE TAG TABLE iot_sensors (
    sensor_id VARCHAR(50) PRIMARY KEY,
    event_time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED
) WITH ROLLUP;
```

**2단계.** 샘플 데이터를 입력합니다:

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 10:05:15', 20.1);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 10:15:30', 20.5);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 10:55:00', 21.0);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 11:05:00', 21.5);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 11:35:45', 21.8);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_B', '2024-03-10 10:10:00', 15.0);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_B', '2024-03-10 11:10:00', 16.0);
```

**3단계.** 센서 TEMP_A의 시간별 평균 온도를 조회합니다:

```sql
SELECT
    ROLLUP('hour', 1, event_time) AS hour_interval,
    AVG(temperature) AS avg_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time BETWEEN TO_DATE('2024-03-10 10:00:00') AND TO_DATE('2024-03-10 12:00:00')
GROUP BY
    hour_interval
ORDER BY
    hour_interval;
```

예상 출력(근사):

```text
hour_interval                   avg_temp
---------------------------------------------------------------
2024-03-10 10:00:00 000:000:000 20.533...  -- Avg of 20.1, 20.5, 21.0
2024-03-10 11:00:00 000:000:000 21.65      -- Avg of 21.5, 21.8
```

### 예제 2: 사용자 정의 롤업 생성과 조회

15분마다 데이터를 집계하는 사용자 정의 롤업 테이블을 만드는 예제입니다.

사전 조건: 예제 1의 iot_sensors 테이블이 있다고 가정합니다.

**1단계.** 'temperature' 컬럼을 기준으로 15분 사용자 정의 롤업 테이블을 만듭니다:

```sql
CREATE ROLLUP _iot_sensors_rollup_15min
ON iot_sensors (temperature)
INTERVAL 15 MIN;
```

**2단계.** TEMP_A의 15분 구간별 최소·최대 온도를 조회합니다:

```sql
SELECT
    ROLLUP('min', 15, event_time) AS interval_15min,
    MIN(temperature) AS min_temp,
    MAX(temperature) AS max_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time BETWEEN TO_DATE('2024-03-10 10:00:00') AND TO_DATE('2024-03-10 12:00:00')
GROUP BY
    interval_15min
ORDER BY
    interval_15min;
```

예상 출력(근사):

```text
interval_15min                  min_temp    max_temp
---------------------------------------------------------------
2024-03-10 10:00:00 000:000:000 20.1        20.1        -- 10:00 to 10:14:59
2024-03-10 10:15:00 000:000:000 20.5        20.5        -- 10:15 to 10:29:59
2024-03-10 10:45:00 000:000:000 21.0        21.0        -- 10:45 to 10:59:59 (data at 10:55)
2024-03-10 11:00:00 000:000:000 21.5        21.5        -- 11:00 to 11:14:59
2024-03-10 11:30:00 000:000:000 21.8        21.8        -- 11:30 to 11:44:59
```

### 예제 3: 확장 롤업 조회(FIRST/LAST)

확장 롤업으로 구간 내 첫 값과 마지막 값을 조회하는 예제입니다.

**1단계.** 기본 롤업과 EXTENSION을 함께 지정해 TAG 테이블을 만듭니다(FIRST()·LAST() 활성화):

```sql
DROP TABLE IF EXISTS iot_sensors_ext CASCADE;
```

```sql
CREATE TAG TABLE iot_sensors_ext (
    sensor_id VARCHAR(50) PRIMARY KEY,
    event_time DATETIME BASETIME,
    pressure DOUBLE SUMMARIZED
) WITH ROLLUP EXTENSION;
```

**2단계.** 샘플 데이터를 입력합니다:

```sql
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 09:01:00', 1000.1);
```

```sql
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 09:05:00', 1000.5);
```

```sql
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 09:55:00', 1001.0);
```

```sql
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 10:02:00', 1001.2);
```

```sql
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 10:08:00', 1001.5);
```

```sql
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 10:40:00', 1001.8);
```

**3단계.** PRES_1의 시간별 첫 압력값과 마지막 압력값을 조회합니다:

```sql
SELECT
    ROLLUP('hour', 1, event_time) AS hour_interval,
    FIRST(event_time, pressure) AS first_pressure,
    LAST(event_time, pressure) AS last_pressure
FROM
    iot_sensors_ext
WHERE
    sensor_id = 'PRES_1'
GROUP BY
    hour_interval
ORDER BY
    hour_interval;
```

예상 출력(근사):

```text
hour_interval                   first_pressure last_pressure
----------------------------------------------------------------------
2024-03-10 09:00:00 000:000:000 1000.5         1001.0
2024-03-10 10:00:00 000:000:000 1001.2         1001.8
```

### 예제 4: 다른 단위로 조회하기(일별/주별)

`iot_sensors` 테이블(여러 일·주에 걸친 데이터가 있다고 가정)에서 일별·주별 평균을 조회하는 예제입니다.

'iot_sensors' 테이블에 2024-03-01부터 2024-03-15까지 TEMP_A 데이터가 있다고 가정합니다.

**질의 1.** TEMP_A의 일별 평균 온도:

```sql
SELECT
    ROLLUP('day', 1, event_time) AS day_interval,
    AVG(temperature) AS avg_daily_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-03-01') AND event_time < TO_DATE('2024-03-16')
GROUP BY
    day_interval
ORDER BY
    day_interval;
```

**질의 2.** 월요일('2024-03-04')을 주 시작으로 맞춘 TEMP_A의 주별 평균 온도:

```sql
SELECT
    ROLLUP('week', 1, event_time, '2024-03-04') AS week_start_monday,
    AVG(temperature) AS avg_weekly_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-03-01') AND event_time < TO_DATE('2024-03-16')
GROUP BY
    week_start_monday
ORDER BY
    week_start_monday;
```


### 예제 5: 월별 롤업 조회

롤업 기능으로 데이터를 월 단위로 집계하는 예제입니다. 효율적인 계산을 위해 보통 HOUR 단위 롤업 테이블을 기반으로 동작합니다.

예제 1의 'iot_sensors' 테이블에 여러 달(센서 'TEMP_A'의 2024년 1월~4월)에 걸친 데이터가 있다고 가정합니다. 예제 데이터를 추가로 입력합니다:

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-01-15 12:00:00', 18.0);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-01-25 14:00:00', 18.5);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-02-10 08:00:00', 19.0);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-02-20 09:00:00', 19.2);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-05 10:00:00', 19.5);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-20 11:00:00', 20.0);
```

**질의 1.** TEMP_A의 월별 평균 온도(origin의 기본값 '1970-01-01'이 일반 달력 월에 맞습니다):

```sql
SELECT
    ROLLUP('month', 1, event_time) AS month_interval,
    AVG(temperature) AS avg_monthly_temp,
    COUNT(temperature) AS data_points_per_month
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-01-01') AND event_time < TO_DATE('2024-04-01')
GROUP BY
    month_interval
ORDER BY
    month_interval;
```

예상 출력(근사):

```text
month_interval                  avg_monthly_temp data_points_per_month
--------------------------------------------------------------------------
2024-01-01 00:00:00 000:000:000 18.25            2
2024-02-01 00:00:00 000:000:000 19.1             2
2024-03-01 00:00:00 000:000:000 20.55            8
```

**질의 2.** TEMP_A의 분기(3개월) SUM과 COUNT('month' 단위에 period=3 사용):

```sql
SELECT
    ROLLUP('month', 3, event_time) AS quarter_interval,
    SUM(temperature) AS sum_quarterly_temp,
    COUNT(temperature) AS data_points_per_quarter
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-01-01') AND event_time < TO_DATE('2024-04-01')
GROUP BY
    quarter_interval
ORDER BY
    quarter_interval;
```

예상 출력(근사):

```text
quarter_interval                sum_quarterly_temp data_points_per_quarter
----------------------------------------------------------------------------
2024-01-01 00:00:00 000:000:000 241.1              12
```

**질의 3.** Origin을 명시적으로 지정합니다('month'에 origin을 지정할 때는 반드시 어떤 달의 1일이어야 합니다):

```sql
SELECT
    ROLLUP('month', 1, event_time, '2024-01-01') AS month_interval,
    MIN(temperature) AS min_monthly_temp,
    MAX(temperature) AS max_monthly_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-01-01') AND event_time < TO_DATE('2024-04-01')
GROUP BY
    month_interval
ORDER BY
    month_interval;
```

예상 출력(근사):

```text
month_interval                  min_monthly_temp max_monthly_temp
--------------------------------------------------------------------
2024-01-01 00:00:00 000:000:000 18.0             18.5
2024-02-01 00:00:00 000:000:000 19.0             19.2
2024-03-01 00:00:00 000:000:000 19.5             21.8
```

### 예제 6: 롤업 관리 명령

상태 확인, 강제 처리, 오래된 롤업 데이터 삭제, 롤업이 있는 테이블 삭제 방법을 보여 주는 예제입니다.

**1단계.** 모든 롤업의 현재 갭 상태를 확인합니다:

```sql
SHOW ROLLUPGAP;
```

**2단계.** 특정 사용자 정의 롤업의 처리를 즉시 수행합니다:

```sql
EXEC ROLLUP_FORCE('_iot_sensors_rollup_15min');
```

**3단계.** iot_sensors 테이블의 롤업에서 2024년 3월 1일 이전 데이터를 삭제합니다:

```sql
DELETE FROM iot_sensors ROLLUP BEFORE TO_DATE('2024-03-01 00:00:00');
```

**4단계.** iot_sensors_ext 테이블과 연결된 모든 롤업 테이블을 삭제합니다:

```sql
DROP TABLE iot_sensors_ext CASCADE;
```
