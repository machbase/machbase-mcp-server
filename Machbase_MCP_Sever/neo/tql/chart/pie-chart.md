# Machbase Neo Pie Chart

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
| `TRANSPOSE()` | 행을 열로 전치 | `TRANSPOSE()` |

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

### 파이 차트 데이터 형식

**배열 형식**: `[["name", value], ["name2", value2]]`

**객체 형식**: `[{name: "name", value: value}, {name: "name2", value: value2}]`

---

## 1. 기본 파이 차트

비율 분포를 보여주는 표준 파이 차트입니다.

```js
FAKE( json({
    ["Search Engine", 1048 ],
    ["Direct"       ,  735 ],
    ["Email"        ,  580 ],
    ["Union Ads"    ,  484 ],
    ["Video Ads"    ,  300 ]
}) )
MAPVALUE(0, list(value(0), value(1)))
CHART(
    chartOption({
        tooltip: {
            trigger: "item"
        },
        legend: {
            orient: "vertical",
            left: "left"
        },
        dataset: [ { source: column(0) } ],
        series: [
            {
                name: "Access From",
                type: "pie",
                radius: "70%",
                datasetIndex: 0,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: "rgba(0, 0, 0, 0.5)"
                    }
                }
            }
        ]
    })
)
```

**설명**: 트래픽 유입 경로 분포를 표시하는 기본 파이 차트입니다. 각 조각이 전체에서 차지하는 비율을 나타냅니다.

**핵심 포인트**:

**데이터 파이프라인**:
- `json({...})`이 카테고리-값 쌍을 만듭니다
- `list(value(0), value(1))`이 배열로 감쌉니다
- `dataset: [{source: column(0)}]`이 dataset으로 데이터를 바인딩합니다
- 최종 형식: `[["Search Engine", 1048], ["Direct", 735], ...]`

**차트 설정**:
- `type: "pie"`로 파이 차트를 만듭니다
- `radius: "70%"`가 차트 크기를 지정합니다(컨테이너의 70%)
- 값이 하나면 꽉 찬 원형 파이
- `datasetIndex: 0`이 첫 번째 dataset을 참조합니다

**범례**:
- `orient: "vertical"`로 항목을 세로로 쌓습니다
- `left: "left"`로 왼쪽에 배치합니다
- 색상 표시와 함께 카테고리 이름을 보여줍니다

**툴팁**:
- `trigger: "item"`으로 조각에 마우스를 올리면 표시됩니다
- 카테고리 이름과 값을 표시합니다
- 백분율은 자동으로 표시됩니다

**강조(마우스오버)**:
- `shadowBlur: 10`이 흐림 효과를 더합니다
- `shadowColor`가 깊이감을 만듭니다
- 마우스를 올리면 조각이 약간 커집니다

---

## 2. 도넛 차트

가운데가 비어 있는 파이 차트(도넛/링 차트)입니다.

```js
FAKE( json({
    ["Search Engine", 1048 ],
    ["Direct"       ,  735 ],
    ["Email"        ,  580 ],
    ["Union Ads"    ,  484 ],
    ["Video Ads"    ,  300 ]
}) )
MAPVALUE(0, list(value(0), value(1)))
CHART(
    chartOption({
        tooltip: {
            trigger: "item"
        },
        legend: {
            orient: "vertical",
            left: "left"
        },
        dataset: [ { source: column(0) } ],
        series: [
            {
                name: "Access From",
                type: "pie",
                radius: ["40%", "70%"],
                datasetIndex: 0,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: "rgba(0, 0, 0, 0.5)"
                    }
                }
            }
        ]
    })
)
```

**설명**: 가운데가 비어 있는 도넛 차트입니다. radius를 두 값으로 주어 링 모양을 만든다는 점만 파이 차트와 다릅니다.

**핵심 차이**:
- **파이**: `radius: "70%"` (단일 값 = 꽉 찬 원)
- **도넛**: `radius: ["40%", "70%"]` (배열 = 링 모양)
  - 첫 값(40%) = 안쪽 반지름 (구멍을 만듦)
  - 둘째 값(70%) = 바깥 반지름 (차트 크기)
  - 두 값의 차이가 링 두께가 됨

**장점**:
- 가운데 공간에 추가 텍스트·라벨을 넣을 수 있음
- 더 깔끔한 외형
- 여러 시리즈(중첩 링)에 적합
- 시각적 무게감이 덜함

**주요 용도**:
- 중앙에 핵심 지표 표시
- 중첩 비교(여러 개의 링)
- 현대적인 대시보드 미감

---

## 3. 나이팅게일(로즈) 차트

값에 따라 조각의 반지름이 달라지는 파이 차트(나이팅게일/로즈 차트)입니다.

```js
FAKE(csv(`rose 1,rose 2,rose 3,rose 4,rose 5,rose 6,rose 7,rose 8
40,38,32,30,28,26,22,18
`))

TRANSPOSE(header(true))
MAPVALUE(0, dict("name", value(0), "value", value(1)))

CHART(
    chartOption({
        legend: {
            "top": "bottom"
        },
        toolbox: {
            show: true,
            feature: {
                saveAsImage: { show: true, title: "save as image", name: "sample" }
            }
        },
        series: [
            {
                name: "Nightingale Chart",
                type: "pie",
                radius: ["50", "250"],
                center: ["50%", "50%"],
                roseType: "area",
                itemStyle: {
                    borderRadius: 8
                },
                data: column(0)
            }
        ]
    })
)
```

**설명**: 조각의 반지름이 값의 크기를 나타내는 나이팅게일(로즈) 차트입니다. 사망률 데이터 시각화에 이 방식을 사용한 플로렌스 나이팅게일의 이름을 땄습니다.

**핵심 포인트**:

**데이터 준비**:
- `csv(...)`가 헤더와 값이 있는 CSV를 불러옵니다
- `TRANSPOSE(header(true))`가 첫 행을 헤더로 삼아 데이터를 피벗합니다
- `dict("name", ..., "value", ...)`가 객체 형식을 만듭니다
- 결과: `[{name: "rose 1", value: 40}, {name: "rose 2", value: 38}, ...]`

**로즈 차트 설정**:
- `roseType: "area"`가 나이팅게일 모드를 활성화합니다
  - 조각 반지름이 값에 비례
  - 값이 클수록 조각이 길어짐
- `radius: ["50", "250"]`이 최소/최대 반지름을 픽셀로 지정합니다
  - 안쪽: 50px
  - 바깥: 최대 250px (값에 따라 달라짐)
- `itemStyle.borderRadius: 8`이 조각 모서리를 둥글게 합니다

**시각적 인코딩**:
- **각도**: 모든 조각이 동일 (시계처럼)
- **반지름**: 값에 따라 달라짐 (파이와의 핵심 차이)
- 크기 차이를 강조
- 값 비교에는 파이보다 유리

**툴박스**:
- `saveAsImage`가 다운로드 기능을 활성화합니다
- 사용자가 차트를 PNG로 저장할 수 있습니다
- 파일명은 "sample"로 지정

**roseType 옵션**:
- `"area"`: 값에 기반한 반지름
- `"radius"`: 값의 제곱근에 기반한 반지름
- 미지정: 일반 파이 차트

**파이 대비 장점**:
- 값 비교가 쉬움
- 각도와 반지름 모두가 정보를 전달
- 시각적으로 눈에 띔
- 값의 범위가 넓은 데이터에 적합

**활용 사례**:
- 계절 패턴(주기적 데이터)
- 카테고리가 있는 순위
- 절대값도 중요한 비율 표현
- 시각적 임팩트가 중요한 경우
