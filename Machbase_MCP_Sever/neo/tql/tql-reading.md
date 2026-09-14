# Machbase Neo TQL Reading API

> **참고**: 예제를 실행하려면 아래 SQL로 테이블을 만들고 데이터를 넣으세요.

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
VALUE DOUBLE SUMMARIZED);

INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-12'), 10);
INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-13'), 11);
```

TQL 스크립트를 저장하면 에디터 우측 상단에 링크 아이콘이 표시됩니다. 클릭하면 스크립트 파일의 주소가 복사됩니다.

## CSV

### 기본 CSV 출력

아래 코드를 `output-csv.tql`로 저장합니다.

```js
SQL( `select * from example limit 2` )
CSV()
```

*curl* 명령으로 tql 파일을 호출합니다.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-csv.tql
```

**출력:**

```csv
TAG0,1628694000000000000,10
TAG0,1628780400000000000,11
```

### 구분자를 지정한 CSV

아래 코드를 `output-csv.tql`로 저장합니다.

```js
SQL( `select * from example limit 2` )
CSV( delimiter("|") )
```

*curl* 명령으로 tql 파일을 호출합니다.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-csv.tql
```

**출력:**

```csv
TAG0|1628694000000000000|10
TAG0|1628780400000000000|11
```

## JSON

### 기본 JSON 출력

아래 코드를 `output-json.tql`로 저장합니다.

```js
SQL( `select * from example limit 2` )
JSON()
```

*curl* 명령으로 tql 파일을 호출합니다.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-json.tql
```

**출력:**

```json
{
    "data": {
        "columns": [ "NAME", "TIME", "VALUE" ],
        "types": [ "string", "datetime", "double" ],
        "rows": [
            [ "TAG0", 1628694000000000000, 10 ],
            [ "TAG0", 1628780400000000000, 11 ]
        ]
    },
    "success": true,
    "reason": "success",
    "elapse": "770.078µs"
}
```

### transpose()를 사용한 JSON

아래 코드를 `output-json.tql`로 저장합니다.

```js
SQL( `select * from example limit 2` )
JSON( transpose(true) )
```

*curl* 명령으로 tql 파일을 호출합니다.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-json.tql
```

**출력:**

```json
{
    "data": {
        "columns": [ "NAME", "TIME", "VALUE" ],
        "types": [ "string", "datetime", "double" ],
        "cols": [
            [ "TAG0", "TAG0" ],
            [ 1628694000000000000, 1628780400000000000 ],
            [ 10, 11 ]
        ]
    },
    "success": true,
    "reason": "success",
    "elapse": "718.625µs"
}
```

### rowsFlatten()을 사용한 JSON

아래 코드를 `output-json.tql`로 저장합니다.

```js
SQL( `select * from example limit 2` )
JSON( rowsFlatten(true) )
```

*curl* 명령으로 tql 파일을 호출합니다.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-json.tql
```

**출력:**

```json
{
    "data": {
        "columns": [ "NAME", "TIME", "VALUE" ],
        "types": [ "string", "datetime", "double" ],
        "rows": [
            "TAG0", 1628694000000000000, 10,
            "TAG0", 1628780400000000000, 11
        ]
    },
    "success": true,
    "reason": "success",
    "elapse": "718.625µs"
}
```

### rowsArray()를 사용한 JSON

아래 코드를 `output-json.tql`로 저장합니다.

```js
SQL( `select * from example limit 2` )
JSON( rowsArray(true) )
```

*curl* 명령으로 tql 파일을 호출합니다.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-json.tql
```

**출력:**

```json
{
    "data": {
        "columns": [ "NAME", "TIME", "VALUE" ],
        "types": [ "string", "datetime", "double" ],
        "rows": [
            { "NAME": "TAG0", "TIME": 1628694000000000000, "VALUE": 10 },
            { "NAME": "TAG0", "TIME": 1628780400000000000, "VALUE": 11 }
        ]
    },
    "success": true,
    "reason": "success",
    "elapse": "718.625µs"
}
```

## NDJSON

아래 코드를 `output-ndjson.tql`로 저장합니다.

```js
SQL( `select * from example limit 2` )
NDJSON( )
```

*curl* 명령으로 tql 파일을 호출합니다.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-ndjson.tql
```

**출력:**

```json
{ "NAME": "TAG0", "TIME": 1628694000000000000, "VALUE": 10 }
{ "NAME": "TAG0", "TIME": 1628780400000000000, "VALUE": 11 }
```

## MARKDOWN

### 기본 MARKDOWN 출력

아래 코드를 `output-markdown.tql`로 저장합니다.

```js
SQL( `select * from example limit 2` )
MARKDOWN()
```

*curl* 명령으로 tql 파일을 호출합니다.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-markdown.tql
```

**출력:**

```
|NAME|TIME|VALUE|
|:-----|:-----|:-----|
|TAG0|1628694000000000000|10.000000|
|TAG0|1628780400000000000|11.000000|
```

### html()을 사용한 MARKDOWN

아래 코드를 `output-markdown.tql`로 저장합니다.

```js
SQL( `select * from example limit 2` )
MARKDOWN( html(true) )
```

*curl* 명령으로 tql 파일을 호출합니다.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-markdown.tql
```

**출력:**

```html
<div>
<table>
<thead>
    <tr><th align="left">NAME</th><th align="left">TIME</th><th align="left">VALUE</th></tr>
</thead>
<tbody>
    <tr><td align="left">TAG0</td><td align="left">1628694000000000000</td><td align="left">10.000000</td></tr>
    <tr><td align="left">TAG0</td><td align="left">1628780400000000000</td><td align="left">11.000000</td>
    </tr>
</tbody>
</table>
</div>
```

## HTML

`HTML()` 함수는 제공된 템플릿 언어로 서식을 적용해 HTML 문서를 출력으로 생성합니다.
이를 통해 쿼리 결과를 바탕으로 HTML 출력의 구조와 모양을 자유롭게 구성할 수 있습니다.

템플릿 표현식(컬럼 값을 위한 `{{ .V.column_name }}`, 첫 행을 위한 `{{ if .IsFirst }}`, 마지막 행을 위한 `{{ if .IsLast }}` 등)으로 HTML 생성 방식을 제어할 수 있습니다. 덕분에 TQL 스크립트에서 바로 표, 리포트 등 HTML 기반 표현을 손쉽게 만들 수 있습니다.

```html
SQL(`select name, time, value from example limit 5`)
HTML({
{{ if .IsFirst }}
    <html>
    <body>
        <h2>HTML Template Example</h2>
        <hr>
        <table>
{{ end }}
    <tr>
        <td>{{ .V.name }}</td>
        <td>{{ .V.time }}</td>
        <td>{{ .V.value }}</td>
    </tr>
{{ if .IsLast }}
    </table>
        <hr>
        Total: {{ .Num }}
    </body>
    </html>
{{ end }}
})
```

## CHART

### 기본 CHART 사용법

**TQL 파일 저장**

아래 코드를 `output-chart.tql`로 저장합니다.

```js
SQL(`select time, value from example where name = ? limit 2`, "TAG0")
CHART(
    chartOption({
        xAxis: { data: column(0) },
        yAxis: {},
        series: { type:"bar", data: column(1) }
    })
)
```

**HTTP GET**

웹 브라우저에서 `http://127.0.0.1:5654/db/tql/output-chart.tql`를 엽니다.

> **참고**: 레거시 `CHART_LINE()`, `CHART_BAR()`, `CHART_SCATTER()` 및 관련 함수들은 새로운 `CHART()` 함수로 대체되어 폐기되었습니다. 예제는 CHART()를 참고하세요.

### chartJson()을 사용한 CHART

**TQL 파일 저장**

아래 코드를 `output-chart.tql`로 저장합니다.

```js
SQL(`select time, value from example where name = ? limit 2`, "TAG0")
CHART(
    chartJson(true),
    chartOption({
        xAxis: { data: column(0) },
        yAxis: {},
        series: { type:"bar", data: column(1) }
    })
)
```

**HTTP GET**

웹 브라우저에서 `http://127.0.0.1:5654/db/tql/output-chart.tql`를 엽니다.

**출력:**

```json
{
  "chartID":"MzM3NjYzNjg5MTYxNjQ2MDg_", 
  "jsAssets": ["/web/echarts/echarts.min.js"],
  "jsCodeAssets": ["/web/api/tql-assets/MzM3NjYzNjg5MTYxNjQ2MDg_.js"],
  "style": {
      "width": "600px",
      "height": "600px"	
  },
  "theme": "white"
}
```

### chartID()를 사용한 CHART

**TQL 파일 저장**

아래 코드를 `output-chart.tql`로 저장합니다.

```js
SQL(`select time, value from example where name = ? limit 2`, "TAG0")
CHART(
    chartID("myChart"),
    chartJson(true),
    chartOption({
        xAxis: { data: column(0) },
        yAxis: {},
        series: { type:"bar", data: column(1) }
    })
)
```

**HTTP GET**

웹 브라우저에서 `http://127.0.0.1:5654/db/tql/output-chart.tql`를 엽니다.

**출력:**

```json
{
  "chartID":"myChart", 
  "jsAssets": ["/web/echarts/echarts.min.js"],
  "jsCodeAssets": ["/web/api/tql-assets/myChart.js"],
  "style": {
      "width": "600px",
      "height": "600px"	
  },
  "theme": "white"
}
```

이 방식은 DOM 문서에 `<div id='myChart'/>`가 있을 때 유용합니다.

**HTML 사용 예:**

```html
... in HTML ...
<div id='myChart' />
<script>
    fetch('http://127.0.0.1:5654/db/tql/output-chart.tql').then( function(rsp) {
        return rsp.json();
    }).then( function(c) {
        c.jsAssets.concat(c.jsCodeAssets).forEach((src) => {
            const sScript = document.createElement('script');
            sScript.src = src;
            sScript.type = 'text/javascript';
            document.getElementsByTagName('head')[0].appendChild(sScript);
        })
    })
</script>
... omit ...
```

## 결과 데이터 캐시

*버전 8.0.43 이상*

아래와 같이 `CSV()`, `JSON()`, `NDJSON()`, `HTML()` SINK에 `cache()` 옵션 함수가 추가되었습니다.

```js
SQL( "select * from example limit ?, 1000",  param("offset") ?? 0 )
JSON( cache( param("offset") ?? "0", "60s" ) )
```

`cache()` 옵션은 필수 파라미터 두 개(`CACHE_KEY`, `TTL`)와 선택 파라미터 하나(`r`)를 받습니다.

**문법**: `cache(CACHE_KEY string, TTL string, [r float])`

### 파라미터

1. **CACHE_KEY** (첫 번째): 캐시 데이터를 등록/검색할 때 사용하며 `[파일명] + [소스코드 해시] + [CACHE_KEY]`로 구성됩니다. 따라서 같은 TQL(같은 파일명 + 같은 코드)에서 같은 `CACHE_KEY`로 실행한 결과는 같은 키를 가지며, 나중에 실행된 결과가 기존 캐시 데이터를 덮어씁니다.

2. **TTL** (두 번째): 주어진 기간이 지나면 캐시를 자동으로 삭제합니다. TTL 이후에 들어온 요청은 실제 DB를 조회해 결과를 반환하고, 그 결과가 다시 캐시에 등록됩니다.

3. **r** (세 번째, 선택): "선점형 캐시 갱신 비율"이며 0과 1.0 사이의 값이어야 합니다(0과 1.0 제외). `r * TTL`과 `TTL` 사이에 들어온 첫 요청에 대해서는 현재 캐시 데이터로 응답한 뒤 쿼리를 실행해 캐시를 갱신합니다. 이후 요청들은 갱신된 결과를 캐시에서 받습니다. 이를 통해 자주 요청되는 `CACHE_KEY`의 캐시 데이터가 백그라운드에서 계속 갱신됩니다.

### 캐시 동작

코드가 수정되면 `source_code_hash`가 바뀌어 캐시 미스가 발생합니다. `TTL`이 만료되어 캐시가 자동 삭제된 경우에도 캐시 미스가 발생합니다. 두 경우 모두 요청이 실행되고 결과 데이터가 캐시에 등록됩니다.

위 동작은 SINK 함수에 `cache()` 옵션을 추가했을 때만 적용됩니다. `cache()` 옵션이 없는 TQL은 캐시를 조회하지 않습니다.

> **주의**: 캐시를 과도하게 사용하면 메모리 부족 문제가 생길 수 있습니다. 예를 들어 수십억 건을 SELECT하는 TQL에 cache()를 쓰는 경우...
