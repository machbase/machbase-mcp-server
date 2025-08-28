---
title: Seoul
type: docs
weight: 10
---

```js {{linenos=table,linenostart=1}}
FAKE(json({
    ["노원구", 10], ["도봉구", 50], ["강북구", 90],
    ["성북구", 20], ["종로구", 10], ["서대문구", 40],
    ["은평구", 90], ["마포구", 60], ["강서구", 20],
    ["양천구", 55], ["구로구", 75], ["영등포구", 35],
    ["중구", 100], ["용산구", 20], ["성동구", 65],
    ["광진구", 25], ["동대문구", 10], ["중랑구", 70],
    ["강동구", 10], ["송파구", 30], ["강남구", 50],
    ["서초구", 50], ["동작구", 90], ["관악구", 70], ["금천구", 90]
}))
SCRIPT({
    data = [];
},{
    data.push({name:$.values[0], value:$.values[1]})
}, {
    $.yield(data)
})
CHART(
    chartOption({
        title:{ text: "GEOJSON - Seoul"},
        tooltip: { trigger: "item", formatter: "{b}<br/>{c} %"},
        visualMap: {
            min: 0,
            max: 100,
            text: ["100%", "0%"],
            realtime: false,
            calculable: true,
            inRange: {
                color: [ "#89b6fe", "#25529a"]
            },
        },
        series: []
    }),
    chartJSCode({
        fetch("https://docs.machbase.com/assets/example/seoul_gu.json"
        ).then( function(rsp) {
            return rsp.json();
        }).then( function(seoulJSON) {
            echarts.registerMap("seoul_gu", seoulJSON);
            _chartOption.geo = {
                map: "seoul_gu",
                zoom: 1.2,
                roam: true,
                itemStyle: {
                    areaColor: "#e7e8ea"
                }
            };
            _chartOption.series[0] ={
                type: "map",
                geoIndex: 0,
                data: column(0)[0]
            };
            _chart.setOption(_chartOption);
        }).catch(function(err){
            console.warn("geojson error", err)
        });
    })
)
```

