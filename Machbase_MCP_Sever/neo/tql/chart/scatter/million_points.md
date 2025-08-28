---
title: 1M Points
type: docs
weight: 930
---

```js {{linenos=table,linenostart=1}}
FAKE( linspace(0, 10, 500000) )

MAPVALUE(1, random()*10)
MAPVALUE(2, sin(value(0)) - value(0)*(0.1*random()) + 1)
MAPVALUE(3, cos(value(0)) - value(0)*(0.1*random()) - 1)
POPVALUE(1)

CHART(
    chartOption({
        legend: { show: false },
        xAxis: { data: column(0) },
        yAxis: {},
        dataZoom: [
            { type: "inside" },
            { type: "slider" }
        ],
        animation: false,
        series: [
            {
                name: "A",
                type: "scatter",
                data: column(1),
                symbolSize: 3,
                itemStyle: {
                    color: "#9ECB7F",
                    opacity: 0.5
                },
                large: true
            },
            {
                name: "B",
                type: "scatter",
                data: column(2),
                symbolSize: 3,
                itemStyle: {
                    color: "#5872C0",
                    opacity: 0.5
                },
                large: true
            }
        ]
    })
)
```

