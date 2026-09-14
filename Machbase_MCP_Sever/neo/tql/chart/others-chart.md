# Machbase Neo Other Charts

## 빠른 참조

### TQL 파이프라인 구조

TQL은 **데이터 흐름(파이프라인)** 방식으로 동작합니다:

```
SRC (데이터 소스) → MAP (변환) → SINK (출력)
```

---

### SRC - 데이터 소스

**데이터를 생성하거나 가져오는** 함수 (파이프라인 시작)

| 함수 | 용도 | 예시 |
|----------|---------|---------|
| `FAKE()` | 테스트 데이터 생성 | `FAKE(linspace(0, 100, 10))` |
| `SQL()` | 데이터베이스 쿼리 | `SQL('SELECT time, value FROM example')` |
| `CSV()` | CSV 파일 읽기 | `CSV(file('/path/to/data.csv'))` |
| `SCRIPT()` | JavaScript 코드 | `SCRIPT({ $.yield(1, 2, 3) })` |

---

### MAP - 데이터 변환

**데이터를 가공하고 변환하는** 함수 (파이프라인 중간)

| 함수 | 용도 | 예시 |
|----------|---------|---------|
| `MAPVALUE()` | 컬럼 추가/수정 | `MAPVALUE(1, value(0) * 2)` |
| `MAPKEY()` | 키 수정 | `MAPKEY(strUpper(key()))` |
| `PUSHVALUE()` | 앞쪽에 컬럼 삽입 | `PUSHVALUE(0, "new_value")` |
| `POPVALUE()` | 컬럼 제거 | `POPVALUE(2)` |
| `GROUP()` | 그룹화/집계 | `GROUP(by(value(0)), avg(value(1)))` |
| `SCRIPT()` | JavaScript 처리 | `SCRIPT({}, { /* process */ }, {})` |

---

### SINK - 데이터 출력

**데이터를 출력하거나 저장하는** 함수 (파이프라인 끝)

| 함수 | 용도 | 예시 |
|----------|---------|---------|
| `CHART()` | 차트 생성 | `CHART(chartOption({...}))` |
| `CSV()` | CSV 출력 | `CSV()` |
| `JSON()` | JSON 출력 | `JSON()` |
| `INSERT()` | DB 입력 | `INSERT(...)` |
| `APPEND()` | DB append | `APPEND(table('example'))` |

---

### CHART() 함수 기본 사용법

**문법**: `CHART(chartOption() [,size()] [, theme()] [, chartJSCode()])`

*버전 8.0.8부터 사용 가능*

#### 주요 옵션

**chartOption()**
- `chartOption( { json in apache echarts options } )`
- Apache ECharts 옵션을 JSON 형식으로 전달합니다.

**size()**
- `size(width, height)`
- `width` *string* HTML 문법의 차트 너비, 예: `'800px'`
- `height` *string* HTML 문법의 차트 높이, 예: `'800px'`

**theme()**
- `theme(name)`
- `name` *string* 테마 이름
- 사용 가능한 테마: `white`, `dark`, `chalk`, `essos`, `infographic`, `macarons`, `purple-passion`, `roma`, `romantic`, `shine`, `vintage`, `walden`, `westeros`, `wonderland`

**chartJSCode()**
- `chartJSCode( { user javascript code } )`
- 사용자 정의 JavaScript 코드를 실행합니다.

**plugins()**
- `plugins(plugin...)`
- `plugin` *string* 미리 정의된 플러그인 이름 또는 플러그인 모듈의 URL

---

### 핵심 함수

#### value(index)
**현재 레코드**의 값에 접근합니다 (파이프라인 중간에서 사용)

- `value(0)` = 현재 레코드의 첫 번째 값
- `value(1)` = 현재 레코드의 두 번째 값
- `value()` = 값 배열 전체

---

#### column(index)
**모든 레코드**에서 특정 컬럼을 배열로 모읍니다 (CHART() 전용)

- `column(0)` = 모든 레코드의 첫 번째 값 → 배열
- `column(1)` = 모든 레코드의 두 번째 값 → 배열
- **⚠️ CHART() 안에서만 사용 가능**

**비교**:

| 함수 | 사용 위치 | 반환 | 예시 |
|----------|----------|---------|---------|
| `value(0)` | 파이프라인 중간 | 단일 값 | `10` |
| `column(0)` | CHART() 내부 | 배열 | `[1,2,3]` |

---

## 1. 생키 다이어그램

노드 간 연결과 흐름의 양을 보여주는 다이어그램입니다.

```js
FAKE(csv(
`a,a1,5
a,a2,3
b,b1,8
a,b1,3
b1,a1,1
b1,c,2
`))
SCRIPT({
    data = [];
},{
    data.push({source: $.values[0], target: $.values[1], value: $.values[2]})
},{
    $.yield({
        series: {
            type: "sankey",
            layout: "none",
            emphasis: {
                focus: "adjacency"
            },
            links: data,
            data: [
                {name: "a"}, {name: "b"}, {name: "a1"}, {name: "a2"}, {name: "b1"}, {name: "c"}
            ]
        }
    })
})
CHART()
```

**설명**: 노드 간 흐름을 시각화하는 생키 다이어그램입니다. 연결선의 두께가 흐름의 양을 나타냅니다.

**핵심 포인트**:

**Data Format**:
- CSV: `source,target,value`
- 객체로 변환: `{source: "a", target: "a1", value: 5}`
- links 배열이 모든 연결을 정의합니다

**노드 정의**:
- `data: [{name: "a"}, {name: "b"}, ...]`가 모든 노드를 정의합니다
- 모든 source와 target을 포함해야 합니다
- 노드 위치는 자동 계산됩니다

**설정**:
- `type: "sankey"`가 생키 다이어그램을 만듭니다
- `layout: "none"`은 기본 레이아웃 알고리즘을 사용합니다
- `emphasis.focus: "adjacency"`가 마우스오버 시 연결된 노드를 강조합니다
- `links`에 연결 데이터가 들어갑니다
- `value`가 연결선 두께를 결정합니다

**활용 사례**:
- 에너지 흐름도
- 물질 흐름 분석
- 예산 배분
- 사용자 여정 시각화
- 네트워크 트래픽 분석

---

## 2. 워드클라우드

단어 빈도를 크기로 표현하는 시각화입니다.

### 외부 텍스트 파일에서

```js
SCRIPT({
    counter = {};
    data = [];
},{
    const http = require("@jsh/http");
    req = http.request("https://docs.machbase.com/assets/example/wordcount.txt")
    req.do((rsp) => {
        content = rsp.text();
        words = content.split(/\s+/)
        for(w of words) {
            w = w.toLowerCase();
            if(counter[w]) {
                counter[w].count++;
            } else {
                counter[w] = {count:1}
            }
        }
    })
},{
    Object.keys(counter).forEach(w =>{
        data.push({name: w, value: counter[w].count})
    })
    $.yield({
        series: {
            type: "wordCloud",
            gridSize: 4,
            sizeRange: [12, 50],
            rotationRange: [-90, 90],
            shape: "circle",
            width: 580,
            height: 580,
            drawOutOfBound: false,
            left: "center",
            top: "center",
            data: data,
            emphasis: {
                focus: "self",
                textStyle: {
                    textShadowBlur: 10,
                    textShadowColor: "#333"
                }
            },
            layoutAnimation: true,
            textStyle: {
                fontFamily: "sans-serif",
                fontWeight: "bold",
            }
        }
    })
})
CHART(
    plugins("wordcloud"),
    chartOption({}),
    chartJSCode({
        _chartOption.series.textStyle.color = function() {
            let r = Math.round(Math.random() * 160);
            let g = Math.round(Math.random() * 160);
            let b = Math.round(Math.random() * 160);
            return `rgb(${r},${g},${b})`;
        }
        _chart.setOption(_chartOption);
    })
)
```

### CSV 데이터에서

```js
FAKE(csv(
`Deep Learning,6181
Computer Vision,4386
Artificial Intelligence,4055
Neural Network,3500
Algorithm,3333
Model,2700
Supervised,2500
Unsupervised,2333
Natural Language Processing,1900
Chatbot,1800
Virtual Assistant,1500
Speech Recognition,1400
Convolutional Neural Network,1325
Reinforcement Learning,1300
Training Data,1250
Classification,1233
Regression,1000
Decision Tree,900
K-Means,875
N-Gram Analysis,850
Microservices,833
Pattern Recognition,790
APIs,775
Feature Engineering,700
Random Forest,650
Bagging,600
Anomaly Detection,575
Naive Bayes,500
Autoencoder,400
Backpropagation,300
TensorFlow,290
word2vec,280
Object Recognition,250
Python,235
Predictive Analytics,225
Predictive Modeling,215
Optical Character Recognition,200
Overfitting,190
JavaScript,185
Text Analytics,180
Cognitive Computing,175
Augmented Intelligence,160
Statistical Models,155
Clustering,150
Topic Modeling,145
Data Mining,140
Data Science,138
Semi-Supervised Learning,137
Artificial Neural Networks,125
`))
SCRIPT({
    data = [];
},{
    data.push({name: $.values[0], value: $.values[1]})
},{
    $.yield({
        series: {
            type: "wordCloud",
            gridSize: 8,
            sizeRange: [12, 50],
            rotationRange: [-90, 90],
            shape: "circle",
            width: 580,
            height: 580,
            drawOutOfBound: false,
            left: "center",
            top: "center",
            data: data,
            emphasis: {
                focus: "self",
                textStyle: {
                    textShadowBlur: 10,
                    textShadowColor: "#333"
                }
            },
            layoutAnimation: true,
            textStyle: {
                fontFamily: "sans-serif",
                fontWeight: "bold",
            }
        }
    })
})
CHART(
    plugins("wordcloud"),
    chartOption({}),
    chartJSCode({
        _chartOption.series.textStyle.color = function() {
            return 'rgb(' + [
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160)
            ].join(',') + ')';
        }
        _chart.setOption(_chartOption);
    })
)
```

**설명**: 단어 크기가 빈도를 나타내는 워드클라우드입니다. 텍스트 파일에서 단어를 세는 방법과, 이미 집계된 CSV 데이터를 쓰는 두 가지 방식을 보여줍니다.

**핵심 포인트**:

**데이터 준비**:
- **방법 1**: 텍스트를 가져와 공백으로 나누고 출현 횟수를 셉니다
- **방법 2**: 이미 집계된 데이터를 CSV에서 불러옵니다
- 결과 형식: `{name: "word", value: count}`

**설정**:
- `plugins("wordcloud")`가 워드클라우드 플러그인을 로드합니다
- `type: "wordCloud"`가 워드클라우드를 만듭니다
- `gridSize: 4-8`은 단어 간 간격입니다(작을수록 촘촘)
- `sizeRange: [12, 50]`은 최소/최대 글꼴 크기입니다
- `rotationRange: [-90, 90]`은 단어 회전 각도입니다
- `shape: "circle"`은 구름 모양입니다(그 외 "square", "diamond", "pentagon")

**배치**:
- `width: 580, height: 580` canvas size
- `left: "center", top: "center"`로 위치를 지정합니다
- `drawOutOfBound: false`가 경계 밖으로 단어가 나가는 것을 막습니다
- `layoutAnimation: true`가 단어 배치를 애니메이션으로 보여줍니다

**스타일**:
- `chartJSCode`로 무작위 RGB 색상 지정
- 색상값을 0~160으로 제한(어두운 색 위주)
- 굵은 산세리프 글꼴
- 마우스오버 시 그림자 효과

**활용 사례**:
- 텍스트 분석
- Tag clouds
- 설문 응답
- 소셜 미디어 트렌드
- 문서 요약

---

## 3. GEO SVG 경로

사용자 정의 SVG 지도 위의 애니메이션 경로입니다.

```js
FAKE(json({
        [110.6189462165178, 456.64349563895087],
        [124.10988522879458, 450.8570048730469],
        [123.9272226116071, 389.9520693708147],
        [61.58708083147317, 386.87942320312504],
        [61.58708083147317, 72.8954315876116],
        [258.29514854771196, 72.8954315876116],
        [260.75457021484374, 336.8559607533482],
        [280.5277985253906, 410.2406672084263],
        [275.948185765904, 528.0254369698661],
        [111.06907909458701, 552.795792593471],
        [118.87138231445309, 701.365737015904],
        [221.36468155133926, 758.7870354617745],
        [307.86195445452006, 742.164737297712],
        [366.8489324762834, 560.9895157073103],
        [492.8750778390066, 560.9895157073103],
        [492.8750778390066, 827.9639780566406],
        [294.9255269587053, 827.9639780566406],
        [282.79803391043527, 868.2476088113839]
}))
// +-- [ x, y ]
// |
MAPVALUE(0, list(value(0), value(1))) // make coord pair
// |
// +--> [ (x, y), y ]
// | 
POPVALUE(1)  // remove y
// | 
// +--> [ (x, y) ]
CHART(
    chartJSCode({
        fetch("https://docs.machbase.com/assets/example/MacOdrum-LV5-floorplan-web.svg"
        ).then( function(rsp) {
            return rsp.text();
        }).then( function(svg) {
            // 'echarts' has been imported in TQL
            echarts.registerMap("MacOdrum-LV5-floorplan-web", {svg: svg});
            // 'chart' is defined by CHART() in TQL
            let opt = _chart.getOption()
            opt.geo = {
                map: "MacOdrum-LV5-floorplan-web",
                roam: true,
                emphasis: {
                    itemStyle: {
                        color: undefined
                    },
                    label: {
                        show: false
                    }
                }
            };
            _chart.setOption(opt);
        }).catch(function(err){
            console.warn("geomap error, fetch resource", err)
        });
    }),
    chartOption({
        series: [
            {
                type: "lines",
                coordinateSystem: "geo",
                geoIndex: 0,
                polyline: true,
                lineStyle: {
                    color: "#c46e54",
                    width: 5,
                    opacity: 1,
                    type: "dotted"
                },
                effect: {
                    show: true,
                    period: 8,
                    color: "#a10000",
                    constantSpeed: 80,
                    trailLength: 0,
                    symbolSize: [20, 12],
                    symbol: "path://M35.5 40.5c0-22.16 17.84-40 40-40s40 17.84 40 40c0 1.6939-.1042 3.3626-.3067 5H35.8067c-.2025-1.6374-.3067-3.3061-.3067-5zm90.9621-2.6663c-.62-1.4856-.9621-3.1182-.9621-4.8337 0-6.925 5.575-12.5 12.5-12.5s12.5 5.575 12.5 12.5a12.685 12.685 0 0 1-.1529 1.9691l.9537.5506-15.6454 27.0986-.1554-.0897V65.5h-28.7285c-7.318 9.1548-18.587 15-31.2715 15s-23.9535-5.8452-31.2715-15H15.5v-2.8059l-.0937.0437-8.8727-19.0274C2.912 41.5258.5 37.5549.5 33c0-6.925 5.575-12.5 12.5-12.5S25.5 26.075 25.5 33c0 .9035-.0949 1.784-.2753 2.6321L29.8262 45.5h92.2098z"
                },
                data: [ {coords: column(0) }] 
            }
        ]
    })
)
```

**설명**: 사용자 정의 SVG 평면도 위에 애니메이션 경로를 표시합니다. 점선 경로를 따라 이동하는 차량 아이콘을 보여줍니다.

**핵심 포인트**:

**데이터 준비**:
- `[x, y]` 좌표 배열
- `list(value(0), value(1))`이 좌표 쌍을 만듭니다
- 최종 형식: `[[x1, y1], [x2, y2], ...]`

**SVG 지도 로딩**:
- `fetch()`가 외부 SVG 파일을 불러옵니다
- `echarts.registerMap()`이 SVG를 지도로 등록합니다
- `coordinateSystem: "geo"`가 등록된 지도를 사용합니다
- `roam: true`가 이동·확대를 활성화합니다

**선 설정**:
- `type: "lines"`가 폴리라인을 그립니다
- `polyline: true`가 모든 점을 순서대로 연결합니다
- `lineStyle`: 갈색 점선, 두께 5px
- 좌표는 SVG 좌표계에 매핑됩니다

**애니메이션 효과**:
- `effect.show: true`가 이동하는 심볼을 활성화합니다
- `period: 8`은 애니메이션 주기(초)입니다
- `constantSpeed: 80`은 이동 속도입니다
- `trailLength: 0`은 심볼 뒤에 잔상을 남기지 않습니다
- `symbol: "path://..."`는 사용자 정의 SVG 차량 아이콘입니다
- 빨간 차량(#a10000)이 갈색 경로를 따라 이동합니다

**활용 사례**:
- 실내 내비게이션
- 로봇 경로 시각화
- Tour routes
- 대피 계획
- 평면도상 자산 추적
- 사용자 정의 지도 오버레이

**기술 세부사항**:
- SVG 좌표와 데이터 좌표가 일치해야 합니다
- path 데이터로 사용자 정의 SVG 도형 지정
- 모든 SVG 파일(지도, 평면도, 다이어그램)에 사용 가능
- `roam: true`로 대화형 확대·이동 가능
