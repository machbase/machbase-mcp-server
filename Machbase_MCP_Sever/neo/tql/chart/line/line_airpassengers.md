---
title: Air Passengers
type: docs
weight: 920
---

{{< tabs items="HTTP,CSV">}}
{{< tab >}}
```js {linenos=table,linenostart=1}
HTTP(`GET https://docs.machbase.com/assets/example/AirPassengers.csv`)
SCRIPT({
  var body = $.values[0].body.String()
  var lines = body.split('\n');
  // skip header
  // rownames, time, value
  const headers = lines[0].split(','); 
  for (let i = 1; i < lines.length-1; i++) {
    row = lines[i].split(',');
    ts = parseFloat(row[1]);
    value = parseFloat(row[2]);
    year = Math.floor(ts);
    month = Math.round(12 * (Math.round(ts*100)%100)/100) + 1;
    // year float to "year/month"
    $.yield(`${year}/${month}`, value);
  }
})
CHART(
  chartOption({
    xAxis: { data: column(0) },
    yAxis: {},
    series: [
        {type:"line", name:"passengers", smooth:false, data:column(1)}
    ]
  })
)
```
{{< /tab >}}
{{< tab >}}

```js {{linenos=table,linenostart=1}}
CSV (file("https://docs.machbase.com/assets/example/AirPassengers.csv"))

// drop header : rownames,time,value
DROP(1) 
// drop rownames column
POPVALUE(0)

// year float to "year/month"
MAPVALUE(0,
  strSprintf("%.f/%.f",
    floor(parseFloat(value(0))),
    1+round(12 * (mod(round(parseFloat(value(0))*100), 100)/100)) 
  )
)
// passengers
MAPVALUE(1, parseFloat(value(1)))

CHART(
  chartOption({
    xAxis: { data: column(0) },
    yAxis: {},
    series: [
        {type: "line", name: "passengers", smooth: false, data: column(1)}
    ]
  })
)
```

{{< /tab >}}
{{< /tabs >}}

