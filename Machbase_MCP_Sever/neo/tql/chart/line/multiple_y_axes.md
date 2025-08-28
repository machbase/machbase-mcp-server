---
title: Multiple Y-Axes
type: docs
weight: 72
---

```js {{linenos=table,linenostart=1}}
FAKE(json({
    ["Month", "Evaporation", "Precipitation", "Temperature"],
    ["Jan", 2.0,   2.6,   2.0],
    ["Feb", 4.9,   5.9,   2.2],
    ["Mar", 7.0,   9.0,   3.3],        
    ["Apr", 23.2,  26.4,  4.5],         
    ["May", 25.6,  28.7,  6.3],         
    ["Jun", 76.7,  70.7,  10.2],        
    ["Jul", 135.6, 175.6, 20.3],         
    ["Aug", 162.2, 182.2, 23.4],         
    ["Sep", 32.6,  48.7,  23.0],         
    ["Oct", 20.0,  18.8,  16.5],         
    ["Nov", 6.4,   6.0,   12.0],        
    ["Dec", 3.3,   2.3,   6.2]  
}))

CHART(
  chartJSCode({
    const colors = ['#5470C6', '#91CC75', '#EE6666'];
  }),
  chartOption({
    color: colors,
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "cross"
      }
    },
    grid: { right: "23%" },
    toolbox: {
      feature: {
        dataView: { show: true, readOnly: false },
        restore: { show: true },
        saveAsImage: { show: true }
      }
    },
    legend: { bottom: 10, data: [ column(1)[0], column(2)[0], column(3)[0]] },
    xAxis: [
        {
          type: "category",
          axisTick: {
            alignWithLabel: true
          },
          data: column(0).slice(1)
        }
      ],
    yAxis: [
      {
        type: "value",
        name: "Evaporation",
        position: "right",
        alignTicks: true,
        axisLine: { show: true, lineStyle: { color: colors[0] } },
        axisLabel: { formatter: "{value} ml" }
      },
      {
        type: "value",
        name: "Precipitation",
        position: "right",
        alignTicks: true,
        offset: 80,
        axisLine: { show: true, lineStyle: { color: colors[1] } },
        axisLabel: { formatter: "{value} ml" }
      },
      {
        type: "value",
        name: "Temperature",
        position: "left",
        alignTicks: true,
        axisLine: { show: true, lineStyle: { color: colors[2] } },
        axisLabel: { formatter: "{value} °C" }
      }
    ],
    series: [
      {
        name: "Evaporation",
        type: "bar",
        data: column(1).slice(1)
      },
      {
        name: "Precipitation",
        type: "bar",
        yAxisIndex: 1,
        data: column(2).slice(1)
      },
      {
        name: "Temperature",
        type: "line",
        yAxisIndex: 2,
        data: column(3).slice(1)
      }
    ]
  })
)
```

