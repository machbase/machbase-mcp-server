# Append API

Machbase Append API는 여러 행을 연속 입력하는 대량 입력 API입니다. JDBC에서는
`MachStatement` 확장 메서드를 사용하며, 이 페이지는 LOG 입력 예제를 중심으로 설명합니다.
다른 테이블 타입의 지원 범위는 SDK 지원표를
함께 확인합니다.

## API

| 메서드 | 설명 |
|--------|------|
| `executeAppendOpen(tableName, errorCheckCount)` | Append 세션을 시작하고 컬럼 메타데이터를 반환합니다. |
| `executeAppendOpen(tableName, inputColumns, errorCheckCount)` | Machbase DBMS 8.7.0에서 선택 컬럼 또는 ARRAY 요소 대상으로 Append 세션을 시작합니다. |
| `executeAppendData(metadata, data)` | 한 행을 전송합니다. |
| `executeAppendDataByTime(metadata, time, data)` | 나노초 시간을 지정해 한 행을 전송합니다. |
| `executeAppendFlush()` | 대기 중인 응답을 동기화합니다. |
| `executeAppendClose()` | Append 세션을 종료합니다. |
| `executeSetAppendErrorCallback(callback)` | 행 오류 콜백을 등록합니다. |
| `getAppendSuccessCount()` | 성공한 행 수를 반환합니다. |
| `getAppendFailureCount()` | 실패한 행 수를 반환합니다. |

공개 `executeAppendData()`는 성공하면 `1`을 반환하고 유효하지 않은 내부 결과에는
`SQLException`을 던집니다. 최종 성공·실패 건수와 콜백도 함께 확인합니다.

## 입력 예제

```sql
CREATE LOG TABLE sensor_data (
    time DATETIME,
    name VARCHAR(40),
    value DOUBLE
);
```

```java
import com.machbase.jdbc.MachStatement;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.util.ArrayList;

try (MachStatement statement =
         (MachStatement) connection.createStatement()) {
    ResultSet appendResult =
        statement.executeAppendOpen("sensor_data", 100);
    ResultSetMetaData metadata = appendResult.getMetaData();

    statement.executeSetAppendErrorCallback(
        (errorNumber, errorMessage, rowMessage) ->
            System.err.printf(
                "Append error [%05d]: %s%n%s%n",
                errorNumber, errorMessage, rowMessage));

    long baseTime = System.currentTimeMillis() * 1_000_000L;

    for (int index = 0; index < 10_000; index++) {
        ArrayList<Object> row = new ArrayList<>();
        row.add(baseTime + index);
        row.add("sensor-" + (index % 10));
        row.add(20.0 + index * 0.001);

        int result = statement.executeAppendData(metadata, row);
        if (result != 1 && result != 2) {
            throw new SQLException(
                "Append failed at row " + index);
        }
    }

    statement.executeAppendFlush();
    statement.executeAppendClose();
    appendResult.close();

    System.out.printf("success=%d failure=%d%n",
        statement.getAppendSuccessCount(),
        statement.getAppendFailureCount());
}
```

## ARRAY와 선택 컬럼

희소 ARRAY 입력에는 컬럼 선택이 필수가 아닙니다. 일반
`executeAppendOpen(tableName, errorCheckCount)`으로 열고 반환된 메타데이터에 맞춰
`MachSparseArray`를 행의 ARRAY 값으로 전달합니다.

```java
ResultSet opened = statement.executeAppendOpen("ARRAY_APPEND_FULL_EXAMPLE", 0);
```

연결·입력·Close·조회까지의 일반 Open 예제를
먼저 확인하십시오. `ID`와 ARRAY 컬럼을 선언 순서대로 전달하며 자동 `_arrival_time`은
행에 추가하지 않습니다.

Machbase DBMS 8.7.0에서는 `executeAppendOpen()` 오버로드에 컬럼명이나
`ARRAY_COLUMN[position]`을 전달할 수 있습니다.

```java
ResultSet appendResult = statement.executeAppendOpen(
    "sensor_array",
    new String[] {"ID", "CHANNELS[0]", "CHANNELS[3]"},
    0);
```

행마다 다른 ARRAY 위치를 입력할 때는 `MachConnection.createSparseArrayOf()`로
`MachSparseArray`를 생성합니다. map 키는 0부터 시작하며 빈 맵은 모든 요소가 NULL인
ARRAY입니다. Java `null`은 배열 전체 NULL입니다.

```java
Map<Integer, Object> entries = new HashMap<Integer, Object>();
entries.put(Integer.valueOf(1), Integer.valueOf(200));
entries.put(Integer.valueOf(3), Integer.valueOf(400));

MachSparseArray sparse = connection.createSparseArrayOf(
    "INT32", 4, entries);
```

밀집 ARRAY의 조회와 prepared 입력에는 `java.sql.Array`, `Connection.createArrayOf()`와
`PreparedStatement.setArray()`를 사용합니다. 전체 예제와 대상 충돌 규칙은
Sparse ARRAY와 선택 컬럼 Append API를
참고하십시오.

SQL ARRAY 요소 대상과 `MachSparseArray` 위치는 0부터 시작하는 인덱스입니다. JDBC 표준의
매개변수 순번과 `java.sql.Array.getArray(index, count)` slice 인덱스는 기존처럼
1부터 시작하는 인덱스이므로 서로 혼동하지 마십시오.

## DATETIME

Append의 DATETIME 값은 epoch 나노초 단위의 `long`으로 전달합니다.

```java
long epochNanoseconds =
    System.currentTimeMillis() * 1_000_000L;
```

`executeAppendDataByTime()`은 별도의 시간 값을 받는 테이블 입력 경로에서 사용합니다.
입력 컬럼 순서와 Java 타입은 `executeAppendOpen()`이 반환한 ResultSetMetaData에 맞춥니다.

## flush와 close

1. `executeAppendOpen()`으로 세션을 시작합니다.
2. `executeAppendData()`를 반복 호출합니다.
3. 중간 확인이 필요하면 `executeAppendFlush()`를 호출합니다.
4. 모든 입력을 보낸 뒤 `executeAppendClose()`를 호출합니다.
5. 성공·실패 건수와 콜백 결과를 확인합니다.

예외가 발생해도 Append 세션과 Statement가 닫히도록 try-with-resources와 `finally`를
사용합니다. 콜백에서는 실패 행을 별도 저장하거나 로깅하고, 무조건적인 재시도로
중복 입력을 만들지 않도록 업무 키를 사용합니다.

## 크기와 사용 범위

ordered append는 프로토콜 패킷 한도를 공유하므로 한 행의 전체 인코딩 크기를 64KiB
미만으로 유지합니다. BLOB/CLOB처럼 큰 값을 입력할 때는 행 크기와 클라이언트 메모리
사용량을 함께 확인합니다.

TRANSACTION 테이블의 Append 배치는 SQL 트랜잭션에 포함되지 않고 독립적으로
반영됩니다. 롤백이 필요한 여러 DML은 JDBC 트랜잭션을
사용합니다.
