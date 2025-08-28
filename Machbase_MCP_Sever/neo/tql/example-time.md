---
title: Time examples
type: docs
weight: 100
---

{{< callout emoji="📌" >}}
For smooth practice, the following query should be run to prepare tables and data.
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-12 12:00:00 123:456:789'), 10);
INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-13 12:00:00 123:456:789'), 11);
```


TQL supports several `Time` manipulation functions.

## Time function

### Now

`time("now")` returns the current time.

```js
SQL(`select to_char(time), value from example where time < ?`, time('now'))
CSV()
```

`result`

```
2021-08-12 12:00:00 123:456:789,10
2021-08-13 12:00:00 123:456:789,11
```

### Timestamp

`time(epoch)`  returns time that represents in UNIX epoch in nano-seconds.

```js
SQL(`select to_char(time), value from example where time = ?`, time(1628737200123456789))
CSV()
```


## Time manipulation

TQL can be used to facilitate conversion between `Timestamp` and `Time format string`.

### Timestamp to Time format string

Copy the code below into TQL editor and save `time_to_format.tql`.

```js
STRING(param("format_time") ?? "808210800", separator('\n'))
SCRIPT({
    epoch = parseInt($.values[0])
    time = new Date(epoch*1000)
    $.yield(epoch, time.toISOString())
})
CSV()
```

[http://127.0.0.1:5654/db/tql/time_to_format.tql?format_time=808210800000000001](http://127.0.0.1:5654/db/tql/time_to_format.tql?format_time=808185601)

### Time format string to Timestamp

Copy the code below into TQL editor and save `format_to_time.tql`.

```js
STRING(param("timestamp") ?? "1995-08-12T00:00:00.000Z", separator('\n'))
SCRIPT({
    ts = new Date(Date.parse($.values[0]));
    epoch = ts.getTime() / 1000;
    $.yield(epoch, ts.toISOString())
})
CSV()
```

`http://127.0.0.1:5654/db/tql/format_to_time.tql?timestamp=1995-08-12T00:00:00.000Z`


## Format

It specifies how to represents time in output.

### None

```js
SQL(`select to_char(time), time from example`)
CSV()
```

`result`

```
2021-08-12 12:00:00 123:456:789,1628737200123456789
2021-08-13 12:00:00 123:456:789,1628823600123456789
```

### Default

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('DEFAULT'))
```

`result`

```
2021-08-12 12:00:00 123:456:789,2021-08-12 03:00:00.123
2021-08-13 12:00:00 123:456:789,2021-08-13 03:00:00.123
```
#### Additional Default Types
| Type     |  Description  |
|:-----------------|:-------------|
|DEFAULT_MS | 2006-01-02 15:04:05.999|
|DEFAULT_US | 2006-01-02 15:04:05.999999|
|DEFAULT_NS | 2006-01-02 15:04:05.999999999|
|DEFAULT.MS | 2006-01-02 15:04:05.000|
|DEFAULT.US | 2006-01-02 15:04:05.000000|
|DEFAULT.NS | 2006-01-02 15:04:05.000000000|

### Numeric

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('NUMERIC'))
```

`result`

```
2021-08-12 12:00:00 123:456:789,08/12 03:00:00AM '21 +0000
2021-08-13 12:00:00 123:456:789,08/13 03:00:00AM '21 +0000
```

### Ansic

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('ANSIC'))
```

`result`

```
2021-08-12 12:00:00 123:456:789,Thu Aug 12 03:00:00 2021
2021-08-13 12:00:00 123:456:789,Fri Aug 13 03:00:00 2021
```

### Unix

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('NUMERIC'))
```

`result`

```
2021-08-12 12:00:00 123:456:789,Thu Aug 12 03:00:00 UTC 2021
2021-08-13 12:00:00 123:456:789,Fri Aug 13 03:00:00 UTC 2021
```

### RFC822

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('RFC822'))
```

`result`

```
2021-08-12 12:00:00 123:456:789,12 Aug 21 03:00 UTC
2021-08-13 12:00:00 123:456:789,13 Aug 21 03:00 UTC
```

### RFC3339

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('RFC3339'))
```

`result`

```
2021-08-12 12:00:00 123:456:789,2021-08-12T03:00:00Z
2021-08-13 12:00:00 123:456:789,2021-08-13T03:00:00Z
```

## Timezone

The `tz` function specifies time zone.

### Local

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('DEFAULT'), tz('local'))
```

`result`

```
2021-08-12 12:00:00 123:456:789,2021-08-12 12:00:00.123
2021-08-13 12:00:00 123:456:789,2021-08-13 12:00:00.123
```

### UTC

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('DEFAULT'), tz('UTC'))
```

`result`

```
2021-08-12 12:00:00 123:456:789,2021-08-12 03:00:00.123
2021-08-13 12:00:00 123:456:789,2021-08-13 03:00:00.123
```

### Seoul

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('DEFAULT'), tz('Asia/Seoul'))
```

`result`

```
2021-08-12 12:00:00 123:456:789,2021-08-12 12:00:00.123
2021-08-13 12:00:00 123:456:789,2021-08-13 12:00:00.123
```

### EST

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('DEFAULT'), tz('EST'))
```

`result`

```
2021-08-12 12:00:00 123:456:789,2021-08-11 22:00:00.123
2021-08-13 12:00:00 123:456:789,2021-08-12 22:00:00.123
```

### Paris

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('DEFAULT'), tz('Europe/Paris'))
```

`result`

```
2021-08-12 12:00:00 123:456:789,2021-08-12 05:00:00.123
2021-08-13 12:00:00 123:456:789,2021-08-13 05:00:00.123
```
