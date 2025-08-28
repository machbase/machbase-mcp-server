---
title: Utility Functions
type: docs
weight: 41
---

Utility functions can be commonly used as parameters of any functions.

## Constants

| constants        | description                         |
|:---------------- | :---------------------------------- |
| `NULL`           | null value                          |
| `PI`             | 3.141592....   https://oeis.org/A000796 |

## Context

### key()

*Syntax*: `key()`

Returns the key of the current record.

### value()

*Syntax*: `value( [index] )`

- `index` *integer* *optional* index of the value array

Returns the whole value of the current records in array.
If the index is given, it returns the element of the values.

For example, If the current value is `[0, true, "hello", "world"]`

- `value()` returns the whole value array `[0, true, "hello", "world"]`
- `value(0)` returns the first element of the value `0`
- `value(3)` returns the last element of the value `"world"`

### payload()

*Syntax*: `payload()`

Returns the current input stream that sent from caller of the *tql* script.
If the *tql* script is called via HTTP, the result of `payload()` is the stream of the body content of POST request.
If the *tql* script is called via MQTT, the `payload()` returns the payload of the PUBLISH message.

### param()

*Syntax*: `param( name )`

- `name` *string* name of the query parameter

When the *tql* script is called via HTTP, the requested query parameters can be accessed by `param()` function.

### context()

*Syntax*: `context()`

Returns context object of the script runtime.

## String

### escapeParam()

*Syntax*: `escapeParam( str ) : string` {{< neo_since ver="8.0.7" />}}

`escapeParam()` escapes the string so it can be safely placed inside a URL query.

```js {linenos=table,hl_lines=["3"],linenostart=1}
CSV(
    file(`http://127.0.0.1:5654/db/query?format=csv&q=`+
        escapeParam(`select count(*) from example`)
    )
)
CSV()
```

### strTrimSpace()

*Syntax*: `strTrimSpace(str) : string` {{< neo_since ver="8.0.7" />}}

`strTrimSpace` returns a slice of the string str, with all leading and trailing white space removed.

### strTrimPrefix()

*Syntax*: `strTrimPrefix(str, prefix) : string` {{< neo_since ver="8.0.7" />}}

`strTrimPrefix` returns str without the provided leading prefix string. If str doesn't start with prefix, str is returned unchanged.

### strTrimSuffix()

*Syntax*: `strTrimSuffix(str, suffix) : string` {{< neo_since ver="8.0.7" />}}

`strTrimSuffix` returns str without the provided trailing suffix string. If str doesn't end with suffix, str is returned unchanged.

### strHasPrefix()

*Syntax*: `strHasPrefix(str, prefix) : boolean` {{< neo_since ver="8.0.7" />}}

`strHasPrefix` tests whether the string str begins with prefix.

### strHasSuffix()

*Syntax*: `strHasSuffix(str, suffix) : boolean` {{< neo_since ver="8.0.7" />}}

`strHasSuffix` tests whether the string s ends with suffix.

### strReplaceAll()

*Syntax*: `strReplaceAll(str, old, new) : string` {{< neo_since ver="8.0.7" />}}

`strReplaceAll` returns a copy of the string s with all non-overlapping instances of old replaced by new.
If old is empty, it matches at the beginning of the string
and after each UTF-8 sequence, yielding up to k+1 replacements for a k-rune string.

### strReplace()

*Syntax*: `strReplace(str, old, new, n) : string` {{< neo_since ver="8.0.7" />}}

- `str` *string*
- `old` *string*
- `new` *string*
- `n` *integer*

`strReplace`returns a copy of the string s with the first n non-overlapping instances of old replaced by new.
If old is empty, it matches at the beginning of the string and after each UTF-8 sequence,
yielding up to k+1 replacements for a k-rune string.
If n < 0, there is no limit on the number of replacements.

### strSub()

*Syntax*: `strSub(str, offset [, count]) : string` {{< neo_since ver="8.0.7" />}}

`strSub` returns substring of str.

### strIndex()

*Syntax*: `strIndex(str, substr) : number` {{< neo_since ver="8.0.15" />}}

Returns the index of the first instance of substr in str, or -1 if substr is not present in str.

### strLastIndex()

*Syntax*: `strLastIndex(str, substr) : number` {{< neo_since ver="8.0.15" />}}

Returns the index of the last instance of substr in str, or -1 if substr is not present in str.

### strToUpper()

*Syntax*: `strToUpper(str) : string` {{< neo_since ver="8.0.7" />}}

`strToUpper` returns str with all Unicode letters mapped to their upper case.

### strToLower()

*Syntax*: `strToLower(str, suffix) : string` {{< neo_since ver="8.0.7" />}}

`strToLower` returns str with all Unicode letters mapped to their lower case.

### strSprintf()

*Syntax*: `strSprintf(fmt, args...) : string` {{< neo_since ver="8.0.7" />}}

`strSprintf()` formats according to a format specifier and returns the resulting string.

The syntax of `fmt` format string is `%[flags][width][.precision]verb`.

The verb at the end defines the type and the interpretation of its corresponding argument.

| verb  | description     |
| :---- | :-------------- |
| f     | decimal floating point, lowercase |
| F     | decimal floating point, uppercase |
| e     | scientific notation (mantissa/exponent), lowercase |
| E     | scientific notation (mantissa/exponent), uppercase |
| g     | the shortest representation of %e or %f |
| G     | the shortest representation of %E or %F |
| q     | a quoted string        |
| t     | the word true or false |
| s     | a string               |
| v     | default format         |
| %%    | a single %             |

```js {linenos=table,hl_lines=["3"],linenostart=1}
FAKE( csv(`world,3.141792`) )
MAPVALUE(1, parseFloat(value(1)))
MAPVALUE(2, strSprintf(`hello %s? %1.2f`, value(0), value(1)))
CSV()
```

```csv
world,3.141792,hello world? 3.14
```

### strTime()

*Syntax*: `strTime(time, format [, tz]) : string` {{< neo_since ver="8.0.7" />}}

- `time` *time*
- `format` *string*|*sqlTimeformat()*
- `tz` *tz()* optional, time zone if omitted default is `tz('UTC')`.

`strTime()` formats time value to string according to the given format and time zone.

**numeric timeformat**

```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE( linspace(0, 1, 1))
MAPVALUE(0, strTime(time("now"), "2006/01/02 15:04:05.999", tz("UTC")), "result")
MARKDOWN(rownum(true))
```

**sqlTimeformat()**

```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE( linspace(0, 1, 1))
MAPVALUE(0, strTime(time("now"), sqlTimeformat("YYYY/MM/DD HH24:MI:SS.nnn"), tz("UTC")), "result")
MARKDOWN(rownum(true))
```

|ROWNUM|result|
|:-----|:-----|
|1|2024/01/10 07:27:29.667|

**named timeformat**

{{< neo_since ver="8.0.12" />}}

```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE( linspace(0, 1, 1))
MAPVALUE(0, strTime(time("now"), "RFC822", tz("UTC")), "time")
MARKDOWN(rownum(true))
```

|ROWNUM|time|
|:-----|:-----|
|1|10 Jan 24 07:23 UTC|

### parseFloat()

*Syntax*: `parseFloat( str )  : number` {{< neo_since ver="8.0.7" />}}

- `str` *string*

Parsing `str` into float number.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE( csv(`world,3.141792`) )
MAPVALUE(1, parseFloat(value(1)))
JSON()
```
{{< /tab >}}
{{< tab >}}
```json
{
    "data": {
        "columns": [ "column0", "column1" ],
        "types": [ "string", "double" ],
        "rows": [ [ "world", 3.141792 ] ]
    },
    "success": true,
    "reason": "success",
    "elapse": "140.125µs"
}
```
{{< /tab >}}
{{< /tabs >}}

### parseBool()

*Syntax*: `parseBool( str ) : boolean` {{< neo_since ver="8.0.7" />}}

- `str` *string*

It takes one of the accepted string values: "1", "t", "T", "TRUE", "true", "True", "0", "f", "F", "FALSE", "false", "False" 
and converts it to the equivalent boolean value: true or false. For any other string, the function returns an error.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE( csv(`world,True`) )
MAPVALUE(1, parseBool(value(1)))
JSON()
```
{{< /tab >}}
{{< tab >}}
```json
{
    "data": {
        "columns": [ "column0", "column1" ],
        "types": [ "string", "bool" ],
        "rows": [ [ "world", true ] ]
    },
    "success": true,
    "reason": "success",
    "elapse": "122.667µs"
}
```
{{< /tab >}}
{{< /tabs >}}

## String Match

### glob()

*Syntax*: `glob(pattern, text) : boolean` {{< neo_since ver="8.0.7" />}}

`glob` returns true if the `text` does match with `pattern`.

```js {linenos=table,hl_lines=["3"],linenostart=1}
FAKE( linspace(1, 4, 4))
PUSHVALUE(0, "map."+value(0))
WHEN( glob("*.3", value(0)), doLog("found", value(1)))
CSV()
```

### regexp()

*Syntax*: `regexp(expression, text) : boolean` {{< neo_since ver="8.0.7" />}}

`regexp` returns true if the `text` does match with `expression`.

```js {linenos=table,hl_lines=["3"],linenostart=1}
FAKE( linspace(1, 4, 4))
PUSHVALUE(0, "map."+value(0))
WHEN( regexp(`^map\.[2,3]$`, value(0)), doLog("found", value(1)))
CSV()
```

## Time

### time()

*Syntax*: `time( number|string ) : time`

- `time('now')` returns current time.
- `time('now -10s50ms')` returns the time 10.05 seconds before from now.
- `time(1672531200*1000000000)` returns the time of Jan-1-2023 AM 12:00:00

{{< tabs items="time('now'),time(epoch)">}}
{{< tab >}}
```js {linenos=table}
SQL(`select to_char(time), value from example where time < ?`, time('now'))
CSV()
```
{{< /tab >}}
{{< tab >}}
```js
SQL(`select to_char(time), value from example where time = ?`, time(1628737200123456789))
CSV()
```
{{< /tab >}}
{{< /tabs >}}

### timeYear()

*Syntax*: `timeYear( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeYear() returns the year in which *time* occurs.

### timeMonth()

*Syntax*: `timeMonth( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeMonth()  returns the month of the year specified by *time*.

### timeDay()

*Syntax*: `timeMonth( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeDay()  returns the day of the month specified by *time*.

### timeHour()

*Syntax*: `timeHour( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeHour() returns the hour within the day specified by *time*, in the range [0, 23]..

### timeMinute()

*Syntax*: `timeMinute( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeMinute() returns the minute offset within the hour specified by *time*, in the range [0, 59].

### timeSecond()

*Syntax*: `timeSecond( time ) : number`  {{< neo_since ver="8.0.15" />}}

timeSecond() returns the second offset within the minute specified by *time*, in the range [0, 59].

### timeNanosecond()

*Syntax*: `timeNanosecond( time ) : number`  {{< neo_since ver="8.0.15" />}}

timeNanosecond() returns the nanosecond offset within the second specified by *time*, in the range [0, 999999999].

### timeISOYear()

*Syntax*: `timeISOYear( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeISOYear() returns the ISO 8601 year number in which ts occurs.

### timeISOWeek()

*Syntax*: `timeISOWeek( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeISOWeek() returns the ISO 8601 week number in which *time* occurs.
Week ranges from 1 to 53. Jan 01 to Jan 03 of year n might belong to
week 52 or 53 of year n-1, and Dec 29 to Dec 31 might belong to week 1
of year n+1.

According to the rule that the first calendar week of a calendar year is
the week including the first Thursday of that year, and that the last one is
the week immediately preceding the first calendar week of the next calendar year.
See https://www.iso.org/obp/ui#iso:std:iso:8601:-1:ed-1:v1:en:term:3.1.1.23 for details.

### timeYearDay()

*Syntax*: `timeYearDay( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeYearDay() returns the day of the year specified by *time*, in the range [1,365] for non-leap years, and [1,366] in leap years.

### timeWeekDay()

*Syntax*: `timeWeekDay( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeWeekDay() returns the day of the week specified by *time*. (Sunday = 0, ...).

```js {{linenos=table,hl_lines=[3]}}
FAKE(arrange(1, 7, 1))
MAPVALUE(0, time(strSprintf("now - %.fd",value(0))))
GROUP( lazy(true), by(timeWeekDay(value(0))), count(value(0)) )
CSV()
```

### timeUnix()

*Syntax*: `timeUnix( time ) : number` {{< neo_since ver="8.0.13" />}}

*timeUnix* returns `time` as a Unix time, the number of seconds elapsed
since January 1, 1970 UTC. The result does not depend on the
location associated with `time`.

### timeUnixMilli()

*Syntax*: `timeUnixMilli( time ) : number` {{< neo_since ver="8.0.13" />}}

*timeUnixMilli* returns `time` as a Unix time, the number of milliseconds elapsed
since January 1, 1970 UTC. The result does not depend on the
location associated with `time`.

### timeUnixMicro()

*Syntax*: `timeUnixMicro( time ) : number` {{< neo_since ver="8.0.13" />}}

*timeUnixMicro* returns `time` as a Unix time, the number of microseconds elapsed
since January 1, 1970 UTC. The result does not depend on the
location associated with `time`.

### timeUnixNano()

*Syntax*: `timeUnixNano( time ) : number` {{< neo_since ver="8.0.13" />}}

*timeUnixNano* returns `time` as a Unix time, the number of nanoseconds elapsed
since January 1, 1970 UTC. The result does not depend on the
location associated with `time`.

### timeAdd()

*Syntax*: `timeAdd( number|string|time [, timeExpression] ) : time`

*Example)*

- `timeAdd('now', 0)` returns current time.
- `timeAdd('now', '-10s50ms')` returns the time 10.05 seconds before from now.
- `timeAdd(value(0), '1m')` if value(0) is time, it returns the time of 1 minute later from value(0).

{{< tabs items="timeAdd('now'),timeAdd(epoch)">}}
{{< tab >}}
```js {linenos=table}
SQL(`select to_char(time), value from example where time < ?`, timeAdd('now', '-10s'))
CSV()
```
{{< /tab >}}
{{< tab >}}
```js
SQL(`select to_char(time), value from example where time = ?`, timeAdd(1628737200123456789, '-5s'))
CSV()
```
{{< /tab >}}
{{< /tabs >}}

### roundTime()

*Syntax*: `roundTime( time, duration ) : time`

Returns rounded time.

*Example)*

- `roundTime(time('now'), '1h')`
- `roundTime(value(0), '1s')`

### parseTime()

*Syntax*: `parseTime( time, format [, timezone] ) : time`

- `time` *string* time expression
- `format` *string* time format expression
- `timezone` *tz* timezone, use `tz()` to get the demand location, if omitted default is `tz("UTC")`.

*Example)*

- `parseTime("2023-03-01 14:01:02", "DEFAULT", tz("Asia/Tokyo"))`
- `parseTime("2023-03-01 14:01:02", "DEFAULT", tz("local"))`

### tz()

*Syntax*: `tz( name ) : timeZone`

Returns time zone that matched with the given name

*Example)*
- `tz('local')`
- `tz('UTC')`
- `tz('EST')`
- `tz("Europe/Paris")`

### timeformat()

*Syntax*: `timeformat( format )`

- `format` *string*

```js {linenos=table,hl_lines=["6"],linenostart=1}
FAKE( json({
    [ 1701345032123456789, 10],
    [ 1701345043219876543, 11]
}))
MAPVALUE(0, time(value(0)) )
CSV(timeformat("DEFAULT"), tz("Asia/Seoul"))
```

```
2023-11-30 20:50:32.123,10
2023-11-30 20:50:43.219,11
```

| format         | result of timeformatting                          |
|:---------------|:------------------------------------------------- |
| DEFAULT        | 2006-01-02 15:04:05.999                           |
| NUMERIC        | 01/02 03:04:05PM '06 -0700                        |
| ANSIC          | Mon Jan _2 15:04:05 2006                          |
| UNIX           | Mon Jan _2 15:04:05 MST 2006                      |
| RUBY           | Mon Jan 02 15:04:05 -0700 2006                    |
| RFC822         | 02 Jan 06 15:04 MST                               |
| RFC822Z        | 02 Jan 06 15:04 -0700                             |
| RFC850         | Monday, 02-Jan-06 15:04:05 MST                    |
| RFC1123        | Mon, 02 Jan 2006 15:04:05 MST                     |
| RFC1123Z       | Mon, 02 Jan 2006 15:04:05 -0700                   |
| RFC3339        | 2006-01-02T15:04:05Z07:00                         |
| RFC3339NANO    | 2006-01-02T15:04:05.999999999Z07:00               |
| KITCHEN        | 3:04:05PM                                         |
| STAMP          | Jan _2 15:04:05                                   |
| STAMPMILLI     | Jan _2 15:04:05.000                               |
| STAMPMICRO     | Jan _2 15:04:05.000000                            |
| STAMPNANO      | Jan _2 15:04:05.000000000                         |
| s              | unix epoch time in seconds                        |
| ms             | unix epoch time in milliseconds                   |
| us             | unix epoch time in microseconds                   |
| ns             | unix epoch time in nanoseconds                    |
| s_ms           | seconds and millisec (05.999)                     |
| s_us           | seconds and microsec (05.999999)                  |
| s_ns           | seconds and nanosec  (05.999999999)               |
| s.ms           | seconds and millisec, zero padding (05.000)       |
| s.us           | seconds and microsec, zero padding (05.000000)    |
| s.ns           | seconds and nanosec, zero padding  (05.000000000) |

### sqlTimeformat()

*Syntax*: `sqlTimeformat( format )`

- `format` *string*

| format         | result of timeformatting                          |
|:---------------|:------------------------------------------------- |
| YYYY           | four-digit year value                             |
| YY             | two-digit year value                              |
| MM             | two-digit month value between 01 to 12            |
| MMM            | day of week                                       |
| DD             | two-digit day of month between 01 to 31           |
| HH24           | two-digit hour value between 00 to 23             |
| HH12           | two-digit hour value between 0 to 12              |
| HH             | two-digit hour value between 0 to 12              |
| MI             | two-digit minute value between 00 to 59           |
| SS             | two-digit seconds value between 0 and 59          |
| AM             | AM/PM                                             |
| nnn...         | 1 to 9 digits fractions of a second               |

```js {linenos=table,hl_lines=["6"],linenostart=1}
FAKE( json({
    [ 1701345032123456789, 10],
    [ 1701345043219876543, 11]
}))
MAPVALUE(0, time(value(0)) )
CSV( sqlTimeformat("YYYY-MM-DD HH24:MI:SS.nnnnnn"), tz("Asia/Seoul") )
```

```
2023-11-30 20:50:32.123456,10
2023-11-30 20:50:43.219876,11
```

### ansiTimeformat()

*Syntax*: `ansiTimeformat( format )`

- `format` *string*

```js {linenos=table,hl_lines=["6"],linenostart=1}
FAKE( json({
    [ 1701345032123456789, 10],
    [ 1701345043219876543, 11]
}))
MAPVALUE(0, time(value(0)) )
CSV( ansiTimeformat("yyyy-mm-dd hh:nn:ss.ffffff"), tz("UTC"))
```

```
2023-11-30 11:50:32.123456,10
2023-11-30 11:50:43.219876,11
```

| format         | result of timeformatting                          |
|:---------------|:------------------------------------------------- |
| yyyy           | four-digit year value                             |
| mm             | two-digit month value between 01 to 12            |
| dd             | two-digit day value between 01 to 31              |
| hh             | two-digit hour value between 00 to 23             |
| nn             | two-digit minute value between 00 to 59           |
| ss             | two-digit seconds value between 0 and 59          |
| fff...         | 1 to 9 digits fractions of a second               |

## Math

Mathematical functions. {{< neo_since ver="8.0.6" />}}

> This functions does not guarantee bit-identical results across system architectures.

| function         | description                         |
|:---------------- | :---------------------------------- |
| `abs(x)`         | the absolute value of x.            |
| `acos(x)`        | the arccosine, in radians, of x.    |
| `acosh(x)`       | the inverse hyperbolic cosine of x. |
| `asin(x)`        | the arcsine, in radians, of x.      |
| `asinh(x)`       | the inverse hyperbolic sine of x.   |
| `atan(x)`        | the arctangent, in radians, of x.   |
| `atanh(x)`       | the inverse hyperbolic tangent of x. |
| `ceil(x)`        | the least integer value greater than or equal to x.|
| `cos(x)`         | the cosine of the radian argument x. |
| `cosh(x)`        | the hyperbolic cosine of x.          |
| `exp(x)`         | e**x, the base-e exponential of x.   |
| `exp2(x)`        | 2**x, the base-2 exponential of x.   |
| `floor(x)`       | the greatest integer value less than or equal to x. |
| `log(x)`         | the natural logarithm of x.          |
| `log2(x)`        | the binary logarithm of x. The special cases are the same as for log. |
| `log10(x)`       | the decimal logarithm of x. The special cases are the same as for log. |
| `max(x,y)`       | the larger of x or y.                |
| `min(x,y)`       | the smaller of x or y.               |
| `mod(x,y)`       | the floating-point remainder of x/y.<br/>The magnitude of the result is less than y and its sign agrees with that of x. |
| `pow(x, y)`      | x**y, the base-x exponential of y.   |
| `pow10(x)`       | 10**x, the base-10 exponential of n. |
| `remainder(x,y)` | the IEEE 754 floating-point remainder of x/y. |
| `round(x)`       | the nearest integer, rounding half away from zero.  |
| `sin(x)`         | the sine of the radian argument x.   |
| `sinh(x)`        | the hyperbolic sine of x.            |
| `sqrt(x)`        | the square root of x.                |
| `tan(x)`         | the tangent of the radian argument x. |
| `tanh(x)`        | the hyperbolic tangent of x.          |
| `trunc(x)`       | the integer value of x.               |

An example usage of math functions with `MAPVALUE`.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js {linenos=table,hl_lines=["3"],linenostart=1}
FAKE(meshgrid(linspace(-4,4,100), linspace(-4,4, 100)))
MAPVALUE(2,
    sin(pow(value(0), 2) + pow(value(1), 2)) / (pow(value(0), 2) + pow(value(1), 2))
)
MAPVALUE(0, list(value(0), value(1), value(2)))
POPVALUE(1, 2)
CHART(
    plugins("gl"),
    size("600px", "600px"),
    chartOption({
        grid3D:{},
        xAxis3D:{},
        yAxis3D:{},
        zAxis3D:{},
        series:[
            {type: "line3D", data: column(0)},
        ]
    })
)
```
{{< /tab >}}
{{< tab >}}

{{< /tab >}}
{{< /tabs >}}

### random()

*Syntax*: `random() : number` {{< neo_since ver="8.0.7" />}}

`random()` returns a float, a pseudo-random number in the half-open interval [0.0,1.0).

### simplex()

*Syntax*: `simplex(seed, dim1 [, dim2 [, dim3 [, dim4]]]) : number` {{< neo_since ver="8.0.7" />}}

- `seed` *int* seed number
- `dim1` ~ `dim4` *float number*

`simplex()` returns SimpleX noise([wikipedia](https://en.wikipedia.org/wiki/Simplex_noise)) by given seed and dimension values.

{{< tabs items="CODE,RESULT">}}
{{< tab >}}
```js {linenos=table,hl_lines=["6"],linenostart=1}
FAKE(
    meshgrid(
        linspace(0, 10, 100), linspace(0, 10, 100)
    )
)
MAPVALUE(2, abs( simplex(123, value(0), value(1)) ) * 10)
MAPVALUE(0, list(value(0), value(1), value(2)))
CHART(
    plugins("gl"),
    size("600px", "600px"),
    chartOption({
        visualMap: {
            max: 8,
            inRange:{ color:[ 
                    "#313695", "#74add1", "#e0f3f8",
                    "#fee090",  "#f46d43", "#a50026"]}
        },
        grid3D:{ boxWidth:100, boxDepth:100, boxHeight:20},
        xAxis3D:{}, yAxis3D:{}, zAxis3D:{},
        series:[
            {type: "bar3D", data: column(0), itemStyle:{opacity:1.0}},
        ]
    })
)
```
{{< /tab >}}
{{< tab >}}

{{< /tab >}}
{{< /tabs >}}

## List

### count()

*Syntax*: `count( array|tuple ) : number`

Returns the number of the elements.

### list()

*Syntax*: `list(args...) : list` {{< neo_since ver="8.0.7" />}}

`list()` returns a new tuple that contains the `args` as its elements.

### dict()

*Syntax*: `dict( name1, value1 [, name2, value2 ...]) : dictionary` {{< neo_since ver="8.0.8" />}}

`dict()` returns a new dictionary that contains pairs of name*n*:value*n*.
