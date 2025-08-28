---
title: Liquidfill
type: docs
weight: 500
---

```js {{linenos="table",hl_lines=[5,8]}}
FAKE(json({
    [0.6]
}))
CHART(
    plugins("liquidfill"),
    chartOption({
        series: [
            { type: "liquidFill", data: column(0) }
        ]
    })
)
```

