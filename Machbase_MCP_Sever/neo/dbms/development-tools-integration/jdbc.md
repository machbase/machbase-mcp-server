# JDBC

Machbase JDBC 드라이버는 Java 8을 기준으로 JDBC 4.2 핵심 API를 제공합니다. 표준 JDBC
API로 서버에 연결하고 PreparedStatement, 타입 지정 조회와 바인딩, 데이터베이스
메타데이터, 로컬 트랜잭션과 커넥션 풀을 사용할 수 있습니다.

| 항목 | 값 |
|------|----|
| Java 바이트코드 기준 | Java 8 |
| 드라이버가 보고하는 JDBC 버전 | 4.2 |
| 드라이버 버전 | 3.0.0 |
| JDBC URL | `jdbc:machbase://<host-list>/[database]` |
| `Driver.jdbcCompliant()` | `false` |

`jdbcCompliant()`의 `false`는 JDBC 4.2 API 지원 여부가 아니라 SQL-92 Entry Level 전체
지원 여부를 나타냅니다. 애플리케이션에서는 필요한 선택 기능을
`DatabaseMetaData`의 기능 메서드로 확인합니다.

## 다중 데이터베이스

URL 경로 또는 `database` 연결 속성으로 초기 데이터베이스를 지정할 수 있습니다.

```java
String url = "jdbc:machbase://127.0.0.1:5656/factory_a";
Connection conn = DriverManager.getConnection(url, "APP_A", password);

System.out.println(conn.getCatalog());
conn.setCatalog("FACTORY_A");
```

`getCatalog()`와 `setCatalog()`는 서버 현재 데이터베이스와 동기화됩니다. URL 경로와
설정 속성을 동시에 지정하면 값이 같아야 하며, JDBC 메타데이터에서 카탈로그는 데이터베이스,
스키마는 소유자입니다. pooled 연결은 반환 시 초기 카탈로그로 복원되는지 확인하고,
준비된 문장과 append 핸들은 생성 시점 데이터베이스에 고정된다는 점을 고려합니다.

## 드라이버 설치

### JAR 파일 사용

Machbase 설치 디렉터리의 `machbase.jar`를 classpath에 추가합니다.

```bash
ls -l "$MACHBASE_HOME/lib/machbase.jar"
javac -classpath ".:$MACHBASE_HOME/lib/machbase.jar" MyApp.java
java -classpath ".:$MACHBASE_HOME/lib/machbase.jar" MyApp
```

JAR에는 `META-INF/services/java.sql.Driver`가 포함되어 있습니다. JDBC 4.0 이후 환경에서는
`Class.forName("com.machbase.jdbc.MachDriver")`를 호출하지 않아도 드라이버가 자동으로
등록됩니다. 기존 애플리케이션의 명시적 호출은 그대로 사용할 수 있습니다.

### Maven

```xml
<dependency>
    <groupId>com.machbase</groupId>
    <artifactId>machjdbc</artifactId>
    <version>LATEST</version>
</dependency>
```

### Gradle

```groovy
dependencies {
    implementation 'com.machbase:machjdbc:LATEST'
}
```

배포 산출물 버전은 Maven Central (https://mvnrepository.com/artifact/com.machbase/machjdbc)에서
확인합니다. 드라이버가 런타임 메타데이터로 반환하는 `3.0.0`과 배포 산출물 버전은 서로 다른
버전 체계입니다.

## 서버에 연결

사용자 이름과 비밀번호는 소스 코드에 기록하지 않고 환경 변수나 비밀 관리 시스템으로
전달합니다.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.util.Properties;

String url = "jdbc:machbase://127.0.0.1:5656/machbasedb";

Properties properties = new Properties();
properties.setProperty("user", "SYS");
properties.setProperty("password", System.getenv("MACHBASE_PASSWORD"));

try (Connection connection =
         DriverManager.getConnection(url, properties)) {
    // SQL을 실행합니다.
}
```

### 연결 옵션

연결 옵션은 `Properties` 또는 URL 쿼리 문자열로 지정합니다. `randomHost`는
`Properties`에서 지정하거나 다중 호스트 URL의 `^` 구분자를 사용합니다.

| 옵션 | 설명 |
|------|------|
| `user`, `password` | 비밀번호 인증 정보 |
| `TIMEZONE` | 세션 타임존. `+0900` 형식을 사용합니다. |
| `randomHost` | 호스트 목록에서 첫 연결 대상을 무작위로 선택합니다. |
| `maxStatements` | 풀링 연결의 최대 캐시 Statement 수 |
| `CONNECTION_TIMEOUT` | 소켓 연결 시간 초과(초). `0`은 제한 없음입니다. |
| `SOCKET_TIMEOUT` | 소켓 읽기 시간 초과(초). `0`은 제한 없음입니다. |
| `characterEncoding` | 클라이언트 문자 인코딩 |
| `AUTH_MODE` | `PASSWORD` 또는 `CHALLENGE` |
| `AUTH_SIG_SCHEME` | `ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS` |
| `AUTH_KEY_FILE` | PEM 개인키 파일 경로 |

```java
String url =
    "jdbc:machbase://127.0.0.1:5656/machbasedb?TIMEZONE=+0900";
```

### 다중 호스트 연결

Machbase 8.7.0 JDBC 드라이버는 하나의 URL에 여러 호스트를 지정할 수 있습니다.

| 선택 방식 | 지정 방법 | 동작 |
|-----------|-----------|------|
| 순차 선택 | 호스트를 `,`로 구분 | URL에 작성한 순서대로 연결을 시도합니다. |
| 무작위 시작 | 호스트를 `^`로 구분 | 호스트 목록에서 첫 연결 대상을 무작위로 선택합니다. |
| 무작위 시작 | `Properties`에 `randomHost=true` 지정 | `,`로 구분한 목록에서 첫 연결 대상을 무작위로 선택합니다. |

다음 URL은 `db1` 연결에 실패하면 `db2`에 연결을 시도합니다.

```java
String url =
    "jdbc:machbase://db1.example.com:5656,db2.example.com:5656/" +
    "machbasedb?CONNECTION_TIMEOUT=5";
```

`^` 구분자를 사용하면 첫 연결 대상을 무작위로 선택합니다.

```java
String url =
    "jdbc:machbase://db1.example.com:5656^db2.example.com:5656/" +
    "machbasedb?CONNECTION_TIMEOUT=5";
```

`randomHost` 설정 속성을 사용하려면 `,`로 호스트를 구분합니다.

```java
Properties properties = new Properties();
properties.setProperty("randomHost", "true");

String url =
    "jdbc:machbase://db1.example.com:5656,db2.example.com:5656/" +
    "machbasedb?CONNECTION_TIMEOUT=5";
```

- `,`와 `^` 구분자를 하나의 URL에서 함께 사용할 수 없습니다.
- 연결 refused, 연결 시간 초과, 소켓 오류 등 연결 단계의 I/O 오류가 발생하면
  다음 호스트로 연결을 시도합니다. 모든 호스트가 실패하면
  `DriverManager.getConnection()`이 `SQLException`을 반환합니다.
- `CONNECTION_TIMEOUT`은 호스트별 연결 시도에 적용됩니다. 따라서 전체 연결 대기 시간은
  호스트 수와 각 호스트의 응답 시간에 따라 길어질 수 있습니다.
- `SOCKET_TIMEOUT`은 연결된 소켓의 읽기 대기 시간을 제한하며 호스트 선택 순서를 변경하지
  않습니다.

다중 호스트 전환은 새 연결 또는 재연결 과정의 소켓 연결에 적용됩니다. 연결이 끊긴 뒤
자동 reconnect가 성공해도 이전 Statement, PreparedStatement와 ResultSet은 재사용하지
않습니다. 진행 중이던 SQL의 성공 여부나 안전한 재실행을 보장하지 않으므로, 활성
트랜잭션에서 연결 오류가 발생하면 연결을 폐기하고 업무의 멱등성 정책에 따라 전체
트랜잭션을 다시 실행합니다.

## AUTH KEY 인증

공개키 기반 challenge 인증에서는 비밀번호 대신 로컬 개인키로 서버 challenge에
서명합니다.

```java
Properties properties = new Properties();
properties.setProperty("user", "app_user");
properties.setProperty("AUTH_MODE", "CHALLENGE");
properties.setProperty("AUTH_SIG_SCHEME", "ECDSA");
properties.setProperty(
    "AUTH_KEY_FILE", "/opt/machbase/keys/app_user_ecdsa.pem");

Connection connection = DriverManager.getConnection(
    "jdbc:machbase://127.0.0.1:5656/machbasedb", properties);
```

- `AUTH_MODE=CHALLENGE`에서는 `password`를 인증에 사용하지 않습니다.
- `AUTH_KEY_FILE`은 필수입니다.
- `AUTH_SIG_SCHEME`을 생략하면 키 종류에 맞는 기본 서명 방식을 선택합니다.
- POSIX 환경에서는 개인키 파일 권한을 `600`으로 제한합니다.

## 빠른 시작

다음 예제는 LOG 테이블에 값을 입력하고 다시 조회합니다.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.Properties;

public class JdbcQuickStart {
    public static void main(String[] args) throws Exception {
        Properties properties = new Properties();
        properties.setProperty("user", "SYS");
        properties.setProperty(
            "password", System.getenv("MACHBASE_PASSWORD"));

        try (Connection connection = DriverManager.getConnection(
                 "jdbc:machbase://127.0.0.1:5656/machbasedb",
                 properties);
             Statement statement = connection.createStatement()) {
            statement.execute(
                "CREATE LOG TABLE jdbc_sensor " +
                "(ts DATETIME, name VARCHAR(40), value DOUBLE)");

            try (PreparedStatement insert = connection.prepareStatement(
                     "INSERT INTO jdbc_sensor VALUES (?, ?, ?)")) {
                insert.setLong(1, System.currentTimeMillis() * 1_000_000L);
                insert.setString(2, "sensor-1");
                insert.setDouble(3, 25.3);
                insert.executeUpdate();
            }

            try (ResultSet result = statement.executeQuery(
                     "SELECT name, value FROM jdbc_sensor")) {
                while (result.next()) {
                    System.out.printf("%s %.1f%n",
                        result.getString("NAME"),
                        result.getDouble("VALUE"));
                }
            }
        }
    }
}
```

DATETIME에 epoch 나노초 값을 전달할 때는 `long`을 사용합니다. 예제의 테이블이 이미
존재하면 `CREATE LOG TABLE`을 생략하거나 다른 이름을 사용합니다.

## INSERT 결과 ROWID

Standard Edition에서 단일 `INSERT ... VALUES`가 성공하면 JDBC 표준 generated keys API로
입력된 행의 ROWID를 확인할 수 있습니다.

```java
String sql = "INSERT INTO jdbc_sensor VALUES (?, ?, ?)";
try (PreparedStatement insert = connection.prepareStatement(
         sql, Statement.RETURN_GENERATED_KEYS)) {
    insert.setLong(1, System.currentTimeMillis() * 1_000_000L);
    insert.setString(2, "sensor-2");
    insert.setDouble(3, 26.1);
    insert.executeUpdate();

    try (ResultSet keys = insert.getGeneratedKeys()) {
        if (keys.next()) {
            java.sql.RowId rowId = keys.getRowId("ROWID");
        }
    }
}
```

결과는 `ROWID` 컬럼 하나와 최대 한 행으로 구성됩니다. 반환할 ROWID가 없으면 빈
`ResultSet`입니다. 지원 여부는 `DatabaseMetaData.supportsGetGeneratedKeys()`로 확인합니다.
배치, Append, `INSERT ... SELECT`, UPSERT의 차이는
ROWID와 INSERT 결과 ID를 참고하십시오.

## 버전 확인

```java
import java.sql.DatabaseMetaData;

DatabaseMetaData metadata = connection.getMetaData();

System.out.println(metadata.getDriverName());
System.out.println(metadata.getDriverVersion());
System.out.println(metadata.getJDBCMajorVersion()); // 4
System.out.println(metadata.getJDBCMinorVersion()); // 2
```

## 관련 문서

| 문서 | 내용 |
|------|------|
| PreparedStatement와 타입 | 매개변수 메타데이터, 이름 기반 bind, SQLType, NULL과 타입 변환 |
| ResultSet, Statement와 LOB | typed 조회, 스트림, LOB, 시간 초과와 자원 관리 |
| 트랜잭션과 커넥션 풀 | Standard 로컬 트랜잭션, DataSource와 연결 풀 |
| DatabaseMetaData | 테이블, 컬럼, 키, 인덱스와 기능 조회 |
| Append API | `MachStatement` 기반 고속 입력 |
| 마이그레이션과 문제 해결 | 이전 드라이버 전환, 미지원 기능과 오류 처리 |
