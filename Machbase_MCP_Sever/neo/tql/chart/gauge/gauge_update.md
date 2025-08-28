---
title: Update Gauge
type: docs
weight: 30
---

```js {{linenos=table,linenostart=1}}
FAKE(linspace(0, 1, 1))
CHART(
    chartOption({
        tooltip: {
            formatter: "{a} <br/>{b} : {c}%"
        },
        series: [
            {
                name: "Pressure",
                type: "gauge",
                progress: {
                    show: true
                },
                detail: {
                    valueAnimation: true,
                    formatter: "{value}"
                },
                data: [
                    {
                        value: 0,
                        name: "RANDOM"
                    }
                ]
            }
        ]
    }),
    chartJSCode({
        function updateGauge() {
            fetch("/db/tql", {
                method: "POST",
                body: `
                    FAKE(linspace(0, 1, 1))
                    MAPVALUE(0, floor(random() * 100))
                    JSON()
                `
            }).then(function(rsp){
                return rsp.json()
            }).then(function(obj){
                _chartOption.series[0].data[0].value = obj.data.rows[0][0]
                _chart.setOption(_chartOption)
                if (document.getElementById(_chartID) != null) {
                    setTimeout(updateGauge, 1000)
                }
            }).catch(function(err){
                console.warn("data fetch error", err)
            });
        };
        setTimeout(updateGauge, 10)
    })
)
```

