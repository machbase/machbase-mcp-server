# Machbase TypeScript Client (npm)

The Machbase TypeScript client (`@machbase/ts-client`) is a pure TypeScript
implementation of the Machbase CMI protocol. It allows Node.js applications to
connect to a Machbase (standard edition) server, execute SQL statements, fetch
results, work with prepared statements, and append batches of log data without
native bindings.

This document is the English-language product manual for the npm package. It
covers installation, core APIs, practical examples, and important behavioural
notes so that new users can get productive quickly.

---

## 0. End‑User Install (from the Web)

Most users should install the prebuilt package from the npm registry, not build
from source.

Requirements:

- Node.js 18 or newer (LTS recommended)
- A reachable Machbase server (standard edition)

Install via your package manager:

```bash
npm install @machbase/ts-client
# or
yarn add @machbase/ts-client
# or
pnpm add @machbase/ts-client
```

Offline/air‑gapped install (if you received a `.tgz` file from Machbase):

```bash
# example file name; your version may differ
npm install ./machbase-ts-client-0.9.0.tgz
```

Usage (ESM/TypeScript):

```ts
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

Notes:

- This client targets Node.js and uses TCP sockets; it is not a browser library
  (no WebSocket transport).
- Default credentials shown here (`SYS`/`MANAGER`) are for local testing only.
  Use dedicated users/passwords in production.

Common issues and fixes:

- ECONNREFUSED – Verify the server is started (`machadmin -u`) and the host/port
  are correct, and that firewalls permit TCP to the listener port (default 5656).
- Authentication failed – Check user/password and that the target database is
  created (`machadmin -c`).

—

## 1. Installation & Project Layout

```bash
cd npm/machbase-client
npm install       # install local dependencies
npm run build     # compile TypeScript sources into dist/
```

Key directories:

```
npm/machbase-client/
├─ package.json            # scripts: build / lint / test / smoke
├─ src/
│   ├─ connection.ts       # core protocol engine (internal)
│   ├─ machbase.ts         # createConnection facade
│   ├─ constants.ts        # protocol constants and helper flags
│   ├─ marshal.ts          # marshal encoder/decoder utilities
│   ├─ example-js/         # runnable CommonJS examples (Node)
│   ├─ examples-ts/        # TypeScript examples (compiled to dist/examples-ts)
│   └─ tests/
│       └─ integration.ts  # end-to-end verification suite
└─ dist/                   # compiled JavaScript + type declarations
```

---

## 2. Quick Start

```js
// quickstart.js (CommonJS, Node 18+)
const { createConnection } = require('@machbase/ts-client');

async function main() {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER', port: 5656 });
  await conn.connect();

  const [rows] = await conn.query('SELECT * FROM v$tables ORDER BY NAME LIMIT ?', [10]);
  console.table(rows);

  await conn.end();
}

main().catch(err => console.error('Unexpected failure:', err));
```

> **Transaction notice:** Machbase autocommits every statement. Commands such as
> `BEGIN`, `COMMIT`, or `ROLLBACK` always return an error and should only be used
> to detect the lack of transaction support.

### 2.1 Machbase facade

For applications that prefer the Machbase facade, the client now
exposes a familiar surface via `createConnection`:

```js
// facade-basic.js (CommonJS)
const { createConnection } = require('@machbase/ts-client');

async function bootstrap() {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  try {
    const [rows, fields] = await conn.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [3]);
    console.log('rows', rows, 'fields', fields?.map(f => f.name));

    await new Promise((resolve, reject) =>
      conn.query('SELECT VALUE FROM v$sysstat WHERE NAME = ?', ['SERVER_VERSION'], (err, result) => {
        if (err) return reject(err);
        console.log('callback result', result);
        resolve();
      })
    );
  } finally {
    await conn.end();
  }
}

bootstrap().catch(console.error);
```

The facade honours both callback and promise flows (via `.promise()`), surfaces
`QueryError` instances when operations fail, and forwards server messages.

> ⚠️ `beginTransaction`, `commit`, and `rollback` report `QueryError` immediately
> because Machbase does not support SQL transactions. `UPDATE` statements aimed
> at LOG or TAG tables likewise fail fast with an explicit error from the server.

---

## 3. API Reference

The public surface area is exposed through the connection facade returned by `createConnection` and a
handful of helper types. Each function below is explained with parameters,
behaviour notes, and example code.

### 3.1 `createConnection(config)` and `connect()`

Establishes a network session to the Machbase listener and completes the CMI
handshake.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `host` | string | `127.0.0.1` | IP or hostname of the Machbase server |
| `port` | number | `5656` | Listener port |
| `user` | string | – | Database user (commonly `SYS`) |
| `password` | string | – | Password (commonly `MANAGER`) |
| `database` | string | `data` | Database name |
| `clientId` | string | `CLI` | Client identifier shown in server logs |
| `showHiddenColumns` | boolean | `false` | Include hidden columns in metadata |
| `timezone` | string | empty | Optional time zone identifier |
| `connectTimeout` | number | 5000 | Socket connect timeout (ms) |
| `queryTimeout` | number | 60000 | Per-command timeout (ms) |

```js
const conn = createConnection({ host: '192.168.1.10', user: 'SYS', password: 'MANAGER' });
await conn.connect();
```

The promise rejects if the socket fails, authentication fails, or the handshake
response is unexpected.

### 3.2 `execute(sql, values?)`

Runs a statement that does not necessarily return rows. Use it for DDL
(`CREATE`, `ALTER`, `DROP`) or data modification (`INSERT`, `UPDATE`, `DELETE`).

```js
const [create] = await conn.execute('CREATE TABLE demo (ID INTEGER, NAME VARCHAR(32))');
console.log('Rows affected:', create.affectedRows); // -> 0 for DDL

const [insert] = await conn.execute("INSERT INTO demo VALUES (1, 'alpha')");
console.log('Rows affected:', insert.affectedRows); // -> 1

await expectTransactionUnsupported(conn, 'COMMIT'); // demonstrates lack of transactions
```

Helper used in the integration suite:

```js
async function expectTransactionUnsupported(conn, sql) {
  try {
    await conn.execute(sql);
    throw new Error(`Expected ${sql} to fail because Machbase does not support transactions.`);
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    console.log(`${sql} expected failure:`, msg);
  }
}
```

### 3.3 `query(sql, values?)`

Executes a statement that returns rows. The facade resolves with a two‑element
tuple `[rows, fields]`, matching mysql2's default shape.

```js
const [rows, fields] = await conn.query('SELECT ID, NAME FROM demo ORDER BY ID');
console.table(rows);
```

### 3.4 `prepare(sql)` / `PreparedStatementInfo`

Creates a prepared statement on the server:

```js
const stmt = await conn.prepare('SELECT NAME FROM demo WHERE ID = ?');
try {
  const [rows] = await stmt.execute([1]);
  console.log(rows); // -> [ { NAME: 'alpha' } ]
} finally {
  await stmt.close();
}
```

Methods on the returned object:

- `execute(parameters?: MachbaseBindInput[])` – runs the statement and resolves
  to `[rowsOrPacket, fields]`.
- `getColumns()` – returns cached column metadata.
- `getLastMessage()` – surfaces the last server message for the statement.
- `getStatementId()` – exposes the internal statement identifier.
- `close()` – frees the server resource; safe to call more than once.

Bind values can be supplied as plain primitives or typed descriptors, e.g.
`[{ value: null, type: 'varchar' }]`.

#### Prepared statement example gallery

Three runnable walkthroughs live in `src/examples/` and compile into
`dist/examples/` after `npm run build`. Configure access with the same
environment variables used by the smoke test (for convenience the scripts look
for `MACHBASE_EXAMPLE_*` first, then fall back to `MACHBASE_SMOKE_*`, finally to
`SYS/MANAGER@127.0.0.1`).

- `prepared-select-reuse.ts` shows how to populate a volatile table and reuse a
  `SELECT ... WHERE DEVICE_ID = ?` statement for multiple primary-key lookups.
- `prepared-upsert.ts` demonstrates an `INSERT ... ON DUPLICATE KEY UPDATE` flow
  using `execute` to inspect `affectedRows` as values change.
- `prepared-nullable.ts` highlights typed binds, explicitly sending `NULL`
  values and timestamps while keeping the `WHERE` clause anchored on the
  primary key.

Each script creates and drops its own `VOLATILE` table so it is safe to run on a
shared development server.

##### Example: Reusing a prepared `SELECT`

```
npm run build
node dist/examples/prepared-select-reuse.js
```

The script inserts a handful of sensor rows, prepares
`SELECT DEVICE_ID, SENSOR_VALUE FROM <table> WHERE DEVICE_ID = ?`, and reuses it
inside a loop:

```js
const select = await conn.prepare(`SELECT ... WHERE DEVICE_ID = ?`);
for (const { id } of samples) {
  const [rows] = await select.execute([id]);
  console.log(`selected ${id}:`, rows);
}
```

##### Example: Prepared upsert with `execute`

```
npm run build
node dist/examples/prepared-upsert.js
```

The script binds three parameters to an
`INSERT ... ON DUPLICATE KEY UPDATE` statement and inspects the returned
`affectedRows` 

```js
const upsert = await conn.prepare('INSERT ... ON DUPLICATE KEY UPDATE');
const [result] = await upsert.execute([deviceId, firstValue, firstValue]);
console.log(result.affectedRows);
```

##### Example: Typed parameters and explicit `NULL`

```
npm run build
node dist/examples/prepared-nullable.js
```

This walkthrough shows how to send typed binds (including `Date`) and explicit
`NULL` values. It first inserts a row with metadata and then clears the comment
column by binding `{ value: null, type: 'varchar' }` so the server receives the
expected sentinel:

```js
await update.execute([
  { value: null, type: 'varchar' },
  { value: new Date(), type: 'varchar' },
  { value: 'sensor-200', type: 'varchar' },
]);
```

### 3.5 Machbase facade helpers

`src/machbase.ts` hosts the facade layer. Key entry points:

- **`createConnection(config)`** – returns a Machbase facade connection. The
  config matches the classic connector options (`host`, `port`, `user`,
  `password`, `database`, `timezone`, etc.).
- **`QueryError`** – error class emitted for rejected operations. Includes
  Machbase-specific code/SQL details.
- **`connection.promise()`** – produces a promise-first wrapper mirroring the
  familiar `.promise()` behaviour.
- **`PreparedStatementInfo.execute(values)`** – executes server-prepared
  statements via promise or callback overloads.
  
Additional helpers on the facade:

- **`ping()`** – health check using `SELECT 1 FROM V$TABLES`.
- **`escape`, `escapeId`, `format`** – convenience utilities for building SQL
  strings safely.
- **`beginTransaction` / `commit` / `rollback`** – always fail with
  `ERR_MACHBASE_NO_TX` (Machbase is auto‑commit only).

Limitations surfaced by the facade:

- Transactions are not implemented. `beginTransaction`, `commit`, and
  `rollback` callbacks receive `QueryError` with code `ERR_MACHBASE_NO_TX`.
- Named parameter binding (`{ id: 1 }`) is intentionally rejected; provide an
  ordered array of values for `?` placeholders.
- Log/Tag tables do not support `UPDATE`. When attempted, the facade forwards
  the server error so the application can retry with a supported table type.

See `src/examples/machbase-facade-basic.ts` and `src/examples/machbase-facade-promise.ts` for live
samples combining callbacks, promises, and usage tips.

### 3.6 `appendBatch(table, columns, rows, options?)`

Appends rows to a **log table** using the `CMI_APPEND_BATCH_PROTOCOL`. Provide
only user-visible columns (log tables implicitly contain `_arrival_time` and
`_rid`). When the server does not support the batch protocol for the target
table type (for example TAG tables), the facade automatically falls back to
prepared statements so behaviour remains deterministic.

```js
const appendResult = await conn.appendBatch(
  'sensor_log',
  [
    { name: 'ID', type: 'int32' },
    { name: 'NAME', type: 'varchar' },
    { name: 'VALUE', type: 'float64' },
  ],
  [
    [1, 'alpha', 0.5],
    { values: [2, 'bravo', 1.25], arrivalTime: Date.now() * 1_000_000 },
  ],
);
console.log('Appended rows:', appendResult.rowsAppended);
```

- Supported column types: `int32`, `int64`, `float64`, `varchar`.
- `rows` accepts either plain arrays or `{ values, arrivalTime }` objects. Nulls
  are automatically encoded using Machbase sentinel values.
- `options` may supply `arrivalTime` (single default) or `arrivalTimes` (array
  per row).

The promise resolves to `{ table, rowsAppended, rowsFailed, message }`.

> Tip: A “column count does not match” error usually means the target table is
> not a log table or the provided columns are not in schema order. Use
> `appendOpen` for TAG tables.

### 3.7 `appendOpen(table, columns, options?)`

Opens a lightweight append session. By default native APPEND open/data/close
is enabled (success path sends no per‑chunk response). To disable native and
force prepared‑statement appends, set `MACHBASE_NATIVE_APPEND=0`. If the server
rejects native APPEND for any reason, the facade automatically falls back to the
prepared statement implementation.

```js
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

TAG tables expose a `DATETIME` column—supply either `Date` objects or `bigint`
epoch values. See `src/examples/tagdata-append-stream.ts` for a complete example
that exercises the API (using the prepared-statement fallback by default).

### 3.8 `append(rows)` on an append stream

Sends one or more rows to the open append stream. Accepts an array of value
arrays or objects with `values` and optional `arrivalTime`. Returns the number
of frames sent. In native mode, success responses are suppressed for maximum
throughput; errors still return failure packets.

```js
const frames = await stream.append([
  ['S-001', new Date(), 1.0],
  ['S-002', new Date(Date.now() + 1), 2.0],
]);
console.log('frames sent:', frames);
```

### 3.9 `close()`

Closes the underlying socket. After calling `close`, any further operation will
throw an error.

```js
await conn.end();
```

---

## 4. Testing & Diagnostics

### 4.1 Scripts

- `npm run build` – compile TypeScript.
- `npm run lint` – run ESLint on `src/`.
- `npm run smoke` – optional smoke test (skipped without environment variables).
- `npm test` – full integration suite (requires a live server):
  1. Creates a log table.
  2. Inserts and selects sample data.
  3. Demonstrates prepared statements with positional binds.
  4. Performs stress append (default: 5 batches × 200 rows) and verifies row
     counts.
  5. Issues `COMMIT` in each stage to demonstrate the expected transaction
     failure.
  6. Exercises the Machbase facade (callbacks, promise wrapper, prepared
     statements) and asserts that transactions or `UPDATE` on log/tag tables
     raise `QueryError` immediately.

Sample console output (abridged):

```
COMMIT expected failure: Expected COMMIT to fail because Machbase does not support transactions.
machbase-facade-basic callback query returned 3 rows.
machbase-facade-update-log-fails message: UPDATE is not supported for LOG tables.
append-batch progress: batch 4/5 { table: 'TS_CLIENT_IT_...', rowsAppended: 200, rowsFailed: 0 }
append-batch final count: 1004
```

### 4.2 Transaction verification helper

The integration suite uses a shared helper to show that `COMMIT` fails with the
expected error:

```js
async function expectTransactionUnsupported(conn, sql) {
  try {
    await conn.execute(sql);
    throw new Error(`Expected ${sql} to fail because Machbase does not support transactions.`);
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    console.log(`${sql} expected failure:`, msg);
  }
}
```

---

## 5. Behaviour Notes & Limitations

### 5.1 Transactions

Machbase autocommits every statement. Transactional keywords such as `BEGIN`,
`COMMIT`, or `ROLLBACK` always fail, and the facade mirrors that behaviour by
calling the supplied callback with a `QueryError` (`ERR_MACHBASE_NO_TX`). The
integration suite (`npm test`) exercises this contract in the `direct-exec-*`
stages and again in `machbase-facade-basic`.

### 5.2 Result buffering & pagination

The facade connection's `query` method buffers the entire rowset before resolving. For large
tables, page manually with `ORDER BY … LIMIT` queries or primary-key ranges—the
facade examples use the same pattern when browsing `V$TABLES`.

### 5.3 Parameter binding

Typed binds cover the portable scalar set (`int32`, `int64`, `float64`, and
`varchar`). When supplying `null`, pair it with a concrete type (for example,
`{ value: null, type: 'varchar' }`) so the client can encode the correct Machbase
sentinel. The `prepared-nullable.ts` example—and its counterpart in the
integration suite—demonstrates clearing a column while retaining audit
timestamps.

### 5.4 Append protocol

Use `appendBatch` for log tables and the streaming helper (`appendOpen` /
`append`) for scenarios that need incremental ingest. When the server does not
support the streaming protocol for a given table type (for example TAG tables),
the facade automatically falls back to a prepared-statement loop, so the safe
pattern is still to chunk data, observe `rowsFailed`, and retry when necessary.

### 5.5 Error handling

Errors propagate as standard `Error` objects (or `QueryError` when using the
facade). Inspect `error.message` or the `QueryError` fields (`code`, `sql`) to
diagnose issues. The integration suite deliberately triggers missing-table
selects and log-table `UPDATE` attempts to ensure failure messages stay
descriptive.

### 5.6 Machbase SQL semantics (table types)

- LOG and TAG tables support `SELECT`, `INSERT`, and `DELETE`, but not `UPDATE`.
- VOLATILE and LOOKUP tables support all DML, but queries must include the
  primary key in `WHERE` clauses for correct index access and performance.

---

## 6. Tutorials

This chapter contains fully runnable, end‑to‑end examples. Each script creates
and drops its own tables.

### 6.1 Quickstart (log table)

```js
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

### 6.2 Prepared statements (reuse)

```js
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
    } finally { await stmt.close(); }
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

### 6.3 Batch append to a log table

```js
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
      [ { name: 'ID', type: 'int32' }, { name: 'NAME', type: 'varchar' }, { name: 'VALUE', type: 'float64' } ],
      [ [1, 'X', 0.5], [2, 'Y', 1.25] ],
    );
    console.log(result);
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

### 6.4 Streaming append to a TAG table

```js
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

> Native mode is enabled by default. To disable, set `MACHBASE_NATIVE_APPEND=0`.
> On success the server does not send a per‑chunk response; errors are still returned.

### 6.5 Promise wrapper + ping

```js
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

---

## 7. Revision History

### 2025‑10‑08

- Added “End‑User Install (from the Web)” with npm/yarn/pnpm and offline `.tgz`
  installation steps and an ESM usage example.
- Clarified that the package targets Node.js (not browsers) and added common
  connection troubleshooting notes.
- Fixed a mixed‑language sentence in the `query` section.

### 2025‑10‑03

- Added beginner‑friendly TAG example that prints all rows and cleans up after
  itself (see “Quick Start → Beginner‑friendly, self‑contained sample”).
- Documented default‑enabled `MACHBASE_NATIVE_APPEND` behaviour and the automatic TAG fallback
  that keeps sessions stable when native streaming is unsafe.
- Improved native encoder notes to clarify arrival‑time defaults and time unit
  semantics (microseconds).

### 2025‑10‑02

- Introduced the Machbase facade (`createConnection`, `QueryError`, `.promise()`,
  facade prepared statements).
- Extended integration tests with Machbase facade callback/promise coverage and
  explicit `UPDATE` rejection on log/tag tables.
- Added Machbase facade example scripts and refreshed documentation to
  highlight transaction/update limitations.

### 2025‑09‑30

- Implemented prepared statements with positional parameter binding.
- Added `appendBatch` helper for log tables, including null handling and success
  statistics.
- Normalised result decoding for variable-length fields.
- Created an integration suite that exercises DDL, DML, prepared statements, and
  batch appends while logging expected transaction errors.
- Published prepared statement example scripts (`prepared-select-reuse.ts`,
  `prepared-upsert.ts`, `prepared-nullable.ts`) and referenced them from the
  manual.
- Added behaviour-focused samples (transactions, pagination, parameter binding,
  append chunking, error handling) and rewrote the limitations section to link
  each limitation to runnable code and integration coverage.

---