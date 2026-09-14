# 조회와 분석

VOLATILE 테이블의 키 조회, 일반 조건 조회, 임시 집계를 실행 가능한 예제로 설명합니다.

## 예제 데이터 준비

VOLATILE 테이블은 다른 테이블 타입과 동일하게 `SELECT` 문으로 조회합니다. 다음 예제는
마지막 정리 구문까지 순서대로 실행할 수 있습니다.

```sql
CREATE VOLATILE TABLE ch10_query (
    device_id  VARCHAR(64) PRIMARY KEY,
    status     VARCHAR(16),
    value      DOUBLE,
    updated_at DATETIME
);

INSERT INTO ch10_query VALUES ('DEV-01', 'RUNNING', 42.5, NOW);
INSERT INTO ch10_query VALUES ('DEV-02', 'STOPPED', 0, NOW);
```

## PRIMARY KEY 조회

키 조건은 최신 상태 캐시의 단건 조회에 적합합니다.

```sql
SELECT device_id, status, value, updated_at
FROM ch10_query
WHERE device_id = 'DEV-01';
```

## 일반 조건 조회

`PRIMARY KEY`가 아닌 컬럼으로 반복 조회한다면 보조 인덱스를 검토합니다.

```sql
CREATE INDEX ch10_query_status_idx ON ch10_query(status);

SELECT device_id, value, updated_at
FROM ch10_query
WHERE status = 'RUNNING';
```

인덱스도 메모리를 사용하므로 실제 조회에 필요한 컬럼에만 생성합니다.

## 임시 집계 조회

짧은 주기의 집계 결과를 저장하면 대시보드나 알람 판단에서 반복 계산을 줄일 수 있습니다.

```sql
CREATE VOLATILE TABLE ch10_query_summary (
    summary_key VARCHAR(96) PRIMARY KEY,
    sensor_id   VARCHAR(64),
    bucket_time DATETIME,
    avg_value   DOUBLE,
    max_value   DOUBLE,
    sample_cnt  LONG
);

INSERT INTO ch10_query_summary
VALUES ('TEMP-01:2026-01-01T00:00', 'TEMP-01', TO_DATE('2026-01-01 00:00:00'),
        21.5, 23.0, 60);

SELECT sensor_id, bucket_time, avg_value, max_value
FROM ch10_query_summary
WHERE sensor_id = 'TEMP-01'
ORDER BY bucket_time DESC
LIMIT 10;

DROP TABLE ch10_query_summary;
DROP TABLE ch10_query;
```

집계 결과를 장기 보관해야 하면 LOG 또는 TRANSACTION 테이블로 주기적으로 복사합니다.

## 조회 시 주의사항

- 서버 재시작 후에는 데이터가 비어 있으므로 초기 적재 여부를 먼저 확인합니다.
- 키 조회가 중심이면 `PRIMARY KEY`를 지정합니다.
- 범위 조회나 정렬에 자주 쓰는 컬럼은 보조 인덱스를 검토합니다.
- 중요한 원본 데이터는 영속 테이블에 저장하고 VOLATILE은 캐시로 사용합니다.
