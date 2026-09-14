# 활용 패턴과 시나리오

LOOKUP 테이블의 활용 패턴과 시나리오를 다룹니다.

## 활용 사례

LOOKUP 테이블은 다음과 같은 데이터를 저장하는 데 적합합니다.

## 적합한 데이터 유형

| 유형 | 예시 |
|------|------|
| 코드 테이블 | 국가 코드, 언어 코드, 상태 코드 |
| 기준 정보 | 설비 목록, 제품 분류, 부서 정보 |
| 실시간 갱신 참조 | 환율 테이블, 임계값 설정 |
| 태그 메타데이터 대체 | 센서 정보 (소규모) |

## 코드 테이블

```sql
CREATE LOOKUP TABLE ch9_pattern_country (
    code   VARCHAR(4)   PRIMARY KEY,
    name   VARCHAR(64),
    region VARCHAR(32)
);

INSERT INTO ch9_pattern_country VALUES ('KR', '대한민국', 'Asia');
INSERT INTO ch9_pattern_country VALUES ('US', '미국', 'America');
UPDATE ch9_pattern_country SET name = 'United States' WHERE code = 'US';

SELECT code, name FROM ch9_pattern_country ORDER BY code;
```

두 행이 조회되며, US 행의 name만 `United States`로 바뀌어 있습니다.

상태 코드나 알람 코드도 같은 방식으로 관리하며, 이벤트 원본과 JOIN해 사용합니다.

```sql
CREATE LOOKUP TABLE ch9_pattern_status (
    code  VARCHAR(16) PRIMARY KEY,
    label VARCHAR(64),
    color VARCHAR(16)
);
INSERT INTO ch9_pattern_status VALUES ('RUN',  '가동', 'green');
INSERT INTO ch9_pattern_status VALUES ('STOP', '정지', 'red');

CREATE LOG TABLE ch9_pattern_event (
    event_time DATETIME,
    device_id  VARCHAR(64),
    status     VARCHAR(16)
);
INSERT INTO ch9_pattern_event
VALUES (TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'DEV-01', 'RUN');
INSERT INTO ch9_pattern_event
VALUES (TO_DATE('2026-01-01 10:05:00', 'YYYY-MM-DD HH24:MI:SS'), 'DEV-01', 'STOP');
EXEC TABLE_FLUSH(ch9_pattern_event);

SELECT e.event_time, e.device_id, c.label
  FROM ch9_pattern_event e
  JOIN ch9_pattern_status c ON e.status = c.code
 ORDER BY e.event_time;
```

두 행이 코드 대신 `가동`·`정지` 라벨로 조회됩니다. 코드에 없는 상태가 이벤트에 들어오면
INNER JOIN에서 그 행이 빠지므로, 코드 테이블의 누락도 함께 점검합니다.

## 설비 마스터

```sql
CREATE LOOKUP TABLE ch9_pattern_equip (
    equip_id   VARCHAR(32) PRIMARY KEY,
    equip_name VARCHAR(128),
    location   VARCHAR(64),
    dept       VARCHAR(64),
    install_dt DATETIME
);
INSERT INTO ch9_pattern_equip
VALUES ('TEMP-01', 'Boiler', 'Seoul', 'Production',
        TO_DATE('2025-01-01', 'YYYY-MM-DD'));
INSERT INTO ch9_pattern_equip
VALUES ('TEMP-02', 'Chiller', 'Busan', 'Facility',
        TO_DATE('2025-01-01', 'YYYY-MM-DD'));
```

TAG 테이블의 센서 데이터와 JOIN하면 위치, 부서 같은 기준 정보를 함께 조회할 수 있습니다.

```sql
CREATE TAG TABLE ch9_pattern_sensor (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
INSERT INTO ch9_pattern_sensor
VALUES ('TEMP-01', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 90.0);
INSERT INTO ch9_pattern_sensor
VALUES ('TEMP-02', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 20.0);
EXEC TABLE_FLUSH(ch9_pattern_sensor);

SELECT d.name, m.location, m.dept, d.value
  FROM ch9_pattern_sensor d
  JOIN ch9_pattern_equip m ON d.name = m.equip_id
 WHERE m.dept = 'Production'
 ORDER BY d.name;
```

TEMP-01 한 행만 조회됩니다. 부서 조건은 LOOKUP 쪽 컬럼이므로, 조건을 바꾸면 읽는 TAG
원본은 그대로여도 결과 집합이 달라집니다.

## 임계값 설정

```sql
CREATE LOOKUP TABLE ch9_pattern_threshold (
    sensor_name VARCHAR(64) PRIMARY KEY,
    low_limit   DOUBLE,
    high_limit  DOUBLE,
    alert_level SHORT
);
INSERT INTO ch9_pattern_threshold VALUES ('TEMP-01', 0.0, 100.0, 1);
INSERT INTO ch9_pattern_threshold VALUES ('TEMP-02', 0.0, 100.0, 1);

-- 실시간 임계값 변경
UPDATE ch9_pattern_threshold SET high_limit = 85.0 WHERE sensor_name = 'TEMP-01';
```

임계값 테이블은 TAG 데이터와 결합해 알람 조건을 판단하는 데 사용합니다.

```sql
SELECT s.name, s.value, t.high_limit
  FROM ch9_pattern_sensor s
  JOIN ch9_pattern_threshold t ON s.name = t.sensor_name
 WHERE s.value > t.high_limit
 ORDER BY s.name;
```

TEMP-01만 초과로 판정됩니다. 값 90은 변경 전 한계 100에서는 정상이었으므로, 같은 원본이라도
임계값을 언제 바꿨는지에 따라 판정이 달라진다는 점을 함께 기록합니다.

## SEQUENCE 기반 이력 번호

작은 규모의 관리 이력이나 운영 이벤트에 순번이 필요하면 SEQUENCE 컬럼을 사용할 수 있습니다.

```sql
CREATE LOOKUP TABLE ch9_pattern_note (
    seq        LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    target_id  VARCHAR(64),
    note       VARCHAR(512),
    created_at DATETIME
);

INSERT INTO ch9_pattern_note
VALUES (NEXTVAL(seq), 'TEMP-01', 'threshold changed', NOW);
INSERT INTO ch9_pattern_note
VALUES (NEXTVAL(seq), 'TEMP-02', 'inspection done', NOW);

SELECT seq, target_id FROM ch9_pattern_note ORDER BY seq;
```

seq는 1과 2입니다. 대량 원본 이력은 LOOKUP보다 LOG 테이블에 저장합니다.

이 페이지의 실습 객체는 다음과 같이 정리합니다.

```sql
DROP TABLE ch9_pattern_note;
DROP TABLE ch9_pattern_threshold;
DROP TABLE ch9_pattern_sensor;
DROP TABLE ch9_pattern_equip;
DROP TABLE ch9_pattern_event;
DROP TABLE ch9_pattern_status;
DROP TABLE ch9_pattern_country;
```

## 부적합한 경우

- 명시적 트랜잭션과 일반 관계형 DML이 필요한 데이터 → TRANSACTION 테이블 권장
- UPDATE 불필요한 추가 전용 이력 → LOG 테이블 권장
- 센서 계측값 → TAG 테이블 권장
- 재시작 후 사라져도 되는 최신 상태 캐시 → VOLATILE 테이블 권장
