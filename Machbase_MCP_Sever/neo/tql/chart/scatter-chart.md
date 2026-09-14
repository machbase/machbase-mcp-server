# Machbase Neo Scatter Chart

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

### 산점도 데이터 형식

산점도는 보통 다음 형식을 사용합니다:
- 단일 값: `[y1, y2, y3, ...]` (x는 xAxis.data에서)
- 좌표 쌍: `[[x1, y1], [x2, y2], ...]`

---

## 1. 기본 산점도

사인파 패턴을 보여주는 단순한 산점도입니다.

```js
FAKE( linspace(0, 360, 100) )
MAPVALUE( 2, sin((value(0)/180)*PI) )
CHART(
    chartOption({
        xAxis:{ data: column(0) },
        yAxis:{},
        series:[
            { type:"scatter", data: column(1) }
        ]
    })
)
```

**설명**: 사인파를 따르는 100개 점을 찍는 기본 산점도입니다. 카테고리 x축과 단일 y값을 사용합니다.

**핵심 포인트**:
- `linspace(0, 360, 100)`이 균등 간격의 x값 100개를 생성합니다
- `sin((value(0)/180)*PI)`가 각 x의 사인값을 계산합니다
- x값은 `xAxis.data`로 전달합니다
- y값은 단일 배열 `column(1)`로 전달합니다
- 산점 심볼 크기와 색상은 기본값 사용

---

## 2. 앤스컴 콰르텟

통계값은 같지만 패턴이 전혀 다른 네 개의 산점도입니다.

```js
FAKE( json({
    [1701059601000000000,  4.26, 3.1 ,  5.39, 12.5],
    [1701059602000000000,  5.68, 4.74,  5.73, 6.89],
    [1701059603000000000,  7.24, 6.13,  6.08, 5.25],
    [1701059604000000000,  4.82, 7.26,  6.42, 7.91],
    [1701059605000000000,  6.95, 8.14,  6.77, 5.76],
    [1701059606000000000,  8.81, 8.77,  7.11, 8.84],
    [1701059607000000000,  8.04, 9.14,  7.46, 6.58],
    [1701059608000000000,  8.33, 9.26,  7.81, 8.47],
    [1701059609000000000, 10.84, 9.13,  8.15, 5.56],
    [1701059610000000000,  7.58, 8.74, 12.74, 7.71],
    [1701059611000000000,  9.96, 8.1 ,  8.84, 7.04]
}) )

MAPVALUE(0, time(value(0)))
MAPVALUE(1, list(value(0), value(1)))
MAPVALUE(2, list(value(0), value(2)))
MAPVALUE(3, list(value(0), value(3)))
MAPVALUE(4, list(value(0), value(4)))
CHART(
    chartOption({
        title: {
            text: "Anscombe's quartet",
            left: "center",
            top: 0
        },
        grid: [
            { left:  "7%", top: "7%", width: "38%", height: "38%" },
            { right: "7%", top: "7%", width: "38%", height: "38%" },
            { left:  "7%", bottom: "7%", width: "38%", height: "38%" },
            { right: "7%", bottom: "7%", width: "38%", height: "38%" }
        ],
        xAxis: [
            { gridIndex: 0, type:"time", min: 1701059598000, max: 1701059614000 },
            { gridIndex: 1, type:"time", min: 1701059598000, max: 1701059614000 },
            { gridIndex: 2, type:"time", min: 1701059598000, max: 1701059614000 },
            { gridIndex: 3, type:"time", min: 1701059598000, max: 1701059614000 }
        ],
        yAxis: [
            { gridIndex: 0, min: 0, max: 15 },
            { gridIndex: 1, min: 0, max: 15 },
            { gridIndex: 2, min: 0, max: 15 },
            { gridIndex: 3, min: 0, max: 15 }
        ],
        series: [
            {   name: "I",
                type: "scatter",
                data: column(1),
                xAxisIndex: 0,
                yAxisIndex: 0,
                markLine: {
                    animation:false,
                    data: [
                        [ {coord: [1701059598000, 3], symbol: "none"}, {coord: [1701059614000, 13], symbol: "none"} ]
                    ]
                }
            },
            {   name: "II",
                type: "scatter",
                data: column(2),
                xAxisIndex: 1,
                yAxisIndex: 1,
                markLine: {
                    animation:false,
                    data: [
                        [ {coord: [1701059598000, 3], symbol: "none"}, {coord: [1701059614000, 13], symbol: "none"} ]
                    ]
                }
            },
            {   name: "III",
                type: "scatter",
                data: column(3),
                xAxisIndex: 2,
                yAxisIndex: 2,
                markLine: {
                    animation:false,
                    data: [
                        [ {coord: [1701059598000, 3], symbol: "none"}, {coord: [1701059614000, 13], symbol: "none"} ]
                    ]
                }
            },
            {   name: "IV",
                type: "scatter",
                data: column(4),
                xAxisIndex: 3,
                yAxisIndex: 3,
                markLine: {
                    animation: false,
                    data: [
                        [ {coord: [1701059598000, 3], symbol: "none"}, {coord: [1701059614000, 13], symbol: "none"} ]
                    ]
                }
            }
        ]
    })
)
```

**설명**: 평균·분산·상관계수가 동일하지만 분포는 완전히 다른 네 데이터셋을 보여주는 고전적인 앤스컴 콰르텟 시각화입니다. 통계값만으로는 알 수 없는 것을 시각화가 드러낸다는 점을 보여줍니다.

**핵심 포인트**:

**데이터 준비**:
- Raw data: `[timestamp, y1, y2, y3, y4]`
- 타임스탬프를 time 객체로 변환
- 시리즈마다 `[time, y_value]` 좌표 쌍 생성
- 산점도 4개를 위한 4개 컬럼

**멀티 그리드 배치**:
- `grid: [...]`가 4개의 차트 영역을 만듭니다
- 2×2 배치: 좌상, 우상, 좌하, 우하
- 각 그리드: 너비 38% × 높이 38%
- left/right/top/bottom 속성으로 위치 지정

**축 설정**:
- 그리드마다 x축 하나씩 총 4개 (`gridIndex: 0-3`)
- 그리드마다 y축 하나씩 총 4개 (`gridIndex: 0-3`)
- 모두 같은 시간 범위와 y 범위를 사용
- `xAxisIndex`와 `yAxisIndex`가 시리즈를 해당 축에 연결

**MarkLine (회귀선)**:
- 모든 시리즈가 동일한 회귀선을 가집니다
- 좌표: `(1701059598000, 3)` → `(1701059614000, 13)`
- `symbol: "none"`이 끝점 표식을 제거합니다
- `animation: false`로 선을 정적으로 유지
- 네 개 모두 기울기와 절편이 같습니다

**통계적 시사점**:
- 네 데이터셋 모두 다음이 같습니다:
  - x와 y의 평균
  - 분산
  - 상관계수
  - 회귀선
- 그러나 패턴은 완전히 다릅니다:
  - I: 선형 관계
  - II: 비선형(곡선) 관계
  - III: 이상치가 있는 선형
  - IV: 이상치가 있는 수직선

**교훈**: 통계값만으로는 오도될 수 있습니다 — 시각화가 실제 패턴을 드러냅니다.

---

## 3. 100만 개 포인트

100만 개 데이터 포인트와 줌 기능을 갖춘 대규모 산점도입니다.

```js
FAKE( linspace(0, 10, 500000) )

MAPVALUE(1, random()*10)
MAPVALUE(2, sin(value(0)) - value(0)*(0.1*random()) + 1)
MAPVALUE(3, cos(value(0)) - value(0)*(0.1*random()) - 1)
POPVALUE(1)

CHART(
    chartOption({
        legend: { show: false },
        xAxis: { data: column(0) },
        yAxis: {},
        dataZoom: [
            { type: "inside" },
            { type: "slider" }
        ],
        animation: false,
        series: [
            {
                name: "A",
                type: "scatter",
                data: column(1),
                symbolSize: 3,
                itemStyle: {
                    color: "#9ECB7F",
                    opacity: 0.5
                },
                large: true
            },
            {
                name: "B",
                type: "scatter",
                data: column(2),
                symbolSize: 3,
                itemStyle: {
                    color: "#5872C0",
                    opacity: 0.5
                },
                large: true
            }
        ]
    })
)
```

**설명**: 100만 개 포인트(시리즈당 50만 개)를 그리는 고성능 산점도입니다. 줌 기능과 함께 효율적인 렌더링을 보여줍니다.

**핵심 포인트**:

**데이터 생성**:
- `linspace(0, 10, 500000)`이 50만 개 x값을 만듭니다
- 시리즈 A(초록): 하향 드리프트와 노이즈가 더해진 `sin(x)`
- 시리즈 B(파랑): 하향 드리프트와 노이즈가 더해진 `cos(x)`
- 합계: 1,000,000개 데이터 포인트

**성능 최적화**:
- `large: true`가 대용량 데이터셋 모드를 활성화합니다
  - WebGL 렌더링 사용
  - 단순화된 드로잉 알고리즘
  - 개별 포인트 마우스오버·선택 불가
- `animation: false`로 애니메이션을 끕니다
- 작은 `symbolSize: 3`이 시각적 혼잡을 줄입니다
- 반투명(`opacity: 0.5`)이 밀도를 드러냅니다

**데이터 줌**:
- `type: "inside"`는 마우스 휠·트랙패드 줌
- `type: "slider"`는 슬라이더 컨트롤
- 밀집 구간을 탐색할 수 있게 합니다
- 대용량 데이터에는 필수입니다

**시각 디자인**:
- 위쪽 패턴은 초록(#9ECB7F)
- 아래쪽 패턴은 파랑(#5872C0)
- 반투명이 겹치는 영역을 드러냅니다
- 작은 심볼이 과밀 표시를 막습니다

**활용 분야**:
```js
large: true              // WebGL acceleration
animation: false         // Disable transitions
symbolSize: 2-5         // Small symbols
opacity: 0.3-0.6        // See through overlaps
progressive: 1000       // Progressive rendering
```

**활용 사례**:
- 센서 데이터 시각화
- 과학 데이터셋
- 시계열 분석
- 대용량 데이터의 패턴 탐지
- IoT 장비 데이터

**기술적 한계**:
- `large: true` 사용 시: 수백만 개 포인트
- 미사용 시: 약 1만 개 포인트까지 무난
- 브라우저 메모리에 좌우됨
- 복잡도가 올라가면 성능이 떨어짐
