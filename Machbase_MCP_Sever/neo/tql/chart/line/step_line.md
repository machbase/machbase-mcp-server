---
title: Step Line
type: docs
weight: 60
---

{{< tabs items="SCRIPT,FAKE">}}
{{< tab >}}
```js {{linenos=table,linenostart=1}}
SCRIPT({
  days    = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"];
  starts  = [120,132,101,134,90,230,210];
  middles = [220,282,201,234,290,430,410];
  ends    = [450,432,401,454,590,530,510];

  $.yield({
    legend: { show:true },
    grid: [{
      left: "3%",
      right: "4%",
      bottom: "3%",
      containLabel: true
    }],
    xAxis: { type: "category", data: days },
    yAxis: {},
    series: [
      {type: "line", data: starts, step: "start", name: "Step Start"},
      {type: "line", data: middles, step: "middle", name: "Step Middle"},
      {type: "line", data: ends, step: "end", name: "Step End"}
    ]
  })
})
CHART()
```
{{< /tab >}}
{{< tab >}}
```js {{linenos=table,linenostart=1}}
FAKE( json({
  ["Mon", 120, 220, 450],
  ["Tue", 132, 282, 432],
  ["Wed", 101, 201, 401],
  ["Thu", 134, 234, 454],
  ["Fri", 90,  290, 590],
  ["Sat", 230, 430, 530],
  ["Sun", 210, 410, 510]
}) )
CHART(
  chartOption({
    legend: { show:true },
    grid: [{
      left: "3%",
      right: "4%",
      bottom: "3%",
      containLabel: true
    }],
    xAxis: { type: "category", data: column(0) },
    yAxis: {},
    series: [
      {type: "line", data: column(1), step: "start", name: "Step Start"},
      {type: "line", data: column(2), step: "middle", name: "Step Middle"},
      {type: "line", data: column(3), step: "end", name: "Step End"}
    ]
  })
)
```
{{< /tab >}}
{{< /tabs >}}

