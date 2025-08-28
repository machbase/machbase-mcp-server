---
title: SRC
type: docs
weight: 11
---

All *tql* scripts must start with one of the data source functions.

There are several SRC functions are included. For example, `SQL()` produces records by querying machbase-neo database or even external (bridged) database with the given sql statement. `FAKE()` generates artificial data. `CSV()` can read csv data, `BYTES()` reads arbitrary binary data from file system or client's HTTP request and MQTT payload.

![tql_src](../img/tql_src.jpg)

## SQL()

*Syntax*: `SQL( [bridge(),] sqltext [, params...])`

- `bridge()` *bridge('name')* If a bridge is given, the SQL query is executed on the bridge
- `sqltext` *string* : SQL SELECT statement to retrieve data from database. Use backtick(`) for multi-line sql string.
- `params` : Variadic arguments for the bind arguments for the query.

*Example)*

- Query to machbase

```js
SQL (`
    SELECT time, value 
    FROM example 
    WHERE name ='temperature'
    LIMIT 10000
`)
```

- Query with variadic arguments

```js
SQL(`SELECT time, value FROM example WHERE name = ? LIMIT ?`,
    param('name') ?? 'temperature',
    param('limit') ?? 10)
```

- Query to bridge database

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

*Syntax*: `SQL_SELECT( fields..., from(), between() [, limit()] )` {{< neo_since ver="8.0.15" />}}

- `fields` `string` : column names, multiple columns are possible.

*SQL_SELECT()* source function provides same functionality with *SQL()*, but it simplifies the usage by standardization option functions other than using the raw SQL statement.

This function actually works equivalent to `SQL()` but it takes query conditions via simplified options instead of a full SQL statement.
It assigns time range condition easier way than using `WHERE` condition in SQL statement.

The example below process data by query `SELECT time, value FROM example WHERE NAME = 'temperature' AND time BETWEEN...`.

```js
SQL_SELECT(
    'time', 'value',
    from('example', 'temperature'),
    between('last-10s', 'last')
)
```
is equivalent with the `SQL()` statement below
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

*Syntax*: `from( table, tag [, time_column [, name_column] ] )`

It provides table name and tag name to `SQL_SELECT()` function generating SQL internally. It may equivalent to `... FROM <table> WHERE NAME = <tag> ...`.

- `table` *string* table name
- `tag` *string* tag name
- `time_column` *string* specify "time" column name, if omitted default is `'time'`.
- `name_column` *string* specify "name" column name, if omitted default is `'name'`. {{< neo_since ver="8.0.5" />}}

### between()

*Syntax*: `between( fromTime, toTime [, period] )`

It provides time range condition to `SQL_SELECT()` function generating SQL internally.
It may equivalent to `... WHERE ... TIME BETWEEN <fromTime> AND <toTime>...`.

- `fromTime` *string,number* time expression with 'now' and 'last' as string, Or assign number as unix epoch time in nanosecond
- `toTime` *string,number* time expression
- `period` *string,number* duration expression, Or assign number for the unix epoch time in nanoseconds. Logically only positive period makes sense.

You can specify `fromTime` and `toTime` with 'now' and 'last' with delta duration expression. 
For example, `'now-1h30m'` specifies the time that 1 hour 30 minutes before from now.
`'last-30s'` means 30 seconds before the latest(=max) time of the `base_time_column`.

If `period` is specified it will generate 'GROUP BY' *time* expression with aggregation SQL functions. In this case the base *time* column should be included in the *fields* arguments of the `SQL_SELECT()`.

If it is required to use string expressions for the `fromTime`, `toTime` instead of unix epoch nano seconds, use `parseTime()` to convert
string-time-expression to time value. Refer to the document about utility function [*parseTime()*](/neo/tql/utilities/#parsetime)

*Example)*

```js
between( parseTime("2023-03-01 14:00:00", "DEFAULT", tz("Local")),
         parseTime("2023-03-01 14:05:00", "DEFAULT", tz("Local")))
```

### limit()

*Syntax*: `limit( [offset ,] count )`

It will be translated into `SELECT... LIMIT offset, count` statement.

- `offset` *number* default is `0`. if omitted
- `count` *number*

## CSV()

*Syntax*: `CSV( file(file_path_string) | payload() [, charset()] [,field()...[, header()]] )`

Load CSV and yield key-value records, the key is generated in sequence number and the fields of CSV become the value of the record.
The string parameter of 'file' should be absolute path to the CSV.
If `payload()` is used, it will reads CSV from HTTP POST request body stream. It is useful to make an API that writes data into database when remote client sends data by HTTP POST.

- `file() | payload()` input stream
- `field(idx, type, name)` specifying fields
- `header(bool)` specifies if the first line of input stream is a header
- `charset(string)` specify charset if the CSV data is in non UTF-8. {{< neo_since ver="8.0.8" />}}
- `logProgress([int])` logs progress messages every `n` rows. If `n` is omitted, it defaults to 500,000. {{< neo_since ver="8.0.29" />}}

*Example)*

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

Combination of `CSV()` and `APPEND()` as above example, it is simple, useful. Be aware that it is 5 times slower than command line import command, but still faster than `INSERT()` function when writing more than several thousands records per a HTTP request.

Use `??` operator to make it works with or without HTTP POST request.

```js
CSV(payload() ?? file('/absolute/path/to/data.csv'),
    field(0, floatType(), 'freq'),
    field(1, floatType(), 'ampl')
)
CHART_LINE()
```

### file()

*Syntax*: `file(path)`

Open the given file and returns input stream for the content. the path should be the absolute path to the file.

- `path` *string* path to the file to open, or http url where to get resource from.

If `path` starts with "http://" or "https://", it retrieves the content of the specified http url {{< neo_since ver="8.0.7" />}}. Otherwise it is looking for the path on the file system.

The code below shows how to call a remote HTTP api with `file()` that it actually invokes machbase-neo itself for the demonstration purpose, the SQL query which safely url escaped by `escapeParam()`.

```js
CSV( file(`http://127.0.0.1:5654/db/query?`+
        `format=csv&`+
        `q=`+escapeParam(`select * from example limit 10`)
))
CSV() // or JSON()
```

### payload()

*Syntax*: `payload()`

Returns the input stream of the request content if the *tql* script has been invoked from HTTP POST or MQTT PUBLISH.

### field()

*Syntax*: `field(idx, typefunc, name)`

Specify field-types of the input CSV data.

- `idx` *number* 0-based index of the field.
- `typefunc` specify the type of the field. (see below)
- `name` *string* specify the name of the field.

| type function    | type      |
|:-----------------| :---------|
| `stringType()`   | string    |
| `doubleType()`   | double    |
| `datetimeType()` | datetime  |
| `boolType()`     | boolean  {{< neo_since ver="8.0.20" />}} |
| ~~`floatType()`~~    | *deprecated, use `doubleType()`*  {{< neo_since ver="8.0.20" />}} |
| ~~`timeType()`~~     | *deprecated, use `datetimeType()`*  {{< neo_since ver="8.0.20" />}}|

The `stringType()`, `boolType()` and `floatType()` take no arguments, `timeType()` function takes one or two parameters for proper conversion of date-time data.

If the input data of the field specifies time in unix epoch time, specify the one of the time units `ns`, `us`, `ms` and `s`.
- `datetimeType('s')`
- `datetimeType('ms')`
- `datetimeType('us')`
- `datetimeType('ns')`

The input field represents time in human readable format, it is requires to specifying how to parse them including time zone.

- `datetimeType('DEFAULT', 'Local')`

```js
CSV(payload() ??
`name,2006-01-02 15:04:05.999,10`,
field(1, datetimeType('DEFAULT', 'Local'), 'time'))
CSV()
```

- `datetimeType('RFC3339', 'EST')`

```js
CSV(payload() ??
`name,2006-01-02T15:04:05.999Z,10`,
field(1, datetimeType('RFC3339', 'EST'), 'time'))
CSV()
```

If the timezone is omitted, it assumes 'UTC' by default.

- `datetimeType('RC822')`

The first argument of the `timeType()` directs how to parse the input data that uses the same syntax with `timeformat()` function. Please refer to the description of the `timeformat()` function for the [timeformat spec](../utilities/#timeformat).

### charset()

*Syntax*: `charset(name)` {{< neo_since ver="8.0.8" />}}

- `name` *string* character set name

Supported character set.

UTF-8, ISO-2022-JP, EUC-KR, SJIS , CP932, SHIFT_JIS, EUC-JP, UTF-16, UTF-16BE, UTF-16LE,
CP437, CP850, CP852, CP855, CP858, CP860, CP862, CP863, CP865, CP866, LATIN-1,
ISO-8859-1, ISO-8859-2, ISO-8859-3, ISO-8859-4, ISO-8859-5, ISO-8859-6, ISO-8859-7, 
ISO-8859-8, ISO-8859-10, ISO-8859-13, ISO-8859-14, ISO-8859-15, ISO-8859-16,
KOI8R, KOI8U, MACINTOSH, MACINTOSHCYRILLIC, WINDOWS1250, WINDOWS1251, WINDOWS1252,
WINDOWS1253, WINDOWS1254, WINDOWS1255, WINDOWS1256, WINDOWS1257, WINDOWS1258, WINDOWS874,
XUSERDEFINED, HZ-GB2312

## SCRIPT()

Supporting user defined script language.

See [SCRIPT](../script/) section for the details with examples.

## HTTP()

Request HTTP Request within simple DSL.

See [HTTP](../http/) section for the details with examples.

## BYTES(), STRING()

*Syntax*: `BYTES( src [, separator(char), trimspace(boolean) ] )`

*Syntax*: `STRING( src [, separator(char), trimspace(boolean) ] )`

- `src` data source, it can be one of `payload()`, `file()` and a constant text `string`.
- `separator(char)` *optional* set`separator("\n")` to read a line by line, or omit it to read whole string in a time.
- `trimspace(boolean)` *optional* trim spaces, default is `false`

Split the input content by separator and yield records that separated sub content as value and the key is increment number of records.

*Example)*

- `STRING('A,B,C', separator(","))` yields 3 records `["A"]`, `["B"]` and `["C"]`.
- `STRING('A,B,C')` yields 1 record `["A,B,C"]`.

The both of `BYTES()` and `STRING()` works exactly same,
except the value types that yields, as the function's name implies,
`BYTES()` yields value in 'array of byte' and `STRING()` yields `string` value.

```js
STRING(payload() ?? `12345
                    23456
                    78901`, separator("\n"))
```
 
The example code above generates 3 records `["12345"]`, `["␣␣␣␣␣␣␣␣␣␣23456"]`, `["␣␣␣␣␣␣␣␣␣␣78901"]`.

```js
STRING(payload() ?? `12345
                    23456
                    78901`, separator("\n"), trimspace(true))
```

The example code above generates 3 records `["12345"]`, `["23456"]`, `["78901"]`.

```js
STRING( file(`http://example.com/data/words.txt`), separator("\n") )
```
It retrieves the content from the http address. `file()` supports http url {{< neo_since ver="8.0.7" />}}.

## ARGS()

*Syntax*: `ARGS()` {{< neo_since ver="8.0.7" />}}

`ARGS` generates a record that values are passed by parent TQL flow as arguments.
It is purposed to be used as a SRC of a sub flow within a `WHEN...do()` statement.

```js {linenos=table,hl_lines=[6],linenostart=1}
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

The code print log message on the output console.
```
OUTPUT: 2 WORLD
```

## FAKE()

*Syntax*: `FAKE( generator )`

- `generator` one of the `oscillator()`, `meshgrid()`, `linspace()`, `arrange()`, `csv()`, `json()`

Producing "fake" data by given generator.

### oscillator()

*Syntax*: `oscillator( freq() [, freq()...], range() )`

Generating wave data by given frequency and time range. If provide multiple `freq()` arguments, it composites waves.

{{< tabs items="Clean,Add noise">}}
{{< tab >}}
```js {{linenos=table,hl_lines=[1],linenostart=1}}
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
{{< /tab >}}
{{< tab >}}
```js {{linenos=table,hl_lines=[4],linenostart=1}}
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
{{< /tab >}}
{{< /tabs >}}

#### freq()

*Syntax*: `freq( frequency, amplitude [, bias, phase])`

It produce sine wave by time `amplitude * SIN( 2*Pi * frequency * time + phase) + bias`.

- `frequency` *number* frequency in Hertz (Hz).
- `amplitude` *number*
- `bias` *number*
- `phase` *number* in radian

#### range()

*Syntax*: `range( fromTime, duration, period )`

It specifies time range from `fromTime` to `fromTime+duration`.

- `fromTime` *string*|*number* 'now' and 'last' is available for string type, Or assign number as unix epoch time in nanosecond
- `duration` *string*|*number* duration expression, Or assign number in nanoseconds. ex) `'-1d2h30m'`, `'1s100ms'`
- `period` *string*|*number* duration expression, Or assign number in nanoseconds. Logically only positive period makes sense.

### arrange()

*Syntax*: `arrange(start, stop, step)` {{< neo_since ver="8.0.12" />}}

- `start` *number*
- `stop` *number*
- `step` *number*

```js {{linenos="table",hl_lines=[2]}}
FAKE(
   arrange(1, 2, 0.5)
)
CSV()
```

```csv
1
1.5
2
```

### linspace()

*Syntax*: `linspace(start, stop, num)`

It generates 1 dimension linear space.

{{< tabs items="CSV,CHART">}}
{{< tab >}}
```js {{linenos="table",hl_lines=[2]}}
FAKE(
   linspace(1, 3, 3)
)
CSV()
```

```csv
1
2
3
```
{{< /tab >}}
{{< tab >}}

```js {{linenos="table",hl_lines=[1]}}
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

{{< /tab >}}
{{< /tabs >}}

### meshgrid()

*Syntax*: `meshgrid(xseries, yseries)`

It generates meshed values - [xseries, yseries].

{{< tabs items="CSV,CHART">}}
{{< tab >}}
```js {{linenos="table",hl_lines=[2]}}
FAKE(
    meshgrid( linspace(1, 3, 3), linspace(10, 30, 3) )
)
CSV()
```

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
{{< /tab >}}
{{< tab >}}
```js {{linenos="table",hl_lines=[1]}}
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

{{< /tab >}}
{{< /tabs >}}

### csv()

*Syntax*: `csv(content)` {{< neo_since ver="8.0.7" />}}

- `content` *string* csv content

It generates records from the given csv content.

```js {{linenos="table",hl_lines=["2-6"]}}
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

```csv
A,10,true
B,20,false
C,30,true
```

### json()

*Syntax*: `json({...})` {{< neo_since ver="8.0.7" />}}

It generates records from the given multiple json array.

```js {{linenos="table",hl_lines=["2-6"]}}
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

```csv
A,10,true
B,20,false
C,30,true
```
