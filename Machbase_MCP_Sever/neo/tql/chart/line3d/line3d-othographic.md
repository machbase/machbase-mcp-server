---
title: Orthographic Projection
type: docs
weight: 20
---

```js {{linenos=table,linenostart=1}}
FAKE(linspace(0, 24.999, 25000))
MAPVALUE(1, (1 + 0.25 * cos(75 * value(0))) * cos(value(0)))
MAPVALUE(2, (1 + 0.25 * cos(75 * value(0))) * sin(value(0)))
MAPVALUE(3, value(0) + 2.0 * sin(75 * value(0)))
MAPVALUE(0, list(value(1), value(2), value(3)))
POPVALUE(1,2,3)
CHART(
    plugins("gl"),
    chartOption({
        tooltip: {},
        backgroundColor: "#fff",
        visualMap: {
            show: false,
            dimension: 2,
            min: 0,
            max: 30,
            inRange: {
                color: [
                    "#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf",
                    "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"
                ]
            }
        },
        xAxis3D: { type: "value" },
        yAxis3D: { type: "value" },
        zAxis3D: { type: "value" },
        grid3D: {
            viewControl: {
                projection: "orthographic"
            }
        },
        series: [
            {
                type: "line3D",
                data: column(0),
                lineStyle: { width: 4}
            }
        ]
    })
)
```

