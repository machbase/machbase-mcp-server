---
title: Glance at TQL
type: docs
weight: 01
---

Machbase-neo supports Transforming Query Language (TQL) and execution API.

As application developers, we typically follow a similar approach to build applications that utilize databases.
The process usually starts with querying the database and retrieving data in a tabular form (rows and columns).
This data is then converted into the desired data structure, manipulated, and displayed in the required formats such as JSON, CSV, or charts.

TQL simplifies this process with just a few lines of script.
Additionally, other applications can interact with TQL via HTTP endpoints, treating it as an executable API.

## What is TQL
TQL (Transforming Query Language) is a domain-specific language (DSL) for data manipulation.
It defines a flow of data streams, where each individual data unit is a record.
A record has a *key* and a *value*.
The key is generally an auto-generated sequential integer,
similar to *ROWNUM* in query results.
The value is a tuple that contains the actual data fields.

![tql_records](../img/tql_records.jpg)

TQL scripts start with *SRC* (source) functions that define how to retrieve data and generate records by transforming the raw data.
The script ends with *SINK* functions, which define how to output the records.
Between *SRC* and *SINK*, you can use *MAP* functions to transform the data as needed.

![tql_flow_min](../img/tql_flow_min.jpg)

In some cases, a TQL script needs to transform records, involving mathematical calculations, simple string concatenations,
or interactions with external databases. These tasks can be defined using *MAP* functions.

Thus, a TQL script should start with *SRC* functions and end with *SINK* functions.
It can include zero or more *MAP* functions in between to perform the necessary transformations.

![tql_flow](../img/tql_flow.jpg)

### SRC

There are several SRC functions available in TQL.
For example, the `SQL()` function produces records by querying the Machbase-neo database or even external (bridged) databases using the given SQL statement.
The `FAKE()` function generates artificial data for testing purposes.
The `CSV()` function reads data from CSV files,
while the `BYTES()` function reads arbitrary binary data from the file system, client's HTTP request, or MQTT payload.

![tql_src](../img/tql_src.jpg)

### SINK

The basic SINK functions include `INSERT()`, which writes the incoming records to the Machbase-neo database,
and `CHART()`, which renders a chart with the incoming records.
Additionally, `JSON()` and `CSV()` functions encode the incoming data into their respective formats,
making it easier to integrate with other applications or display the data in a user-friendly manner.

![tql_sink](../img/tql_sink.jpg)

### MAP

*MAP* functions are essential for transforming data from one shape to another.
They allow you to perform various operations such as mathematical calculations, string manipulations, and data format conversions.
By using *MAP* functions, you can efficiently process and reshape your data to meet the specific requirements of your application.

![tql_map](../img/tql_map.jpg)

## Run TQL

{{% steps %}}

### Open Web UI

Open the Machbase-neo web UI in your web browser.
The default address is `http://127.0.0.1:5654/`.
Use the username `sys` and the password `manager`.

### New TQL Page

Select "TQL" on the 'New...' page.
<br/>

### Copy the code and run

Copy and paste the sample TQL code into the TQL editor.

Then click the ▶︎ icon on the top left of the editor.
It will display a line chart as shown in the image below, representing a wave with a frequency of 1.5 Hz and an amplitude of 1.0.

{{% /steps %}}

{{< tabs items="SCATTER,LINE,BAR">}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_SCATTER()
```

{{< /tab >}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_LINE()
```

{{< /tab >}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_BAR()
```

{{< /tab >}}
{{< /tabs >}}

Let's explore some data formats like CSV and JSON.

- **CSV Format**: This format is useful for exporting data to spreadsheets or other applications that support CSV files.
- **JSON Format**: This format is ideal for web applications and APIs, as it is easy to parse and integrate with JavaScript.

By using TQL, you can easily convert your data into these formats with just a few lines of code.

{{< tabs items="JSON-rows,JSON-cols,CSV,MARKDOWN,HTML">}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
JSON()
```

{{< /tab >}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
JSON( transpose(true) )
```

{{< /tab >}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CSV()
```

{{< /tab >}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
MARKDOWN()
```

{{< /tab >}}
{{< tab >}}
```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
MARKDOWN( html(true) )
```

{{< /tab >}}
{{< /tabs >}}

## TQL as API

Save this code as `hello.tql` by clicking the save icon at the top right corner of the editor.
You can then access it through your web browser at [http://127.0.0.1:5654/db/tql/hello.tql](http://127.0.0.1:5654/db/tql/hello.tql),
or use the *curl* command in the terminal to retrieve the data.

| Icon      | Description |
|-----------|:------------|
|  | When a TQL script is saved, the editor displays a link icon at the top right corner. Click this icon to copy the address of the script file. |

```sh
curl -o - http://127.0.0.1:5654/db/tql/hello.tql
```

```sh
$ curl -o - -v http://127.0.0.1:5654/db/tql/hello.tql
...omit...
>
< HTTP/1.1 200 OK
< Content-Type: text/csv
< Transfer-Encoding: chunked
<
1686787739025518000,-0.238191
1686787739035518000,-0.328532
1686787739045518000,-0.415960
1686787739055518000,-0.499692
1686787739065518000,-0.578992
...omit...
```

### JSON()

Let's try to change `CSV()` to `JSON()`, save and execute again.
    

And invoke the hello.tql with `curl` from terminal.

```sh
$ curl -o - -v http://127.0.0.1:5654/db/tql/hello.tql
...omit...
< HTTP/1.1 200 OK
< Content-Type: application/json
< Transfer-Encoding: chunked
<
{
"data": {
    "columns": [ "time", "value" ],
    "types": [ "datetime", "double" ],
    "rows": [
    [ 1686788907538618000, 0.9344920354538058 ],
    [ 1686788907548618000, 0.8968436523101743 ],
    ...omit...
},
"success": true,
"reason": "success",
"elapse": "956.291µs"
}
```

### JSON() with transpose()

If you are developing a data visualization application,
it is helpful to know that TQL's JSON output supports transposing the result into columns instead of rows.
By applying `JSON( transpose(true) )` and invoking it again, the resulting JSON will contain a `cols` array.

```sh
$ curl -o - -v http://127.0.0.1:5654/db/tql/hello.tql
...omit...
< HTTP/1.1 200 OK
< Content-Type: application/json
< Transfer-Encoding: chunked
<
{
"data": {
    "columns": [ "time", "value" ],
    "types": [ "datetime", "double" ],
    "cols": [
        [ 1686789517241103000, ...omit..., 1686789520231103000],
        [ -0.7638449771082523, ...omit..., 0.8211935584502427]
    ]
},
"success": true,
"reason": "success",
"elapse": "1.208166ms"
}
```

This feature is the simplest way for developers to create RESTful APIs, allowing other applications to access data seamlessly.

### INSERT

Change `CSV()` to `INSERT("time", "value", table("example"), tag("temperature"))` and execute again.

### Select Table

```js
SQL('select * from tag limit 10')
CSV()
```

