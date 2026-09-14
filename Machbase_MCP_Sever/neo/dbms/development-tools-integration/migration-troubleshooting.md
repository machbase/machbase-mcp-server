# 마이그레이션과 문제 해결

최신 Machbase JDBC는 Java 8/JDBC 4.2를 기준으로 버전 보고, 메타데이터, 타입 변환,
트랜잭션과 자원 수명주기를 표준 JDBC 계약에 맞춥니다. 이전 동작에 의존하는
애플리케이션은 다음 차이를 확인합니다.

## 이전 드라이버에서 전환

| 영역 | 현재 동작 | 애플리케이션 확인 사항 |
|------|-----------|------------------------|
| Java/JDBC 기준 | Java 8 바이트코드, JDBC 4.2 보고 | 실행 JDK를 Java 8 이상으로 사용합니다. |
| 드라이버 버전 | 드라이버와 메타데이터가 3.0.0 보고 | 버전 판별 로직을 갱신합니다. |
| 자동 검색 | JDBC 서비스 프로바이더 제공 | 명시적 `Class.forName()`은 선택 사항입니다. |
| ParameterMetaData | JDBC precision, DB 타입 이름과 Java 클래스 반환 | precision의 타입별 의미를 확인하고 저장 바이트 크기로 해석하지 않습니다. |
| 트랜잭션 | lazy `BEGIN`, 실제 commit/rollback | Standard TRANSACTION 작업을 명시적으로 완료합니다. |
| holdability | `CLOSE_CURSORS_AT_COMMIT` | 커밋 후 ResultSet을 다시 조회합니다. |
| DatabaseMetaData | 표준 결과 구조와 지원 기능 반환 | 드라이버 고유의 컬럼 순번 대신 표준 컬럼 이름을 사용합니다. |
| 타입 API | typed `getObject()`, `JDBCType`, Boolean, unsigned, LOB | 메타데이터의 Java 클래스로 조회·바인딩합니다. |
| 오류 | 잘못된 상태에서 표준 `SQLException` 반환 | SQLState로 오류를 분기합니다. |
| 시간 초과 | query/network 시간 초과 지원 | 네트워크 시간 초과 뒤 연결을 폐기합니다. |
| 커넥션 풀 | 논리 연결 대여 기간과 상태 초기화 | 닫힌 핸들과 메타데이터를 재사용하지 않습니다. |
| generated keys | Standard 단일 INSERT의 ROWID 반환 | `getGeneratedKeys()`의 `ROWID`를 읽습니다. |

이름 기반 bind는 호환 서버에서 사용합니다. 이전 서버가 이름 기반 bind를 지원하지 않으면
SQLState `0A000`이 발생하므로 `?` 위치 기반 매개변수로 전환합니다.

## 미지원 기능

다음 JDBC 선택 기능은 지원하지 않습니다.

- savepoint
- XA와 분산 트랜잭션
- 저장 프로시저와 CallableStatement 성공 경로
- scrollable 또는 updateable ResultSet
- Statement pooling
- multiple open results
- Struct, Ref, SQLXML과 UDT 타입 매핑
- 별도 NClob 스토리지와 factory
- Machbase 전용 RowSet 프로바이더
- JDBC 4.3 sharding과 request boundary API

Machbase DBMS 8.7.0과 ARRAY 지원 JDBC 빌드에서는 `java.sql.Array`, `createArrayOf()`와
`setArray()`를 사용할 수 있습니다. 기존 드라이버의 ARRAY 미지원 안내를 적용하지 말고
ARRAY와 선택 컬럼 Append의 버전과 인덱스 기준을 확인합니다.

미지원 기능은 일반적으로 `SQLFeatureNotSupportedException`과 SQLState `0A000`을
반환합니다. 기능을 호출하기 전에 DatabaseMetaData 기능을 확인합니다.

## `No suitable driver`

**증상**

`DriverManager.getConnection()`에서 `No suitable driver`가 발생합니다.

**확인 및 해결**

1. 실행 classpath에 `machbase.jar`가 있는지 확인합니다.
2. JAR에 `META-INF/services/java.sql.Driver`가 있는지 확인합니다.
3. URL이 `jdbc:machbase://<host>:<port>/machbasedb` 형식인지 확인합니다.
4. 여러 버전의 Machbase JDBC JAR가 동시에 포함되지 않았는지 확인합니다.

## SQLState `0A000`

선택한 기능이나 서버가 해당 API를 지원하지 않습니다. savepoint, scrollable 커서와
XA에는 대체 흐름을 사용합니다. generated keys는 Standard Edition과 ROWID를 지원하는
서버·JDBC 조합에서 사용하며, `DatabaseMetaData.supportsGetGeneratedKeys()`로 확인합니다.
이름 기반 bind에서 발생하면 위치 기반 매개변수인 `?`를 사용합니다.

## commit 이후 ResultSet이 닫힘

정상 동작입니다. Machbase의 트랜잭션 holdability는
`CLOSE_CURSORS_AT_COMMIT`입니다. 커밋 전에 결과를 소비하거나 커밋 후 쿼리를 다시
실행합니다. Statement와 PreparedStatement는 다시 사용할 수 있습니다.

## LOG DML이 rollback되지 않음

수동 트랜잭션에서 TRANSACTION 테이블을 변경하기 전에 실행한 첫 LOG DML은 호환
경로에서 auto-commit으로 재실행될 수 있습니다. 이 입력은 이후 롤백 대상이 아닙니다.
롤백이 필요한 데이터는 TRANSACTION 테이블을 사용합니다.

## 여러 TRANSACTION 테이블을 함께 commit

정상적인 커밋과 롤백은 지원하지만 백엔드 커밋 중 장애가 발생했을 때 여러
TRANSACTION 테이블의 전역 원자성을 보장하지 않습니다. 중요한 원자 작업은 하나의
TRANSACTION 테이블 범위로 설계합니다.

## network timeout 또는 연결 오류

소켓 읽기 시간 초과와 SQLState 클래스 `08` 연결 오류가 발생하면 해당 물리 연결을
재사용하지 않습니다. 커넥션 풀에서 새 연결을 대여하고, 활성 트랜잭션은 업무 멱등성
정책에 따라 처음부터 다시 실행합니다. 커밋 성공 여부를 예외만으로 추정하지 않습니다.

## close한 pool 객체 재사용

논리 Connection을 닫은 뒤 그 Connection에서 얻은 Statement, ResultSet과
DatabaseMetaData를 다음 연결 대여 기간에서 재사용하면 SQLState `08003`이 발생합니다. 각 연결 대여 기간의
객체를 try-with-resources 범위 안에서만 사용합니다.
