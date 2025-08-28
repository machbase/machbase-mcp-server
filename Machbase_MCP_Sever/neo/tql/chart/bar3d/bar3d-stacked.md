---
title: Stacked 3D Bar
type: docs
weight: 20
---

```js {{linenos=table,linenostart=1}}
FAKE( meshgrid(linspace(0, 10, 11), linspace(0, 10, 11)) )
MAPVALUE(2, list( value(0), value(1), simplex(10, value(0)/5, value(1)/5) * 2 + 4))
MAPVALUE(3, list( value(0), value(1), simplex(20, value(0)/5, value(1)/5) * 2 + 4))
MAPVALUE(4, list( value(0), value(1), simplex(30, value(0)/5, value(1)/5) * 2 + 4))
MAPVALUE(5, list( value(0), value(1), simplex(40, value(0)/5, value(1)/5) * 2 + 4))
POPVALUE(0,1)
CHART(
    plugins("gl"),
    chartOption({
        xAxis3D: { type: "value" },
        yAxis3D: { type: "value" },
        zAxis3D: { type: "value" },
        grid3D: {
            viewControl: {
                // autoRotate: true
            },
            light: {
                main: {
                    shadow: true,
                    quality: "ultra",
                    intensity: 1.5
                }
            }
        },
        series: [
            {
                type: "bar3D",
                data: column(0),
                stack: "stack",
                shading: "lambert",
                emphasis: {
                    label: { show: false }
                }
            },
            {
                type: "bar3D",
                data: column(1),
                stack: "stack",
                shading: "lambert",
                emphasis: {
                    label: { show: false }
                }
            },
            {
                type: "bar3D",
                data: column(2),
                stack: "stack",
                shading: "lambert",
                emphasis: {
                    label: { show: false }
                }
            },
            {
                type: "bar3D",
                data: column(3),
                stack: "stack",
                shading: "lambert",
                emphasis: {
                    label: { show: false }
                }
            }
        ]
    })
)
```

