# Machbase Neo Candlestick Chart

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
| `MAP_MOVAVG()` | 이동평균 계산 | `MAP_MOVAVG(6, value(2), 5, "MA5")` |
| `MAP_DIFF()` | 차분 계산 | `MAP_DIFF(7, value(2))` |

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

**chartDispatchAction()**
- `chartDispatchAction({ type, ...params })`
- 확대, 강조, 브러시 등 차트 동작을 실행합니다.

---

### 캔들스틱 데이터 형식

캔들스틱 차트는 `[open, close, lowest, highest]` 형식의 데이터가 필요합니다.

Example:
```js
[20, 34, 10, 38]  // open=20, close=34, lowest=10, highest=38
```

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

## 1. 기본 캔들스틱 차트

기본 OHLC(시가-고가-저가-종가) 데이터를 보여주는 단순한 캔들스틱 차트입니다.

### SCRIPT 사용

```js
SCRIPT({
  dates = [ "2017-10-24", "2017-10-25", "2017-10-26", "2017-10-27"];
  values = [ [20, 34, 10, 38], [40, 35, 30, 50],
             [31, 38, 33, 44], [38, 15,  5, 42] ];
  $.yield({
    legend: { show: false },
    xAxis: { data: dates },
    yAxis: {},
    series: [ { type: "candlestick", data: values } ]
  })
})

CHART()
```

### Using FAKE

```js
FAKE(json({
    ["2017-10-24", 20, 34, 10, 38 ], 
    ["2017-10-25", 40, 35, 30, 50 ],
    ["2017-10-26", 31, 38, 33, 44 ],
    ["2017-10-27", 38, 15,  5, 42 ]
}))

MAPVALUE(1, list(value(1), value(2), value(3), value(4)))
POPVALUE(2, 3, 4)
CHART(
    chartOption({
        legend: { show: false },
        xAxis: { data: column(0) },
        yAxis: {},
        series: [
            { type: "candlestick", data: column(1) }
        ]
    })
)
```

**설명**: 4일간의 주가 데이터를 표시하는 기본 캔들스틱 차트입니다. SCRIPT로 차트 옵션을 직접 만드는 방법과, FAKE로 데이터 변환 파이프라인을 쓰는 두 가지 방식을 보여줍니다.

**데이터 형식**: 캔들 하나마다 `[open, close, lowest, highest]` 값이 필요합니다.

---

## 2. 이동평균이 있는 주가지수

여러 개의 이동평균 지표를 함께 표시하는 캔들스틱 차트입니다.

```js
//            open     close    lowest  highest
FAKE(json({
  ["2013/1/24", 2320.26, 2320.26, 2287.3, 2362.94],
  ["2013/1/25", 2300, 2291.3, 2288.26, 2308.38],
  ["2013/1/28", 2295.35, 2346.5, 2295.35, 2346.92],
  ["2013/1/29", 2347.22, 2358.98, 2337.35, 2363.8],
  ["2013/1/30", 2360.75, 2382.48, 2347.89, 2383.76],
  ["2013/1/31", 2383.43, 2385.42, 2371.23, 2391.82],
  ["2013/2/1",  2377.41, 2419.02, 2369.57, 2421.15],
  ["2013/2/4",  2425.92, 2428.15, 2417.58, 2440.38],
  ["2013/2/5",  2411, 2433.13, 2403.3, 2437.42],
  ["2013/2/6",  2432.68, 2434.48, 2427.7, 2441.73],
  ["2013/2/7",  2430.69, 2418.53, 2394.22, 2433.89],
  ["2013/2/8",  2416.62, 2432.4, 2414.4, 2443.03],
  ["2013/2/18", 2441.91, 2421.56, 2415.43, 2444.8],
  ["2013/2/19", 2420.26, 2382.91, 2373.53, 2427.07],
  ["2013/2/20", 2383.49, 2397.18, 2370.61, 2397.94],
  ["2013/2/21", 2378.82, 2325.95, 2309.17, 2378.82],
  ["2013/2/22", 2322.94, 2314.16, 2308.76, 2330.88],
  ["2013/2/25", 2320.62, 2325.82, 2315.01, 2338.78],
  ["2013/2/26", 2313.74, 2293.34, 2289.89, 2340.71],
  ["2013/2/27", 2297.77, 2313.22, 2292.03, 2324.63],
  ["2013/2/28", 2322.32, 2365.59, 2308.92, 2366.16],
  ["2013/3/1",  2364.54, 2359.51, 2330.86, 2369.65],
  ["2013/3/4",  2332.08, 2273.4, 2259.25, 2333.54],
  ["2013/3/5",  2274.81, 2326.31, 2270.1, 2328.14],
  ["2013/3/6",  2333.61, 2347.18, 2321.6, 2351.44],
  ["2013/3/7",  2340.44, 2324.29, 2304.27, 2352.02],
  ["2013/3/8",  2326.42, 2318.61, 2314.59, 2333.67],
  ["2013/3/11", 2314.68, 2310.59, 2296.58, 2320.96],
  ["2013/3/12", 2309.16, 2286.6, 2264.83, 2333.29],
  ["2013/3/13", 2282.17, 2263.97, 2253.25, 2286.33],
  ["2013/3/14", 2255.77, 2270.28, 2253.31, 2276.22],
  ["2013/3/15", 2269.31, 2278.4, 2250, 2312.08],
  ["2013/3/18", 2267.29, 2240.02, 2239.21, 2276.05],
  ["2013/3/19", 2244.26, 2257.43, 2232.02, 2261.31],
  ["2013/3/20", 2257.74, 2317.37, 2257.42, 2317.86],
  ["2013/3/21", 2318.21, 2324.24, 2311.6, 2330.81],
  ["2013/3/22", 2321.4, 2328.28, 2314.97, 2332],
  ["2013/3/25", 2334.74, 2326.72, 2319.91, 2344.89],
  ["2013/3/26", 2318.58, 2297.67, 2281.12, 2319.99],
  ["2013/3/27", 2299.38, 2301.26, 2289, 2323.48],
  ["2013/3/28", 2273.55, 2236.3, 2232.91, 2273.55],
  ["2013/3/29", 2238.49, 2236.62, 2228.81, 2246.87],
  ["2013/4/1",  2229.46, 2234.4, 2227.31, 2243.95],
  ["2013/4/2",  2234.9, 2227.74, 2220.44, 2253.42],
  ["2013/4/3",  2232.69, 2225.29, 2217.25, 2241.34],
  ["2013/4/8",  2196.24, 2211.59, 2180.67, 2212.59],
  ["2013/4/9",  2215.47, 2225.77, 2215.47, 2234.73],
  ["2013/4/10", 2224.93, 2226.13, 2212.56, 2233.04],
  ["2013/4/11", 2236.98, 2219.55, 2217.26, 2242.48],
  ["2013/4/12", 2218.09, 2206.78, 2204.44, 2226.26],
  ["2013/4/15", 2199.91, 2181.94, 2177.39, 2204.99],
  ["2013/4/16", 2169.63, 2194.85, 2165.78, 2196.43],
  ["2013/4/17", 2195.03, 2193.8, 2178.47, 2197.51],
  ["2013/4/18", 2181.82, 2197.6, 2175.44, 2206.03],
  ["2013/4/19", 2201.12, 2244.64, 2200.58, 2250.11],
  ["2013/4/22", 2236.4, 2242.17, 2232.26, 2245.12],
  ["2013/4/23", 2242.62, 2184.54, 2182.81, 2242.62],
  ["2013/4/24", 2187.35, 2218.32, 2184.11, 2226.12],
  ["2013/4/25", 2213.19, 2199.31, 2191.85, 2224.63],
  ["2013/4/26", 2203.89, 2177.91, 2173.86, 2210.58],
  ["2013/5/2",  2170.78, 2174.12, 2161.14, 2179.65],
  ["2013/5/3",  2179.05, 2205.5, 2179.05, 2222.81],
  ["2013/5/6",  2212.5, 2231.17, 2212.5, 2236.07],
  ["2013/5/7",  2227.86, 2235.57, 2219.44, 2240.26],
  ["2013/5/8",  2242.39, 2246.3, 2235.42, 2255.21],
  ["2013/5/9",  2246.96, 2232.97, 2221.38, 2247.86],
  ["2013/5/10", 2228.82, 2246.83, 2225.81, 2247.67],
  ["2013/5/13", 2247.68, 2241.92, 2231.36, 2250.85],
  ["2013/5/14", 2238.9, 2217.01, 2205.87, 2239.93],
  ["2013/5/15", 2217.09, 2224.8, 2213.58, 2225.19],
  ["2013/5/16", 2221.34, 2251.81, 2210.77, 2252.87],
  ["2013/5/17", 2249.81, 2282.87, 2248.41, 2288.09],
  ["2013/5/20", 2286.33, 2299.99, 2281.9, 2309.39],
  ["2013/5/21", 2297.11, 2305.11, 2290.12, 2305.3],
  ["2013/5/22", 2303.75, 2302.4, 2292.43, 2314.18],
  ["2013/5/23", 2293.81, 2275.67, 2274.1, 2304.95],
  ["2013/5/24", 2281.45, 2288.53, 2270.25, 2292.59],
  ["2013/5/27", 2286.66, 2293.08, 2283.94, 2301.7],
  ["2013/5/28", 2293.4, 2321.32, 2281.47, 2322.1],
  ["2013/5/29", 2323.54, 2324.02, 2321.17, 2334.33],
  ["2013/5/30", 2316.25, 2317.75, 2310.49, 2325.72],
  ["2013/5/31", 2320.74, 2300.59, 2299.37, 2325.53],
  ["2013/6/3",  2300.21, 2299.25, 2294.11, 2313.43],
  ["2013/6/4",  2297.1, 2272.42, 2264.76, 2297.1],
  ["2013/6/5",  2270.71, 2270.93, 2260.87, 2276.86],
  ["2013/6/6",  2264.43, 2242.11, 2240.07, 2266.69],
  ["2013/6/7",  2242.26, 2210.9, 2205.07, 2250.63],
  ["2013/6/13", 2190.1, 2148.35, 2126.22, 2190.1]
}))

//  date          open      close     lowest    highest
MAPVALUE(1, list(value(1), value(2), value(3), value(4)), "data")
MAP_MOVAVG(5, value(2), 5, "MA5")
MAP_MOVAVG(6, value(2), 10, "MA10")
MAP_MOVAVG(7, value(2), 20, "MA20")
MAP_MOVAVG(8, value(2), 30, "MA30")
POPVALUE(2, 3, 4)

CHART(
    chartOption({
        xAxis: { type: "category", data: column(0) },
        yAxis: { min: 2100, max: 2500 },
        dataZoom: [
            { type: "inside", start: 50, end: 100 },
            { show: true, type: "slider", top: "90%", start: 50, end: 100 }
        ],
        toolbox: {
            feature: {
                saveAsImage: { show: true, title: "save as image", name: "stock" }
            }
        },
        series: [
            {
                name: "日K",
                data: column(1),
                type: "candlestick",
                itemStyle: {
                    color: "#ec0000",
                    color0: "#00da3c",
                    borderColor: "#8A0000",
                    borderColor0: "#008F28"
                }
            },
            {
                name: "MA5",
                data: column(2),
                type: "line",
                smooth: true,
                lineStyle: { opacity: 0.5 }
            },
            {
                name: "MA10",
                data: column(3),
                type: "line",
                smooth: true,
                lineStyle: { opacity: 0.5 }
            },
            {
                name: "MA20",
                data: column(4),
                type: "line",
                smooth: true,
                lineStyle: { opacity: 0.5 }
            },
            {
                name: "MA30",
                data: column(5),
                type: "line",
                smooth: true,
                lineStyle: { opacity: 0.5 }
            }
        ]
    })
)
```

**설명**: 이동평균 지표 4종(MA5, MA10, MA20, MA30)을 함께 표시하는 주가지수 캔들스틱 차트입니다. dataZoom으로 이동·확대가 가능하고, 상승(초록)과 하락(빨강) 캔들에 사용자 정의 색상을 적용합니다.

**핵심 포인트**:
- `MAP_MOVAVG()`가 서로 다른 구간의 이동평균을 계산합니다
- `dataZoom`이 슬라이더로 대화형 확대를 제공합니다
- 사용자 정의 색상으로 상승과 하락을 구분합니다
- 여러 선 시리즈를 캔들 위에 겹쳐 추세를 분석합니다

---

## 3. 거래량이 있는 다우존스 지수

거래량 막대와 기술적 지표를 함께 표시하는 고급 캔들스틱 차트입니다.

```js
CSV( file("https://docs.machbase.com/assets/example/stock-DJI.csv") )
DROP(1) // drop header
MAPVALUE(0, value(0), "date")
MAPVALUE(1, parseFloat(value(1)), "open")
MAPVALUE(2, parseFloat(value(2)), "close")
MAPVALUE(3, parseFloat(value(3)), "lowest")
MAPVALUE(4, parseFloat(value(4)), "highest")
MAPVALUE(5, parseFloat(value(5)), "volume")

MAP_MOVAVG(6, value(2), 5, "MA5")
MAP_MOVAVG(7, value(2), 10, "MA10")
MAP_MOVAVG(8, value(2), 20, "MA20")
MAP_MOVAVG(9, value(2), 30, "MA30")

//make data shape 
MAPVALUE(1, list(value(1), value(2), value(3), value(4)), "DJI")
POPVALUE(2,3,4)
//  |    0    1                            2      3   4    5    6
//  +-> date [open,close,lowest,highest]  volume MA5 MA10 MA20 MA30

MAP_DIFF(7, value(2))
//  |    0    1                            2      3   4    5    6     7
//  +-> date [open,close,lowest,highest]  volume MA5 MA10 MA20 MA30  volumeDiff

MAPVALUE(7, value(7) == NULL || value(7) > 0 ? 1 : -1)
//  |    0    1                            2      3   4    5    6     7
//  +-> date [open,close,lowest,highest]  volume MA5 MA10 MA20 MA30  (1 or -1)

MAPVALUE(2, list(value(0), value(2), value(7)))
POPVALUE(7)
//  |    0    1                            2                        3   4    5    6    
//  +-> date [open,close,lowest,highest]  [date, volume, (1 or -1)] MA5 MA10 MA20 MA30

// chart
CHART(
    chartJSCode({
        function tooltipPosition(pos, params, el, elRect, size) {
            const obj = {
                top: 10
            };
            obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
            return obj;
        }
    }),
    chartOption({
        animation: false,
        legend: {
            bottom: 10,
            left: "center",
            data:["Dow-Jones Index", "MA5", "MA10", "MA20", "MA30"]
        },
        tooltip: {
            trigger: "axis",
            axisPointer: { "type": "cross" },
            borderWidth: 1,
            borderColor: "#ccc",
            padding: 10,
            textStyle: {
                color: "#000"
            },
            backgroundColor: "#ffff"
            // ,"position": tooltipPosition
        },
        axisPointer: {
            link: [
                { xAxisIndex: "all"}
            ],
            label: {
                backgroundColor: "#aaa"
            }
        },
        toolbox: {
            feature: {
                saveAsImage: { show: true, title: "save as image", name: "dji" },
                dataZoom: {
                    yAxisIndex: false,
                    title: { zoom: "zoom", back: "restore"}
                },
                brush: {
                    type: ["lineX", "clear"],
                    title: { lineX: "Horizontal selection", clear: "Clear selection"}
                }
            }
        },
        brush: {
            xAxisIndex: "all",
            brushLink: "all",
            outOfBrush: {
                colorAlpha: 0.1
            }
        },
        visualMap: {
            show: false,
            seriesIndex: 1,
            dimension: 2,
            pieces: [
                { value: 1, color: "#ec0000" }, 
                { value: -1, color: "#00da3c" }
            ]
        },
        grid: [
            {
                left: "10%",
                right: "8%",
                height: "50%"
            },
            {
                left: "10%",
                right: "8%",
                top: "65%",
                height: "16%"
            }
        ],
        dataZoom: [
            {
                type: "inside",
                xAxisIndex: [0, 1],
                start: 98,
                end: 100
            },
            {
                show: true,
                type: "slider",
                xAxisIndex: [0, 1],
                top: "85%",
                start: 98,
                end: 100
            }
        ],
        xAxis: [
            {
                type: "category",
                data: column(0),
                boundaryGap: false,
                axisLine: {onZero: false},
                splitLine: {show: false},
                min: "dataMin",
                max: "dataMax",
                axisPointer: {
                    z: 100
                }
            },
            {
                type: "category",
                gridIndex: 1,
                data: column(0),
                boundaryGap: false,
                axisLine: { onZero: false },
                axisTick: { show: false },
                splitLine: { show: false },
                axisLabel: { show: false},
                min: "dataMin",
                max: "dataMax",
                axisPointer: {
                    z: 100
                }
            }
        ],
        yAxis: [
            {
                scale: true,
                splitArea: {
                    show: true
                }
            },
            {
                scale: true,
                gridIndex: 1,
                splitNumber: 2,
                axisLabel: { show: false },
                axisLine: { show: false },
                axisTick: { show: false },
                splitLine: { show: false }
            }
        ],
        series: [
            {
                name: "Dow-Jones Index",
                type: "candlestick",
                data: column(1),
                smooth: true,
                itemStyle: {
                    color: "#00da3c",
                    color0: "#ec0000",
                    borderColor: "#00da3c",
                    borderColor0: "#ec0000"
                }
            },
            {
                name: "Volume",
                type: "bar",
                data: column(2),
                xAxisIndex: 1,
                yAxisIndex: 1
            },
            {
                name: "MA5",
                type: "line",
                data: column(3),
                lineStyle: {
                    opacity: 0.5
                }
            },
            {
                name: "MA10",
                type: "line",
                data: column(4),
                lineStyle: {
                    opacity: 0.5
                }
            },
            {
                name: "MA20",
                type: "line",
                data: column(5),
                lineStyle: {
                    opacity: 0.5
                }
            },
            {
                name: "MA30",
                type: "line",
                data: column(6),
                lineStyle: {
                    opacity: 0.5
                }
            }
        ]
    }),
    chartDispatchAction({
        type: "brush",
        areas:[
            {
                brushType: "lineX",
                coordRange: ["2016-06-02", "2016-06-20"],
                xAxisIndex: 0
            }
        ]
    })
)
```

**설명**: 캔들스틱 가격 데이터와 별도 그리드의 거래량 막대를 결합한 전문가용 주가 차트입니다. 외부 CSV 파일에서 다우존스 지수 데이터를 불러와 여러 기술적 지표와 고급 상호작용 기능을 제공합니다.

**핵심 포인트**:
- 이중 그리드 배치: 위는 가격, 아래는 거래량
- `MAP_DIFF()`가 거래량 변화 방향을 계산합니다
- `visualMap`이 가격 변동 방향에 따라 거래량 막대에 색을 입힙니다
- 브러시 도구로 특정 기간을 선택할 수 있습니다
- `chartDispatchAction()`이 로드 시 날짜 범위를 미리 선택합니다
- 두 그리드의 확대·이동이 연동됩니다
- 툴팁 위치를 지정하는 사용자 정의 함수
