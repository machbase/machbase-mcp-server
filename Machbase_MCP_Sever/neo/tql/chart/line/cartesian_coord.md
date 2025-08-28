---
title: Cartesian Coordinate System
type: docs
weight: 70
---

```js {{linenos=table,linenostart=1}}
FAKE(json({
    [10, 40],
    [50, 100],
    [40, 20]
}))
MAPVALUE(0, list(value(0), value(1)))
POPVALUE(1)
CHART(
    chartOption({
        title: { text: "Line Chart in Cartesian Coordinate System"},
        xAxis: {},
        yAxis: {},
        series: [
            { type: "line", data: column(0)}
        ]
    })
)
```

