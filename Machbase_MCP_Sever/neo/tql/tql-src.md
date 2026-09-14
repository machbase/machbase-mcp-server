# Machbase Neo TQL Source Functions

모든 TQL 스크립트는 데이터 소스 함수 중 하나로 시작해야 합니다.

여러 SRC 함수가 제공됩니다. 예를 들어 `SQL()`은 주어진 SQL 문으로 machbase-neo 데이터베이스나 외부(브리지) 데이터베이스에 질의해 레코드를 만듭니다. `FAKE()`는 인공 데이터를 생성합니다. `CSV()`는 CSV 데이터를 읽고, `BYTES()`는 파일 시스템이나 클라이언트의 HTTP 요청·MQTT 페이로드에서 임의의 이진 데이터를 읽습니다.

## SQL()

**문법**: `SQL( [bridge(),] sqltext [, params...])`

**Parameters:**
- `bridge()` - bridge('name'), 브리지를 지정하면 해당 브리지에서 SQL 쿼리가 실행됩니다
- `sqltext` - 문자열, 데이터베이스에서 데이터를 가져올 SQL SELECT 문. 여러 줄 SQL은 백틱(`)을 사용하세요.
- `params` - 쿼리의 바인드 인자로 쓰이는 가변 인자.

### Machbase 조회

```js
SQL (`
    SELECT time, value 
    FROM example 
    WHERE name ='temperature'
    LIMIT 10000
`)
```

### 가변 인자를 사용한 조회

```js
SQL(`SELECT time, value FROM example WHERE name = ? LIMIT ?`,
    param('name') ?? 'temperature',
    param('limit') ?? 10)
```

### 브리지 데이터베이스 조회

```js
SQL( bridge('sqlite'), `SELECT * FROM EXAMPLE`)
```

```js
SQL(
    bridge('sqlite'),
    `SELECT time, value FROM example WHERE name = ?`,
    param('name') ?? "temperature")
```

## SQL_SELECT()

**문법**: `SQL_SELECT( fields..., from(), between() [, limit()] )`

*버전 8.0.15 이상*

**Parameters:**
- `fields` - 문자열, 컬럼 이름. 여러 컬럼을 지정할 수 있습니다.

`SQL_SELECT()` 소스 함수는 `SQL()`과 같은 기능을 제공하지만, 원시 SQL 문 대신 표준화된 옵션 함수로 사용법을 단순화합니다.

이 함수는 실제로 `SQL()`과 동일하게 동작하지만, 전체 SQL 문 대신 단순화된 옵션으로 조회 조건을 받습니다. SQL의 `WHERE` 조건보다 쉽게 시간 범위 조건을 지정할 수 있습니다.

아래 예제는 `SELECT time, value FROM example WHERE NAME = 'temperature' AND time BETWEEN...` 쿼리로 데이터를 처리합니다.

```js
SQL_SELECT(
    'time', 'value',
    from('example', 'temperature'),
    between('last-10s', 'last')
)
```

아래 `SQL()` 문과 동일합니다

```js
SQL(`SELECT
        time, value
    FROM
        EXAMPLE
    WHERE
        name = 'TAG1'
    AND time BETWEEN (
        SELECT MAX_TIME-10000000000
        FROM V$EXAMPLE_STAT
        WHERE name = 'temperature')
    AND (
        SELECT MAX_TIME
        FROM V$EXAMPLE_STAT
        WHERE name = 'temperature')
    LIMIT 0, 1000000
`)
```

### from()

**문법**: `from( table, tag [, time_column [, name_column] ] )`

`SQL_SELECT()` 함수에 테이블 이름과 태그 이름을 전달해 내부적으로 SQL을 생성합니다. `... FROM <table> WHERE NAME = <tag> ...`와 동일합니다.

**Parameters:**
- `table` - 문자열, 테이블 이름
- `tag` - 문자열, 태그 이름
- `time_column` - 문자열, "time" 컬럼 이름 지정. 생략하면 기본값은 `'time'`입니다.
- `name_column` - 문자열, "name" 컬럼 이름 지정. 생략하면 기본값은 `'name'`입니다. (버전 8.0.5 이상)

### between()

**문법**: `between( fromTime, toTime [, period] )`

`SQL_SELECT()` 함수에 시간 범위 조건을 전달해 내부적으로 SQL을 생성합니다. `... WHERE ... TIME BETWEEN <fromTime> AND <toTime>...`와 동일합니다.

**Parameters:**
- `fromTime` - 문자열 또는 숫자. 문자열로 'now', 'last' 같은 시간 표현을 쓰거나, 숫자로 나노초 단위 unix epoch 시간을 지정합니다
- `toTime` - 문자열 또는 숫자, 시간 표현
- `period` - 문자열 또는 숫자. 기간 표현을 쓰거나 나노초 단위 숫자를 지정합니다. 논리적으로 양수 기간만 의미가 있습니다.

`fromTime`과 `toTime`은 'now'와 'last'에 시간 차 표현을 붙여 지정할 수 있습니다. 예를 들어 `'now-1h30m'`은 현재로부터 1시간 30분 전을 뜻하고, `'last-30s'`는 `base_time_column`의 가장 최근(=최대) 시각으로부터 30초 전을 뜻합니다.

`period`를 지정하면 집계 SQL 함수와 함께 'GROUP BY' 시간 표현이 생성됩니다. 이 경우 기준 시간 컬럼이 `SQL_SELECT()`의 fields 인자에 포함되어야 합니다.

나노초 unix epoch 대신 문자열 표현으로 `fromTime`, `toTime`을 써야 한다면 `parseTime()`으로 문자열 시간 표현을 시간 값으로 변환하세요. 유틸리티 함수 문서를 참고하세요.

**Example:**

```js
between( parseTime("2023-03-01 14:00:00", "DEFAULT", tz("Local")),
         parseTime("2023-03-01 14:05:00", "DEFAULT", tz("Local")))
```

### limit()

**문법**: `limit( [offset ,] count )`

`SELECT... LIMIT offset, count` 문으로 변환됩니다.

**Parameters:**
- `offset` - 숫자, 생략하면 기본값은 `0`
- `count` - Number

## CSV()

**문법**: `CSV( file(file_path_string) | payload() [, charset()] [,field()...[, header()]] )`

CSV를 읽어 키-값 레코드를 만듭니다. 키는 순번으로 생성되고 CSV의 필드가 레코드의 값이 됩니다. 'file'의 문자열 파라미터는 CSV의 절대 경로여야 합니다. `payload()`를 사용하면 HTTP POST 요청 본문 스트림에서 CSV를 읽습니다. 원격 클라이언트가 HTTP POST로 보낸 데이터를 데이터베이스에 쓰는 API를 만들 때 유용합니다.

**Parameters:**
- `file() | payload()` - 입력 스트림
- `field(idx, type, name)` - 필드 지정
- `header(bool)` - 입력 스트림의 첫 줄이 헤더인지 지정
- `charset(string)` - CSV 데이터가 UTF-8이 아닐 때 문자셋 지정 (버전 8.0.8 이상)
- `logProgress([int])` - `n`행마다 진행 로그를 남깁니다. `n`을 생략하면 기본값은 500,000입니다 (버전 8.0.29 이상)

**Example:**

```js
// Read CSV from HTTP request body.
// ex)
// barn,1677646800,0.03135
// dew_point,1677646800,24.4
// dishwasher,1677646800,3.33e-05
CSV(payload(), 
    field(0, stringType(), 'name'),
    field(1, timeType('s'), 'time'),
    field(2, floatType(), 'value'),
    header(false)
)
APPEND(table('example'))
```

위 예제처럼 `CSV()`와 `APPEND()`를 조합하면 간단하고 유용합니다. 명령행 import 명령보다 5배 느리지만, HTTP 요청 하나로 수천 건 이상을 쓸 때는 `INSERT()` 함수보다 빠릅니다.

`??` 연산자를 사용하면 HTTP POST 요청이 있든 없든 동작하게 만들 수 있습니다.

```js
CSV(payload() ?? file('/absolute/path/to/data.csv'),
    field(0, floatType(), 'freq'),
    field(1, floatType(), 'ampl')
)
CHART_LINE()
```

### file()

**문법**: `file(path)`

주어진 파일을 열어 내용에 대한 입력 스트림을 반환합니다. 경로는 파일의 절대 경로여야 합니다.

**Parameters:**
- `path` - 문자열, 열 파일의 경로 또는 리소스를 가져올 http URL.

`path`가 "http://" 또는 "https://"로 시작하면 해당 http URL의 내용을 가져옵니다(버전 8.0.7 이상). 그렇지 않으면 파일 시스템에서 경로를 찾습니다.

아래 코드는 `file()`로 원격 HTTP API를 호출하는 방법을 보여줍니다. 시연을 위해 machbase-neo 자신을 호출하며, SQL 쿼리는 `escapeParam()`으로 안전하게 URL 이스케이프됩니다.

```js
CSV( file(`http://127.0.0.1:5654/db/query?`+
        `format=csv&`+
        `q=`+escapeParam(`select * from example limit 10`)
))
CSV() // or JSON()
```

### payload()

**문법**: `payload()`

TQL 스크립트가 HTTP POST 또는 MQTT PUBLISH로 호출된 경우 요청 내용의 입력 스트림을 반환합니다.

### field()

**문법**: `field(idx, typefunc, name)`

입력 CSV 데이터의 필드 타입을 지정합니다.

**Parameters:**
- `idx` - 숫자, 필드의 0부터 시작하는 인덱스.
- `typefunc` - 필드의 타입 지정 (아래 참고)
- `name` - 문자열, 필드의 이름 지정.

**타입 함수:**

| 타입 함수 | 타입 |
|:--------------|:-----|
| `stringType()` | string |
| `doubleType()` | double |
| `datetimeType()` | datetime |
| `boolType()` | boolean (버전 8.0.20 이상) |
| ~~`floatType()`~~ | *폐기됨, `doubleType()` 사용* (버전 8.0.20 이상) |
| ~~`timeType()`~~ | *폐기됨, `datetimeType()` 사용* (버전 8.0.20 이상) |

`stringType()`, `boolType()`, `floatType()`은 인자를 받지 않으며, `timeType()` 함수는 날짜·시간 데이터를 올바르게 변환하기 위해 하나 또는 두 개의 파라미터를 받습니다.

필드의 입력 데이터가 unix epoch 시간이라면 `ns`, `us`, `ms`, `s` 중 하나의 시간 단위를 지정하세요.
- `datetimeType('s')`
- `datetimeType('ms')`
- `datetimeType('us')`
- `datetimeType('ns')`

입력 필드가 사람이 읽는 형식으로 시간을 표현한다면, 시간대를 포함해 어떻게 파싱할지 지정해야 합니다.

#### DEFAULT 형식 사용

```js
CSV(payload() ??
`name,2006-01-02 15:04:05.999,10`,
field(1, datetimeType('DEFAULT', 'Local'), 'time'))
CSV()
```

#### RFC3339 형식 사용

```js
CSV(payload() ??
`name,2006-01-02T15:04:05.999Z,10`,
field(1, datetimeType('RFC3339', 'EST'), 'time'))
CSV()
```

시간대를 생략하면 기본적으로 'UTC'로 간주합니다.

`timeType()`의 첫 번째 인자는 입력 데이터를 어떻게 파싱할지 지정하며, `timeformat()` 함수와 같은 문법을 사용합니다. 시간 형식 사양은 `timeformat()` 함수 설명을 참고하세요.

### charset()

**문법**: `charset(name)`

*버전 8.0.8 이상*

**Parameters:**
- `name` - 문자열, 문자셋 이름

**지원하는 문자셋:**

UTF-8, ISO-2022-JP, EUC-KR, SJIS , CP932, SHIFT_JIS, EUC-JP, UTF-16, UTF-16BE, UTF-16LE,
CP437, CP850, CP852, CP855, CP858, CP860, CP862, CP863, CP865, CP866, LATIN-1,
ISO-8859-1, ISO-8859-2, ISO-8859-3, ISO-8859-4, ISO-8859-5, ISO-8859-6, ISO-8859-7, 
ISO-8859-8, ISO-8859-10, ISO-8859-13, ISO-8859-14, ISO-8859-15, ISO-8859-16,
KOI8R, KOI8U, MACINTOSH, MACINTOSHCYRILLIC, WINDOWS1250, WINDOWS1251, WINDOWS1252,
WINDOWS1253, WINDOWS1254, WINDOWS1255, WINDOWS1256, WINDOWS1257, WINDOWS1258, WINDOWS874,
XUSERDEFINED, HZ-GB2312

## SCRIPT()

사용자 정의 스크립트 언어를 지원합니다.

자세한 내용과 예제는 SCRIPT 항목을 참고하세요.

## HTTP()

간단한 DSL로 HTTP 요청을 보냅니다.

자세한 내용과 예제는 HTTP 항목을 참고하세요.

## BYTES(), STRING()

**문법**: `BYTES( src [, separator(char), trimspace(boolean) ] )`

**문법**: `STRING( src [, separator(char), trimspace(boolean) ] )`

**Parameters:**
- `src` - 데이터 소스. `payload()`, `file()`, 상수 텍스트 `string` 중 하나입니다.
- `separator(char)` - 선택. `separator("\n")`을 지정하면 한 줄씩 읽고, 생략하면 전체 문자열을 한 번에 읽습니다.
- `trimspace(boolean)` - 선택, 공백 제거 여부. 기본값은 `false`

입력 내용을 구분자로 나눠, 나뉜 부분 내용을 값으로 갖는 레코드를 만듭니다. 키는 레코드의 증가 번호입니다.

**Examples:**
- `STRING('A,B,C', separator(","))`은 레코드 3개 `["A"]`, `["B"]`, `["C"]`를 만듭니다.
- `STRING('A,B,C')`는 레코드 1개 `["A,B,C"]`를 만듭니다.

`BYTES()`와 `STRING()`은 만들어내는 값의 타입만 다르고 동작은 완전히 같습니다. 이름 그대로 `BYTES()`는 '바이트 배열' 값을, `STRING()`은 `string` 값을 만듭니다.

### 예제 1: trimspace 없이

```js
STRING(payload() ?? `12345
                    23456
                    78901`, separator("\n"))
JSON()                    
```
 
위 예제 코드는 레코드 3개 `["12345"]`, `["␣␣␣␣␣␣␣␣␣␣23456"]`, `["␣␣␣␣␣␣␣␣␣␣78901"]`를 만듭니다.

### 예제 2: trimspace 사용

```js
STRING(payload() ?? `12345
                    23456
                    78901`, separator("\n"), trimspace(true))
JSON()                    
```

위 예제 코드는 레코드 3개 `["12345"]`, `["23456"]`, `["78901"]`를 만듭니다.

### 예제 3: HTTP URL

```js
STRING( file(`http://example.com/data/words.txt`), separator("\n") )
JSON()
```

http 주소에서 내용을 가져옵니다. `file()`은 http URL을 지원합니다(버전 8.0.7 이상).

## ARGS()

**문법**: `ARGS()`

*버전 8.0.7 이상*

`ARGS`는 상위 TQL 흐름이 인자로 전달한 값들로 레코드를 만듭니다. `WHEN...do()` 문 안의 하위 흐름에서 SRC로 사용하기 위한 것입니다.

```js
FAKE( json({
    [ 1, "hello" ],
    [ 2, "world" ]
}))
WHEN( value(0) == 2, do( value(0), strToUpper(value(1)), {
    ARGS()
    WHEN( true, doLog("OUTPUT:", value(0), value(1)) )
    DISCARD()
}))
CSV()
```

이 코드는 출력 콘솔에 로그 메시지를 출력합니다.

```
OUTPUT: 2 WORLD
```

## FAKE()

**문법**: `FAKE( generator )`

**Parameters:**
- `generator` - One of the `oscillator()`, `meshgrid()`, `linspace()`, `arrange()`, `csv()`, `json()`

주어진 생성기로 "가짜" 데이터를 만듭니다.

### oscillator()

**문법**: `oscillator( freq() [, freq()...], range() )`

주어진 주파수와 시간 범위로 파형 데이터를 생성합니다. `freq()` 인자를 여러 개 주면 파형이 합성됩니다.

#### Clean Wave

```js
FAKE( oscillator( freq(3, 1.0), range("now-3s", "3s", "5ms") ))
// | 0        1
// | time     amplitude
MAPVALUE(0, list(value(0), value(1)))
// | 0                  1
// | (time, amplitude)  amplitude
POPVALUE(1)
// | 0
// | (time, amplitude)
CHART(
    chartOption({
        xAxis: { type: "time" },
        yAxis: {},
        series:[ { type: "line", data: column(0) } ]
    })
)
```

#### 노이즈가 있는 파형

```js
FAKE( oscillator( freq(3, 1.0), range("now-3s", "3s", "5ms") ))
// | 0        1
// | time     amplitude
MAPVALUE(1, value(1) + (random()-0.5) * 0.2 )
// | 0        1
// | time     amplitude
MAPVALUE(0, list(value(0), value(1)))
// | 0                  1
// | (time, amplitude)  amplitude
POPVALUE(1)
// | 0
// | (time, amplitude)
CHART(
    chartOption({
        xAxis: { type: "time" },
        yAxis: {},
        series:[ { type: "line", data: column(0) } ]
    })
)
```

#### freq()

**문법**: `freq( frequency, amplitude [, bias, phase])`

`amplitude * SIN( 2*Pi * frequency * time + phase) + bias` 식으로 시간에 따른 사인파를 만듭니다.

**Parameters:**
- `frequency` - 숫자, 헤르츠(Hz) 단위 주파수
- `amplitude` - Number
- `bias` - Number
- `phase` - 숫자, 라디안 단위

#### range()

**문법**: `range( fromTime, duration, period )`

`fromTime`부터 `fromTime+duration`까지의 시간 범위를 지정합니다.

**Parameters:**
- `fromTime` - 문자열 또는 숫자. 문자열로는 'now'와 'last'를 쓸 수 있고, 숫자로는 나노초 단위 unix epoch 시간을 지정합니다
- `duration` - 문자열 또는 숫자. 기간 표현을 쓰거나 나노초 단위 숫자를 지정합니다. 예) `'-1d2h30m'`, `'1s100ms'`
- `period` - 문자열 또는 숫자. 기간 표현을 쓰거나 나노초 단위 숫자를 지정합니다. 논리적으로 양수 기간만 의미가 있습니다.

### arrange()

**문법**: `arrange(start, stop, step)`

*버전 8.0.12 이상*

**Parameters:**
- `start` - Number
- `stop` - Number
- `step` - Number

**Example:**

```js
FAKE(
   arrange(1, 2, 0.5)
)
CSV()
```

**Output:**

```csv
1
1.5
2
```

### linspace()

**문법**: `linspace(start, stop, num)`

1차원 선형 공간을 생성합니다.

#### CSV Output

```js
FAKE(
   linspace(1, 3, 3)
)
CSV()
```

**Output:**

```csv
1
2
3
```

#### CHART 출력

```js
FAKE( linspace(0,4*PI,100) )
MAPVALUE(1, sin(value(0)))
MAPVALUE(2, cos(value(0)))
CHART(
  theme("dark"),
  size("600px", "340px"),
  chartOption({
    title: {text: "sin-cos"},
    xAxis:{ data: column(0) },
    yAxis:{},
    series: [
      { name:"SIN", type: "line", data: column(1), 
          markLine:{ data: [{yAxis: 0.5}], label:{show: true, formatter: "half {c} "} } },
      { name:"COS", type: "line", data: column(2) },
    ]
  })
)
```

### meshgrid()

**문법**: `meshgrid(xseries, yseries)`

격자 값 [xseries, yseries]를 생성합니다.

#### CSV Output

```js
FAKE(
    meshgrid( linspace(1, 3, 3), linspace(10, 30, 3) )
)
CSV()
```

**Output:**

```csv
1,10
1,20
1,30
2,10
2,20
2,30
3,10
3,20
3,30
```

#### CHART 출력

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
    grid3D:{},
    xAxis3D:{}, yAxis3D:{}, zAxis3D:{},
    visualMap:[{ 
      min:-1, max:1, 
      inRange:{color:["#313695",  "#74add1", "#ffffbf","#f46d43", "#a50026"]
    }}],
    series:[
      { type:"scatter3D", data: column(0)}
    ]
  })
)
```

### csv()

**문법**: `csv(content)`

*버전 8.0.7 이상*

**Parameters:**
- `content` - 문자열, CSV 내용

주어진 CSV 내용으로 레코드를 만듭니다.

**Example:**

```js
FAKE(
    csv( strTrimSpace(`
        A,1,true
        B,2,false
        C,3,true
    `))
)
MAPVALUE(0, strTrimSpace(value(0)))
MAPVALUE(1, parseFloat(value(1))*10)
MAPVALUE(2, parseBool(value(2)))
CSV()
```

**Output:**

```csv
A,10,true
B,20,false
C,30,true
```

### json()

**문법**: `json({...})`

*버전 8.0.7 이상*

주어진 여러 JSON 배열로 레코드를 만듭니다.

**Example:**

```js
FAKE(
    json({
        ["A", 1, true],
        ["B", 2, false],
        ["C", 3, true]
    })
)
MAPVALUE(1, value(1)*10)
CSV()
```

**Output:**

```csv
A,10,true
B,20,false
C,30,true
```
