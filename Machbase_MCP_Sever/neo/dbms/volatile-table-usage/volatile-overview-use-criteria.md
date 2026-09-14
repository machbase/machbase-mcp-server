# 개요와 사용 기준

VOLATILE 테이블은 데이터를 메모리에 저장하는 임시 테이블입니다. 서버가 재시작되면 데이터가 소멸하므로, 재생성 가능한 최신 상태, 임시 집계, 세션 간 공유 캐시 용도로 사용합니다.

## VOLATILE 테이블의 특성

VOLATILE 테이블은 `CREATE VOLATILE TABLE` 문으로 생성합니다.

```sql
CREATE VOLATILE TABLE ch10_overview (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    updated_at DATETIME
);
```

VOLATILE 테이블의 주요 특성은 다음과 같습니다.

| 항목 | 내용 |
|------|------|
| 주요 용도 | 최신 상태 캐시, 임시 집계, 중간 결과 |
| 저장 위치 | 메모리 |
| 재시작 후 데이터 | 소멸 |
| 공유 범위 | 서버 수준 공유 |
| 키 | PRIMARY KEY 선택 |
| 주요 기능 | UPDATE, DELETE, `ON DUPLICATE KEY UPDATE`, Red-Black 트리 인덱스 |
| 백업 | 지원하지 않음 |

## 사용 기준

다음 조건에 해당하면 VOLATILE 테이블을 사용합니다.

- 서버 재시작 후 데이터가 없어져도 됩니다.
- 원본 데이터에서 언제든 다시 계산하거나 재구성할 수 있습니다.
- 최신 상태, 최근 집계, 임시 작업 결과를 빠르게 조회해야 합니다.
- 여러 세션에서 같은 임시 상태를 공유해야 합니다.
- 디스크 영속성보다 메모리 기반 응답 시간이 중요합니다.

최신 센서 상태를 유지하는 예시는 다음과 같습니다.

```sql
INSERT INTO ch10_overview VALUES ('TEMP-01', 23.5, NOW)
ON DUPLICATE KEY UPDATE SET value = 23.5, updated_at = NOW;

SELECT *
FROM ch10_overview
WHERE sensor_id = 'TEMP-01';

-- 다음 절에서 같은 이름을 다시 사용하므로 정리합니다.
DROP TABLE ch10_overview;
```

### 활용 패턴

| 패턴 | key | 재생성 원본 | 권장 만료 방식 |
|------|-----|-------------|----------------|
| 장비 최신 상태 | 장비 ID | TAG 또는 LOG | 같은 key 갱신 |
| 짧은 주기 집계 | 대상과 시간 bucket | TAG 또는 LOG | bucket 교체 또는 재구성 |
| 작업 진행 상태 | 작업 ID | 작업 시스템 | 완료 후 key 삭제 |
| 임시 조회 cache | 요청 또는 객체 ID | 영속 table | 전체 재구성 |

최신 상태 갱신은 데이터 입력과 변경을, 임시 집계는
조회와 분석을 참고합니다.

## 다른 테이블을 검토할 경우

다음 요구사항에는 다른 테이블 타입을 사용합니다.

| 요구사항 | 권장 테이블 |
|----------|-------------|
| 재시작 후에도 반드시 보존해야 하는 원본 데이터 | TAG 또는 LOG |
| 기준 코드나 장비 마스터처럼 영속 참조 데이터 | LOOKUP |
| 트랜잭션과 관계형 갱신이 필요한 업무 데이터 | TRANSACTION |
| 장기 분석 대상 시계열 데이터 | TAG |

VOLATILE 테이블에만 저장된 데이터는 서버 종료 시 복구할 수 없습니다. 중요한 데이터는 TAG, LOG, LOOKUP, TRANSACTION 중 적합한 영속 테이블에 저장하고, VOLATILE 테이블은 캐시나 중간 결과로 사용합니다.

## 설계 순서

VOLATILE 테이블 설계 시 다음 순서로 결정합니다.

1. 데이터가 재생성 가능한지 확인합니다.
2. PRIMARY KEY가 필요한지 결정합니다.
3. 예상 행 수와 메모리 사용량을 산정합니다.
4. 재시작 후 초기 적재 절차를 준비합니다.
5. 보존해야 하는 결과는 애플리케이션의 명시적인 쓰기 작업으로 영속 테이블에 저장합니다.
   VOLATILE을 영속화하는 전용 flush 명령은 없습니다.

스키마와 PRIMARY KEY 설계는 테이블 구조와 스키마에서, 재시작 대응은 재시작과 데이터 소실에서 다룹니다.
