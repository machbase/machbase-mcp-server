# ResultSet, Statement와 LOB

Machbase JDBC ResultSet은 forward-only, 읽기 전용 커서입니다. Connection, Statement와
ResultSet은 try-with-resources로 닫습니다.

```java
statement.getResultSetType();        // ResultSet.TYPE_FORWARD_ONLY
statement.getResultSetConcurrency(); // ResultSet.CONCUR_READ_ONLY
```

scrollable 또는 updateable ResultSet은 지원하지 않습니다. `next()` 전, 마지막 행 이후,
close 이후의 getter 호출과 범위를 벗어난 컬럼 인덱스에는 `SQLException`이 발생합니다.

## 타입 지정 조회

`getObject(index, Class<T>)`와 `getObject(label, Class<T>)`를 지원합니다.

```java
import java.math.BigDecimal;
import java.sql.Timestamp;

try (ResultSet result = statement.executeQuery(
         "SELECT id, value, created_at FROM sensor_tx")) {
    while (result.next()) {
        Integer id = result.getObject("ID", Integer.class);
        BigDecimal value =
            result.getObject("VALUE", BigDecimal.class);
        Timestamp createdAt =
            result.getObject("CREATED_AT", Timestamp.class);
    }
}
```

| Java 타입 | 일반적인 Machbase 타입 |
|-----------|-------------------------|
| `String` | CHAR, VARCHAR, TEXT, IPV4, IPV6, JSON |
| `Short`, `Integer`, `Long` | 정수 타입 |
| `Float`, `Double` | 실수 타입 |
| `BigDecimal` | DECIMAL, NUMERIC |
| `Boolean` | BOOLEAN |
| `Timestamp`, `Date`, `Time` | DATETIME |
| `byte[]` | BINARY |
| `Blob`, `Clob` | BLOB, CLOB |

SQL NULL은 객체 getter에서 Java `null`을 반환합니다. primitive getter는 0 또는 `false`를
반환하며, 바로 뒤의 `wasNull()`로 SQL NULL 여부를 확인합니다. 지원하지 않는 변환과 null
대상 클래스에는 `SQLException`이 발생합니다.

Machbase SQL에서 빈 문자열 리터럴 `''`은 SQL `NULL`입니다. 따라서 해당 결과 컬럼의
`ResultSetMetaData.isNullable()`은 `columnNullable`이고 `getObject()`는 `null`을
반환합니다. `''''`는 작은따옴표 한 글자이므로 NULL이 아닌 문자열입니다.

unsigned 타입의 기본 객체 매핑은 다음과 같습니다.

| Machbase 타입 | `getObject()` 반환 타입 |
|---------------|-------------------------|
| `USHORT` | `Integer` |
| `UINTEGER` | `Long` |
| `ULONG` | `BigInteger` |

`SHORT`는 `Integer`, 32비트 `FLOAT`는 `Float` 객체로 반환합니다. BOOLEAN 문자열은
`true`와 `false`만 허용합니다.

## 문자와 바이너리 stream

`setAsciiStream()`, `setBinaryStream()`과 `setCharacterStream()`은 `int` 길이, `long`
길이와 길이 없는 오버로드를 제공합니다. `setNCharacterStream()`과 `setNString()`은 별도
NCHAR 저장 타입이 아니라 VARCHAR 경로의 별칭입니다.

ResultSet에서는 다음 getter를 인덱스 또는 컬럼 이름으로 사용할 수 있습니다.

- `getAsciiStream()`, `getBinaryStream()`
- `getCharacterStream()`, `getNCharacterStream()`
- `getNString()`

길이를 지정한 입력이 선언한 길이보다 짧거나, 길이가 음수이거나,
`Integer.MAX_VALUE`를 초과하면 `SQLException`이 발생합니다. 현재 스트림은 클라이언트
메모리에 materialize하므로 일정한 메모리만 사용하는 대용량 스트리밍 용도로 사용하지
않습니다.

## BLOB과 CLOB

LOG 테이블의 BLOB/CLOB 컬럼은 표준 `Blob`과 `Clob` 객체로 조회하고 바인딩할 수 있습니다.

```java
import java.io.ByteArrayInputStream;
import java.io.StringReader;
import java.sql.Blob;
import java.sql.Clob;

try (PreparedStatement insert = connection.prepareStatement(
         "INSERT INTO event_log (payload, message) VALUES (?, ?)")) {
    insert.setBlob(1, new ByteArrayInputStream(payload));
    insert.setClob(2, new StringReader(message));
    insert.executeUpdate();
}

try (ResultSet result = statement.executeQuery(
         "SELECT payload, message FROM event_log")) {
    while (result.next()) {
        Blob payloadObject = result.getBlob("PAYLOAD");
        Clob messageObject = result.getClob("MESSAGE");

        byte[] payloadBytes = payloadObject.getBytes(
            1, (int) payloadObject.length());
        String messageText = messageObject.getSubString(
            1, (int) messageObject.length());

        payloadObject.free();
        messageObject.free();
    }
}
```

`Connection.createBlob()`과 `createClob()`으로 mutable 객체를 만들고 `setBytes()`,
`setString()`, `setBinaryStream()`, `setCharacterStream()`과 `truncate()`를 사용할 수
있습니다. 사용을 마치면 `free()`를 호출합니다.

LOB 위치는 JDBC 표준대로 1부터 시작합니다. 부분 스트림의 전체 요청 범위가 실제 값 안에
있어야 하며 끝을 넘어가면 짧게 잘라 반환하지 않고 SQLState `22003`이 발생합니다. 음수
길이 또는 Java 배열로 표현할 수 없는 길이에는 `HY090`이 발생합니다. `free()` 이후 객체를
다시 사용하면 `SQLException`이 발생합니다.

LOB은 전체 값을 클라이언트 메모리에 materialize합니다. 수백 MiB 이상의 값을 일정한
메모리로 처리하는 스트리밍 LOB 구현은 아닙니다.

## ResultSet 메타데이터

`ResultSetMetaData.isNullable()`로 SELECT 결과 컬럼의 NULL 가능 여부를 확인합니다.

```java
ResultSetMetaData metadata = result.getMetaData();
int nullable = metadata.isNullable(columnIndex);
```

`columnNullableUnknown`은 NOT NULL을 의미하지 않습니다. 테이블 컬럼의 제약은
`DatabaseMetaData.getColumns()`에서 확인하고 PRIMARY KEY는
`DatabaseMetaData.getPrimaryKeys()`로 별도 조회합니다.

## 행 수와 fetch 설정

JDBC 4.2 large update API는 update 건수를 `long`으로 반환합니다.

```java
long count = statement.executeLargeUpdate(
    "DELETE FROM sensor_tx WHERE id < 100");
long[] counts = statement.executeLargeBatch();
```

`setLargeMaxRows()`와 `getLargeMaxRows()`도 사용할 수 있습니다. `setMaxRows()` 또는
`setLargeMaxRows()`는 ResultSet에서 가져올 최대 행 수를 제한하지만 Statement의
`fetchSize` 값을 변경하지 않습니다.

## Statement 수명주기

- `closeOnCompletion()`을 설정하면 마지막 ResultSet이 닫힐 때 Statement도 닫힙니다.
- 한 Statement의 이전 ResultSet은 재실행 전에 닫습니다.
- 커밋은 ResultSet을 닫지만 Statement와 PreparedStatement는 다시 사용할 수 있습니다.
- 한 ResultSet의 `next()`와 getter를 여러 스레드에서 동시에 호출하지 않습니다.

## 취소와 query timeout

`Statement.cancel()`은 현재 실행 중인 문장을 별도 세션으로 취소합니다. 실행 중인
문장이 없으면 아무 작업도 하지 않으며 PreparedStatement의 bind와 메타데이터는 유지됩니다.

`setQueryTimeout(seconds)`이 만료되면 `SQLTimeoutException`과 SQLState `HYT00`이
발생합니다. 같은 Statement는 예외 처리가 끝난 뒤 다음 쿼리에 재사용할 수 있습니다.
이전 실행의 시간 초과 작업은 다음 실행을 취소하지 않습니다.

독립 쿼리를 병렬 실행하려면 같은 Connection을 여러 worker가 공유하지 말고 커넥션
풀에서 worker별 논리 Connection을 대여합니다. 진행 중 fetch를 종료해야 할 때는 다른
스레드에서 `close()`, `cancel()` 또는 `Connection.abort()`를 호출할 수 있습니다.
