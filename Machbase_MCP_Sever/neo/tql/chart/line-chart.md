# Machbase Neo Line Chart

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
| `HTTP()` | HTTP 요청 | `HTTP('GET https://example.com/data.csv')` |
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
| `FILTER()` | 레코드 필터링 | `FILTER(value(0) > 10)` |
| `DROP()` | 앞의 N개 레코드 버리기 | `DROP(1)` |
| `SCRIPT()` | JavaScript 처리 | `SCRIPT({}, { /* process */ }, {})` |

---

### SINK - 데이터 출력

**데이터를 출력하거나 저장하는** 함수 (파이프라인 끝)

| 함수 | 용도 | 예시 |
|----------|---------|---------|
| `CHART()` | 차트 생성 | `CHART(chartOption({...}))` |
| `CSV()` | CSV 출력 | `CSV()` |
| `JSON()` | JSON 출력 | `JSON()` |
| `HTML()` | HTML output | `HTML(template({...}))` |
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

## 1. 기본 선 차트

여러 데이터 소스 방식을 보여주는 단순한 선 차트입니다.

### Using FAKE

```js
FAKE( linspace(0, 360, 100))
// |   0
// +-> x
// |
MAPVALUE(1, sin((value(0)/180)*PI))
// |   0   1
// +-> x   sin(x)
// |
CHART(
    chartOption({
        xAxis: {
            type: "category",
            data: column(0)
        },
        yAxis: {},
        series: [
            {
                type: "line",
                data: column(1)
            }
        ]
    })
)
```

### SCRIPT 사용

```js
SCRIPT({
    for( x = 0; x < 360; x+=3.6) {
        $.yield(x, Math.sin(x/180*Math.PI));
    }
})
CHART(
    chartOption({
        xAxis: {
            type: "category",
            data: column(0)
        },
        yAxis: {},
        series: [
            {
                type: "line",
                data: column(1)
            }
        ]
    })
)
```

### Using SQL

**먼저 데이터를 준비합니다:**

```js
FAKE( arrange(1, 100, 1))
// |   0
// +-> seq
// |
MAPVALUE(1, sin((2*PI*value(0)/100)))
// |   0       1
// +-> seq     value
// |
MAPVALUE(0, timeAdd("now-100s", strSprintf("+%.fs", value(0))))
// |   0       1
// +-> time    value
// |
PUSHVALUE(0, "chart-line")
// |   0       1       2
// +-> name    time    value
// |
APPEND(table("example"))
```

**SCRIPT로 데이터 준비**

```js
SCRIPT({
    const gen = require("@jsh/generator");
    const sys = require("@jsh/system");
    ts = (new Date()).getTime() - 100 * 1000; // now - 100s.
    for(x of gen.arrange(1, 100, 1)) {
        y = Math.sin(x/100*2*Math.PI)
        ts += 1000; // add 1 sec.
        $.yield("chart-line", sys.parseTime(ts, "ms"), y);
    }
})
APPEND(table("example"))
```

**조회 후 시각화:**

```js
SQL(`select time, value from example where name = 'chart-line'`)
SCRIPT({
    $.yield([$.values[0], $.values[1]])
})
CHART(
    chartOption({
        xAxis: { type: "time" },
        yAxis: {},
        tooltip: { trigger:"axis" },
        series: [
            {
                type: "line",
                data: column(0)
            }
        ]
    })
)
```

### DB 클라이언트와 함께 SCRIPT 사용

```js
SCRIPT({
    db = require("@jsh/db");
    cli = new db.Client();
    conn = cli.connect();
    rows = conn.query(`select time, value from example where name = 'chart-line'`)
    data = [];
    for( r of rows) {
        data.push([r.time, r.value]);
    }
    $.yield({
        xAxis: { type: "time" },
        yAxis: {},
        tooltip: { trigger:"axis" },
        series: [
            {
                type: "line",
                data: data,
            }
        ]
    })
})
CHART()
```

### HTML 템플릿 사용

```html
SQL(`select time, value from example where name = 'chart-line'`)
SCRIPT({
    data = [];
}, {
    data.push([$.values[0], $.values[1]]);
}, {
    $.yield(data); 
})
HTML(template({
    <span>
        <script src="/web/echarts/echarts.min.js"></script>
        <div id='xyz' style="width:600px;height:400px;"></div>
        <script>
            var data = {{ .Values }};
            var chartDom = document.getElementById('xyz');
            var myChart = echarts.init(chartDom);
            var option = {
                xAxis: { type: "time" },
                yAxis: {},
                tooltip: { trigger:"axis" },
                series: [
                    {type: 'line',  data: data[0], symbol:"none"}
                ]
            };
            option && myChart.setOption(option);
        </script>
    </span>
}))
```

**설명**: 다섯 가지 방식을 보여주는 기본 선 차트입니다:
- **FAKE**: 테스트 데이터 생성
- **SCRIPT**: 사용자 정의 JavaScript 로직
- **SQL**: 파이프라인 처리를 곁들인 데이터베이스 쿼리
- **DB 클라이언트와 SCRIPT**: `@jsh/db` 모듈로 데이터베이스 직접 접근
- **HTML 템플릿**: ECharts가 내장된 독립 HTML 출력

---

## 2. 기본 영역 차트

곡선 아래를 채운 선 차트입니다.

```js
FAKE( json({
    ["Mon", 820],
    ["Tue", 932],
    ["Wed", 901],
    ["Thu", 934],
    ["Fri", 1290],
    ["Sat", 1330],
    ["Sun", 1320]
}) )
// |   0      1
// +-> day    value
// |
CHART(
    chartOption({
        legend:{ show:false },
        xAxis: { type:"category", data: column(0) },
        yAxis: {},
        series:[
            { type: "line", smooth:false, color:"#7585CE", areaStyle:{}, data: column(1) }
        ]
    })
)
```

**설명**: 주간 데이터를 보여주는 영역 차트입니다. `areaStyle:{}` 옵션이 선 아래 영역을 채웁니다.

---

## 3. 누적 선 차트

여러 선 시리즈를 위로 쌓아 올린 차트입니다.

```js
FAKE( json({
    ["Mon", 120, 220, 150, 320, 820],
    ["Tue", 132, 182, 232, 332, 932],
    ["Wed", 101, 191, 201, 301, 901],
    ["Thu", 134, 234, 154, 334, 934],
    ["Fri",  90, 290, 190, 390, 1290],
    ["Sat", 230, 330, 330, 330, 1330],
    ["Sun", 210, 310, 410, 320, 1320]
}) )
// |   0      1       2      3      4       5
// +-> day    email   ads    video  direct  search
// |
CHART(
    chartOption({
        xAxis: { data: column(0) },
        yAxis: {},
        series: [
            {type: "line", data: column(1), smooth:false, name: "email", stack: "total"},
            {type: "line", data: column(2), smooth:false, name: "ads", stack: "total"},
            {type: "line", data: column(3), smooth:false, name: "video", stack: "total"},
            {type: "line", data: column(4), smooth:false, name: "direct", stack: "total"},
            {type: "line", data: column(5), smooth:false, name: "search", stack: "total"}
        ]
    })
)
```

**설명**: 여러 트래픽 유입 경로를 보여주는 누적 선 차트입니다. 모든 시리즈가 `stack: "total"`을 공유해 값이 쌓입니다.

---

## 4. 누적 영역 차트

최상단 시리즈에 라벨이 붙은 누적 영역 차트입니다.

```js
FAKE( json({
    ["Mon", 120, 220, 150, 320, 820],
    ["Tue", 132, 182, 232, 332, 932],
    ["Wed", 101, 191, 201, 301, 901],
    ["Thu", 134, 234, 154, 334, 934],
    ["Fri",  90, 290, 190, 390, 1290],
    ["Sat", 230, 330, 330, 330, 1330],
    ["Sun", 210, 310, 410, 320, 1320]
}) )
// |   0      1       2      3      4       5
// +-> day    email   ads    video  direct  search
// |
CHART(
    chartOption({
        xAxis: {data: column(0)},
        yAxis: {},
        animation: false,
        series: [
            {type: "line", data:column(1), name: "email", stack: "total", areaStyle:{} },
            {type: "line", data:column(2), name: "ads", stack: "total", areaStyle:{} },
            {type: "line", data:column(3), name: "video", stack: "total", areaStyle:{} },
            {type: "line", data:column(4), name: "direct", stack: "total", areaStyle:{} },
            {type: "line", data:column(5), name: "search", stack: "total", areaStyle:{},
                label: {show: true, position: "top"}
            }
        ]
    })
)
```

**설명**: 누적 선 차트와 비슷하지만 영역이 채워집니다. 최상단 시리즈는 값을 라벨로 표시합니다.

---

## 5. Area Pieces

visualMap으로 구간별 색을 다르게 한 영역 차트입니다.

```js
SCRIPT({
    data = [
        ["2019-10-10", 200], ["2019-10-11", 560], ["2019-10-12", 750],
        ["2019-10-13", 580], ["2019-10-14", 250], ["2019-10-15", 300],
        ["2019-10-16", 450], ["2019-10-17", 300], ["2019-10-18", 100]
    ];
    $.yield({
      title: { text: "Area Pieces" },
      xAxis: { type: "category", boundaryGap: false },
      yAxis: { type: "value", boundaryGap: [0, "30%"] },
      visualMap:{
        type: "piecewise",
        show: false,
        dimension: 0,
        seriesIndex: 0,
        pieces: [
          { gt: 1, lt: 3, color: "rgba(0, 0, 180, 0.4)" },
          { gt: 5, lt: 7, color: "rgba(0, 0, 180, 0.4)" }
        ]
      },
      series: [
        {
          type: "line",
          smooth: 0.6,
          symbol: "none",
          data: data,
          lineStyle: { color: "#5470C6", width: 5 },
          areaStyle:{},
          markLine: {
            symbol: ["none", "none"],
            label: { show: false },
            data: [{ xAxis: 1 }, { xAxis: 3 }, { xAxis: 5 }, { xAxis: 7 }]
          }
        }   
      ]
    })
})
CHART()
```

```js
FAKE(
  json({
        ["2019-10-10", 200], ["2019-10-11", 560], ["2019-10-12", 750],
        ["2019-10-13", 580], ["2019-10-14", 250], ["2019-10-15", 300],
        ["2019-10-16", 450], ["2019-10-17", 300], ["2019-10-18", 100]
  })
)
// |   0      1
// +-> date   value
// |
MAPVALUE(0, list(value(0), value(1)))
// |   0               1
// +-> [date, value]   value
// |
POPVALUE(1)
// |   0
// +-> [date, value]
// |
CHART(
  chartOption({
    title: { text: "Area Pieces" },
    xAxis: { type: "category", boundaryGap: false },
    yAxis: { type: "value", boundaryGap: [0, "30%"] },
    visualMap:{
      type: "piecewise",
      show: false,
      dimension: 0,
      seriesIndex: 0,
      pieces: [
        { gt: 1, lt: 3, color: "rgba(0, 0, 180, 0.4)" },
        { gt: 5, lt: 7, color: "rgba(0, 0, 180, 0.4)" }
      ]
    },
    series: [
      {
        type: "line",
        smooth: 0.6,
        symbol: "none",
        data: column(0),
        lineStyle: {
          color: "#5470C6",
          width: 5
        },
        areaStyle:{},
        markLine: {
          symbol: ["none", "none"],
          label: { show: false },
          data: [{ xAxis: 1 }, { xAxis: 3 }, { xAxis: 5 }, { xAxis: 7 }]
        }
      }   
    ]
  })
)
```

**설명**: `visualMap.pieces`로 특정 구간의 색을 다르게 칠한 영역 차트입니다. MarkLine이 x축의 특정 위치를 강조합니다.

---

## 6. Step Line

계단식 보간을 적용한 선 차트입니다.

```js
SCRIPT({
  days    = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"];
  starts  = [120,132,101,134,90,230,210];
  middles = [220,282,201,234,290,430,410];
  ends    = [450,432,401,454,590,530,510];

  $.yield({
    legend: { show:true },
    grid: [{
      left: "3%",
      right: "4%",
      bottom: "3%",
      containLabel: true
    }],
    xAxis: { type: "category", data: days },
    yAxis: {},
    series: [
      {type: "line", data: starts, step: "start", name: "Step Start"},
      {type: "line", data: middles, step: "middle", name: "Step Middle"},
      {type: "line", data: ends, step: "end", name: "Step End"}
    ]
  })
})
CHART()
```

```js
FAKE( json({
  ["Mon", 120, 220, 450],
  ["Tue", 132, 282, 432],
  ["Wed", 101, 201, 401],
  ["Thu", 134, 234, 454],
  ["Fri", 90,  290, 590],
  ["Sat", 230, 430, 530],
  ["Sun", 210, 410, 510]
}) )
CHART(
  chartOption({
    legend: { show:true },
    grid: [{
      left: "3%",
      right: "4%",
      bottom: "3%",
      containLabel: true
    }],
    xAxis: { type: "category", data: column(0) },
    yAxis: {},
    series: [
      {type: "line", data: column(1), step: "start", name: "Step Start"},
      {type: "line", data: column(2), step: "middle", name: "Step Middle"},
      {type: "line", data: column(3), step: "end", name: "Step End"}
    ]
  })
)
```

**설명**: start, middle, end 세 가지 계단 보간 방식을 보여주는 계단식 선 차트입니다.

---

## 7. 다중 X축

서로 다른 기간을 비교하기 위해 x축을 두 개 사용하는 차트입니다.

```js
FAKE(csv(`2015-1,2.6
2015-2,5.9
2015-3,9.0
2015-4,26.4
2015-5,28.7
2015-6,70.7
2015-7,175.6
2015-8,182.2
2015-9,48.7
2015-10,18.8
2015-11,6.0
2015-12,2.3
2016-1,3.9
2016-2,5.9
2016-3,11.1
2016-4,18.7
2016-5,48.3
2016-6,69.2
2016-7,231.6
2016-8,46.6
2016-9,55.4
2016-10,18.4
2016-11,10.3
2016-12,0.7
`))
PUSHVALUE(1, value(0))
// | 0        1         2
// + YYYY-M   YYYY-M    value
// |
MAPVALUE(1, strHasPrefix(value(1), "2015-") ? "2015" : value(1))
MAPVALUE(1, strHasPrefix(value(1), "2016-") ? "2016" : value(1))
// | 0        1         2
// + YYYY-M   YYYY      value
// |
PUSHVALUE(2, strSub(value(0), 5) )
// | 0        1         2         3
// + YYYY-M   YYYY      Month     value
// |
GROUP(
    by(parseFloat(value(2))),
    max(value(3), where(value(1) == "2016")),
    max(value(3), where(value(1) == "2015")),
    lazy(true)
)
// | 0        1              2
// + Month    2015-value     2016-value
// |
MAPVALUE(1, list(strSprintf("2015-%.f",value(0)), value(1)))
MAPVALUE(2, list(strSprintf("2016-%.f",value(0)), value(2)))
// | 0        1                         2
// + Month    ["2015-M", 2015-value]    ["2015-M", 2016-value]
// |
CHART(
    chartJSCode({
        function colors() {
            return ['#5470C6', '#EE6666'];
        }
        function labelformat (params) {
            return (
                'Precipitation  ' +
                params.value +
                (params.seriesData.length ? '：' + params.seriesData[0].data : '')
            );
        }
    }),
    chartOption({
        color: colors(),
        tooltip: {
            trigger: "none",
            axisPointer: {
                type: "cross"
            }
        },
        legend: {},
        grid: {
            top: 70,
            bottom: 50
        },
        xAxis: [
            {
                type: "category",
                axisTick: {
                    alignWithLabel: true
                },
                axisLine: {
                    onZero: false,
                    lineStyle: {
                        color: colors()[1]
                    }
                },
                axisPointer: {
                    label: {
                        formatter: labelformat
                    }
                }
            },
            {
                type: "category",
                axisTick: {
                    alignWithLabel: true
                },
                axisLine: {
                    onZero: false,
                    lineStyle: {
                        color: colors()[0]
                    }
                },
                axisPointer: {
                    label: {
                        formatter: labelformat
                    }
                }
            }
        ],
        yAxis: [
            { type: "value" }
        ],
        series: [
            {
                name: "Precipitation(2015)",
                type: "line",
                xAxisIndex: 1,
                smooth: true,
                emphasis: {
                    focus: "series"
                },
                data: column(1)
            },
            {
                name: "Precipitation(2016)",
                type: "line",
                xAxisIndex: 0,
                smooth: true,
                emphasis: {
                    focus: "series"
                },
                data: column(2)
            }
        ]
    })
)
```

**설명**: 2015년과 2016년 월별 데이터를 비교하는 이중 x축 차트입니다. 각 시리즈가 서로 다른 x축 인덱스를 사용합니다.

---

## 8. 다중 Y축

서로 다른 측정 단위를 위해 y축을 세 개 사용하는 차트입니다.

```js
FAKE(json({
    ["Month", "Evaporation", "Precipitation", "Temperature"],
    ["Jan", 2.0,   2.6,   2.0],
    ["Feb", 4.9,   5.9,   2.2],
    ["Mar", 7.0,   9.0,   3.3],        
    ["Apr", 23.2,  26.4,  4.5],         
    ["May", 25.6,  28.7,  6.3],         
    ["Jun", 76.7,  70.7,  10.2],        
    ["Jul", 135.6, 175.6, 20.3],         
    ["Aug", 162.2, 182.2, 23.4],         
    ["Sep", 32.6,  48.7,  23.0],         
    ["Oct", 20.0,  18.8,  16.5],         
    ["Nov", 6.4,   6.0,   12.0],        
    ["Dec", 3.3,   2.3,   6.2]  
}))

CHART(
  chartJSCode({
    const colors = ['#5470C6', '#91CC75', '#EE6666'];
  }),
  chartOption({
    color: colors,
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "cross"
      }
    },
    grid: { right: "23%" },
    toolbox: {
      feature: {
        dataView: { show: true, readOnly: false },
        restore: { show: true },
        saveAsImage: { show: true }
      }
    },
    legend: { bottom: 10, data: [ column(1)[0], column(2)[0], column(3)[0]] },
    xAxis: [
        {
          type: "category",
          axisTick: {
            alignWithLabel: true
          },
          data: column(0).slice(1)
        }
      ],
    yAxis: [
      {
        type: "value",
        name: "Evaporation",
        position: "right",
        alignTicks: true,
        axisLine: { show: true, lineStyle: { color: colors[0] } },
        axisLabel: { formatter: "{value} ml" }
      },
      {
        type: "value",
        name: "Precipitation",
        position: "right",
        alignTicks: true,
        offset: 80,
        axisLine: { show: true, lineStyle: { color: colors[1] } },
        axisLabel: { formatter: "{value} ml" }
      },
      {
        type: "value",
        name: "Temperature",
        position: "left",
        alignTicks: true,
        axisLine: { show: true, lineStyle: { color: colors[2] } },
        axisLabel: { formatter: "{value} °C" }
      }
    ],
    series: [
      {
        name: "Evaporation",
        type: "bar",
        data: column(1).slice(1)
      },
      {
        name: "Precipitation",
        type: "bar",
        yAxisIndex: 1,
        data: column(2).slice(1)
      },
      {
        name: "Temperature",
        type: "line",
        yAxisIndex: 2,
        data: column(3).slice(1)
      }
    ]
  })
)
```

**설명**: 단위가 다른 값(ml, °C)을 위해 y축 3개를 두고 막대와 선 차트를 결합합니다. 각 시리즈는 `yAxisIndex`로 특정 y축을 참조합니다.

---

## 9. 기본 혼합 (선 + 막대)

선과 막대를 결합한 차트입니다.

```js
FAKE( linspace(0, 360, 50))
MAPVALUE(1, sin((value(0)/180)*PI))
MAPVALUE(2, cos((value(0)/180)*PI))
CHART(
    chartOption({
        xAxis: { data: column(0) },
        yAxis: {},
        series: [
            {type: "bar", name: "SIN", data: column(1)},
            {type: "line", name: "COS", color:"#093", data: column(2)}
        ]
    })
)
```

**설명**: 사인파와 코사인파를 막대와 선 시리즈로 섞어 보여줍니다.

---

## 10. 대규모 영역 차트

LTTB 알고리즘으로 2만 개 데이터 포인트를 효율적으로 렌더링합니다.

```js
FAKE(linspace(0,19999,20000))
// |   0
// +-- n
// |         -42109200000000000 = epoch "1968/09/01" and add a day
PUSHVALUE(0, -42109200000000000 + value(0)*3600*24*1000000000)
// |   0              1
// +-- daily-epoch    n
// |         convert from epoch to time
MAPVALUE(0, time(value(0)))
// |   0         1
// +-- time      n
// |         convert time to date string
MAPVALUE(0, strTime(value(0), sqlTimeformat("YYYY/MM/DD"), tz("Local")))
// |   0         1
// +-- date      n
// |         random values
MAPVALUE(1, sin(value(1)/20000 * 3*PI) * 300 + (100*random())+50)
// |   0         1
// +-- date      value
// |   
CHART(
    chartJSCode({
        function position(pt) {
            return [pt[0], '10%'];
        }
        function areaColor() {
            return new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
                offset: 0,
                color: 'rgb(255, 158, 68)'
            },
            {
                offset: 1,
                color: 'rgb(255, 70, 131)'
            }
            ]);
        }
    }),
    chartOption({
        tooltip: {
            trigger: "axis",
            position: position
        },
        title: {
            left: "center",
            text: "Large Area Chart"
        },
        toolbox: {
            feature: {
                dataZoom: {
                    yAxisIndex: "none"
                },
                restore: {},
                saveAsImage: {}
            }
        },
        xAxis: {
            type: "category",
            boundaryGap: false,
            data: column(0)
        },
        yAxis: {
            type: "value",
            boundaryGap: [0, "100%"]
        },
        dataZoom: [
            {
                type: "inside",
                start: 0,
                end: 10
            },
            {
                start: 0,
                end: 10
            }
        ],
        series: [
            {
                name: "Fake Data",
                type: "line",
                symbol: "none",
                sampling: "lttb",
                itemStyle: {
                    color: "rgb(255, 70, 131)"
                },
                areaStyle: {
                    color: areaColor()
                },
                data: column(1)
            }
        ]
    })
)
```

**설명**: `sampling: "lttb"`(Largest-Triangle-Three-Buckets 알고리즘)로 2만 개 포인트의 대용량 데이터를 효율적으로 렌더링합니다. DataZoom으로 탐색할 수 있습니다.

---

## 11. 데이터 변환

외부 CSV 데이터를 변환하고 필터링합니다.

```js
CSV( file("https://docs.machbase.com/assets/example/life-expectancy-table.csv") )
DROP(1) // skip header line
// |   0          1                 2            3         4
// +-> income     life expectancy   population   Country   Year
// |
POPVALUE(1,2)
// |   0          1         2
// +-> income     Country   Year
// |
FILTER( value(1) in ("Germany", "France") )
// |   0          1         2
// +-> income     Country   Year
// |
MAPVALUE(0, parseFloat(value(0)))
// |   0          1         2
// +-> income     Country   Year
// |
GROUP(
    by(value(2)),
    max(value(0), where( value(1) == "Germany" )),
    max(value(0), where( value(1) == "France" ))
)
// |   0      1               2
// +-> Year   Germany-income  France-income
// |
CHART(
    chartOption({
        xAxis: { name: "Year", type: "category", data: column(0) },
        yAxis: { name: "Income"},
        legend: { show: true },
        tooltip: {
            trigger: "axis",
            formatter:"{b}<br/> {a0}:{c0}<br/> {a1}:{c1}"
        },
        series: [
            {
                type: "line",
                name: "Germany",
                showSymbol: false,
                data: column(1),
                tooltip: ["income"]
            },
            {
                type: "line",
                name: "France",
                showSymbol: false,
                data: column(2),
                tooltip: ["income"]
            }
        ]
    })
)
```

**설명**: 외부 CSV를 불러와 독일과 프랑스만 걸러내고, 연도별로 묶어 소득 추이를 비교합니다.

---

## 12. 항공 승객 수

외부 CSV의 시계열 데이터를 처리합니다.

```js
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

**설명**: 소수 연도 형식(예: 1949.08)을 "YYYY/M" 형식으로 변환해 항공 승객 데이터를 그립니다.

---

## 13. 직교 좌표계

[x, y] 좌표 쌍을 사용하는 선 차트입니다.

```js
FAKE(json({
    [10, 40],
    [50, 100],
    [40, 20]
}))
MAPVALUE(0, list(value(0), value(1)))
POPVALUE(1)
CHART(
    chartOption({
        title: { text: "Line Chart in Cartesian Coordinate System"},
        xAxis: {},
        yAxis: {},
        series: [
            { type: "line", data: column(0)}
        ]
    })
)
```

**설명**: 별도의 x축 카테고리 대신 [x, y] 좌표 쌍을 사용하는 단순한 선 차트입니다.
