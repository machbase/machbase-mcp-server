# Machbase Neo 3D Line Chart

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

### 3D 라인 데이터 형식

3D 라인 차트는 `[x, y, z]` 형식의 데이터가 필요합니다.

예:
```js
[1.5, 2.3, 4.7]  // x=1.5, y=2.3, z=4.7
```

---

## 정사영(Orthographic) 3D 라인

정사영 투영과 색상 그라데이션을 적용한 3D 매개변수 곡선입니다.

```js
FAKE(linspace(0, 24.999, 25000))
MAPVALUE(1, (1 + 0.25 * cos(75 * value(0))) * cos(value(0)))
MAPVALUE(2, (1 + 0.25 * cos(75 * value(0))) * sin(value(0)))
MAPVALUE(3, value(0) + 2.0 * sin(75 * value(0)))
MAPVALUE(0, list(value(1), value(2), value(3)))
POPVALUE(1,2,3)
CHART(
    plugins("gl"),
    chartOption({
        tooltip: {},
        backgroundColor: "#fff",
        visualMap: {
            show: false,
            dimension: 2,
            min: 0,
            max: 30,
            inRange: {
                color: [
                    "#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf",
                    "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"
                ]
            }
        },
        xAxis3D: { type: "value" },
        yAxis3D: { type: "value" },
        zAxis3D: { type: "value" },
        grid3D: {
            viewControl: {
                projection: "orthographic"
            }
        },
        series: [
            {
                type: "line3D",
                data: column(0),
                lineStyle: { width: 4}
            }
        ]
    })
)
```

**설명**: 25,000개 점으로 그린 3D 매개변수 나선을 정사영으로 렌더링합니다. 선 색상이 z축을 따라 파랑(낮음)에서 빨강(높음)으로 변하며 무지개 효과를 만듭니다.

**핵심 포인트**:

**매개변수 방정식**:
반지름이 변조된 3D 나선을 생성합니다:
- `t`는 0부터 약 25까지 (25,000개 점)
- `x = (1 + 0.25*cos(75t)) * cos(t)` - x 방향 반지름 변조
- `y = (1 + 0.25*cos(75t)) * sin(t)` - y 방향 반지름 변조
- `z = t + 2.0*sin(75t)` - 진동이 더해진 수직 위치

**수학적 특성**:
- 기본 반지름: 1 단위
- 반지름 변조: ±0.25 (75회 진동)
- 수직 진행: 사인파가 더해진 선형 진행
- 전체 수직 범위: 약 25 단위
- 잔물결이 있는 촘촘한 나선 코일을 형성

**데이터 파이프라인**:
- `linspace(0, 24.999, 25000)`으로 매개변수 t를 생성
- x, y, z 좌표를 각각 계산
- `list(x, y, z)`로 3D 점으로 결합
- `POPVALUE(1,2,3)`으로 중간 컬럼 제거
- 결과: `[x, y, z]` 배열로 이루어진 단일 컬럼

**투영**:
- `projection: "orthographic"`은 평행 투영을 사용합니다
- 원근 투영과 달리 평행선이 평행하게 유지됩니다
- 거리에 따른 크기 변화가 없습니다
- 과학적 시각화에 더 적합합니다
- 모든 깊이에서 상대적 크기가 보존됩니다

**색상 매핑**:
- `visualMap.dimension: 2`로 색상을 z좌표에 매핑
- `show: false`로 범례를 숨김
- 11색 그라데이션: 파랑 → 청록 → 노랑 → 빨강
- 색상이 나선의 높이를 나타냄
- 최소/최대(0~30)가 전체 z 범위를 포함

**성능**:
- 25,000개 점을 효율적으로 렌더링
- `lineStyle.width: 4`로 선이 잘 보이게 설정
- ECharts GL이 대용량 데이터셋을 부드럽게 처리

**활용 사례**:
- 매개변수 곡선 시각화
- 수학 함수(나선, 매듭, 어트랙터)
- 궤적 데이터(입자 경로, 궤도)
- 3차원 시계열
- 원근 왜곡을 피해야 하는 과학 데이터 시각화

**정사영 vs 원근투영**:
- **정사영(Orthographic)**: 평행 투영, 깊이 왜곡 없음, 기술/CAD 스타일
- **원근투영(Perspective)**: 사실적인 깊이감, 멀수록 작아짐, 자연스러운 시야
