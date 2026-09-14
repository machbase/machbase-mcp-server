# Machbase Neo 3D Globe Chart

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
| `DROP()` | 앞의 N개 레코드 버리기 | `DROP(1)` |

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

#### latlon(longitude, latitude)
지구본 시각화용 지리 좌표를 생성합니다

- `latlon(lon, lat)`은 지구본 차트용 좌표 객체를 반환합니다
- 지리 데이터를 3D 지구본 표면에 매핑할 때 사용합니다

---

## 1. Hello World Globe

사실적인 텍스처와 조명을 적용한 기본 3D 지구본입니다.

```js
FAKE( json({
    ["world.topo.bathy.200401.jpg", "starfield.jpg", "pisa.hdr"]
}) )

MAPVALUE(0, "https://docs.machbase.com/assets/example/"+value(0))
MAPVALUE(1, "https://docs.machbase.com/assets/example/"+value(1))
MAPVALUE(2, "https://docs.machbase.com/assets/example/"+value(2))

CHART(
    plugins("gl"),
    chartOption({
        backgroundColor: "#000",
        globe: {
            baseTexture: column(0)[0],
            heightTexture: column(0)[0],
            displacementScale: 0.04,
            shading: "realistic",
            environment: column(1)[0],
            realisticMaterial: {
                roughness: 0.9
            },
            postEffect: {
                enable: true
            },
            light: {
                main: {
                    intensity: 5,
                    shadow: true
                },
                ambientCubemap: {
                    texture: column(2)[0],
                    diffuseIntensity: 0.2
                }
            }
        }
    })
)
```

**설명**: 지구 해저지형 텍스처, 별자리 배경, HDR 조명을 적용한 사실적인 3D 지구본입니다. 변위 매핑으로 지형 고도를 표현하고 그림자가 있는 사실적 재질 렌더링을 사용합니다.

**핵심 포인트**:
- `plugins("gl")`이 3D 렌더링을 위한 ECharts GL을 활성화합니다
- `baseTexture`가 지구 표면 이미지를 제공합니다
- `heightTexture`가 변위 매핑으로 3D 지형을 만듭니다
- `displacementScale: 0.04`가 지형 높이 과장 정도를 조절합니다
- `shading: "realistic"`은 물리 기반 렌더링을 사용합니다
- `environment`가 별자리 배경을 추가합니다
- `ambientCubemap`이 HDR 환경광을 제공합니다
- `postEffect`가 화면 공간 효과를 활성화합니다
- `light.main`이 그림자가 있는 방향광을 설정합니다

**사용된 텍스처**:
- Base/Height: `world.topo.bathy.200401.jpg` (지구 해저지형)
- Environment: `starfield.jpg` (우주 배경)
- Lighting: `pisa.hdr` (HDR 환경광)

---

## 2. 지구본 위 항공 노선

도시 간 항공 노선을 표시하는 3D 지구본입니다.

```js
CSV(file("https://docs.machbase.com/assets/example/flights.csv"))
DROP(1) // skip header
// |   0         1     2    3      4     5    6
// +-> flights   name1 lon1 lat1   name2 lon2 lat2
// |
MAPVALUE(0, latlon( parseFloat(value(2)), parseFloat(value(3))))
MAPVALUE(1, latlon( parseFloat(value(5)), parseFloat(value(6))))
// |   0     1      2    3      4     5    6
// +-> loc1  loc2   lon1 lat1   name2 lon2 lat2
// |
MAPVALUE(0, list(value(0), value(1)))
// |   0            1         2    3      4     5    6
// +-> [loc1,loc2]  (lat,lon) lon1 lat1   name2 lon2 lat2
// |
POPVALUE(1, 2, 3, 4, 5, 6)
// |   0
// +-> [loc1,loc2]
// |
CHART(
    plugins("gl"),
    chartOption({
        backgroundColor: "#000",
        globe: {
            baseTexture: "https://docs.machbase.com/assets/example/world.topo.bathy.200401.jpg",
            heightTexture: "https://docs.machbase.com/assets/example/bathymetry_bw_composite_4k.jpg",
            shading: "lambert",
            light: {
                ambient: {
                    intensity: 0.4
                },
                main: {
                    intensity: 0.4
                }
            },
            viewControl: {
                autoRotate: false
            }
        },
        series: {
            type: "lines3D",
            coordinateSystem: "globe",
            blendMode: "lighter",
            lineStyle: {
                width: 0.5,
                color: "rgb(50, 50, 150)",
                opacity: 0.1
            },
            data: column(0)
        }
    })
)
```

**설명**: 3D 지구본 위에 항공 노선을 시각화합니다. 출발지/도착지 좌표가 담긴 CSV를 불러와 지구본 표면에서 도시를 잇는 곡선을 그립니다.

**핵심 포인트**:

**데이터 파이프라인**:
- `CSV(file(...))`으로 좌표가 포함된 항공 노선 데이터를 불러옵니다
- `DROP(1)`으로 CSV 헤더 행을 건너뜁니다
- `latlon(lon, lat)`이 숫자 좌표를 지구본 좌표 객체로 변환합니다
- `list(loc1, loc2)`가 선분의 양 끝점을 만듭니다
- 최종 데이터 형식: `[[lon1, lat1], [lon2, lat2]]` 쌍의 배열

**지구본 설정**:
- `shading: "lambert"`는 단순 확산 조명을 사용합니다(realistic보다 빠름)
- `viewControl.autoRotate: false`로 자동 회전을 끕니다
- 환경광과 주광의 세기를 균형 있게(각 0.4) 설정합니다

**선 렌더링**:
- `type: "lines3D"`가 지구본 표면에 곡선을 그립니다
- `coordinateSystem: "globe"`가 선을 3D 구면에 매핑합니다
- `blendMode: "lighter"`가 겹치는 선에 가산 혼합을 적용합니다
- 반투명 파란 선(`opacity: 0.1`)이 노선 밀도를 드러냅니다
- 얇은 선(`width: 0.5`)이 시각적 혼잡을 줄입니다

**활용 사례**: 다음을 시각화하기에 적합합니다:
- 항공 노선과 항공사 네트워크
- 이동·이주 패턴
- 무역 경로
- 통신 네트워크
- 지점 간 지리적 연결 전반
