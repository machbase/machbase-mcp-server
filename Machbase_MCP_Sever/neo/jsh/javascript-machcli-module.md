# Machbase Neo JavaScript MachCLI Module

The `machcli` module provides a Machbase client API for JSH applications.

## Client

Creates a database client.

<h6>Syntax</h6>

```js
new Client(config)
```

<h6>Configuration fields</h6>

- `host` (default: `127.0.0.1`)
- `port` (default: `5656`)
- `user` (default: `sys`)
- `password` (default: `manager`)
- `alternativeHost` (optional)
- `alternativePort` (optional)

<h6>Usage example</h6>

```js
const { Client } = require('machcli');
const db = new Client({ host: '127.0.0.1', port: 5656, user: 'sys', password: 'manager' });
```

**Client.connect()**

Opens a connection and returns a `Connection` object.

**Client.close()**

Closes the underlying database client.

**Client.user()**

Returns the configured user name (uppercase).

**Client.normalizeTableName()**

Normalizes a table name into `[database, user, table]` format.

## Connection

Connection object returned by `Client.connect()`.

**Connection.query()**

Executes a SELECT query and returns a `Rows` object.

<h6>Syntax</h6>

```js
query(sql[, ...params])
```

<h6>Usage example</h6>

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

Executes a query and returns a single row object. Returned object includes `_ROWNUM` and each column as a property.

**Connection.exec()**

Executes DDL/DML and returns result object with `rowsAffected` and `message`.

**Connection.explain()**

Returns an execution plan string.

**Connection.append()**

Creates an appender object for bulk inserts.

<h6>Usage example</h6>

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

Closes the connection.

## Rows

Result set object returned by `Connection.query()`.

- `message` - Message from query execution.
- `isFetchable()` - Returns whether the result set can fetch rows.
- `next()` - Returns an iterator result object.
- `close()` - Closes the result set.

## Row

Represents a fetched row object. Each column is available as `row.COLUMN_NAME`. `for...of` iteration is supported.

## queryDatabaseId()

Returns backup tablespace ID for a mounted database. Returns `-1` for default database.

## queryTableType()

Returns table type code by normalized table name tokens.

## TableType

Table type constants: `Log`, `Fixed`, `Volatile`, `Lookup`, `KeyValue`, `Tag`.

`stringTableType(type)` converts type code to string.

## TableFlag

Table flag constants: `None`, `Data`, `Rollup`, `Meta`, `Stat`.

`stringTableFlag(flag)` converts flag code to string.

`stringTableDescription(type, flag)` returns combined table description.

## ColumnType

Column type constants: `Short`, `UShort`, `Integer`, `UInteger`, `Long`, `ULong`, `Float`, `Double`, `Varchar`, `Text`, `Clob`, `Blob`, `Binary`, `Datetime`, `IPv4`, `IPv6`, `JSON`.

`stringColumnType(columnType)` converts type code to string.

`columnWidth(columnType, length)` returns default display width.

## ColumnFlag

Column flag constants: `TagName`, `Basetime`, `Summarized`, `MetaColumn`.

`stringColumnFlag(flag)` converts flag code to string.
