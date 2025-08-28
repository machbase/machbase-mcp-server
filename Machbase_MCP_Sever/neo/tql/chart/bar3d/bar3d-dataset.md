---
title: 3D Bar with Dataset
type: docs
weight: 10
---

```js {{linenos=table,linenostart=1}}
CSV( file("https://docs.machbase.com/assets/example/life-expectancy-table.csv") )
// |   0        1                 2            3        4
// +-> income   life-expectancy   population   country  year
// |
DROP(1) // drop header
// |
MAPVALUE(0, value(4))
// |   0        1                 2            3        4
// +-> year     life-expectancy   population   country  year
// |
POPVALUE(4)
// |   0        1                 2            3
// +-> year     life-expectancy   population   country
// |
MAPVALUE(1, parseFloat(value(1)) )
MAPVALUE(2, parseFloat(value(2)) )
// |   0        1                 2            3 
// +-> year     life-expectancy   population   country
// |
MAPVALUE(0, list(value(0), value(1), value(2), value(3)))
POPVALUE(1,2,3)
// |   0 
// +-> [year, life-expectancy, population, country]
// |
CHART(
    plugins("gl"),
    chartOption({
        grid3D: {},
        tooltip: {},
        xAxis3D: { type: "category" },
        yAxis3D: { type: "category" },
        zAxis3D: {},
        visualMap: { max: 100000000, dimension: "Population"},
        dataset: {
            dimensions: [
                { name: "Year", type: "ordinal"},
                "Life Expectancy",
                "Population",
                "Country"
            ],
            source: column(0)
        },
        series: [
            {
                type: "bar3D",
                shading: "lambert",
                encode: {
                    x: "Year",
                    y: "Country",
                    z: "Lefe Expectancy",
                    tooltip: [0, 1, 2, 3]
                }
            }
        ]
    })
)
```

