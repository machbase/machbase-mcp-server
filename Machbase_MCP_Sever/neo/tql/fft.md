---
title: FFT()
type: docs
weight: 70
---

## Fast Fourier Transform

{{< callout emoji="📌" >}}
For smooth practice, the following query should be run to prepare tables and data.
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
```

## Generates sample data

Open a new *tql* editor on the web ui and copy the code below and run it.

In this example, `oscillator()` generates a composite wave of 15Hz 1.0 + 24Hz 1.5.
And `CHART_SCATTER()` has `dataZoom()` option function that provides an slider under the x-Axis.

```js {linenos=table,hl_lines=["2-5"],linenostart=1}
FAKE( 
  oscillator(
    freq(15, 1.0), freq(24, 1.5),
    range('now', '10s', '1ms')
  )
)
CHART_SCATTER( size("600px", "350px"), dataZoom('slider', 95, 100) )
```

## Store data into database

Store the generated data into the database with the tag name 'signal'.

```js {linenos=table,hl_lines=["10"],linenostart=1}
FAKE(
  oscillator(
    freq(15, 1.0), freq(24, 1.5),
    range('now', '10s', '1ms')
  )
)
// |    0      1
// +--> time   magnitude
// |
INSERT( 'time', 'value', table('example'), tag('signal') )
```

It will show "10000 rows inserted." message in the "Result" pane.

For a comment, it took about *270ms* in a test machine (Apple mac mini M1), but using `APPEND()` method in the example below, took *65ms* (x4 faster).

```js {linenos=table,hl_lines=["14"],linenostart=1}
FAKE(
  oscillator(
    freq(15, 1.0), freq(24, 1.5),
    range('now', '10s', '1ms')
  )
)
// |    0      1
// +--> time   magnitude
// |
PUSHVALUE(0,'signal')
// |    0         1      2
// +--> 'signal' time   magnitude
// |
APPEND( table('example') )
```

{{< callout type="warning" >}}
The 'APPEND' works only when fields of input records exactly match with columns of the table in order and types.
{{< /callout >}}

## Read data from database

The code below reads the stored data from the 'example' table.

```js
SQL_SELECT('time', 'value', from('example', 'signal'), between('last-10s', 'last'))
CHART_LINE( size("600px", "350px"), dataZoom('slider', 95, 100))
```

## Fast Fourier Transform

Add few data manipulation function between `SQL_SELECT()` source and `CHART_LINE()` sink.

{{< tabs items="GROUPBYKEY,SCRIPT">}}
{{< tab >}}
```js {linenos=table,hl_lines=["2-4"],linenostart=1}
SQL_SELECT('time', 'value', from('example', 'signal'), between('last-10s', 'last'))
MAPKEY('sample')
GROUPBYKEY()
FFT()
CHART_LINE(
  size("600px", "350px"), 
  xAxis(0, 'Hz'),
  yAxis(1, 'Amplitude'),
  dataZoom('slider', 0, 10) 
)
```
{{< /tab >}}
{{< tab >}}

```js {linenos=table,hl_lines=[10,12],linenostart=1}
SQL_SELECT('time', 'value', from('example', 'signal'), between('last-10s', 'last'))
SCRIPT({
    var list = [];
    function finalize() {
        $.yield(list);
    }
},{
    ts = $.values[0];
    val = $.values[1];
    list.push([ts, val]);
})
FFT()
CHART_LINE(
  size("600px", "350px"), 
  xAxis(0, 'Hz'),
  yAxis(1, 'Amplitude'),
  dataZoom('slider', 0, 10) 
)
```
{{< /tab >}}
{{< /tabs >}}

## How it works

{{% steps %}}

### SQL_SELECT()
`SQL_SELECT(...)` yields records from the query result in the form of `{key: rownum, value: (time, value) }`

### MAPKEY('sample')
`MAPKEY('sample')` sets the constant string 'sample' as a new key for all records.
As result all records have same *key* `'sample'` and `(time, value)` as *value*. `{key: 'sample', value:(time, value)}`

### GROUPBYKEY()
`GROUPBYKEY()` merge all records that has the same key. In this example, all query results are combined into a record that has same *key* 'sample' and value is an array of tuples which formed `{key: 'sample', value:[ (time1, value1), (time2, value2), ..., (timeN, valueN) ]}`.

### FFT()
`FFT()` applies Fast Fourier Transform on the value of the record and transform the value (time-value) into an array of tuples (frequency-amplitude). `{key: 'sample', value:[ (Hz1, Ampl1), (Hz2, Ampl2), ... ]}`.

{{% /steps %}}

## Adding time axis

```js {linenos=table,hl_lines=["3-7"],linenostart=1}
SQL_SELECT( 'time', 'value', from('example', 'signal'), between('last-10s', 'last'))

MAPKEY( roundTime(value(0), '500ms') )
GROUPBYKEY()
FFT(minHz(0), maxHz(100))
FLATTEN()
PUSHKEY('fft')
CHART_BAR3D(
      xAxis(0, 'time', 'time'),
      yAxis(1, 'Hz'),
      zAxis(2, 'Amp'),
      size('600px', '600px'), visualMap(0, 1.5), theme('westeros')
)
```

## How it works

{{% steps %}}

### SQL_SELECT()

`SQL_SELECT(...)` yields records from the query result. `{key: time, value: (value) }`

### MAPKEY()
`MAPKEY( roundTime(value(0), '500ms'))` sets the new key with the result of roundTime `value(0)` by 500 milliseconds. 
As result the records are transformed into `{key: (time/500ms)*500ms, value:(time, value)}`

### GROUPBYKEY()
`GROUPBYKEY()` makes records grouped in every 500ms. `{key: time1In500ms, value:[(time1, value1), (time2, value2)...]}`

### FFT()
`FFT()` applies Fast Fourier Transform for each record. The optional functions `minHz(0)` and `maxHz(100)` limits the scope of the output just for the better visualization. `{key:time1In500ms, value:[(Hz1, Ampl1), ...]}`, `{key:'time2In500ms', value:[(Hz1, Ampl1), ...]}`, ...

### FLATTEN()
`FLATTEN()` reduces the dimension of the value array by splitting into multiple records. As result it yields.

### PUSHKEY()
`PUSHKEY('fft')` sets the constant string 'fft' as new key for all records. and the previous key will be "pushed" into the first place of value array. `{key:'fft', value:(time1In500ms, Hz1, Ampl1)}`, `{key:'fft', value:(time1In500ms, Hz2, Ampl2)}`...

{{% /steps %}}

