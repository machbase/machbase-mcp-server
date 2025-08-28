---
title: Noise Filters
type: docs
weight: 80
---

## Measuring sensors

The IoT data we can observe is composed of values measured through sensors.
Every sensor inherently includes some degree of noise, which represents unavoidable errors.
Data without any noise, in a purely theoretical sense, can only be mathematically generated as virtual data.

{{< tabs items="chart,SCRIPT,SET-MAP">}}
{{< tab >}}

{{< /tab >}}
{{< tab >}}
```js {{linenos=table,hl_lines=[5]}}
SCRIPT({
    $.result = { columns: ["val", "sig"], types: ["double", "double"] }
    for (i = 1.0; i <= 5.0; i+=0.03) {
        val = Math.round(i*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        $.yield( val, sig );
    }
})
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value" },
        ],
        legend: { bottom: 10 },
    })
)
```
{{< /tab >}}
{{< tab >}}
```js {{linenos=table,hl_lines=[4,5]}}
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)

SET(sig, sin(1.2 * 2 * PI * value(0)) )
MAPVALUE(1, $sig)

CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value" },
        ],
        legend: { bottom: 10 },
    })
)
```
{{< /tab >}}
{{< /tabs >}}

Generally, noise tends to be higher frequency than the data we intend to observe, as depicted in the graph below.

{{< tabs items="chart,SCRIPT,SET-MAP">}}
{{< tab >}}

{{< /tab >}}
{{< tab >}}
```js {{linenos=table,hl_lines=[6,7]}}
SCRIPT({
    $.result = { columns: ["val", "sig", "noise"], types: ["double", "double", "double"] }
    for (i = 1.0; i <= 5.0; i+=0.03) {
        val = Math.round(i*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        noise = 0.09 * Math.cos(9*2*Math.PI*val) + 
                0.15 * Math.sin(12*2*Math.PI*val);
        $.yield( val, sig, noise );
    }
})
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value" },
            { type: "line", data: column(2), name:"noise" },
        ],
        legend: { bottom: 10 },
    })
)
```
{{< /tab >}}
{{< tab >}}
```js {{linenos=table,hl_lines=[5,7]}}
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)

SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig)
MAPVALUE(2, $noise)

CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value" },
            { type: "line", data: column(2), name:"noise" },
        ],
        legend: { bottom: 10 }
    })
)
```
{{< /tab >}}
{{< /tabs >}}

Ultimately, the values measured through sensors result in a graph like the one below, where noise is mixed in.

In databases, the stored values are a blend of the aforementioned noise, and during the data analysis process, we often desire to observe the data with some degree of noise removal (noise filtering).

{{< tabs items="chart,SCRIPT,SET-MAP">}}
{{< tab >}}

{{< /tab >}}
{{< tab >}}
```js {{linenos=table,hl_lines=[6,7,17]}}
SCRIPT({
    $.result = { columns: ["val", "sig"], types: ["double", "double"] }
    for (i = 1.0; i <= 5.0; i+=0.03) {
        val = Math.round(i*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        noise = 0.09 * Math.cos(9*2*Math.PI*val) + 
                0.15 * Math.sin(12*2*Math.PI*val);
        $.yield( val, sig + noise );
    }
})
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
        ],
        legend: { bottom: 10 },
    })
)
```
{{< /tab >}}
{{< tab >}}
```js {{linenos=table,hl_lines=[5,12]}}
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig + $noise)
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
        ],
        legend: { bottom: 10 }
    })
)
```
{{< /tab >}}
{{< /tabs >}}

## Average

Imagine the zero-point calibration process for sensors. When we accumulate consecutive values and calculate their average, we can observe that the sine wave, as shown below, eventually converges to zero.

{{< tabs items="chart,SCRIPT,SET-MAP">}}
{{< tab >}}

{{< /tab >}}
{{< tab >}}
```js {{linenos=table,hl_lines=[2,11]}}
SCRIPT({
    const filter = require("@jsh/filter")
    const avg = new filter.Avg();
    const { arrange } = require("@jsh/generator");
}, {
    for( val of arrange(1, 5, 0.03)) {
        val = Math.round(val*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        noise = 0.09 * Math.cos(9*2*Math.PI*val) + 
                0.15 * Math.sin(12*2*Math.PI*val);
        $.yield( val, sig + noise, avg.eval(sig+noise) );
    }
})
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"AVG" },
        ],
        legend: { bottom: 10 },
    })
)
```
{{< /tab >}}
{{< tab >}}
```js {{linenos=table,hl_lines=[6,14]}}
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig + $noise)
MAP_AVG(2, value(1))
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"AVG" },
        ],
        legend: { bottom: 10 }
    })
)
```
{{< /tab >}}
{{< /tabs >}}

## Moving Average

Instead of calculating the average for the entire accumulated sample, we use a fixed-size window of samples to compute the average. This concept aligns with the commonly seen moving average over a certain number of days in stock charts.

{{< tabs items="chart,SCRIPT,SET-MAP">}}
{{< tab >}}

{{< /tab >}}
{{< tab >}}
```js {{linenos=table,hl_lines=[2,11]}}
SCRIPT({
    const filter = require("@jsh/filter")
    const movavg = new filter.MovAvg(10);
    const { arrange } = require("@jsh/generator");
    $.result = { columns: ["val", "sig", "ma10"], types: ["double", "double", "double"] }
}, {
    for( val of arrange(1, 5, 0.03)) {
        val = Math.round(val*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        noise = 0.09 * Math.cos(9*2*Math.PI*val) + 
                0.15 * Math.sin(12*2*Math.PI*val);
        $.yield( val, sig + noise, movavg.eval(sig+noise) );
    }
})
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"MA(10)" },
        ],
        legend: { bottom: 10 },
    })
)
```
{{< /tab >}}
{{< tab >}}
```js {{linenos=table,hl_lines=[6,14]}}
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig + $noise)
MAP_MOVAVG(2, value(1), 10)
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"MA(10)" },
        ],
        legend: { bottom: 10 }
    })
)
```
{{< /tab >}}
{{< /tabs >}}

## Low Pass Filter

While moving averages are convenient to use and understand, they have some limitations:

They tend to be slow in reflecting recent trends due to equal weighting applied to all samples within the window.
They are less responsive to significant changes in values.
To address this, a common practice is to apply different weights to the most recent and older values within the window when calculating the average.

{{< tabs items="chart,SCRIPT,SET-MAP">}}
{{< tab >}}

{{< /tab >}}
{{< tab >}}
```js {{linenos=table,hl_lines=[2,11]}}
SCRIPT({
    const filter = require("@jsh/filter")
    const lowpass = new filter.Lowpass(0.40);
    const { arrange } = require("@jsh/generator");
    $.result = { columns: ["val", "sig", "lpf"], types: ["double", "double", "double"] }
}, {
    for( val of arrange(1, 5, 0.03)) {
        val = Math.round(val*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        noise = 0.09 * Math.cos(9*2*Math.PI*val) + 
                0.15 * Math.sin(12*2*Math.PI*val);
        $.yield( val, sig + noise, lowpass.eval(sig+noise) );
    }
})
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"lpf" },
        ],
        legend: { bottom: 10 },
    })
)
```
{{< /tab >}}
{{< tab >}}
```js {{linenos=table,hl_lines=[6,14]}}
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig + $noise)
MAP_LOWPASS(2, $sig + $noise, 0.40)
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"lpf" },
        ],
        legend: { bottom: 10 }
    })
)
```
{{< /tab >}}
{{< /tabs >}}

## Kalman Filter

The `model()` argument of the `MAP_KALMAN()` function takes input values representing mathematical system variables. Explaining how to determine optimal system values lies beyond the scope of this document.
However, in practice, you can easily apply a simple Kalman filter model in TQL and iteratively find empirically optimal parameters.

The example below demonstrates how changing the model’s value affects the graph.
Feel free to experiment with different model values and observe how the graph responds

{{< tabs items="chart,SCRIPT,SET-MAP">}}
{{< tab >}}

{{< /tab >}}
{{< tab >}}
```js {{linenos=table,hl_lines=[2,13]}}
SCRIPT({
    const filter = require("@jsh/filter")
    const kalman = new filter.Kalman(0.1, 0.5, 1.0);
    const { arrange } = require("@jsh/generator");
    var ts = require("@jsh/system").now();
    $.result = { columns: ["val", "sig", "kalman"], types: ["double", "double", "double"] }
}, {
    for( val of arrange(1, 5, 0.03)) {
        val = Math.round(val*100)/100;
        sig = Math.sin( 1.2*2*Math.PI*val );
        noise = 0.09 * Math.cos(9*2*Math.PI*val) + 
                0.15 * Math.sin(12*2*Math.PI*val);
        ts = ts.Add(1000000000)
        $.yield( val, sig+noise, kalman.eval(ts, sig+noise) );
    }
})
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"kalman" },
        ],
        legend: { bottom: 10 },
    })
)
```
{{< /tab >}}
{{< tab >}}
```js {{linenos=table,hl_lines=[6,14]}}
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig + $noise)
MAP_KALMAN(2, $sig + $noise, model(0.1, 0.6, 1.0))
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"kalman" },
        ],
        legend: { bottom: 10 }
    })
)
```
{{< /tab >}}
{{< /tabs >}}
