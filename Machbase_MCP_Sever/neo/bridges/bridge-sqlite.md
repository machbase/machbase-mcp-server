# Machbase Neo Bridge - SQLite

## sqlite3 브리지 등록

SQLite에 연결하는 브리지를 등록합니다.

```
bridge add -t sqlite sqlitedb file:/data/sqlite.db;
```

SQLite는 아래처럼 메모리 전용 모드를 지원합니다.

```
bridge add -t sqlite mem file::memory:?cache=shared
```

아래 명령은 다음 이미지의 웹 UI와 동일합니다.

## 브리지 연결 확인

```
machbase-neo» bridge test mem;
Test bridge mem connectivity... success 11.917µs
```

## 테이블 생성

machbase-neo 셸을 열고 아래 명령을 실행해 `mem` 브리지로 `mem_example` 테이블을 만듭니다.

```sh
bridge exec mem CREATE TABLE IF NOT EXISTS mem_example(
    id         INTEGER NOT NULL PRIMARY KEY,
    company    TEXT,
    employee   INTEGER,
    discount   REAL,
    code       TEXT,
    valid      BOOLEAN,
    memo       BLOB,
    created_on DATETIME NOT NULL
);
```

표준 SQL 에디터는 `-- env: bridge=<name>` 주석이 있으면 브리지 데이터베이스에 SQL을 실행할 수 있습니다. 이 *env* 주석은 `-- env: reset`으로 해제할 때까지 유효합니다.

```sql
-- env: bridge=mem
CREATE TABLE IF NOT EXISTS mem_example(
    id         INTEGER NOT NULL PRIMARY KEY,
    company    TEXT,
    employee   INTEGER,
    discount   REAL,
    code       TEXT,
    valid      BOOLEAN,
    memo       BLOB,
    created_on DATETIME NOT NULL
);
-- env: reset
```

## SQL 에디터에서의 DML

```sql
-- env: bridge=mem
INSERT INTO mem_example(company, employee, created_on) 
    values('Fedel-Gaylord', 12, datetime('now'));

INSERT INTO mem_example(company, employee, created_on) 
    values('Simoni', 23, datetime('now'));

SELECT company, employee, datetime(created_on, 'localtime') from mem_example;

DELETE from mem_example;
-- env: reset
```

## SQLite에 *TQL*로 쓰기

```js
FAKE( json({
    ["COMPANY", "EMPLOYEE"],
    ["NovaWave", 10],
    ["Sunflower", 20]
}))

DROP(1) // skip header
MAPVALUE(2, time("now"))

INSERT(bridge("mem"), table("mem_example"), "company", "employee", "created_on")
```

```
machbase-neo» bridge query mem select * from mem_example;
╭────┬─────────┬──────────┬──────────┬───────┬───────┬──────┬──────────────────────────────────────╮
│ ID │ COMPANY │ EMPLOYEE │ DISCOUNT │ CODE  │ VALID │ MEMO │ CREATED_ON                           │
├────┼─────────┼──────────┼──────────┼───────┼───────┼──────┼──────────────────────────────────────┤
│  1 │ acme    │       10 │ <nil>    │ <nil> │ <nil> │ []   │ 2023-08-10 14:33:08.667491 +0900 KST │
╰────┴─────────┴──────────┴──────────┴───────┴───────┴──────┴──────────────────────────────────────╯
```

## SQLite에서 *TQL*로 읽기

아래 코드를 `sqlite.tql`로 저장합니다.

```js
SQL(bridge('mem'), "select company, employee, created_on from mem_example")
CSV()
```

그리고 `curl` 명령으로 엔드포인트를 호출하거나 브라우저에서 엽니다.

```sh
curl -o - http://127.0.0.1:5654/db/tql/sqlite.tql
```

```csv
NovaWave,10,1704866777160399000
Sunflower,20,1704866777160407000
```

## SQLite와 데이터 복사

이 예제는 Machbase에서 SQLite 브리지로 데이터를 복사하는 방법을 보여줍니다.

**Bridge**

다음 내용으로 `sqlite` 브리지를 정의합니다:

- Type: `SQLite`
- 연결 문자열: `file:///tmp/sqlite.db`

**SQL**

"/tmp/sqlite.db"에 있는 SQLite 데이터베이스에 `example` 테이블을 만듭니다.

```sql
--env: bridge=sqlite
CREATE TABLE IF NOT EXISTS example (
    NAME TEXT,
    TIME DATETIME,
    VALUE REAL
);
-- env: reset
```

**TQL**

아래 TQL 스크립트는 `SQL()` 함수로 `SELECT` 문을 실행해 필요한 데이터를 가져온 뒤, 첫 인자로 `bridge("sqlite")`를 준 `INSERT()` 함수로 SQLite 데이터베이스에 씁니다.

```js
SQL(`select name, time, value from example where name = 'my-car'`)
INSERT(bridge("sqlite"), "name", "time", "value", table("example"))
```

**SQL**

```sql
--env: bridge=sqlite
SELECT * FROM example order by TIME;
-- env: reset
```
