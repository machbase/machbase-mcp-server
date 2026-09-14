# Machbase Neo TQL Sink Functions

모든 TQL 스크립트는 SINK 함수 중 하나로 끝나야 합니다.

가장 기본적인 SINK 함수는 들어온 레코드를 machbase-neo 데이터베이스에 쓰는 `INSERT()`입니다. `CHART()` 함수는 들어온 레코드로 다양한 차트를 그립니다. `JSON()`과 `CSV()`는 들어온 데이터를 각 형식으로 인코딩합니다.

## INSERT()

**문법**: `INSERT( [bridge(),] columns..., table() [, tag()] )`

`INSERT()`는 레코드마다 'INSERT' 문을 실행해 지정한 데이터베이스 테이블에 저장합니다.

**Parameters:**
- `bridge()` - bridge('name'), 선택
- `columns` - 문자열, 컬럼 목록
- `table()` - table('name'), 대상 테이블 이름 지정
- `tag()` - tag('name'), 선택, 태그 테이블에만 적용

### 예제: 기본 INSERT

태그 이름이 포함된 레코드를 machbase에 씁니다.

```js
FAKE(json({
    ["temperature", 1708582790, 23.45],
    ["temperature", 1708582791, 24.56]
}))
MAPVALUE(1, value(1)*1000000000) // convert epoch sec to nanosec
INSERT("name", "time", "value", table("example"))
```

### 예제: PUSHVALUE() 사용

`PUSHVALUE()`로 "name" 필드를 추가해 동일한 태그 이름으로 machbase에 씁니다.

```js
FAKE(json({
    [1708582792, 32.34],
    [1708582793, 33.45]
}))
PUSHVALUE(0, "temperature")
MAPVALUE(1, value(1)*1000000000) // convert epoch sec to nanosec
INSERT("name","time", "value", table("example"))
```

### 예제: tag() 사용

대상이 태그 테이블이면 `tag()` 옵션으로 동일한 태그 이름을 지정해 machbase에 씁니다.

```js
FAKE(json({
    [1708582792, 32.34],
    [1708582793, 33.45]
}))
MAPVALUE(0, value(0)*1000000000) // convert epoch sec to nanosec
INSERT("time", "value", table("example"), tag('temperature'))
```

### 예제: 브리지 데이터베이스

브리지로 연결된 데이터베이스에 레코드를 삽입합니다.

```js
INSERT(
    bridge("sqlite"),
    "company", "employee", "created_on", table("mem_example")
)
```

## APPEND()

**문법**: `APPEND( table() )`

`APPEND()`는 machbase-neo의 'append' 방식으로 들어온 레코드를 지정한 테이블에 저장합니다.

**Parameters:**
- `table()` - table(string), 대상 테이블 지정

```js
FAKE(json({
    ["temperature", 1708582794, 12.34],
    ["temperature", 1708582795, 13.45]
}))
MAPVALUE(1, value(1)*1000000000 ) // convert epoch sec to nanosec
APPEND( table("example") )
```

## binaryformat (v8.5.2부터)

`binaryformat()` 옵션은 이진 컬럼 데이터를 텍스트 출력에서 어떻게 표현할지 제어합니다. CSV(), JSON(), NDJSON(), BOX() SINK에 적용됩니다.

지원하는 값:
- `hex` (기본값): 16진수 인코딩
- `base64`: Base64 인코딩
- `bytes`: 원시 바이트 표현
- `preview`: 미리보기(잘린) 표시

## CSV()

**문법**: `CSV( [tz(), timeformat(), precision(), rownum(), heading(), delimiter(), nullValue() ] )`

결과 레코드를 CSV 형식으로 만듭니다. 레코드의 값들이 CSV 줄의 필드가 됩니다. 데이터의 끝은 연속된 개행 문자 두 개(`\n\n`)로 식별합니다.

예를 들어 레코드가 `{key: k, value:[v1,v2]}`이면 `v1,v2` 형태의 CSV 레코드가 생성됩니다.

**Parameters:**
- `tz` - tz(name), 시간대, 기본값은 `tz('UTC')`
- `timeformat` - timeformat(string), datetime 필드의 표현 형식 지정, 기본값은 `timeformat('ns')`
- `rownum` - rownum(boolean), rownum 컬럼 추가
- `precision` - precision(int), 실수 필드의 정밀도 지정. `precision(-1)`은 제한 없음, `precision(0)`은 정수로 변환
- `heading` - heading(boolean), 첫 행에 필드 이름 추가
- `delimiter` - delimiter(string), 기본 쉼표(`,`) 대신 사용할 필드 구분자 지정
- `nullValue()` - NULL 값을 대체할 문자열 지정, 기본값은 `nullValue('NULL')` (버전 8.0.14 이상)
- `substituteNull` - substitute(string), NULL 값을 대체할 문자열 지정, 기본값은 `substituteNull('NULL')` (폐기됨, `nullValue()`로 대체)
- `cache()` - 결과 데이터를 캐시합니다. 자세한 내용은 결과 데이터 캐시 항목 참고 (버전 8.0.43 이상)

### 예제: 기본 출력

```js
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10)
CSV()
```

**Output:**

```csv
1,10
2,20
3,30
```

### 예제: heading() 사용

```js
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
CSV( heading(true) )
```

**Output:**

```csv
x,x10
1,10
2,20
3,30
```

### 예제: delimiter() 사용

```js
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
CSV( heading(true), delimiter("|") )
```

**Output:**

```csv
x|x10
1|10
2|20
3|30
```

### 예제: nullValue() 사용

```js
FAKE( json({ ["A", 123], ["B", null], ["C", 234] }) )
CSV( nullValue("***") )
```

**Output:**

```csv
A|123
B|***
C|234
```

## JSON()

**문법**: `JSON( [transpose(), tz(), timeformat(), precision(), rownum(), rowsFlatten(), rowsArray() ] )`

레코드의 값으로 JSON 결과를 생성합니다.

**Parameters:**
- `transpose` - transpose(boolean), 행과 열을 전치합니다. 대부분의 차트 라이브러리에서는 `transpose(true)` 지정이 유용합니다
- `tz` - tz(name), 시간대, 기본값은 `tz('UTC')`
- `timeformat` - timeformat(string), datetime 필드의 표현 형식 지정, 기본값은 `timeformat('ns')`
- `rownum` - rownum(boolean), rownum 컬럼 추가
- `precision` - precision(int), 실수 필드의 정밀도 지정. `precision(-1)`은 제한 없음, `precision(0)`은 정수로 변환
- `rowsFlatten` - rowsFlatten(boolean), JSON 객체의 rows 필드 배열 차원을 낮춥니다. `JSON()`에 `transpose(true)`와 `rowsFlatten(true)`이 함께 있으면 `rowsFlatten(true)`은 무시되고 `transpose(true)`만 적용됩니다 (버전 8.0.12 이상)
- `rowsArray` - rowsArray(boolean), 레코드마다 객체 배열만 담은 JSON을 생성합니다. `rowsArray(true)`가 `transpose(true)`·`rowsFlatten(true)`보다 우선합니다 (버전 8.0.12 이상)
- `cache()` - 결과 데이터를 캐시합니다. 자세한 내용은 결과 데이터 캐시 항목 참고 (버전 8.0.43 이상)

### 예제: 기본 출력

```js
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10)
JSON()
```

**Output:**

```json
{
    "data": {
        "columns": [ "x" ],
        "types": [ "double" ],
        "rows": [ [ 1, 10 ], [ 2, 20 ], [ 3, 30 ] ]
    },
    "success": true,
    "reason": "success",
    "elapse": "228.541µs"
}
```

### 예제: transpose() 사용

```js
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
JSON( transpose(true) )
```

**Output:**

```json
{
    "data": {
        "columns": [ "x", "x10" ],
        "types": [ "double", "double" ],
        "cols": [ [ 1, 2, 3 ], [ 20, 30, 40 ] ]
    },
    "success": true,
    "reason": "success",
    "elapse": "121.375µs"
}
```

### 예제: rowsFlatten() 사용

```js
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
JSON( rowsFlatten(true) )
```

**Output:**

```json
{
    "data": {
        "columns": [ "x", "x10" ],
        "types": [ "double", "double" ],
        "rows": [ 1, 10, 2, 20, 3, 30 ]
    },
    "success": true,
    "reason": "success",
    "elapse": "130.916µs"
}
```

### 예제: rowsArray() 사용

```js
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
JSON( rowsArray(true) )
```

**Output:**

```json
{
    "data": {
        "columns": [ "x", "x10" ],
        "types": [ "double", "double" ],
        "rows": [ { "x": 1, "x10": 10 }, { "x": 2, "x10": 20 }, { "x": 3, "x10": 30 } ]
    },
    "success": true,
    "reason": "success",
    "elapse": "549.833µs"
}
```

## NDJSON()

**문법**: `NDJSON( [tz(), timeformat(), rownum()] )`

*버전 8.0.33 이상*

레코드의 값으로 NDJSON 결과를 생성합니다.

NDJSON(Newline Delimited JSON)은 각 줄이 하나의 유효한 JSON 객체인 스트리밍 JSON 형식입니다. 한 번에 JSON 객체 하나씩 처리할 수 있어 대용량 데이터셋이나 스트리밍 데이터를 다룰 때 유용합니다. 데이터의 끝은 연속된 개행 문자 두 개(`\n\n`)로 식별합니다.

**Parameters:**
- `tz` - tz(name), 시간대, 기본값은 `tz('UTC')`
- `timeformat` - timeformat(string), datetime 필드의 표현 형식 지정, 기본값은 `timeformat('ns')`
- `rownum` - rownum(boolean), rownum 컬럼 추가
- `cache()` - 결과 데이터를 캐시합니다. 자세한 내용은 결과 데이터 캐시 항목 참고 (버전 8.0.43 이상)

**Example:**

```js
SQL(`select * from example where name = 'neo_load1' limit 3`)
NDJSON(timeformat('Default'), tz('local'), rownum(true))
```

**Output:**

```json
{"NAME":"neo_load1","ROWNUM":1,"TIME":"2024-09-06 14:46:19.852","VALUE":4.58}
{"NAME":"neo_load1","ROWNUM":2,"TIME":"2024-09-06 14:46:22.853","VALUE":4.69}
{"NAME":"neo_load1","ROWNUM":3,"TIME":"2024-09-06 14:46:25.852","VALUE":4.69}

```

## MARKDOWN()

마크다운 형식 또는 HTML 표를 생성합니다.

**문법**: `MARKDOWN( [ options... ] )`

**Parameters:**
- `tz(string)` - 시간대, 기본값은 `tz('UTC')`
- `timeformat(string)` - datetime 필드의 표현 형식 지정, 기본값은 `timeformat('ns')`
- `html(boolean)` - HTML 렌더러로 결과를 생성, 기본값 `false`
- `rownum(boolean)` - rownum 컬럼 표시
- `precision` - precision(int), 실수 필드의 정밀도 지정. `precision(-1)`은 제한 없음, `precision(0)`은 정수로 변환
- `brief(boolean)` - 결과 행을 생략합니다. `brief(true)`는 `briefCount(5)`와 같습니다
- `briefCount(limit int)` - 레코드가 주어진 한도를 넘으면 결과 행을 생략합니다. 한도가 `0`이면 생략하지 않습니다

### 예제: 기본 출력

```js
FAKE( csv(`
10,The first line 
20,2nd line
30,Third line
40,4th line
50,The last is 5th
`))
MARKDOWN()
```

**Output:**

```
|column0 |	column1 |
|:-------|:---------|
| 10     | The first line |
| 20     | 2nd line |
| 30     | Third line |
| 40     | 4th line |
| 50     | The last is 5th |
```

### 예제: briefCount 사용

```js
FAKE( csv(`
10,The first line 
20,2nd line
30,Third line
40,4th line
50,The last is 5th
`))
MARKDOWN( briefCount(2) )
```

**Output:**

```
|column0 |	column1 |
|:-------|:---------|
| 10     | The first line |
| 20     | 2nd line |
| ...    | ...      |

> 전체 5건
```

### 예제: html() 사용

```js
FAKE( csv(`
10,The first line 
20,2nd line
30,Third line
40,4th line
50,The last is 5th
`))
MARKDOWN( briefCount(2), html(true) )
```

**Output:**

|column0 |	column1 |
|:-------|:---------|
| 10     | The first line |
| 20     | 2nd line |
| ...    | ...      |

> 전체 5건

## HTML()

**문법**: `HTML(templates...)`

*버전 8.0.52 이상*

제공된 템플릿으로 HTML 문서를 생성합니다.

자세한 사용법과 예제는 HTML 항목을 참고하세요.

## TEXT()

**문법**: `TEXT(templates...)`

*버전 8.0.52 이상*

제공된 템플릿으로 텍스트 문서를 생성합니다.

`HTML()`과 비슷하게 동작하지만 데이터에 HTML 이스케이프를 적용하지 않습니다.

## DISCARD()

**문법**: `DISCARD()`

*버전 8.0.7 이상*

`DISCARD()`는 이름 그대로 모든 레코드를 조용히 버리며 아무 출력도 생성하지 않습니다.

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

## CHART()

**문법**: `CHART()`

*버전 8.0.8 이상*

Apache ECharts로 차트를 생성합니다.

다양한 사용법은 CHART() 예제를 참고하세요.

### 예제: CHART() 사용

```js
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--> time   value
// |
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis: { name: "T", type:"time" },
        yAxis: { name: "V"},
        legend: { show: true },
        tooltip: { show: true, trigger: "axis" },
        series: [{ 
            type: "line",
            name: "column[1]",
            data: column(0).map(function(t, idx){
                return [t, column(1)[idx]];
            })
        }]
    })
)
```

```js
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--> time   value
// |
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis: { name: "T", type:"time" },
        yAxis: { name: "V"},
        legend: { show: true },
        tooltip: { show: true, trigger: "axis" },
        series: [{ 
            type: "bar",
            name: "column[1]",
            data: column(0).map(function(t, idx){
                return [t, column(1)[idx]];
            })
        }]
    })
)
```

```js
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--> time   value
// |
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis: { name: "T", type:"time" },
        yAxis: { name: "V"},
        legend: { show: true },
        tooltip: { show: true, trigger: "axis" },
        series: [{ 
            type: "scatter",
            name: "column[1]",
            data: column(0).map(function(t, idx){
                return [t, column(1)[idx]];
            })
        }]
    })
)
```

```js
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--> x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--> x   y   z
// |
CHART(
  plugins("gl"),
  size('600px', '600px'),
  chartOption({
    grid3D:{ boxWidth: 100, boxHeight: 30, boxDepth: 100},
    xAxis3D:{name:"x"},
    yAxis3D:{name:"y"},
    zAxis3D:{name:"z"},
    series:[{
        type: "line3D",
        lineStyle: { "width": 2 },
        data: column(0).map(function(x, idx){
            return [x, column(1)[idx], column(2)[idx]]
        })
    }],
    visualMap: {
        min: -0.12, max:0.12,
        inRange: {
            color:["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf",
		    "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"]
        }
    }
  })
)
```

```js
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--> x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--> x   y   z
// |
CHART(
  plugins("gl"),
  size('600px', '600px'),
  chartOption({
    grid3D:{ boxWidth: 100, boxHeight: 30, boxDepth: 100},
    xAxis3D:{name:"x"},
    yAxis3D:{name:"y"},
    zAxis3D:{name:"z"},
    series:[{
        type: "bar3D",
        data: column(0).map(function(x, idx){
            return [x, column(1)[idx], column(2)[idx]]
        })
    }],
    visualMap: {
        min: -0.12, max:0.12,
        inRange: {
            color:["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf",
		    "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"]
        }
    }
  })
)
```

```js
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--> x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--> x   y   z
// |
CHART(
  plugins("gl"),
  size('600px', '600px'),
  chartOption({
    grid3D:{ boxWidth: 100, boxHeight: 30, boxDepth: 100},
    xAxis3D:{name:"x"},
    yAxis3D:{name:"y"},
    zAxis3D:{name:"z"},
    series:[{
        type: "scatter3D",
        data: column(0).map(function(x, idx){
            return [x, column(1)[idx], column(2)[idx]]
        })
    }],
    visualMap: {
        min: -0.12, max:0.12,
        inRange: {
            color:["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf",
		    "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"]
        }
    }
  })
)
```
