---
title: Basic Gauge
type: docs
weight: 10
---

{{< tabs items="SCRIPT,FAKE">}}
{{< tab >}}

```js {{linenos=table,linenostart=1}}
SCRIPT({
    value = 55;
    $.yield({
      tooltip: { formatter: "{a} <br/>{b} : {c}%" },
      series: [
        {
          name: "Pressure",
          type: "gauge",
          detail: { formatter: "{value}" },
          data: [
              { value: value, name: "PRESSURE" }
          ]
        }
      ]
    })
})
CHART()
```

{{< /tab >}}
{{< tab >}}

```js {{linenos=table,linenostart=1}}
FAKE(linspace(55, 60, 1))
CHART(
    chartOption({
        tooltip: { formatter: "{a} <br/>{b} : {c}%" },
        series: [
          {
            name: "Pressure",
            type: "gauge",
            detail: { formatter: "{value}" },
            data: [
                { value: column(0)[0], name: "PRESSURE" }
            ]
          }
        ]
    })
)
```

{{< /tab >}}
{{< /tabs >}}

