# 모델링 패턴

실제 운영 환경에서 자주 쓰이는 데이터 모델링 패턴을 다룹니다.

각 절의 SQL은 서로 다른 모델을 보여 주는 예제입니다. 필요한 절을 선택해 별도 실습
환경에서 실행하며, 같은 이름의 테이블이 있는지 먼저 확인합니다. 스키마 생성만으로
수집·집계·캐시 갱신 작업이 자동 실행되지는 않습니다. 입력 애플리케이션이나 작업
스케줄러가 수행할 일과 실패 처리도 함께 설계합니다.

- **시간축 모델링**
- **거리축 모델링**
- **상태·캐시 모델링**
- **이벤트·로그 모델링**
- **참조·마스터 모델링**
- **영속·임시 혼합 패턴**
- **INSERT·UPDATE 패턴**
- **JOIN·메타데이터 설계**
- **복합 타입 조합 패턴**

## 시간축 모델링

시간을 기준 축으로 삼는 패턴으로, 센서 계측값·에너지 모니터링·환경 데이터 등에 적합합니다.

한 행은 계량기 한 대의 한 번의 관측입니다. `time`은 수신 시각이 아닌 측정 시각으로
정하고, `kwh`는 누적 계량값인지 구간 사용량인지 수집 계약에 기록합니다. 다음 스키마는
전압과 전류도 같은 관측에 포함된다는 전제입니다. 측정 주기나 시각이 서로 다르면 같은 행에
억지로 맞추기보다 별도 시계열로 저장하거나 결측 처리 규칙을 정합니다.

### 기본 패턴: TAG 테이블

```sql
CREATE TAG TABLE power_meter (
    meter_id  VARCHAR(32) PRIMARY KEY,
    time      DATETIME    BASETIME,
    kwh       DOUBLE,
    voltage   DOUBLE,
    current   DOUBLE
) METADATA (
    location  VARCHAR(64),
    phase     SHORT,
    rating_kw DOUBLE
);
```

### 시간 범위 집계

```sql
-- 1시간 단위 계량값 평균과 최댓값 (최근 24시간)
SELECT meter_id,
       DATE_TRUNC('hour', time, 1) AS hour,
       AVG(kwh) AS avg_kwh,
       MAX(kwh) AS peak_kwh
FROM power_meter
WHERE time >= NOW - 86400000000000
GROUP BY meter_id, hour
ORDER BY meter_id, hour;
```

`kwh`가 누적 전력량이면 위 평균은 계량기 지시값의 평균이며 시간당 소비량이 아닙니다.
구간 소비량은 시작·종료 계량값의 차이와 계량기 초기화·교체·최댓값 초과 처리 규칙을
함께 적용해 계산합니다. 전력(kW)과 전력량(kWh)도 구분해 컬럼 이름과 단위를 정합니다.

### 다중 해상도 저장 패턴

원시 데이터(고해상도)와 집계 데이터(저해상도)를 별도 테이블에 나누어 저장합니다.

```sql
-- 원시 데이터 (초 단위)
CREATE TAG TABLE power_raw (
    meter_id VARCHAR(32) PRIMARY KEY,
    time     DATETIME    BASETIME,
    kwh      DOUBLE
);

-- 1분 집계 (VOLATILE 또는 별도 TAG로 캐싱)
CREATE VOLATILE TABLE power_1min (
    key_id   VARCHAR(80) PRIMARY KEY,
    meter_id VARCHAR(32),
    ts       DATETIME,
    avg_kwh  DOUBLE,
    max_kwh  DOUBLE
);
```

위 DDL은 저장 공간만 만듭니다. `power_1min`의 `key_id`에는 계량기와 구간을 유일하게
식별할 값을 애플리케이션이 지정하고 집계값을 채워야 합니다. VOLATILE의 결과는 재시작하면
사라지므로 장기 집계 보관소로 사용하지 않습니다. 원본 삭제 후에도 필요한 통계는 영속
TAG 테이블이나 지원되는 ROLLUP으로 보관하고 각각의 보존 정책을 확인합니다.

### 시간대 처리

DATETIME은 시점을 나타내며 문자열 입력과 출력은 접속 환경의 시간대 영향을 받습니다.
한국 시각으로 표시하려면 클라이언트의 시간대 설정을 맞춥니다. 저장된 시각에 9시간을
더하면 같은 시점을 다른 시간대로 표시하는 것이 아니라 값 자체를 9시간 뒤로 바꾸므로
표시용 변환과 구분해야 합니다.

```sql
-- 클라이언트 시간대를 확인한 뒤 원래 시각을 조회
SELECT meter_id,
       time,
       kwh
FROM power_meter
WHERE meter_id = 'MTR-001'
  AND time >= '2024-01-01 00:00:00';
```

입력 시각의 시간대와 접속 시간대가 다르면 입력 전에 기준을 통일합니다. JDBC의
`TIMEZONE` 설정 예는 JDBC 연결을 참고하십시오.

## 거리축 모델링

거리(위치)를 기준 축으로 삼는 패턴으로, 파이프라인 검사·도로 센서·레이저 스캔 등에 적합합니다.

거리축은 시간축의 다른 표시 형식이 아닙니다. 시간축 전용 ROLLUP과 Retention을 그대로
적용할 수 없습니다. 같은 파이프를 반복 검사한다면 `pipe_id`만으로 서로 다른 검사 회차를
섞지 않도록 회차 식별자나 테이블 분리 기준을 정합니다. 아래 예제는 한 파이프의 한 회차를
가정하며 거리 단위는 m, 두께 단위는 mm입니다.

### 기본 패턴

```sql
CREATE TAG TABLE pipeline_thickness (
    pipe_id   VARCHAR(32) PRIMARY KEY,
    distance  DOUBLE      BASEDISTANCE,    -- 단위: 미터
    thickness DOUBLE,
    temp      DOUBLE
);
```

### 구간 데이터 조회

```sql
-- 파이프 ID별 0~50m 구간 데이터 조회
SELECT pipe_id, distance, thickness
FROM pipeline_thickness
WHERE pipe_id = 'PIPE-A'
  AND distance BETWEEN 0.0 AND 50.0
ORDER BY distance;

-- 임계치 이하 구간 조회
SELECT pipe_id, distance, thickness
FROM pipeline_thickness
WHERE pipe_id = 'PIPE-A'
  AND thickness < 8.0   -- 두께가 8mm 미만인 구간
ORDER BY distance;
```

### 거리 기반 집계

```sql
-- 10m 구간별 평균 두께
SELECT pipe_id,
       FLOOR(distance / 10.0) * 10 AS segment_start,
       AVG(thickness) AS avg_thickness,
       MIN(thickness) AS min_thickness
FROM pipeline_thickness
WHERE pipe_id = 'PIPE-A'
GROUP BY pipe_id, FLOOR(distance / 10.0) * 10
ORDER BY segment_start;
```

### 시간 + 거리 복합 모델링

검사 시각과 위치를 함께 관리해야 하면 시간축 TAG 테이블에 거리 컬럼을 추가합니다.

```sql
-- 시간축 + 위치 정보 함께 저장
CREATE TAG TABLE inspection_data (
    inspector  VARCHAR(64) PRIMARY KEY,
    time       DATETIME    BASETIME,
    distance   DOUBLE,      -- 위치 컬럼 (축은 아님)
    thickness  DOUBLE,
    defect     SHORT
);

-- 특정 날짜·구간 조회
SELECT inspector, time, distance, thickness
FROM inspection_data
WHERE inspector = 'INSPECTOR-01'
  AND time BETWEEN '2024-01-01' AND '2024-01-02'
  AND distance BETWEEN 100.0 AND 200.0
ORDER BY time;
```

## 상태·캐시 모델링

디바이스나 센서의 현재 상태를 실시간 조회하기 위한 캐시 모델링 패턴입니다.

### 최신 상태 캐시 패턴

VOLATILE 테이블로 각 디바이스의 현재 상태를 캐싱합니다.

```sql
-- 상태 캐시 (VOLATILE)
CREATE VOLATILE TABLE device_status (
    device_id  VARCHAR(64) PRIMARY KEY,
    status     VARCHAR(16),
    value      DOUBLE,
    updated_at DATETIME
);

-- 상태 이력 (TAG 또는 LOG)
CREATE TAG TABLE device_status_history (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE,
    status VARCHAR(16)
);
```

### 상태 업데이트 흐름

다음 SQL은 이력과 캐시를 각각 갱신하는 동작을 보여 줍니다. 두 입력은 하나의 트랜잭션이
아니며, 각각 평가하는 `NOW`도 같은 시각이라고 보장하지 않습니다. 실제 수집에서는 한 번
정한 측정 시각을 두 경로에 전달합니다. 늦게 도착한 과거 값이 최신 캐시를 덮어쓰지 않도록
이벤트 순서 판정과 동시 갱신 처리를 애플리케이션에서 정합니다.

```sql
-- 새 계측값 수신 시:
-- 1. TAG 테이블에 이력 저장
INSERT INTO device_status_history VALUES ('DEV-01', NOW, 78.5, 'WARNING');

-- 2. VOLATILE 캐시 업데이트 (ON DUPLICATE KEY UPDATE)
INSERT INTO device_status VALUES ('DEV-01', 'WARNING', 78.5, NOW)
ON DUPLICATE KEY UPDATE SET status = 'WARNING', value = 78.5, updated_at = NOW;
```

### 대시보드 조회 패턴

```sql
-- 현재 ALARM 상태인 모든 디바이스
SELECT device_id, status, value, updated_at
FROM device_status
WHERE status IN ('ALARM', 'WARNING')
ORDER BY updated_at DESC;

-- 특정 디바이스의 최신 상태
SELECT device_id, status, value, updated_at
FROM device_status
WHERE device_id = 'DEV-01';
```

### 상태 정의 참조 패턴

상태 코드의 의미는 LOOKUP 테이블에서 관리합니다.

```sql
CREATE LOOKUP TABLE status_definition (
    code    VARCHAR(16) PRIMARY KEY,
    label   VARCHAR(64),
    color   VARCHAR(16),
    severity SHORT
);

INSERT INTO status_definition VALUES ('NORMAL', '정상', 'green', 0);
INSERT INTO status_definition VALUES ('WARNING', '경고', 'yellow', 1);
INSERT INTO status_definition VALUES ('ALARM', '알람', 'red', 2);

-- JOIN 조회
SELECT d.device_id, s.label, s.color, d.value
FROM device_status d
JOIN status_definition s ON d.status = s.code
ORDER BY s.severity DESC;
```

## 이벤트·로그 모델링

시스템 이벤트, 알람, 감사 로그를 LOG 테이블로 모델링하는 패턴입니다.

### 계층적 이벤트 모델

```sql
-- 알람 이벤트 LOG 테이블
CREATE LOG TABLE alarm_event (
    severity    SHORT,          -- 1=INFO, 2=WARN, 3=ERROR, 4=CRITICAL
    category    VARCHAR(32),    -- 카테고리
    source      VARCHAR(64),    -- 발생 소스
    message     VARCHAR(512),
    src_ip      IPV4            -- 발생 IP (있는 경우)
);

-- 시스템 감사 LOG 테이블
CREATE LOG TABLE audit_log (
    user_id    VARCHAR(64),
    action     VARCHAR(32),    -- INSERT, UPDATE, DELETE, LOGIN 등
    target     VARCHAR(128),   -- 대상 테이블/리소스
    detail     TEXT,           -- 상세 내용 (전문 검색 대상)
    result     VARCHAR(8)      -- SUCCESS, FAILURE
);

CREATE INDEX idx_audit_detail ON audit_log(detail) INDEX_TYPE KEYWORD;
```

### 알람 집계 패턴

```sql
-- 최근 1시간 심각도별 알람 수
SELECT severity, COUNT(*) AS cnt
FROM alarm_event
WHERE _arrival_time >= NOW - 3600000000000
GROUP BY severity
ORDER BY severity DESC;

-- 소스별 알람 현황 (최근 24시간)
SELECT source, COUNT(*) AS total,
       SUM(CASE WHEN severity = 4 THEN 1 ELSE 0 END) AS critical_cnt
FROM alarm_event
WHERE _arrival_time >= NOW - 86400000000000
GROUP BY source
ORDER BY total DESC;
```

### 로그 레벨 필터 패턴

```sql
-- ERROR 이상 로그 조회 (최근 10분)
SELECT _arrival_time, source, message
FROM alarm_event
WHERE severity >= 3
  AND _arrival_time >= NOW - 600000000000
ORDER BY _arrival_time DESC
LIMIT 100;
```

### 전문 검색 패턴

```sql
-- 특정 키워드를 포함하는 감사 로그 조회
SELECT _arrival_time, user_id, action, target
FROM audit_log
WHERE detail SEARCH 'password'
  AND _arrival_time >= NOW - 86400000000000;
```

## 참조·마스터 모델링

코드 테이블, 설비 마스터, 사용자 정보 등 참조 데이터를 LOOKUP 테이블로 모델링하는 패턴입니다.

식별자만 이력에 저장하면 이름과 위치를 반복 저장하는 비용을 줄일 수 있습니다. 하지만
현재 마스터의 위치를 바꾸면 과거 이력을 조인한 결과도 새 위치로 표시됩니다. “발생 당시
어느 라인에 있었는가”가 중요하면 유효 기간이 있는 별도 변경 이력을 설계하거나 원본 행에
당시 속성을 기록합니다. 아래 계층 스키마의 참조 관계가 외래 키로 자동 검증되는 것은
아니므로 존재하지 않는 공장·라인 코드를 입력하지 않도록 애플리케이션에서 확인합니다.

### 계층적 코드 체계

```sql
-- 대분류 코드
CREATE LOOKUP TABLE category_main (
    code  VARCHAR(8)  PRIMARY KEY,
    label VARCHAR(64)
);

-- 중분류 코드 (대분류 참조)
CREATE LOOKUP TABLE category_sub (
    code      VARCHAR(16) PRIMARY KEY,
    main_code VARCHAR(8),
    label     VARCHAR(64)
);

CREATE INDEX idx_sub_main ON category_sub(main_code);
```

### 설비 계층 마스터

```sql
-- 공장 마스터
CREATE LOOKUP TABLE factory (
    factory_id VARCHAR(16) PRIMARY KEY,
    name       VARCHAR(64),
    location   VARCHAR(128)
);

-- 라인 마스터 (공장 참조)
CREATE LOOKUP TABLE production_line (
    line_id    VARCHAR(16) PRIMARY KEY,
    factory_id VARCHAR(16),
    name       VARCHAR(64)
);

-- 설비 마스터 (라인 참조)
CREATE LOOKUP TABLE equipment (
    equip_id   VARCHAR(32) PRIMARY KEY,
    line_id    VARCHAR(16),
    equip_name VARCHAR(128),
    equip_type VARCHAR(32),
    install_dt DATETIME
);

CREATE INDEX idx_equip_line ON equipment(line_id);
CREATE INDEX idx_equip_type ON equipment(equip_type);
```

### 마스터 조인 조회 패턴

계측 테이블에는 설비 식별자를 저장하고, 공장·라인·설비 이름 같은 속성은 LOOKUP 테이블에
한 번만 저장합니다. 조회할 때 계측 테이블의 시간 범위를 먼저 제한한 뒤 설비 식별자로
LOOKUP 테이블을 조인합니다. 실제 조인 구문과 실행 계획 확인 방법은
JOIN·서브쿼리을 참고하십시오.

## 영속·임시 혼합 패턴

영속 테이블(TAG, LOG, TRANSACTION, LOOKUP)에 원본을 보관하고 VOLATILE에 조회용 캐시를
유지하는 패턴입니다. 두 저장 경로가 하나의 트랜잭션으로 처리된다고 가정하지 말고,
캐시 지연과 실패 후 재구성 절차를 함께 설계합니다.

### 원본 + 집계 캐시 패턴

원본 데이터는 영속 테이블에, 집계 결과는 VOLATILE 테이블에 저장합니다.

```sql
-- 원본 데이터 (TAG, 영속)
CREATE TAG TABLE sensor_data (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE
);

-- 집계 캐시 (VOLATILE, 임시)
CREATE VOLATILE TABLE sensor_recent_avg (
    key_id    VARCHAR(64) PRIMARY KEY,
    sensor_id VARCHAR(64),
    base_ts   DATETIME,
    avg_val   DOUBLE,
    max_val   DOUBLE,
    cnt       LONG
);
```

### 캐시 갱신 패턴

캐시 한 행은 센서 하나의 최근 2시간 통계입니다. `base_ts`는 집계 창의 경계가 아니라
집계에 포함된 가장 최근 측정 시각입니다. 매번 같은 범위 정의로 계산하고, 정확히 같은
시각의 결과를 비교해야 하면 실행마다 기준 시각을 한 번 정해 사용합니다.
아래 예제는 미래 시각의 측정값을 제외합니다. 결과 비교 시에는 각 SQL의 `NOW` 대신
동일한 고정 기준 시각을 전달해 하한과 상한을 함께 계산합니다.

```sql
-- 주기적 집계 갱신 (1시간마다 실행)
DELETE FROM sensor_recent_avg;

INSERT INTO sensor_recent_avg
SELECT name AS key_id,
       name,
       MAX(time) AS base_ts,
       AVG(value),
       MAX(value),
       COUNT(*)
FROM sensor_data
WHERE time >= NOW - 3600000000000 * 2  -- 최근 2시간 재계산
  AND time <= NOW
GROUP BY name;
```

`INSERT ... SELECT`에는 `ON DUPLICATE KEY UPDATE`를 붙이지 않습니다. 캐시를 재구성할 때는
기존 캐시를 삭제한 뒤 다시 적재합니다.

삭제와 재적재 사이에는 캐시가 비거나 일부만 채워진 상태를 다른 조회가 볼 수 있습니다.
일괄 갱신 중 표시할 결과, 실패 시 재시도와 원본 조회 여부를 애플리케이션에서 정합니다.
항상 일관된 전체 결과가 필요하면 그 요구를 충족하는 별도의 전환·트랜잭션 모델을 검토합니다.

### 대시보드 조회 최적화

```sql
-- 저장된 캐시 조회 (원본 조회로의 전환은 애플리케이션에서 처리)
SELECT sensor_id, base_ts, avg_val, max_val
FROM sensor_recent_avg
WHERE base_ts >= NOW - 3600000000000 * 2
  AND base_ts <= NOW
ORDER BY sensor_id, base_ts;
```

이 조건은 최신 측정 시각이 최근 2시간에 속한 캐시 행을 표시합니다. 기존 평균을 조회
시각 기준으로 다시 계산하는 것은 아니므로, 집계 자체의 최신성은 갱신 주기로 관리합니다.

### 장애 복구

서버 재시작으로 VOLATILE 테이블과 캐시가 소멸되면 테이블을 먼저 다시 만든 뒤 원본
TAG 테이블에서 같은 최근 2시간 통계를 재계산합니다. 아래 CREATE는 테이블이 사라진
재시작 이후에만 실행합니다. 원본 보존 기간 안에 재계산할 데이터가 남아 있어야 합니다.

```sql
-- 캐시 재구성 (서버 재시작 후)
CREATE VOLATILE TABLE sensor_recent_avg (
    key_id    VARCHAR(64) PRIMARY KEY,
    sensor_id VARCHAR(64),
    base_ts   DATETIME,
    avg_val   DOUBLE,
    max_val   DOUBLE,
    cnt       LONG
);

INSERT INTO sensor_recent_avg
SELECT name,
       name, MAX(time), AVG(value), MAX(value), COUNT(*)
FROM sensor_data
WHERE time >= NOW - 3600000000000 * 2  -- 정상 갱신과 같은 최근 2시간
  AND time <= NOW
GROUP BY name;
```

복구 후 캐시의 센서별 건수·평균·최신 시각을 같은 기준 시각의 원본 집계와 비교합니다.
`cnt`는 NULL 측정값을 포함한 행 수입니다. 평균에 사용한 표본 수가 필요하면
`COUNT(value)`를 별도 컬럼으로 저장합니다.

## INSERT·UPDATE 패턴

모델은 어떤 데이터를 변경 가능하게 둘지 결정해야 하지만, 이 페이지에서 DML 지원표를 다시
정의하지 않습니다. 테이블별 변경 조건은 데이터 변경 정책을,
INSERT·Append·파일 입력 선택은
데이터 입력과 반출을 사용하십시오.

## JOIN·메타데이터 설계

여러 테이블 타입을 조합할 때는 다음 원칙을 적용합니다.

먼저 조인의 관계를 정합니다. 센서 코드마다 마스터가 정확히 한 행인지, 코드가 공장마다
반복되는지 확인하십시오. 한 원본 행이 여러 기준 행과 일치하면 결과 행이 늘고 SUM 같은
집계도 중복될 수 있습니다. 코드의 이름뿐 아니라 식별 범위와 타입을 맞춰야 합니다.

1. 원본 행 수뿐 아니라 필터 적용 후 행 수와 실행 계획을 보고 조인 순서를 검토합니다.
2. JOIN 조건 컬럼의 타입을 맞추고, 지원되는 인덱스의 사용 여부를 확인합니다.
3. WHERE 절에 시간 범위와 업무 조건을 명시해 조인할 행 수를 줄입니다.
4. TAG 속성을 함께 조회하는 목적이라면 별도 LOOKUP 대신 METADATA가 적합한지 검토합니다.

재현 가능한 조인 예제는 TAG 조회와 분석과
LOOKUP 조회와 분석을 참고하십시오.

## 복합 타입 조합 패턴

실제 운영 시스템에서 여러 테이블 타입을 조합하는 대표적인 설계 패턴입니다.

### 제조 설비 모니터링 시스템

```
┌─────────────────────────────────────────────────┐
│           설비 모니터링 시스템                     │
├──────────────┬──────────────┬───────────────────┤
│ TAG 테이블   │ LOG 테이블   │ LOOKUP 테이블      │
│ sensor_data  │ alarm_event  │ equipment_master   │
│ (계측값 이력) │ (알람 이벤트) │ (설비 기준 정보)   │
├──────────────┴──────────────┴───────────────────┤
│             VOLATILE 테이블                      │
│             sensor_latest (최신값 캐시)           │
└─────────────────────────────────────────────────┘
```

### 물류·주문 관리 시스템 (Standard Edition)

```
┌─────────────────────────────────────────────────┐
│              물류 관리 시스템                     │
├──────────────┬──────────────┬───────────────────┤
│ TRANSACTION 테이블   │ LOG 테이블   │ LOOKUP 테이블      │
│ orders       │ delivery_log │ product_master     │
│ (주문 관리)  │ (배송 이벤트) │ (제품 기준 정보)   │
│ UPDATE/DELETE│              │                   │
├──────────────┴──────────────┴───────────────────┤
│             VOLATILE 테이블                      │
│             order_status_cache (현재 상태 캐시)  │
└─────────────────────────────────────────────────┘
```

### 패턴 요약

| 역할 | 권장 타입 | 이유 |
|------|---------|------|
| 고빈도 계측값 이력 | TAG | Append API 고속 버퍼, 시계열 최적화 |
| 이벤트·알람 로그 | LOG | 추가 전용, 도착 시각 자동 |
| 관계형 업무 (UPDATE/DELETE) | TRANSACTION | SELECT/INSERT/UPDATE/DELETE 모두 지원 |
| 기준·코드 정보 | LOOKUP | PK 식별과 일반 조건식 UPDATE/DELETE, 영속 |
| 실시간 상태 캐시 | VOLATILE | 메모리 속도, UPSERT |

---

다음으로 읽을 내용:

- SELECT의 GROUP BY와 집계
- 운영 및 구성
