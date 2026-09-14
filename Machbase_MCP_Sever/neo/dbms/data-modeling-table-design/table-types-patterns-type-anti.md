# 안티패턴

안티패턴은 특정 테이블을 사용했다는 사실보다 데이터의 의미와 요구사항에 맞지 않는
방식으로 사용한 경우를 뜻합니다. 아래 예제의 전제가 자신의 업무에도 적용되는지 확인한 뒤
대안을 선택하십시오. 같은 스키마라도 현재 상태 관리에는 맞고 이력 누적에는 맞지 않을 수 있습니다.

- **LOOKUP에 무제한 이력 누적**
- **센서별 테이블 생성**
- **잘못된 타입 선택**
- **VOLATILE 영속 저장 오용**
- **시계열 데이터 TRANSACTION 오용**

## LOOKUP에 무제한 이력 누적

### LOOKUP에 무제한 이력 누적 문제

문제는 조회 빈도 자체가 아니라, 계속 늘어나는 계측 이력을 LOOKUP에 저장하는 설계입니다.
LOOKUP은 전체 행과 인덱스를 메모리에 유지하므로 장기 시계열 이력이 쌓일수록 메모리 부담이
커집니다. 작은 기준 정보를 키로 반복 조회하는 용도에는 적합합니다.

### LOOKUP에 무제한 이력 누적 안티패턴 예시

```sql
-- 잘못된 설계: 센서 계측값을 LOOKUP 테이블에 저장
CREATE LOOKUP TABLE sensor_data_wrong (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    ts         DATETIME
);

-- 이 스키마는 sensor_id가 PK이므로 센서마다 현재 한 행만 저장
-- 측정 이력을 그대로 추가하면 같은 PK와 충돌
INSERT INTO sensor_data_wrong VALUES ('TEMP-01', 25.3, NOW);
INSERT INTO sensor_data_wrong VALUES ('TEMP-01', 25.5, NOW);  -- PK 중복 오류
```

### LOOKUP에 무제한 이력 누적 올바른 패턴

태그별 계측 이력 수집과 조회가 중심이면 TAG를 검토합니다. LOOKUP에서도 측정마다 다른
키를 부여할 수 있지만 전체 이력이 메모리에 상주하는 비용은 남습니다. 최신값 캐시는
별도의 성능상 필요가 있고 원본에서 복구할 수 있을 때 VOLATILE로 추가합니다. TAG의
최신값 조회로 요구사항을 만족한다면 캐시를 별도로 유지할 필요가 없습니다.

```sql
-- 올바른 설계: 이력은 TAG 테이블
CREATE TAG TABLE sensor_data (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE
);

-- 최신값 캐시는 VOLATILE 테이블
CREATE VOLATILE TABLE sensor_latest (
    sensor_id VARCHAR(64) PRIMARY KEY,
    value     DOUBLE,
    updated_at DATETIME
);
```

### 결과

| | 안티패턴 (LOOKUP) | 올바른 설계 (TAG) |
|-|-----------------|-----------------|
| 같은 센서 키로 이력 누적 | X (예제의 센서 키가 행을 식별) | O (태그 이름 아래 여러 계측 행 저장) |
| 지속 입력 경로 | 행 식별자 중심 | 시계열 Append API 사용 가능 |
| 시간 범위 조회 | 일반 조건 조회 | 태그·시간 축 조회 |

## 센서별 테이블 생성

### 센서별 테이블 생성 문제

센서(태그)마다 별도 테이블을 생성하는 패턴입니다. 센서 수가 늘어날수록 DDL, 권한과 조회
대상도 함께 늘어나 운영 비용이 커집니다.

### 센서별 테이블 생성 안티패턴 예시

```sql
-- 잘못된 설계: 센서마다 테이블 생성
CREATE TAG TABLE sensor_temp_01 (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE
);
CREATE TAG TABLE sensor_temp_02 (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE
);
CREATE TAG TABLE sensor_temp_03 (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE
);
-- ... 센서가 10,000개면 테이블도 10,000개
```

### 센서별 테이블 생성 문제점

| 문제 | 설명 |
|------|------|
| 관리 복잡도 | 테이블 수만큼 DDL 관리 필요 |
| 쿼리 불편 | 여러 테이블을 결합해야 센서 간 집계 가능 |
| 메타데이터 증가 | 시스템 카탈로그 부하 |
| 신규 센서 추가 | 매번 DDL 실행 필요 |

### 센서별 테이블 생성 올바른 패턴

센서 이름을 PRIMARY KEY로 하는 하나의 TAG 테이블에 모든 센서 데이터를 저장합니다.

이 원칙은 같은 컬럼 구조·권한·보관 정책을 공유하는 센서 집합에 적용합니다. 측정 단위,
스키마, 접근 권한이나 보관 기간을 독립적으로 관리해야 한다면 테이블을 나누는 것이
적절할 수 있습니다. 센서 수 자체를 테이블 분리 기준으로 삼지 않는 것이 핵심입니다.

```sql
-- 올바른 설계: 모든 온도 센서를 하나의 테이블로
CREATE TAG TABLE temperature_sensor (
    name   VARCHAR(128) PRIMARY KEY,
    time   DATETIME     BASETIME,
    value  DOUBLE
);

-- 모든 센서 데이터를 하나의 테이블에 삽입
INSERT INTO temperature_sensor VALUES ('TEMP-01', NOW, 23.5);
INSERT INTO temperature_sensor VALUES ('TEMP-02', NOW, 24.1);
INSERT INTO temperature_sensor VALUES ('TEMP-10000', NOW, 22.9);
```

### 장점

- 신규 센서 추가 시 DDL 불필요 (새 태그 이름으로 INSERT만 하면 됨)
- 크로스-센서 집계 용이
- 운영 관리 포인트 최소화

## 잘못된 타입 선택

데이터 특성에 맞지 않는 테이블 타입을 선택하는 대표적인 안티패턴입니다.

### 안티패턴 1: 이벤트 로그를 TAG 테이블에 저장

```sql
-- 잘못됨: 이벤트 로그를 TAG로 저장
CREATE TAG TABLE error_log_wrong (
    name   VARCHAR(256) PRIMARY KEY,  -- 이벤트 내용이 태그 이름이 됨
    time   DATETIME     BASETIME,
    level  SHORT
);
-- 문제: 이벤트마다 고유 이름 → 태그 수 폭발
```

**올바른 설계**: LOG 테이블 사용

```sql
CREATE LOG TABLE error_log (
    level   SHORT,
    msg     VARCHAR(512),
    src     VARCHAR(128)
);
```

### 안티패턴 2: 센서 값을 LOG 테이블에 저장

LOG에 센서 값이 있다는 사실이 오류는 아닙니다. 문제는 아래처럼 실제 측정 시각을
생략하고, 요구사항은 태그별 측정 시간 집계인데 수신 시각만 남기는 경우입니다.
여러 필드로 된 장비 이벤트를 검색하는 것이 주목적이면 LOG가 적합할 수 있습니다.

```sql
-- 측정 시각이 필요한 요구사항에 부족한 스키마
CREATE LOG TABLE sensor_wrong (
    sensor_id VARCHAR(64),
    value     DOUBLE
    -- 실제 측정 시각이 없고 서버 수신 시각만 자동 저장됨
);
```

**올바른 설계**: TAG 테이블 사용

```sql
CREATE TAG TABLE sensor_measurements (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    value DOUBLE
);
```

### 안티패턴 3: 대용량 이력을 LOOKUP에 저장

```sql
-- 잘못됨: 관계형 트랜잭션이 필요한 주문 이력을 LOOKUP에 저장
CREATE LOOKUP TABLE order_history_wrong (
    order_id LONG PRIMARY KEY,
    customer VARCHAR(64)
    -- 전체 행과 인덱스의 메모리 비용, 명시적 트랜잭션 요구를 확인
);
```

**올바른 설계**: TRANSACTION 테이블 사용

```sql
CREATE TRANSACTION TABLE order_history (
    order_id  LONG,
    customer  VARCHAR(64),
    item_id   INTEGER,
    amount    DOUBLE,
    status    VARCHAR(16)
);
-- UPDATE/DELETE/SELECT 모두 지원
UPDATE order_history SET status = 'SHIPPED' WHERE order_id = 1001;
```

### 안티패턴 4: 시계열 데이터를 TRANSACTION 테이블에 저장

TRANSACTION에도 시간 컬럼과 Append API를 사용할 수 있지만 TAG 전용 시간축 저장 구조와
ROLLUP은 제공되지 않습니다. 관계형 변경보다 계측 이력 수집과 집계가 중심이면 TAG를
검토합니다. 자세한 내용은 시계열 데이터 TRANSACTION 오용을
참고하십시오.

## VOLATILE 영속 저장 오용

### VOLATILE 영속 저장 오용 문제

VOLATILE 테이블에 영구 보존이 필요한 데이터를 저장하는 패턴입니다.

### VOLATILE 영속 저장 오용 안티패턴 예시

```sql
-- 잘못됨: 중요 설정을 VOLATILE에 저장
CREATE VOLATILE TABLE critical_config (
    key_name VARCHAR(64) PRIMARY KEY,
    value    VARCHAR(256)
);

INSERT INTO critical_config VALUES ('license_key', 'XXXX-XXXX-XXXX');
INSERT INTO critical_config VALUES ('max_connections', '1000');
-- 서버 재시작 시 모든 설정 소멸!
```

### VOLATILE 영속 저장 오용 문제점

- 서버가 종료되거나 재시작되면 테이블과 데이터가 소멸합니다.
- 서버 프로세스가 종료되는 장애에서도 메모리의 데이터를 복구할 수 없으므로,
  유일한 원본을 VOLATILE에 저장하면 데이터 손실로 이어집니다.

### VOLATILE 영속 저장 오용 올바른 패턴

영구 보존이 필요한 데이터는 LOOKUP 또는 TRANSACTION 테이블에 저장합니다.

```sql
-- 올바름: 설정은 LOOKUP 테이블
CREATE LOOKUP TABLE app_config (
    key_name VARCHAR(64) PRIMARY KEY,
    value    VARCHAR(256)
);

INSERT INTO app_config VALUES ('max_connections', '1000');
-- 서버 재시작 후에도 데이터 유지
```

### VOLATILE의 올바른 용도

VOLATILE에는 재시작 후 재생성하거나 폐기할 수 있는 데이터를 저장합니다. 조회용 캐시뿐
아니라 수명이 명확한 작업 상태도 포함할 수 있습니다. 업무상 반드시 보존해야 하는
결과를 메모리에만 두지 않습니다.

| 적합 | 부적합 |
|------|--------|
| 센서 최신값 캐시 | 원본 트랜잭션 데이터 |
| 실시간 집계 결과 | 중요 설정 값 |
| 세션 임시 상태 | 감사 로그 |
| 대시보드 캐시 | 사용자 정보 |

## 시계열 데이터 TRANSACTION 오용

### 시계열 데이터 TRANSACTION 오용 문제

센서·IoT 계측값 같은 지속적인 시계열 데이터를 TRANSACTION 테이블에 저장하는 패턴입니다.
관계형 갱신이 필요하지 않다면 TAG 테이블의 태그·시간 축과 ROLLUP을 활용할 수 없으므로
해당 기능이 필요한 조회와 운영 요구에 맞지 않을 수 있습니다. 반대로 측정값 등록을
다른 업무 변경과 하나의 트랜잭션으로 묶어야 하면 TRANSACTION을 선택할 이유가 있습니다.

### 시계열 데이터 TRANSACTION 오용 안티패턴 예시

```sql
-- 잘못됨: 센서 시계열 데이터를 TRANSACTION 테이블에 저장
CREATE TRANSACTION TABLE sensor_timeseries (
    sensor_id VARCHAR(64),
    ts        DATETIME,
    value     DOUBLE,
    unit      VARCHAR(16)
);
```

### 시계열 데이터 TRANSACTION 오용 문제점

| 문제 | 설명 |
|------|------|
| 입력 의미 불일치 | 관계형 트랜잭션이 필요하지 않은 값에도 관계형 쓰기 경로 사용 |
| 시간 축 부재 | TAG의 BASETIME 기반 조회 구조를 사용할 수 없음 |
| 집계 기능 차이 | TAG 전용 ROLLUP을 사용할 수 없음 |

### 시계열 데이터 TRANSACTION 오용 올바른 패턴

센서 계측값은 TAG 테이블에 저장합니다.

```sql
-- 올바름: TAG 테이블 사용
CREATE TAG TABLE sensor_history (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE,
    unit   VARCHAR(16)
);

-- Append API 고속 버퍼로 대량 입력 가능
-- 시간 단위 집계와 TAG 전용 최적화 활용 가능
SELECT name, DATE_TRUNC('hour', time, 1) AS hour, AVG(value), MAX(value)
FROM sensor_history
WHERE time >= NOW - 86400000000000
GROUP BY name, hour;
```

### TRANSACTION 테이블이 적합한 경우

TRANSACTION 테이블은 관계형 구조의 업무 데이터(주문, 재고, 설비 이력 등)에 씁니다. 시간 컬럼이 있더라도 UPDATE/DELETE가 필요한 업무 이력이라면 TRANSACTION 테이블을, 수정 없이 계속 쌓이는 고빈도 계측값이라면 TAG를 선택합니다.

## 의미가 다른 값을 같은 통계로 계산

스키마가 같아도 단위나 행의 의미가 다르면 단순 집계할 수 없습니다. 누적 전력량(kWh)의
평균은 소비 전력(kW)이 아니며, 여러 구간 평균의 단순 평균은 전체 표본 평균과 다를 수
있습니다. NULL을 0으로 채우면 측정 실패가 정상적인 0으로 바뀝니다.

타입을 정할 때 단위, 표본 수와 품질 규칙도 함께 기록합니다. 구간별 통계를 재집계할 때는
합계와 유효 건수 같은 필요한 통계를 유지하고, 원본을 지우기 전에 향후 분석에 필요한
해상도를 확인합니다.
