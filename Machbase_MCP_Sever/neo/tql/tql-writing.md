# Machbase Neo TQL Writing API

> **참고**: 예제를 실행하려면 아래 SQL로 테이블을 먼저 생성하세요.

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
```

## INSERT CSV

### 1. TQL 파일 생성

아래 코드를 `input-csv.tql`로 저장합니다. TQL 스크립트를 저장하면 에디터 우측 상단에 링크 아이콘이 표시됩니다. 클릭하면 스크립트 파일의 주소가 복사됩니다.

```js
CSV(payload(), 
    field(0, stringType(), 'name'),
    field(1, datetimeType('ns'), 'time'),
    field(2, doubleType(), 'value'),
    header(false)
)
SQL(`insert into example values(?,?,?)`, value(0), value(1), value(2))
```

### 2. HTTP POST

#### HTTP Request 사용

~~~
```http
POST http://127.0.0.1:5654/db/tql/input-csv.tql
Content-Type: text/csv

TAG0,1628866800000000000,12
TAG0,1628953200000000000,13
```
~~~

#### cURL 사용

데이터 파일을 `input-csv.csv`로 준비합니다.

```csv
TAG0,1628866800000000000,12
TAG0,1628953200000000000,13
```

`curl` 명령으로 데이터 파일과 함께 `input-csv.tql`을 호출합니다.

```sh
curl -X POST http://127.0.0.1:5654/db/tql/input-csv.tql \
    -H "Content-Type: text/csv" \
    --data-binary "@input-csv.csv"
```

### 3. MQTT PUBLISH

데이터 파일을 `input-csv.csv`로 준비합니다.

```csv
TAG1,1628866800000000000,12
TAG1,1628953200000000000,13
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/tql/input-csv.tql \
    -f input-csv.csv
```

## APPEND CSV

### 1. TQL 파일 생성

아래 코드를 `append-csv.tql`로 저장합니다. TQL 스크립트를 저장하면 에디터 우측 상단에 링크 아이콘이 표시됩니다. 클릭하면 스크립트 파일의 주소가 복사됩니다.

```js
CSV(payload(), 
    field(0, stringType(), 'name'),
    field(1, datetimeType('ns'), 'time'),
    field(2, doubleType(), 'value'),
    header(false)
)
APPEND(table('example'))
```

### 2. HTTP POST

#### HTTP Request 사용

~~~
```http
POST http://127.0.0.1:5654/db/tql/append-csv.tql
Content-Type: text/csv

TAG0,1628866800000000000,12
TAG0,1628953200000000000,13
```
~~~

#### cURL 사용

데이터 파일을 `append-csv.csv`로 준비합니다.

```csv
TAG2,1628866800000000000,12
TAG2,1628953200000000000,13
```

`curl` 명령으로 데이터 파일과 함께 `append-csv.tql`을 호출합니다.

```sh
curl -X POST http://127.0.0.1:5654/db/tql/append-csv.tql \
    -H "Content-Type: text/csv" \
    --data-binary "@append-csv.csv"
```

### 3. MQTT PUBLISH

데이터 파일을 `append-csv.csv`로 준비합니다.

```csv
TAG3,1628866800000000000,12
TAG3,1628953200000000000,13
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/tql/input-csv.tql \
    -f append-csv.csv
```

## 사용자 정의 JSON

### 1. TQL 파일 생성

`SCRIPT()` 함수로 사용자 정의 형식의 JSON을 파싱합니다.

아래 코드를 `input-json.tql`로 저장합니다.

```js
SCRIPT({
    obj = JSON.parse($.payload)
    obj.data.rows.forEach(r => $.yield(...r))
})
SQL(`insert into example values(?,?,?)`, value(0), value(1), value(2))
```

### 2. HTTP POST

#### HTTP Request 사용

~~~
```http
POST http://127.0.0.1:5654/db/tql/input-json.tql
Content-Type: application/json

{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      [ "TAG0", 1628866800000000000, 12 ],
      [ "TAG0", 1628953200000000000, 13 ]
    ]
  }
}
```
~~~

#### cURL 사용

데이터 파일을 `input-json.json`으로 준비합니다.

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      [ "TAG0", 1628866800000000000, 12 ],
      [ "TAG0", 1628953200000000000, 13 ]
    ]
  }
}
```

`curl` 명령으로 데이터 파일과 함께 `input-json.tql`을 호출합니다.

```sh
curl -X POST http://127.0.0.1:5654/db/tql/input-json.tql \
    -H "Content-Type: application/json" \
    --data-binary "@input-json.json"
```

### 3. MQTT PUBLISH

데이터 파일을 `input-json.json`으로 준비합니다.

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      [ "TAG1", 1628866800000000000, 12 ],
      [ "TAG1", 1628953200000000000, 13 ]
    ]
  }
}
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/tql/input-json.tql \
    -f input-json.json
```

## 사용자 정의 텍스트

데이터베이스에 쓰기 전에 데이터 변환이 필요한 경우, 적절한 TQL 스크립트를 준비하고 `db/tql/` + `{tql_file.tql}` 이름의 토픽으로 데이터를 발행합니다.

### 1. TQL 파일 생성

아래 예제 코드는 여러 줄 텍스트 데이터를 테이블에 쓰는 방법을 보여줍니다.

#### MAP 함수 사용

MAP 함수를 이용한 변환입니다.

```js
// payload() returns the payload that arrived via HTTP-POST or MQTT,
// The ?? operator means that if tql is called without content,
//        the right side value is applied
// It is a good practice while the code is being developed on the tql editor of web-ui.
STRING( payload() ?? ` 12345
                     23456
                     78901
                     89012
                     90123
                  `, separator('\n'), trimspace(true))
FILTER( len(value(0)) > 0 )   // filter empty line
// transforming data
MAPVALUE(-1, time("now"))     // equiv. PUSHVALUE(0, time("now"))
MAPVALUE(-1, "text_"+key())   // equiv. PUSHVALUE(0, "text_"+key())
MAPVALUE(2, strSub( value(2), 0, 2 ) )

// Run this code in the tql editor of web-ui for testing
CSV( timeformat("DEFAULT") )
// Use APPEND(table('example')) for the real action
// APPEND(table('example'))
```

#### SCRIPT 함수 사용

`SCRIPT` 함수를 이용한 대안입니다.

```js
// payload() returns the payload that arrived via HTTP-POST or MQTT,
// The ?? operator means that if tql is called without content,
//        the right side value is applied
// It is a good practice while the code is being developed on the tql editor of web-ui.
STRING( payload() ?? ` 12345
                     23456
                     78901
                     89012
                     90123
                  `, separator('\n'), trimspace(true) )
FILTER( len(value(0)) > 0) // filter empty line
// transforming data
SCRIPT({
  str = $.values[0].trim() ;  // trim spaces
  str = str.substring(0, 2);  // takes the first 2 letters of the line
  ts = (new Date()).getTime() * 1000000 // ms. to ns.
  $.yieldKey("text_"+$.key, ts, parseInt(str))
})
CSV()
// APPEND(table('example'))
```

**결과:**

```csv
text_1,2023-12-02 11:03:36.054,12
text_2,2023-12-02 11:03:36.054,23
text_3,2023-12-02 11:03:36.054,78
text_4,2023-12-02 11:03:36.054,89
text_5,2023-12-02 11:03:36.054,90
```

위 코드를 실행해 오류 없이 의도대로 동작하면, 마지막 줄 `CSV()`를 `APPEND(table('example'))`로 바꿉니다.

코드를 "script-post-lines.tql"로 저장한 뒤, `db/tql/script-post-lines.tql` 토픽으로 테스트 데이터를 보냅니다.

**샘플 데이터 파일** - `cat lines.txt`

```
110000
221111
332222
442222
```

### 2. HTTP POST

참고로 같은 TQL 파일이 HTTP POST에서도 동작합니다.

```sh
curl -H "Content-Type: text/plain" \
    --data-binary @lines.txt \
    http://127.0.0.1:5654/db/tql/script-post-lines.tql
```

### 3. MQTT PUBLISH

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/tql/script-post-lines.tql \
    -f lines.txt
```

그리고 데이터가 제대로 변환되어 저장됐는지 확인합니다.

```sh
$ machbase-neo shell "select * from example where name like 'text_%'"
 ROWNUM  NAME    TIME(LOCAL)              VALUE     
────────────────────────────────────────────────────
      1  text_3  2023-07-14 08:51:10.926  44.000000 
      2  text_0  2023-07-14 08:51:10.925  11.000000 
      3  text_1  2023-07-14 08:51:10.926  22.000000 
      4  text_2  2023-07-14 08:51:10.926  33.000000 
4 rows fetched.
```
