---
title: Basic Mix
type: docs
weight: 900
---

```js {{linenos=table,linenostart=1}}
FAKE( linspace(0, 360, 50))
MAPVALUE(1, sin((value(0)/180)*PI))
MAPVALUE(2, cos((value(0)/180)*PI))
CHART(
    chartOption({
        xAxis: { data: column(0) },
        yAxis: {},
        series: [
            {type: "bar", name: "SIN", data: column(1)},
            {type: "line", name: "COS", color:"#093", data: column(2)}
        ]
    })
)
```

