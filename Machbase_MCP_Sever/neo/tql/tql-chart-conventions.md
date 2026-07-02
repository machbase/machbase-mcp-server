# TQL 차트 작성 컨벤션 (대시보드용)

대시보드의 TQL 차트를 **직접 작성**할 때 지킬 규칙과 골격입니다.
아래 골격의 **구조(SQL → SCRIPT → CHART 형태)는 그대로 두고**, TABLE / TAG / 기간 / 집계함수 / 시리즈만 바꿔서 쓰세요. 구조를 새로 발명하면 오류가 늘어 재시도가 많아집니다.

## 기본 골격 (단일 시계열)
```tql
CHART(
    tz('Asia/Seoul'),
    chartOption({
        title: { text: "차트 제목", subtext: "부제(한 줄 설명)", left: 10, top: 5 },
        grid: { left: 72, right: 30, top: 66, bottom: 78 },
        legend: { bottom: 30 },
        xAxis: { type: "time" },
        yAxis: { type: "value" },
        dataZoom: [{ type: "slider", bottom: 6, height: 16 }, { type: "inside" }],
        series: [{ type: "line", smooth: true, data: column(0) }]
    })
)
```
- **제목/부제는 좌상단**(`title: { left: 10, top: 5 }` — Neo 표준 위치). 심층 대시보드는 패널 헤더가 없으니 차트가 직접 표시합니다. `grid.top`(≈66)으로 제목 영역을 확보하세요(작으면 부제와 플롯이 붙습니다).
- **하단을 충분히 벌려 겹침 방지**: `grid.bottom≈78` 안에 아래에서 위로 [줌 슬라이더 `bottom:6` → 범례 `bottom:30` → x축 라벨] 순으로 쌓입니다. `grid.bottom`이 작으면 **범례가 x축 라벨과 겹치니** 줄이지 마세요. (여러 시리즈/멀티태그 골격도 이 레이아웃 그대로 사용)

## ROLLUP 유무별 데이터 골격 (위 CHART 골격에 연결)

먼저 describe_table 결과의 `ROLLUP: available / not available` 를 보고 분기하세요.

### ROLLUP 있을 때 (시간 버킷 집계)
```tql
SQL(`SELECT ROLLUP('day', 1, TIME), AVG(VALUE) FROM TABLE WHERE NAME = 'tag' AND TIME BETWEEN TO_DATE('START') AND TO_DATE('END') GROUP BY ROLLUP('day', 1, TIME) ORDER BY ROLLUP('day', 1, TIME)`)
SCRIPT({ $.yield([$.values[0], $.values[1]]) })
```

### ROLLUP 없을 때 (원시 시계열)
```tql
SQL(`SELECT TIME, VALUE FROM TABLE WHERE NAME = 'tag' AND TIME BETWEEN TO_DATE('START') AND TO_DATE('END') ORDER BY TIME`)
SCRIPT({ $.yield([$.values[0], $.values[1]]) })
```
- ROLLUP/GROUP BY 없이 원시 조회. 포인트가 많으면 위 CHART series에 `symbol: "none"`, `sampling: "lttb"` 를 추가해 렌더 시 다운샘플하세요 (ROLLUP 다운샘플의 대안).

### 여러 시리즈 (밴드/비교) — SCRIPT 3-block 누적
```tql
SQL(`SELECT ROLLUP('day', 1, TIME), MAX(VALUE), MIN(VALUE), AVG(VALUE) FROM TABLE WHERE NAME = 'tag' AND TIME BETWEEN TO_DATE('START') AND TO_DATE('END') GROUP BY ROLLUP('day', 1, TIME) ORDER BY ROLLUP('day', 1, TIME)`)
SCRIPT({
    var maxArr = []; var minArr = []; var avgArr = [];
},{
    maxArr.push([$.values[0], $.values[1]]);
    minArr.push([$.values[0], $.values[2]]);
    avgArr.push([$.values[0], $.values[3]]);
},{
    for (var i = 0; i < maxArr.length; i++) $.yield(maxArr[i], minArr[i], avgArr[i]);
})
// CHART series: [{ type:"line", data: column(0) }, { type:"line", data: column(1) }, { type:"line", data: column(2) }]
```
- **SCRIPT는 3-block**: `{초기화}, {레코드마다}, {끝나고}`. 가운데(main) 블록이 **레코드마다 자동 실행**되며 `$.values[i]` 로 컬럼 접근. 단일 시리즈는 main 한 줄 `$.yield([$.values[0], $.values[1]])`.
- ❌ `$.foreach(...)`, `for (row of ...)` 같은 행 순회 API는 **TQL SCRIPT에 없습니다** (main 블록 자체가 행마다 돕니다).
- ❌ `$.yield([arr0, arr1, arr2])` 처럼 배열 묶음을 한 번에 yield하지 마세요 — `column(0)`에 통째로 잡혀 빈 차트가 됩니다. deinit에서 **인덱스별로** `$.yield(시리즈0[i], 시리즈1[i], ...)` 하면 `column(0)`,`column(1)`...이 각 시리즈가 됩니다.

### 여러 태그 비교 (서로 다른 NAME을 각각의 시리즈로)
```tql
SQL(`SELECT TIME, NAME, VALUE FROM TABLE WHERE NAME IN ('tagA','tagB','tagC') AND TIME BETWEEN TO_DATE('START') AND TO_DATE('END') ORDER BY TIME`)
SCRIPT({
    var s = {};
},{
    if (!s[$.values[1]]) s[$.values[1]] = [];
    s[$.values[1]].push([$.values[0], $.values[2]]);   // 태그별 [time, value] 페어 누적
},{
    var a = s['tagA'] || [], b = s['tagB'] || [], c = s['tagC'] || [];
    var n = Math.max(a.length, b.length, c.length);
    for (var i = 0; i < n; i++) $.yield(a[i] || null, b[i] || null, c[i] || null);
})
// CHART series: [{ name:"tagA", data: column(0) }, { name:"tagB", data: column(1) }, { name:"tagC", data: column(2) }]
```
- 각 시리즈 = **한 태그의 [time, value] 페어 배열**. deinit에서 **인덱스별로** 각 태그의 페어를 yield → `column(0)`=tagA, `column(1)`=tagB ...
- ❌ **`$.yield(time, name, value)` 처럼 NAME(문자열)을 컬럼으로 내보내지 마세요** → `column(0)`에 시간, `column(1)`에 이름 문자열이 잡혀 **시간축이 1970~로 펼쳐지고 차트가 깨집니다** (실제 발생한 버그).
- 태그별 길이가 달라도 `|| null` 패딩 — 각 페어가 자기 시간을 들고 있어 ECharts가 올바른 위치에 그립니다.

> 캔들스틱·히트맵·FFT·3D 등 **특수 차트**는 `tql/chart/` 전용 문서를 참고하세요(여기에 타입별 골격을 넣지 않습니다). 단 위 **TIME=Time 객체·테마·제목/부제·범례/축 레이아웃 규칙은 그대로 적용**합니다.

## 필수 규칙

### 1. 테마 / 제목·부제 / 범례·줌 배치
- 대시보드는 **white(흰색) 테마**입니다. chartOption에 `theme` 이나 `backgroundColor` 를 **넣지 마세요** (패널이 white로 감쌈). `theme(...)` 를 직접 지정하면 그 차트만 색이 어긋납니다. (저장 시 서버가 theme() 호출을 자동 제거합니다.)
- 심층(TQL) 대시보드는 **패널 헤더가 없으므로** 각 차트가 **직접 제목+부제**를 표시: `title: { text: "제목", subtext: "부제", left: 10, top: 5 }` (Neo 표준 좌상단 위치). `grid.top`≈66 으로 제목 영역 확보(작으면 부제와 플롯이 붙어 보임).
- **하단 겹침 금지**: `grid: { bottom: 78 }` + `legend: { bottom: 30 }` + `dataZoom: [{ type:"slider", bottom: 6, height: 16 }, { type:"inside" }]`. `grid.bottom`을 작게 잡으면 범례가 x축 라벨과 겹칩니다(아래에서 위로 슬라이더→범례→x축라벨 순으로 쌓일 공간 필요).
- **y축 이름(`yAxis.name`)을 넣지 마세요** — 축 이름은 축 상단(좌상단)에 떠서 **제목/부제와 겹칩니다.** 축 의미는 부제에 적으세요(예: 부제 "… (단위: $)"). 꼭 필요하면 `nameLocation:"middle", nameGap:48, nameRotate:90`으로 세로 배치.
- **y축 값이 크면 라벨이 잘립니다** — 거래량 합계처럼 6자리 이상 값은 `grid.left`를 **85~95**로 키우세요(기본 72는 5자리까지). 이중 Y축(`yAxisIndex`)이면 `grid.right`도 같이 키우고, 오른쪽 축에도 `name`을 쓰지 마세요.

### 2. 시간축 — [timestamp, value] 페어
- 시계열 차트는 `xAxis: { type: "time" }` + `series.data` 에 **[timestamp, value] 페어 배열**을 넣습니다.
- SQL 결과(시간, 값)를 SCRIPT에서 `$.yield([$.values[0], $.values[1]])` 로 페어 yield → CHART에서 `data: column(0)`.
- TIME과 VALUE를 별도 컬럼/축으로 주거나 인덱스를 x축에 쓰면 **시간축이 깨집니다** (예: `09:00:00 030` 처럼 표시됨).
- ⚠️ **`$.values[0]`(TIME)은 숫자/문자열이 아니라 Time 객체입니다.** [t,v] 페어엔 그대로 넣으면 됩니다(Neo가 직렬화). 하지만 **일자 버킷 등 계산이 필요하면** `$.values[0].UnixNano() / 1000000` 로 ms를 얻어 `new Date(...)` 로 변환하세요. Time 객체에 직접 `/` · `Math.floor` 같은 산술을 하면 **`NaN`** 이 되어 데이터가 한 곳에 뭉쳐 **빈 차트**가 됩니다(실제 캔들스틱 버그였음).

### 3. NULL 회피
- 빈 시간 버킷의 집계, 0으로 나누기 등으로 **NULL 표현식**이 생기면 `MACH-ERR 2042 (Expression cannot have a NULL value)` 가 납니다.
- 1단계에서 확인한 데이터가 있는 기간만 조회하고, MAX-MIN/비율 등 NULL 가능 표현식은 데이터 유무를 확인하세요.

### 4. SQL 규칙
- `SQL(...)` 은 **백틱(`)** 으로 감싸고 큰따옴표(`"`) 금지.
- SQL() 안에서 시간 집계 시 **GROUP BY 필수**. 파일당 SQL() 은 1회만.
- ROLLUP은 **describe_table 결과가 `ROLLUP: available` 일 때만** 사용:
  - 표현식을 그대로 GROUP BY / ORDER BY 에 쓰고 **alias 금지** (예: `GROUP BY ROLLUP('day',1,TIME) ORDER BY ROLLUP('day',1,TIME)`).
  - 단위: `sec` / `min` / `hour` / `day` / `week` / `month` (**ms 불가**).
  - ROLLUP이 없는 테이블이면 `ROLLUP()` 쓰지 말고 원시 데이터를 시간순으로 조회하세요.
- **ROLLUP 쿼리에는 NAME(태그) 같은 비-ROLLUP 컬럼을 SELECT/GROUP BY에 넣지 마세요** → `MACH-ERR 2264`. 단일 태그를 `WHERE NAME = 'tag'` 로만 필터하고, SELECT에는 ROLLUP 표현식 + 집계(AVG/MAX/MIN/SUM 등)만.
  - **여러 태그 비교**는 ROLLUP 없이 raw 조회 + 위 "여러 태그 비교" 골격을 그대로 따르세요 (절대 `(time, name, value)` 로 yield하지 말 것). ROLLUP + 여러 태그 동시는 불가.
- 차트에는 `tz('Asia/Seoul')` 사용.

### 5. 자주 쓰는 계산
- RMS = `sqrt(SUMSQ(VALUE) / COUNT(VALUE))` — SQL에서 SUMSQ/COUNT를 구한 뒤 `MAPVALUE(1, sqrt(value(1)/value(2)))` → `POPVALUE(2)`.
- ROLLUP은 STDDEV를 지원하지 않습니다. 변동성은 MAX-MIN 또는 SUMSQ 기반으로.

