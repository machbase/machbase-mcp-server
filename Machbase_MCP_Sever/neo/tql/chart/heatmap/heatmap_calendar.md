---
title: Calendar Heatmap
type: docs
weight: 620
---

```js {{linenos=table,linenostart=1}}
FAKE(linspace(1, 365, 365))
MAPVALUE(1, simplex(10, value(0))+0.9)
MAPVALUE(0, 1672444800+(value(0)*3600*24)) // 2023/01/01 00:00:00
MAPVALUE(0, time(value(0)*1000000000))
MAPVALUE(0, list(value(0), value(1)))
CHART(
    chartOption({
        title: {
            top: 30,
            left: "center",
            text: "Daily Measurements"
        },
        tooltip: {},
        visualMap: {
            min: 0,
            max: 2.0,
            type: "piecewise",
            orient: "horizontal",
            left: "center",
            top: 65
        },
        calendar: {
            top: 120,
            left: 30,
            right: 30,
            cellSize: ["auto", 13],
            range: "2023",
            itemStyle: {
                borderWidth: 0.5
            },
            yearLabel: {show:true}
        },
        series: {
            type: "heatmap",
            coordinateSystem: "calendar",
            data: column(0)
        }
    })
)
```

