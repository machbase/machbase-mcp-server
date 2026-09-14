# Machbase Neo Embed Chart in HTML

아래 코드를 `basic_line.tql`로 저장한 뒤, 이 TQL의 결과를 웹 페이지에 삽입하는 방법을 설명합니다.

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

```html
<html>
<body>
    <iframe src="basic_line.tql" width="600" height="600"/>
</body>
</html>
```

## JSON 응답

`.tql` 스크립트 파일을 호출할 때 HTTP 헤더 `X-Tql-Output: json`을 지정하면(버전 8.0.42부터 사용 가능하며, 8.0.14의 폐기된 `X-Chart-Output` 헤더를 대체합니다) 전체 HTML 문서 대신 JSON으로 결과를 받을 수 있습니다. 이를 통해 호출한 쪽에서 HTML DOM의 원하는 위치에 차트를 삽입할 수 있습니다.

`X-Tql-Output: json` 헤더는 실제로 `CHART()` SINK에 `chartJson(true)` 옵션을 지정한 것(`CHART( chartJson(true), chartOption({...}))`)과 동일합니다.

`/db/tql`의 응답이 JSON일 때, 결과 자바스크립트에 필요한 주소들이 담겨 있습니다.

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

**응답 필드:**
- `chartID` - echarts의 무작위 생성 chartID이며, 클라이언트가 `chartID()` 옵션으로 특정 ID를 지정할 수 있습니다.
- `jsAssets` - 서버가 반환하는 echarts 리소스 주소입니다. 메인 echarts(`echarts.min.js`)와 추가 플러그인 자바스크립트 파일이 포함될 수 있습니다.
- `jsCodeAssets` - Machbase Neo가 결과 데이터로 echarts를 올바르게 렌더링하기 위해 생성한 자바스크립트입니다.

아래 HTML 문서는 위 JSON 응답을 활용해 echarts를 렌더링하는 예제입니다.

```html
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

**핵심 포인트:**
- **3번째 줄**: 위 응답 예제의 `jsAssets` 필드에 포함된 Apache ECharts 라이브러리를 미리 로드합니다.
- **14번째 줄**: HTTP 헤더 `X-Tql-Output: json`은 Machbase Neo TQL 엔진이 전체 HTML 문서 대신 차트 메타 정보가 담긴 JSON을 생성하도록 합니다. 클라이언트가 `*.tql` 파일을 `GET`으로 요청하면 Machbase Neo는 기본적으로 차트용 HTML 문서를 생성하기 때문입니다.
- **23번째 줄**: `jsCodeAssets`로 응답된 js 파일들을 HTML DOM 트리에 로드합니다.

## 동적 TQL

`/db/tql` API는 POST로 전달된 TQL 스크립트를 받아 결과를 자바스크립트로 생성할 수 있습니다. 호출 측 자바스크립트는 아래 예제처럼 결과 자바스크립트를 동적으로 로드할 수 있습니다.

이 예제에서는 `chartID()`(20번째 줄)를 지정했고, 문서에 같은 `id`를 가진 `<div>`가 있습니다.

```html
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

## 로딩 순서 문제

위 예제들에서 `jsAssets`와 `jsCodeAssets`를 모두 동적으로 로드하려고 하면, 예를 들어 아래 코드처럼:

```js
const assets = obj.jsAssets.concat(obj.jsCodeAssets)
assets.forEach((js) => loadJS(js))
```

로딩 순서 문제가 생길 수 있습니다. `obj.jsAssets`의 차트 라이브러리(Apache ECharts)가 완전히 로드되기 전에 `obj.jsCodeAssets`가 로드될 수 있기 때문입니다.

이 문제는 아래 코드처럼 해결할 수 있습니다.

**load 이벤트 리스너를 추가해 로드 완료 콜백을 활성화:**

```js
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

**마지막 `jsAssets`가 로드되면 `jsCodeAssets` 로드를 시작:**

```js
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
