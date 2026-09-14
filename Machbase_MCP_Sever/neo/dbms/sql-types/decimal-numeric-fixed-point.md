# DECIMAL과 NUMERIC 고정소수점 타입

`DECIMAL`은 10진수 값을 오차 없이 저장하는 exact fixed-point 타입입니다. `NUMERIC`, `DEC`,
`FIXED`, `NUMBER`는 `DECIMAL`의 alias이며 `DESC`, `SHOW`와 결과 메타데이터에서는 canonical
이름인 `DECIMAL`로 표시됩니다. `NUMBER`는 MySQL alias가 아닌 Machbase 호환 확장 alias입니다.

## 선언 문법

```sql
DECIMAL
DECIMAL(precision)
DECIMAL(precision, scale)

NUMERIC
NUMERIC(precision)
NUMERIC(precision, scale)
```

| 선언 | 해석 |
|------|------|
| `DECIMAL` | `DECIMAL(10,0)` |
| `DECIMAL(M)` | `DECIMAL(M,0)` |
| `DECIMAL(M,D)` | precision `M`, scale `D` |

- precision은 전체 유효 숫자 수이며 `1`부터 `65`까지 지정합니다.
- scale은 소수점 이하 숫자 수이며 `0`부터 `30`까지 지정합니다.
- scale은 precision보다 클 수 없습니다.
- `UNSIGNED`와 `ZEROFILL`은 지원하지 않습니다.

```sql
CREATE TRANSACTION TABLE invoice (
    invoice_id LONG PRIMARY KEY,
    amount     DECIMAL(18,2),
    tax_rate   NUMERIC(7,4)
);
```

## 반올림과 범위 초과

입력 값의 소수 자릿수가 scale을 초과하면 0에서 멀어지는 방향의 절반 올림
(round-half-away-from-zero)을 적용합니다.

```sql
CREATE TRANSACTION TABLE decimal_rounding (
    id     INTEGER PRIMARY KEY,
    amount DECIMAL(5,2)
);

INSERT INTO decimal_rounding VALUES (1, 1.235);   -- 1.24
INSERT INTO decimal_rounding VALUES (2, -1.235);  -- -1.24
```

precision을 초과하는 값은 잘라내거나 부동소수점으로 변환하지 않고 오류로 처리합니다.
`DECIMAL`의 NULL은 특정 숫자 값을 sentinel로 사용하지 않고 값과 별도로 관리합니다.

## 테이블 타입별 지원

| 테이블 타입 | DECIMAL 컬럼 | 주요 사용 위치 |
|------------|:------------:|----------------|
| LOG | O | 금액·정산 이벤트, exact 집계 |
| TAG | O | exact 계측값과 집계 대상 데이터 컬럼 |
| VOLATILE | O | 상태·캐시 값, primary key |
| LOOKUP | O | 기준 금액·비율, primary key와 보조 인덱스 |
| TRANSACTION | O | 관계형 업무 데이터, PK/UNIQUE/일반 인덱스 |

```sql
CREATE LOG TABLE payment_log (
    occurred_at DATETIME,
    amount      DECIMAL(18,2)
);

CREATE TAG TABLE meter_value (
    name   VARCHAR(80) PRIMARY KEY,
    time   DATETIME BASETIME,
    value  DECIMAL(24,6)
);

CREATE VOLATILE TABLE exchange_cache (
    rate_key DECIMAL(12,6) PRIMARY KEY,
    label    VARCHAR(32)
);

CREATE LOOKUP TABLE price_rule (
    rule_id LONG PRIMARY KEY,
    amount  DECIMAL(18,2)
);
```

Cluster Edition에서는 LOG/TAG 테이블의 DECIMAL 컬럼과 DDL 전파를 지원합니다. TRANSACTION 테이블은
DECIMAL 타입과 무관하게 Standard Edition에서 사용합니다.

## 비교와 인덱스

모든 테이블 엔진은 동일한 DECIMAL 비교 규칙을 사용합니다. 표현 scale이 달라도 수치가 같으면
동일한 값으로 비교합니다.

```sql
-- 1, 1.0, 1.00은 equality, PK, UNIQUE 비교에서 같은 값입니다.
SELECT * FROM price_rule WHERE amount = 1.00;
```

VOLATILE과 LOOKUP의 primary key 메모리 인덱스, TRANSACTION 테이블의 일반·UNIQUE·PRIMARY KEY 인덱스에서
DECIMAL을 사용할 수 있습니다. TRANSACTION 인덱스는 equality, range, ordering에 같은 수치 순서를
적용합니다.

VIEW의 derived column도 DECIMAL precision과 scale을 유지합니다. `DESC`, `SHOW`,
`M$SYS_COLUMNS`와 클라이언트 result metadata에서 precision과 scale을 각각 확인할 수 있습니다.

## 식과 집계 함수

`+`, `-`, `*`, `/`, `ROUND`, `TRUNC`, CAST와 다음 집계·정렬 연산에서
DECIMAL 값을 사용할 수 있습니다.

- `SUM`, `AVG`, `MIN`, `MAX`
- `GROUP BY`, `ORDER BY`, `DISTINCT`

exact DECIMAL 경로가 없는 고급 통계 함수, percentile, `TOP_K` 등은 DECIMAL 값을 DOUBLE로
변환해 계산하므로 결과가 근삿값일 수 있습니다.

## 입출력과 클라이언트 매핑

machloader의 `.fmt`, CSV import/export와 Append 경로는 부호, NULL, precision과 scale을
보존합니다. 부동소수점 타입을 경유하지 않고 문자열 또는 각 언어의 decimal 타입으로
전달하십시오.

| 인터페이스 | 권장 매핑 |
|-----------|-----------|
| ODBC | `SQL_DECIMAL` / `SQL_NUMERIC`, `SQL_C_NUMERIC` |
| JDBC | `java.math.BigDecimal` |
| Python | `decimal.Decimal` |
| Node.js | decimal-compatible 문자열 또는 connector의 decimal 표현 |
| .NET | `decimal`, `DbType.Decimal` |

Go에서 NUMERIC 값을 처리할 때도 `float64`로 변환하지 말고 connector가 제공하는
decimal-preserving 값 또는 문자열 표현을 사용합니다.

## 타입 선택

- 통화, 세율, 정산값처럼 10진수 정확성이 필요하면 `DECIMAL`을 사용합니다.
- 센서 실수처럼 근삿값과 넓은 지수 범위가 중요하면 `FLOAT` 또는 `DOUBLE`을 사용합니다.
- 저장·비교·연산 중 DECIMAL 값을 DOUBLE로 변환하면 exact fixed-point 의미가 사라집니다.
