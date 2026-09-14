# 테이블 타입 선택

잘못된 타입 선택은 성능 저하와 기능 제한으로 이어지므로, 설계 초기에 데이터 성격에 맞는 타입을 결정해야 합니다.

- **타입 선택 결정 가이드**
- **타입 비교표**
- **TRANSACTION vs LOOKUP 비교**

테이블 타입의 역할과 저장 개념은 데이터 모델 개념을
참고하십시오. 같은 데이터라도 이력을 누적할지, 현재 상태를 갱신할지에 따라 적합한 타입이
달라집니다. 변경·조회·영속성 요구사항을 함께 검토합니다.

### 선택 전에 작성할 데이터 설명

테이블 이름보다 먼저 한 행이 나타내는 사실을 한 문장으로 적습니다. 같은 설비에서 나온
데이터라도 “온도 측정 한 건”, “현재 운전 상태 한 건”, “정비 작업 한 건”은 서로 다른
행의 단위이며 키와 변경 방식도 달라집니다.

| 설계 질문 | 설비 모니터링에서 정할 내용 |
|---|---|
| 한 행은 무엇인가? | 센서 한 개의 측정 한 건인지, 설비의 현재 상태인지 구분 |
| 무엇으로 찾는가? | 센서 이름과 발생 시각, 설비 ID, 정비 작업 번호 |
| 값은 어떻게 변하는가? | 새 이력 추가, 잘못된 값 보정, 현재 행 덮어쓰기 |
| 함께 확정할 변경이 있는가? | 정비 작업 등록과 부품 수량 변경을 한 트랜잭션으로 묶을지 결정 |
| 얼마나 보관하는가? | 원본 기간, 집계 기간, 재시작 후 재생성 가능 여부 |
| 어느 정도의 크기인가? | 태그 수, 초당 행 수, 행 크기, 기준 정보와 인덱스의 메모리 사용량 |

예를 들어 온도 이력은 TAG, 알람 사건은 LOG, 설비 코드표는 LOOKUP이 후보입니다.
부품 재고 변경과 작업 등록을 함께 확정해야 하면 Standard Edition의 TRANSACTION을
검토합니다. 현재 상태 캐시는 원본에서 재구성할 수 있을 때 VOLATILE로 분리할 수 있습니다.
이들을 한 테이블로 합치기보다 각 행의 의미와 실패 시 복구 방법을 먼저 맞춥니다.

## 타입 선택 결정 가이드

아래 흐름으로 후보를 좁힌 뒤, 필요한 DML과 트랜잭션, 메모리 사용량, Edition 지원 여부를
비교표에서 확인합니다. 예를 들어 기준 정보라도 여러 변경을 하나의 트랜잭션으로 묶어야
한다면 LOOKUP 대신 TRANSACTION을 검토합니다.

### 결정 흐름

```
데이터가 센서/기기 계측값인가?
  ├── YES → 시간축인가?    YES → TAG TABLE (BASETIME)
  │            거리축인가?  YES → TAG TABLE (BASEDISTANCE)
  └── NO  ↓

데이터가 이벤트/로그/패킷인가? (추가 전용)
  ├── YES → LOG TABLE
  └── NO  ↓

데이터가 코드 테이블/기준 정보인가? (반복 조회·갱신)
  ├── YES → LOOKUP TABLE
  └── NO  ↓

데이터가 서버 재시작 시 폐기 가능한 인메모리 상태/캐시인가?
  ├── YES → VOLATILE TABLE
  └── NO  ↓

일반 관계형 업무 데이터 (UPDATE/DELETE/SELECT/INSERT 모두 필요)
  └── TRANSACTION TABLE
```

### 주요 판단 기준

| 질문 | 타입 |
|------|------|
| 시간 또는 거리 기반 계측값인가? | TAG |
| 원본 이벤트를 추가하고 오래된 구간만 정리하는가? | LOG |
| PRIMARY KEY가 필요한 기준 정보이며 반복 조회·갱신하는가? | LOOKUP |
| 서버 재시작 시 데이터가 사라져도 되는가? | VOLATILE |
| 일반 관계형 업무 (INSERT/UPDATE/DELETE/SELECT)? | TRANSACTION |

### 주의사항

- 이벤트마다 고유한 이름을 태그 식별자로 사용하면 태그 수와 메타데이터가 계속 늘어납니다.
  반복 계측 대상이 없는 이벤트는 LOG 테이블을 검토합니다.
- LOG 테이블은 UPDATE와 일반 조건 DELETE가 불가하므로 수정 가능성이 있는 데이터에는 부적합합니다. 보존/정리 목적의 `BEFORE`, `OLDEST`, `EXCEPT` DELETE만 사용합니다.
- TRANSACTION 테이블은 Standard Edition 전용입니다. Cluster Edition 환경에서는 LOOKUP(소규모) 또는 외부 RDBMS를 활용합니다.
- VOLATILE 테이블은 서버 재시작 시 데이터가 소멸됩니다.

## 타입 비교표

### 기능 비교

| 항목 | TAG | LOG | TRANSACTION | VOLATILE | LOOKUP |
|------|-----|-----|-----|----------|--------|
| DDL | `CREATE TAG TABLE` | `CREATE LOG TABLE` | `CREATE TABLE` / `CREATE TRANSACTION TABLE` / `CREATE TXN TABLE` | `CREATE VOLATILE TABLE` | `CREATE LOOKUP TABLE` |
| 주 용도 | 센서·계측값 | 이벤트·로그 | 관계형 업무 | 임시 집계 | 코드·기준 |
| INSERT | O | O | O | O | O |
| UPDATE | O (Standard, 태그/BASETIME 조건) | X | O | O | O |
| DELETE | O (BEFORE/조건/전체) | O (BEFORE/OLDEST/EXCEPT/전체) | O | O (PK 일치/전체) | O (일반 조건식/전체 삭제) |
| PRIMARY KEY | 필수 | X | 선택 | 선택 | 필수 |
| BASETIME | 필수 (시간축) | X | X | X | X |
| _arrival_time | X | 자동 추가 | X | X | X |
| 인덱스 | 태그·축 접근, 지원되는 보조 인덱스 | BITMAP/KEYWORD/LSM | BTREE PK + 보조 인덱스 | 키·보조 인덱스 | 키·보조 인덱스 |
| 영속성 | O | O | O | X (메모리) | O |
| Cluster Edition | O | O | X | O | O |

Append API는 테이블뿐 아니라 SDK와 입력 경로에 따라 지원 범위가 달라집니다.
SDK Append 지원표에서
사용하는 드라이버와 테이블 조합을 확인합니다.

### 스토리지 특성

| 항목 | TAG | LOG | TRANSACTION | VOLATILE | LOOKUP |
|------|-----|-----|-----|----------|--------|
| 스토리지 | 컬럼형 | 컬럼형 | 행 기반 (관계형) | 메모리 | 영속 저장 + 전체 행 메모리 상주 |
| 용량 검토 기준 | 태그 수·원본·ROLLUP·보관 기간 | 원본·검색 인덱스·보관 기간 | 행·인덱스·트랜잭션 부하 | 전체 행·인덱스의 메모리 크기 | 전체 행·인덱스의 메모리 크기와 재시작 적재 시간 |

메모리 테이블의 “작다”는 고정 행 수를 의미하지 않습니다. 행 폭, 가변 길이 값과 보조
인덱스를 포함해 실제 메모리 사용량을 측정합니다. 디스크 기반 테이블도 압축률이나
서버 사양만으로 처리량을 보장할 수 없으므로 대표 입력과 조회를 함께 실행합니다.

### TRANSACTION 테이블 제약

TRANSACTION 테이블은 다음 제약이 있습니다.

- **Cluster Edition 미지원**: Standard Edition 전용
- **최소 컬럼 수**: 1개 이상

## TRANSACTION vs LOOKUP 비교

TRANSACTION 테이블과 LOOKUP 테이블은 모두 관계형 데이터를 저장하지만, 대상 규모와 기능에 차이가 있습니다.

### 비교표

| 항목 | TRANSACTION 테이블 | LOOKUP 테이블 |
|------|-----------|--------------|
| DDL | `CREATE TRANSACTION TABLE` | `CREATE LOOKUP TABLE` |
| PRIMARY KEY | 선택 | 필수 |
| INSERT | O | O |
| UPDATE (WHERE 포함) | O | O |
| UPDATE (WHERE 없음) | O (전체 행) | X |
| DELETE | O | O |
| 명시적 트랜잭션 | 여러 문장을 COMMIT/ROLLBACK으로 제어 | 참여하지 않음, 문장별 변경 |
| 인덱스 | BTREE PK + 보조 인덱스 | 메모리 키·보조 인덱스 |
| 데이터 규모 | 디스크 용량과 트랜잭션 부하로 검증 | 참조 데이터 조회·갱신 부하로 검증 |
| JOIN 대상 | O | O |
| Cluster Edition | X | O |

### 선택 가이드

**TRANSACTION 테이블을 선택하는 경우**
- 명시적 트랜잭션과 관계형 DML이 필요한 데이터
- UPDATE·DELETE·INSERT·SELECT가 모두 필요한 일반 관계형 워크로드
- PRIMARY KEY 없이 다양한 컬럼 조합으로 조회하는 경우
- Standard Edition 환경

**LOOKUP 테이블을 선택하는 경우**
- 코드 테이블과 기준 정보
- PRIMARY KEY 조회와 단건 UPDATE/DELETE가 필요한 경우
- Cluster Edition 환경에서도 사용해야 하는 경우
- 실시간 기준 정보 갱신이 필요한 경우

### 예시

```sql
-- LOOKUP: 국가 코드 테이블 (PK 조회와 조건 기반 UPDATE)
CREATE LOOKUP TABLE country_code (
    code   VARCHAR(4)   PRIMARY KEY,
    name   VARCHAR(64)
);
INSERT INTO country_code VALUES ('KR', 'Republic of Korea');
UPDATE country_code SET name = 'Korea' WHERE code = 'KR';
SELECT code, name FROM country_code WHERE code = 'KR';

-- TRANSACTION: 주문 이력 (대규모, 일반 UPDATE/DELETE 지원)
CREATE TRANSACTION TABLE order_history (
    order_id  LONG PRIMARY KEY,
    item_id   INTEGER,
    qty       INTEGER,
    amount    DECIMAL(18,2)
);
INSERT INTO order_history VALUES (12345, 501, 1, 12000.00);
UPDATE order_history SET qty = 10 WHERE order_id = 12345;
SELECT order_id, qty, amount FROM order_history WHERE order_id = 12345;
DELETE FROM order_history WHERE order_id = 12345;
SELECT COUNT(*) FROM order_history WHERE order_id = 12345;
```

첫 SELECT는 변경된 국가명을, 주문 SELECT는 수량 `10`을 반환합니다. 마지막 COUNT는
`0`입니다. 이 예제의 `amount`는 수량 변경과 별도로 유지하는 예시 금액이며 자동 재계산되지
않습니다. 실제 주문 모델에서는 단가·수량·합계의 관계와 함께 변경할 컬럼을 명시합니다.
실습을 끝내면 이 예제에서 만든 테이블만 `DROP TABLE`로 정리합니다.
