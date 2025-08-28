---
title: SINK
type: docs
weight: 21
---

All *tql* scripts must end with one of the sink functions.

The basic SINK function might be `INSERT()` which write the incoming records onto machbase-neo database. `CHART()` function can render various charts with incoming records. `JSON()` and `CSV()` encode incoming data into proper formats.

![tql_sink](../img/tql_sink.jpg)

## INSERT()

*Syntax*: `INSERT( [bridge(),] columns..., table() [, tag()] )`

`INSERT()` stores incoming records into specified database table by an 'INSERT' statement for each record.

- `bridge()` *bridge('name')* optional.
- `columns` *string* column list.
- `table()` *table('name')* specify the destination table name.
- `tag()` *tag('name')* optional, applicable only to tag tables.

{{<tabs items="Example,PUSHVALUE(),tag()">}}
{{<tab>}}
Write records to machbase that contains tag name.

```js {{linenos=table,hl_lines=[6]}}
FAKE(json({
    ["temperature", 1708582790, 23.45],
    ["temperature", 1708582791, 24.56]
}))
MAPVALUE(1, value(1)*1000000000) // convert epoch sec to nanosec
INSERT("name", "time", "value", table("example"))
```
{{</tab>}}
{{<tab>}}
Write records to machbase with same tag name by adding "name" field by `PUSHVALUE()`.
```js {{linenos=table,hl_lines=[5,7]}}
FAKE(json({
    [1708582792, 32.34],
    [1708582793, 33.45]
}))
PUSHVALUE(0, "temperature")
MAPVALUE(1, value(1)*1000000000) // convert epoch sec to nanosec
INSERT("name","time", "value", table("example"))
```
{{</tab>}}
{{<tab>}}
Write records to machbase with same tag name by using `tag()` option if the destination is a tag table.
```js {{linenos=table,hl_lines=[6]}}
FAKE(json({
    [1708582792, 32.34],
    [1708582793, 33.45]
}))
MAPVALUE(0, value(0)*1000000000) // convert epoch sec to nanosec
INSERT("time", "value", table("example"), tag('temperature'))
```
{{</tab>}}
{{</tabs>}}

Insert records into bridged database.

```js {{linenos=table,hl_lines=[2]}}
INSERT(
    bridge("sqlite"),
    "company", "employee", "created_on", table("mem_example")
)
```

## APPEND()

*Syntax*: `APPEND( table() )`

*APPEND()* stores incoming records into specified database table via the 'append' method of machbase-neo.

- `table()` *table(string)* specify destination table

```js {{linenos=table,hl_lines=[6]}}
FAKE(json({
    ["temperature", 1708582794, 12.34],
    ["temperature", 1708582795, 13.45]
}))
MAPVALUE(1, value(1)*1000000000 ) // convert epoch sec to nanosec
APPEND( table("example") )
```

## CSV()

*Syntax*: `CSV( [tz(), timeformat(), precision(), rownum(), heading(), delimiter(), nullValue() ] )`

Makes the records of the result in CSV format. The values of the records become the fields of the CSV lines.
The end of the data is identified by the last two consecutive newline characters (`\n\n`).

For example, if a record was `{key: k, value:[v1,v2]}`, it generates an CSV records as `v1,v2`.

- `tz` *tz(name)* time zone, default is `tz('UTC')`
- `timeformat` *timeformat(string)* specify the format how represents datetime fields, default is `timeformat('ns')`
- `rownum` *rownum(boolean)* adds rownum column
- `precision` *precision(int)* specify precision of float fields, `precision(-1)` means no restriction, `precision(0)` converts to integer
- `heading` *heading(boolean)* add fields names as the first row
- `delimiter` *delimiter(string)* specify fields separator other than the default comma(`,`).
- `nullValue()` specify substitution string for the *NULL* value, default is `nullValue('NULL')`. {{< neo_since ver="8.0.14" />}}
- `substituteNull` *substitute(string)* specify substitution string for the *NULL* value, default is `substituteNull('NULL')`. (deprecated, replaced by `nullValue()`)
- `cache()` cache result data. see [Cache Result Data](../reading/#cache-result-data) for details. {{< neo_since ver="8.0.43" />}}

{{< tabs items="default,heading(),delimiter(),nullValue()">}}
{{< tab >}}
```js {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10)
CSV()
```
```csv
1,10
2,20
3,30
```
{{</ tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
CSV( heading(true) )
```
```csv
x,x10
1,10
2,20
3,30
```
{{</ tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
CSV( heading(true), delimiter("|") )
```
```csv
x|x10
1|10
2|20
3|30
```
{{</ tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=[2],linenostart=1}
FAKE( json({ ["A", 123], ["B", null], ["C", 234] }) )
CSV( nullValue("***") )
```
```csv
A|123
B|***
C|234
```
{{</ tab >}}
{{</ tabs >}}

## JSON()

*Syntax*: `JSON( [transpose(), tz(), timeformat(), precision(), rownum(), rowsFlatten(), rowsArray() ] )`

Generates JSON results from the values of the records.

- `transpose` *transpose(boolean)* transpose rows and columns, it is useful that specifying `transpose(true)` for the most of chart libraries.
- `tz` *tz(name)* time zone, default is `tz('UTC')`.
- `timeformat` *timeformat(string)* specify the format how represents datetime fields, default is `timeformat('ns')`.
- `rownum` *rownum(boolean)` adds rownum column.
- `precision` *precision(int)* specify precision of float fields, `precision(-1)` means no restriction, `precision(0)` converts to integer.
- `rowsFlatten` *rowsFlatten(boolean)* reduces the array dimension of the *rows* field in the JSON object. If `JSON()` has `transpose(true)` and `rowsFlatten(true)` together, it ignores `rowsFlatten(true)` and only `transpose(true)` affects on the result. {{< neo_since ver="8.0.12" />}}
- `rowsArray` *rowsArray(boolean)* produces JSON that contains only array of object for each record. The `rowsArray(true)` has higher priority than `transpose(true)` and `rowsFlatten(true)`. {{< neo_since ver="8.0.12" />}}
- `cache()` cache result data. see [Cache Result Data](../reading/#cache-result-data) for details. {{< neo_since ver="8.0.43" />}}

{{< tabs items="default,transpose(),rowsFlatten(),rowsArray()">}}
{{< tab >}}
```js {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10)
JSON()
```

```json {hl_lines=[5]}
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
{{</ tab >}}
{{< tab >}}
```js  {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
JSON( transpose(true) )
```

```json {hl_lines=[5]}
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
{{</ tab >}}
{{< tab >}}
```js  {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
JSON( rowsFlatten(true) )
```

```json {hl_lines=[5]}
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
{{</ tab >}}
{{< tab >}}
```js  {linenos=table,hl_lines=[3],linenostart=1}
FAKE( arrange(1, 3, 1))
MAPVALUE(1, value(0)*10, "x10")
JSON( rowsArray(true) )
```

```json {hl_lines=[5]}
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
{{</ tab >}}
{{</ tabs >}}

## NDJSON()

*Syntax*: `NDJSON( [tz(), timeformat(), rownum()] )` {{< neo_since ver="8.0.33" />}}

Generates NDJSON results from the values of the records.

NDJSON (Newline Delimited JSON) is a format for streaming JSON data where each line is a valid JSON object. This is useful for processing large datasets or streaming data because it allows you to handle one JSON object at a time.
The end of the data is identified by the last two consecutive newline characters (`\n\n`).

- `tz` *tz(name)* time zone, default is `tz('UTC')`.
- `timeformat` *timeformat(string)* specify the format how represents datetime fields, default is `timeformat('ns')`.
- `rownum` *rownum(boolean)` adds rownum column.
- `cache()` cache result data. see [Cache Result Data](../reading/#cache-result-data) for details. {{< neo_since ver="8.0.43" />}}

```js {linenos=table,hl_lines=[2],linenostart=1}
SQL(`select * from example where name = 'neo_load1' limit 3`)
NDJSON(timeformat('Default'), tz('local'), rownum(true))
```

```json
{"NAME":"neo_load1","ROWNUM":1,"TIME":"2024-09-06 14:46:19.852","VALUE":4.58}
{"NAME":"neo_load1","ROWNUM":2,"TIME":"2024-09-06 14:46:22.853","VALUE":4.69}
{"NAME":"neo_load1","ROWNUM":3,"TIME":"2024-09-06 14:46:25.852","VALUE":4.69}

```

## MARKDOWN()

Generates a table in markdown format or HTML.

*Syntax*: `MARKDOWN( [ options... ] )`

- `tz(string)` time zone, default is `tz('UTC')`
- `timeformat(string)` specify the format how represents datetime fields, default is `timeformat('ns')`
- `html(boolean)` produce result by HTML renderer, default `false`
- `rownum(boolean)` show rownum column
- `precision` *precision(int)* specify precision of float fields, `precision(-1)` means no restriction, `precision(0)` converts to integer.
- `brief(boolean)` omit result rows, `brief(true)` is equivalent with `briefCount(5)`
- `briefCount(limit int)` omit result rows if the records exceeds the given limit, no omission if limit is `0`

{{< tabs items="default,briefCount,html">}}
{{< tab >}}
```js {linenos=table,hl_lines=[8]}
FAKE( csv(`
10,The first line 
20,2nd line
30,Third line
40,4th line
50,The last is 5th
`))
MARKDOWN()
```
```
|column0 |	column1 |
|:-------|:---------|
| 10     | The first line |
| 20     | 2nd line |
| 30     | Third line |
| 40     | 4th line |
| 50     | The last is 5th |
```
{{< /tab >}}
{{< tab >}}

```js {linenos=table,hl_lines=[8]}
FAKE( csv(`
10,The first line 
20,2nd line
30,Third line
40,4th line
50,The last is 5th
`))
MARKDOWN( briefCount(2) )
```

```
|column0 |	column1 |
|:-------|:---------|
| 10     | The first line |
| 20     | 2nd line |
| ...    | ...      |

> Total 5 records
```
{{< /tab >}}
{{< tab >}}

```js {linenos=table,hl_lines=[8]}
FAKE( csv(`
10,The first line 
20,2nd line
30,Third line
40,4th line
50,The last is 5th
`))
MARKDOWN( briefCount(2), html(true) )
```

|column0 |	column1 |
|:-------|:---------|
| 10     | The first line |
| 20     | 2nd line |
| ...    | ...      |

> Total 5 records

{{< /tab >}}
{{< /tabs >}}

## HTML()

*Syntax*: `HTML(templates...)` {{< neo_since ver="8.0.52" />}}

Generates an HTML document using the provided templates.

For detailed usage and examples, refer to the [HTML](../html/) section.

## TEXT()

*Syntax*: `TEXT(templates...)` {{< neo_since ver="8.0.52" />}}

Generates a text document using the provided templates.

It functions similarly to `HTML()`, but does not perform HTML escaping on the data.

## DISCARD()

*Syntax*: `DISCARD()` {{< neo_since ver="8.0.7" />}}

`DISCARD()` silently ignore all records as its name implies, so that no output generates.

```js {linenos=table,hl_lines=[8],linenostart=1}
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

*Syntax*: `CHART()` {{< neo_since ver="8.0.8" />}}

Generates chart using Apache echarts.

Refer to [CHART() examples](/neo/tql/chart/) for the various usages.

<!-- ## Deprecated

### CHART_LINE()

> **DEPRECATED**: use CHART() instead.

*Syntax*: `CHART_LINE()`

Generates a line chart in HTML format.

{{< tabs items="CHART_LINE(),CHART()">}}
{{< tab >}}
```js {linenos=table,hl_lines=["5-8"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--> time   value
// |
CHART_LINE(
    size("600px", "400px"),
    xAxis(0, "T", "time"), yAxis(0, "V", "value")
)
```
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=["7-19"],linenostart=1}
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
{{< /tab >}}
{{< /tabs >}}

### CHART_BAR()

> **DEPRECATED**: use CHART() instead.

*Syntax*: `CHART_BAR()`

Generates a bar chart in HTML format.

{{< tabs items="CHART_BAR(),CHART()">}}
{{< tab >}}
```js {linenos=table,hl_lines=["5-8"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--> time   value
// |
CHART_BAR(
    size("600px", "300px"),
    xAxis(0, "T", "time"), yAxis(0, "V", "value")
)
```
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=["7-19"],linenostart=1}
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
{{< /tab >}}
{{< /tabs >}}

### CHART_SCATTER()

> **DEPRECATED**: use CHART() instead.

*Syntax*: `CHART_SCATTER()`

Generates a scatter chart in HTML format.

{{< tabs items="CHART_SCATTER(),CHART()">}}
{{< tab >}}
```js {linenos=table,hl_lines=["5-8"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '25ms')))
// |    0      1
// +--> time   value
// |
CHART_SCATTER(
    size("600px", "300px"),
    xAxis(0, "T", "time"), yAxis(0, "V", "value")
)
```
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=["7-19"],linenostart=1}
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
{{< /tab >}}
{{< /tabs >}}

### CHART_LINE3D()

> **DEPRECATED**: use CHART() instead.

*Syntax*: `CHART_LINE3D()`

Generates a 3D line chart in HTML format.

{{< tabs items="CHART_LINE3D(),CHART()">}}
{{< tab >}}
```js {linenos=table,hl_lines=["9-14"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--> x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--> x   y   z
// |
CHART_LINE3D(
  size('600px', '600px'),
  lineWidth(2), 
  gridSize(100, 30, 100), 
  visualMap(-0.12, 0.12)
)
```
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=[10, "12-31"],linenostart=1}
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
{{< /tab >}}
{{< /tabs >}}

### CHART_BAR3D()

> **DEPRECATED**: use CHART() instead.

*Syntax*: `CHART_BAR3D()`

Generates a 3D bar chart in HTML format.

{{< tabs items="CHART_BAR3D(),CHART()">}}
{{< tab >}}
```js {linenos=table,hl_lines=["9-14"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--> x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--> x   y   z
// |
CHART_BAR3D(
  size('600px', '600px'),
  lineWidth(2), 
  gridSize(100, 30, 100), 
  visualMap(-0.12, 0.12)
)
```
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=[10, "12-30"],linenostart=1}
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
{{< /tab >}}
{{< /tabs >}}

### CHART_SCATTER3D()

> **DEPRECATED**: use CHART() instead.

*Syntax*: `CHART_SCATTER3D()`

Generates a 3D scatter chart in HTML format.

{{< tabs items="CHART_SCATTER3D(),CHART()">}}
{{< tab >}}
```js {linenos=table,hl_lines=["9-14"],linenostart=1}
FAKE(meshgrid(linspace(-1.0,1.0,100), linspace(-1.0, 1.0, 100)))
// |    0   1
// +--> x   y
// |
MAPVALUE(2, sin(10*(pow(value(0), 2) + pow(value(1), 2))) / 10 )
// |    0   1   2
// +--> x   y   z
// |
CHART_SCATTER3D(
  size('600px', '600px'),
  lineWidth(2), 
  gridSize(100, 30, 100), 
  visualMap(-0.12, 0.12)
)
```
{{< /tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=[10, "12-30"],linenostart=1}
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
{{< /tab >}}
{{< /tabs >}}

### title()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `title(label)`

- `label` *string*

### subtitle()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `subtitle(label)`

- `label` *string*

### xAxis(), yAxis(), zAxis()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `xAxis(idx, label [, type])`

- `idx` *number* index of column for the axis
- `label` *string* label of the axis
- `type` *string* type fo the axis, available: `'time'` and `'value'`, default is `'value'` if not specified.

> zAxis() is effective only with 3D chart

### dataZoom()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `dataZoom(type, minPercentage, maxPercentage)`

- `type` *string* "slider", "inside"
- `minPercentage` *number* 0 ~ 100
- `maxPercentage` *number* 0 ~ 100

> 2D chart only

### opacity()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `opacity(alpha)`

- `alpha` *number* 0.0 ~ 1.0

> 3D chart only

### autoRotate()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `autoRotate( [speed] )`

- `speed` *number* degree/sec, default is 10

### gridSize()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `gridSize( width, height, depth )`

- `width` *number* percentage (default: 100)
- `height` *number* percentage (default: 100)
- `depth` *number* percentage (default: 100)

> 3D chart only

### seriesLabels()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `seriesLabels( label... )`

- `label` *string*

Specify the label text of each series.

### toolbox

#### toolboxSaveAsImage()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `toolboxSaveAsImage(filename)` {{< neo_since ver="8.0.4" />}}

- `filename` *string* filename with extension supporting (.png, .jpeg, .svg).

Show the toolbox button to save chart as an image file.

#### toolboxDataZoom()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `toolboxDataZoom()` {{< neo_since ver="8.0.4" />}}

Show the toolbox button for data zoom.

#### toolboxDataView()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `toolboxDataView()` {{< neo_since ver="8.0.4" />}}

Show the toolbox button for raw data viewer.

```js {linenos=table,hl_lines=["6-8"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '20ms')) )
CHART_LINE( 
    xAxis(0, "T", "time"),
    yAxis(1, "V", "value"),
    size('400px', '300px'),
    toolboxSaveAsImage('image.png'),
    toolboxDataZoom(),
    toolboxDataView()
)
```

### visualMap()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `visualMap(min, max)`

- `min` *number*
- `max` *number*

It calls `visualMapColor()` internally with pre-defined default colors.

### visualMapColor()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `visualMapColor(min, max, colors...)` {{< neo_since ver="8.0.4" />}}

- `min` *number*
- `max` *number*
- `colors` *colors in array of string*

Example)

```js {linenos=table,hl_lines=["6-11"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '20ms')) )
CHART_LINE( 
    size('400px', '300px'),
    xAxis(0, "T", "time"),
    yAxis(1, "V", "value"),
    visualMapColor(-2.0, 2.0, 
        "#a50026", "#d73027", "#f46d43", "#fdae61", "#e0f3f8", 
        "#abd9e9", "#74add1", "#4575b4", "#313695", "#313695", 
        "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#fdae61",
        "#f46d43", "#d73027", "#a50026"
    )
)
```

### markArea()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `markArea(coord0, coord1 [, label [, color [, opacity]]])`

- `coord0` *any* : area beginning x-value
- `coord1` *any* : area ending x-value
- `label` *string* : title
- `color` *string* : color of area
- `opacity` *number* : 0~1 of opacity

*Example)*

```js {linenos=table,hl_lines=["6-7"],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_SCATTER(
    size('400px', '300px'),
    xAxis(0, "T", "time"),
    yAxis(1, "V", "value"),
    markArea(time('now+1s'), time('now+2s'), 'Error', '#ff000033'),
    markArea(time('now+1.5s'), time('now+2.5s'), 'Marked', '#22ff0022')
 )
```

### markXAxis()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `markXAxis(coord, label)`

- `coord` *any* : marked x-value
- `label` *string* : title

```js {linenos=table,hl_lines=[6],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_SCATTER(
    size('400px', '300px'),
    xAxis(0, "T", "time"),
    yAxis(1, "V", "value"),
    markXAxis(time('now+1.5s'), 'NOW')
)
```

### markYAxis()

> **DEPRECATED**: use chartOption() with CHART() instead.

*Syntax*: `markYAxis(coord, label)`

- `coord` *any* : marked y-value
- `label` *string* : title

```js {linenos=table,hl_lines=[6,7],linenostart=1}
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_SCATTER(
    size('400px', '300px'),
    xAxis(0, "T", "time"),
    yAxis(1, "V", "value"),
    markYAxis(1.0, 'max'),
    markYAxis(-1.0, 'min')
)
```

 -->
