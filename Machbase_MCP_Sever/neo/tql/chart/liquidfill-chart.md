# Machbase Neo Liquidfill Chart

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

**plugins()**
- `plugins(plugin...)`
- `plugin` *string* 미리 정의된 플러그인 이름 또는 플러그인 모듈의 URL
- liquidfill 차트에는 `plugins("liquidfill")`을 사용합니다.

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

### Liquidfill 데이터 형식

Liquidfill 차트는 백분율 값(0.0 ~ 1.0)을 받습니다:
- 단일 값: `[0.6]` = 60% 채움
- 다중 파형: `[0.6, 0.5, 0.4, 0.3]` = 4개의 겹치는 파형

---

## 1. 기본 Liquidfill

애니메이션 파형 하나를 보여주는 단순한 액체 게이지입니다.

```js
FAKE(json({
    [0.6]
}))
CHART(
    plugins("liquidfill"),
    chartOption({
        series: [
            { type: "liquidFill", data: column(0) }
        ]
    })
)
```

**설명**: 단일 애니메이션 파형으로 60% 채움 수준을 표시하는 기본 액체 게이지입니다. 파형이 부드럽게 진동해 사실적인 물 효과를 만듭니다.

**핵심 포인트**:
- `plugins("liquidfill")`로 liquidfill 플러그인을 로드
- `type: "liquidFill"`로 액체 채움 차트 생성
- 단일 값 `[0.6]` = 60% 채움 수준
- 파형 움직임이 있는 기본 애니메이션
- 원형 컨테이너 모양
- 기본값은 파란색 그라데이션

**기본 동작**:
- 파형 진폭: 보통 수준의 진동
- 파형 애니메이션: 지속적인 수평 이동
- 파형 주기 자동 계산
- 중앙에 백분율 라벨 표시

---

## 2. 다중 파형

여러 개의 겹치는 애니메이션 파형을 가진 액체 게이지입니다.

```js
FAKE(json({
    [0.6, 0.5, 0.4, 0.3]
}))
TRANSPOSE()
CHART(
    plugins("liquidfill"),
    chartOption({
        series: [
            { type: "liquidFill", data: column(0) }
        ]
    })
)
```

**설명**: 서로 다른 높이의 파형 4개가 겹쳐 투명도가 다른 층상 물 효과를 만듭니다.

**핵심 포인트**:
- `TRANSPOSE()`가 행을 열 형식으로 변환
- 값이 여러 개면 파형도 여러 개: `[0.6, 0.5, 0.4, 0.3]`
- 각 파형은 다음이 다릅니다:
  - 채움 수준 (60%, 50%, 40%, 30%)
  - 애니메이션 위상 (시작 시점 차이)
  - 불투명도 (자동 그라데이션)
- 파형들이 독립적으로 움직입니다
- 사실적인 다층 물 효과를 만듭니다

**시각 효과**:
- 상단 파형(0.6): 가장 불투명
- 하위 파형: 점점 더 투명
- 겹침으로 깊이감 형성
- 위상이 달라 동기화되지 않음
- 단일 파형보다 역동적인 모습

---

## 3. 정지 파형 (애니메이션 없음)

정적인 파형(애니메이션 없음)의 액체 게이지입니다.

```js
FAKE(json({
    [0.6, 0.5, 0.4, 0.3]
}))
TRANSPOSE()
CHART(
    plugins("liquidfill"),
    chartOption({
        series: [
            {
                type: "liquidFill",
                data: column(0),
                amplitude: 0,
                waveAnimation: 0
            }
        ]
    })
)
```

**설명**: 여러 개의 정적 파형을 가진 액체 게이지입니다. 파형 움직임이나 진동이 전혀 없는 순수 정적 시각화입니다.

**핵심 포인트**:
- `amplitude: 0`으로 수직 진동 제거
- `waveAnimation: 0`으로 수평 파형 이동 비활성화
- 파형이 완전히 정지 상태 유지
- 여러 채움 수준은 그대로 표시됨
- 정적 리포트나 스크린샷에 유용

**활용 사례**:
- **애니메이션(기본값)**: 동적 대시보드, 실시간 모니터링
- **정지(amplitude/animation = 0)**:
  - 정적 리포트
  - 인쇄물
  - 성능 최적화
  - 시선 분산 감소

**설정 옵션**:
```js
{
    amplitude: 0,          // Wave height (0 = flat)
    waveAnimation: 0,      // Animation speed (0 = still)
    direction: 'right',    // Wave direction: 'left'/'right'
    period: 2000,          // Animation period in ms
    phase: 0,              // Initial wave phase (0-360)
    color: ['#294D99'],    // Wave color(s)
    backgroundStyle: {...}, // Container background
    outline: {...}         // Container outline
}
```

**값 범위**:
- 데이터 값: 0.0 ~ 1.0 (0% ~ 100%)
- Amplitude: 0 ~ 약 20 (파형 높이)
- Period: 밀리초 (작을수록 빠름)
- Phase: 0 ~ 360도

**자주 쓰는 패턴**:
```js
// Percentage display
data: [0.75]  // Shows "75%"

// Multiple waves
data: [0.8, 0.7, 0.6]  // 3 overlapping waves

// Custom colors
color: ['#FF6B6B', '#4ECDC4', '#45B7D1']

// Fast animation
period: 1000, waveAnimation: 1
```
