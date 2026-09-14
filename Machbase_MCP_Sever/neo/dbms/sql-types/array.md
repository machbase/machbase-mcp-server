# 숫자 ARRAY 타입

Machbase DBMS 8.7.0은 같은 숫자 타입의 값을 정해진 개수만큼 저장하는 고정 길이
1차원 `ARRAY` 타입을 지원합니다. 센서의 좌표, 축별 측정값처럼 하나의 행에 여러 숫자
값을 함께 저장하고 요소별로 조회할 때 사용합니다.

일부 위치만 입력하는 방법과 선택 컬럼 Append API는
Sparse ARRAY와 선택 컬럼 Append API를
참고하십시오.

## 지원 타입과 선언 범위

컬럼을 선언할 때 숫자 요소 타입 뒤에 `[cardinality]`를 붙입니다. cardinality는 배열에
저장할 요소 개수이며, 각 행에서 NULL이 아닌 요소의 개수가 아니라 컬럼에 선언한 고정
길이를 뜻합니다. 배열 전체가 없는 상태(whole NULL)와 배열 안의 특정 값만 없는 상태
(element NULL)는 서로 구분합니다.

| 요소 타입 | DDL 예 | 설명 |
|---|---|---|
| `INT16` | `INT16[4]` | signed 16-bit 정수 |
| `UINT16` | `UINT16[4]` | unsigned 16-bit 정수 |
| `INT32` | `INT32[4]` | signed 32-bit 정수 |
| `UINT32` | `UINT32[4]` | unsigned 32-bit 정수 |
| `INT64` | `INT64[4]` | signed 64-bit 정수 |
| `UINT64` | `UINT64[4]` | unsigned 64-bit 정수 |
| `FLOAT` | `FLOAT[4]` | 단정밀도 부동소수점 |
| `DOUBLE` | `DOUBLE[4]` | 배정밀도 부동소수점 |
| `DECIMAL(p,s)` | `DECIMAL(12,4)[4]` | 고정소수점 숫자 |

- cardinality 범위는 `1..1024`입니다.
- `DECIMAL` precision 범위는 `1..65`입니다.
- `DECIMAL` scale 범위는 `0..30`이며 precision보다 클 수 없습니다.

다음 별칭은 해당 대표 요소 타입으로 처리됩니다.

| 별칭 | 대표 타입 |
|---|---|
| `SHORT` | `INT16` |
| `USHORT` | `UINT16` |
| `INT`, `INTEGER` | `INT32` |
| `UINTEGER` | `UINT32` |
| `LONG` | `INT64` |
| `ULONG` | `UINT64` |
| `NUMERIC`, `DEC`, `FIXED`, `NUMBER` | `DECIMAL` |

## 테이블 생성과 컬럼 추가

다음 예제는 네 개의 채널 값, 세 개의 누적값, 두 개의 고정소수점 값을 저장합니다.

```sql
CREATE LOG TABLE SENSOR_ARRAY
(
    ID       INTEGER,
    CHANNELS DOUBLE[4],
    COUNTERS UINT64[3],
    AMOUNTS  DECIMAL(12,4)[2]
);
```

기존에 `ADD COLUMN`을 지원하는 테이블에는 같은 ARRAY 선언을 사용해 컬럼을 추가하고
기존 `DROP COLUMN` 문법으로 제거할 수 있습니다.

```sql
ALTER TABLE SENSOR_ARRAY
    ADD COLUMN (STATUS_VALUES INT32[3]);

ALTER TABLE SENSOR_ARRAY
    ADD COLUMN (LIMITS DECIMAL(12,4)[2] DEFAULT [0.0000, NULL]);

ALTER TABLE SENSOR_ARRAY
    DROP COLUMN (STATUS_VALUES);

ALTER TABLE SENSOR_ARRAY
    DROP COLUMN (LIMITS);
```

`DECIMAL(12)[2]`처럼 scale을 생략하면 `DECIMAL(12,0)[2]`로 처리합니다.

TAG METADATA ARRAY는 `METADATA ADD COLUMN`과 `METADATA DROP COLUMN`을 사용합니다.

```sql
ALTER TABLE SENSOR_TAG METADATA
    ADD COLUMN (LIMITS DECIMAL(12,4)[2] DEFAULT [0.0000, NULL]);

ALTER TABLE SENSOR_TAG METADATA
    DROP COLUMN (LIMITS);
```

`ARRAY`는 다음 위치의 일반 데이터 컬럼에 사용할 수 있습니다.

- LOG 테이블
- TAG DATA의 일반 DATA 컬럼
- TAG METADATA의 일반 metadata 컬럼
- VOLATILE 테이블
- LOOKUP 테이블
- Standard Edition의 TRANSACTION 테이블

`ARRAY` 추가가 각 테이블의 기존 DML 범위를 넓히지는 않습니다. 예를 들어 LOG 테이블의
`UPDATE`는 계속 지원하지 않으며 TAG 테이블의 `UPDATE`도 기존에 허용된 DATA 또는
METADATA 경로만 사용할 수 있습니다.

### ADD COLUMN 지원 범위

| Edition | 테이블 또는 컬럼 영역 | ARRAY ADD/DROP |
|---|---|:---:|
| Standard | LOG | O |
| Standard | VOLATILE | O |
| Standard | LOOKUP | O |
| Standard | TRANSACTION | O |
| Standard | TAG METADATA | O |
| Standard | TAG DATA 일반 컬럼 | X |
| Cluster | LOG | O |
| Cluster | 그 외 테이블 또는 TAG METADATA | X |

TAG DATA 일반 ARRAY 컬럼은 `CREATE TABLE`에서 선언할 수 있지만 ALTER로 추가할 수
없습니다.

### DEFAULT와 기존 행

- DEFAULT가 없으면 ALTER 전에 존재한 행의 새 ARRAY 컬럼은 전체 NULL입니다.
- LOG, LOOKUP, TRANSACTION과 TAG METADATA에서는 명시한 ARRAY DEFAULT를 기존 행에
  적용합니다.
- VOLATILE은 단일 값 컬럼의 `ADD COLUMN`과 마찬가지로 기존 행을 DEFAULT로 다시 쓰지
  않으므로 새 ARRAY 컬럼은 전체 NULL입니다.
- Cluster LOG는 명시한 ARRAY DEFAULT를 기존 행에 적용합니다.
- DEFAULT 배열 생성식의 요소 수는 선언한 cardinality와 정확히 같아야 합니다.

ALTER 이후에 TAG DATA의 INSERT 또는 Append로 새 태그가 자동 등록되면, 새 메타데이터
행에는 ADD COLUMN의 DEFAULT를 적용하지 않습니다. 추가한 ARRAY 메타데이터 컬럼은
전체 NULL로 생성됩니다. 이 DEFAULT는 ALTER 전에 존재한 메타데이터 행에만 적용됩니다.

다음 역할에는 `ARRAY`를 사용할 수 없습니다.

- PRIMARY KEY, UNIQUE 또는 일반 인덱스 키
- `AUTO_INCREMENT`, `SEQUENCE`
- TAG 테이블의 NAME, BASETIME, BASE DISTANCE, SUMMARIZED 컬럼

TAG METADATA ARRAY 컬럼에는 자동 index를 생성하지 않으며 명시적 index도 지원하지
않습니다.

다음 선언은 지원하지 않습니다.

```sql
INT32[]
INT32[0]
INT32[1025]
VARCHAR[4]
INT32[2][3]
DECIMAL[4](12,4)
```

## ARRAY 값 입력

`ARRAY[...]`와 축약형 `[...]`를 모두 사용할 수 있습니다.

```sql
INSERT INTO SENSOR_ARRAY VALUES
    (1,
     ARRAY[1.5, NULL, 3.5, 4.5],
     [1, NULL, 3],
     [12.3400, NULL]);

INSERT INTO SENSOR_ARRAY VALUES
    (2,
     [10.0, 20.0, 30.0, 40.0],
     [4, 5, 6],
     [1.2500, 2.5000]);

INSERT INTO SENSOR_ARRAY VALUES (3, NULL, NULL, NULL);
```

constructor의 요소 수는 대상 컬럼의 cardinality와 정확히 같아야 합니다. 길이가 다르면
padding하거나 자르지 않고 문장을 실패시킵니다. 빈 `[]`와 `ARRAY[]`도 cardinality가
0인 저장값으로 사용할 수 없습니다.

요소마다 대상 숫자 타입의 변환, 부호, 범위, `DECIMAL` precision과 scale 규칙을
적용합니다. 한 요소라도 변환할 수 없으면 문장 전체가 실패하고 부분 `ARRAY`를 저장하지
않습니다.

### 숫자 범위

정수 타입은 내부 NULL sentinel을 실제 값으로 저장할 수 없습니다.

| 타입 | 저장 가능한 범위 |
|---|---|
| `INT16` | `-32767..32767` |
| `UINT16` | `0..65534` |
| `INT32` | `-2147483647..2147483647` |
| `UINT32` | `0..4294967294` |
| `INT64` | `-9223372036854775807..9223372036854775807` |
| `UINT64` | `0..18446744073709551614` |

`FLOAT`와 `DOUBLE`의 예약된 최대 finite NULL sentinel 값도 실제 요소로 저장할 수
없습니다. 그보다 큰 입력의 Infinity 처리는 대응 scalar 타입과 동일합니다.

### 대상이 없는 ARRAY 타입 추론

`SELECT [1,2,3]`처럼 대상 컬럼이 없는 문맥에서는 전체 요소에서 공통 타입을 추론합니다.

- 모든 non-NULL 요소가 같은 타입이면 그 타입을 유지합니다.
- signed와 unsigned 정수는 모든 값을 담을 수 있는 가장 작은 정수 타입으로 승격합니다.
- signed 정수와 `UINT64`가 함께 있으면 `DECIMAL(20,0)`을 사용합니다.
- `DECIMAL`끼리는 필요한 정수 자릿수와 scale을 합칩니다.
- `FLOAT`만 있으면 `FLOAT`를 유지하고 다른 숫자 타입과 혼합하면 `DOUBLE`로 승격합니다.
- 빈 배열, 모든 요소가 NULL인 배열, 숫자가 아닌 요소 또는 중첩 배열은 추론 오류입니다.

INSERT, UPDATE 또는 prepared parameter처럼 대상 컬럼이 있으면 대상 컬럼의 요소 타입,
cardinality와 `DECIMAL` 메타데이터로 각 요소를 검증합니다.

### whole NULL과 element NULL

`ARRAY` 자체의 NULL과 NULL 요소를 가진 `ARRAY`는 서로 다른 값입니다.

```sql
-- ARRAY 자체가 NULL입니다.
INSERT INTO SENSOR_ARRAY (ID, CHANNELS) VALUES (10, NULL);

-- ARRAY는 존재하며 네 요소가 모두 NULL입니다.
INSERT INTO SENSOR_ARRAY (ID, CHANNELS)
VALUES (11, [NULL, NULL, NULL, NULL]);
```

`NOT NULL`은 `ARRAY` 전체의 NULL만 제한합니다. 따라서 모든 요소가 NULL인 `ARRAY`는
`NOT NULL` 컬럼에도 입력할 수 있습니다.

## 요소 조회

요소 위치는 0부터 시작합니다. cardinality가 4이면 유효한 위치는 `0..3`입니다.

```sql
SELECT CHANNELS,
       CHANNELS[0] AS FIRST_CHANNEL,
       CHANNELS[3] AS LAST_CHANNEL,
       CHANNELS[4] AS OUT_OF_RANGE
  FROM SENSOR_ARRAY;
```

다음 경우에는 오류 대신 SQL `NULL`을 반환합니다.

- 인덱스가 음수 또는 cardinality 이상인 경우
- 인덱스 표현식이 SQL NULL인 경우
- `ARRAY` 전체가 NULL인 경우
- 해당 요소가 NULL인 경우

> **주의**
> 요소 위치를 나타내는 `[위치]`는 따옴표로 감싸지 않은 단순 컬럼명 뒤에만 붙일 수 있습니다.
> `A[0]`은 가능하지만
> `T.A[0]`과 `"A"[0]`은 지원하지 않습니다.

## ARRAY_LENGTH

`ARRAY_LENGTH()`는 배열 전체가 NULL이 아니면 선언한 요소 개수(cardinality)를 반환합니다.

```sql
SELECT ID, ARRAY_LENGTH(CHANNELS)
  FROM SENSOR_ARRAY;
```

모든 요소가 NULL이어도 cardinality를 반환합니다. whole NULL은 NULL을 반환합니다.
타입 정보가 없는 `ARRAY_LENGTH(NULL)`은 인자 타입을 결정할 수 없으므로 오류입니다.

## ARRAY 전체 CAST

같은 cardinality의 숫자 `ARRAY`는 `CAST(array_expression AS TYPE[N])`로 요소 타입을
전체 변환할 수 있습니다.

```sql
SELECT CAST(CHANNELS AS INT32[4])
  FROM SENSOR_ARRAY;

SELECT CAST(AMOUNTS AS DECIMAL(10,2)[2])
  FROM SENSOR_ARRAY;
```

- 입력은 숫자 `ARRAY` 또는 SQL `NULL`이어야 합니다.
- 대상에는 이 문서의 숫자 요소 타입과 별칭을 사용할 수 있습니다.
- 입력과 대상 cardinality는 정확히 같아야 합니다.
- whole NULL과 각 element NULL은 변환 뒤에도 유지됩니다.
- 각 non-NULL 요소에는 대응하는 scalar CAST의 숫자 변환 규칙을 적용합니다.
- `DECIMAL[N]`은 `DECIMAL(10,0)[N]`, `DECIMAL(p)[N]`은 `DECIMAL(p,0)[N]`으로
  처리합니다.
- 한 요소라도 범위나 변환 규칙을 위반하면 CAST와 이를 포함한 문장 전체가 실패합니다.

준비된 문장(prepared statement)에서는 CAST 대상이 매개변수와 결과의 요소 타입,
cardinality, DECIMAL의 전체·소수 자릿수를 결정합니다. 같은 문장에 ARRAY 값, 전체 NULL,
일부 위치만 지정한 sparse ARRAY를 다시 바인딩할 수 있습니다.

```sql
SELECT CAST(? AS INT32[3]);
SELECT CAST(? AS DECIMAL(12,4)[3]);
```

`CASE`와 `UNION ALL`에서 ARRAY 결과를 결합하려면 요소 타입, cardinality와 DECIMAL
precision/scale이 모두 같아야 합니다. 서로 다르면 명시적으로 같은 ARRAY 타입으로
CAST한 뒤 결합합니다.

다음 변환은 지원하지 않습니다.

- scalar 값을 ARRAY로 확장
- ARRAY를 scalar로 축소
- 서로 다른 cardinality 사이의 padding 또는 truncation
- 문자열, 날짜, IP, BINARY, JSON ARRAY 대상

전체 문법, 숫자 변환과 오류 규칙은
CAST 함수를 참고하십시오.

## 비교와 표현식

`ARRAY` 전체에 `=`, `<>`, `IS NULL`, `IS NOT NULL`을 사용할 수 있습니다. 같은 위치의
NULL 요소끼리는 전체 `ARRAY` 동등 비교에서 일치합니다. whole NULL 비교는 일반 SQL
NULL 규칙을 따릅니다.

```sql
SELECT ID
  FROM SENSOR_ARRAY
 WHERE CHANNELS = [1.5, NULL, 3.5, 4.5]
    OR CHANNELS[1] IS NULL;
```

요소 표현식은 해당 숫자 타입의 일반 표현식과 조건식에 사용할 수 있습니다. 반면 전체
`ARRAY`를 다음 위치에 사용하는 기능은 지원하지 않습니다.

- `DISTINCT`
- `GROUP BY`
- `ORDER BY`
- 집계 함수의 DISTINCT 인자

## VIEW, INSERT SELECT, CASE와 upsert

VIEW와 `INSERT ... SELECT`는 요소 타입, cardinality, `DECIMAL` precision과 scale을
보존합니다. 서로 다른 숫자 `ARRAY` 타입으로 입력하면 요소마다 대상 타입으로 변환하고,
한 요소라도 변환할 수 없으면 문장 전체가 실패합니다.

INSERT와 UPDATE의 `CASE` 결과에도 대상 `ARRAY` 계약을 적용합니다.

```sql
UPDATE SENSOR_LOOKUP
   SET AMOUNTS = CASE WHEN ID = 1
                     THEN [12345678.1234, NULL]
                     ELSE AMOUNTS
                 END
 WHERE ID = 1;
```

LOOKUP 또는 VOLATILE 테이블의 duplicate-key upsert에서도 direct `ARRAY`, 상수 `CASE`,
prepared whole-ARRAY bind에 같은 변환 규칙을 적용합니다. upsert의 오른쪽 식에서 기존 행
컬럼을 참조할 수 있는지는 각 테이블의 기존 정책을 따릅니다.

## 메타데이터와 표시 형식

`DESC`와 SQL export에는 canonical 선언을 표시합니다.

```sql
DESC SENSOR_ARRAY;
```

시스템 카탈로그는 `ARRAY` type code, cardinality, precision과 scale을 개별 필드로
보존합니다. SQLCLI 또는 ODBC의 `SQLColumns()`는 다음 정보를 반환합니다.

- `DATA_TYPE`: `SQL_MACHBASE_ARRAY`
- `TYPE_NAME`: `INT32[3]`, `DECIMAL(12,4)[2]` 같은 canonical 선언
- `COLUMN_SIZE`: cardinality
- `DECIMAL_DIGITS`: `DECIMAL` 요소의 scale

`machsql`, 범용 ODBC text 조회와 Go `database/sql`처럼 문자열 결과가 필요한 경로는
`[value,null,value]` 형식을 사용합니다. 소문자 `null`은 element NULL이며 컬럼 결과의
SQL `NULL`은 whole NULL입니다.

## SDK에서 ARRAY 읽기와 쓰기

다음 예제는 공통 테이블과 데이터를 사용합니다.

```sql
CREATE LOG TABLE SDK_ARRAY_SAMPLE
(
    ID INTEGER,
    A_I32 INT32[3],
    A_U64 UINT64[3],
    A_DEC DECIMAL(12,4)[3]
);

INSERT INTO SDK_ARRAY_SAMPLE VALUES
    (1,
     [1,NULL,-3],
     [1,NULL,18446744073709551614],
     [1.2500,NULL,-3.7500]);
INSERT INTO SDK_ARRAY_SAMPLE (ID) VALUES (2);
```

whole NULL은 각 SDK의 NULL 값으로 표현하고 element NULL은 collection 내부의 NULL 값으로
표현합니다. `UINT64`와 `DECIMAL`은 SDK가 제공하는 정밀도 보존 타입을 사용해야 합니다.

### C SQLCLI

typed fetch에는 `SQL_C_MACHBASE_ARRAY`와 `SQL_MACHBASE_ARRAY_DESC`를 사용합니다.

```c
SQLINTEGER values[3] = {0};
SQLLEN elements[3] = {0};
SQLLEN outer = 0;
SQL_MACHBASE_ARRAY_DESC array = {0};

array.struct_size = sizeof(array);
array.element_c_type = SQL_C_SLONG;
array.capacity = 3;
array.values = values;
array.element_indicators = elements;

SQLExecDirect(stmt,
    (SQLCHAR*)"SELECT A_I32 FROM SDK_ARRAY_SAMPLE WHERE ID=1", SQL_NTS);
SQLBindCol(stmt, 1, SQL_C_MACHBASE_ARRAY, &array, sizeof(array), &outer);
SQLFetch(stmt);
/* outer != SQL_NULL_DATA, array.count == 3,
 * values[0] == 1, elements[1] == SQL_NULL_DATA, values[2] == -3 */
```

whole NULL이면 `outer == SQL_NULL_DATA`이고 `array.count == 0`입니다. NULL 요소를
구분하려면 `element_indicators`를 제공해야 합니다. `DECIMAL`을 문자열로 받을 때는
`element_c_type = SQL_C_CHAR`와 요소 버퍼 간 `value_stride`를 설정합니다.

prepared INSERT는 `capacity`, `count`, `ColumnSize`를 대상 cardinality로 설정합니다.

```c
array.count = 3;
SQLPrepare(stmt,
    (SQLCHAR*)"INSERT INTO SDK_ARRAY_SAMPLE(ID,A_I32) VALUES(3,?)", SQL_NTS);
SQLBindParameter(stmt, 1, SQL_PARAM_INPUT,
    SQL_C_MACHBASE_ARRAY, SQL_MACHBASE_ARRAY, 3, 0,
    &array, sizeof(array), &outer);
SQLExecute(stmt);
```

전체 NULL 입력은 `outer = SQL_NULL_DATA`로 지정합니다. ARRAY parameter-set execute는
현재 지원하지 않으며 `HYC00`을 반환합니다. 기존 `SQLAppendBatch`도 ARRAY type code가
없어 ARRAY를 지원하지 않지만 동일한 SQLSTATE를 계약하지는 않습니다.

### C++

C++은 SQLCLI descriptor ABI를 그대로 사용합니다. bind부터 fetch가 끝날 때까지
`vector`의 주소가 바뀌지 않도록 크기를 고정합니다.

```cpp
std::vector<SQLINTEGER> values(3);
std::vector<SQLLEN> indicators(3);
SQLLEN outer = 0;
SQL_MACHBASE_ARRAY_DESC array{};
array.struct_size = sizeof(array);
array.element_c_type = SQL_C_SLONG;
array.capacity = values.size();
array.values = values.data();
array.element_indicators = indicators.data();

SQLBindCol(stmt, 1, SQL_C_MACHBASE_ARRAY,
           &array, sizeof(array), &outer);
```

애플리케이션 모델에서는 whole NULL을
`std::optional<std::vector<std::optional<T>>>`의 바깥 `optional`, element NULL을
안쪽 `optional`로 표현할 수 있습니다.

### Machbase ODBC와 범용 ODBC

Machbase 전용 header를 사용하는 ODBC C 프로그램은 C SQLCLI와 같은 ARRAY descriptor를
사용합니다. 전용 타입을 해석하지 않는 범용 도구는 canonical text로 조회하거나 요소를
각각 projection합니다.

```sql
SELECT ID, A_I32, A_I32[1], A_I32[2], A_I32[3]
  FROM SDK_ARRAY_SAMPLE
 ORDER BY ID;
```

### JDBC

JDBC는 `java.sql.Array`를 반환합니다. `UINT64`는 `BigInteger`, `DECIMAL`은
`BigDecimal`로 보존합니다.

```java
try (Connection con = DriverManager.getConnection(
         "jdbc:machbase://127.0.0.1:5656/machbasedb", "SYS", "MANAGER");
     Statement st = con.createStatement();
     ResultSet rs = st.executeQuery(
         "SELECT A_I32 FROM SDK_ARRAY_SAMPLE ORDER BY ID")) {
    rs.next();
    java.sql.Array sqlArray = rs.getArray(1);
    Object[] values = (Object[])sqlArray.getArray();
    // [Integer(1), null, Integer(-3)]
    rs.next();
    assert rs.getArray(1) == null && rs.wasNull();
}
```

metadata의 JDBC type은 `Types.ARRAY`, precision은 cardinality, `DECIMAL` scale은 요소
scale입니다. `Connection.createArrayOf()`로 만든 값을 `PreparedStatement.setArray()`에
전달할 수 있습니다.

### Python

Python은 ARRAY를 `list`, element NULL과 whole NULL을 각각 내부 `None`과 컬럼 자체의
`None`으로 반환합니다. `UINT64`는 arbitrary precision `int`, `DECIMAL`은 `Decimal`입니다.

```python
from decimal import Decimal
from machbaseAPI import connect

conn = connect(host="127.0.0.1", port=5656,
               user="SYS", password="MANAGER")
try:
    rows = conn.cursor(dictionary=True).execute(
        "SELECT A_I32,A_U64,A_DEC FROM SDK_ARRAY_SAMPLE ORDER BY ID"
    ).fetchall()
    assert rows[0]["A_I32"] == [1, None, -3]
    assert rows[0]["A_U64"][2] == 18446744073709551614
    assert rows[0]["A_DEC"][0] == Decimal("1.2500")
    assert rows[1]["A_I32"] is None
finally:
    conn.close()
```

prepared `execute()`와 `executemany()`는 `list` 또는 `tuple`을 ARRAY로 encode합니다.
`cursor.column_metadata`에서 ARRAY type code, cardinality와 `DECIMAL` 요소 metadata를
확인할 수 있습니다.

### Node.js

Node.js는 ARRAY를 JavaScript `Array`로 반환합니다. `INT64`와 `UINT64`는 `bigint`,
`DECIMAL`은 정밀도 보존을 위해 문자열로 반환합니다.

```javascript
const { createConnection } = require('@machbase/ts-client');
const conn = createConnection({
  host: '127.0.0.1', port: 5656, user: 'SYS', password: 'MANAGER',
});
await conn.connect();
try {
  const [rows] = await conn.query(
    'SELECT A_I32,A_U64,A_DEC FROM SDK_ARRAY_SAMPLE ORDER BY ID',
  );
  console.log(rows[0].A_I32); // [1, null, -3]
  console.log(rows[0].A_U64); // [1n, null, 18446744073709551614n]
  console.log(rows[1].A_I32); // null: whole NULL
} finally {
  await conn.end();
}
```

`JSON.stringify()` 전에 `bigint`를 문자열로 바꾸고 `DECIMAL` 문자열을 `Number`로 강제
변환하지 마십시오. prepared statement의 `getColumns()`에서 ARRAY cardinality와 요소
precision/scale metadata를 확인할 수 있습니다.

### .NET full/legacy provider

MachConnector40 full/legacy provider는 ARRAY를 `object[]`로 반환합니다. element NULL은
배열 안의 `null`, whole NULL은 `IsDBNull()`로 구분합니다.

```csharp
using Mach.Data.MachClient;
using var conn = new MachConnection(
    "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER");
conn.Open();
using var cmd = new MachCommand(
    "SELECT A_I32 FROM SDK_ARRAY_SAMPLE ORDER BY ID", conn);
using var reader = cmd.ExecuteReader();
reader.Read();
var values = (object[])reader.GetValue(0);
Console.WriteLine((int)values[0]);
Console.WriteLine(values[1] is null);
reader.Read();
Console.WriteLine(reader.IsDBNull(0));
```

각 요소는 `short`, `ushort`, `int`, `uint`, `long`, `ulong`, `float`, `double`,
`decimal`입니다. CLR `decimal` 범위를 벗어나는 값은 invariant 문자열로 반환합니다.
`GetSchemaTable()`은 provider type, cardinality, element scale과 `object[]` field type을
제공합니다.

### Go neo-client

이 항목은 Machbase Neo 서버가 아니라 `neo-client`가 Machbase DBMS에 직접 연결하는 SDK
경로입니다. 0-based ARRAY API는
`neo-client` PR #17 (https://github.com/machbase/neo-client/pull/17) 이후의 v2 module
소스에 있습니다.
공개 v2 릴리스가 지정되기 전에는 해당 소스 checkout과 `go.work` 또는 `replace` 등
명시적 로컬 module 연결이 필요합니다. 공개 v1 릴리스에 기능이 있다고 가정하지 마십시오.

```go
import (
    "context"
    "database/sql"
    "fmt"

    client "github.com/machbase/neo-client/v2"
    "github.com/machbase/neo-client/v2/api"
)

db, err := sql.Open(client.DefaultDriverName, dsn)
if err != nil { return err }
defer db.Close()

dense, err := api.NewArray(api.SqlTypeInt32,
    int32(10), nil, int32(30))
if err != nil { return err }
if _, err = db.ExecContext(context.Background(),
    "INSERT INTO SDK_ARRAY_SAMPLE(ID,A_I32) VALUES(3,?)", dense); err != nil {
    return err
}

rows, err := db.QueryContext(context.Background(),
    "SELECT A_I32 FROM SDK_ARRAY_SAMPLE WHERE ID=3")
if err != nil { return err }
defer rows.Close()
for rows.Next() {
    var raw sql.NullString
    if err := rows.Scan(&raw); err != nil { return err }
    fmt.Println(raw.String) // [10,null,30]
}
return rows.Err()
```

`database/sql` 결과 경계는 canonical 문자열을 제공합니다. `sql.NullString`으로 whole
NULL을 확인하고 유효한 값이면 `array.Scan(raw.String)`, whole NULL이면
`array.Scan(nil)`로 해석합니다. 원래의 narrow integer와 `FLOAT` 타입까지 보존하려면
요소 metadata로 receiver를 먼저 만듭니다. `DECIMAL` precision/scale은
`NewSparseArrayWithMeta()`로 지정합니다.

`ColumnTypes()`의 `DatabaseTypeName()`은 ARRAY 타입 이름을, `DecimalSize()`는
`DECIMAL` 요소 precision/scale을 제공합니다. 현재 `Length()`는 cardinality가 아니라
encoded payload byte length이므로 cardinality로 사용하면 안 됩니다. 표준
`database/sql` metadata만으로 cardinality를 직접 얻을 수 없습니다.

## 명령행 도구와 데이터 이동

### machsql

`machsql`은 canonical `ARRAY` 문자열을 출력합니다.

```sql
SELECT ID, CHANNELS, ARRAY_LENGTH(CHANNELS), CHANNELS[1]
  FROM SENSOR_ARRAY
 ORDER BY ID;
```

SQL 파일로 저장한 뒤 다음과 같이 실행할 수 있습니다.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f array_query.sql
```

### machloader

machloader의 text 입력과 출력은 canonical `[value,null,value]` 형식을 사용합니다.
delimiter나 quote가 ARRAY 내부에 포함되므로 CSV에서는 ARRAY 필드를 enclosure로
감쌉니다.

```csv
1,"[1.5,null,3.5,4.5]"
```

whole NULL과 all-element-NULL `ARRAY`가 서로 바뀌지 않는지 round trip으로 확인합니다.
CSV 자동 테이블 생성에서는 `ARRAY`를 자동 추론하지 않으므로 테이블을 먼저 명시적으로
생성합니다.

### backup, restore와 mount

backup과 restore는 요소 타입, cardinality, `DECIMAL` precision/scale과 NULL 정보를
보존합니다. mount 조회도 같은 결과와 메타데이터를 제공합니다. ARRAY를 포함하는 데이터는
Machbase DBMS 8.7.0 환경에서 backup, restore와 mount를 수행합니다.

## 버전과 오류 처리

- `ARRAY` 타입은 Machbase DBMS 8.7.0에서 지원합니다.
- ARRAY의 SQL 요소 위치와 Machbase 전용 SDK position은 0-based입니다. 기존 1-based
  SQL과 SDK 호출은 위치를 1씩 낮춰야 합니다.
- Machbase DBMS 8.7.0 서버와 ARRAY 기능이 포함된 SDK 빌드를 함께 사용합니다.
- 지원하지 않는 서버 또는 SDK에서는 ARRAY를 다른 타입으로 자동 변환하지 않고 오류를
  반환합니다.
- cardinality, position 또는 요소 변환 오류는 문장 전체를 실패시키며 부분 ARRAY를
  저장하지 않습니다.
- 애플리케이션은 whole NULL과 all-element-NULL `ARRAY`를 별개의 값으로 처리해야 합니다.
- 이 문서는 Machbase DBMS의 SQL과 SDK 기능을 다루며 Machbase Neo, HTTP, TQL과 ILP는
  범위에 포함하지 않습니다.
