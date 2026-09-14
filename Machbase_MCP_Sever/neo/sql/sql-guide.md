# Machbase Neo SQL Guide

## Quick Start

### 테이블 생성

메뉴에서 "SQL"을 선택해 SQL 편집기를 엽니다. 왼쪽 패널에 SQL 편집기가, 오른쪽 패널에 결과와 로그가 표시됩니다.

아래 DDL 문을 복사해 편집기에 붙여 넣습니다:

```sql
CREATE TAG TABLE IF NOT EXISTS example (
  name varchar(100) primary key,
  time datetime basetime,
  value double summarized
);
```

"Ctrl+Enter"를 누르거나 패널 왼쪽 위의 ▶︎ 아이콘을 클릭해 실행합니다. 문장 끝의 세미콜론을 빠뜨리지 마세요.

### 테이블 입력

아래 문장을 실행해 레코드 한 건을 입력합니다:

```sql
INSERT INTO example VALUES('my-car', now, 1.2345);
```

### 테이블 조회

아래 SELECT 문을 실행합니다. 오른쪽 패널에 결과가 표시됩니다:

```sql
SELECT time, value FROM example WHERE name = 'my-car';
```

### Chart Draw

insert 문을 반복 실행해 레코드를 더 입력합니다.

```sql
INSERT INTO example VALUES('my-car', now, 1.2345*1.1);
```

```sql
INSERT INTO example VALUES('my-car', now, 1.2345*1.2);
```

```sql
INSERT INTO example VALUES('my-car', now, 1.2345*1.3);
```

그다음 저장된 'my-car' 레코드를 확인합니다.

```sql
SELECT time, value FROM example WHERE name = 'my-car';
```

오른쪽 패널의 *CHART* 탭을 클릭합니다. 질의 결과가 선 차트로 표시됩니다.

### CSV 파일 내려받기

질의의 전체 결과를 CSV 파일로 내보낼 수 있습니다.

### 테이블 삭제

*DELETE* 문으로 레코드를 삭제합니다.

```sql
DELETE FROM example WHERE name = 'my-car'
```

또는 새로 만들고 싶다면 테이블을 제거합니다.

```sql
DROP TABLE example;
```

## Non-SQL

### show tables

`M$SYS_TABLES` 테이블을 조회하는 간편 명령입니다.

```
show tables;
```

### desc _table_name_

테이블의 컬럼과 관련 인덱스를 설명합니다.

```
desc example;
```

### show tags _table_name_

```
show tags example;
```

테이블에 저장된 태그를 조회합니다. TAG 테이블에서만 동작합니다.

---

## SQL 예제

이 절에는 Machbase Neo에서 실제로 실행해 검증한 SQL 예제가 들어 있습니다.

### 1. 테이블 생성 - 예제 10개

#### 1.1 기본 TAG 테이블 생성
**목적**: 시계열 데이터를 저장하는 기본 테이블
**키워드**: CREATE TAG TABLE, PRIMARY KEY, BASETIME, SUMMARIZED

```sql
-- Basic time-series table
CREATE TAG TABLE sensor_data (
    name VARCHAR(80) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
```

#### 1.2 추가 컬럼이 있는 TAG 테이블
**목적**: SUMMARIZED 컬럼 하나와 추가 데이터 컬럼이 있는 테이블
**키워드**: 단일 SUMMARIZED, 추가 컬럼

```sql
-- Table with additional columns (only one SUMMARIZED allowed)
CREATE TAG TABLE enhanced_sensor (
    device_id VARCHAR(50) PRIMARY KEY,
    timestamp DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED,  -- Only one SUMMARIZED allowed
    location VARCHAR(100),           -- Regular column
    status INTEGER                   -- Regular column
);
```

#### 1.3 전체 롤업이 있는 테이블
**목적**: 초/분/시 단위 자동 집계
**키워드**: WITH ROLLUP

```sql
-- Full Rollup for all units (second/minute/hour)
CREATE TAG TABLE iot_sensors (
    name VARCHAR(80) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP;
```

#### 1.4 롤업(분/시)이 있는 테이블
**목적**: 분/시 단위만 집계
**키워드**: WITH ROLLUP(MIN)

```sql
-- Rollup for minute/hour units only
CREATE TAG TABLE hourly_stats (
    tag_id VARCHAR(50) PRIMARY KEY,
    event_time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED
) WITH ROLLUP(MIN);
```

#### 1.5 롤업(시 단위만)이 있는 테이블
**목적**: 시 단위만 집계
**키워드**: WITH ROLLUP(HOUR)

```sql
-- Rollup for hour unit only
CREATE TAG TABLE daily_summary (
    sensor_id VARCHAR(50) PRIMARY KEY,
    timestamp DATETIME BASETIME,
    avg_value DOUBLE SUMMARIZED
) WITH ROLLUP(HOUR);
```

#### 1.6 통계 기능이 있는 테이블
**목적**: 태그별 통계 정보 자동 수집
**키워드**: TAG_STAT_ENABLE

```sql
-- Statistics feature enabled
CREATE TAG TABLE stat_enabled_table (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) TAG_STAT_ENABLE = 1;
```

#### 1.7 이상치 제거(최솟값 검증)
**목적**: 최솟값 미만 데이터 자동 필터링
**키워드**: LOWER LIMIT

```sql
-- Pressure monitoring (minimum value validation only)
CREATE TAG TABLE pressure_monitor (
    tag_id VARCHAR(50) PRIMARY KEY,
    event_time DATETIME BASETIME,
    pressure_kpa INTEGER SUMMARIZED
);
```

#### 1.8 이상치 제거(최소/최대 값 검증)
**목적**: 범위를 벗어난 데이터 자동 필터링
**키워드**: LOWER LIMIT, UPPER LIMIT

```sql
-- Temperature monitoring (min/max value validation)
CREATE TAG TABLE temperature_sensor (
    sensor_name VARCHAR(50) PRIMARY KEY,
    measurement_time DATETIME BASETIME,
    temp_celsius DOUBLE SUMMARIZED
);
```

#### 1.9 데이터 보존 정책이 있는 테이블
**목적**: 파티션 수 제한으로 오래된 데이터 관리
**키워드**: TAG_PARTITION_COUNT

```sql
-- Table with retention policy
CREATE TAG TABLE retention_table (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP(MIN) 
TAG_PARTITION_COUNT = 4;
```

#### 1.10 고급 기능을 개별 적용한 테이블
**목적**: 고급 기능을 개별적으로 적용
**키워드**: 개별 옵션 적용

롤업 Extension 기능이 있는 테이블:

```sql
CREATE TAG TABLE rollup_extended_sensor (
    device_name VARCHAR(100) PRIMARY KEY,
    recorded_time DATETIME BASETIME,
    sensor_value DOUBLE SUMMARIZED
) WITH ROLLUP EXTENSION;
```

통계 기능이 있는 테이블:

```sql
CREATE TAG TABLE stat_enabled_sensor (
    device_name VARCHAR(100) PRIMARY KEY,
    recorded_time DATETIME BASETIME,
    sensor_value DOUBLE SUMMARIZED
) TAG_STAT_ENABLE = 1;
```

파티션 수를 제한한 테이블:

```sql
CREATE TAG TABLE partition_limited_sensor (
    device_name VARCHAR(100) PRIMARY KEY,
    recorded_time DATETIME BASETIME,
    sensor_value DOUBLE SUMMARIZED
) TAG_PARTITION_COUNT = 12;
```

---

### 2. 데이터 입력 - 예제 10개

#### 2.1 기본 단건 INSERT
**목적**: 레코드 한 건 입력
**키워드**: INSERT INTO VALUES

```sql
-- Single record insertion
INSERT INTO sensor_data VALUES ('TEMP_A', '2024-03-10 10:05:15', 20.1);
```

#### 2.2 현재 시각 단건 INSERT
**목적**: 현재 시각으로 데이터 입력
**키워드**: NOW

```sql
-- Insert data with current time
INSERT INTO sensor_data VALUES ('SENSOR_01', NOW, 25.5);
```

#### 2.3 추가 컬럼을 포함한 INSERT
**목적**: 모든 컬럼에 데이터 입력
**키워드**: 전체 컬럼 입력

```sql
-- Insert data into all columns
INSERT INTO enhanced_sensor VALUES ('DEVICE_01', NOW, 23.5, 'Building A', 1);
```

#### 2.4 밀리초 정밀도 INSERT
**목적**: 밀리초 정밀도 시각으로 데이터 입력
**키워드**: 밀리초 타임스탬프

```sql
-- Millisecond precision time insertion (supports up to .123)
INSERT INTO sensor_data VALUES ('HIGH_FREQ', '2024-03-10 10:05:15.123', 45.67);
```

#### 2.5 연속 단건 INSERT
**목적**: 여러 레코드를 개별 입력(일괄 INSERT 미지원)
**키워드**: 연속 입력

개별 INSERT(일괄 INSERT 문법은 지원되지 않음):

```sql
INSERT INTO iot_sensors VALUES ('SENSOR_01', '2024-03-10 10:00:00', 10.0);
```

```sql
INSERT INTO iot_sensors VALUES ('SENSOR_01', '2024-03-10 10:00:01', 10.1);
```

```sql
INSERT INTO iot_sensors VALUES ('SENSOR_01', '2024-03-10 10:00:02', 10.2);
```

#### 2.6 여러 태그 연속 INSERT
**목적**: 여러 센서의 데이터를 개별 입력
**키워드**: 다중 태그 연속 입력

여러 태그를 개별 입력:

```sql
INSERT INTO sensor_data VALUES ('CPU_TEMP', '2024-03-10 15:30:00', 68.5);
```

```sql
INSERT INTO sensor_data VALUES ('CPU_USAGE', '2024-03-10 15:30:00', 85.2);
```

```sql
INSERT INTO sensor_data VALUES ('MEMORY_USAGE', '2024-03-10 15:30:00', 76.4);
```

#### 2.7 정상 범위 데이터 INSERT
**목적**: 이상치 기능 테스트 - 정상 범위
**키워드**: 정상 값 입력

```sql
-- Normal range data (success)
INSERT INTO temperature_sensor (sensor_name, measurement_time, temp_celsius) 
VALUES ('ROOM_A', NOW, 22.5);
```

#### 2.8 일부 컬럼만 INSERT
**목적**: 필요한 컬럼만 입력
**키워드**: 부분 INSERT

```sql
-- Insert only required columns (excluding NULL-allowed columns)
INSERT INTO enhanced_sensor (device_id, timestamp, temperature) 
VALUES ('DEVICE_03', NOW, 25.8);
```

#### 2.9 정수 데이터 INSERT
**목적**: 정수형 SUMMARIZED 컬럼에 입력
**키워드**: INTEGER 타입

```sql
-- Integer data insertion
INSERT INTO pressure_monitor (tag_id, event_time, pressure_kpa) 
VALUES ('VALVE_01', NOW, 1250);
```

---

### 3. 데이터 조회 - 예제 10개

#### 3.1 기본 전체 데이터 조회
**목적**: 최신 데이터 확인
**키워드**: SELECT *, ORDER BY, LIMIT

```sql
-- Query all data in latest order
SELECT * FROM sensor_data 
ORDER BY time DESC 
LIMIT 100;
```

#### 3.2 특정 태그 데이터 조회
**목적**: 특정 센서의 데이터만 확인
**키워드**: WHERE name

```sql
-- Query specific tag data only
SELECT * FROM sensor_data 
WHERE name = 'TEMP_A' 
ORDER BY time DESC 
LIMIT 10;
```

#### 3.3 시간 범위 조회
**목적**: 특정 기간의 데이터 분석
**키워드**: BETWEEN

```sql
-- Time range query
SELECT name, time, value FROM sensor_data 
WHERE time BETWEEN '2024-03-10 09:00:00' AND '2024-03-10 18:00:00'
ORDER BY time;
```

#### 3.4 값 조건 필터링
**목적**: 임계값을 넘는 데이터 검색
**키워드**: WHERE 조건

```sql
-- Data exceeding threshold
SELECT name, time, value 
FROM sensor_data 
WHERE value > 25.0 
ORDER BY time DESC;
```

#### 3.5 다중 태그 조회
**목적**: 여러 센서 데이터를 동시에 확인
**키워드**: IN

```sql
-- Query multiple tags simultaneously
SELECT name, time, value FROM sensor_data 
WHERE name IN ('TEMP_A', 'TEMP_B', 'HUMIDITY_A')
ORDER BY name, time DESC;
```

#### 3.6 패턴 매칭 조회
**목적**: 특정 패턴의 태그 이름 검색
**키워드**: LIKE

```sql
-- Pattern matching query
SELECT * FROM sensor_data 
WHERE name LIKE 'TEMP_%' 
AND time >= '2024-03-10'
ORDER BY name, time;
```

#### 3.7 집계 함수 조회
**목적**: 그룹별 통계 계산
**키워드**: GROUP BY, AVG, COUNT

```sql
-- Calculate average by tag
SELECT name, 
       COUNT(*) as record_count,
       AVG(value) as avg_value,
       MIN(value) as min_value,
       MAX(value) as max_value
FROM sensor_data 
WHERE time >= '2024-03-01'
GROUP BY name
ORDER BY name;
```

#### 3.8 태그별 최신 시각 조회
**목적**: 태그별 최신 데이터 시각 확인
**키워드**: GROUP BY, MAX

```sql
-- Latest data time for each tag
SELECT name, MAX(time) as latest_time 
FROM sensor_data 
GROUP BY name 
ORDER BY name;
```

#### 3.9 고정 시각 기준 필터링
**목적**: 특정 시각 이후 데이터 조회
**키워드**: 고정 시각 조건

```sql
-- Data after specific timestamp (fixed time only)
SELECT * FROM sensor_data 
WHERE time >= '2025-08-12 00:00:00'
ORDER BY time DESC;
```

#### 3.10 복합 조건 조회
**목적**: 여러 조건을 조합한 검색
**키워드**: AND, OR 조건

```sql
-- Complex condition query
SELECT name, time, value FROM sensor_data 
WHERE (name LIKE 'TEMP_%' AND value > 20.0)
   OR (name LIKE 'PRESSURE_%' AND value > 1000.0)
ORDER BY time DESC
LIMIT 50;
```

---

### 4. 기본 집계 - 예제 10개

#### 4.1 태그별 기본 통계
**목적**: 태그별 기본 통계 정보
**키워드**: GROUP BY 기본 집계

```sql
-- Basic statistics by tag
SELECT name,
       COUNT(*) as count_value,
       AVG(value) as avg_value,
       MIN(value) as min_value,
       MAX(value) as max_value,
       MAX(value) - MIN(value) as value_range
FROM iot_sensors
GROUP BY name
ORDER BY name;
```

#### 4.2 전체 데이터 요약
**목적**: 시스템 전체 데이터 요약
**키워드**: 전체 통계

```sql
-- Overall system data summary
SELECT COUNT(*) as total_records,
       COUNT(DISTINCT name) as total_tags,
       AVG(value) as system_avg,
       MIN(value) as system_min,
       MAX(value) as system_max
FROM iot_sensors;
```

#### 4.3 값 구간별 분포
**목적**: 값 구간별 데이터 분포 확인
**키워드**: CASE WHEN 분류

```sql
-- Data distribution by value range
SELECT 
    CASE 
        WHEN value < 10 THEN 'LOW (< 10)'
        WHEN value < 20 THEN 'MEDIUM (10-20)'
        WHEN value < 30 THEN 'HIGH (20-30)'
        ELSE 'VERY HIGH (≥ 30)'
    END as value_range,
    COUNT(*) as count,
    AVG(value) as avg_in_range
FROM iot_sensors
GROUP BY 
    CASE 
        WHEN value < 10 THEN 'LOW (< 10)'
        WHEN value < 20 THEN 'MEDIUM (10-20)'
        WHEN value < 30 THEN 'HIGH (20-30)'
        ELSE 'VERY HIGH (≥ 30)'
    END
ORDER BY avg_in_range;
```

#### 4.4 태그별 최신 데이터
**목적**: 태그별 가장 최근 데이터
**키워드**: MAX 시각 조회

```sql
-- Latest data time for each tag
SELECT name,
       MAX(time) as latest_time,
       COUNT(*) as total_records
FROM iot_sensors
GROUP BY name
ORDER BY latest_time DESC;
```

#### 4.5 값이 높은 태그
**목적**: 평균값이 높은 태그 식별
**키워드**: HAVING 조건

```sql
-- Tags with average value exceeding threshold
SELECT name,
       COUNT(*) as record_count,
       AVG(value) as avg_value,
       MAX(value) as max_value
FROM iot_sensors
GROUP BY name
HAVING AVG(value) > 15.0
ORDER BY avg_value DESC;
```

#### 4.6 데이터 수집 활동
**목적**: 태그별 데이터 수집 활동 분석
**키워드**: COUNT 기반 분류

```sql
-- Tag classification by data collection volume
SELECT name,
       COUNT(*) as record_count,
       CASE 
           WHEN COUNT(*) < 2 THEN 'LOW_ACTIVITY'
           WHEN COUNT(*) < 10 THEN 'MEDIUM_ACTIVITY'
           ELSE 'HIGH_ACTIVITY'
       END as activity_level
FROM iot_sensors
GROUP BY name
ORDER BY record_count DESC;
```

#### 4.7 값 변동성 분석
**목적**: 태그별 값 변동성 분석
**키워드**: 변동성 계산

```sql
-- Value volatility by tag (range-based)
SELECT name,
       COUNT(*) as sample_size,
       MIN(value) as min_val,
       MAX(value) as max_val,
       MAX(value) - MIN(value) as value_range,
       CASE 
           WHEN MAX(value) - MIN(value) > 10 THEN 'HIGH_VOLATILITY'
           WHEN MAX(value) - MIN(value) > 5 THEN 'MEDIUM_VOLATILITY'
           ELSE 'LOW_VOLATILITY'
       END as volatility_level
FROM iot_sensors
GROUP BY name
ORDER BY value_range DESC;
```

#### 4.8 임계값 초과 분석
**목적**: 설정한 임계값을 넘는 데이터 분석
**키워드**: 조건부 COUNT

```sql
-- Threshold violation data analysis
SELECT name,
       COUNT(*) as total_count,
       SUM(CASE WHEN value > 25.0 THEN 1 ELSE 0 END) as over_threshold,
       SUM(CASE WHEN value < 5.0 THEN 1 ELSE 0 END) as under_threshold,
       AVG(value) as avg_value
FROM iot_sensors
GROUP BY name
ORDER BY name;
```

#### 4.9 데이터 품질 분석
**목적**: 태그별 데이터 품질 분석
**키워드**: NULL 값 분석

```sql
-- Data quality analysis
SELECT name,
       COUNT(*) as total_records,
       COUNT(value) as valid_values,
       COUNT(*) - COUNT(value) as null_values,
       CASE 
           WHEN COUNT(value) = COUNT(*) THEN 'COMPLETE'
           WHEN COUNT(value) > COUNT(*) * 0.9 THEN 'GOOD'
           ELSE 'INCOMPLETE'
       END as data_quality
FROM iot_sensors
GROUP BY name
ORDER BY data_quality, name;
```

---

### 5. 테이블 관리 - 예제 10개

#### 5.1 시스템 테이블 조회
**목적**: 생성된 테이블 목록 확인
**키워드**: M$SYS_TABLES

```sql
-- Query all table list
SELECT name FROM M$SYS_TABLES ORDER BY name;
```

#### 5.2 특정 패턴 테이블 검색
**목적**: 특정 이름 패턴의 테이블 찾기
**키워드**: LIKE 패턴

```sql
-- Search sensor-related tables
SELECT name FROM M$SYS_TABLES WHERE name LIKE '%SENSOR%' ORDER BY name;
```

#### 5.3 조건부 테이블 생성
**목적**: 중복 생성 방지
**키워드**: IF NOT EXISTS

```sql
-- Create only if not exists
CREATE TAG TABLE IF NOT EXISTS backup_sensor (
    name VARCHAR(80) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
```

#### 5.4 메타데이터 테이블 조회
**목적**: TAG 테이블의 메타데이터 확인
**키워드**: _META table

```sql
-- Check metadata table contents
SELECT * FROM _ENHANCED_SENSOR_META;
```

#### 5.5 테이블 구성 요소 확인
**목적**: TAG 테이블의 내부 테이블 확인
**키워드**: 시스템 테이블 패턴

```sql
-- Check all components of specific table
SELECT name FROM M$SYS_TABLES 
WHERE name LIKE '_IOT_SENSORS_%' 
ORDER BY name;
```

#### 5.6 롤업 테이블 확인
**목적**: 자동 생성된 롤업 테이블 확인
**키워드**: ROLLUP 테이블

```sql
-- Check Rollup table list
SELECT name FROM M$SYS_TABLES 
WHERE name LIKE '%_ROLLUP_%' 
ORDER BY name;
```

#### 5.7 단일 테이블 삭제
**목적**: 불필요한 테이블 제거
**키워드**: DROP TABLE

```sql
-- Drop single table
DROP TABLE backup_sensor;
```

#### 5.8 관련 테이블 포함 삭제
**목적**: 롤업 테이블까지 모두 삭제
**키워드**: CASCADE

```sql
-- Drop including Rollup tables
DROP TABLE test_table CASCADE;
```

#### 5.9 삭제 전 존재 확인
**목적**: 안전한 테이블 삭제
**키워드**: 삭제 전 존재 확인

```sql
SELECT COUNT(*) as table_exists
FROM M$SYS_TABLES
WHERE name = 'TEMPORARY_DATA';
```

존재할 때만 삭제(직접 확인 필요):

```sql
DROP TABLE temporary_data;
```

#### 5.10 테이블 존재 확인
**목적**: 테이블 존재 여부 확인
**키워드**: 존재 확인

```sql
-- Check specific table existence
SELECT COUNT(*) as table_exists 
FROM M$SYS_TABLES 
WHERE name = 'IOT_SENSORS';
```

---

### 6. 데이터 분석 - 예제 10개

#### 6.1 태그별 데이터 분포
**목적**: 태그별 데이터 분포 확인
**키워드**: 태그별 분석

```sql
-- Data distribution analysis by tag
SELECT name, 
       COUNT(*) as record_count,
       MIN(time) as first_record,
       MAX(time) as last_record
FROM sensor_data 
GROUP BY name 
ORDER BY record_count DESC;
```

#### 6.2 시스템 전체 요약
**목적**: 시스템 전체 데이터 현황
**키워드**: 전체 요약

```sql
-- Overall system data summary
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT name) as total_sensors,
    MIN(time) as earliest_data,
    MAX(time) as latest_data,
    AVG(value) as system_avg_value
FROM sensor_data;
```

#### 6.3 값 범위 분석
**목적**: 태그별 값 범위 분석
**키워드**: 값 범위 통계

```sql
-- Value range analysis by tag
SELECT name,
       COUNT(*) as count,
       MIN(value) as min_val,
       MAX(value) as max_val,
       AVG(value) as avg_val,
       MAX(value) - MIN(value) as value_range
FROM sensor_data 
GROUP BY name 
ORDER BY value_range DESC;
```

#### 6.4 임계값 초과 분석
**목적**: 설정한 임계값을 넘는 데이터 분석
**키워드**: 임계값 분석

```sql
-- Threshold violation data analysis
SELECT name,
       COUNT(CASE WHEN value > 30.0 THEN 1 END) as over_30,
       COUNT(CASE WHEN value < 10.0 THEN 1 END) as under_10,
       COUNT(*) as total,
       COUNT(CASE WHEN value > 30.0 THEN 1 END) * 100 / COUNT(*) as over_percentage
FROM sensor_data 
GROUP BY name
ORDER BY over_percentage DESC;
```

#### 6.5 데이터 품질 점검
**목적**: NULL 값이나 유효성 확인
**키워드**: 데이터 품질

```sql
-- Data quality check
SELECT name,
       COUNT(*) as total_records,
       COUNT(value) as valid_values,
       COUNT(*) - COUNT(value) as null_values
FROM sensor_data 
GROUP BY name
ORDER BY null_values DESC;
```

#### 6.6 시간 기준 기본 분석
**목적**: 고정 시간 범위 데이터 분석
**키워드**: 시간 범위 분석

```sql
-- Data analysis for specific period
SELECT name, 
       COUNT(*) as record_count,
       AVG(value) as avg_value
FROM sensor_data 
WHERE time >= '2025-08-12 00:00:00'
AND time < '2025-08-13 00:00:00'
GROUP BY name
ORDER BY record_count DESC;
```

#### 6.7 값 분포 구간 분석
**목적**: 값 구간별 분포 확인
**키워드**: 구간 기반 분석

```sql
-- Distribution analysis by value ranges
SELECT name,
       SUM(CASE WHEN value < 10 THEN 1 ELSE 0 END) as low_range,
       SUM(CASE WHEN value >= 10 AND value < 20 THEN 1 ELSE 0 END) as medium_range,
       SUM(CASE WHEN value >= 20 THEN 1 ELSE 0 END) as high_range,
       COUNT(*) as total
FROM sensor_data 
GROUP BY name
ORDER BY name;
```

#### 6.8 극단값 분석
**목적**: 극단값 데이터 확인
**키워드**: 극단값 분석

```sql
-- Top 10 highest values
SELECT name, time, value
FROM sensor_data 
ORDER BY value DESC
LIMIT 10;
```

#### 6.9 태그별 최신 상태
**목적**: 태그별 현재 상태 확인
**키워드**: 최신 상태

```sql
-- Latest data status by tag
SELECT name,
       COUNT(*) as total_records,
       MAX(time) as last_update,
       AVG(value) as current_avg,
       MAX(value) as current_max
FROM sensor_data 
GROUP BY name
ORDER BY last_update DESC;
```

#### 6.10 성능 지표 요약
**목적**: 센서 시스템 전체 성능 지표
**키워드**: 성능 지표

```sql
-- Sensor system performance metrics
SELECT 
    COUNT(DISTINCT name) as active_sensors,
    COUNT(*) as total_data_points,
    AVG(value) as system_average,
    MIN(value) as system_minimum,
    MAX(value) as system_maximum,
    MAX(value) - MIN(value) as total_range
FROM sensor_data 
WHERE time >= '2025-08-01';
```

---

### 7. 백업과 복원 - 예제 10개

#### 7.1 백업 전 데이터 확인
**목적**: 백업 대상 데이터 확인
**키워드**: 백업 전 검증

```sql
-- Check backup target table size
SELECT COUNT(*) as total_records,
       MIN(time) as earliest,
       MAX(time) as latest
FROM sensor_data;
```

#### 7.2 테이블별 레코드 수
**목적**: 백업할 테이블의 데이터 양 확인
**키워드**: 백업 대상 선정

```sql
-- Backup target table list and sizes
SELECT name FROM M$SYS_TABLES 
WHERE name NOT LIKE '_%' 
AND name IN ('SENSOR_DATA', 'IOT_SENSORS', 'ENHANCED_SENSOR')
ORDER BY name;
```

#### 7.3 특정 기간 데이터 확인
**목적**: 부분 백업할 데이터 범위 확인
**키워드**: 시간 범위 확인

```sql
-- Check specific period data
SELECT name,
       COUNT(*) as record_count,
       MIN(time) as start_time,
       MAX(time) as end_time
FROM sensor_data 
WHERE time >= '2025-08-01' AND time < '2025-08-13'
GROUP BY name
ORDER BY name;
```

#### 7.4 주요 메타데이터 백업 확인
**목적**: 메타데이터 테이블 상태 확인
**키워드**: 메타데이터 확인

```sql
-- Check metadata tables
SELECT name FROM M$SYS_TABLES 
WHERE name LIKE '%_META' 
ORDER BY name;
```

#### 7.5 시스템 테이블 목록
**목적**: 시스템 구성 요소 확인
**키워드**: 시스템 상태

```sql
-- Overall system tables status
SELECT name FROM M$SYS_TABLES 
ORDER BY name;
```

#### 7.6 백업 전 데이터 무결성 점검
**목적**: 백업 전 데이터 무결성 확인
**키워드**: 무결성 검사

```sql
-- Data integrity check
SELECT name,
       COUNT(*) as total_records,
       COUNT(value) as valid_values,
       COUNT(*) - COUNT(value) as null_values
FROM sensor_data 
GROUP BY name
ORDER BY name;
```

#### 7.7 최근 활동 테이블 확인
**목적**: 활성 테이블 식별
**키워드**: 활성 테이블

```sql
-- Check tables with recent activity
SELECT name,
       COUNT(*) as recent_records,
       MAX(time) as last_activity
FROM sensor_data 
WHERE time >= '2025-08-01'
GROUP BY name
ORDER BY last_activity DESC;
```

#### 7.8 백업 후 검증 준비
**목적**: 백업 후 비교를 위한 기준 데이터
**키워드**: 검증 기준

```sql
-- Baseline data for backup verification
SELECT 
    COUNT(*) as total_count,
    SUM(CASE WHEN name = 'SENSOR_01' THEN 1 ELSE 0 END) as sensor01_count,
    SUM(CASE WHEN name = 'TEMP_A' THEN 1 ELSE 0 END) as temp_a_count
FROM sensor_data;
```

#### 7.9 테이블 의존성 확인
**목적**: 관련 테이블 확인
**키워드**: 의존성 분석

```sql
-- Check related table structure
SELECT name FROM M$SYS_TABLES 
WHERE name LIKE 'SENSOR_DATA%' OR name LIKE '_SENSOR_DATA_%'
ORDER BY name;
```

#### 7.10 백업 후 검증
**목적**: 백업 성공 여부 확인
**키워드**: 백업 검증

```sql
-- Check current status after backup completion
SELECT 
    COUNT(DISTINCT name) as unique_tags,
    COUNT(*) as total_records,
    MIN(time) as earliest_time,
    MAX(time) as latest_time
FROM sensor_data;
```

---

### 8. 모니터링과 진단 - 예제 10개

#### 8.1 실시간 데이터 확인
**목적**: 최근 데이터 수집 상태 확인
**키워드**: 실시간 모니터링

```sql
-- Recent data collection status
SELECT name, COUNT(*) as recent_count,
       MAX(time) as last_update
FROM sensor_data 
WHERE time >= '2025-08-12 00:00:00'
GROUP BY name
ORDER BY recent_count DESC;
```

#### 8.2 태그별 활동 상태
**목적**: 센서별 최근 활동 확인
**키워드**: 활동 상태

```sql
-- Recent activity time by tag
SELECT name,
       MAX(time) as last_activity,
       COUNT(*) as total_records
FROM sensor_data 
GROUP BY name
ORDER BY last_activity DESC;
```

#### 8.3 데이터 수집 현황
**목적**: 시스템 전체 데이터 수집 현황
**키워드**: 수집 현황

```sql
-- Overall data collection status
SELECT 
    COUNT(DISTINCT name) as active_sensors,
    COUNT(*) as total_records_today,
    MIN(time) as earliest_today,
    MAX(time) as latest_today
FROM sensor_data 
WHERE time >= '2025-08-12 00:00:00';
```

#### 8.4 이상값 모니터링
**목적**: 이상값 실시간 감지
**키워드**: 이상 감지

```sql
-- Anomaly detection
SELECT name, time, value,
       CASE 
           WHEN value > 100 THEN 'HIGH_ALARM'
           WHEN value < -10 THEN 'LOW_ALARM'
           WHEN value > 50 THEN 'HIGH_WARNING'
           ELSE 'NORMAL'
       END as alarm_level
FROM sensor_data 
WHERE (value > 50 OR value < -10)
ORDER BY time DESC
LIMIT 20;
```

#### 8.5 센서 응답성 점검
**목적**: 센서별 데이터 수집 빈도 확인
**키워드**: 응답성 점검

```sql
-- Data collection frequency by sensor
SELECT name,
       COUNT(*) as record_count,
       MIN(time) as first_record,
       MAX(time) as last_record
FROM sensor_data 
WHERE time >= '2025-08-01'
GROUP BY name
ORDER BY record_count DESC;
```

#### 8.6 시스템 성능 요약
**목적**: 시스템 전체 성능 확인
**키워드**: 성능 요약

```sql
-- System performance summary
SELECT 
    COUNT(DISTINCT name) as total_sensors,
    COUNT(*) as total_records,
    AVG(value) as avg_value,
    MIN(value) as min_value,
    MAX(value) as max_value
FROM sensor_data 
WHERE time >= '2025-08-01';
```

#### 8.7 데이터 무결성 점검
**목적**: 중복 또는 누락 데이터 확인
**키워드**: 무결성 검사

```sql
-- Data quality check
SELECT name,
       COUNT(*) as total_records,
       COUNT(value) as valid_values,
       COUNT(*) - COUNT(value) as null_count,
       MIN(value) as min_val,
       MAX(value) as max_val
FROM sensor_data 
GROUP BY name
ORDER BY null_count DESC;
```

#### 8.8 센서 상태 분류
**목적**: 센서 상태별 분류
**키워드**: 상태 분류

```sql
-- Sensor status classification
SELECT name,
       COUNT(*) as record_count,
       MAX(time) as last_seen,
       CASE 
           WHEN COUNT(*) > 10 THEN 'ACTIVE'
           WHEN COUNT(*) > 1 THEN 'MODERATE'
           ELSE 'INACTIVE'
       END as activity_status
FROM sensor_data 
WHERE time >= '2025-08-01'
GROUP BY name
ORDER BY record_count DESC;
```

#### 8.9 알람 이벤트 요약
**목적**: 알람 발생 통계
**키워드**: 알람 통계

```sql
-- Alarm event statistics
SELECT name,
       COUNT(*) as total_events,
       SUM(CASE WHEN value > 50 THEN 1 ELSE 0 END) as warning_events,
       SUM(CASE WHEN value > 100 THEN 1 ELSE 0 END) as critical_events,
       MAX(value) as max_value_seen
FROM sensor_data 
WHERE time >= '2025-08-01'
GROUP BY name
ORDER BY critical_events DESC, warning_events DESC;
```

#### 8.10 센서 상태 진단 요약
**목적**: 센서 시스템 전체 건강 상태
**키워드**: 상태 진단

```sql
-- Sensor system health check summary
SELECT 
    name,
    COUNT(*) as records_count,
    MAX(time) as last_seen,
    AVG(value) as avg_value,
    CASE 
        WHEN COUNT(*) >= 5 THEN 'HEALTHY'
        WHEN COUNT(*) >= 2 THEN 'WARNING'
        ELSE 'CRITICAL'
    END as health_status
FROM sensor_data 
WHERE time >= '2025-08-01'
GROUP BY name
ORDER BY 
    CASE health_status 
        WHEN 'CRITICAL' THEN 1 
        WHEN 'WARNING' THEN 2 
        ELSE 3 
    END, name;
```

---

## 활용 시나리오 예제

### IoT 센서 데이터 처리 전체 가이드
1. **초기 설정**: 롤업과 통계 기능을 갖춘 센서 테이블 생성 (1.3, 1.6)
2. **데이터 수집**: 실시간 센서 데이터 일괄 입력 (2.3, 2.6)
3. **실시간 모니터링**: 분/시 집계 데이터로 추세 분석 (4.2, 4.3)
4. **이상 감지**: 임계값 기반 자동 이상 감지 (6.4, 8.4)
5. **성능 관리**: 데이터 수집 현황과 시스템 성능 모니터링 (8.1, 8.10)
6. **정기 백업**: 일일 자동 백업과 검증 (7.1, 7.9)

### 설비 모니터링 시스템
1. **설비별 테이블**: 이상치 제거 기능으로 비정상 데이터 자동 필터링 (1.7, 1.8)
2. **임계값 관리**: 메타데이터를 통한 동적 임계값 설정 (5.5, 5.6)
3. **예방 정비**: 데이터 분석으로 설비 이상 조기 감지 (6.6, 6.9)
4. **리포트 생성**: 롤업 데이터로 일간/월간 리포트를 효율적으로 작성 (4.10, 6.7)

### 데이터 보관 전략
1. **보존 정책**: 파티션 기반 데이터 관리 (1.9)
2. **백업 자동화**: 예약 백업과 검증 절차 (7.1-7.10)
3. **데이터 품질**: 정기적인 데이터 무결성 점검 (6.5, 8.7)

---

## SQL Guide

다음 절에서는 TAG 테이블의 핵심 개념과 기능을 개괄합니다.  
자세한 내용과 추가 기능은 DBMS 레퍼런스를 참고하세요.
