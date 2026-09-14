# Machbase Neo JavaScript MachCLI Module

`machcli` 모듈은 JSH 애플리케이션에 Machbase 클라이언트 API를 제공합니다.

## Client

데이터베이스 클라이언트를 만듭니다.

<h6>문법</h6>

```js
new Client(config)
```

<h6>설정 필드</h6>

- `host` (default: `127.0.0.1`)
- `port` (default: `5656`)
- `user` (default: `sys`)
- `password` (default: `manager`)
- `alternativeHost` (optional)
- `alternativePort` (optional)

<h6>사용 예제</h6>

```js
const { Client } = require('machcli');
const db = new Client({ host: '127.0.0.1', port: 5656, user: 'sys', password: 'manager' });
```

**Client.connect()**

연결을 열고 `Connection` 객체를 반환합니다.

**Client.close()**

내부 데이터베이스 클라이언트를 닫습니다.

**Client.user()**

설정된 사용자 이름을 대문자로 반환합니다.

**Client.normalizeTableName()**

테이블 이름을 `[database, user, table]` 형식으로 정규화합니다.

## Connection

`Client.connect()`가 반환하는 연결 객체입니다.

**Connection.query()**

SELECT 쿼리를 실행하고 `Rows` 객체를 반환합니다.

<h6>문법</h6>

```js
query(sql[, ...params])
```

<h6>사용 예제</h6>

```js
const { Client } = require('machcli');
var db, conn, rows;
const conf = {
  host: '127.0.0.1',
  port: 5656,
  user: 'sys',
  password: 'manager'
};
try {
  db = new Client(conf);
  conn = db.connect();
  rows = conn.query('SELECT NAME, TIME, VALUE FROM TAG LIMIT ?', 1);
  for (const row of rows) {
    console.println(row.NAME, row.TIME, row.VALUE);
  }
} catch( e ) {
  console.println("ERROR", e.message);
}
rows && rows.close();
conn && conn.close();
db && db.close();
```

**Connection.queryRow()**

쿼리를 실행하고 단일 행 객체를 반환합니다. 반환 객체는 `_ROWNUM`과 각 컬럼을 속성으로 포함합니다.

**Connection.exec()**

DDL/DML을 실행하고 `rowsAffected`와 `message`를 담은 결과 객체를 반환합니다.

**Connection.explain()**

실행 계획 문자열을 반환합니다.

**Connection.append()**

대량 입력을 위한 appender 객체를 만듭니다.

<h6>사용 예제</h6>

```js
const { Client } = require('machcli');
const db = new Client({ host: '127.0.0.1', port: 5656, user: 'sys', password: 'manager' });
const conn = db.connect();
const appender = conn.append('TAG');
appender.append('sensor-1', new Date(), 12.34);
appender.flush();
const result = appender.close();
console.println(result);
conn.close();
db.close();
```

**Connection.close()**

연결을 닫습니다.

## Rows

`Connection.query()`가 반환하는 결과 집합 객체입니다.

- `message` - 쿼리 실행 메시지.
- `isFetchable()` - 결과 집합에서 행을 가져올 수 있는지 반환합니다.
- `next()` - 반복자 결과 객체를 반환합니다.
- `close()` - 결과 집합을 닫습니다.

## Row

가져온 행 객체를 나타냅니다. 각 컬럼은 `row.COLUMN_NAME`으로 접근하며 `for...of` 순회를 지원합니다.

## queryDatabaseId()

마운트된 데이터베이스의 백업 테이블스페이스 ID를 반환합니다. 기본 데이터베이스는 `-1`을 반환합니다.

## queryTableType()

정규화된 테이블 이름 토큰으로 테이블 타입 코드를 반환합니다.

## TableType

테이블 타입 상수: `Log`, `Fixed`, `Volatile`, `Lookup`, `KeyValue`, `Tag`.

`stringTableType(type)`은 타입 코드를 문자열로 변환합니다.

## TableFlag

테이블 플래그 상수: `None`, `Data`, `Rollup`, `Meta`, `Stat`.

`stringTableFlag(flag)`는 플래그 코드를 문자열로 변환합니다.

`stringTableDescription(type, flag)`은 결합된 테이블 설명을 반환합니다.

## ColumnType

컬럼 타입 상수: `Short`, `UShort`, `Integer`, `UInteger`, `Long`, `ULong`, `Float`, `Double`, `Varchar`, `Text`, `Clob`, `Blob`, `Binary`, `Datetime`, `IPv4`, `IPv6`, `JSON`.

`stringColumnType(columnType)`은 타입 코드를 문자열로 변환합니다.

`columnWidth(columnType, length)`는 기본 표시 너비를 반환합니다.

## ColumnFlag

컬럼 플래그 상수: `TagName`, `Basetime`, `Summarized`, `MetaColumn`.

`stringColumnFlag(flag)`는 플래그 코드를 문자열로 변환합니다.
