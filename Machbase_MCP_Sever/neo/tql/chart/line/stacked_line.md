---
title: Stacked Line Chart
type: docs
weight: 30
---

```js {{linenos=table,linenostart=1}}
FAKE( json({
    ["Mon", 120, 220, 150, 320, 820],
    ["Tue", 132, 182, 232, 332, 932],
    ["Wed", 101, 191, 201, 301, 901],
    ["Thu", 134, 234, 154, 334, 934],
    ["Fri",  90, 290, 190, 390, 1290],
    ["Sat", 230, 330, 330, 330, 1330],
    ["Sun", 210, 310, 410, 320, 1320]
}) )
// |   0      1       2      3      4       5
// +-> day    email   ads    video  direct  search
// |
CHART(
    chartOption({
        xAxis: { data: column(0) },
        yAxis: {},
        series: [
            {type: "line", data: column(1), smooth:false, name: "email", stack: "total"},
            {type: "line", data: column(2), smooth:false, name: "ads", stack: "total"},
            {type: "line", data: column(3), smooth:false, name: "video", stack: "total"},
            {type: "line", data: column(4), smooth:false, name: "direct", stack: "total"},
            {type: "line", data: column(5), smooth:false, name: "search", stack: "total"}
        ]
    })
)
```

