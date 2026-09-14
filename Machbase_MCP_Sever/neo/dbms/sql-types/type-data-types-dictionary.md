# 데이터 타입 사전

Machbase에서 지원하는 SQL 데이터 타입을 설명합니다.

타입은 저장할 값의 범위와 정밀도에 맞춰 선택합니다. 정수의 최솟값 또는 최댓값처럼
NULL 표현에 예약된 값은 일반 데이터로 사용할 수 없습니다. 아래 표의 `NULL 값`은 내부
표현이며, SQL에서는 `NULL`을 입력하고 `IS NULL`로 검사합니다.

## 데이터 타입 요약

| 타입 | 크기 | 값 범위 | NULL 값 |
|------|------|---------|---------|
| `SHORT` | 2 bytes | -32,767 ~ 32,767 | -32,768 |
| `USHORT` | 2 bytes | 0 ~ 65,534 | 65,535 |
| `INTEGER` | 4 bytes | -2,147,483,647 ~ 2,147,483,647 | -2,147,483,648 |
| `UINTEGER` | 4 bytes | 0 ~ 4,294,967,294 | 4,294,967,295 |
| `LONG` | 8 bytes | -9,223,372,036,854,775,807 ~ 9,223,372,036,854,775,807 | -9,223,372,036,854,775,808 |
| `ULONG` | 8 bytes | 0 ~ 18,446,744,073,709,551,614 | 18,446,744,073,709,551,615 |
| `FLOAT` | 4 bytes | 32비트 단정밀도 부동소수점 | 양수 최대값 |
| `DOUBLE` | 8 bytes | 64비트 배정밀도 부동소수점 | 양수 최대값 |
| `DECIMAL(M,D)` | precision에 따라 가변 | exact fixed-point, M: 1~65, D: 0~30 | - |
| `ARRAY` | 요소 타입과 cardinality에 따라 가변 | 고정 길이 1차원 숫자 배열, cardinality 1~1024 | whole NULL과 element NULL 구분 |
| `DATETIME` | 8 bytes | 1970-01-01 ~ 2262-04-11 (나노초 정밀도) | - |
| `VARCHAR(n)` | 가변 | 최대 n 바이트 (LOG 선언 범위: 1~32,767) | - |
| `IPV4` | 4 bytes | 0.0.0.0 ~ 255.255.255.255 | - |
| `IPV6` | 16 bytes | 0000:...:0000 ~ FFFF:...:FFFF | - |
| `TEXT` | 가변 | 0 ~ 64MB (전문 검색 인덱스 지원) | - |
| `BINARY` | 가변 | LOG: 0~64MB / TAG: 1~32,767 bytes (고정 길이) | - |
| `JSON` | 가변 | JSON 문서: 1~32,768 bytes / path: 1~512 bytes | - |

---

## 정수 타입

### SHORT

16비트 부호 있는 정수 타입입니다. C의 `int16_t`와 저장 크기는 같지만 최소값
(-32,768)은 NULL 표현으로 예약됩니다. SQL에서는 `INT16` 별칭도 사용할 수 있습니다.

```sql
CREATE LOG TABLE t (c1 SHORT);
INSERT INTO t VALUES (-32767);  -- 유효한 최솟값
INSERT INTO t VALUES (-32768);  -- NULL로 처리됨
```

### USHORT

16비트 부호 없는 정수(`uint16_t`). 최대값(65,535)은 NULL로 인식됩니다.

### INTEGER

32비트 부호 있는 정수 타입입니다. C의 `int32_t`와 저장 크기는 같지만 최소값은 NULL
표현으로 예약됩니다. SQL에서는 `INT32` 또는 `INT` 별칭도 사용할 수 있습니다.

### UINTEGER

32비트 부호 없는 정수(`uint32_t`).

### LONG

64비트 부호 있는 정수 타입입니다. C의 `int64_t`와 저장 크기는 같지만 최소값은 NULL
표현으로 예약됩니다. SQL에서는 `INT64` 별칭도 사용할 수 있습니다.

### ULONG

64비트 부호 없는 정수(`uint64_t`).

---

## 부동소수점 타입

### FLOAT

C 언어의 32비트 부동소수점 타입 `float`와 동일합니다. 양수 최대값은 NULL로 인식됩니다.

### DOUBLE

C 언어의 64비트 부동소수점 타입 `double`과 동일합니다. 양수 최대값은 NULL로 인식됩니다.

---

## 고정소수점 타입

### DECIMAL / NUMERIC

선언한 전체 자릿수와 소수 자릿수 범위에서 10진수를 정확하게 저장하는 고정소수점
타입입니다. 입력값의 소수 자릿수가 선언한 범위를 넘으면 반올림이 발생할 수 있으므로
금액이나 비율을 저장할 때 필요한 자릿수를 먼저 정합니다. `NUMERIC`, `DEC`, `FIXED`,
`NUMBER`는 `DECIMAL`의 별칭입니다.

```sql
CREATE TRANSACTION TABLE invoice (
    id     LONG PRIMARY KEY,
    amount DECIMAL(18,2),
    rate   NUMERIC(7,4)
);
```

`DECIMAL`은 `DECIMAL(10,0)`으로, `DECIMAL(M)`은 `DECIMAL(M,0)`으로 해석합니다. 선언 규칙,
반올림, 인덱스, 집계 및 클라이언트 매핑은 DECIMAL과 NUMERIC 고정소수점 타입을
참고하십시오.

---

## ARRAY 타입

Machbase DBMS 8.7.0은 숫자 요소를 정해진 개수만큼 저장하는 고정 길이 1차원
`ARRAY` 타입을 지원합니다. 요소 타입 뒤에 cardinality를 지정합니다.

```sql
CREATE LOG TABLE sensor_array (
    id INTEGER,
    location DOUBLE[2],
    acceleration FLOAT[3]
);
```

지원 요소 타입, NULL 구분, 입력·조회 문법과 SDK별 표현은
숫자 ARRAY 타입을 참고하십시오.

---

## 날짜/시간 타입

### DATETIME

1970년 1월 1일 자정 이후 경과된 시간의 나노초 값을 내부적으로 저장합니다. 표현 범위는 1970-01-01 00:00:00 000:000:000 ~ 2262-04-11 23:47:16.854:775:807입니다.

- 나노초 단위까지 처리 가능
- 내부 표현: 8바이트 정수 (nanoseconds since epoch)
- 문자열 표현: `YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn`

```sql
-- 문자열에서 DATETIME으로 변환
SELECT TO_DATE('2024-01-15 10:30:00 000:000:000');

-- DATETIME에서 문자열로 변환
SELECT TO_CHAR(ts, 'YYYY-MM-DD HH24:MI:SS') FROM t;
```

---

## 문자열 타입

### VARCHAR(n)

가변 길이 문자열 타입입니다. `n`은 문자 수가 아니라 저장할 수 있는 바이트 수이며,
LOG의 선언 범위는 1~32,767입니다. UTF-8 문자열은 문자에 따라 필요한 바이트 수가 다르므로 한글과
이모지 등을 저장할 때는 실제 인코딩 크기를 고려해 길이를 지정합니다.

```sql
CREATE LOG TABLE t (name VARCHAR(100), description VARCHAR(1000));
```

### TEXT

VARCHAR 크기를 초과하는 대용량 텍스트를 저장하기 위한 타입입니다. 최대 64MB를 저장할 수
있습니다. 텍스트 저장 지원과 KEYWORD 인덱스 지원은 구분하며, 인덱스 사용 가능 여부는
테이블 유형에 따라 다릅니다.

- LOG와 Standard Edition의 TRANSACTION 테이블에서 지원
- LOG 테이블은 KEYWORD 인덱스와 `SEARCH` 연산자로 키워드 검색 가능
- TAG, LOOKUP, VOLATILE 테이블에서는 지원하지 않음

LOG의 TEXT 컬럼 자체에는 ORDER BY·GROUP BY를 적용할 수 없습니다.
단순 성능 권장사항이 아니라 쿼리 검증에서 거부되는 제약입니다.
정렬·집계에 사용할 장치, 오류 코드, 등급 등은 별도 VARCHAR·숫자 컬럼으로 두세요.
TEXT를 VARCHAR로 변경하려고 `MODIFY COLUMN`을 사용하는 것도 지원하지 않습니다.

```sql
CREATE LOG TABLE log_table (ts DATETIME, message TEXT);
-- 키워드 인덱스 생성
CREATE INDEX idx_msg ON log_table (message) INDEX_TYPE KEYWORD;
```

---

## 바이너리 타입

### BINARY

이미지, 문서 등 비정형 바이너리 데이터를 저장하는 타입입니다.

- **LOG 테이블**: 가변 길이, 최대 64MB
- **TRANSACTION 테이블**: 가변 길이 바이너리 값 지원 (Standard Edition)
- **TAG 테이블**: `BINARY(n)` 형식의 고정 길이 변형, 1 ~ 32,767 bytes
- LOOKUP, VOLATILE 테이블에서는 지원하지 않음

TAG 테이블의 `BINARY(n)`:
- `X'...'`, `B'...'`, `O'...'` 리터럴 지원 (소문자 prefix도 지원)
- 기존 호환성을 위해 `'0x...'` 형식도 지원
- 선언된 길이를 초과하면 `ERR-02233` 오류 발생

---

## 네트워크 주소 타입

### IPV4

IPv4 주소를 저장하는 타입입니다. 내부적으로 4바이트를 사용하며 `"0.0.0.0"` ~ `"255.255.255.255"` 범위를 표현합니다.

```sql
CREATE LOG TABLE access_log (ts DATETIME, src_ip IPV4, dst_ip IPV4);
INSERT INTO access_log VALUES (NOW, '192.168.0.1', '10.0.0.1');
SELECT * FROM access_log WHERE src_ip = TO_IPV4('192.168.0.1');
```

### IPV6

IPv6 주소를 저장하는 타입입니다. 내부적으로 16바이트를 사용합니다. 축약 표기도 지원합니다.

- `"::FFFF:1232"` — 선행 0 생략
- `"::FFFF:192.168.0.3"` — IPv4 호환 표기
- `"::192.168.3.1"` — IPv4 호환 표기 (deprecated)

```sql
CREATE LOG TABLE v6_log (ts DATETIME, src_ip IPV6);
INSERT INTO v6_log VALUES (NOW, '21DA:D3:0:2F3B:2AA:FF:FE28:9C5A');
```

---

## JSON 타입

JSON 문서를 저장하는 타입입니다. "Key-Value" 쌍으로 구성된 JSON 데이터를 텍스트 형식으로 저장합니다.

- 데이터 최대 크기: 32,768 bytes
- JSON path 최대 길이: 512 bytes
- TAG, LOG, LOOKUP, TRANSACTION 테이블에서 지원
- VOLATILE 테이블에서는 JSON 컬럼 생성 불가
- LOOKUP 테이블의 JSON 컬럼은 primary key로 사용할 수 없음

```sql
CREATE LOG TABLE sensor_data (
    ts   DATETIME,
    data JSON
);
INSERT INTO sensor_data VALUES (NOW, '{"temp":23.5,"hum":60}');
SELECT data -> 'temp' AS temperature FROM sensor_data;
```

자세한 테이블 타입별 JSON 지원 범위는 JSON 타입의 테이블 타입별 지원 범위를 참고하십시오.

---

## SQL 데이터 타입 매핑

Machbase 데이터 타입과 SQL 표준 타입 및 C 타입의 대응 관계입니다.

| Machbase 타입 | Machbase CLI 타입 | SQL 타입 | C 타입 | C 기본 타입 |
|--------------|------------------|----------|--------|------------|
| `short` | SQL_SMALLINT | SQL_SMALLINT | SQL_C_SSHORT | `int16_t` |
| `ushort` | SQL_USMALLINT | SQL_SMALLINT | SQL_C_USHORT | `uint16_t` |
| `integer` | SQL_INTEGER | SQL_INTEGER | SQL_C_SLONG | `int32_t` |
| `uinteger` | SQL_UINTEGER | SQL_INTEGER | SQL_C_ULONG | `uint32_t` |
| `long` | SQL_BIGINT | SQL_BIGINT | SQL_C_SBIGINT | `int64_t` |
| `ulong` | SQL_UBIGINT | SQL_BIGINT | SQL_C_UBIGINT | `uint64_t` |
| `float` | SQL_FLOAT | SQL_REAL | SQL_C_FLOAT | `float` |
| `double` | SQL_DOUBLE | SQL_FLOAT, SQL_DOUBLE | SQL_C_DOUBLE | `double` |
| `decimal` | SQL_DECIMAL | SQL_DECIMAL, SQL_NUMERIC | SQL_C_NUMERIC | decimal-preserving value |
| `datetime` | SQL_TIMESTAMP | SQL_TYPE_TIMESTAMP | SQL_C_TYPE_TIMESTAMP | `char *` (YYYY-MM-DD ...) |
| `varchar` | SQL_VARCHAR | SQL_VARCHAR | SQL_C_CHAR | `char *` |
| `ipv4` | SQL_IPV4 | SQL_VARCHAR | SQL_C_CHAR | `char *` (IP 문자열) |
| `ipv6` | SQL_IPV6 | SQL_VARCHAR | SQL_C_CHAR | `char *` (IP 문자열) |
| `text` | SQL_TEXT | SQL_LONGVARCHAR | SQL_C_CHAR | `char *` |
| `binary` | SQL_BINARY | SQL_BINARY | SQL_C_BINARY | `char *` |
| `json` | SQL_JSON | SQL_JSON | SQL_C_CHAR | `json_t` |

---

## 테이블 타입별 지원 데이터 타입

| 타입 | TAG | LOG | LOOKUP | VOLATILE | TRANSACTION |
|------|:---:|:---:|:------:|:--------:|:---:|
| SHORT | O | O | O | O | O |
| USHORT | O | O | O | O | O |
| INTEGER | O | O | O | O | O |
| UINTEGER | O | O | O | O | O |
| LONG | O | O | O | O | O |
| ULONG | O | O | O | O | O |
| FLOAT | O | O | O | O | O |
| DOUBLE | O | O | O | O | O |
| DECIMAL / NUMERIC | O | O | O | O | O |
| DATETIME | O | O | O | O | O |
| VARCHAR | O | O | O | O | O |
| IPV4 | O | O | O | O | O |
| IPV6 | O | O | O | O | O |
| TEXT | X | O | X | X | O |
| JSON | O | O | O | X | O |
| BINARY | O (고정 길이) | O | X | X | O |

DECIMAL은 모든 public 테이블 타입에서 지원합니다. TRANSACTION 테이블 자체는 Standard Edition에서
사용하며, Cluster Edition에서는 LOG/TAG 테이블의 DECIMAL 컬럼과 DDL 전파를 지원합니다.
