# 테이블 구조와 스키마

VOLATILE 테이블의 PRIMARY KEY 설계와 스키마 구성 방법을 다룹니다.

## PRIMARY KEY 설계

VOLATILE 테이블은 PRIMARY KEY 없이도 생성할 수 있습니다. 단, PK 기반 조회나 `ON DUPLICATE KEY UPDATE`를 사용하려면 PRIMARY KEY가 필요합니다.

### 단일 PRIMARY KEY

```sql
CREATE VOLATILE TABLE ch10_schema_state (
    device_id  VARCHAR(32) PRIMARY KEY,
    state      VARCHAR(16),
    updated_at DATETIME
);
```

### 복합 키가 필요한 경우

여러 컬럼 조합으로 행을 고유하게 식별해야 하면 조합 키를 별도 PRIMARY KEY 컬럼으로 둡니다.

```sql
CREATE VOLATILE TABLE ch10_schema_hourly (
    key_id     VARCHAR(96) PRIMARY KEY,
    sensor_id  VARCHAR(64),
    hour_ts    DATETIME,
    avg_value  DOUBLE,
    sample_cnt INTEGER
);

-- 조합 키 삽입
INSERT INTO ch10_schema_hourly
VALUES ('TEMP-01:2026010110', 'TEMP-01', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 23.5, 60);
INSERT INTO ch10_schema_hourly
VALUES ('TEMP-01:2026010111', 'TEMP-01', TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS'), 24.1, 60);
INSERT INTO ch10_schema_hourly
VALUES ('TEMP-02:2026010110', 'TEMP-02', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 21.0, 60);

-- 조합 키 조회
SELECT sensor_id, avg_value FROM ch10_schema_hourly
 WHERE key_id = 'TEMP-01:2026010110';
```

### ON DUPLICATE KEY UPDATE와 함께 사용

```sql
-- PRIMARY KEY 중복 시 UPDATE 실행
INSERT INTO ch10_schema_state VALUES ('DEV-01', 'ONLINE', NOW)
ON DUPLICATE KEY UPDATE SET state = 'ONLINE', updated_at = NOW;
```

### 주의사항

- PRIMARY KEY 없이 생성할 수 있지만, PK 기반 동작(UPSERT, PK 조회 등)은 사용할 수 없습니다.
- PRIMARY KEY가 같은 행을 둘 이상 저장할 수 없습니다. `ON DUPLICATE KEY UPDATE`는 중복 행을
  추가하는 대신 기존 행을 갱신합니다.
- PRIMARY KEY 컬럼은 하나만 지정합니다.

## VOLATILE 테이블 설계

VOLATILE 테이블은 데이터를 메모리에만 두고, 서버 재시작 시 데이터가 소멸합니다.
테이블 정의는 남으므로 설계에서 정할 것은 "무엇을 잃어도 되는가"와 "어떻게 다시 채우는가"
두 가지입니다. 여러 세션이 공유하되 재시작 후 복구할 필요가 없는 상태나 캐시에 사용합니다.

스키마를 정할 때는 다음 항목을 함께 검토합니다.

- 활용 사례
- 영속성 차이와 DDL
- 메모리 생명주기
- Red-Black 트리 인덱스
- ON DUPLICATE KEY UPDATE
- 재시작과 데이터 재구성

이 페이지의 실습 테이블은 다음과 같이 정리합니다.

```sql
DROP TABLE ch10_schema_hourly;
DROP TABLE ch10_schema_state;
```
