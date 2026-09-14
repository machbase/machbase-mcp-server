# 조회와 분석

LOOKUP 테이블의 키 조회, 일반 조건 조회, TAG 데이터와의 JOIN을 실행 가능한 예제로 설명합니다.

## 예제 데이터 준비

다음 LOOKUP 테이블과 TAG 테이블을 준비합니다.

```sql
CREATE LOOKUP TABLE ch9_query_master (
    sensor_id VARCHAR(32) PRIMARY KEY,
    site      VARCHAR(32),
    unit      VARCHAR(16),
    status    VARCHAR(16)
);

INSERT INTO ch9_query_master VALUES ('TEMP-01', 'SEOUL', 'C', 'ACTIVE');
INSERT INTO ch9_query_master VALUES ('TEMP-02', 'BUSAN', 'C', 'INACTIVE');

CREATE TAG TABLE ch9_query_data (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

INSERT INTO ch9_query_data VALUES ('TEMP-01', TO_DATE('2026-01-01 00:00:00'), 23.5);
INSERT INTO ch9_query_data VALUES ('TEMP-02', TO_DATE('2026-01-01 00:00:00'), 19.0);
```

## PRIMARY KEY 조회

단건 조회는 `PRIMARY KEY` 조건을 사용합니다.

```sql
SELECT sensor_id, site, unit, status
FROM ch9_query_master
WHERE sensor_id = 'TEMP-01';
```

## 일반 조건 조회

LOOKUP 테이블은 일반 컬럼 조건으로도 조회할 수 있습니다. 자주 사용하는 조건 컬럼에는 인덱스를 추가합니다.

```sql
SELECT sensor_id, site, unit
FROM ch9_query_master
WHERE site = 'SEOUL'
  AND status = 'ACTIVE';
```

자주 사용하는 일반 조건 컬럼에는 인덱스를 추가할 수 있습니다. 인덱스 설계와 생성 방법은
인덱스를 참고합니다.

## TAG·LOG 테이블과 JOIN

LOOKUP 테이블은 TAG 또는 LOG 테이블의 원본 데이터에 설명 정보를 붙이는 용도로 자주 사용합니다.

```sql
SELECT d.name, m.site, m.unit, d.time, d.value
FROM ch9_query_data d
JOIN ch9_query_master m ON d.name = m.sensor_id
WHERE m.status = 'ACTIVE';
```

## 분석 패턴

LOOKUP 테이블은 원본 데이터를 저장하기보다 분석 기준을 제공합니다. 다음과 같은 패턴에 적합합니다.

| 패턴 | 설명 |
|------|------|
| 코드 변환 | 상태 코드, 알람 코드, 장비 타입을 라벨로 변환 |
| 기준값 비교 | 센서값을 임계값 테이블과 JOIN해 초과 여부 판단 |
| 그룹 기준 제공 | 위치, 부서, 라인 등 집계 기준 제공 |
| 최신 설정 반영 | 운영 중 변경되는 설정값을 조회 시점에 반영 |

같은 방식으로 임계값 LOOKUP 테이블과 TAG 원본을 JOIN해 기준값 초과 여부를 판정할 수 있습니다.
시간 범위가 큰 TAG 또는 LOG 테이블은 JOIN 전에 시간 조건으로 조회 범위를 제한합니다.

```sql
DROP TABLE ch9_query_data CASCADE;
DROP TABLE ch9_query_master;
```

## 조회 성능 기준

- 단건 조회와 JOIN 기준 컬럼은 `PRIMARY KEY` 또는 인덱스 컬럼을 사용합니다.
- 조건에 자주 쓰는 일반 컬럼은 별도 인덱스를 검토합니다.
- 대량 원본 데이터와 JOIN할 때는 원본 테이블의 시간 범위를 먼저 좁힙니다.
- LOOKUP 테이블에는 기준 정보를 저장하고, 장기 원본 데이터는 TAG 또는 LOG 테이블에 저장합니다.
