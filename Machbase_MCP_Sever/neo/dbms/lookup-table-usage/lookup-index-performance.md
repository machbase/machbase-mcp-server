# 인덱스와 성능

LOOKUP 테이블의 인덱스 구조와 성능 튜닝을 다룹니다.

## LOOKUP 인덱스 튜닝

LOOKUP의 PRIMARY KEY에는 Red-Black 트리 인덱스가 자동 생성됩니다. 전체 행과 인덱스는
SQL 조회 중 메모리에 상주합니다. 필요하면 non-PK 컬럼에도 Red-Black 보조 인덱스를
추가할 수 있습니다.

### LOOKUP 테이블 인덱스

#### PK 자동 Red-Black 트리 인덱스

LOOKUP 테이블을 생성하면 PRIMARY KEY 컬럼에 Red-Black 트리 인덱스가 자동으로 생성됩니다.
인덱스 항목은 해당 key의 전체 컬럼 값이 들어 있는 메모리 행을 가리킵니다. 따라서 영속
테이블이지만 조회 실행 경로는 메모리 기반이며, 소규모 기준 정보를 key로 반복 조회하는
패턴에 최적화되어 있습니다.

```sql
CREATE LOOKUP TABLE ch9_index_device (
    device_id   VARCHAR(64) PRIMARY KEY,  -- Red-Black 트리 자동 생성
    device_name VARCHAR(128),
    location    VARCHAR(256),
    category    VARCHAR(32)
);

INSERT INTO ch9_index_device VALUES ('DEV-01', 'Boiler', 'Seoul', 'temperature');
INSERT INTO ch9_index_device VALUES ('DEV-02', 'Pump',   'Busan', 'pressure');
```

```sql
-- PK 조회: Red-Black 트리 인덱스 사용
SELECT device_id, device_name, location FROM ch9_index_device
 WHERE device_id = 'DEV-01';
```

한 행이 조회됩니다. 이벤트 로그와 결합할 때도 LOOKUP 쪽은 PK로 찾습니다.

```sql
CREATE LOG TABLE ch9_index_event (device_id VARCHAR(64), level SHORT);
INSERT INTO ch9_index_event VALUES ('DEV-01', 3);
INSERT INTO ch9_index_event VALUES ('DEV-02', 1);
EXEC TABLE_FLUSH(ch9_index_event);

SELECT e.device_id, e.level, d.location
  FROM ch9_index_event e, ch9_index_device d
 WHERE e.device_id = d.device_id
 ORDER BY e.device_id;
```

두 행이 조회됩니다. LOG 쪽에 시간 범위를 함께 걸면 읽을 원본을 더 줄일 수 있습니다.

#### non-PK 컬럼 보조 인덱스

non-PK 컬럼에도 Red-Black 보조 인덱스를 생성할 수 있습니다. 보조 인덱스가 없는 컬럼으로 필터링하면 테이블 전체를 순차 스캔합니다.

```sql
-- 자주 필터링하는 non-PK 컬럼에 보조 인덱스 생성
CREATE INDEX ch9_index_device_location ON ch9_index_device(location);

SELECT device_id FROM ch9_index_device WHERE location = 'Seoul';

-- 인덱스가 없는 컬럼은 전체 스캔 가능
SELECT device_id FROM ch9_index_device WHERE category = 'temperature';
```

두 조회 모두 DEV-01을 반환합니다. 결과가 같아도 접근 경로가 다르므로,
실제 비교는 운영 규모의 데이터에서 실행 계획과 함께 확인합니다.

보조 인덱스는 조회를 빠르게 하지만 갱신 비용과 메모리 사용량이 늘어납니다. 자주 사용하는 조건 컬럼에만 생성합니다.

#### LOOKUP 테이블 사용 가이드라인

Primary key와 Red-Black 보조 인덱스의 조회 비용은 트리 크기에 따라 증가하고, 인덱스가 없는
조건은 메모리에 적재된 전체 행을 스캔합니다. 행 수만으로 사용 한계를 정하지 말고 전체 행의
실제 크기, 가변 길이 값, 인덱스 수, 조회와 갱신 비율을 같은 워크로드로 측정합니다. 서버
기동 시 영속 데이터를 모두 읽어 메모리 행과 인덱스를 구성하므로 기동 시간도 함께 확인합니다.

| 사용 패턴 | 적합성 |
|----------|-------|
| PK로 장치 정보 조회 | 적합 (PK 사용) |
| non-PK 컬럼으로 목록 검색 | 보조 인덱스 생성 시 적합 |
| 소수의 기준 코드 테이블 | 적합 |
| 전체 행이 서버 메모리에 들어가지 않는 대규모 기준 정보 | TRANSACTION 테이블 검토 |
| 관계형 트랜잭션이 필요한 기준 정보 | TRANSACTION 테이블 검토 |

### VOLATILE과의 구분

VOLATILE은 재시작 때 데이터가 사라지는 별도 테이블 타입입니다. VOLATILE 인덱스 설계는
VOLATILE 인덱스와 성능을 참고하십시오.

### 대용량 기준 정보가 필요한 경우

LOOKUP 테이블의 크기와 보조 인덱스 갱신 비용 때문에 다음 시나리오에서는 대안을 고려합니다.

**시나리오**: 장치 기준 정보를 여러 컬럼으로 필터링하고 변경 이력도 함께 보존해야 하는 경우

```sql
-- 대안: LOG 테이블 + LSM/BITMAP 인덱스
CREATE LOG TABLE ch9_index_device_hist (
    device_id   VARCHAR(64),
    device_name VARCHAR(128),
    location    VARCHAR(256),
    category    VARCHAR(32),
    updated_at  DATETIME
);

-- non-PK 컬럼에 인덱스 생성 가능
CREATE INDEX ch9_index_hist_location ON ch9_index_device_hist (location);
CREATE INDEX ch9_index_hist_category ON ch9_index_device_hist (category) INDEX_TYPE BITMAP;
```

단, LOG 테이블은 Append 전용이므로 기준 정보 갱신 패턴에 맞게 설계해야 합니다.

실습에 사용한 객체는 다음과 같이 정리합니다.

```sql
DROP TABLE ch9_index_device_hist;
DROP INDEX ch9_index_device_location;
DROP TABLE ch9_index_event;
DROP TABLE ch9_index_device;
```

### 핵심 정리

- PRIMARY KEY 인덱스는 자동 생성됩니다.
- 반복하는 non-PK 조건에만 보조 인덱스를 만듭니다.
- 행·가변 길이 값·인덱스의 메모리, 기동 시간과 갱신 부하를 함께 측정합니다.
