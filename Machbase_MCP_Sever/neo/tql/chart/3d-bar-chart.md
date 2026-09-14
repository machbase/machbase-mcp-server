# Machbase Neo 3D Bar Chart

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

**plugins()**
- `plugins(plugin...)`
- `plugin` *string* 미리 정의된 플러그인 이름 또는 플러그인 모듈의 URL
- 3D 차트에는 `plugins("gl")`을 사용합니다.

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

## 1. Dataset을 사용한 3D 막대

외부 데이터셋을 사용하는 3D 막대 차트입니다.

```js
CSV( file("https://docs.machbase.com/assets/example/life-expectancy-table.csv") )
// |   0        1                 2            3        4
// +-> income   life-expectancy   population   country  year
// |
DROP(1) // drop header
// |
MAPVALUE(0, value(4))
// |   0        1                 2            3        4
// +-> year     life-expectancy   population   country  year
// |
POPVALUE(4)
// |   0        1                 2            3
// +-> year     life-expectancy   population   country
// |
MAPVALUE(1, parseFloat(value(1)) )
MAPVALUE(2, parseFloat(value(2)) )
// |   0        1                 2            3 
// +-> year     life-expectancy   population   country
// |
MAPVALUE(0, list(value(0), value(1), value(2), value(3)))
POPVALUE(1,2,3)
// |   0 
// +-> [year, life-expectancy, population, country]
// |
CHART(
    plugins("gl"),
    chartOption({
        grid3D: {},
        tooltip: {},
        xAxis3D: { type: "category" },
        yAxis3D: { type: "category" },
        zAxis3D: {},
        visualMap: { max: 100000000, dimension: "Population"},
        dataset: {
            dimensions: [
                { name: "Year", type: "ordinal"},
                "Life Expectancy",
                "Population",
                "Country"
            ],
            source: column(0)
        },
        series: [
            {
                type: "bar3D",
                shading: "lambert",
                encode: {
                    x: "Year",
                    y: "Country",
                    z: "Lefe Expectancy",
                    tooltip: [0, 1, 2, 3]
                }
            }
        ]
    })
)
```

**설명**: 외부 CSV 파일을 사용해 연도별·국가별 기대수명 데이터를 표시하는 3D 막대 차트입니다. 데이터 바인딩에 `dataset`을, 인구 기반 색상 매핑에 `visualMap`을 사용합니다.

---

## 2. 누적 3D 막대

여러 시리즈를 쌓아 올린 3D 막대 차트입니다.

```js
FAKE( meshgrid(linspace(0, 10, 11), linspace(0, 10, 11)) )
MAPVALUE(2, list( value(0), value(1), simplex(10, value(0)/5, value(1)/5) * 2 + 4))
MAPVALUE(3, list( value(0), value(1), simplex(20, value(0)/5, value(1)/5) * 2 + 4))
MAPVALUE(4, list( value(0), value(1), simplex(30, value(0)/5, value(1)/5) * 2 + 4))
MAPVALUE(5, list( value(0), value(1), simplex(40, value(0)/5, value(1)/5) * 2 + 4))
POPVALUE(0,1)
CHART(
    plugins("gl"),
    chartOption({
        xAxis3D: { type: "value" },
        yAxis3D: { type: "value" },
        zAxis3D: { type: "value" },
        grid3D: {
            viewControl: {
                // autoRotate: true
            },
            light: {
                main: {
                    shadow: true,
                    quality: "ultra",
                    intensity: 1.5
                }
            }
        },
        series: [
            {
                type: "bar3D",
                data: column(0),
                stack: "stack",
                shading: "lambert",
                emphasis: {
                    label: { show: false }
                }
            },
            {
                type: "bar3D",
                data: column(1),
                stack: "stack",
                shading: "lambert",
                emphasis: {
                    label: { show: false }
                }
            },
            {
                type: "bar3D",
                data: column(2),
                stack: "stack",
                shading: "lambert",
                emphasis: {
                    label: { show: false }
                }
            },
            {
                type: "bar3D",
                data: column(3),
                stack: "stack",
                shading: "lambert",
                emphasis: {
                    label: { show: false }
                }
            }
        ]
    })
)
```

**설명**: 심플렉스 노이즈로 여러 데이터 층을 생성한 누적 3D 막대 차트입니다. 그림자가 있는 고급 조명과 lambert 셰이딩을 이용한 고품질 렌더링이 특징입니다.

---

## 3. 반투명 3D 막대

투명도와 사용자 정의 스타일을 적용한 3D 막대 차트입니다.

```js
FAKE( json({
    [0, 0, 5], [0, 1, 1], [0, 2, 0], [0, 3, 0], [0, 4, 0], [0, 5, 0], [0, 6, 0], [0, 7, 0],
    [0, 8, 0], [0, 9, 0], [0, 10, 0], [0, 11, 2], [0, 12, 4], [0, 13, 1], [0, 14, 1], [0, 15, 3],
    [0, 16, 4], [0, 17, 6], [0, 18, 4], [0, 19, 4], [0, 20, 3], [0, 21, 3], [0, 22, 2], [0, 23, 5],
    [1, 0, 7], [1, 1, 0], [1, 2, 0], [1, 3, 0], [1, 4, 0], [1, 5, 0], [1, 6, 0], [1, 7, 0],
    [1, 8, 0], [1, 9, 0], [1, 10, 5], [1, 11, 2], [1, 12, 2], [1, 13, 6], [1, 14, 9], [1, 15, 11],
    [1, 16, 6], [1, 17, 7], [1, 18, 8], [1, 19, 12], [1, 20, 5], [1, 21, 5], [1, 22, 7], [1, 23, 2],
    [2, 0, 1], [2, 1, 1], [2, 2, 0], [2, 3, 0], [2, 4, 0], [2, 5, 0], [2, 6, 0], [2, 7, 0],
    [2, 8, 0], [2, 9, 0], [2, 10, 3], [2, 11, 2], [2, 12, 1], [2, 13, 9], [2, 14, 8], [2, 15, 10],
    [2, 16, 6], [2, 17, 5], [2, 18, 5], [2, 19, 5], [2, 20, 7], [2, 21, 4], [2, 22, 2], [2, 23, 4],
    [3, 0, 7], [3, 1, 3], [3, 2, 0], [3, 3, 0], [3, 4, 0], [3, 5, 0], [3, 6, 0], [3, 7, 0],
    [3, 8, 1], [3, 9, 0], [3, 10, 5], [3, 11, 4], [3, 12, 7], [3, 13, 14], [3, 14, 13], [3, 15, 12],
    [3, 16, 9], [3, 17, 5], [3, 18, 5], [3, 19, 10], [3, 20, 6], [3, 21, 4], [3, 22, 4], [3, 23, 1],
    [4, 0, 1], [4, 1, 3], [4, 2, 0], [4, 3, 0], [4, 4, 0], [4, 5, 1], [4, 6, 0], [4, 7, 0],
    [4, 8, 0], [4, 9, 2], [4, 10, 4], [4, 11, 4], [4, 12, 2], [4, 13, 4], [4, 14, 4], [4, 15, 14],
    [4, 16, 12], [4, 17, 1], [4, 18, 8], [4, 19, 5], [4, 20, 3], [4, 21, 7], [4, 22, 3], [4, 23, 0],
    [5, 0, 2], [5, 1, 1], [5, 2, 0], [5, 3, 3], [5, 4, 0], [5, 5, 0], [5, 6, 0], [5, 7, 0],
    [5, 8, 2], [5, 9, 0], [5, 10, 4], [5, 11, 1], [5, 12, 5], [5, 13, 10], [5, 14, 5], [5, 15, 7],
    [5, 16, 11], [5, 17, 6], [5, 18, 0], [5, 19, 5], [5, 20, 3], [5, 21, 4], [5, 22, 2], [5, 23, 0],
    [6, 0, 1], [6, 1, 0], [6, 2, 0], [6, 3, 0], [6, 4, 0], [6, 5, 0], [6, 6, 0], [6, 7, 0],
    [6, 8, 0], [6, 9, 0], [6, 10, 1], [6, 11, 0], [6, 12, 2], [6, 13, 1], [6, 14, 3], [6, 15, 4],
    [6, 16, 0], [6, 17, 0], [6, 18, 0], [6, 19, 0], [6, 20, 1], [6, 21, 2], [6, 22, 2], [6, 23, 6]
}) )
MAPVALUE(0, list(value(1), value(0), value(2)))
POPVALUE(1,2)
CHART(
    plugins("gl"),
    chartJSCode({
        var hours = ['12a', '1a', '2a', '3a', '4a', '5a', '6a',
                    '7a', '8a', '9a', '10a', '11a',
                    '12p', '1p', '2p', '3p', '4p', '5p',
                    '6p', '7p', '8p', '9p', '10p', '11p'];
        var days = ['Saturday', 'Friday', 'Thursday',
                    'Wednesday', 'Tuesday', 'Monday', 'Sunday'];
    }),
    chartOption({
        tooltip: {},
        visualMap: {
            max: 20,
            inRange: {
                color: [
                    "#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf",
                    "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"
                ]
            }
        },
        xAxis3D: { type: "category", data: hours },
        yAxis3D: { type: "category", data: days },
        zAxis3D: { type: "value" },
        grid3D: {
            boxWidth: 200,
            boxDepth: 80,
            light: {
                main: {
                    intensity: 1.2
                },
                ambient: {
                    intensity: 0.3
                }
            }
        },
        series: [
            {
                type: "bar3D",
                data: column(0),
                shading: "color",
                label: {
                    show: false,
                    fontSize: 16,
                    borderWidth: 1
                },
                itemStyle: {
                    opacity: 0.6
                },
                emphasis: {
                    label: {
                        fontSize: 20,
                        color: '#900'
                    },
                    itemStyle: {
                        color: '#900'
                    }
                }
            }
        ]
    })
)
```

**설명**: 요일·시간대별 활동량을 보여주는 반투명 3D 막대 차트입니다. 반투명 막대(opacity: 0.6)에 색상 셰이딩과 visualMap 다색 그라데이션을 적용했고, 마우스오버 시 강조 스타일이 적용됩니다.
