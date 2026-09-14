# Machbase Neo HTTP Query

Query API endpoint is `/db/query`.

query API는 "SELECT"뿐 아니라 "CREATE TABLE", "ALTER TABLE", "INSERT" 등 다른 모든 SQL 문도 지원합니다.

`/db/query` API는 *GET*, *POST JSON*, *POST form-data*를 지원하며, 모든 방식이 동일한 파라미터를 지원합니다.

예를 들어 `format` 파라미터는 *GET* 메서드에서 `GET /db/query?format=csv` 처럼 쿼리 파라미터로 지정할 수 있고,
or be a JSON field in *POST-JSON* method as `{ "format": "csv" }`.

**쿼리 예제**

**HTTP:**
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 2
```
~~~

**cURL:**
```sh 
curl -o - http://127.0.0.1:5654/db/query \
     --data-urlencode "q=select * from EXAMPLE limit 2"
```

## Parameters

**쿼리 파라미터**

| 파라미터       | 기본값 | 설명                   |
|:----------- |---------|:----------------------------- |
| **q**       | _필수_ | SQL 쿼리 문자열              |
| p           |            | SQL 쿼리의 `?` 바인드 자리표시자에 넣을 파라미터 JSON 배열. 예: `"p": ["name", 1234, 1.23, true]`. SQL에서는 `?`를 자리표시자로 사용합니다: `SELECT * FROM EXAMPLE WHERE name = ? LIMIT ?` |
| format      | `json`    | 결과 데이터 형식: json, csv, box, ndjson |
| timeformat  | `ns`      | 시간 형식: s, ms, us, ns    |
| tz          | `UTC`     | 시간대: UTC, Local, 지역 지정 |
| compress    | _압축 안 함_   | 압축 방식: gzip      |
| rownum      | `false`   | rownum 포함 여부: true, false |
| binaryformat | `hex`    | (v8.5.2부터) 응답에서 이진 컬럼 데이터의 인코딩 방식을 제어합니다. 지원 값: `hex`(기본), `base64`, `bytes`, `preview` |

**`format=json`에서 사용 가능한 파라미터**

* 이 옵션들은 `format=json`일 때만 사용할 수 있습니다. 서로 배타적이므로 요청당 하나만 적용됩니다.

| 파라미터       | 기본값 | 설명                   |
|:----------- |---------|:----------------------------- |
| transpose   | false   | rows 대신 cols 배열을 생성합니다.|
| rowsFlatten | false   | JSON 객체의 *rows* 필드 배열 차원을 낮춥니다.|
| rowsArray   | false   | 레코드마다 객체 배열만 담은 JSON을 생성합니다.|

**`format=csv`에서 사용 가능한 파라미터**

| 파라미터       | 기본값 | 설명                    |
|:----------- |---------|:------------------------------ |
| header      |         | `skip`은 헤더 줄을 넣지 않으며 `heading=false`와 같습니다 |
| heading     | `true`  | 헤더 줄 표시: true, false. 폐기됨, `header`를 사용하세요  |
| precision   | `-1`    | 실수 값의 정밀도. -1은 반올림 없음, 0은 정수 |

**사용 가능한 시간 형식**
 
* 사용 가능한 시간 형식은 API 옵션/timeformat 항목을 참고하세요.

## Outputs

응답 내용이 너무 커서 전체 길이를 알 수 없으면 `Transfer-Encoding: chunked` 헤더가 설정되고 `Content-Length` 헤더는 생략됩니다. 응답의 끝은 연속된 두 개의 개행 문자(`\n\n`)로 식별합니다.

- `Transfer-Encoding: chunked`: 데이터를 여러 조각으로 나눠 보낸다는 뜻이며 스트리밍에 유용합니다.
- `Content-Length` 없음: 응답 본문의 전체 길이를 미리 알 수 없다는 뜻입니다.

### JSON

`/db/query` API의 기본 출력 형식은 json입니다.
질의 파라미터로 `format=json`을 지정하거나 생략하면 기본값이 적용됩니다.

**HTTP:**
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 2
```
~~~

**cURL:**
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2"
```

The server responses in `Content-Type: application/json`.

| 이름         | 타입       |  설명                        |
|:------------ |:-----------|:------------------------------------|
| **success**  | bool       | 쿼리 실행이 성공하면 `true` |
| **reason**   | string     | 실행 결과 메시지. `success`가 `false`이면 오류 메시지가 담깁니다  |
| **elapse**   | string     | 질의 실행에 걸린 시간                 |
| data         |            | 실행이 성공했을 때만 존재  |
| data.columns | 문자열 배열 | 결과의 컬럼을 나타냅니다    |
| data.types   | 문자열 배열 | 결과의 데이터 타입을 나타냅니다 |
| data.rows    | 레코드 배열 | 결과 집합의 레코드를 나타내는 배열.<br/>`transpose`가 `true`이면 `cols`로 대체됩니다 |
| data.cols    | 시리즈 배열  | 결과 집합의 컬럼 시리즈를 나타내는 배열.<br/> `transpose`가 `true`일 때 존재합니다 |

**default:**
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 3
```
~~~

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      [ "wave.sin", 1705381958775759000, 0.8563571936170834 ],
      [ "wave.sin", 1705381958785759000, 0.9011510331449053 ],
      [ "wave.sin", 1705381958795759000, 0.9379488170706388 ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "1.887042ms"
}
```

**transpose:**
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 3
    &transpose=true
```
~~~

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "cols": [
      [ "wave.sin", "wave.sin", "wave.sin" ],
      [ 1705381958775759000, 1705381958785759000, 1705381958795759000 ],
      [ 0.8563571936170834, 0.9011510331449053, 0.9379488170706388 ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "4.090667ms"
}
```

**rowsFlatten:**
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 3
    &rowsFlatten=true
```
~~~

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      "wave.sin", 1705381958775759000, 0.8563571936170834,
      "wave.sin", 1705381958785759000, 0.9011510331449053,
      "wave.sin", 1705381958795759000, 0.9379488170706388
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "2.255625ms"
}
```

**rowsArray:**
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 3
    &rowsArray=true
```
~~~

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      { "NAME": "wave.sin", "TIME": 1705381958775759000, "VALUE": 0.8563571936170834 },
      { "NAME": "wave.sin", "TIME": 1705381958785759000, "VALUE": 0.9011510331449053 },
      { "NAME": "wave.sin", "TIME": 1705381958795759000, "VALUE": 0.9379488170706388 }
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "3.178458ms"
}
```

### NDJSON

요청에 질의 파라미터 `format=ndjson`을 지정합니다.

NDJSON(Newline Delimited JSON)은 각 줄이 유효한 JSON 객체인 스트리밍 JSON 형식입니다. JSON 객체를 한 번에 하나씩 처리할 수 있어 대용량 데이터셋이나 스트리밍 데이터를 다룰 때 유용합니다.

**HTTP:**
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 2
    &format=ndjson
```
~~~

**cURL:**
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2" \
    --data-urlencode "format=ndjson"
```

응답은 `Content-Type: application/x-ndjson`으로 전달됩니다.

```json
{"NAME":"wave.sin","TIME":1705381958775759000,"VALUE":0.8563571936170834}
{"NAME":"wave.sin","TIME":1705381958785759000,"VALUE":0.9011510331449053}

```

### CSV

요청에 질의 파라미터 `format=csv`를 지정합니다.

CSV 형식도 한 번에 한 줄씩 처리할 수 있어 대용량 데이터셋이나 스트리밍 데이터 처리에 유용합니다.

**HTTP:**
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 2
    &format=csv
```
~~~

**cURL:**
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2" \
    --data-urlencode "format=csv"
```

응답은 `Content-Type: text/csv; utf-8`로 전달됩니다

```csv
NAME,TIME,VALUE
wave.sin,1705381958775759000,0.8563571936170834
wave.sin,1705381958785759000,0.9011510331449053
```

### BOX

요청에 질의 파라미터 `format=box`를 지정합니다.

**HTTP:**
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 2
    &format=box
```
~~~

**cURL:**
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2" \
    --data-urlencode "format=box"
```

결과 데이터를 아스키 박스 형태의 일반 텍스트로 표시합니다. 응답의 Content-Type은 `plain/text`입니다 

```
+----------+---------------------+--------------------+
| NAME     | TIME(UTC)           | VALUE              |
+----------+---------------------+--------------------+
| wave.sin | 1705381958775759000 | 0.8563571936170834 |
| wave.sin | 1705381958785759000 | 0.9011510331449053 |
+----------+---------------------+--------------------+
```

**CSV 형식 응답**

요청에 질의 파라미터 `format=csv`를 지정합니다.

**HTTP:**
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 2
    &format=csv
```
~~~

**cURL:**
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2" \
    --data-urlencode "format=csv"
```

응답은 `Content-Type: text/csv`로 전달됩니다

```csv
NAME,TIME,VALUE
wave.sin,1705381958775759000,0.8563571936170834
wave.sin,1705381958785759000,0.9011510331449053
```

## POST JSON

아래 예제처럼 JSON 형태로 질의를 요청할 수도 있습니다.

**요청 JSON 메시지**

**HTTP:**
~~~
```http
POST http://127.0.0.1:5654/db/query
Content-Type: application/json

{
  "q": "select * from EXAMPLE limit 2"
}
```
~~~

**cURL:**
```sh
curl -o - -X POST http://127.0.0.1:5654/db/query \
    -H 'Content-Type: application/json' \
    -d '{ "q":"select * from EXAMPLE limit 2" }'
```

## POST Form

HTML 폼 데이터 형식도 사용할 수 있습니다. 이 경우 HTTP 헤더 `Content-type`은 `application/x-www-form-urlencoded` 여야 합니다.

**HTTP:**
~~~
```http
POST http://127.0.0.1:5654/db/query
Content-Type: application/x-www-form-urlencoded

q=select * from EXAMPLE limit 2
```
~~~

**cURL:**
```sh
curl -o - -X POST http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2"
```

## 예제s

API의 자세한 내용은 다음을 참고하세요 
- 요청 엔드포인트와 파라미터
- 위키백과의 시간대 목록

이 튜토리얼을 위해 아래 데이터를 미리 입력하세요.

### 1단계: 테이블 생성

~~~
```http
POST http://127.0.0.1:5654/db/query
Content-Type: application/json

{
  "q":"create tag table if not exists EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
}
```
~~~

### 2단계: 데이터 입력

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=ns
Content-Type: application/json

{
    "data":{
      "columns":["NAME","TIME","VALUE"],
      "rows":[
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

### CSV 형식으로 조회

**요청**

CSV 형식으로 받으려면 `format=csv` 질의 파라미터를 지정합니다.

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 5
    &format=csv
```
~~~

**응답**

```
NAME,TIME,VALUE
wave.sin,1676432361000000000,0.111111
wave.sin,1676432362111111111,0.222222
wave.sin,1676432363222222222,0.333333
wave.sin,1676432364333333333,0.444444
wave.sin,1676432365444444444,0.555555
```

### BOX 형식으로 조회

**요청**

BOX 형식으로 받으려면 `format=box` 질의 파라미터를 지정합니다.

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 5
    &format=box
```
~~~

**응답**

```
+----------+---------------------+----------+
| NAME     | TIME                | VALUE    |
+----------+---------------------+----------+
| wave.sin | 1676432361000000000 | 0        |
| wave.sin | 1676432362111111111 | 0.406736 |
| wave.sin | 1676432363222222222 | 0.743144 |
| wave.sin | 1676432364333333333 | 0.951056 |
| wave.sin | 1676432365444444444 | 0.994522 |
+----------+---------------------+----------+
```

### BOX 형식으로 조회 (rownum 포함)

**요청**

BOX 형식으로 받으려면 `format=box` 질의 파라미터를 지정합니다.

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 5
    &format=box
    &rownum=true
```
~~~

**응답**

```
+--------+----------+---------------------+----------+
| ROWNUM | NAME     | TIME                | VALUE    |
+--------+----------+---------------------+----------+
|      1 | wave.sin | 1676432361000000000 | 0.111111 |
|      2 | wave.sin | 1676432362111111111 | 0.222222 |
|      3 | wave.sin | 1676432363222222222 | 0.333333 |
|      4 | wave.sin | 1676432364333333333 | 0.444444 |
|      5 | wave.sin | 1676432365444444444 | 0.555555 |
+--------+----------+---------------------+----------+
```


### BOX 형식으로 조회 (헤더 없이)

**요청**

헤더 없는 BOX 형식으로 받으려면 `format=box`와 `header=skip` 질의 파라미터를 지정합니다.

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 5
    &format=box
    &header=skip
```
~~~

**응답**

```
+----------+---------------------+----------+
| wave.sin | 1676432361000000000 | 0        |
| wave.sin | 1676432362111111111 | 0.406736 |
| wave.sin | 1676432363222222222 | 0.743144 |
| wave.sin | 1676432364333333333 | 0.951056 |
| wave.sin | 1676432365444444444 | 0.994522 |
+----------+---------------------+----------+
```

### BOX 형식으로 조회 (값을 INTEGER로)

**요청**

정수 정밀도의 BOX 형식으로 받으려면 `format=box`와 `precision=0` 질의 파라미터를 지정합니다.

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 5
    &format=box
    &precision=0
```
~~~

**응답**

```
+----------+---------------------+-------+
| NAME     | TIME                | VALUE |
+----------+---------------------+-------+
| wave.sin | 1676432361000000000 | 0     |
| wave.sin | 1676432362111111111 | 0     |
| wave.sin | 1676432363222222322 | 0     |
| wave.sin | 1676432364333333233 | 0     |
| wave.sin | 1676432365444444444 | 1     |
+----------+---------------------+-------+
```
