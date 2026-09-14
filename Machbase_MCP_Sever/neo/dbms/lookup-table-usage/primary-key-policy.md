# PRIMARY KEY 정책

LOOKUP 테이블의 PRIMARY KEY 설계 원칙과 정책을 다룹니다. SDK가 SELECT 결과에서 PK 여부를
확인하는 방법은 PRIMARY KEY 메타데이터 지원 범위를
참고합니다.

## PRIMARY KEY 설계

LOOKUP 테이블은 `PRIMARY KEY`가 필수입니다. PRIMARY KEY는 행을 고유하게 식별하고 중복 입력을
제어합니다. UPDATE와 DELETE의 `WHERE` 절에는 일반 조건식을 사용할 수 있지만, Primary key
컬럼 자체는 UPDATE할 수 없습니다.

### 기본 문법

```text
CREATE LOOKUP TABLE table_name (
    pk_col   type    PRIMARY KEY,
    col2     type,
    ...
);
```

### 단일 컬럼 PRIMARY KEY

```sql
CREATE LOOKUP TABLE ch9_pk_country_code (
    code     VARCHAR(4)  PRIMARY KEY,
    name     VARCHAR(64),
    region   VARCHAR(32)
);
```

### 복합 키가 필요한 경우

```sql
CREATE LOOKUP TABLE ch9_pk_price (
    price_key  VARCHAR(64) PRIMARY KEY,
    product_id VARCHAR(32),
    region     VARCHAR(16),
    price      DOUBLE
);

-- 삽입
INSERT INTO ch9_pk_price VALUES ('PROD-01:KR', 'PROD-01', 'KR', 99.0);
INSERT INTO ch9_pk_price VALUES ('PROD-01:US', 'PROD-01', 'US', 79.0);

-- 조합 키 기반 UPDATE
UPDATE ch9_pk_price SET price = 89.0
WHERE price_key = 'PROD-01:KR';
```

LOOKUP 테이블은 PRIMARY KEY 컬럼을 하나만 지정할 수 있습니다. 여러 컬럼의 조합이
비즈니스 키라면 조합 문자열 또는 대리키를 별도 PRIMARY KEY 컬럼으로 둡니다.

### PRIMARY KEY 타입 선택

| 타입 | 장점 | 단점 |
|------|------|------|
| `VARCHAR(n)` | 가독성, 의미 있는 키 | 문자열 비교 비용 |
| `INTEGER` / `LONG` | 비교 빠름, 저장 효율 | 의미 없음, 별도 매핑 필요 |

### 주의사항

- PRIMARY KEY 값은 중복될 수 없습니다.
- PRIMARY KEY 값은 변경할 수 없습니다 (변경 시 DELETE + INSERT).
- PRIMARY KEY 컬럼에는 인덱스가 자동 생성됩니다.
- PRIMARY KEY 컬럼은 하나만 지정합니다.

## PRIMARY KEY 선택 정책

PRIMARY KEY 설계 시 고려할 정책과 모범 사례입니다.

### 자연키 vs 대리키

#### 자연키 (Natural Key)

비즈니스 의미를 갖는 값을 그대로 PRIMARY KEY로 사용합니다.

```sql
-- 국가 코드: 표준화된 자연키
CREATE LOOKUP TABLE ch9_pk_country (
    iso_code VARCHAR(4) PRIMARY KEY,  -- ISO 3166-1 alpha-2
    name     VARCHAR(64)
);
```

**장점**: 의미 파악 쉬움, 별도 조회 불필요
**단점**: 키 변경 시 참조 무결성 문제

#### 대리키 (Surrogate Key)

SEQUENCE 컬럼이나 UUID처럼 의미 없는 값을 PRIMARY KEY로 사용합니다.

```sql
-- 설비 마스터: 대리키
CREATE LOOKUP TABLE ch9_pk_equip (
    equip_id  LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    code      VARCHAR(32),          -- 비즈니스 키
    name      VARCHAR(128)
);
CREATE INDEX ch9_pk_equip_idx ON ch9_pk_equip(code);
```

**장점**: 불변, 조인 효율적
**단점**: 코드-ID 변환 필요

### PRIMARY KEY 불변 원칙

PRIMARY KEY 값은 UPDATE할 수 없습니다. 변경이 필요하면 DELETE + INSERT를 사용합니다.

```sql
-- 잘못된 패턴 (PK 변경은 DELETE + INSERT로)
-- UPDATE는 PK 변경 불가

-- 올바른 패턴
DELETE FROM ch9_pk_country WHERE iso_code = 'OLD';
INSERT INTO ch9_pk_country VALUES ('NEW', '새 국가명');
```

LOOKUP 테이블 DML은 개별 문장 단위로 실행합니다. `BEGIN`/`COMMIT`으로 묶는 TRANSACTION
트랜잭션에는 LOOKUP DML을 포함할 수 없습니다.

따라서 두 문장 사이의 조회와 삽입 실패에 대비해야 합니다. 기존 값을 보관하고 참조하는
키의 전환 순서를 정한 뒤 변경하며, 전체 변경의 원자성이 필요하면 TRANSACTION 테이블을
검토합니다.

이 페이지의 실습 테이블은 다음과 같이 정리합니다.

```sql
DROP INDEX ch9_pk_equip_idx;
DROP TABLE ch9_pk_equip;
DROP TABLE ch9_pk_country;
DROP TABLE ch9_pk_price;
DROP TABLE ch9_pk_country_code;
```
