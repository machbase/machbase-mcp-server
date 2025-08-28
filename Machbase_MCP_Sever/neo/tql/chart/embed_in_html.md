---
title: Embed in HTML
type: docs
weight: 10
---

Save the code below as `basic_line.tql` and we will show you how to embed the result of this *TQL* into web page.

```js
FAKE( linspace(0, 360, 100))
MAPVALUE(2, sin((value(0)/180)*PI))
CHART(
    theme("white"),
    chartOption({
        "xAxis": { "type": "category", "data": column(0) },
        "yAxis": {},
        "series": [ { "type": "line", "data": column(1) } ]
    })
)
```

## IFRAME

```html {linenos=table,hl_lines=[3],linenostart=1}
<html>
<body>
    <iframe src="basic_line.tql" width="600" height="600"/>
</body>
</html>
```

## JSON Response

Call *.tql* script file with a custom HTTP header `X-Tql-Output: json` {{< neo_since ver="8.0.42" />}} (which replaces the deprecated header `X-Chart-Output` {{< neo_since ver="8.0.14" />}})
to produce the result in JSON instead of full HTML document,
so that caller can embed the chart into any place of the HTML DOM.
The `X-Tql-Output: json` header is actually equivalent to the `CHART()` SINK with `chartJson(true)` option like `CHART( chartJson(true), chartOption({...}))`.
The example of `chartJson(true)` can be found in the section "[As Reading API](/neo/tql/reading/#chart-with-chartjson)".

When the reponse of `/db/tql` is JSON, it contains required addresses of the result javascript.

```json
{
    "chartID": "NDg4ODQ4MzMxMjgyMDYzMzY",
    "jsAssets": ["/web/echarts/echarts.min.js"],
	"jsCodeAssets": ["/web/api/tql-assets/NDg4ODQ4MzMxMjgyMDYzMzY.js"],
    "style": {
        "width": "600px",
        "height": "600px"	
    },
    "theme": "white"
}
```

- `chartID` random generated chartID of echarts, a client can set a specific ID with `chartID()` option.
- `jsAssets` server returns the addresses of echarts resources. The array may contains the main echarts (`echarts.min.js`) and extra plugins javascript files.
- `jsCodeAssets` machbase-neo generates the javascript to properly render the echarts with the result data.

The HTML document below is an exmaple to utilize the JSON response above to render echarts.

```html {linenos=table,hl_lines=[3,14,19,23],linenostart=1}
<html>
<body>
    <script src="/web/echarts/echarts.min.js"></script>
    <div id="chart_is_here"></div>
    <script>
        function loadJS(url) {
            var scriptElement = document.createElement('script');
            scriptElement.src = url;
            document.getElementsByTagName('body')[0].appendChild(scriptElement);
        }
    </script>
    <script>
        fetch("basic_line.tql", {
            headers: { "X-Tql-Output": "json" }
        }).then(function(rsp){
            return rsp.json()
        }).then(function(obj) {
            const chartDiv = document.createElement('div')
            chartDiv.setAttribute("id", obj.chartID)
            chartDiv.style.width = obj.style.width
            chartDiv.style.height = obj.style.height
            document.getElementById('chart_is_here').appendChild(chartDiv)
            obj.jsCodeAssets.forEach((js) => loadJS(js))
        }).catch(function(err){
            console.log("chart fetch error", err)
        })
    </script>
</body>
</html>
```
- Line 3, Pre-load apache echarts library which is included in `jsAssets` fields in above response example.
- Line 14, The HTTP header `X-Tql-Output: json`.
so that machbase-neo TQL engine generates a JSON containing meta information of chart instead of full HTML document.
Becuase when a client requests a `*.tql` file with `GET` method, machbase-neo generates HTML document for the chart by default.
- Line 23, Load js files into the HTML DOM tree that are generated and replied in `jsCodeAssets`.


## Dynamic TQL

The api `/db/tql` can receive POSTed TQL script and produces the result in javascript.
Caller side javascrpt can load the result javascript dynamically as the example below.

In this example, the `chartID()` (line 20) is provided and the document has a `<div>` with the same `id`.

```html {linenos=table,hl_lines=[4,13,20,34],linenostart=1}
<html>
<body id="body">
    <script src="/web/echarts/echarts.min.js"></script>
    <div id="chart_is_here"/>
    <script>
        function loadJS(url) {
            var scriptElement = document.createElement('script');
            scriptElement.src = url;
            document.getElementsByTagName('body')[0].appendChild(scriptElement);
        }
    </script>
    <script>
        fetch("/db/tql", 
            {
                method:"POST", 
                body:`
                    FAKE( linspace(0, 360, 100) )
                    MAPVALUE( 1, sin(value(0)/180*PI) )
                    CHART(
                        chartID("chart_is_here"),
                        chartOption({
                            xAxis: { type: "category", data: column(0) },
                            yAxis: {},
                            series: [ { type: "line", data: column(1) } ]
                        })
                    )
            `}
        ).then(function(rsp){
            return rsp.json()
        }).then(function(obj) {
            const chartDiv = document.getElementById('chart_is_here')
            chartDiv.style.width = obj.style.width
            chartDiv.style.height = obj.style.height
            obj.jsCodeAssets.forEach((js) => loadJS(js))
        }).catch(function(err){
            console.log("chart fetch error", err)
        })
    </script>
</body>
</html>
```

## Loading Sequence Problem

In the examples above, if we tried to load the both of `jsAssets` and `jsCodeAssets` dynamically, like below code for example.

```js {linenos=table,linenostart=38}
const assets = obj.jsAssets.concat(obj.jsCodeAssets)
assets.forEach((js) => loadJS(js))
```

There must be some loading sequence issue, because the chart library (apache echarts) in `obj.jsAssets` might not be completely loaded 
before `obj.jsCodeAssets` are loaded.
To avoid the problem of loading sequence, it can be fixed like below code.

Add `load` event listener to enable callback for load-completion.

```js {linenos=table,hl_lines=["5-9"],linenostart=6}
function loadJS(url, callback) {
    var scriptElement = document.createElement('script');
    scriptElement.src = url;
    document.getElementsByTagName('body')[0].appendChild(scriptElement);
    scriptElement.addEventListener("load", ()=>{
        if (callback !== undefined) {
            callback()
        }
    })
}
```

When the last `jsAssets` loaded, start to load `jsCodeAssets`.

```js {linenos=table,hl_lines=[4,"6-8"],linenostart=34}
for (let i = 0; i < obj.jsAssets.length; i++ ){
    if (i < obj.jsAssets.length -1){ 
        loadJS(obj.jsAssets[i])
    } else { // when the last asset file is loaded, start to load jsCodeAssets
        loadJS(obj.jsAssets[i], () => {
            obj.jsCodeAssets.forEach(js => loadJS(js)) 
        })
    }
}
```