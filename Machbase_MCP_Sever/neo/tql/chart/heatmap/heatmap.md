---
title: Heatmap
type: docs
weight: 600
---

```js {{linenos=table,linenostart=1}}
FAKE( meshgrid( linspace(1, 200, 200), linspace(1, 100, 100)) )
MAPVALUE(2, simplex(4, value(0)/40, value(1)/20) + 0.8 )
MAPVALUE(2, list(value(0), value(1), value(2)))
CHART(
    chartOption({
        tooltip: {},
        xAxis: { type: "category", value: column(0) },
        yAxis: { type: "category", value: column(1) },
        visualMap: {
            min: 0,
            max: 1.6,
            calculable: true,
            realtime: false,
            inRange: {
                color: [
                    "#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf",
                    "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"
                ]
            }
        },
        series: [
            { 
                name: "SimpleX Noise",
                type: "heatmap",
                data: column(2),
                emphasis: {
                    itemStyle: {
                        borderColor: "#333",
                        borderWidth: 1
                    }
                },
                progressive: 1000,
                animation: false
            }
        ]
    })
)
```

