# Machbase Neo Bar Chart

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

## 1. 기본 막대 차트

기본 막대 차트 예제입니다.

```js
FAKE( linspace(0, 360, 50))
MAPVALUE(2, sin((value(0)/180)*PI))
CHART(
    chartOption({
        xAxis:{ "data": column(0) },
        yAxis:{},
        series: [
            { type: "bar", data: column(1)}
        ]
    })
)
```

**설명**: 사인 함수를 막대 차트로 시각화합니다.

---

## 2. 카테고리 막대 (GROUP-by-lazy)

카테고리별로 묶은 막대 차트입니다.

```js
FAKE( json({
    ["2011", "Brazil", 18203],
    ["2011", "Indonesia", 23489],
    ["2011", "USA", 29034],
    ["2011", "India", 104970],
    ["2011", "China", 131744],
    ["2011", "World", 630230],
    ["2022", "Brazil", 19325],
    ["2022", "Indonesia", 23438],
    ["2022", "USA", 31000],
    ["2022", "India", 121594],
    ["2022", "China", 134141],
    ["2022", "World", 681807]
}) )
// |   0      1         2
// +-> year   country   population
// |
MAPVALUE(3, value(0) == "2011" ? value(2) : 0)
// |   0      1         2            3
// +-> year   country   population   2011-population
// |
MAPVALUE(4, value(0) == "2022" ? value(2) : 0)
// |   0      1         2            3                  4
// +-> year   country   population   2011-population   2022-population
// |
POPVALUE(0, 2)
// |   0        1                  2
// +-> country  2011-population   2022-population
// |
GROUP( by(value(0)), max(value(1)), max(value(2)), lazy(true))
// |
CHART(
    chartOption({
        legend: { show:true},
        tooltip: {
            trigger: "axis",
            axisPointer: {
                type: "shadow"
            }
        },
        xAxis: { type: "category", data: column(0) },
        yAxis: { },
        series: [
            { type: "bar", name: "2011", data: column(1) },
            { type: "bar", name: "2022", data: column(2) }
        ]
    })
)
```

**설명**: 2011년과 2022년의 국가별 인구 데이터를 비교하는 그룹 막대 차트입니다.

---

## 3. 접선형 극좌표 막대

극좌표계를 사용하는 막대 차트입니다.

```js
FAKE( json({
    ["A", 2],
    ["B", 1.2],
    ["C", 2.4],
    ["D", 3.6]
}) )

CHART(
    chartOption({
        title: {
            text: "Tangential Polar Bar Label Position (middle)"
        },
        polar: { radius: [30, "80%"] },
        radiusAxis: {
            type: "category",
            data: column(0)
        },
        angleAxis: { max: 4, startAngle: 90 },
        tooltip: {},
        series: {   
            type: "bar",
            coordinateSystem: "polar",
            data: column(1),
            label: {
                show: true,
                position: "middle",
                formatter: "{b}: {c}"
            }
        }
    })
)
```

**설명**: 극좌표를 사용해 막대를 원형으로 배치한 차트입니다.

---

## 4. 음수 값이 있는 막대 차트

음수 값을 포함하는 막대 차트입니다.

```js
FAKE(csv(`day,profit,income,expenses
Mon,200,320,-120
Tue,170,302,-132
Wed,240,341,-101
Thu,244,374,-134
Fri,200,390,-190
Sat,220,450,-230
Sun,210,420,-210
`))

DROP(1) // drop header
MAPVALUE(1, parseFloat(value(1))) // parse float from string
MAPVALUE(2, parseFloat(value(2))) // parse float from string
MAPVALUE(3, parseFloat(value(3))) // parse float from string

CHART(
    chartOption({
        tooltip: {
            trigger: "axis",
            axisPointer: {
                type: "shadow"
            }
        },
        legend: {
            data: ["Profit", "Expenses", "Income"]
        },
        grid: {
            left: "3%",
            right: "4%",
            bottom: "3%",
            containLabel: true
        },
        xAxis: [
            {
                type: "value"
            }
        ],
        yAxis: [
            {
                type: "category",
                axisTick: {
                    show: false
                },
                data: column(0)
            }
        ],
        series: [
            {
                name: "Profit",
                type: "bar",
                label: {
                    show: true,
                    position: "inside"
                },
                emphasis: {
                    focus: "series"
                },
                data: column(1)
            },
            {
                name: "Income",
                type: "bar",
                stack: "Total",
                label: {
                    show: true
                },
                emphasis: {
                    focus: "series"
                },
                data: column(2)
            },
            {
                name: "Expenses",
                type: "bar",
                stack: "Total",
                label: {
                    show: true,
                    position: "left"
                },
                emphasis: {
                    focus: "series"
                },
                data: [-120, -132, -101, -134, -190, -230, -210]
            }
        ]
    })
)
```

**설명**: 이익·수입·지출을 보여주는 차트로, 음수 값(지출)을 누적 형식으로 표시합니다.

---

## 5. 누적 막대 정규화 (백분율)

백분율로 정규화한 누적 막대 차트입니다.

```js
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

**설명**: 각 카테고리의 비중을 백분율로 표시하는 정규화 누적 차트입니다.

---

## 6. 대규모 막대 차트 (50만 건)

대규모 데이터를 다루는 막대 차트입니다.

```js
FAKE(linspace(0,1,1))
CHART(
    chartJSCode({
        const data = generateData(5e5);
        function generateData(count) {
            let baseValue = Math.random() * 1000;
            let time = +new Date(2011, 0, 1);
            let smallBaseValue;
            function next(idx) {
                smallBaseValue =
                    idx % 30 === 0
                        ? Math.random() * 700
                        : smallBaseValue + Math.random() * 500 - 250;
                baseValue += Math.random() * 20 - 10;
                return Math.max(0, Math.round(baseValue + smallBaseValue) + 3000);
            }
            const categoryData = [];
            const valueData = [];
            for (let i = 0; i < count; i++) {
                categoryData.push(
                    echarts.format.formatTime('yyyy-MM-dd\nhh:mm:ss', time, false)
                );
                valueData.push(next(i).toFixed(2));
                time += 1000;
            }
            return {
                categoryData: categoryData,
                valueData: valueData
            };
        }
    }),
    chartOption({
        title: {
            text: "500,000 Data",
            left: 10
        },
        toolbox: {
            feature: {
                dataZoom: {
                    yAxisIndex: false
                },
                saveAsImage: {
                    pixelRatio: 2
                }
            }
        },
        tooltip: {
            trigger: "axis",
            axisPointer: {
                type: "shadow"
            }
        },
        grid: {
            bottom: 90
        },
        dataZoom: [
            {
                "type": "inside"
            },
            {
                "type": "slider"
            }
        ],
        xAxis: {
            data: data.categoryData,
            silent: false,
            splitLine: {
                show: false
            },
            splitArea: {
                show: false
            }
        },
        yAxis: {
            splitArea: {
                show: false
            }
        },
        series: [
            {
                type: "bar",
                data: data.valueData,
                large: true
            }
        ]
    })
)
```

**설명**: 50만 개 데이터 포인트를 효율적으로 렌더링하는 대규모 차트입니다. `dataZoom`으로 확대·축소할 수 있습니다.

---

## 7. Bar Race

시간에 따라 변화하는 애니메이션 막대 차트입니다.

```js
CSV( file("https://docs.machbase.com/assets/example/life-expectancy-table.csv") )
CHART(
    chartOption({
        grid: {
            top: 10,
            bottom: 30,
            left: 150,
            right: 80
        },
        xAxis: {
            max: "dataMax",
            axisLabel: { }
        },
        dataset: {
            source: [],
        },
        yAxis: {
            type: "category",
            inverse: true,
            max: 10,
            axisLabel: {
                show: true,
                fontSize: 14,
                rich: {
                    flag: {
                        fontSize: 25,
                        padding: 5
                    }
                }
            },
            animationDuration: 300,
            animationDurationUpdate: 300
        },
        series: [
            {
                realtimeSort: true,
                type: "bar",
                seriesLayoutBy: "column",
                itemStyle: {
                    color:""
                },
                encode: {
                    x: 0, y: 3
                },
                label: {
                    show: true,
                    precision: 1,
                    position: "right",
                    valueAnimation: true,
                    fontFamily: "monospace"
                }
            }
        ],
        animationDuration: 0,
        animationDurationUpdate: 2000,
        animationEasing: "linear",
        animationEasingUpdate: "linear",
        graphic: {
            elements: [
                {
                    type: "text",
                    right: 40,
                    bottom: 60,
                    style: {
                        text: "loading...",
                        font: "bolder 50px monospace",
                        fill: "rgba(100, 100, 100, 0.25)"
                    },
                    z: 100
                }
            ]
        }
    }),
    chartJSCode({
        fetch("https://fastly.jsdelivr.net/npm/emoji-flags@1.3.0/data.json").then( function(rsp) {
            return rsp.json();
        }).then( function(flags) {
            const data = [];
            for (let i = 0; i < _columns[0].length; ++i) {
                var row = [];
                for (let c = 0; c < _columns.length; ++c) {
                    row.push(_columns[c][i]);
                }
                data.push(row);
            }

            const years = [];
            for (let i = 0; i < data.length; ++i) {
                if (years.length === 0 || years[years.length - 1] !== data[i][4]) {
                    years.push(data[i][4]);
                }
            }

            const updateFrequency = 2000;
            const countryColors = {
                "Australia": "#00008b",
                "Canada": "#f00",
                "China": "#ffde00",
                "Cuba": "#002a8f",
                "Finland": "#003580",
                "France": "#ed2939",
                "Germany": "#000",
                "Iceland": "#003897",
                "India": "#f93",
                "Japan": "#bc002d",
                "North Korea": "#024fa2",
                "South Korea": "#000",
                "New Zealand": "#00247d",
                "Norway": "#ef2b2d",
                "Poland": "#dc143c",
                "Russia": "#d52b1e",
                "Turkey": "#e30a17",
                "United Kingdom": "#00247d",
                "United States": "#b22234"
            };
            function getFlag(countryName) {
                if (!countryName) {
                    return '';
                }
                return (
                    flags.find(function (item) {
                        return item.name === countryName;
                    }) || {}
                ).emoji;
            }
            
            let startIndex = 10;
            let startYear = years[startIndex];
            let option = _chart.getOption()
            option.dataset.source = data.slice(1).filter(function (d) {
                return d[4] === startYear;
            });
            option.xAxis[0].axisLabel.formatter = function (n) {
                return Math.round(n) + '';
            };
            option.yAxis[0].axisLabel.formatter = function (value) {
                return value + "{flag|" + getFlag(value) + "}";
            };
            option.series[0].itemStyle.color = function (param) {
                return countryColors[param.value[3]] || "#5470c6";
            };
            option.graphic[0].elements[0].style.text = startYear;
            _chart.setOption(option);
            for (let i = startIndex; i < years.length - 1; ++i) {
                (function (i) {
                    setTimeout(function () {
                        updateYear(years[i + 1]);
                    }, (i - startIndex) * updateFrequency);
                })(i);
            }
            function updateYear(year) {
                let source = data.slice(1).filter(function (d) {
                    return d[4] === year;
                });
                option.series[0].data = source;
                option.graphic[0].elements[0].style.text = year;
                _chart.setOption(option);
            }
        }).catch(function(err){
            console.warn("data error, fetch resource", err)
        });
    })
)
```

**설명**: 국가별 기대수명 데이터를 시간순 애니메이션으로 보여주는 바 레이스 차트입니다. 외부 CSV 파일과 국기 이모지를 사용합니다.
