---
title: As Reading API
type: docs
weight: 05
---

{{< callout type="info" >}}
For the examples, create a table and insert data with the following SQL statements.
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
VALUE DOUBLE SUMMARIZED);

INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-12'), 10);
INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-13'), 11);
```

When you save a TQL script, the editor will display a link icon <img src="/images/copy_addr_icon.jpg" width="24px" style="display:inline"> in the top right corner. Click on it to copy the address of the script file.

## CSV

{{< tabs items="default,delimiter()" >}}
{{< tab >}}
Save the code below as `output-csv.tql`.

```js {linenos=table,hl_lines=[2]}
SQL( `select * from example limit 2` )
CSV()
```
Invoke the tql file with *curl* command.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-csv.tql
```

```csv
TAG0,1628694000000000000,10
TAG0,1628780400000000000,11
```
{{< /tab >}}
{{< tab >}}
Save the code below as `output-csv.tql`.

```js {linenos=table,hl_lines=[2]}
SQL( `select * from example limit 2` )
CSV( delimiter("|") )
```

Invoke the tql file with *curl* command.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-csv.tql
```

```csv
TAG0|1628694000000000000|10
TAG0|1628780400000000000|11
```
{{< /tab >}}
{{< /tabs >}}

## JSON

{{< tabs items="default,transpose(),rowsFlatten(),rowsArray()" >}}
{{< tab >}}
Save the code below as `output-json.tql`.

```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `select * from example limit 2` )
JSON()
```

Invoke the tql file with *curl* command.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-json.tql
```

```json {hl_lines=["5-8"]}
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
{{< /tab >}}
{{< tab >}}
Save the code below as `output-json.tql`.

```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `select * from example limit 2` )
JSON( transpose(true) )
```

Invoke the tql file with *curl* command.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-json.tql
```

```json {hl_lines=["5-9"]}
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
{{< /tab >}}
{{< tab >}}
Save the code below as `output-json.tql`.

```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `select * from example limit 2` )
JSON( rowsFlatten(true) )
```

Invoke the tql file with *curl* command.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-json.tql
```

```json {hl_lines=["5-8"]}
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
{{< /tab >}}
{{< tab >}}
Save the code below as `output-json.tql`.

```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `select * from example limit 2` )
JSON( rowsArray(true) )
```

Invoke the tql file with *curl* command.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-json.tql
```

```json {hl_lines=["5-8"]}
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
{{< /tab >}}
{{< /tabs >}}

## NDJSON

Save the code below as `output-ndjson.tql`.

```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `select * from example limit 2` )
NDJSON( )
```

Invoke the tql file with *curl* command.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-ndjson.tql
```

```json {hl_lines=["5-8"]}
{ "NAME": "TAG0", "TIME": 1628694000000000000, "VALUE": 10 }↵
{ "NAME": "TAG0", "TIME": 1628780400000000000, "VALUE": 11 }↵
↵
```

## MARKDOWN

{{< tabs items="default,html()">}}
{{< tab >}}
Save the code below as `output-markdown.tql`.

```js {linenos=table,hl_lines=[2]}
SQL( `select * from example limit 2` )
MARKDOWN()
```

Invoke the tql file with *curl* command.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-markdown.tql
```

```
|NAME|TIME|VALUE|
|:-----|:-----|:-----|
|TAG0|1628694000000000000|10.000000|
|TAG0|1628780400000000000|11.000000|
```
{{< /tab >}}
{{< tab >}}
Save the code below as `output-markdown.tql`.

```js {linenos=table,hl_lines=[2]}
SQL( `select * from example limit 2` )
MARKDOWN( html(true) )
```

Invoke the tql file with *curl* command.

```sh
$ curl http://127.0.0.1:5654/db/tql/output-markdown.tql
```

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
{{< /tab >}}
{{< /tabs >}}

## HTML

The `HTML()` function generates an HTML document as output, using the provided template language for formatting.
This allows you to fully customize the structure and appearance of the HTML output based on your query results.

You can use template expressions (such as `{{ .V.column_name }}` for column values, `{{ if .IsFirst }}` for the first row, and `{{ if .IsLast }}` for the last row) to control how the HTML is generated. This makes it easy to create tables, reports, or any other HTML-based representation of your data directly from TQL scripts.

```html {linenos=table,hl_lines=["10-14"]}
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

**Save *tql* file**

Save the code below as `output-chart.tql`.

```js {linenos=table,hl_lines=[4,6],linenostart=1}
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

Open web browser with `http://127.0.0.1:5654/db/tql/output-chart.tql`

> The legacy `CHART_LINE()`, `CHART_BAR()`, `CHART_SCATTER()` and its family functions are deprecated 
> with the new `CHART()` function.
> Please refer to the [CHART()](/neo/tql/chart) for the examples.

### CHART with chartJson()

**Save *tql* file**

Save the code below as `output-chart.tql`.

```js {linenos=table,hl_lines=[3],linenostart=1}
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

Open web browser with `http://127.0.0.1:5654/db/tql/output-chart.tql`

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

### CHART with chartID()

**Save *tql* file**

Save the code below as `output-chart.tql`.

```js {linenos=table,hl_lines=[3],linenostart=1}
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

Open web browser with `http://127.0.0.1:5654/db/tql/output-chart.tql`

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

This scenario is useful when your DOM document has `<div id='myChart'/>`.

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

## Cache Result Data

{{< neo_since ver="8.0.43" />}}

The `cache()` option function has been added to `CSV()`, `JSON()`, `NDJSON()` and `HTML()` SINK as shown below.

```js
SQL( "select * from example limit ?, 1000",  param("offset") ?? 0 )
JSON( cache( param("offset") ?? "0", "60s" ) )
```

The new `cache()` option accepts two mandatory parameters, `CACHE_KEY` and `TTL`, and one optional parameter `r`.

**Syntax**: `cache(CACHE_KEY string, TTL string, [r float])`

1.	The first parameter, `CACHE_KEY`, is used to register/search the cache data and is composed of 
    `[filename] + [source_code_hash] + [CACHE_KEY]`. 
    Therefore, the results executed with the same `CACHE_KEY` in the same TQL (same filename + same code) 
    will have the same key, and the later executed results will overwrite the existing cache data.
2.	The second parameter, `TTL`, automatically deletes the cache after the given period.
    Requests received after TTL will query the actual DB and return the result data,
    which will then be registered in the cache again.
3.	The third optional parameter, `r`, is the "preemptive-cache-update-ratio" 
    and must be a value between 0 and 1.0 (excludes 0 and 1.0).
    For the first request received between `r * TTL` and `TTL`,
    the system will respond with the current cache data and then execute the query to update the cache.
    Subsequent requests will get the updated results from the cache.
    This ensures that frequently requested `CACHE_KEY`s have continuously updated cache data in the background.

If the code is modified, the `source_code_hash` will change, resulting in a cache miss.
A cache miss will also occur if the `TTL` has expired and the cache is automatically deleted.
In either case, the request will be executed, and the result data will be registered in the cache.

The described behavior only applies when the `cache()` option is added to the SINK function.
TQLs without the `cache()` option will not search the cache.

> Note: Excessive use of cache may cause memory shortage issues.
> For example, using cache() in TQLs that SELECT multiple billions of records...
