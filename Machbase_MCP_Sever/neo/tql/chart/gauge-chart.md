# Machbase Neo Gauge Chart

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

## 1. 기본 게이지

단일 값을 표시하는 단순한 게이지 차트입니다.

### SCRIPT 사용

```js
SCRIPT({
    value = 55;
    $.yield({
      tooltip: { formatter: "{a} <br/>{b} : {c}%" },
      series: [
        {
          name: "Pressure",
          type: "gauge",
          detail: { formatter: "{value}" },
          data: [
              { value: value, name: "PRESSURE" }
          ]
        }
      ]
    })
})
CHART()
```

### FAKE 사용

```js
FAKE(linspace(55, 60, 1))
CHART(
    chartOption({
        tooltip: { formatter: "{a} <br/>{b} : {c}%" },
        series: [
          {
            name: "Pressure",
            type: "gauge",
            detail: { formatter: "{value}" },
            data: [
                { value: column(0)[0], name: "PRESSURE" }
            ]
          }
        ]
    })
)
```

**설명**: 압력 값을 보여주는 기본 게이지 차트입니다. 바늘이 있는 전통적인 다이얼 형태로 표시합니다. `SCRIPT`로 값을 직접 정의하는 방법과 `FAKE`로 데이터 파이프라인을 쓰는 두 가지 방식을 보여줍니다.

**핵심 포인트**:
- 게이지는 하나의 숫자 값을 표시합니다
- `detail.formatter`가 값 표시 형식을 제어합니다
- `tooltip.formatter`가 마우스오버 정보를 지정합니다
- 게이지 기본 범위는 0~100입니다

---

## 2. 속도계 게이지

진행 막대 스타일을 적용한 현대적인 게이지 차트입니다.

```js
FAKE(json(`[70]`))
CHART(
    chartOption({
        series: [{
            type: "gauge",
            progress: {
                show: true,
                width: 18
            },
            axisLine: {
                lineStyle: {
                    width: 18
                }
            },
            axisTick: {
                show: false
            },
            splitLine: {
                length: 15,
                lineStyle: {
                    width: 2,
                    color: "#999"
                }
            },
            axisLabel: {
                distance: 25,
                color: "#999",
                fontSize: 20
            },
            anchor: {
                show: true,
                showAbove: true,
                size: 25,
                itemStyle: {
                    borderWidth: 10
                }
            },
            title: {
                show: false
            },
            detail: {
                valueAnimation: true,
                fontSize: 80,
                offsetCenter: [0, "70%"]
            },
            data: [
                {
                    value: column(0)
                }
            ]
        }]
    })
)
```

**설명**: 원형 진행 막대가 있는 현대적인 속도계 스타일 게이지입니다. 큰 숫자 표시와 부드러운 값 애니메이션, 세련된 스타일링이 특징입니다.

**핵심 포인트**:
- `progress.show: true`로 원형 진행 막대 시각화를 활성화합니다
- `axisTick.show: false`로 눈금을 숨겨 더 깔끔하게 만듭니다
- `anchor`가 중앙에 눈에 띄는 핀/앵커 지점을 만듭니다
- `detail.valueAnimation`이 숫자 전환을 부드럽게 합니다
- `detail.fontSize: 80`으로 크고 눈에 띄는 값 표시를 만듭니다
- `detail.offsetCenter`가 값 텍스트의 위치를 지정합니다

---

## 3. 실시간 갱신 게이지

자동으로 실시간 갱신되는 게이지 차트입니다.

```js
FAKE(linspace(0, 1, 1))
CHART(
    chartOption({
        tooltip: {
            formatter: "{a} <br/>{b} : {c}%"
        },
        series: [
            {
                name: "Pressure",
                type: "gauge",
                progress: {
                    show: true
                },
                detail: {
                    valueAnimation: true,
                    formatter: "{value}"
                },
                data: [
                    {
                        value: 0,
                        name: "RANDOM"
                    }
                ]
            }
        ]
    }),
    chartJSCode({
        function updateGauge() {
            fetch("/db/tql", {
                method: "POST",
                body: `
                    FAKE(linspace(0, 1, 1))
                    MAPVALUE(0, floor(random() * 100))
                    JSON()
                `
            }).then(function(rsp){
                return rsp.json()
            }).then(function(obj){
                _chartOption.series[0].data[0].value = obj.data.rows[0][0]
                _chart.setOption(_chartOption)
                if (document.getElementById(_chartID) != null) {
                    setTimeout(updateGauge, 1000)
                }
            }).catch(function(err){
                console.warn("data fetch error", err)
            });
        };
        setTimeout(updateGauge, 10)
    })
)
```

**설명**: 데이터베이스에서 가져온 난수 값으로 1초마다 갱신되는 애니메이션 게이지입니다. TQL API 호출을 통한 자동 새로고침으로 실시간 데이터 시각화를 구현합니다.

**핵심 포인트**:
- `chartJSCode()`로 사용자 정의 갱신 로직을 구현합니다
- `fetch("/db/tql")`로 클라이언트 측에서 TQL 쿼리를 실행합니다
- `setTimeout()`으로 주기적 갱신(1초 간격)을 만듭니다
- `valueAnimation: true`로 값 전환을 부드럽게 합니다
- `document.getElementById(_chartID)`를 확인해 차트가 제거되면 갱신을 멈춥니다
- `_chart.setOption()`이 새 데이터로 차트를 갱신합니다
- `random() * 100`이 0~100 사이 값을 생성합니다

**갱신 동작 순서**:
1. 초기 차트가 값 0으로 렌더링됨
2. 10ms 후 첫 갱신 실행
3. TQL 쿼리가 난수 값을 생성
4. 새 값으로 차트 갱신
5. 1000ms마다 반복
6. 차트 요소가 DOM에서 제거되면 자동 중단
