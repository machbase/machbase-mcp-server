---
title: TQL
type: docs
weight: 70
---
Transforming Query Language
It is required to properly read and transform data that has been sent by sensors.
And also read and send data from database to other systems in demanded format.

### Output format independent

{{< tabs items="CSV,JSON,CHART,HTML">}}
{{< tab >}}
```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `SELECT TIME, VALUE FROM EXAMPLE WHERE NAME='signal' LIMIT 100` )
CSV( timeformat("Default") )
```

{{</ tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=[2],linenostart=1}
SQL( `SELECT TIME, VALUE FROM EXAMPLE WHERE NAME='signal' LIMIT 100` )
JSON( timeformat("Default") )
```

{{</ tab >}}
{{< tab >}}
```js {linenos=table,hl_lines=[2-9],linenostart=1}
SQL( `SELECT TIME, VALUE FROM EXAMPLE WHERE NAME='signal' LIMIT 100` )
CHART(
    size("600px", "340px"),
    chartOption({
        xAxis:{data:column(0)},
        yAxis:{},
        series:[ { type:"line", data:column(1)} ]
    })
)
```

{{</ tab >}}
{{< tab >}}
```html {linenos=table,hl_lines=[2],linenostart=1}
SQL(`SELECT TIME, VALUE FROM EXAMPLE WHERE NAME='signal' LIMIT 100`)
HTML({
  {{if .IsFirst }}
    <table>
    <tr>
        <th>TIME</th><th>VALUE</th>
    </tr>
  {{end}}
    <tr>
        <td>{{.V.TIME}}</td><td>{{.V.VALUE}}</td>
    </tr>
  {{if .IsLast }}
    </table>
  {{end}}
})
```

{{</ tab >}}
{{</ tabs >}}

### Data source independent

{{< tabs items="JSON,CSV,SQL,SCRIPT-json,SCRIPT-for">}}
{{< tab >}}
```js {{linenos="table",hl_lines=["1-5"]}}
FAKE( json({ 
    [ "A", 1.0 ],
    [ "B", 1.5 ],
    [ "C", 2.0 ],
    [ "D", 2.5 ] }))

MAPVALUE(1, value(1) * 10 )

CSV()
```
{{</ tab >}}
{{< tab >}}
```js {{linenos="table",hl_lines=["1-4"]}}
CSV(`A,1.0
B,1.5
C,2.0
D,2.5`, field(1, floatType(), "value"))

MAPVALUE(1, value(1) * 10 )

CSV()
```
{{</ tab >}}
{{< tab >}}
```js  {{linenos="table",hl_lines=[1]}}
SQL(`select time, value from example where name = 'my-car' limit 4`)

MAPVALUE(1, value(1) * 10 )

CSV()
```
{{</ tab >}}
{{< tab >}}
```js {{linenos="table",hl_lines=[2]}}
SCRIPT({
    list = JSON.parse(`[["A",1.0], ["B",1.5], ["C",2.0], ["D",2.5]]`);
    for( v of list) {
        $.yield(v[0], v[1])
    }
})
MAPVALUE(1, value(1) * 10 )
CSV()
```
{{</ tab >}}
{{< tab >}}
```js {{linenos="table",hl_lines=["1-5"]}}
SCRIPT({
    for (i = 0; i < 10; i++) {
        $.yield("script", Math.random())
    }
})

MAPVALUE(1, value(1) * 10 )

CSV()
{{</ tab >}}
{{</ tabs >}}

The purpose of *TQL* is transforming data format.
This chapter shows how to do this without developing additional applications.

### N:M transforming

### Iris

The example tql code below gives a brief idea of what is TQL for.

{{< tabs items="AVG,STAT,SCRIPT-bar,SCRIPT-boxplot">}}
{{< tab >}}

- avg. values of each classes.

```js {{linenos="table"}}
CSV(file("https://docs.machbase.com/assets/example/iris.csv"))
GROUP( by(value(4), "species"),
    avg(value(0), "Avg. Sepal L."),
    avg(value(1), "Avg. Sepal W."),
    avg(value(2), "Avg. Petal L."),
    avg(value(3), "Avg. Petal W.")
)
CHART(
    chartOption({
        "xAxis":{"type": "category", "data": column(0)},
        "yAxis": {},
        "legend": {"show": true},
        "series": [
            { "type": "bar", "name": "Avg. Sepal L.", "data": column(1)},
            { "type": "bar", "name": "Avg. Sepal W.", "data": column(2)},
            { "type": "bar", "name": "Avg. Petal L.", "data": column(3)},
            { "type": "bar", "name": "Avg. Petal W.", "data": column(4)}
        ]
    })
)
```

{{</ tab >}}
{{< tab >}}

- min, median, avg, max, stddev of sepal length of the setosa class.

```js {{linenos="table"}}
CSV(file("https://docs.machbase.com/assets/example/iris.csv"))
FILTER( strToUpper(value(4)) == "IRIS-SETOSA")
GROUP( by(value(4)), 
    min(value(0), "Min"),
    median(value(0), "Median"),
    avg(value(0), "Avg"),
    max(value(0), "Max"),
    stddev(value(0), "StdDev.")
)
CHART(
    chartOption({
        "xAxis": { "type": "category", "data": ["iris-setosa"]},
        "yAxis": {},
        "legend": {"show": "true"},
        "series": [
            {"type":"bar", "name": "Min", "data": column(1)},
            {"type":"bar", "name": "Median", "data": column(2)},
            {"type":"bar", "name": "Avg", "data": column(3)},
            {"type":"bar", "name": "Max", "data": column(4)},
            {"type":"bar", "name": "StdDev.", "data": column(5)}
        ]
    })
)
```

{{</ tab >}}

{{<tab>}}

```js {{linenos="table"}}
CSV(file("https://docs.machbase.com/assets/example/iris.csv"))
SCRIPT({
    var board = {};
},{
    species = $.values[4];
    o = board[species];
    if(o === undefined) {
        o = {
            sepalLength: [],
            sepalWidth: [],
            petalLength: [],
            petalWidth: [],
        };
        board[species] = o;
    }
    o.sepalLength.push(parseFloat($.values[0]));
    o.sepalWidth.push(parseFloat($.values[1]));
    o.petalLength.push(parseFloat($.values[2]));
    o.petalWidth.push(parseFloat($.values[3]))
},{
    chart = {
        xAxis: {type: "category", data:[]},
        yAxis: {},
        legend: {show:true},
        series: [
            {type: "bar", name: "min. sepal L.", data:[]},
            {type: "bar", name: "max. sepal L.", data:[]},
            {type: "bar", name: "min. sepal W.", data:[]},
            {type: "bar", name: "max. sepal W.", data:[]},
            {type: "bar", name: "min. petal L.", data:[]},
            {type: "bar", name: "max. petal L.", data:[]},
            {type: "bar", name: "min. petal W.", data:[]},
            {type: "bar", name: "max. petal W.", data:[]},
        ],
    };
    for( s in board) {
        o = board[s];
        chart.xAxis.data.push(s);
        chart.series[0].data.push(Math.min(...o.sepalLength));
        chart.series[1].data.push(Math.max(...o.sepalLength));
        chart.series[2].data.push(Math.min(...o.sepalWidth));
        chart.series[3].data.push(Math.max(...o.sepalWidth));
        chart.series[4].data.push(Math.min(...o.petalLength));
        chart.series[5].data.push(Math.max(...o.petalLength));
        chart.series[6].data.push(Math.min(...o.petalWidth));
        chart.series[7].data.push(Math.max(...o.petalWidth));
    }
    $.yield(chart);
})
CHART()
```

{{</tab>}}
{{<tab>}}

```js {{linenos="table"}}
CSV(file("https://docs.machbase.com/assets/example/iris.csv"))
SCRIPT({
    var board = {};
},{
    species = $.values[4];
    o = board[species];
    if(o === undefined) {
        o = {
            sepalLength: [],
            sepalWidth: [],
            petalLength: [],
            petalWidth: [],
        };
        board[species] = o;
    }
    o.sepalLength.push(parseFloat($.values[0]));
    o.sepalWidth.push(parseFloat($.values[1]));
    o.petalLength.push(parseFloat($.values[2]));
    o.petalWidth.push(parseFloat($.values[3]))
},{
    chart = {
        title: {text: "Iris Sepal/Petal Length", left: "center"},
        grid: {bottom: "10%"},
        xAxis: {type: "category", data:[], boundaryGap: true},
        yAxis: {type: "value", splitArea:{show:true}},
        legend: {show:true, bottom:"2%"},
        tooltip: {trigger: "item", axisPointer:{type:"shadow"}},
        series: [
            {type: "boxplot", name: "sepal length", data:[]},
            {type: "boxplot", name: "petal length", data:[]},
        ],
    };
    const ana = require("@jsh/analysis");
    for( s in board) {
        o = board[s];
        chart.xAxis.data.push(s);
        // sepal length
        o.sepalLength = ana.sort(o.sepalLength)
        min = Math.min(...o.sepalLength);
        max = Math.max(...o.sepalLength);
        q1 = ana.quantile(0.25, o.sepalLength);
        q2 = ana.quantile(0.5, o.sepalLength);
        q3 = ana.quantile(0.75, o.sepalLength);
        chart.series[0].data.push([min, q1, q2, q3, max]);
        // petal length
        o.petalLength = ana.sort(o.petalLength)
        min = Math.min(...o.petalLength);
        max = Math.max(...o.petalLength);
        q1 = ana.quantile(0.25, o.petalLength);
        q2 = ana.quantile(0.5, o.petalLength);
        q3 = ana.quantile(0.75, o.petalLength);
        chart.series[1].data.push([min, q1, q2, q3, max]);
    }
    $.yield(chart);
})
CHART()
```

{{</tab>}}
{{</ tabs >}}

## In this chapter

{{< children_toc />}}
