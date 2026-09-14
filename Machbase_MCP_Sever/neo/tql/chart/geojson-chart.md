# Machbase Neo GeoJSON Chart

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
| `SCRIPT()` | JavaScript 처리 | `SCRIPT({}, { /* process */ }, {})` |

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

## GeoJSON 지도 차트 - 서울 자치구

서울 자치구 GeoJSON 데이터를 사용한 단계구분도(choropleth) 시각화입니다.

```js
FAKE(json({
    ["노원구", 10], ["도봉구", 50], ["강북구", 90],
    ["성북구", 20], ["종로구", 10], ["서대문구", 40],
    ["은평구", 90], ["마포구", 60], ["강서구", 20],
    ["양천구", 55], ["구로구", 75], ["영등포구", 35],
    ["중구", 100], ["용산구", 20], ["성동구", 65],
    ["광진구", 25], ["동대문구", 10], ["중랑구", 70],
    ["강동구", 10], ["송파구", 30], ["강남구", 50],
    ["서초구", 50], ["동작구", 90], ["관악구", 70], ["금천구", 90]
}))
SCRIPT({
    data = [];
},{
    data.push({name:$.values[0], value:$.values[1]})
}, {
    $.yield(data)
})
CHART(
    chartOption({
        title:{ text: "GEOJSON - Seoul"},
        tooltip: { trigger: "item", formatter: "{b}<br/>{c} %"},
        visualMap: {
            min: 0,
            max: 100,
            text: ["100%", "0%"],
            realtime: false,
            calculable: true,
            inRange: {
                color: [ "#89b6fe", "#25529a"]
            },
        },
        series: []
    }),
    chartJSCode({
        fetch("https://docs.machbase.com/assets/example/seoul_gu.json"
        ).then( function(rsp) {
            return rsp.json();
        }).then( function(seoulJSON) {
            echarts.registerMap("seoul_gu", seoulJSON);
            _chartOption.geo = {
                map: "seoul_gu",
                zoom: 1.2,
                roam: true,
                itemStyle: {
                    areaColor: "#e7e8ea"
                }
            };
            _chartOption.series[0] ={
                type: "map",
                geoIndex: 0,
                data: column(0)[0]
            };
            _chart.setOption(_chartOption);
        }).catch(function(err){
            console.warn("geojson error", err)
        });
    })
)
```

**설명**: 서울 25개 자치구를 백분율 값에 따라 색으로 구분한 단계구분도입니다. GeoJSON 경계 데이터를 불러와 데이터 값을 색상 그라데이션에 매핑합니다.

**핵심 포인트**:

**데이터 준비**:
- `FAKE(json({...}))`로 자치구 이름과 값의 쌍을 만듭니다
- `SCRIPT()`가 데이터를 `{name, value}` 객체로 변환합니다
- 3단계 SCRIPT: 초기화, 레코드별 처리, 마무리

**GeoJSON 연동**:
- `fetch()`로 서울 자치구 경계가 담긴 GeoJSON 파일을 불러옵니다
- `echarts.registerMap()`으로 지리 데이터를 등록합니다
- "seoul_gu"라는 지도 이름이 chartOption과 등록된 GeoJSON을 연결합니다

**시각적 매핑**:
- `visualMap`이 색상 범례(0~100%)를 만듭니다
- `inRange.color`가 연한 파랑(#89b6fe)에서 진한 파랑(#25529a)까지의 그라데이션을 정의합니다
- `calculable: true`로 범위를 대화형으로 조정할 수 있습니다

**지도 설정**:
- `geo.map`이 등록된 GeoJSON 지도를 참조합니다
- `zoom: 1.2`로 초기 확대 수준을 설정합니다
- `roam: true`로 이동·확대 조작을 활성화합니다
- `itemStyle.areaColor`가 기본 영역 색상을 지정합니다

**데이터 바인딩**:
- `series[0].type: "map"`으로 지도 시리즈를 만듭니다
- `geoIndex: 0`으로 시리즈를 geo 컴포넌트에 연결합니다
- `data: column(0)[0]`으로 자치구 값을 지도 영역에 바인딩합니다
- 데이터의 지역 이름은 GeoJSON의 feature 이름과 일치해야 합니다

**사용 패턴**:
1. 지리적 지역 이름이 포함된 데이터를 준비합니다
2. GeoJSON 파일을 불러와 등록합니다
3. 값을 색상으로 변환하는 시각적 매핑을 설정합니다
4. 이름 일치를 통해 데이터를 지도 영역에 연결합니다
