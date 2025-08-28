---
title: Iris Sepal Length
type: docs
weight: 110
---

- Line 4: `BOXPLOT()` is available {{< neo_since ver="8.0.15" />}}.
- Line 5: `value(0)` sepal length
- Line 6: `value(4)` species
- Line 8: `boxplotOutput("chart")` makes `BOXPLOT()` to yield records those formats are fit to echarts.
- Line 17: a series for the boxplot.
- Line 18: column().flat() is required to display outlier points.

```js {linenos=table,hl_lines=[5,6,8,17,18]}
CSV(file("https://docs.machbase.com/assets/example/iris.csv"))
MAPVALUE(4, strToUpper(strTrimPrefix(value(4), "Iris-")))

BOXPLOT(
    value(0),
    category(value(4)),
    order("SETOSA", "VERSICOLOR", "VIRGINICA"),
    boxplotOutput("chart")
)

CHART(
    chartOption({
        grid: { bottom: "15%" },
        xAxis:{ type:"category", boundaryGap: true, data: column(0) },
        yAxis:{ type:"value", name: "sepal length", min:4, max:8, splitArea:{ show: true } },
        series:[
            { name: "sepal length", type:"boxplot", data: column(1)},
            { name: "outlier", type:"scatter", data: column(2).flat()},
        ],
        tooltip: { trigger: 'item', axisPointer: { type: 'shadow' } },
        legend: {show: true, bottom:'2%'},
        title:[ { text: "Iris Sepal Length", left: "center" } ]
    })
)
```

