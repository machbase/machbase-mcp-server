# Machbase Neo TQL SCRIPT Function

TQL은 **SRC**와 **MAP** 양쪽에서 JavaScript(ECMA5)를 사용할 수 있는 `SCRIPT()` 함수를 지원합니다(버전 8.0.36 이상). 개발자가 익숙한 프로그래밍 언어를 그대로 쓸 수 있어 TQL 안에서 더 동적이고 강력한 스크립트를 작성할 수 있습니다.

**문법**: `SCRIPT({main_code})`

**문법**: `SCRIPT({init_code}, {main_code})`

**문법**: `SCRIPT({init_code}, {main_code}, {deinit_code})`

**Parameters:**
- `init_code` - 초기화 코드 (선택이지만 deinit_code가 있으면 필수)
- `main_code` - 스크립트 코드 (필수)
- `deinit_code` - 종료 코드 (선택)

`init_code`는 선택이며 처음에 한 번만 실행됩니다. `main_code`는 필수이며 생략할 수 없습니다.

## 주의사항

- `use strict`는 아무 동작도 하지 않습니다.
- ECMA5만 지원합니다. Typed Array나 백틱 문자열 보간 같은 일부 ES6 기능은 지원되지 않습니다.
- 정규식이 ECMA5 사양과 완전히 호환되지는 않습니다. 다음 정규식 문법은 호환되지 않습니다:
    - `(?=)` 긍정 전방탐색 — 파싱 오류가 발생합니다
    - `(?!)` 부정 전방탐색 — 파싱 오류가 발생합니다
    - `\1`, `\2`, `\3`, ... 역참조 — 파싱 오류가 발생합니다

## JSH Modules

*버전 8.0.52 이상*

`require()`로 JSH 모듈을 SCRIPT()에 가져올 수 있습니다. JSH 애플리케이션 내부에서만 접근 가능한 `@jsh/process`를 제외한 모든 "@jsh" 모듈을 사용할 수 있습니다.

```js
SCRIPT({
    const { arrange } = require("@jsh/generator")
    arrange(0, 6, 3).forEach((i) =>$.yield(i))
})
CSV()
```

## 컨텍스트 객체

Machbase-neo는 `$` 변수를 컨텍스트 객체로 제공합니다. JavaScript는 이 컨텍스트를 통해 레코드와 데이터베이스에 접근하고 레코드를 내보낼 수 있습니다.

**속성과 메서드:**
- `$.payload` - 요청의 입력 데이터. `SCRIPT()`가 SRC 노드로 쓰일 때만 사용 가능하며, 그 외에는 `undefined`입니다.
- `$.params` - 요청의 입력 쿼리 파라미터.
- `$.result` - `SCRIPT()` 함수가 내보내는 결과 컬럼의 이름과 타입을 지정합니다.
- `$.key`, `$.values` - 현재 레코드의 키와 값에 접근하는 JavaScript 지점. `SCRIPT()`가 MAP 함수일 때만 사용 가능합니다.
- `$.yield()` - 값들로 새 레코드를 내보냅니다
- `$.yieldKey()` - 키와 값들로 새 레코드를 내보냅니다
- `$.yieldArray()` - `$.yield()`와 같지만 여러 인자 대신 배열 하나만 받습니다.
- `$.db()` - 새 데이터베이스 연결을 반환합니다.
- `$.db().query()` - SQL 쿼리를 실행합니다.
- `$.db().exec()` - SELECT가 아닌 SQL을 실행합니다.
- `$.request().do()` - 원격 서버로 HTTP 요청을 보냅니다.

### $.payload

JavaScript는 `$.payload`로 요청의 입력 데이터에 접근할 수 있습니다. 입력 데이터가 없으면 `$.payload`는 `undefined`입니다. `$.payload`는 `SCRIPT()`가 SRC 노드로 쓰일 때만 사용 가능합니다.

```js
SCRIPT({
    var data = $.payload;
    if (data === undefined) {
        data = '{ "prefix": "name", "offset": 0, "limit": 10}';
    }
    var obj = JSON.parse(data);
    $.yield(obj.prefix, obj.offset, obj.limit);
})
CSV()
```

요청 본문 없이 tql 파일을 호출하면 `$.payload`가 `undefined`가 됩니다.

```sh
curl -o - -X POST http://127.0.0.1:5654/db/tql/test.tql
```

그러면 결과는 기본값 `name,0,10` 입니다.

사용자 데이터와 함께 tql 파일을 호출합니다.

```sh
curl -o - -X POST http://127.0.0.1:5654/db/tql/test.tql \
-d '{"prefix":"testing", "offset":10, "limit":10}'
```

그러면 결과는 `testing,10,10` 입니다.

### $.params

JavaScript는 `$.params`로 요청의 쿼리 파라미터에 접근할 수 있습니다. 파라미터 값은 점 표기법(`$.params.name`)이나 대괄호 표기법(`$.params["name"]`) 두 가지로 접근할 수 있으며, 둘은 서로 바꿔 쓸 수 있습니다.

```js
SCRIPT({
    var prefix = $.params.prefix ? $.params.prefix : "name";
    var offset = $.params.offset ? $.params.offset : 0;
    var limit = $.params.limit ? $.params.limit: 10;
    $.yield(prefix, offset, limit);
})
CSV()
```

파라미터 없이 tql 파일을 호출합니다.

```sh
curl -o - -X POST http://127.0.0.1:5654/db/tql/test.tql
```

결과는 기본값 `name,0,10` 입니다.

파라미터와 함께 tql 파일을 호출합니다.

```sh
curl -o - -X POST "http://127.0.0.1:5654/db/tql/test.tql?"\
"prefix=testing&offset=12&limit=20"
```

결과는 `testing,12,20` 입니다.

### $.result

`SCRIPT` 함수가 내보내는 결과 데이터의 타입을 지정합니다. 아래 예제처럼 init 코드 구역에서 동작합니다.

```js
SCRIPT({
    $.result = {
        columns: ["val", "sig"],
        types: ["double", "double"] 
    }
},{
    for (i = 1.0; i <= 5.0; i+=0.03) {
        val = Math.round(i*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        $.yield( val, sig );
    }
})
JSON()
```

### $.key

현재 레코드의 키에 접근합니다. `SCRIPT`가 MAP 함수로 쓰일 때만 정의되며, SRC 함수로 쓰이면 `undefined`입니다.

```js
SCRIPT({
    for( i = 0; i < 3; i++) {
        $.yieldKey(i, "hello-"+(i+1));
    }
})
SCRIPT({
    $.yieldKey($.key, $.values[0], 'key is '+$.key);
})
CSV()
```

**Output:**

```csv
hello-1,key is 0
hello-2,key is 1
hello-3,key is 2
```

### $.values

현재 레코드의 값들에 접근합니다. `SCRIPT`가 MAP 함수로 쓰일 때만 정의되며, SRC 함수로 쓰이면 `undefined`입니다.

```js
SCRIPT({
        $.yield("string", 10, 3.14);
})
SCRIPT({
    $.yield(
        "the first value is "+$.values[0],
        "2nd value is "+$.values[1],
        "3rd is "+$.values[2]
    );
})
CSV()
```

**Output:**

`the first value is string,2nd value is 10,3rd is 3.14`

### $.yield()

다음 단계로 새 레코드를 내보냅니다. 키는 순차 증가 번호로 자동 지정됩니다.

```js
$.yield(field1, field2, field3);
```

### $.yieldKey()

`yieldKey()`는 `$.yield()`와 비슷하지만 첫 번째 인자가 레코드의 키를 지정한다는 점이 다릅니다.

```js
$.yieldKey(key, field1, field2, field3);
```

### $.yieldArray()

*버전 8.0.39 이상*

배열에 담긴 레코드를 내보냅니다. 가변 인자를 받는 `$.yield()`와 달리 `$.yieldArray()`는 레코드를 나타내는 배열 하나를 인자로 받습니다. 배열을 다룰 때 유용합니다.

```js
var arr = [];
for( i = 0; i < unknown; i++) {
    arr.push(field_values[i]);
}
$.yieldArray(arr);
```

### $.db()

새 데이터베이스 연결을 반환합니다. 이 연결은 `query()`, `exec()` 함수를 제공합니다.

예를 들어 `$.db({bridge: "sqlite"})`처럼 옵션 객체를 인자로 주면 machbase 대신 브리지로 연결된 데이터베이스에 대한 새 연결을 반환합니다.

**Option:**

옵션 파라미터는 버전 8.0.37 이상에서 지원됩니다

```js
{
    bridge: "name", // bridge name
}
```

### $.db().query()

JavaScript는 `$.db().query()`로 데이터베이스에 질의할 수 있습니다. `query()`의 반환값에 `forEach()`로 콜백 함수를 적용하면 조회 결과를 순회할 수 있습니다.

`.forEach()`의 콜백 함수가 명시적으로 `false`를 반환하면 순회가 즉시 중단됩니다. `true`를 반환하거나 아무것도 반환하지 않으면(즉 `undefined`) 조회 결과 끝까지 순회를 계속합니다.

#### MACHBASE 조회

```js
SCRIPT({
  var data = $.payload;
  if (data === undefined) {
    data = '{ "tag": "cpu.percent", "offset": 0, "limit": 3 }';
  }
  var obj = JSON.parse(data);
  $.db()
   .query("SELECT name, time, value FROM example WHERE name = ? LIMIT ?, ?",
    obj.tag, obj.offset, obj.limit
  ).forEach( function(row){
    name = row[0]
    time = row[1]
    value = row[2]
    $.yield(name, time, value);
  })
})
CSV()
```

**Output:**

```csv
cpu.percent,1725330085908925000,73.9
cpu.percent,1725343895315420000,73.6
cpu.percent,1725343898315887000,6.1
```

#### BRIDGE-SQLITE 조회

```js
SCRIPT({
  var data = $.payload;
  if (data === undefined) {
    data = '{ "tag": "testing", "offset": 0, "limit": 3 }';
  }
  var obj = JSON.parse(data);
  $.db({bridge:"mem"})
   .query("SELECT name, time, value FROM example WHERE name = ? LIMIT ?, ?",
    obj.tag, obj.offset, obj.limit
  ).forEach( function(row){
    name = row[0]
    time = row[1]
    value = row[2]
    $.yield(name, time, value);
  })
})
CSV()
```

**Output:**

```csv
testing,1732589744886,16.70559756851126
testing,1732589744886,49.93214293713331
testing,1732589744886,54.485508690434905
```

#### $.yieldArray() 사용

`$.db().query()` 결과에서 특정 컬럼만 골라 `$.yield()`로 내보냅니다. 모든 컬럼을 한 번에 내보내려면 `$.yieldArray()`(버전 8.0.39 이상)를 사용하세요.

```js
SCRIPT({
    var sql = "SELECT name, time, value FROM example WHERE name = 'cpu.percent' LIMIT 3";
    $.db().query(sql).forEach( function(row){
        $.yieldArray(row);
    });
})
CSV()
```

#### $.db().query().yield() 사용

또는 `$.db().query().yield()`(버전 8.0.39 이상)로 자동으로 내보낼 수 있습니다.

```js
SCRIPT({
    var tags = ["mem.total", "mem.used", "mem.free"];
    for( i = 0; i < tags.length; i++) {
        $.yield(tags[i]);
    }
})
SCRIPT({
    var sql = "SELECT * FROM example WHERE name = ? LIMIT 1";
    $.db().query(sql, $.values[0]).yield();
})
CSV( header(true) )
```

### $.db().exec()

SELECT가 아닌 SQL이라면 `$.db().exec()`로 INSERT, DELETE, CREATE TABLE 문을 실행합니다.

#### MACHBASE에서 실행

```js
SCRIPT({
    for( i = 0; i < 3; i++) {
        ts = Date.now()*1000000; // ms to ns
        $.yield("testing", ts, Math.random()*100);
    }
})
SCRIPT({
    // This section contains initialization code
    // that runs once before processing the first record.
    err = $.db().exec("CREATE TAG TABLE IF NOT EXISTS example ("+
        "NAME varchar(80) primary key,"+
        "TIME datetime basetime,"+
        "VALUE double"+
    ")");
    if (err instanceof Error) {
        console.error("Fail to create table", err.message);
    }
}, {
    // This section contains the main code
    // that runs over every record.
    err = $.db().exec("INSERT INTO example values(?, ?, ?)", 
        $.values[0], $.values[1], $.values[2]);
    if (err instanceof Error) {
        console.error("Fail to insert", err.message);
    } else {
        $.yield($.values[0], $.values[1], $.values[2]);
    }
})
CSV()
```

#### BRIDGE-SQLITE에서 실행

```js
SCRIPT({
    for( i = 0; i < 3; i++) {
        ts = Date.now(); // ms
        $.yield("testing", ts, Math.random()*100);
    }
})
SCRIPT({
    // This section contains initialization code
    // that runs once before processing the first record.
    err = $.db({bridge:"mem"}).exec("CREATE TABLE IF NOT EXISTS example ("+
        "NAME TEXT,"+
        "TIME INTEGER,"+
        "VALUE REAL"+
    ")");
    if (err instanceof Error) {
        console.error("Fail to create table", err.message);
    }
}, {
    // This section contains the main code
    // that runs over every record.
    err = $.db({bridge:"mem"}).exec("INSERT INTO example values(?, ?, ?)", 
        $.values[0], $.values[1], $.values[2]);
    if (err instanceof Error) {
        console.error("Fail to insert", err.message);
    } else {
        $.yield($.values[0], $.values[1], $.values[2]);
    }
})
CSV()
```

SQL 에디터에서 브리지 데이터베이스를 조회하려면 쿼리에 `-- env: bridge=name` 표기를 사용하세요.

```sql
-- env: bridge=mem
SELECT
    name,
    datetime(time/1000, 'unixepoch', 'localtime') as time,
    value
FROM
    example;
-- env: reset
```

### $.request().do()

**문법**: `$.request(url [, option]).do(callback)`

**요청 옵션:**

```js
{
    method: "GET|POST|PUT|DELETE", // default is "GET"
    headers: { "Authorization": "Bearer auth-token"}, // key value map
    body: "body content if the method is POST or PUT"
}
```

실제 요청은 응답을 처리할 콜백 함수와 함께 `.then()`이 호출될 때 이루어집니다. 콜백 함수는 여러 속성과 메서드를 제공하는 Response 객체를 인자로 받습니다.

**Response 속성:**

| 속성 | 타입 | 설명 |
|:---------|:----:|:------------|
| `.ok` | Boolean | 응답 상태 코드가 성공이면 `true` (`200<= status < 300`) |
| `.status` | Number | HTTP 응답 코드 |
| `.statusText` | String | 상태 코드와 메시지. 예: `200 OK` |
| `.url` | String | 요청 URL |
| `.headers` | Map | 응답 헤더 |

**Response 메서드:**

Response 객체는 응답 본문을 다루는 유용한 메서드를 제공합니다.

| 메서드 | 설명 |
|:-------|:------------|
| `.text(callback(txt))` | 내용을 문자열로 콜백에 전달 |
| `.blob(callback(bin))` | 내용을 바이너리 배열로 콜백에 전달 |
| `.csv(callback(row))` | 내용을 CSV로 파싱해 행(레코드)마다 `callback()` 호출 |

**Usage:**

```js
$.request("https://server/path", {
    method: "GET",
    headers: { "Authorization": "Bearer auth-token" }
  }).do( function(rsp){
    console.log("ok:", rsp.ok);
    console.log("status:", rsp.status);
    console.log("statusText:", rsp.statusText);
    console.log("url:", rsp.url);
    console.log("Content-Type:", rsp.headers["Content-Type"]);
});
```

### finalize()

`SCRIPT()` 안의 JavaScript 코드가 `function finalize() {}`를 정의하면, 모든 레코드 처리가 끝난 뒤 시스템이 이 함수를 자동으로 호출합니다.

다음 두 코드 예제는 동일하며, 둘 다 마지막 레코드로 `999`를 내보냅니다.

**finalize() 함수 사용:**

```js
FAKE( arrange(1, 3, 1) )
SCRIPT({
    function finalize() {
        $.yield(999);
    }
    $.yield($.values[0]);
})
CSV()
```

**deinit 코드 사용:**

```js
FAKE( arrange(1, 3, 1) )
SCRIPT({
    // init; do nothing
},{
    // main
    $.yield($.values[0]);
}, {
    // deinit;
    $.yield(999);
})
CSV()
```

이 예제는 레코드 4개 `1`,`2`,`3`,`999`를 내보냅니다.

## Examples

### Hello World

```js
SCRIPT({
    console.log("Hello World?");
})
DISCARD()
```

### 내장 Math 객체

#### JavaScript 사용

JavaScript 내장 함수를 사용할 수 있습니다:

```js
FAKE(meshgrid(linspace(0,2*3.1415,30), linspace(0, 3.1415, 20)))

SCRIPT({
  x = Math.cos($.values[0]) * Math.sin($.values[1]);
  y = Math.sin($.values[0]) * Math.sin($.values[1]);
  z = Math.cos($.values[1]);
  $.yield([x,y,z]);
})

CHART(
  plugins("gl"),
  size("600px", "600px"),
  chartOption({
    grid3D:{}, xAxis3D:{}, yAxis3D:{}, zAxis3D:{},
    visualMap:[{  min:-1, max:1, 
      inRange:{color:["#313695",  "#74add1", "#ffffbf","#f46d43", "#a50026"]
    }}],
    series:[ { type:"scatter3D", data: column(0)} ]
  })
)
```

#### SET-MAP 함수 사용

JavaScript 대신 SET-MAP 함수로 같은 결과를 얻는 방법입니다:

```js
FAKE(meshgrid(linspace(0,2*3.1415,30), linspace(0, 3.1415, 20)))

SET(x, cos(value(0))*sin(value(1)))
SET(y, sin(value(0))*sin(value(1)))
SET(z, cos(value(1)))

MAPVALUE(0, list($x, $y, $z))
POPVALUE(1)

CHART(
  plugins("gl"),
  size("600px", "600px"),
  chartOption({
    grid3D:{}, xAxis3D:{}, yAxis3D:{}, zAxis3D:{},
    visualMap:[{  min:-1, max:1, 
      inRange:{color:["#313695",  "#74add1", "#ffffbf","#f46d43", "#a50026"]
    }}],
    series:[ { type:"scatter3D", data: column(0)} ]
  })
)
```

### JSON Parser

```js
SCRIPT({
    $.result = {
        columns: ["NAME", "AGE", "IS_MEMBER", "HOBBY"],
        types: ["string", "int32", "bool", "string"],
    }
},{
    content = $.payload;
    if (content === undefined) {
        content = '{"name":"James", "age": 24, "isMember": true, "hobby": ["book", "game"]}';
    }
    obj = JSON.parse(content);
    $.yield(obj.name, obj.age, obj.isMember, obj.hobby.join(","));
})
JSON()
```

**Output:**

```json
{
    "data": {
        "columns": [ "NAME", "AGE", "IS_MEMBER", "HOBBY" ],
        "types": [ "string", "int32", "bool", "string" ],
        "rows": [ [ "James", 24, true, "book,game" ] ]
    },
    "success": true,
    "reason": "success",
    "elapse": "627.958µs"
}
```

### Request CSV

```js
SCRIPT({
    $.result = {
        columns: ["SepalLen", "SepalWidth", "PetalLen", "PetalWidth", "Species"],
        types: ["double", "double", "double", "double", "string"]
    };
},{
    $.request("https://docs.machbase.com/assets/example/iris.csv")
     .do(function(rsp){
        console.log("ok:", rsp.ok);
        console.log("status:", rsp.status);
        console.log("statusText:", rsp.statusText);
        console.log("url:", rsp.url);
        console.log("Content-Type:", rsp.headers["Content-Type"]);
        if ( rsp.error() !== undefined) {
            console.error(rsp.error())
        }
        var err = rsp.csv(function(fields){
            $.yield(fields[0], fields[1], fields[2], fields[3], fields[4]);
        })
        if (err !== undefined) {
            console.warn(err);
        }
    })
})
CSV(header(true))
```

### JSON 텍스트 요청

이 예제는 원격 서버에서 JSON 내용을 가져와 JavaScript로 파싱하는 방법을 보여줍니다.

```js
SCRIPT({
    $.result = {
        columns: ["ID", "USER_ID", "TITLE", "COMPLETED"],
        types: ["int64", "int64", "string", "boolean"]
    };
},{
    $.request("https://jsonplaceholder.typicode.com/todos")
     .do(function(rsp){
        console.log("ok:", rsp.ok);
        console.log("status:", rsp.status);
        console.log("statusText:", rsp.statusText);
        console.log("URL:", rsp.url);
        console.log("Content-Type:", rsp.headers["Content-Type"]);
        if ( rsp.error() !== undefined) {
            console.error(rsp.error())
        }
        rsp.text( function(txt){
            list = JSON.parse(txt);
            for (i = 0; i < list.length; i++) {
                obj = list[i];
                $.yield(obj.id, obj.userId, obj.title, obj.completed);
            }
        })
    })
})
CSV(header(false))
```
