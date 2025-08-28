---
title: Basic Line Chart
type: docs
weight: 10
---

## SRC :: FAKE()

```js {linenos=table,linenostart=1}
FAKE( linspace(0, 360, 100))
// |   0
// +-> x
// |
MAPVALUE(1, sin((value(0)/180)*PI))
// |   0   1
// +-> x   sin(x)
// |
CHART(
    chartOption({
        xAxis: {
            type: "category",
            data: column(0)
        },
        yAxis: {},
        series: [
            {
                type: "line",
                data: column(1)
            }
        ]
    })
)
```

## SRC :: SCRIPT()

```js {linenos=table,linenostart=1}
SCRIPT({
    for( x = 0; x < 360; x+=3.6) {
        $.yield(x, Math.sin(x/180*Math.PI));
    }
})
CHART(
    chartOption({
        xAxis: {
            type: "category",
            data: column(0)
        },
        yAxis: {},
        series: [
            {
                type: "line",
                data: column(1)
            }
        ]
    })
)
```

## SRC :: SQL()

### Prepare data

```js {linenos=table,linenostart=1}
FAKE( arrange(1, 100, 1))
// |   0
// +-> seq
// |
MAPVALUE(1, sin((2*PI*value(0)/100)))
// |   0       1
// +-> seq     value
// |
MAPVALUE(0, timeAdd("now-100s", strSprintf("+%.fs", value(0))))
// |   0       1
// +-> time    value
// |
PUSHVALUE(0, "chart-line")
// |   0       1       2
// +-> name    time    value
// |
APPEND(table("example"))
```

### Prepare data with SCRIPT

```js {linenos=table,linenostart=1}
SCRIPT({
    const gen = require("@jsh/generator");
    const sys = require("@jsh/system");
    ts = (new Date()).getTime() - 100 * 1000; // now - 100s.
    for(x of gen.arrange(1, 100, 1)) {
        y = Math.sin(x/100*2*Math.PI)
        ts += 1000; // add 1 sec.
        $.yield("chart-line", sys.parseTime(ts, "ms"), y);
    }
})
APPEND(table("example"))
```

### SQL() to CHART()

```js {linenos=table,hl_lines=[4,10],linenostart=1}
SQL(`select time, value from example where name = 'chart-line'`)
SCRIPT({
    $.yield([$.values[0], $.values[1]])
})
CHART(
    chartOption({
        xAxis: { type: "time" },
        yAxis: {},
        tooltip: { trigger:"axis" },
        series: [
            {
                type: "line",
                data: column(0)
            }
        ]
    })
)
```

### SCRIPT() to CHART()

```js {{linenos=table,linenostart=1}}
SCRIPT({
    db = require("@jsh/db");
    cli = new db.Client();
    conn = cli.connect();
    rows = conn.query(`select time, value from example where name = 'chart-line'`)
    data = [];
    for( r of rows) {
        data.push([r.time, r.value]);
    }
    rows.close();
    conn.close();
    $.yield({
        xAxis: { type: "time" },
        yAxis: {},
        tooltip: { trigger:"axis" },
        series: [
            {
                type: "line",
                data: data,
            }
        ]
    })
})
CHART()
```

```html {{linenos=table,linenostart=1}}
SQL(`select time, value from example where name = 'chart-line'`)
SCRIPT({
    data = [];
}, {
    data.push([$.values[0], $.values[1]]);
}, {
    $.yield(data); 
})
HTML(template({
    <span>
        <script src="/web/echarts/echarts.min.js"></script>
        <div id='xyz' style="width:600px;height:400px;"></div>
        <script>
            var data = {{ .Values }};
            var chartDom = document.getElementById('xyz');
            var myChart = echarts.init(chartDom);
            var option = {
                xAxis: { type: "time" },
                yAxis: {},
                tooltip: { trigger:"axis" },
                series: [
                    {type: 'line',  data: data, symbol:"none"}
                ]
            };
            option && myChart.setOption(option);
        </script>
    </span>
}))
```