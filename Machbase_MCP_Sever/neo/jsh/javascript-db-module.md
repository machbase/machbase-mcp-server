# Machbase Neo JavaScript DB Module

## Client

데이터베이스 클라이언트입니다.

**사용 예제**

```js
const db = require("@jsh/db");
const client = new db.Client();
try {    
    conn = client.connect();
    rows = conn.query("select * from example limit 10")
    cols = rows.columns()
    console.log("cols.names:", JSON.stringify(cols.columns));
    console.log("cols.types:", JSON.stringify(cols.types));
    
    count = 0;
    for (const rec of rows) {
        console.log(...rec);
        count++;
    }
    console.log("rows:", count, "selected" );
} catch(e) {
    console.log("Error:", e);
} finally {
    if (rows) rows.close();
    if (conn) conn.close();
}
```

**생성**

| 생성자             | 설명                          |
|:------------------------|:----------------------------------------------|
| new Client(*options*)     | 옵션으로 데이터베이스 클라이언트 객체를 생성합니다 |

`bridge`도 `driver`도 지정하지 않으면 클라이언트는 기본적으로 내부 Machbase DBMS에 접속합니다.

**옵션**

| 옵션              | 타입         | 기본값        | 설명         |
|:--------------------|:-------------|:---------------|:--------------------|
| lowerCaseColumns    | Boolean      | `false`        | 소문자로 바꾼 컬럼 이름을 결과 객체에 매핑합니다 |

- 드라이버용 옵션

`driver`와 `dataSource` 옵션은 미리 정의된 브리지 없이 `sqlite`, `mysql`, `mssql`, `postgresql`, `machbase`를 지원합니다.

| 옵션              | 타입         | 기본값        | 설명         |
|:--------------------|:-------------|:---------------|:--------------------|
| driver              | String       |                | 드라이버 이름         |
| dataSource          | String       |                | 데이터베이스 연결 문자열 |

- 브리지용 옵션

미리 정의된 브리지로 Client를 만들 수도 있습니다.

| 옵션              | 타입         | 기본값        | 설명         |
|:--------------------|:-------------|:---------------|:--------------------|
| bridge              | String       |                | 브리지 이름         |

**속성**

| 속성           | 타입       | 설명           |
|:-------------------|:-----------|:----------------------|
| supportAppend      | Boolean    | 클라이언트가 "Append" 모드를 지원하면 `true`. |

### connect()

데이터베이스에 접속합니다.

**반환값**

- `Object` Conn

## Conn

### close()

데이터베이스 접속을 끊고 자원을 해제합니다

**문법**

```js
close()
```

### query()

**문법**

```js
query(String *sqlText*, any ...*args*)
```

**반환값**

- `Object` Rows

### queryRow()

**문법**

```js
queryRow(String *sqlText*, any ...*args*)
```

**반환값**

- `Object` Row

### exec()

**문법**

```js
exec(sqlText, ...args)
```

**파라미터**

- `sqlText` `String` SQL 문자열
- `args` `any` 가변 길이 인자 목록.

**반환값**

- `Object` Result

### appender()

새 "appender"를 만듭니다.

**문법**

```js
appender(table_name, ...columns)
```

**파라미터**

- `table_name` `String` append할 테이블 이름.
- `columns` `String` 가변 길이 컬럼 이름 목록. `columns`를 생략하면 테이블의 모든 컬럼이 순서대로 append됩니다.

**반환값**

- `Object` Appender

## Rows

Rows는 쿼리 실행으로 얻은 결과 집합을 감쌉니다.

`Symbol.iterator`을 구현하여 두 가지 패턴을 모두 지원합니다:

```js
for(rec := rows.next(); rec != null; rec = rows.next()) {
    console.log(...rec);
}

for (rec of rows) {
    console.log(...rec);
}
```

### close()

데이터베이스 statement를 해제합니다

**문법**

```js
close()
```

**파라미터**

None.

**반환값**

None.

### next()

레코드를 하나 가져오며, 더 이상 없으면 null을 반환합니다

**문법**

```js
next()
```

**파라미터**

None.

**반환값**

- `any[]`

### columns()

**문법**

```js
columns()
```

**파라미터**

None.

**반환값**

- `Object` Columns

### columnNames()

**문법**

```js
columnNames()
```

**파라미터**

None.

**반환값**

- `String[]`

### columnTypes()

**문법**

```js
columnTypes()
```

**파라미터**

None.

**반환값**

- `String[]`

## Row
Row는 단일 레코드를 가져오는 queryRow의 결과를 감쌉니다.

### columns()

**문법**

```js
columns()
```

**파라미터**

None.

**반환값**

- `Object` Columns

### columnNames()

결과의 이름들

**문법**

```js
columnNames()
```

**파라미터**

None.

**반환값**

- `String[]`

### columnTypes()

결과의 타입들

**문법**

```js
columnTypes()
```

**파라미터**

None.

**반환값**

- `String[]`

### values()

결과 컬럼

**문법**

```js
values()
```

**파라미터**

None.

**반환값**

- `any[]`

## Result

Result는 `exec()` 메서드의 결과를 나타내며 실행에 관한 세부 정보를 제공합니다.

**속성**

| 속성           | 타입       | 설명        |
|:-------------------|:-----------|:-------------------|
| message            | String     | 결과 메시지     |
| rowsAffected       | Number     |                    |

## Columns

**속성**

| 속성           | 타입       | 설명        |
|:-------------------|:-----------|:-------------------|
| columns            | String[]   | 결과의 이름들 |
| types              | String[]   | 결과의 타입들 |

## Appender

### append()

지정한 컬럼 순서대로 값을 넣어 `append` 메서드를 호출합니다.

**문법**

```js
append(...values)
```

**파라미터**

- `values` `any` 테이블에 append할 값들이며, 지정한 컬럼 순서대로 전달합니다.

**반환값**

None.

### close()

appender를 닫습니다.

**문법**

```js
close()
```

**파라미터**

None.

**반환값**

None.

### result()

appender가 닫힌 뒤 append 작업의 결과를 반환합니다.

**문법**

```js
result()
```

**파라미터**

None.

**반환값**

- `Object`

| 속성           | 타입       | 설명        |
|:-------------------|:-----------|:-------------------|
| success            | Number     |                    |
| failed             | Number     |                    |
