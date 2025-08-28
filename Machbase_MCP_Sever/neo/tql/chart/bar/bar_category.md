---
title: Category Bar
type: docs
weight: 130
---

```js {{linenos=table,linenostart=1}}
FAKE( json({
    ["2011", "Brazil", 18203],
    ["2011", "Indonesia", 23489],
    ["2011", "USA", 29034],
    ["2011", "India", 104970],
    ["2011", "China", 131744],
    ["2011", "World", 630230],
    ["2022", "Brazil", 19325],
    ["2022", "Indonesia", 23438],
    ["2022", "USA", 31000],
    ["2022", "India", 121594],
    ["2022", "China", 134141],
    ["2022", "World", 681807]
}) )
// |   0      1         2
// +-> year   country   population
// |
MAPVALUE(3, value(0) == "2011" ? value(2) : 0)
// |   0      1         2            3
// +-> year   country   population   2011-population
// |
MAPVALUE(4, value(0) == "2022" ? value(2) : 0)
// |   0      1         2            3                  4
// +-> year   country   population   2011-population   2022-population
// |
POPVALUE(0, 2)
// |   0        1                  2
// +-> country  2011-population   2022-population
// |
GROUP( by(value(0)), max(value(1)), max(value(2)), lazy(true))
// |
CHART(
    chartOption({
        legend: { show:true},
        tooltip: {
            trigger: "axis",
            axisPointer: {
                type: "shadow"
            }
        },
        xAxis: { type: "category", data: column(0) },
        yAxis: { },
        series: [
            { type: "bar", name: "2011", data: column(1) },
            { type: "bar", name: "2022", data: column(2) }
        ]
    })
)
```

