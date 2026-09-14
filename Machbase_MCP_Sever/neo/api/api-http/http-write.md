# Machbase Neo HTTP Write

쓰기 API 엔드포인트는 `/db/write/{TABLE}` 이며, `{TABLE}`은 데이터를 쓸 테이블 이름입니다.

`query` API로도 'INSERT' 문을 실행할 수 있지만 데이터를 쓰는 효율적인 방법은 아니며,
클라이언트가 요청마다 `q` 파라미터에 정적인 SQL 텍스트를 만들어야 하기 때문입니다.
데이터를 쓰는 올바른 방법은 `INSERT` 문에 해당하는 `write` API입니다. 
`write`의 또 다른 장점은 클라이언트 애플리케이션이 한 번의 `write` 요청으로 여러 레코드를 넣을 수 있다는 점입니다.

## Parameters

**쓰기 파라미터**

| 파라미터       | 기본값 | 설명                     |
|:----------- |---------|:------------------------------- |
| timeformat  | `ns`     | 시간 형식: `s`, `ms`, `us`, `ns` |
| tz          | `UTC`    | 시간대: `UTC`, `Local`, 지역 지정 |
| method      | `insert` | 쓰기 방식: `insert`, `append`  |

**INSERT vs. APPEND**

기본적으로 `/db/write` API는 `INSERT INTO...` 문으로 데이터를 씁니다. 레코드 수가 적을 때는 `append` 방식과 성능이 비슷합니다.

대량의 데이터(예: 수십만 건 이상)를 쓸 때는 `method=append` 파라미터를 사용하세요. 기본값인 "INSERT INTO..." 문(`method=insert`) 대신 "append" 방식을 쓰도록 지정하는 것입니다.

**Content-Type 헤더**

machbase-neo 서버는 `Content-Type` 헤더로 들어오는 데이터 스트림의 형식을 인식하며,
예를 들어 JSON 데이터는 `Content-Type: application/json`, CSV 데이터는 `Content-Type: text/csv`, 개행 구분 JSON은 `Content-type: application/x-ndjson` 입니다.

**Content-Encoding 헤더**

클라이언트가 gzip으로 압축한 스트림을 보낸다면 `Content-Encoding: gzip` 헤더를 설정해야 합니다 
들어오는 데이터 스트림이 gzip으로 인코딩되었음을 machbase-neo에 알립니다.

## Inputs

### JSON

이 요청 메시지는 `INSERT into {table} (columns...) values (values...)` INSERT SQL 문을 구성하는 것과 같습니다

| 이름         | 타입       |  설명                        |
|:------------ |:-----------|:------------------------------------|
| data         | object           |                               |
| data.columns | 문자열 배열 | 컬럼을 나타냅니다            |
| data.rows    | 튜플 배열  | 레코드의 값들             |

**JSON**

```json
{
    "data": {
        "columns":["name", "time", "value"],
        "rows": [
            [ "json-data", 1670380342000000000, 1.0001 ],
            [ "json-data", 1670380343000000000, 2.0002 ]
        ]
    }
}
```

`Content-Type` 헤더를 `application/json`으로 설정합니다.

**HTTP:**
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
Content-Type: application/json

{
    "data": {
        "columns":["name", "time", "value"],
        "rows": [
            [ "json-data", 1670380342000000000, 1.0001 ],
            [ "json-data", 1670380343000000000, 2.0002 ]
        ]
    }
}
```
~~~

**cURL:**
```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE \
    -H "Content-Type: application/json" \
    --data-binary "@post-data.json"
```

**압축된 JSON**

`Content-Encoding: gzip` 헤더를 설정하면 들어오는 스트림이 gzip으로 압축되었음을 machbase-neo에 알립니다.

**HTTP:**
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
Content-Type: application/json
Content-Encoding: gzip

< /csv/post-data.json.gz
```
~~~

**cURL:**
```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE \
    -H "Content-Type: application/json" \
    -H "Content-Encoding: gzip" \
    --data-binary "@post-data.json.gz"
```

**timeformat을 사용한 JSON**

시간 필드가 UNIX epoch가 아니라 문자열 형식일 때입니다.

`timeformat`과 `tz` 파라미터를 추가합니다.

**HTTP:**
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=DEFAULT
    &tz=Asia/Seoul
Content-Type: application/json

{
    "data": {
        "columns":["name", "time", "value"],
        "rows": [
            [ "json-data", "2022-12-07 02:32:22", 1.0001 ],
            [ "json-data", "2022-12-07 02:32:23", 2.0002 ]
        ]
    }
}
```
~~~

**cURL:**
```sh
curl -X POST 'http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=DEFAULT&tz=Asia/Seoul' \
    -H "Content-Type: application/json" \
    --data-binary "@post-data.json"
```

- `post-data.json`

```json
{
    "data": {
        "columns":["name", "time", "value"],
        "rows": [
            [ "json-data", "2022-12-07 02:32:22", 1.0001 ],
            [ "json-data", "2022-12-07 02:32:23", 2.0002 ]
        ]
    }
}
```

### NDJSON

NDJSON(Newline Delimited JSON)은 각 줄이 하나의 유효한 JSON 객체인 스트리밍 JSON 형식입니다. 대용량 데이터셋이나 스트리밍 데이터를 처리할 때 유용합니다.

이 요청 메시지는 `INSERT into {table} (columns...) values (values...)` INSERT SQL 문을 구성하는 것과 같습니다

**NDJSON**

```json
{"NAME":"ndjson-data", "TIME":1670380342000000000, "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":1670380343000000000, "VALUE":2.002}
```

`Content-Type` 헤더를 `application/x-ndjson`으로 설정합니다.

**HTTP:**
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
Content-Type: application/x-ndjson

{"NAME":"ndjson-data", "TIME":1670380342000000000, "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":1670380343000000000, "VALUE":2.002}
```
~~~

**cURL:**
```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE \
    -H "Content-Type: application/x-ndjson" \
    --data-binary "@post-data.json"
```

**timeformat을 사용한 NDJSON**

시간 필드가 UNIX epoch가 아니라 문자열 형식일 때입니다.

```json
{"NAME":"ndjson-data", "TIME":"2022-12-07 02:33:22", "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":"2022-12-07 02:33:23", "VALUE":2.002}
```

`timeformat`과 `tz` 파라미터를 추가합니다.

**HTTP:**
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=DEFAULT
    &tz=Local
Content-Type: application/x-ndjson

{"NAME":"ndjson-data", "TIME":"2022-12-07 02:33:22", "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":"2022-12-07 02:33:23", "VALUE":2.002}
```
~~~

**cURL:**
```sh
curl -X POST 'http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=Default&tz=Local' \
    -H "Content-Type: application/x-ndjson" \
    --data-binary "@post-data.json"
```

### CSV

이 옵션들은 본문이 CSV 형식일 때만 적용됩니다.

| 파라미터         | 기본값 | 설명                     |
|:------------- |---------|:------------------------------- |
| header        |         | `skip`: 첫 줄을 건너뜁니다<br/> `columns`: CSV에 컬럼명과 일치하는 헤더 줄이 있습니다. |
| heading       | false   | 폐기됨. `heading=true`는 `header=skip`과 같습니다. |
| delimiter     | ,       | 필드 구분자 |

CSV 데이터에 헤더 줄이 있으면 `header=skip` 쿼리 파라미터를 지정해 machbase-neo가 첫 줄을 무시하도록 하세요.

CSV 헤더 줄이 쓸 컬럼을 지정한다면 `header=columns`를 사용하세요. 이 옵션은 헤더가 테이블 컬럼 이름과 일치하도록 합니다. 헤더 줄은 SQL 문 `INSERT INTO TABLE(columns...) VALUES(...)` 의 *columns* 부분으로 사용됩니다.

헤더 줄이 없고 기본값대로 `header` 옵션을 생략하면(또는 `heading=false`와 같음), SQL 문 `INSERT INTO TABLE VALUES(...)` 에 맞도록 각 줄의 필드가 테이블의 모든 컬럼과 순서까지 일치해야 합니다.

> append 방식의 의미상 `header=columns`는 `method=append`와 함께 동작하지 않습니다.

**header=skip**

`header=skip`을 지정하면 서버가 첫 줄을 무시하며, 데이터는 테이블 컬럼과 같은 순서여야 합니다.

```csv
NAME,TIME,VALUE
csv-data,1670380342000000000,1.0001
csv-data,1670380343000000000,2.0002
```

`Content-Type` 헤더는 `text/csv` 여야 합니다.

**HTTP:**
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE?header=skip
Content-Type: text/csv

NAME,TIME,VALUE
csv-data,1670380342000000000,1.0001
csv-data,1670380343000000000,2.0002
```
~~~

**cURL:**
```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE?header=skip \
    -H "Content-Type: text/csv" \
    --data-binary "@post-data.csv"
```

**header=columns**

CSV 필드의 순서가 다르거나 실제 테이블 컬럼의 일부만 있다면 `header=columns`를 지정하세요. 서버가 첫 줄을 컬럼 이름으로 취급합니다. 아래 예제는 `INSERT INTO EXAMPLE (TIME, NAME, VALUE) VALUES(?, ?, ?)` 와 유사한 내부 SQL 문을 생성합니다.

```csv
TIME,NAME,VALUE
1670380342000000000,csv-data,1.0001
1670380343000000000,csv-data,2.0002
```

`Content-Type` 헤더는 `text/csv` 여야 합니다.

**HTTP:**
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE?header=columns
Content-Type: text/csv

TIME,NAME,VALUE
1670380342000000000,csv-data,1.0001
1670380343000000000,csv-data,2.0002
```
~~~

**cURL:**
```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE?header=columns \
    -H "Content-Type: text/csv" \
    --data-binary "@post-data.csv"
```

**압축된 CSV**

들어오는 스트림이 gzip으로 압축되었음을 알리려면 `Content-Encoding: gzip` 헤더를 설정하세요.

**HTTP:**
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE?header=skip
Content-Type: text/csv
Content-Encoding: gzip

< /csv/post-data.json.gz
```
~~~

**cURL:**
```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE?header=skip \
    -H "Content-Type: text/csv" \
    -H "Content-Encoding: gzip" \
    --data-binary "@post-data.csv.gz"
```

**timeformat을 사용한 CSV**

`timeformat`과 `tz` 쿼리 파라미터를 추가합니다.

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?header=skip
    &timeformat=Default
    &tz=Asia/Seoul
Content-Type: text/csv

NAME,TIME,VALUE
csv-data,2022-12-07 11:39:32,1.0001
csv-data,2022-12-07 11:39:33,2.0002
```
~~~

## 예제s

요청 엔드포인트와 파라미터의 자세한 내용은 API 문서를 참고하세요

**테스트 테이블**

**HTTP:**
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=create tag table if not exists EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)
```
~~~

**cURL:**
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode \
    "q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
```

**Time**

이 예제들의 샘플 파일에 저장된 시간은 초 단위 Unix epoch로 표현됩니다. 따라서 데이터를 적재할 때 `timeformat=s` 옵션을 지정해야 합니다. 데이터가 다른 해상도로 저장되어 있다면 올바른 입력을 위해 이 옵션을 바꿔야 합니다. Machbase Neo의 기본 시간 해상도는 `나노초(ns)`로 가정되어 동작한다는 점에 유의하세요.

### epoch를 사용한 JSON

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=s
Content-Type: application/json

{
  "data":  {
    "columns":["NAME","TIME","VALUE"],
    "rows": [
        ["wave.sin",1676432361,0],
        ["wave.sin",1676432362,0.406736],
        ["wave.sin",1676432363,0.743144],
        ["wave.sin",1676432364,0.951056],
        ["wave.sin",1676432365,0.994522]
    ]
  }
}
```
~~~

**행 조회**

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 10
```
~~~

### epoch를 사용한 CSV

아래처럼 CSV 데이터에 헤더 줄이 있으면 `header=skip` 쿼리 파라미터를 지정하세요.

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=s
    &header=skip
Content-Type: text/csv

NAME,TIME,VALUE
wave.sin,1676432361,0.000000
wave.cos,1676432361,1.000000
wave.sin,1676432362,0.406736
wave.cos,1676432362,0.913546
wave.sin,1676432363,0.743144

```
~~~

### 헤더 없는 CSV

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=s
Content-Type: text/csv

wave.sin,1676432361,0.000000
wave.cos,1676432361,1.000000
wave.sin,1676432362,0.406736
wave.cos,1676432362,0.913546
wave.sin,1676432363,0.743144
```
~~~

### CSV

**입력**

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=Default
Content-Type: text/csv

wave.sin,2023-02-15 03:39:21,0.111111
wave.sin,2023-02-15 03:39:22.111,0.222222
wave.sin,2023-02-15 03:39:23.222,0.333333
wave.sin,2023-02-15 03:39:24.333,0.444444
wave.sin,2023-02-15 03:39:25.444,0.555555
```
~~~

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 10
    &timeformat=Default
    &format=csv
```
~~~

**Append**

큰 CSV 파일을 적재할 때 "append" 방식을 쓰면 "insert" 방식보다 몇 배 빠르게 입력할 수 있습니다.

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=s&method=append
Content-Type: text/csv

wave.sin,1676432361,0.000000
wave.cos,1676432361,1.000000
wave.sin,1676432362,0.406736
wave.cos,1676432362,0.913546
wave.sin,1676432363,0.743144
```
~~~

### 시간대를 지정한 CSV

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=Default
    &tz=Asia/Seoul
Content-Type: text/csv

wave.sin,2023-02-15 12:39:21,0.111111
wave.sin,2023-02-15 12:39:22.111,0.222222
wave.sin,2023-02-15 12:39:23.222,0.333333
wave.sin,2023-02-15 12:39:24.333,0.444444
wave.sin,2023-02-15 12:39:25.444,0.555555
```
~~~

**UTC 기준으로 조회**

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 10
    &timeformat=Default
    &format=csv
```
~~~

### `RFC3339`

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=RFC3339
Content-Type: text/csv

wave.sin,2023-02-15T03:39:21Z,0.111111
wave.sin,2023-02-15T03:39:22Z,0.222222
wave.sin,2023-02-15T03:39:23Z,0.333333
wave.sin,2023-02-15T03:39:24Z,0.444444
wave.sin,2023-02-15T03:39:25Z,0.555555
```
~~~

**UTC 기준으로 조회**

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 10
    &format=csv
    &timeformat=RFC3339
```
~~~

### `RFC3339Nano` in time zone

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=RFC3339Nano
    &tz=America/New_York
Content-Type: text/csv

wave.sin,2023-02-14T22:39:21.000000000-05:00,0.111111
wave.sin,2023-02-14T22:39:22.111111111-05:00,0.222222
wave.sin,2023-02-14T22:39:23.222222222-05:00,0.333333
wave.sin,2023-02-14T22:39:24.333333333-05:00,0.444444
wave.sin,2023-02-14T22:39:25.444444444-05:00,0.555555
```
~~~


**America/New_York 기준으로 조회**

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 10
    &format=box
    &timeformat=RFC3339Nano
    &tz=America/New_York
```
~~~

### Timeformat

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=Default
Content-Type: text/csv

wave.sin,2023-02-15 03:39:21,0.111111
wave.sin,2023-02-15 03:39:22.111111111,0.222222
wave.sin,2023-02-15 03:39:23.222222222,0.333333
wave.sin,2023-02-15 03:39:24.333333333,0.444444
wave.sin,2023-02-15 03:39:25.444444444,0.555555
```
~~~

**UTC 기준으로 조회**

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 10
    &format=csv
    &timeformat=Default

```
~~~

### 사용자 정의 시간 형식

- 뉴욕 시간대의 `hour:min:sec-SPLIT-year-month-day` 형식

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=03:04:05.999999999-SPLIT-2006-01-02
    &tz=America/New_York
Content-Type: text/csv

wave.sin,10:39:21-SPLIT-2023-02-14 ,0.111111
wave.sin,10:39:22.111111111-SPLIT-2023-02-14 ,0.222222
wave.sin,10:39:23.222222222-SPLIT-2023-02-14 ,0.333333
wave.sin,10:39:24.333333333-SPLIT-2023-02-14 ,0.444444
wave.sin,10:39:25.444444444-SPLIT-2023-02-14 ,0.555555
```
~~~

**행 조회**

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 5
    &format=csv
    &timeformat=2006-01-02 03:04:05.999999999
    &tz=America/New_York
```
~~~
