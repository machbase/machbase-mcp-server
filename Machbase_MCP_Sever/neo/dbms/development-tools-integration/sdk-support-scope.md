# SDK 기능 지원 범위

애플리케이션 요구사항에 맞는 SDK를 선택할 수 있도록 기능별 지원 여부와 API 진입점을
비교합니다. 설치, 연결, 함수와 실행 코드는 각 SDK 페이지를 참고합니다.

SDK를 처음 고를 때는 연동 방식 선택을 먼저 읽고, 이
페이지에서는 필요한 기능과 정확한 API 경로를 대조합니다.

## Nullable 메타데이터

Machbase는 SELECT 결과 컬럼의 NULL 가능성을 `NO_NULLS`, `NULLABLE`, `UNKNOWN`으로
구분합니다. 애플리케이션은 `NULLABLE`과 `UNKNOWN`을 모두 NULL 처리 대상으로 가정합니다.

| SDK | 조회 방법 |
|---|---|
| JDBC | `ResultSetMetaData.isNullable()` |
| Python | `cursor.description[i][6]` |
| Go 네이티브 | `api.Column.Nullability` |
| Go `database/sql` | `Rows.ColumnTypeNullable()` |
| Node.js | `ColumnMeta.nullable` |
| .NET | `GetSchemaTable()`의 `AllowDBNull` |
| SQLCLI·ODBC | 디스크립터의 nullable 속성 |

표현식, 집계, VIEW와 JOIN 결과는 `UNKNOWN`이 될 수 있습니다. 직접 컬럼의 스키마 제약과
조회 결과 메타데이터를 같은 것으로 가정하지 마십시오.

## PRIMARY KEY 메타데이터

| SDK | 결과 컬럼 | 테이블 카탈로그 |
|---|:---:|:---:|
| JDBC | O | `DatabaseMetaData.getPrimaryKeys()` |
| Python | O | 카탈로그 SQL |
| Go 네이티브 | O | 카탈로그 SQL |
| Go `database/sql` | 표준 API 없음 | 카탈로그 SQL |
| Node.js | O | 카탈로그 SQL |
| .NET | O | 카탈로그 SQL |
| ODBC | 별도 결과 API 없음 | `SQLPrimaryKeys()` |

표현식·집계·외부 JOIN의 NULL 공급 측은 원본 컬럼의 PK 속성을 그대로 전달하지 않을 수
있습니다.

## INSERT 결과 ROWID

Machbase 8.7.0 Standard Edition에서 성공한 단일 `INSERT ... VALUES`는 지원 SDK에 ROWID를
제공할 수 있습니다.

| SDK·도구 | 확인 방법 | 값이 없을 때 |
|---|---|---|
| machsql | `SHOW LAST ROWID` | `NULL` |
| Machbase SQLCLI | `SQLGetGeneratedRowID()` | `SQL_NO_DATA` |
| 표준 ODBC | 전용 표준 API 없음 | - |
| JDBC | `Statement.getGeneratedKeys()` | 빈 `ResultSet` |
| Python | `cursor.lastrowid` | `None` |
| .NET | `MachCommand.RowId` | `null` |
| Go `database/sql` | `Result.LastInsertId()` | 오류 |
| Go 네이티브 | 미지원 | - |
| Node.js | 실행 결과 `rowId` | `undefined` |

배치, `executemany()`, Append, loader, `INSERT ... SELECT`와 UPSERT에서는 단일 ROWID를
반환하지 않습니다. SQL 의미와 테이블별 제약은 ROWID를
참고하십시오.

## Append API와 table type

| API 경로 | LOG | TAG | LOOKUP | VOLATILE | TRANSACTION | 기준 |
|---|:---:|:---:|:---:|:---:|:---:|---|
| SQLCLI `SQLAppend*` extension | O | O | O | O | O | TRANSACTION은 Standard |
| JDBC `MachStatement.executeAppend*` | O | O | O | O | O | NFX cce422d source/test |
| Python 2.4 `append*` | O | O | O | O | O | NFX cce422d source/test |
| .NET `MachAppendWriter` | O | O | O | O | O | NFX cce422d 프로바이더 |
| Go v1.8.4 네이티브 `Appender` | O | O | X | X | O | TRANSACTION은 Standard |
| Go `database/sql` 표준 API | X | X | X | X | X | `sql.Conn.Raw()` 확장은 네이티브 계약 |
| Node 소스 `appendBatch()` | O | △ | △ | △ | O | NFX cce422d 소스 빌드 |
| Node 소스 `appendOpen()` | O | O | △ | △ | △ | 범용 native/fallback, 테이블별 검증 필요 |

표준 쿼리 연결과 Append 핸들의 생명 주기를 구분하고 close·flush 결과를
확인합니다. `O`는 해당 source/test에서 확인된 범위이고 `△`는 범용 경로만 있어 테이블별
회귀 검증이 더 필요한 범위입니다. Append extension은 표준 ODBC나 `database/sql` 기능이
아닙니다.

### ARRAY와 선택 컬럼 Append

Machbase DBMS 8.7.0의 ARRAY 지원 범위는 다음과 같습니다.

| SDK | 밀집 ARRAY 조회·입력 | 희소 ARRAY | 선택 컬럼 Append |
|---|:---:|:---:|:---:|
| SQLCLI·C++ | O | O | O |
| Machbase ODBC extension | O | O | O |
| JDBC | O | O | O |
| Python | O | O | O |
| Node.js | O | O | O |
| .NET full/legacy 프로바이더 | O | O | O |
| Go | v2 main 소스 | v2 main 소스 | v2 main 소스 |

Machbase DBMS 8.7.0 서버와 ARRAY 기능이 포함된 SDK 빌드를 함께 사용합니다. ARRAY의 SQL
요소 위치와 Machbase 전용 SDK 위치는 0부터 시작하는 인덱스입니다. 기존 전체 행 scalar Append
API는 유지됩니다. Node.js prepared 대체 경로도 `SparseArray`를 지원합니다. Go는
`neo-client` PR #17 (https://github.com/machbase/neo-client/pull/17) 이후의 v2 main
소스를 사용해야 하며 공개 v2 릴리스가 지정되기 전에는
공개 모듈 버전만으로 지원을 가정하지 않습니다. 자세한 입력 방식과 API는
Sparse ARRAY와 선택 컬럼 Append API를
참고하십시오.

## AUTH KEY

| SDK·도구 | 지원 |
|---|:---:|
| machsql, Machbase SQLCLI, ODBC, JDBC | O |
| Go 네이티브, Go `database/sql` | O (neo-client v1.5.0+) |
| Python, Node.js, .NET | X |

키 생성·등록·교체는 AUTH KEY 인증을,
연결 옵션은 지원 SDK 페이지를 참고합니다.

## Transaction, prepare와 bind

| SDK | Transaction API | Server prepared | Named bind API |
|---|:---:|:---:|:---:|
| JDBC | O | O | △ (Machbase extension) |
| Python | X | O | O |
| Go 네이티브 | △ | O | O |
| Go `database/sql` | O | O | O |
| .NET | X | X | △ |
| Node.js | X | O | O |
| SQLCLI | △ | O | O |
| ODBC | △ | O | 순번 bind |

준비된 문장(prepared statement)과 매개변수 바인딩은 트랜잭션 지원과 별개입니다. 자리표시자 문법은
Named Bind Parameter를
참고하십시오.

Machbase 8.7.0 Standard Edition의 TAG 데이터 UPDATE는 각 SDK의 기존 positional/named API로
NAME과 BASETIME 조건 값을 바인딩할 수 있습니다. NFX #4127 회귀 테스트는 C/C++ SQLCLI,
Go `database/sql`, JDBC, Node.js, Python과 .NET 경로를 검증합니다. ODBC는 별도 SDK 회귀
매트릭스에 포함되지 않으며 `?` 또는 이름 기반 SQL의 자리표시자를 표준 `SQLBindParameter()` 순번으로
바인딩합니다. TAG UPDATE 조건 계약은
TAG 데이터 UPDATE bind를
참고합니다.

Transaction 열의 `△`는 전용 객체 대신 같은 연결에서 트랜잭션 SQL을 직접 실행하는
경로입니다. Named bind 열의 `△`는 표준 이름 기반 바인딩 API가 아니라 드라이버 확장
또는 클라이언트가 값을 SQL 리터럴로 변환하는 경로를 뜻합니다.

## 최소 확인 version과 provenance

| SDK | 이 문서의 확인 기준 |
|---|---|
| SQLCLI·JDBC·Python | NFX `cce422d2972`; Python 패키지 2.4 |
| Node.js | NFX `cce422d2972` 소스 빌드 (`package.json` 1.0.1) |
| .NET | Uni 8.0.55, limited 3.1.3, full 3.2.2 |
| Go | released neo-client v1.8.4; AUTH KEY는 v1.5.0+, 데이터베이스 선택은 v1.8.3+ |

NFX cce422d의 Node 기능 일부는 공개 npm 1.0.1 배포 이후 추가되었습니다. registry 패키지의
버전 문자열만으로 동일 기능을 가정하지 말고 배포 산출물의 커밋 출처를
확인하거나 NFX 소스 빌드를 사용합니다.

ARRAY와 선택 컬럼 Append의 확인 기준은 NFX
`655d1333870313c4951698b89c9a3c9ada11d630`과 병합 커밋
`f756986c4836982723e2aa7727ec05b7e05e9707`입니다. 서버는 Machbase DBMS 8.7.0을,
클라이언트는 해당 변경 이후의 검증된 SDK 산출물을 기준으로 판단합니다.

## SDK 레퍼런스

| SDK | 상세 문서 |
|---|---|
| Machbase SQLCLI·ODBC | SQLCLI와 ODBC |
| JDBC | JDBC |
| Python | Python |
| Node.js / TypeScript | Node.js / TypeScript |
| .NET Connector | .NET Connector |
| Go | Go |
