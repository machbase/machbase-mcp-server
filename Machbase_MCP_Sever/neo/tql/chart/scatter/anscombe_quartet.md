---
title: Anscombe's quartet
type: docs
weight: 310
---

```js {{linenos=table,linenostart=1}}
FAKE( json({
    [1701059601000000000,  4.26, 3.1 ,  5.39, 12.5],
    [1701059602000000000,  5.68, 4.74,  5.73, 6.89],
    [1701059603000000000,  7.24, 6.13,  6.08, 5.25],
    [1701059604000000000,  4.82, 7.26,  6.42, 7.91],
    [1701059605000000000,  6.95, 8.14,  6.77, 5.76],
    [1701059606000000000,  8.81, 8.77,  7.11, 8.84],
    [1701059607000000000,  8.04, 9.14,  7.46, 6.58],
    [1701059608000000000,  8.33, 9.26,  7.81, 8.47],
    [1701059609000000000, 10.84, 9.13,  8.15, 5.56],
    [1701059610000000000,  7.58, 8.74, 12.74, 7.71],
    [1701059611000000000,  9.96, 8.1 ,  8.84, 7.04]
}) )

MAPVALUE(0, time(value(0)))
MAPVALUE(1, list(value(0), value(1)))
MAPVALUE(2, list(value(0), value(2)))
MAPVALUE(3, list(value(0), value(3)))
MAPVALUE(4, list(value(0), value(4)))
CHART(
    chartOption({
        title: {
            text: "Anscombe's quartet",
            left: "center",
            top: 0
        },
        grid: [
            { left:  "7%", top: "7%", width: "38%", height: "38%" },
            { right: "7%", top: "7%", width: "38%", height: "38%" },
            { left:  "7%", bottom: "7%", width: "38%", height: "38%" },
            { right: "7%", bottom: "7%", width: "38%", height: "38%" }
        ],
        xAxis: [
            { gridIndex: 0, type:"time", min: 1701059598000, max: 1701059614000 },
            { gridIndex: 1, type:"time", min: 1701059598000, max: 1701059614000 },
            { gridIndex: 2, type:"time", min: 1701059598000, max: 1701059614000 },
            { gridIndex: 3, type:"time", min: 1701059598000, max: 1701059614000 }
        ],
        yAxis: [
            { gridIndex: 0, min: 0, max: 15 },
            { gridIndex: 1, min: 0, max: 15 },
            { gridIndex: 2, min: 0, max: 15 },
            { gridIndex: 3, min: 0, max: 15 }
        ],
        series: [
            {   name: "I",
                type: "scatter",
                data: column(1),
                xAxisIndex: 0,
                yAxisIndex: 0,
                markLine: {
                    animation:false,
                    data: [
                        [ {coord: [1701059598000, 3], symbol: "none"}, {coord: [1701059614000, 13], symbol: "none"} ]
                    ]
                }
            },
            {   name: "II",
                type: "scatter",
                data: column(2),
                xAxisIndex: 1,
                yAxisIndex: 1,
                markLine: {
                    animation:false,
                    data: [
                        [ {coord: [1701059598000, 3], symbol: "none"}, {coord: [1701059614000, 13], symbol: "none"} ]
                    ]
                }
            },
            {   name: "III",
                type: "scatter",
                data: column(3),
                xAxisIndex: 2,
                yAxisIndex: 2,
                markLine: {
                    animation:false,
                    data: [
                        [ {coord: [1701059598000, 3], symbol: "none"}, {coord: [1701059614000, 13], symbol: "none"} ]
                    ]
                }
            },
            {   name: "IV",
                type: "scatter",
                data: column(4),
                xAxisIndex: 3,
                yAxisIndex: 3,
                markLine: {
                    animation: false,
                    data: [
                        [ {coord: [1701059598000, 3], symbol: "none"}, {coord: [1701059614000, 13], symbol: "none"} ]
                    ]
                }
            }
        ]
    })
)
```

