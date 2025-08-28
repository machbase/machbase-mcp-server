---
title: Stacked Bar Normalization
type: docs
weight: 135
---

```js {{linenos=table,linenostart=1}}
FAKE(json({
    ["Day",  "Direct", "Mail Ad", "Affiliate Ad", "Video Ad", "Search Engine"],
    ["Mon", 100, 320, 220, 150, 820],
    ["Tue", 302, 132, 182, 212, 832],
    ["Wed", 301, 101, 191, 201, 901],
    ["Thu", 334, 134, 234, 154, 934],
    ["Fri", 390,  90, 290, 190, 1290],
    ["Sat", 330, 230, 330, 330, 1330],
    ["Sun", 320, 210, 310, 410, 1320]
}))
MAPVALUE(6, value(1)+value(2)+value(3)+value(4)+value(5), "Total")
CHART(
    chartOption({
        legend: {
            selectedMode: false
        },
        grid: {
            left: 100, right: 100, top: 50, bottom: 50
        },
        yAxis: { type: "value", show: false },
        xAxis: { type: "category", data: _column_0.slice(1) },
        series: [ ]
    }),
    chartJSCode({
        let total = _columns[6].slice(1)
        _columns.slice(1, 6).map((cols, cid) => {
            let name = cols[0];
            let data = cols.slice(1).map((v, did) => v / total[did]);
            _chartOption.series.push({
                name: name,
                type: 'bar',
                stack: 'total',
                barWidth: '60%',
                label: {
                    show: true,
                    formatter: (params) => Math.round(params.value*1000) / 10 + '%'
                },
                data: data
            })
        });
        _chart.setOption(_chartOption);
    })
)
```

