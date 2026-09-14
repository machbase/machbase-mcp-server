# 트랜잭션과 커넥션 풀

Machbase JDBC는 Standard Edition의 TRANSACTION 테이블에서 표준 JDBC 로컬 트랜잭션을
지원합니다. Cluster Edition에는 TRANSACTION 테이블이 없으므로 이 페이지의 트랜잭션
기능을 적용하지 않습니다.

## TRANSACTION 테이블 생성

```sql
CREATE TRANSACTION TABLE sensor_tx
(
    id         INTEGER PRIMARY KEY,
    parent_id  INTEGER,
    name       VARCHAR(64),
    value      DECIMAL(20, 4),
    created_at DATETIME,
    payload    BINARY
);
```

## commit과 rollback

`setAutoCommit(false)`, `commit()`과 `rollback()`을 사용합니다. 애플리케이션에서 SQL
`BEGIN`을 직접 전송할 필요가 없습니다.

```java
import java.sql.PreparedStatement;
import java.sql.SQLException;

connection.setAutoCommit(false);

try (PreparedStatement statement = connection.prepareStatement(
         "INSERT INTO sensor_tx (id, value) VALUES (?, ?)")) {
    statement.setInt(1, 1);
    statement.setBigDecimal(2, new BigDecimal("10.5000"));
    statement.executeUpdate();
    connection.commit();
} catch (SQLException exception) {
    try {
        connection.rollback();
    } catch (SQLException rollbackException) {
        exception.addSuppressed(rollbackException);
    }
    throw exception;
}
```

`setAutoCommit(false)`는 즉시 `BEGIN`을 보내지 않습니다. 수동 모드의 첫 Statement를
실행할 때 트랜잭션을 시작합니다. 커밋 또는 롤백 뒤에도 auto-commit은 `false`로
유지되며 다음 Statement가 새 트랜잭션을 시작합니다.

- `setAutoCommit(true)`로 전환할 때 활성 트랜잭션이 있으면 먼저 커밋합니다.
- auto-commit이 `true`일 때 `commit()`이나 `rollback()`을 호출하면 SQLState `25000`이
  발생합니다.
- Connection을 닫을 때 완료하지 않은 트랜잭션은 롤백됩니다.
- 커밋과 롤백은 열린 ResultSet을 닫지만 Statement는 재사용할 수 있습니다.

## 격리 수준과 cursor

지원하는 격리 수준은 `Connection.TRANSACTION_SERIALIZABLE`입니다. 다른 격리 수준을
요청하면 `SQLFeatureNotSupportedException`이 발생합니다.

지원하는 holdability는 `ResultSet.CLOSE_CURSORS_AT_COMMIT`입니다. 커밋 전에 필요한
ResultSet을 소비하거나 커밋 후 쿼리를 다시 실행합니다.

## 테이블 종류별 동작

| 작업 | 수동 트랜잭션 동작 |
|------|--------------------------|
| TRANSACTION 테이블 DML/SELECT | 트랜잭션에 참여합니다. |
| LOG/TAG 테이블 SELECT | 실행할 수 있습니다. |
| TRANSACTION 변경 전 첫 LOG DML | 호환 경로에서 auto-commit으로 재실행될 수 있습니다. |
| 독립 TAG DML | 트랜잭션에 참여하며 롤백할 수 있습니다. |
| TRANSACTION 변경 후 LOG/TAG DML 또는 DDL | 오류가 발생합니다. |

호환 경로로 auto-commit 재실행된 LOG DML은 이후 롤백 대상이 아닙니다. 롤백이
필요한 데이터는 TRANSACTION 테이블을 사용합니다. 여러 TRANSACTION 테이블에 대한 정상
커밋과 롤백은 지원하지만 백엔드 커밋 도중 장애가 발생했을 때 전역 원자성을
보장하지 않습니다. 중요한 원자 작업은 하나의 TRANSACTION 테이블 범위로 설계합니다.

## DataSource

`MachDataSource`는 애플리케이션 서버나 프레임워크에 연결 속성을 주입할 때 사용합니다.

```java
import com.machbase.jdbc.MachDataSource;
import java.sql.Connection;

MachDataSource dataSource = new MachDataSource();
dataSource.setUrl("jdbc:machbase://127.0.0.1:5656/machbasedb");
dataSource.setUser("SYS");
dataSource.setPassword(System.getenv("MACHBASE_PASSWORD"));
dataSource.setLoginTimeout(10);

try (Connection connection = dataSource.getConnection()) {
    // SQL을 실행합니다.
}
```

DataSource는 URL, 사용자, password, login 시간 초과, 로그 writer와 JDBC `Wrapper` 계약을
지원합니다.

## ConnectionPoolDataSource

`MachConnectionPoolDataSource`는 물리 연결을 직접 노출하지 않고 논리 Connection을
반환합니다.

```java
import com.machbase.jdbc.MachConnectionPoolDataSource;
import java.sql.Connection;
import javax.sql.PooledConnection;

MachConnectionPoolDataSource source =
    new MachConnectionPoolDataSource();
source.setUrl("jdbc:machbase://127.0.0.1:5656/machbasedb");
source.setUser("SYS");
source.setPassword(System.getenv("MACHBASE_PASSWORD"));

PooledConnection pooled = source.getPooledConnection();
try {
    try (Connection logical = pooled.getConnection()) {
        // logical connection을 사용합니다.
    }
} finally {
    pooled.close();
}
```

한 PooledConnection에서는 논리 핸들 하나만 활성화합니다. 논리 Connection을 닫으면
다음 상태를 초기화한 뒤 `connectionClosed` 이벤트가 한 번 발생합니다.

- 완료하지 않은 트랜잭션 롤백
- auto-commit 복원
- URL에서 결정한 초기 카탈로그 복원
- 네트워크 시간 초과 복원

close를 시작한 논리 핸들의 호출이 끝나기 전에 다음 연결 대여 기간을 대여하지 않습니다. 닫힌
Connection, Statement 또는 DatabaseMetaData는 다음 연결을 대여한 요청에서 재사용할 수 없으며
SQLState `08003`이 발생합니다. Statement pooling은 지원하지 않습니다.

SQLState 클래스 `08`의 치명적 연결 오류는 물리 연결을 폐기하고
`connectionErrorOccurred`를 발생시킵니다. duplicate 키와 같은 클래스 `23` 오류는 연결
손상이 아니므로 연결 오류 이벤트를 발생시키지 않습니다.

## HikariCP

```java
import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:machbase://127.0.0.1:5656/machbasedb");
config.setUsername("SYS");
config.setPassword(System.getenv("MACHBASE_PASSWORD"));
config.setMaximumPoolSize(10);
config.setMinimumIdle(2);
config.setConnectionTimeout(30_000);
config.setIdleTimeout(600_000);
config.setMaxLifetime(1_800_000);
config.addDataSourceProperty("TIMEZONE", "+0900");

try (HikariDataSource dataSource = new HikariDataSource(config);
     Connection connection = dataSource.getConnection()) {
    // SQL을 실행합니다.
}
```

논리 Connection은 try-with-resources로 즉시 반환하고 반환한 핸들을 보관하지 않습니다.

## Network timeout

`setNetworkTimeout(executor, milliseconds)`는 소켓 읽기 시간 초과를 밀리초 단위로
설정하며 `0`은 제한 없음입니다. 음수 값, null executor 또는 작업을 거부하는 executor에는
`SQLException`이 발생합니다.

실제 네트워크 시간 초과가 만료되면 SQLState 클래스 `08`의 예외가 발생하고 물리 연결은
유효하지 않은 상태가 됩니다. 해당 연결에서 만든 Statement와 ResultSet을 재사용하지 말고
새 연결을 대여합니다. 활성 트랜잭션의 I/O 실패는 자동으로 재실행하지 않습니다.
