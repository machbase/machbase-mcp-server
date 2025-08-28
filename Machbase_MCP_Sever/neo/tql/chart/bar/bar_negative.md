---
title: Bar Chart with Negative Values
type: docs
weight: 130
---

```js {{linenos=table,linenostart=1}}
FAKE(csv(`day,profit,income,expenses
Mon,200,320,-120
Tue,170,302,-132
Wed,240,341,-101
Thu,244,374,-134
Fri,200,390,-190
Sat,220,450,-230
Sun,210,420,-210
`))

DROP(1) // drop header
MAPVALUE(1, parseFloat(value(1))) // parse float from string
MAPVALUE(2, parseFloat(value(2))) // parse float from string
MAPVALUE(3, parseFloat(value(3))) // parse float from string

CHART(
    chartOption({
        tooltip: {
            trigger: "axis",
            axisPointer: {
                type: "shadow"
            }
        },
        legend: {
            data: ["Profit", "Expenses", "Income"]
        },
        grid: {
            left: "3%",
            right: "4%",
            bottom: "3%",
            containLabel: true
        },
        xAxis: [
            {
                type: "value"
            }
        ],
        yAxis: [
            {
                type: "category",
                axisTick: {
                    show: false
                },
                data: column(0)
            }
        ],
        series: [
            {
                name: "Profit",
                type: "bar",
                label: {
                    show: true,
                    position: "inside"
                },
                emphasis: {
                    focus: "series"
                },
                data: column(1)
            },
            {
                name: "Income",
                type: "bar",
                stack: "Total",
                label: {
                    show: true
                },
                emphasis: {
                    focus: "series"
                },
                data: column(2)
            },
            {
                name: "Expenses",
                type: "bar",
                stack: "Total",
                label: {
                    show: true,
                    position: "left"
                },
                emphasis: {
                    focus: "series"
                },
                data: [-120, -132, -101, -134, -190, -230, -210]
            }
        ]
    })
)
```

