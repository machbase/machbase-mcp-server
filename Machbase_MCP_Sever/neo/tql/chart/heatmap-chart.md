# Machbase Neo Heatmap Chart

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

### 히트맵 데이터 형식

히트맵은 `[x, y, value]` 형식의 데이터가 필요합니다.

---

## 1. 기본 히트맵 (2만 건)

연속 색상 매핑을 적용한 대규모 히트맵입니다.

```js
FAKE( meshgrid( linspace(1, 200, 200), linspace(1, 100, 100)) )
MAPVALUE(2, simplex(4, value(0)/40, value(1)/20) + 0.8 )
MAPVALUE(2, list(value(0), value(1), value(2)))
CHART(
    chartOption({
        tooltip: {},
        xAxis: { type: "category", value: column(0) },
        yAxis: { type: "category", value: column(1) },
        visualMap: {
            min: 0,
            max: 1.6,
            calculable: true,
            realtime: false,
            inRange: {
                color: [
                    "#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf",
                    "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"
                ]
            }
        },
        series: [
            { 
                name: "SimpleX Noise",
                type: "heatmap",
                data: column(2),
                emphasis: {
                    itemStyle: {
                        borderColor: "#333",
                        borderWidth: 1
                    }
                },
                progressive: 1000,
                animation: false
            }
        ]
    })
)
```

**설명**: 심플렉스 노이즈로 부드러운 패턴을 만든 2만 개(200×100 격자) 데이터 포인트의 대규모 히트맵입니다. 파랑(낮음)에서 빨강(높음)으로 이어지는 연속 색상 그라데이션이 특징입니다.

**핵심 포인트**:

**데이터 생성**:
- `meshgrid(linspace(...))`가 2차원 격자 좌표를 만듭니다
- `simplex(4, x/40, y/20)`이 부드러운 노이즈 패턴을 생성합니다
- 결과: 200×100 = 20,000개 데이터 포인트
- 최종 형식: `[x, y, value]` 3원소 배열

**색상 매핑**:
- `visualMap`이 값을 색상 그라데이션에 매핑합니다
- `min: 0, max: 1.6`이 값 범위를 정의합니다
- 11색 그라데이션: 파랑 → 청록 → 노랑 → 빨강
- `calculable: true`로 범위를 대화형으로 조정할 수 있습니다
- `realtime: false`가 대용량 데이터의 성능을 최적화합니다

**성능**:
- `progressive: 1000`이 한 번에 1000개씩 나눠 렌더링합니다
- `animation: false`로 애니메이션을 꺼 렌더링을 빠르게 합니다
- 점진적 렌더링이 대용량 데이터에서 UI 멈춤을 막습니다

**강조**:
- 마우스를 올리면 셀 주위에 검은 테두리가 생깁니다
- `borderWidth: 1`이 셀 경계를 뚜렷하게 만듭니다

---

## 2. 이산 색상 매핑 (2만 건)

연속 그라데이션 대신 이산 색상 구간을 사용하는 히트맵입니다.

```js
FAKE( meshgrid( linspace(1, 200, 200), linspace(1, 100, 100)) )
MAPVALUE(2, simplex(4, value(0)/40, value(1)/20) + 0.8 )
MAPVALUE(2, list(value(0), value(1), value(2)))
CHART(
    chartOption({
        tooltip: {},
        grid: { right: "120px", left: "40px"},
        xAxis: { type: "category", value: column(0) },
        yAxis: { type: "category", value: column(1) },
        visualMap: {
            type: "piecewise",
            min: 0,
            max: 1.8,
            left: "right",
            top: "center",
            calculable: true,
            realtime: false,
            splitNumber: 8,
            inRange: {
                color: [
                    "#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf",
                    "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"
                ]
            }
        },
        series: [
            { 
                name: "SimpleX Noise",
                type: "heatmap",
                data: column(2),
                emphasis: {
                    itemStyle: {
                        borderColor: "#333",
                        borderWidth: 1
                    }
                },
                progressive: 1000,
                animation: false
            }
        ]
    })
)
```

**설명**: 기본 히트맵과 비슷하지만 연속 그라데이션 대신 이산 색상 구간을 사용합니다. 값 범위를 8개의 뚜렷한 색상 대역으로 나눕니다.

**기본 히트맵과의 차이**:

**이산 색상 매핑**:
- `type: "piecewise"`가 이산 구간을 만듭니다
- `splitNumber: 8`이 범위를 8개의 동일 대역으로 나눕니다
- 각 대역이 그라데이션에서 서로 다른 색을 갖습니다
- 값 범위를 시각적으로 식별하기 쉽습니다

**범례 위치**:
- `left: "right"`로 범례를 오른쪽에 배치합니다
- `top: "center"`로 세로 중앙 정렬합니다
- `grid: { right: "120px" }`로 범례 공간을 확보합니다

**활용 사례**:
- 정확한 값보다 구간이 중요할 때
- 분류 작업(낮음/중간/높음)
- 값 대역 간 구분을 더 명확히 하고 싶을 때
- 범주형 해석에 적합

---

## 3. 캘린더 히트맵 (2023년)

한 해의 일별 값을 달력 형태로 표시하는 히트맵입니다.

```js
FAKE(linspace(1, 365, 365))
MAPVALUE(1, simplex(10, value(0))+0.9)
MAPVALUE(0, 1672444800+(value(0)*3600*24)) // 2023/01/01 00:00:00
MAPVALUE(0, time(value(0)*1000000000))
MAPVALUE(0, list(value(0), value(1)))
CHART(
    chartOption({
        title: {
            top: 30,
            left: "center",
            text: "Daily Measurements"
        },
        tooltip: {},
        visualMap: {
            min: 0,
            max: 2.0,
            type: "piecewise",
            orient: "horizontal",
            left: "center",
            top: 65
        },
        calendar: {
            top: 120,
            left: 30,
            right: 30,
            cellSize: ["auto", 13],
            range: "2023",
            itemStyle: {
                borderWidth: 0.5
            },
            yearLabel: {show:true}
        },
        series: {
            type: "heatmap",
            coordinateSystem: "calendar",
            data: column(0)
        }
    })
)
```

**설명**: 2023년 한 해의 일별 값을 보여주는 달력 기반 히트맵입니다. 각 날짜가 전통적인 달력 배치(주를 행, 요일을 열로)의 색상 셀로 표시됩니다.

**핵심 포인트**:

**데이터 준비**:
- `linspace(1, 365, 365)`가 일자 번호를 생성합니다
- `1672444800` = 2023-01-01 00:00:00의 Unix 타임스탬프
- `+(value(0)*3600*24)`가 일수를 초 단위로 더합니다
- `time(value(0)*1000000000)`이 time 객체로 변환합니다
- 최종 형식: `[time, value]` 쌍

**달력 설정**:
- `coordinateSystem: "calendar"`가 달력 배치를 사용합니다
- `range: "2023"`이 2023년 전체를 표시합니다
- `cellSize: ["auto", 13]`은 너비 자동, 높이 13px
- `itemStyle.borderWidth: 0.5`가 셀 테두리를 추가합니다
- `yearLabel: {show:true}`가 연도 라벨을 표시합니다

**시각적 매핑**:
- `type: "piecewise"`로 이산 색상 대역을 사용합니다
- `orient: "horizontal"`로 달력 위에 가로 범례를 둡니다
- 제목 아래, 달력 격자 위에 배치됩니다

**레이아웃**:
- 제목은 상단 중앙
- 범례는 제목 아래 가로 중앙 정렬
- 달력 격자는 `top: 120`에서 시작하고 좌우 여백을 둡니다

**활용 사례**:
- 활동 추적(GitHub 기여도 스타일)
- 일별 지표 시각화
- 계절 패턴 식별
- 연도 간 비교
- 출석·빈도 데이터
