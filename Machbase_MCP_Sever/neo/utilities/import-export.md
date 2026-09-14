# Machbase Neo Import & Export Guide

## Import CSV

```sh
curl -o - https://docs.machbase.com/assets/example/example.csv.gz | \
machbase-neo shell import   \
    --input -               \
    --compress gzip         \
    --timeformat s          \
    EXAMPLE
```
위 명령은 `curl`로 원격 웹 서버에서 압축된 csv 파일을 내려받습니다.
`-o -` 옵션을 지정했으므로 데이터(압축된 바이너리)를 표준 출력 스트림으로 내보내고, 그 출력 스트림이 `machbase-neo shell import`로 전달되어 `--input -` 플래그로 읽힙니다.

두 명령을 파이프 `|`로 연결하면 로컬 저장소를 쓰는 임시 파일을 만들 필요가 없습니다.

결과 출력에 1,000건이 입력되었다고 나옵니다.

```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  5352  100  5352    0     0   547k      0 --:--:-- --:--:-- --:--:-- 5226k
import total 1000 record(s) inserted
```

또는 데이터 파일을 로컬 저장소에 내려받은 뒤 그 파일에서 입력할 수도 있습니다.

```sh
curl -o data.csv.gz https://docs.machbase.com/assets/example/example.csv.gz
```

압축된 csv 파일과 압축되지 않은 csv 파일 모두 입력할 수 있습니다.

그다음 `--input <file>` 플래그로 로컬 저장소의 csv 파일을 입력합니다. 파일이 gzip 형식이면 `--compress gzip` 옵션을 사용합니다.

```sh
machbase-neo shell import \
    --input ./data.csv    \
    --timeformat s        \
    EXAMPLE
```

테이블을 조회해 확인합니다.

```sh
machbase-neo shell sql "select * from example order by time desc limit 5"
```
```
 ROWNUM  NAME      TIME(UTC)            VALUE     
──────────────────────────────────────────────────
 1       wave.sin  2023-02-15 03:47:50  0.994540  
 2       wave.cos  2023-02-15 03:47:50  -0.104353 
 3       wave.sin  2023-02-15 03:47:49  0.951002  
 4       wave.cos  2023-02-15 03:47:49  0.309185  
 5       wave.cos  2023-02-15 03:47:48  0.669261  
```

샘플 파일에는 총 1,000건이 들어 있고, 입력 후 테이블에 전부 들어 있습니다.

```sh
machbase-neo shell sql "select count(*) from example"
```
```
 ROWNUM  COUNT(*) 
──────────────────
 1       1000     
```

## Export CSV

테이블 내보내기는 간단합니다. 데이터를 저장할 파일 경로를 `--output` 플래그로 지정합니다.
`--format csv`를 지정하면 machbase-neo가 데이터를 csv 형식으로 내보냅니다.
`--timeformat ns`를 지정하면 출력의 모든 datetime 필드가 Unix epoch 나노초로 표현됩니다.

```sh
machbase-neo shell export --output ./example_out.csv --format csv --timeformat ns EXAMPLE
```

## 내보내기와 입력을 조합한 테이블 복사

내보내기와 입력을 조합하면 로컬 저장소에 임시 파일 없이 테이블을 "복사"할 수 있습니다.

데이터를 복사해 넣을 새 테이블을 만듭니다.

```sh
machbase-neo shell sql "create tag table EXAMPLE_COPY (name varchar(100) primary key, time datetime basetime, value double)"
```

그다음 입력 명령과 내보내기 명령을 함께 실행합니다.

```sh
machbase-neo shell export       \
    --output -                  \
    --no-heading --no-footer    \
    --format csv                \
    --timeformat ns             \
    EXAMPLE  |  \
machbase-neo shell import       \
    --input -                   \
    --format csv                \
    --timeformat ns             \
    EXAMPLE_COPY
```

새로 만든 테이블의 레코드 수를 조회합니다.

```sh
machbase-neo shell sql "select count(*) from EXAMPLE_COPY"
```
```
 ROWNUM  COUNT(*) 
──────────────────
 1       1000     
```

이 예제는 *A* 데이터베이스의 테이블을 *B* 데이터베이스로 "복사"하려는 상황에 적용할 수 있습니다.
"import"과 "export" 명령 중 하나에 `--server <address>` 플래그로 원격 machbase-neo 서버 프로세스를 지정할 수 있고,
두 명령이 서로 다른 원격 서버를 대상으로 실행되게 할 수도 있습니다.

## 질의 결과에서 입력하기

"select" 질의와 import 명령을 조합해 봅시다.

```sh
machbase-neo shell sql \
    --output -         \
    --format csv       \
    --no-rownum        \
    --no-heading       \
    --no-footer        \
    --timeformat ns    \
    "select * from example where name = 'wave.sin' order by time" | \
machbase-neo shell import \
    --input -             \
    --format csv          \
    EXAMPLE_COPY
```

태그 이름이 `wave.sin`인 데이터를 조회해 `EXAMPLE_COPY` 테이블에 입력합니다.
`import` 명령이 들어오는 csv 데이터의 필드 수와 데이터 타입을 확인해야 하므로 `sql` 명령에 `--no-rownum`과 `--no-heading` 옵션이 필요합니다.

## HTTP API로 질의 결과에서 입력하기

질의 결과에서 입력하는 시나리오는 machbase-neo의 HTTP API로도 할 수 있습니다.

```sh
curl -o - http://127.0.0.1:5654/db/query        \
    --data-urlencode "q=select * from EXAMPLE order by time desc limit 100" \
    --data-urlencode "format=csv"                \
    --data-urlencode "heading=false" |           \
curl http://127.0.0.1:5654/db/write/EXAMPLE_COPY \
    -H "Content-Type: text/csv"                  \
    -X POST --data-binary @- 
```

## 입력 방식: Insert와 Append

import 명령은 기본적으로 "INSERT INTO..." 문으로 들어오는 데이터를 씁니다.
쓸 레코드 수가 적으면 "append" 방식과 큰 차이가 없습니다.

대량의 데이터(예: 수십만 건 이상)가 예상된다면,
`--method append` 플래그로 machbase-neo가 "append" 방식을 쓰도록 지정하세요. 
이 플래그가 없으면 `--method insert`가 암묵적으로 지정되어 "INSERT INTO..." 문을 사용합니다. 

## 상세 예제

import 기능으로 데이터 파일을 테이블에 쓸 수 있습니다.

> 원활한 실습을 위해 다음 질의를 실행해 테이블과 데이터를 준비하세요.

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
```

### CSV 입력 예제

`data.csv`에 테스트 데이터를 만듭니다.

```
name-0,1687405320000000000,123.456
name-1,1687405320000000000,234.567000
name-2,1687405320000000000,345.678000
```

Import data

```sh
machbase-neo shell import \
    --input ./data.csv    \
    --timeformat ns        \
    EXAMPLE
```

Select data

```sh
machbase-neo shell sql "SELECT * FROM EXAMPLE"

 ROWNUM  NAME    TIME(LOCAL)          VALUE   
──────────────────────────────────────────────
      1  name-0  2023-06-22 12:42:00  123.456 
      2  name-1  2023-06-22 12:42:00  234.567 
      3  name-2  2023-06-22 12:42:00  345.678 
3 rows fetched.
```

### TQL로 입력하기

**텍스트 가져오기**

`import-data.csv`에 테스트 데이터를 만듭니다.

```
1,100,value,10
2,200,value,11
3,140,value,12
```

아래 코드를 TQL 편집기에 붙여 넣고 `import-tql-csv.tql`로 저장합니다.

```js
STRING(payload() ?? `1,100,value,10
2,200,value,11
3,140,value,12`, separator('\n'))

SCRIPT({
    str =  $.values[0].trim().split(',');
    $.yield(
        "tag-" + str[0],
        (new Date().getTime()*1000000),
        parseInt(str[1])+parseInt(str[3])
    )
})
APPEND(table("example"))
```

테스트 데이터 CSV를 해당 tql로 POST합니다.

```sh
curl -o - --data-binary @import-data.csv http://127.0.0.1:5654/db/tql/import-tql-csv.tql

append 3 rows (success 3, fail 0).
```

Select data

```sh
machbase-neo shell sql "select * from example"

 ROWNUM  NAME   TIME(LOCAL)          VALUE 
───────────────────────────────────────────
      1  tag-1  1970-01-01 09:00:00  10    
      2  tag-2  1970-01-01 09:00:00  11    
      3  tag-3  1970-01-01 09:00:00  12    
3 rows fetched.
```

**JSON 가져오기**

`import-data.json`에 저장할 테스트 데이터를 준비합니다.

```json
{
  "tag": "pump",
  "data": {
    "string": "Hello TQL?",
    "number": "123.456",
    "time": 1687405320,
    "boolean": true
  },
  "array": ["elements", 234.567, 345.678, false]
}
```

아래 코드를 TQL 편집기에 붙여 넣고 `import-tql-json.tql`로 저장합니다.

```js
BYTES( payload() ?? {
    {
        "tag": "pump",
        "data": {
            "string": "Hello TQL?",
            "number": "123.456",
            "time": 1687405320,
            "boolean": true
        },
        "array": ["elements", 234.567, 345.678, false]
    }
})
SCRIPT({
    obj = JSON.parse($.values[0]);
    $.yield(obj.tag+"_0", obj.data.time*1000000000, obj.data.number)
    $.yield(obj.tag+"_1", obj.data.time*1000000000, obj.data.array[1])
    $.yield(obj.tag+"_2", obj.data.time*1000000000, obj.data.array[2])
    for (i = 0; i < obj.array.length; i++) {
    }
})
APPEND(table("example"))
```

테스트 데이터 JSON을 해당 tql로 POST합니다.

```sh
curl -o - --data-binary @import-data.json http://127.0.0.1:5654/db/tql/import-tql-json.tql

append 2 rows (success 2, fail 0).
```

Select data

```sh
machbase-neo shell sql "select * from example"

 ROWNUM  NAME    TIME(LOCAL)          VALUE   
──────────────────────────────────────────────
      1  tag-1   1970-01-01 09:00:00  10      
      2  pump_2  2023-06-22 12:42:00  345.678 
      3  tag-2   1970-01-01 09:00:00  11      
      4  tag-3   1970-01-01 09:00:00  12      
      5  pump_1  2023-06-22 12:42:00  234.567 
5 rows fetched.
```

### 브리지에서 입력하기

**준비**

```sh
bridge add -t sqlite mem file::memory:?cache=shared;

bridge exec mem create table if not exists mem_example(name varchar(20), time datetime, value double);

bridge exec mem insert into mem_example values('tag0', '2021-08-12', 10);
bridge exec mem insert into mem_example values('tag0', '2021-08-13', 11);
```

**브리지에서 데이터 입력**

아래 코드를 TQL 편집기에 붙여 넣고 실행합니다

```js
SQL(bridge('mem'), "select * from mem_example")
APPEND(table('example'))
```

Select data

```sh
machbase-neo shell sql "select * from example"

 ROWNUM  NAME  TIME(LOCAL)          VALUE 
──────────────────────────────────────────
      1  tag0  2021-08-12 09:00:00  10    
      2  tag0  2021-08-13 09:00:00  11    
2 rows fetched.
```

### CSV 내보내기 예제

Export data

```sh
machbase-neo shell export      \
    --output ./data_out.csv    \
    --format csv               \
    --timeformat ns            \
    EXAMPLE
```

Select data

```sh
cat data_out.csv 

TAG0,1628694000000000000,100
TAG0,1628780400000000000,110
```

### JSON 내보내기 예제

Export data

```sh
machbase-neo shell export      \
    --output ./data_out.json   \
    --format json              \
    --timeformat ns            \
    EXAMPLE
```

Select data

```sh
cat data_out.json

{
  "data": {
    "columns": [
      "NAME",
      "TIME",
      "VALUE"
    ],
    "types": [
      "string",
      "datetime",
      "double"
    ],
    "rows": [
      [
        "TAG0",
        1628694000000000000,
        100
      ],
      [
        "TAG0",
        1628780400000000000,
        110
      ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "1.847207ms"
}
```

### TQL로 내보내기

**CSV 내보내기**

```js
SQL(`select * from example`)
CSV()
```

**JSON 내보내기**

```js
SQL(`select * from example`)
JSON()
```

**TQL 스크립트로 CSV 내보내기**

아래 코드를 TQL 편집기에 붙여 넣고 `export-tql-csv.tql`로 저장합니다.

```js
SQL( 'select * from example limit 30' )
SCRIPT({
    if  ($.values[2] % 2 == 0) {
        r_value = "even"
    } else {
        r_value = "odd"
    }

    $.yield($.key + "-tql", $.values[2],  r_value)
})
CSV()
```

웹 브라우저에서 http://127.0.0.1:5654/db/tql/export-tql-csv.tql 로 열거나 터미널에서 *curl* 명령을 사용합니다.

```sh
TAG1-tql,11,odd
TAG0-tql,10,even
```

### 브리지로 내보내기

**준비**

```sh
bridge add -t sqlite mem file::memory:?cache=shared;

bridge exec mem create table if not exists mem_example(name varchar(20), time datetime, value double);
```

**브리지로 데이터 내보내기**

아래 코드를 TQL 편집기에 붙여 넣고 실행합니다

```js
SQL("select * from example")
INSERT(bridge('mem'), table('mem_example'), 'name', 'time', 'value')
```

브리지 테이블 데이터를 조회합니다

```sh
machbase-neo shell bridge query mem "select * from mem_example";

┌──────┬───────────────────────────────┬───────┐
│ NAME │ TIME                          │ VALUE │
├──────┼───────────────────────────────┼───────┤
│ TAG0 │ 2021-08-12 00:00:00 +0900 KST │    10 │
│ TAG1 │ 2021-08-13 00:00:00 +0900 KST │    11 │
└──────┴───────────────────────────────┴───────┘
```

---

## 빠른 참조

| 동작 | 명령 | 주요 옵션 |
|-----------|---------|-------------|
| Import CSV | `machbase-neo shell import` | `--input`, `--timeformat`, `--compress` |
| Export CSV | `machbase-neo shell export` | `--output`, `--format csv`, `--timeformat` |
| HTTP로 입력 | `/db/write/`에 `curl` | `Content-Type: text/csv` |
| HTTP로 내보내기 | `/db/query`에 `curl` | `format=csv`, `heading=false` |
| Copy Table | `export \| import` | `--output -`, `--input -` |
| 대량 데이터 입력 | `--method append` | 수십만 건 규모에 사용 |
| TQL 입력 | `APPEND(table())` | 데이터 가공을 함께 수행 |
| 브리지 연동 | `SQL(bridge())` | 외부 데이터베이스 연결 |

### 공통 플래그

| 플래그 | 설명 | 예 |
|------|-------------|---------|
| `--input` | 입력 파일 경로, `-`이면 표준 입력 | `--input data.csv` |
| `--output` | 출력 파일 경로, `-`이면 표준 출력 | `--output result.csv` |
| `--format` | 데이터 형식 (csv, json) | `--format csv` |
| `--timeformat` | 시간 형식 (s, ms, us, ns) | `--timeformat ns` |
| `--compress` | 압축 방식 | `--compress gzip` |
| `--method` | 입력 방식 (insert, append) | `--method append` |
