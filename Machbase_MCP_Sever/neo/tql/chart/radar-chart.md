# Machbase Neo Radar Chart

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

### 레이더 차트 데이터 형식

레이더 차트에는 다음이 필요합니다:
- **Indicator(지표)**: 축의 이름과 최댓값 정의
- **Data**: 지표 개수와 길이가 맞는 값 배열

예:
```js
radar: {
    indicator: [
        { name: "Axis1", max: 100 },
        { name: "Axis2", max: 200 }
    ]
}
data: [
    { name: "Series1", value: [80, 150] }
]
```

---

## 1. 기본 레이더 차트

배정 예산과 실제 지출을 비교하는 표준 레이더 차트입니다.

```js
//                       sales, admin, it,  cs,   dev,   mkt
FAKE(json({
    ["Allocated Budget", 4200, 3000, 20000, 35000, 50000, 18000],
    ["Actual Spending"  , 5000, 14000, 28000, 26000, 42000, 21000]
}))

MAPVALUE(1, list(value(1), value(2), value(3), value(4), value(5), value(6)))
MAPVALUE(1, dict("name", value(0), "value", value(1)))
POPVALUE(2,3,4,5,6)
CHART(
    chartOption({
        title: { "text": "Basic Radar Chart" },
        legend: {
            data: column(0),
            top: "95%"
        },
        radar: {
            indicator: [
                { name: "Sales", max: 6500 },
                { name: "Administration", max: 16000 },
                { name: "Information Technology", max: 30000 },
                { name: "Customer Support", max: 38000 },
                { name: "Development", max: 52000 },
                { name: "Marketing", max: 25000 }
            ]
        },
        series: [
            {
                name: "Budget vs spending",
                type: "radar",
                data: column(1)
            }
        ]
    })
)
```

**설명**: 6개 부서의 배정 예산과 실제 지출을 비교하는 기본 레이더 차트입니다. 각 축이 부서 하나를 나타내고, 두 개의 다각형이 예산과 지출 패턴을 보여줍니다.

**핵심 포인트**:

**데이터 준비**:
- 원본 데이터: `["Category", val1, val2, val3, val4, val5, val6]`
- `list(value(1)...value(6))`이 값들을 배열로 모읍니다
- `dict("name", ..., "value", ...)`가 객체 형식을 만듭니다
- 결과: `[{name: "Allocated Budget", value: [4200, 3000, ...]}, ...]`

**레이더 설정**:
- `indicator`: 각 축을 정의합니다
  - `name`: 축 라벨(부서 이름)
  - `max`: 해당 축의 최댓값(눈금 기준)
- 지표 6개 = 육각형
- 축마다 독립적인 최댓값을 가집니다

**데이터 매핑**:
- 값 배열의 길이가 지표 개수와 같아야 합니다
- 첫 번째 값 → 첫 번째 지표(Sales)
- 두 번째 값 → 두 번째 지표(Administration)
- 순서가 중요합니다

**시각화**:
- 두 개의 겹치는 다각형
- 파랑: 배정 예산
- 빨강: 실제 지출
- 겹치는 영역은 일치를, 벌어진 부분은 초과·미달 지출을 나타냅니다

**활용 사례**:
- 다차원 비교
- 성과 지표
- 역량 평가
- 제품 기능 비교
- 품질 속성

---

## 2. 커스텀 레이더 차트

원형 모양과 스타일링을 적용한 고도로 커스터마이즈된 레이더 차트입니다.

```js
FAKE( json({
    [100,   8, 0.4,  -80, 2000],
    [ 60,   5, 0.3, -100, 1500]
}))

CHART(
    chartOption({
        color: ["#67F9D8", "#FFE434", "#56A3F1", "#FF917C"],
        title: {
            text: "Customized Radar Chart"
        },
        legend: {},
        radar: [
            {
                indicator: [
                    { text: "Indicator1" },
                    { text: "Indicator2" },
                    { text: "Indicator3" },
                    { text: "Indicator4" },
                    { text: "Indicator5" }
                ],
                center: ["50%", "50%"],
                radius: 200,
                startAngle: 90,
                splitNumber: 4,
                shape: "circle",
                axisName: {
                    formatter: "【{value}】",
                    color: "#428BD4"
                },
                splitArea: {
                    areaStyle: {
                        color: ["#77EADF", "#26C3BE", "#64AFE9", "#428BD4"],
                        shadowColor: "rgba(0, 0, 0, 0.2)",
                        shadowBlur: 10
                    }
                },
                axisLine: {
                    lineStyle: {
                        color: "rgba(211, 253, 250, 0.8)"
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: "rgba(211, 253, 250, 0.8)"
                    }
                }
            },
        ],
        series: [
            {
                type: "radar",
                emphasis: {
                    lineStyle: {
                        width: 4
                    }
                },
                data: [
                    {
                        value: [100, 8, 0.4, -80, 2000],
                        name: "Data A"
                    },
                    {
                        value: [60, 5, 0.3, -100, 1500],
                        name: "Data B",
                        areaStyle: {
                            color: "rgba(255, 228, 52, 0.6)"
                        }
                    }
                ]
            }
        ]
    })
)
```

**설명**: 원형 모양, 그라데이션 배경, 스타일이 적용된 축을 가진 레이더 차트입니다. 레이더 차트의 다양한 스타일링 옵션을 보여줍니다.

**주요 커스터마이즈**:

**모양과 배치**:
- `shape: "circle"`이 원형 거미줄을 만듭니다(기본은 다각형)
- `center: ["50%", "50%"]`로 컨테이너 중앙에 배치합니다
- `radius: 200`으로 크기를 픽셀 단위로 지정합니다
- `startAngle: 90`으로 시작 위치를 회전합니다(90° = 위쪽)
- `splitNumber: 4`가 4개의 동심원을 만듭니다

**축 스타일링**:
- `axisName.formatter: "【{value}】"`가 라벨을 괄호로 감쌉니다
- `axisName.color: "#428BD4"`로 축 라벨을 파랗게 합니다
- `axisLine`이 중심에서 뻗는 방사선을 스타일링합니다
- `splitLine`이 동심원을 스타일링합니다
- 반투명 청록 색상 사용

**배경(분할 영역)**:
- `splitArea.areaStyle.color`가 그라데이션 배열입니다
- 4개 동심 대역에 4가지 색상
- 바깥에서 안쪽으로: 청록 → 시안 → 파랑 → 진한 파랑
- `shadowBlur: 10`이 깊이감을 더합니다

**데이터 시리즈**:
- 값 배열을 직접 지정(데이터 구조에 name 없음)
- 시리즈마다 `areaStyle`을 지정할 수 있습니다
- "Data B"는 노란 반투명 채움
- `emphasis.lineStyle.width: 4`로 마우스오버 시 선이 굵어집니다

**지표 설정**:
- `name` + `max` 대신 `text`를 사용합니다
- 데이터 값에 따라 자동으로 눈금이 조정됩니다
- 명시적 최댓값을 정의하지 않습니다

**기본형과의 차이**:
- 다각형 대신 원형
- 단색 대신 그라데이션 배경
- 전반적인 사용자 정의 색상
- 명시적 최댓값 없음(자동 스케일)
- dataset 대신 인라인 데이터

**고급 옵션**:
```js
radar: {
    shape: "polygon" | "circle",  // Shape type
    startAngle: 90,                // Rotation (degrees)
    splitNumber: 4,                // Concentric circles
    name: {                        // Axis label styling
        formatter: "【{value}】",
        textStyle: {...}
    },
    axisLine: {...},               // Radial lines
    splitLine: {...},              // Concentric circles
    splitArea: {...}               // Background bands
}
```

**활용 사례**:
- 브랜드 대시보드(사용자 정의 색상)
- 미적 요소가 중요한 발표 자료
- 척도가 서로 다른 다중 지표 분석
- 시각적 임팩트가 중요한 경우
- 다각형보다 원형이 선호되는 경우
