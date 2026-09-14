# Node.js / TypeScript

## 개요

Machbase TypeScript 클라이언트(`@machbase/ts-client`)는 네이티브 바인딩 없이 Machbase
Standard Edition 서버에 연결하는 라이브러리입니다. Node.js 애플리케이션에서 SQL 실행,
결과 조회, Prepared Statement 처리, 로그 데이터 Append를 수행할 수 있습니다.

이 문서에서는 설치, 핵심 API, 예제, 테스트 흐름, 동작 특성을 다룹니다.

## 다중 데이터베이스

연결 설정 또는 URL의 `database` 값으로 초기 데이터베이스를 지정합니다. 카탈로그 getter는
제공하지 않으므로 SQL `CURRENT_DATABASE()`와 `USE`로 확인·변경합니다.

```typescript
const conn = createConnection({
  host: '127.0.0.1', port: 5656,
  user: 'APP_A', password: 'secret', database: 'FACTORY_A',
});
await conn.connect();
const [rows] = await conn.query('SELECT CURRENT_DATABASE()');
console.table(rows);
```

Appender와 준비된 문장은 open/prepare 시점의 데이터베이스에 고정됩니다. 세부 규칙은
다중 데이터베이스 운영 가이드를
참조하십시오.

## 설치

### 요구 사항

- Node.js 18 이상(LTS 권장)
- 접속 가능한 Machbase 서버(스탠더드 에디션)

### npm에서 설치

패키지 매니저로 설치합니다.

```bash
npm install @machbase/ts-client
# or
yarn add @machbase/ts-client
# or
pnpm add @machbase/ts-client
```

### 오프라인 설치

Machbase에서 `.tgz` 패키지를 전달받은 경우:

```bash
# example file name; your version may differ
npm install ./machbase-ts-client-<version>.tgz
```

### 설치 확인

```bash
node -e "const { createConnection } = require('@machbase/ts-client'); console.log(typeof createConnection === 'function' ? 'ts-client import ok' : 'ts-client import failed')"
```

> **참고**: 이 클라이언트는 Node.js에서 TCP 소켓을 사용하며, 브라우저용 라이브러리(웹소켓 전송)를 제공하지 않습니다.
> NFX `cce422d2972` 소스 트리의 `package.json`은 `@machbase/ts-client` 1.0.1입니다. 다만
> 이름 기반 bind·nullable·PK·ROWID·TRANSACTION 기능 일부는 공개 1.0.1 게시 뒤 같은 소스
> 버전 문자열 아래 추가되었습니다. npm 버전만으로 동일 기능을 가정하지 말고 배포 산출물의
> 커밋 출처를 확인하거나 이 NFX 소스에서 빌드하십시오.
>
> 이 문서의 기본 계정(`SYS`/`MANAGER`)은 로컬 테스트용 예시입니다. 운영 환경에서는 전용 계정과 비밀번호를 사용하십시오.

## 빠르게 시작하기

아래 예제는 로컬 서버에 연결해 시스템 테이블을 조회하고 세션을 종료합니다.

```typescript
// src/example.ts
import { createConnection } from '@machbase/ts-client';

const conn = createConnection({
  host: process.env.MACH_HOST ?? '127.0.0.1',
  port: +(process.env.MACH_PORT ?? 5656),
  user: process.env.MACH_USER ?? 'SYS',
  password: process.env.MACH_PASS ?? 'MANAGER',
});

await conn.connect();
const [rows] = await conn.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [5]);
console.log(rows);
await conn.end();
```

> **트랜잭션 안내:** 서버는 TRANSACTION 테이블에 plain `BEGIN`, `COMMIT`, `ROLLBACK` SQL을
> 지원합니다. 이 클라이언트의 `beginTransaction`, `commit`, `rollback` 편의 메서드는
> 구현되어 있지 않으므로 `execute()`로 SQL을 직접 실행해야 합니다.

## 자주 발생하는 문제

- **ECONNREFUSED** – 서버 상태(`machadmin -e`), 호스트와 포트, 방화벽의 리스너 포트
  허용 여부를 확인합니다. 기본 SQL 접속 포트는 5656입니다.
- **Authentication failed** – 사용자·비밀번호와 계정의 접속 권한을 확인하십시오.

## API 참조

### 연결 관리

#### createConnection(config)

Machbase 리스너에 연결하고 데이터베이스 세션을 생성합니다.

| 매개변수 | 타입 | 기본값 | 설명 |
|-----------|------|---------|-------------|
| `host` | 문자열 | `127.0.0.1` | Machbase 서버 IP 또는 호스트명 |
| `port` | number | `5656` | 리스너 포트 |
| `user` | 문자열 | – | 데이터베이스 사용자(기본 `SYS`) |
| `password` | 문자열 | – | 비밀번호(기본 `MANAGER`) |
| `database` | 문자열 | `data` | 데이터베이스 이름 |
| `clientId` | 문자열 | `NPM` | 서버 로그에 표시될 클라이언트 ID |
| `showHiddenColumns` | boolean | `false` | 메타데이터에 숨김 컬럼 포함 여부 |
| `timezone` | 문자열 | 빈 값 | 선택적 타임존 식별자 |
| `connectTimeout` | number | 5000 | 소켓 연결 타임아웃(ms) |
| `queryTimeout` | number | 60000 | 명령별 타임아웃(ms) |

```javascript
const conn = createConnection({ host: '192.168.1.10', user: 'SYS', password: 'MANAGER' });
await conn.connect();
```

소켓 연결 실패, 인증 오류, 핸드셰이크 응답 이상 시 프로미스가 reject됩니다.

#### connect()

서버와의 연결을 엽니다.

```javascript
await conn.connect();
```

#### end()

소켓 연결을 종료합니다. `end()` 호출 이후 추가 작업을 시도하면 에러가 발생합니다.

```javascript
await conn.end();
```

### SQL 실행

#### execute(sql, values?)

결과 집합을 반환하지 않을 수도 있는 명령을 실행합니다. DDL(`CREATE`, `ALTER`, `DROP`)이나 DML(`INSERT`, `UPDATE`, `DELETE`)에 사용하십시오.

```javascript
const [create] = await conn.execute('CREATE TRANSACTION TABLE demo (ID INTEGER, NAME VARCHAR(32))');
console.log('Rows affected:', create.affectedRows); // -> 0 for DDL

await conn.execute('BEGIN');
const [insert] = await conn.execute("INSERT INTO demo VALUES (1, 'alpha')");
console.log('Rows affected:', insert.affectedRows); // -> 1
await conn.execute('COMMIT');
```

Standard Edition에서 단일 `INSERT ... VALUES`가 성공하면 실행 결과의 `rowId`에 ROWID가
포함됩니다. 64비트 정밀도를 보존하기 위해 `number`가 아닌 `bigint`로 처리합니다.

```javascript
const [result] = await conn.execute(
  'INSERT INTO sensor_log(message) VALUES(?)',
  ['started']
);

if (result.rowId !== undefined) {
  const rowId = result.rowId; // bigint
}
```

ROWID가 없는 실행에는 `rowId` 값이 `undefined`입니다. 배치, Append, `INSERT ... SELECT`,
UPSERT의 차이는 ROWID와 INSERT 결과 ID를
참고하십시오.

#### query(sql, values?)

행을 반환하는 쿼리를 실행합니다. 반환값은 `[rows, fields]` 형태의 2요소 튜플입니다.

```javascript
const [rows, fields] = await conn.query('SELECT ID, NAME FROM demo ORDER BY ID');
console.table(rows);
```

#### Named Bind Parameter

`execute()`, `query()`와 Prepared Statement의 `execute()`에서 배열은 위치 기반 입력,
plain object는 이름 기반 입력입니다.

```typescript
export type MachbaseNamedBindInput =
  Record<string, MachbaseBindInput>;
export type MachbaseExecuteInput =
  MachbaseBindInput[] | MachbaseNamedBindInput;
```

```javascript
await conn.execute(
  'INSERT INTO demo (ID, NAME) VALUES (:id, :name)',
  { id: 1, name: 'node-client' },
);

const [rows] = await conn.query(
  'SELECT ID, NAME FROM demo WHERE ID = :id OR PARENT_ID = :id',
  { id: 1 },
);
```

Prepared Statement에서도 객체를 전달합니다.

```javascript
const stmt = await conn.prepare(
  'SELECT ID, NAME FROM demo WHERE ID = :id'
);
try {
  const [rows] = await stmt.execute({ id: 1 });
} finally {
  await stmt.close();
}
```

객체 키는 선행 콜론 없이 지정하며 대소문자를 구분합니다. 반복된 이름에는 같은 값이
적용됩니다. 객체 입력과 `?` 자리표시자를 함께 사용하거나, 필요한 키를 누락하거나, SQL에
없는 키를 전달하면 오류를 반환합니다.

| 오류 코드 | 상황 |
|---|---|
| `ERR_MACHBASE_BIND_MISSING` | 필요한 이름이 누락됨 |
| `ERR_MACHBASE_BIND_EXTRA` | SQL에 없는 이름을 전달함 |
| `ERR_MACHBASE_BIND_MIXED` | 이름 기반 자리표시자와 anonymous 자리표시자를 혼용함 |
| `ERR_MACHBASE_NAMED_BIND_UNSUPPORTED` | 서버가 이름 기반 바인딩을 지원하지 않음 |

`fields`의 각 `ColumnMeta` 객체는 `nullable` 속성을 제공합니다.

```typescript
import { ColumnNullable } from '@machbase/ts-client';

const [rows, fields] = await conn.query(
  'SELECT ID, NAME, ID + 1 AS EXPR_VALUE FROM demo ORDER BY ID'
);

for (const field of fields) {
  if (field.nullable === ColumnNullable.NoNulls) {
    console.log(field.name, 'NO_NULLS');
  } else {
    console.log(field.name, 'NULL 처리 필요');
  }
}
```

| 열거형 | 숫자 값 | 의미 |
|--------|:------:|------|
| `ColumnNullable.NoNulls` | `0` | NULL이 될 수 없음 |
| `ColumnNullable.Nullable` | `1` | NULL이 될 수 있음 |
| `ColumnNullable.Unknown` | `2` | 판정할 수 없음 |

`ColumnNullable.Unknown`은 `NOT NULL`을 의미하지 않습니다. NULL이 발생할 수 있는 것으로
처리합니다. SQL 결과의 판정 규칙은
Nullable 메타데이터 지원 범위를
참고합니다.

Machbase SQL에서 `''`은 SQL `NULL`이므로 해당 `field.nullable`은
`ColumnNullable.Nullable`이고 결과 행의 값은 JavaScript `null`입니다. 반대로 `''''`는
작은따옴표 한 글자이므로 `ColumnNullable.NoNulls`와 문자열 값 `'`을 반환합니다.

### SELECT 결과의 PRIMARY KEY 메타데이터

Machbase 8.7.0 서버와 해당 버전 SDK를 사용하면 `query()` 또는 `execute()`가 반환하는
`fields` 배열의 `isPrimaryKey`에서 직접 컬럼의 PRIMARY KEY 여부를 확인할 수 있습니다.

```ts
const [rows, fields] = await conn.query(
  'SELECT ID, VALUE, ID + 1 AS ID_EXPR FROM T_PK'
);
for (const field of fields) {
  console.log(field.name, field.isPrimaryKey);
}
```

표현식·집계식·외부 조인의 NULL 공급 측 컬럼은 `false`입니다. 이전 버전 서버 또는 SDK와
연결한 경우에는 PK 플래그가 제공되지 않을 수 있습니다.

### Prepared Statement 사용

#### prepare(sql)

서버에 Prepared Statement를 생성합니다.

```javascript
const stmt = await conn.prepare('SELECT NAME FROM demo WHERE ID = ?');
try {
  const [rows] = await stmt.execute([1]);
  console.log(rows); // -> [ { NAME: 'alpha' } ]
} finally {
  await stmt.close();
}
```

반환된 객체에서 제공하는 메서드는 다음과 같습니다.

- `execute(parameters?)` – 문을 실행하고 `[rowsOrPacket, fields]`를 반환합니다.
- `getColumns()` – 컬럼 메타데이터 캐시를 반환합니다.
- `getLastMessage()` – 최근 서버 메시지를 확인합니다.
- `getStatementId()` – 내부 Statement ID를 조회합니다.
- `close()` – 서버 리소스를 정리합니다. 여러 번 호출해도 안전합니다.

`getColumns()`가 반환하는 `ColumnMeta`에도 같은 `nullable` 값이 포함됩니다.

```typescript
const stmt = await conn.prepare('SELECT ID, NAME FROM demo WHERE ID = ?');
for (const column of stmt.getColumns()) {
  console.log(column.name, ColumnNullable[column.nullable]);
}
```

#### Prepared Statement Examples

**Prepared SELECT 재사용:**

```javascript
const select = await conn.prepare('SELECT DEVICE_ID, SENSOR_VALUE FROM sensors WHERE DEVICE_ID = ?');
for (const { id } of samples) {
  const [rows] = await select.execute([id]);
  console.log(`selected ${id}:`, rows);
}
await select.close();
```

**Prepared Upsert:**

```javascript
const upsert = await conn.prepare(
  'INSERT INTO devices (DEVICE_ID, SENSOR_VALUE) VALUES (?, ?) ' +
  'ON DUPLICATE KEY UPDATE SET SENSOR_VALUE = ?',
);
const [result] = await upsert.execute([deviceId, firstValue, firstValue]);
console.log('Affected rows:', result.affectedRows);
await upsert.close();
```

**타입 지정 인자와 NULL 처리:**

```javascript
await update.execute([
  { value: null, type: 'varchar' },
  { value: new Date(), type: 'varchar' },
  { value: 'sensor-200', type: 'varchar' },
]);
```

실행 예제 스크립트는 보통 `npm run build` 후 `dist/examples/` 아래에 생성됩니다. 예제는 일반적으로 `MACHBASE_EXAMPLE_*`, `MACHBASE_SMOKE_*`, 마지막으로 `SYS/MANAGER@127.0.0.1` 순서로 접속 정보를 찾습니다.

### API 참조 Append API

#### appendBatch(table, columns, rows, options?)

`appendBatch()`로 **로그 테이블**에 여러 행을 추가합니다. 사용자에게 보이는 컬럼만
전달하면 됩니다(로그 테이블에는 `_arrival_time`,
`_rid`가 자동 포함됩니다).

```javascript
const appendResult = await conn.appendBatch(
  'sensor_log',
  [
    { name: 'ID', type: 'int32' },
    { name: 'NAME', type: 'varchar' },
    { name: 'VALUE', type: 'float64' },
  ],
  [
    [1, 'alpha', 0.5],
    { values: [2, 'bravo', 1.25], arrivalTime: BigInt(Date.now()) * 1_000_000n },
  ],
);
console.log('Appended rows:', appendResult.rowsAppended);
```

지원 컬럼 타입: `int32`, `int64`, `float64`, `varchar`.

- `rows`는 값 배열 또는 `{ values, arrivalTime }` 객체 배열을 받을 수 있습니다. `null`은 Machbase 센티널 값으로 자동 인코딩됩니다.
- `options`는 `arrivalTime`(기본값 1개) 또는 `arrivalTimes`(행별 배열)를 지정할 수 있습니다.
- epoch 나노초를 직접 계산할 때는 먼저 `bigint`로 변환합니다. `number` 곱셈은 안전한
  정수 범위를 넘습니다.

반환값은 `{ table, rowsAppended, rowsFailed, message }` 형태입니다.

> **팁**: "컬럼 건수 does not match" 오류는 대상 테이블이 로그 테이블이 아니거나, 컬럼 순서가 스키마와 일치하지 않을 때 발생합니다. TAG 테이블에는 `appendOpen()`을 사용하십시오.

#### appendOpen(table, columns, options?)

경량 Append 세션을 엽니다. 기본적으로 네이티브 APPEND open/data/close 흐름을 사용하며, 성공한 네이티브 쓰기는 청크별 응답을 반환하지 않습니다.

```javascript
const stream = await conn.appendOpen('sensor_log', [
  { name: 'ID', type: 'int32' },
  { name: 'NAME', type: 'varchar' },
  { name: 'VALUE', type: 'float64' },
]);

await stream.append([
  [1, 'alpha', 0.5],
  [2, 'bravo', 1.25],
]);

await stream.append({ values: [3, 'charlie', 2.5] });
await stream.close();
```

네이티브 Append를 끄고 Prepared Statement 기반으로 강제하려면 `MACHBASE_NATIVE_APPEND=0`을 설정하십시오. 서버가 특정 테이블 타입이나 세션에서 네이티브 Append를 지원하지 않으면 페이사드가 자동으로 Prepared Statement 방식으로 폴백합니다.

TAG 테이블의 `DATETIME` 컬럼에는 `Date` 객체 또는 `bigint` epoch 값을 전달하십시오.

희소 ARRAY는 `appendOpen()`의 ARRAY 값으로 전달할 수 있습니다. 현재
`@machbase/ts-client`는 `columns` 인자가 필수이므로, 전체 행을 입력할 때도 테이블의 입력
컬럼을 순서대로 정의합니다. `appendOpen(table)`이나 빈 컬럼 목록을 통한 자동 추론은
지원하지 않습니다. 아래 예제의 `ID`, `A`가 테이블의 전체 입력 컬럼이면 전체 행 입력입니다.
ARRAY 안에서 입력할 위치는 각 행의 `SparseArray`가 결정합니다.

연결부터 네 행 입력·Close·조회까지의
전체 컬럼 정의 예제를 참고하십시오.

Machbase DBMS 8.7.0의 선택 컬럼 Append에서는 `name`에 일반 컬럼 또는
`ARRAY_COLUMN[position]`을 지정합니다. 행마다 다른 위치를 입력할 때는
`SparseArray`를 배열 전체 대상에 전달합니다. 요소 위치를 지정한 대상과
`SparseArray.set()`의 위치는 0부터 시작하는 인덱스입니다.

```javascript
const { SparseArray } = require('@machbase/ts-client');

const stream = await conn.appendOpen('array_append_example', [
  { name: 'ID', type: 'int64' },
  { name: 'A', type: 'int32-array' },
]);
const sparse = new SparseArray(4).set(1, 200).set(3, 400);
await stream.append([[2n, sparse]]);
await stream.close();
```

`MACHBASE_NATIVE_APPEND=0`으로 prepared 대체 경로를 강제해도 `SparseArray`를
ARRAY-compatible 값으로 처리합니다. 전체 예제와 NULL 구분은
Sparse ARRAY와 선택 컬럼 Append API를
참고하십시오.

#### append(rows) on an append stream

열린 Append 스트림으로 하나 이상의 행을 전송합니다.

```javascript
const frames = await stream.append([
  ['S-001', new Date(), 1.0],
  ['S-002', new Date(Date.now() + 1), 2.0],
]);
console.log('frames sent:', frames);
```

네이티브 모드에서는 최대 처리량을 위해 성공 응답이 생략되며, 오류가 있을 때만 실패 패킷이 반환됩니다.

### Helper Methods

#### ping()

`SELECT 1 FROM V$TABLES`로 연결 상태를 점검합니다.

```javascript
await conn.ping();
```

#### promise()

익숙한 `.promise()`와 같은 형태의 래퍼를 제공합니다.

```javascript
const p = conn.promise();
await p.ping();
const [rows] = await p.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [5]);
```

#### escape, escapeId, format

SQL 문자열을 안전하게 구성하기 위한 유틸리티입니다.

```javascript
const safeName = conn.escapeId('table_name');
const safeValue = conn.escape('user input');
```

## 테스트 및 진단

### 스크립트

- `npm run build` – TypeScript 컴파일
- `npm run lint` – `src/`에 ESLint 수행
- `npm run smoke` – 선택적 스모크 테스트(환경변수 없으면 생략)
- `npm test` – 통합 스위트(실서버 필요)
  1. 로그 테이블 생성
  2. 샘플 데이터 INSERT/SELECT
  3. 자리기반 바인딩 준비문 시연
  4. append 부하 테스트(기본: 5배치 x 200행) 및 건수 검증
  5. TRANSACTION 테이블에서 직접 SQL `BEGIN`/`ROLLBACK`/`COMMIT` 동작 확인
  6. Machbase 페이사드와 `UPDATE` 제한 동작 검증

샘플 출력:

```text
TRANSACTION transaction commit returned 1 row.
machbase-facade-basic callback query returned 3 rows.
machbase-facade-update-log-fails message: UPDATE is not supported for LOG tables.
append-batch progress: batch 4/5 { table: 'TS_CLIENT_IT_...', rowsAppended: 200, rowsFailed: 0 }
append-batch final count: 1004
```

## 튜토리얼

### 빠른 시작 (로그 테이블)

```javascript
// quickstart-log.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', port: 5656, user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  const table = 'JS_LOG_' + Math.random().toString(36).slice(2, 7).toUpperCase();
  try {
    await conn.execute(`CREATE LOG TABLE "${table}" (ID INTEGER, NAME VARCHAR(64), VALUE DOUBLE)`);
    await conn.execute(`INSERT INTO "${table}" VALUES (1, 'A', 0.5)`);
    const [rows] = await conn.query(`SELECT * FROM "${table}" ORDER BY ID`);
    console.table(rows);
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

### Prepared Statement 재사용

```javascript
// prepared-reuse.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  const table = 'JS_VOL_' + Math.random().toString(36).slice(2, 7).toUpperCase();
  try {
    await conn.execute(`CREATE VOLATILE TABLE "${table}" (ID INTEGER PRIMARY KEY, NAME VARCHAR(64))`);
    for (let i = 1; i <= 3; i++) await conn.execute(`INSERT INTO "${table}" VALUES (${i}, 'N${i}')`);
    const stmt = await conn.prepare(`SELECT NAME FROM "${table}" WHERE ID = ?`);
    try {
      for (const id of [1, 2, 3]) {
        const [rows] = await stmt.execute([id]);
        console.log(id, rows[0]?.NAME);
      }
    } finally {
      await stmt.close();
    }
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

### 로그 테이블 배치 Append

```javascript
// append-batch.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  const table = 'JS_LOGAPP_' + Math.random().toString(36).slice(2, 7).toUpperCase();
  try {
    await conn.execute(`CREATE LOG TABLE "${table}" (ID INTEGER, NAME VARCHAR(64), VALUE DOUBLE)`);
    const result = await conn.appendBatch(
      table,
      [
        { name: 'ID', type: 'int32' },
        { name: 'NAME', type: 'varchar' },
        { name: 'VALUE', type: 'float64' },
      ],
      [[1, 'X', 0.5], [2, 'Y', 1.25]],
    );
    console.log(result);
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

### TAG 테이블 스트리밍 Append

```javascript
// append-tag-stream.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  const table = 'JS_TAG_' + Math.random().toString(36).slice(2, 7).toUpperCase();
  try {
    await conn.execute(`CREATE TAG TABLE "${table}" (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED)`);
    const stream = await conn.appendOpen(table, [
      { name: 'NAME', type: 'varchar' },
      { name: 'TIME', type: 'int64' },
      { name: 'VALUE', type: 'float64' },
    ]);
    const now = Date.now();
    await stream.append([
      ['T-0001', new Date(now), 1.0],
      ['T-0002', new Date(now + 1), 2.0],
    ]);
    await stream.close();
    const [rows] = await conn.query(`SELECT COUNT(*) AS CNT FROM "${table}"`);
    console.log('count', rows[0]?.CNT);
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

> 네이티브 모드는 기본 활성화입니다. 비활성화하려면 `MACHBASE_NATIVE_APPEND=0`을 설정하십시오. 성공 시 청크별 응답은 생략되고, 오류만 실패 응답으로 전달됩니다.

### Promise 래퍼와 Ping

```javascript
// promise-and-ping.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  try {
    const p = conn.promise();
    await p.ping(); // SELECT 1 FROM V$TABLES
    const [rows] = await p.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [5]);
    console.log(rows.map(r => r.NAME));
  } finally {
    await conn.end();
  }
})();
```

## 동작 특성과 한계

### 트랜잭션

서버 SQL 트랜잭션은 TRANSACTION 테이블에서 동작하지만, 페이사드의 트랜잭션 편의 메서드는
구현되어 있지 않습니다. 동일한 연결에서 SQL을 직접 실행합니다.

```javascript
await conn.execute('BEGIN');
await conn.execute('UPDATE orders SET status = ? WHERE order_id = ?', ['DONE', 1001]);
await conn.execute('COMMIT');
```

### 결과 버퍼링 및 페이지네이션

래퍼의 `query` 메서드는 전체 결과 집합을 버퍼링한 뒤 반환합니다. 대용량 테이블에서는 `ORDER BY … LIMIT` 쿼리나 기본 키 범위를 이용해 직접 페이지를 나누십시오.

### 파라미터 바인딩

배열 입력은 `?` 위치 기반 자리표시자에, 객체 입력은 `:name` 자리표시자에 바인딩합니다.
지원 타입은 `int32`, `int64`, `float64`, `varchar` 등 범용 스칼라 타입입니다.
`null`을 전달할 경우 명시적 타입을 함께 지정하십시오.

```javascript
{ value: null, type: 'varchar' }
```

이름 규칙과 최대 파라미터 수는
Named Bind Parameter syntax를
참고하십시오.

### 동작 특성과 한계 Append API

로그 테이블에는 `appendBatch`를, 점진적 입력에는 `appendOpen`/`append`를 사용합니다. 특정
테이블 타입(예: TAG 테이블)에서 이 입력 방식을 지원하지 않으면 준비된 문 반복 방식으로
자동 대체됩니다. 운영 시에는 데이터를 청크로 나누고 `rowsFailed`를 확인합니다.

### 오류 처리

오류는 기본 `Error` 객체(래퍼 사용 시 `QueryError`)로 전달됩니다. 문제를 진단하려면 `error.message` 또는 `QueryError`의 `code`, `sql` 필드를 확인하십시오. 통합 테스트는 존재하지 않는 테이블 조회와 지원하지 않는 `UPDATE`를 일부러 실행해 오류 메시지가 충분히 설명적인지 확인합니다.

### 테이블 타입별 SQL 유의사항

- **LOG 테이블**은 `UPDATE`를 지원하지 않습니다.
- **TAG 테이블**의 데이터 UPDATE는 Standard Edition에서만 지원합니다. 태그 선택 조건과
  BASETIME 조건이 필요하며, 태그명·시간축·메타데이터 컬럼은 데이터 UPDATE의 SET 대상이 될 수
  없습니다. SET 우변에서 기존 행 컬럼을 참조할 수 없습니다.
- **VOLATILE 테이블**의 UPDATE/DELETE는 기본 키 조건을 사용합니다. **LOOKUP 테이블**은 기본 키
  조건과 일반 조건식을 모두 지원하며, 단건 변경에는 기본 키 조건이 효율적입니다.

## 모범 사례

1. **항상 연결을 닫기**: `try...finally` 블록으로 `conn.end()`가 호출되도록 보장하십시오.
2. **Prepared Statement 재사용**: 한 번 생성한 후 여러 번 실행하면 성능이 향상됩니다.
3. **배치 입력 활용**: 단건 INSERT 대신 `appendBatch`나 `appendOpen`으로 대량 적재를 수행하십시오.
4. **오류 처리**: DB 작업을 `try...catch`로 감싸고 적절히 로깅합니다.
5. **커넥션 풀 사용**: 운영 환경에서는 커넥션 풀을 도입해 동시 요청을 안정적으로 처리하십시오.
6. **쿼리 파라미터화**: SQL 인젝션을 방지하려면 문자열 결합 대신 바인딩(`?` 플레이스홀더)을 사용하십시오.
