# Machbase Neo Boxplot Chart

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
| `BOXPLOT()` | 박스플롯 통계 계산 | `BOXPLOT(value(0), category(value(1)))` |

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

### BOXPLOT() 함수

**문법**: `BOXPLOT(value, [category()], [order()], [boxplotInterp()], [boxplotOutput()])`

*버전 8.0.15부터 사용 가능*

주어진 값들에 대해 박스플롯 통계(Q1, Q3, 중앙값, 최솟값, 최댓값, 이상치)를 계산합니다.

#### 옵션

**category()**
- `category(categoryValue)` - 데이터를 카테고리별로 묶습니다

**order()**
- `order(cat1, cat2, ...)` - 카테고리 순서를 지정합니다

**boxplotInterp()**
- `boxplotInterp(lowerFence, upperFence, outlier)` - 보간 여부를 지정하는 불리언 플래그
- 최솟값/최댓값과 이상치를 계산하는 방식을 제어합니다

**boxplotOutput()**
- `boxplotOutput("chart")` - ECharts용 출력 형식
- ECharts 박스플롯 시리즈와 호환되는 데이터 구조를 생성합니다

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

## 1. 마이컬슨-몰리 실험

마이컬슨-몰리 실험 데이터를 보여주는 박스플롯 차트입니다.

```js
FAKE(json({
    ["A", 850, 740, 900, 1070, 930, 850, 950, 980, 980, 880, 1000, 980, 930, 650, 760, 810, 1000, 1000, 960, 960],
    ["B", 960, 940, 960, 940, 880, 800, 850, 880, 900, 840, 830, 790, 810, 880, 880, 830, 800, 790, 760, 800],
    ["C", 880, 880, 880, 860, 720, 720, 620, 860, 970, 950, 880, 910, 850, 870, 840, 840, 850, 840, 840, 840],
    ["D", 890, 810, 810, 820, 800, 770, 760, 740, 750, 760, 910, 920, 890, 860, 880, 720, 840, 850, 850, 780],
    ["E", 890, 840, 780, 810, 760, 810, 790, 810, 820, 850, 870, 870, 810, 740, 810, 940, 950, 800, 810, 870]
}))
TRANSPOSE(fixed(0))
BOXPLOT(
    value(1),
    category(value(0)),
    boxplotInterp(true, false, true),
    boxplotOutput("chart")
)
CHART(
    chartOption({
        grid: { bottom: "15%" },
        xAxis:{ type:"category", boundaryGap: true, data: column(0) },
        yAxis:{ type:"value", name: "km/s minus 299,000", min:400, splitArea:{ show: true } },
        series:[
            { name: "boxplot", type:"boxplot", data: column(1)},
            { name: "outlier", type:"scatter", data: column(2).flat()},
        ],
        tooltip: { trigger: 'item', axisPointer: { type: 'shadow' } },
        title:[
            {
                text: "Michelson-Morley Experiment",
                left: "center"
            },
            {
                text: "max: Q3 + 1.5 * IQR \nmin: Q1 - 1.5 * IQR",
                borderColor: "#999",
                borderWidth: 1,
                textStyle: { fontWeight: "normal", fontSize: 12, lineHeight: 16 },
                left: "10%", top: "92%"
            }
        ]
    })
)
```

**설명**: 5회의 실험(A~E)에 걸친 마이컬슨-몰리 실험 데이터를 시각화한 박스플롯입니다. 사분위수, 중앙값, 이상치와 함께 속도 측정값의 분포를 보여줍니다. `BOXPLOT()`에 `boxplotInterp(true, false, true)`를 지정해 이상치 계산 방식을 조정하고, 이상치를 산점으로 표시합니다.

**핵심 포인트**:
- `TRANSPOSE(fixed(0))`이 카테고리 기반 분석을 위해 데이터 구조를 변환합니다
- `boxplotOutput("chart")`가 ECharts 호환 형식으로 데이터를 만듭니다
- 두 개의 시리즈: 주 분포용 boxplot과 이상치용 scatter
- `column(2).flat()`이 이상치 배열을 평탄화해 올바르게 렌더링되게 합니다

---

## 2. 붓꽃 꽃받침 길이

붓꽃 종별 꽃받침 길이를 분석하는 박스플롯 차트입니다.

```js
CSV(file("https://docs.machbase.com/assets/example/iris.csv"))
MAPVALUE(4, strToUpper(strTrimPrefix(value(4), "Iris-")))

BOXPLOT(
    value(0),
    category(value(4)),
    order("SETOSA", "VERSICOLOR", "VIRGINICA"),
    boxplotOutput("chart")
)

CHART(
    chartOption({
        grid: { bottom: "15%" },
        xAxis:{ type:"category", boundaryGap: true, data: column(0) },
        yAxis:{ type:"value", name: "sepal length", min:4, max:8, splitArea:{ show: true } },
        series:[
            { name: "sepal length", type:"boxplot", data: column(1)},
            { name: "outlier", type:"scatter", data: column(2).flat()},
        ],
        tooltip: { trigger: 'item', axisPointer: { type: 'shadow' } },
        legend: {show: true, bottom:'2%'},
        title:[ { text: "Iris Sepal Length", left: "center" } ]
    })
)
```

**설명**: 세 가지 붓꽃 종(Setosa, Versicolor, Virginica)의 꽃받침 길이 분포를 비교하는 박스플롯입니다. 외부 CSV 파일에서 데이터를 불러와 종별 꽃받침 측정값의 통계적 분포를 분석합니다.

**핵심 포인트**:
- `CSV(file(...))`로 외부 소스에서 붓꽃 데이터셋을 불러옵니다
- `strTrimPrefix()`로 "Iris-" 접두를 제거해 종 이름을 정리합니다
- `order("SETOSA", "VERSICOLOR", "VIRGINICA")`로 카테고리 순서를 일관되게 유지합니다
- `value(0)`은 꽃받침 길이 측정값입니다
- `value(4)`는 종 카테고리입니다
- 박스플롯 분포와 이상치 점을 각각 별도 시리즈로 표시합니다
