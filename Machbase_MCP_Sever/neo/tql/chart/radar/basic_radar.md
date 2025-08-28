---
title: Basic Radar
type: docs
weight: 10
---

```js {{linenos=table,linenostart=1}}
//                       sales, admin, it,  cs,   dev,   mkt
FAKE(json({
    ["Allocated Budget", 4200, 3000, 20000, 35000, 50000, 18000],
    ["Actual Spending"  , 5000, 14000, 28000, 26000, 42000, 21000]
}))

MAPVALUE(1, list(value(1), value(2), value(3), value(4), value(5), value(6)))
MAPVALUE(1, dict("name", value(0), "value", value(1)))
POPVALUE(2,3,4,5,6)
CHART(
    chartOption({
        title: { "text": "Basic Radar Chart" },
        legend: {
            data: column(0),
            top: "95%"
        },
        radar: {
            indicator: [
                { name: "Sales", max: 6500 },
                { name: "Administration", max: 16000 },
                { name: "Information Technology", max: 30000 },
                { name: "Customer Support", max: 38000 },
                { name: "Development", max: 52000 },
                { name: "Marketing", max: 25000 }
            ]
        },
        series: [
            {
                name: "Budget vs spending",
                type: "radar",
                data: column(1)
            }
        ]
    })
)
```

