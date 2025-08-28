---
title: Doughnut
type: docs
weight: 920
---

```js {{linenos=table,linenostart=1}}
FAKE( json({
    ["Search Engine", 1048 ],
    ["Direct"       ,  735 ],
    ["Email"        ,  580 ],
    ["Union Ads"    ,  484 ],
    ["Video Ads"    ,  300 ]
}) )
MAPVALUE(0, list(value(0), value(1)))
CHART(
    chartOption({
        tooltip: {
            trigger: "item"
        },
        legend: {
            orient: "vertical",
            left: "left"
        },
        dataset: [ { source: column(0) } ],
        series: [
            {
                name: "Access From",
                type: "pie",
                radius: ["40%", "70%"],
                datasetIndex: 0,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: "rgba(0, 0, 0, 0.5)"
                    }
                }
            }
        ]
    })
)
```

