---
title: Michelson-Morley Experiment
type: docs
weight: 100
---

- Line 9: `BOXPLOT()` is available {{< neo_since ver="8.0.15" />}}.
- Line 13: `boxplotOutput("chart")` makes `BOXPLOT()` to yield records those formats are fit to echarts.
- Line 21: a series for the boxplot.
- Line 22: column().flat() is required to display outlier points.

```js {linenos=table,hl_lines=[9,13,18,21,22]}
FAKE(json({
    ["A", 850, 740, 900, 1070, 930, 850, 950, 980, 980, 880, 1000, 980, 930, 650, 760, 810, 1000, 1000, 960, 960],
    ["B", 960, 940, 960, 940, 880, 800, 850, 880, 900, 840, 830, 790, 810, 880, 880, 830, 800, 790, 760, 800],
    ["C", 880, 880, 880, 860, 720, 720, 620, 860, 970, 950, 880, 910, 850, 870, 840, 840, 850, 840, 840, 840],
    ["D", 890, 810, 810, 820, 800, 770, 760, 740, 750, 760, 910, 920, 890, 860, 880, 720, 840, 850, 850, 780],
    ["E", 890, 840, 780, 810, 760, 810, 790, 810, 820, 850, 870, 870, 810, 740, 810, 940, 950, 800, 810, 870]
}))
TRANSPOSE(fixed(0))
BOXPLOT(
    value(1),
    category(value(0)),
    boxplotInterp(true, false, true),
    boxplotOutput("chart")
)
CHART(
    chartOption({
        grid: { bottom: "15%" },
        xAxis:{ type:"category", boundaryGap: true, data: column(0) },
        yAxis:{ type:"value", name: "km/s minus 299,000", min:400, splitArea:{ show: true } },
        series:[
            { name: "boxplot", type:"boxplot", data: column(1)},
            { name: "outlier", type:"scatter", data: column(2).flat()},
        ],
        tooltip: { trigger: 'item', axisPointer: { type: 'shadow' } },
        title:[
            {
                text: "Michelson-Morley Experiment",
                left: "center"
            },
            {
                text: "max: Q3 + 1.5 * IQR \nmin: Q1 - 1.5 * IQR",
                borderColor: "#999",
                borderWidth: 1,
                textStyle: { fontWeight: "normal", fontSize: 12, lineHeight: 16 },
                left: "10%", top: "92%"
            }
        ]
    })
)
```

