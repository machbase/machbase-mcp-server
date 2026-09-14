# PreparedStatement와 타입

PreparedStatement는 SQL을 서버에서 prepare한 뒤 파라미터만 바꾸어 반복 실행합니다.
Machbase JDBC는 표준 위치 기반 매개변수와 이름 기반 확장 매개변수를 제공합니다.

## ParameterMetaData

`PreparedStatement.getParameterMetaData()`로 실행 전에 파라미터 개수와 타입을 확인할 수
있습니다. INSERT, UPDATE와 SELECT에서 동일하게 사용합니다.

```java
import java.sql.ParameterMetaData;
import java.sql.PreparedStatement;

try (PreparedStatement statement = connection.prepareStatement(
         "INSERT INTO sensor_tx " +
         "(id, value, created_at) VALUES (?, ?, ?)")) {
    ParameterMetaData metadata = statement.getParameterMetaData();

    for (int index = 1; index <= metadata.getParameterCount(); index++) {
        System.out.printf(
            "%d: type=%s precision=%d scale=%d nullable=%d%n",
            index,
            metadata.getParameterTypeName(index),
            metadata.getPrecision(index),
            metadata.getScale(index),
            metadata.isNullable(index));
    }
}
```

파라미터 인덱스는 1부터 시작합니다. 0 또는 파라미터 개수를 초과하는 인덱스에는
`SQLException`이 발생합니다. precision은 타입에 따라 해석합니다. 숫자 타입에서는 저장
바이트 수가 아니라 JDBC의 10진수 자릿수를 나타냅니다. DATETIME은
`java.sql.Types.TIMESTAMP`로 매핑되지만 데이터베이스 타입 이름은
`DATETIME`입니다.

## Named Bind Parameter

`:name` 자리표시자와 `MachPreparedStatement.setObject(String, Object)`는 Machbase 확장
기능입니다. 같은 이름이 여러 번 나오면 해당 이름의 모든 위치에 값이 적용됩니다.

```java
import com.machbase.jdbc.MachPreparedStatement;

try (MachPreparedStatement statement =
         (MachPreparedStatement) connection.prepareStatement(
             "SELECT id FROM sensor_tx " +
             "WHERE id = :id OR parent_id = :id")) {
    statement.setObject("id", Integer.valueOf(10));

    try (ResultSet result = statement.executeQuery()) {
        while (result.next()) {
            System.out.println(result.getInt("ID"));
        }
    }
}
```

- 이름은 선행 콜론을 포함하거나 생략할 수 있습니다.
- 이름은 대소문자를 구분합니다.
- 이름 기반 setter와 숫자 인덱스 setter를 한 문장에서 혼용하지 않습니다.
- SQL에 없는 이름 또는 named/positional 혼용에는 SQLState `07009`가 발생합니다.
- 이름 기반 bind를 지원하지 않는 이전 서버에는 SQLState `0A000`이 발생합니다.

이식성이 필요한 애플리케이션은 JDBC 표준인 `?`와 숫자 인덱스 setter를 사용합니다. 공통
이름 문법은 Named Bind Parameter를
참고합니다.

## Prepared SELECT 재실행

같은 PreparedStatement로 SELECT를 반복 실행할 수 있습니다. 이전 ResultSet을 닫고 값을
다시 바인딩하면 다음 실행에서 새 ResultSet을 반환합니다.

```java
try (PreparedStatement statement = connection.prepareStatement(
         "SELECT id, name FROM sensor_tx WHERE id = ?")) {
    ResultSetMetaData metadata = statement.getMetaData();
    System.out.println(metadata.getColumnCount());

    for (int id = 1; id <= 2; id++) {
        statement.setInt(1, id);
        try (ResultSet result = statement.executeQuery()) {
            while (result.next()) {
                System.out.println(result.getString("NAME"));
            }
        }
    }
}
```

Machbase JDBC는 한 Statement의 multiple open results를 지원하지 않습니다. 각 실행의
ResultSet을 소비하고 닫은 뒤 다음 실행을 시작합니다. prepare 단계의
`ResultSetMetaData`는 Statement가 열려 있는 동안 다시 조회할 수 있습니다.

## JDBC 4.2 SQLType 바인딩

Java 8의 `JDBCType`으로 파라미터의 SQL 타입을 지정할 수 있습니다.

```java
import java.math.BigDecimal;
import java.sql.JDBCType;
import java.sql.Timestamp;

try (PreparedStatement statement = connection.prepareStatement(
         "INSERT INTO sensor_tx " +
         "(id, name, value, created_at, payload) " +
         "VALUES (?, ?, ?, ?, ?)")) {
    statement.setObject(1, Integer.valueOf(1), JDBCType.INTEGER);
    statement.setObject(2, "sensor-1", JDBCType.VARCHAR);
    statement.setObject(
        3, new BigDecimal("12.3400"), JDBCType.DECIMAL, 4);
    statement.setObject(
        4, Timestamp.valueOf("2026-07-26 10:00:00"),
        JDBCType.TIMESTAMP);
    statement.setObject(5, new byte[] {1, 2, 3}, JDBCType.BINARY);
    statement.executeUpdate();
}
```

알 수 없는 vendor `SQLType`에는 `SQLFeatureNotSupportedException`이 발생합니다.
DECIMAL과 NUMERIC은 `BigDecimal`을 사용하며 지정한 소수 자릿수에 맞게 바인딩합니다.

### SQL NULL

`setNull()` 또는 `setObject(index, null, JDBCType)`을 사용하면 대상 타입에 맞는 SQL
NULL이 전달됩니다. 다음 타입도 typed NULL을 지원합니다.

- `REAL`, `BIT`, `TINYINT`, `BOOLEAN`
- `VARBINARY`, `LONGVARBINARY`, `BLOB`, `CLOB`
- `LONGVARCHAR`

unsigned 파라미터의 NULL은 ParameterMetaData를 기준으로 네이티브 NULL 값으로 변환됩니다.
unsigned 최대 데이터 값보다 하나 큰 wire NULL sentinel은 실제 데이터로 저장할 수 없으며,
해당 값을 전달하면 SQLState `22003`이 발생합니다.

| Machbase 타입 | Java 타입 | 데이터 범위 |
|---------------|-----------|-------------|
| `USHORT` | `Integer` | 0~65534 |
| `UINTEGER` | `Long` | 0~4294967294 |
| `ULONG` | `BigInteger` | 0~18446744073709551614 |

NULL을 입력할 때 sentinel 값을 직접 전달하지 말고 `setNull()`을 사용합니다.

## Boolean

`setBoolean()`과 `setObject(index, value, JDBCType.BOOLEAN)`은 `true`를 1, `false`를 0으로
전달합니다. 문자열은 대소문자와 관계없이 `true`와 `false`만 허용하며, 그 밖의 값에는
SQLState `22018`이 발생합니다.

## IPv4와 IPv6

IP 주소 컬럼에는 `MachPreparedStatement` 확장 setter를 사용할 수 있습니다.

```java
MachPreparedStatement statement =
    (MachPreparedStatement) connection.prepareStatement(
        "INSERT INTO net_log(ts, src_ip, dst_ip) VALUES (?, ?, ?)");

statement.setLong(1, System.currentTimeMillis() * 1_000_000L);
statement.setIpv4(2, "192.168.1.100");
statement.setIpv6(3, "::1");
statement.executeUpdate();
```

## Nullable 메타데이터

`ParameterMetaData.isNullable()`은 `parameterNoNulls`, `parameterNullable` 또는
`parameterNullableUnknown`을 반환합니다. `parameterNullableUnknown`을 NOT NULL로
해석하지 않습니다. SQL별 판정 규칙은
Nullable 메타데이터 지원 범위를
참고합니다.
