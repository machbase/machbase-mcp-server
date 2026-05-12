# TQL 분석 템플릿 모음

데이터 성질에 맞는 템플릿을 선택하세요. `{TABLE}`, `{TAG}`, `{UNIT}`을 실제 값으로 교체하세요.

## 사용법
1. 데이터 성질에 맞는 분야를 선택 (금융/센서·진동/일반)
2. 선택한 분야의 템플릿을 선택하여 `{TABLE}`, `{TAG}`, `{UNIT}`을 실제 값으로 교체 -> **아래 변수 설명 준수**
3. `save_tql_file`로 저장
4. `add_chart_to_dashboard`에서 `chart_type="Tql chart"`, `tql_path` 지정

## 변수 설명
| 변수 | 설명 | 예시 |
|------|------|------|
| {TABLE} | 대상 TAG 테이블명 | STAT, GOLD, BEARING |
| {TAG} | list_table_tags로 확인한 실제 태그명 | machbase:http:latency, open |
| {TAG1}, {TAG2} | 비교 템플릿용 태그 2개 | TAG1:open, TAG2:close |
| {UNIT} | ROLLUP 시간 단위 (아래 6개만 허용) | 'sec', 'min', 'hour', 'day', 'week', 'month' |
| {TIME_START} | 조회 시작 시간 (datetime 문자열) | 2024-01-20 00:00:00 |
| {TIME_END} | 조회 종료 시간 (datetime 문자열) | 2024-01-20 23:57:00 |

## ROLLUP 시간 단위 선택 가이드 ({UNIT} 값)

데이터의 시간 범위와 밀도에 따라 적절한 단위를 선택하세요.

| 단위 | 값 | 적합한 데이터 | 데이터 시간 범위 |
|------|------|--------------|----------------|
| 초 | `'sec'` | 고빈도 센서/진동 (kHz~Hz) | 수분 ~ 수시간 |
| 분 | `'min'` | 중빈도 IoT/모니터링 | 수시간 ~ 수일 |
| 시간 | `'hour'` | 장기 센서/시스템 로그 | 수일 ~ 수주 |
| 일 | `'day'` | 금융 일봉, 일별 집계 | 수주 ~ 수년 |
| 주 | `'week'` | 주간 추세 분석 | 수개월 ~ 수년 |
| 월 | `'month'` | 월간/연간 장기 추세 | 수년 이상 |

선택 기준: 차트에 100~5000개 데이터 포인트가 나오도록 단위를 선택하세요.
- 2시간 데이터 → `'sec'` (7200포인트)
- 30일 데이터 → `'hour'` (720포인트) 또는 `'day'` (30포인트)
- 2년 금융 데이터 → `'day'` (730포인트) 또는 `'week'` (104포인트)

---

## 1. 금융 데이터 (주가, 환율, 원자재 등)
OHLC(open/high/low/close) + volume 구조의 데이터에 적합합니다.

### 1-1. 일별 롤업 평균 (장기 추세)
용도: 평균 가격으로 장기 추세를 파악합니다.
```tql
SQL(`SELECT ROLLUP({UNIT}, 1, TIME), AVG(VALUE) FROM {TABLE} WHERE NAME = '{TAG}' AND TIME BETWEEN TO_DATE('{TIME_START}') AND TO_DATE('{TIME_END}') GROUP BY ROLLUP({UNIT}, 1, TIME) ORDER BY ROLLUP({UNIT}, 1, TIME)`)
SCRIPT({
    $.yield([$.values[0], $.values[1]])
})
CHART(
    tz('Asia/Seoul'),
    chartOption({
        title: { text: "{TAG} 평균 추세", left: "center", textStyle: { fontSize: 14 } },
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "Price" },
        dataZoom: [{ type: "slider" }, { type: "inside" }],
        series: [{ type: "line", smooth: true, data: column(0) }]
    })
)
```

### 1-2. 주별 변동성 (가격 변동 폭)
용도: MAX-MIN 차이로 변동성을 시각화합니다.
```tql
SQL(`SELECT ROLLUP({UNIT}, 1, TIME), MAX(VALUE), MIN(VALUE) FROM {TABLE} WHERE NAME = '{TAG}' AND TIME BETWEEN TO_DATE('{TIME_START}') AND TO_DATE('{TIME_END}') GROUP BY ROLLUP({UNIT}, 1, TIME) ORDER BY ROLLUP({UNIT}, 1, TIME)`)
MAPVALUE(1, value(1) - value(2))
POPVALUE(2)
SCRIPT({
    $.yield([$.values[0], $.values[1]])
})
CHART(
    tz('Asia/Seoul'),
    chartOption({
        title: { text: "{TAG} 변동성", left: "center", textStyle: { fontSize: 14 } },
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "Volatility" },
        dataZoom: [{ type: "slider" }, { type: "inside" }],
        series: [{ type: "bar", data: column(0) }]
    })
)
```

### 1-3. 가격 범위 밴드 (MIN/MAX/AVG 엔벨로프)
용도: 가격의 상한/하한/평균 밴드를 오버레이하여 가격 범위를 파악합니다.
```tql
SQL(`SELECT ROLLUP({UNIT}, 1, TIME), MAX(VALUE), MIN(VALUE), AVG(VALUE) FROM {TABLE} WHERE NAME = '{TAG}' AND TIME BETWEEN TO_DATE('{TIME_START}') AND TO_DATE('{TIME_END}') GROUP BY ROLLUP({UNIT}, 1, TIME) ORDER BY ROLLUP({UNIT}, 1, TIME)`)
SCRIPT({
    var maxArr = [];
    var minArr = [];
    var avgArr = [];
},{
    maxArr.push([$.values[0], $.values[1]]);
    minArr.push([$.values[0], $.values[2]]);
    avgArr.push([$.values[0], $.values[3]]);
},{
    for (var i = 0; i < maxArr.length; i++) {
        $.yield(maxArr[i], minArr[i], avgArr[i]);
    }
})
CHART(
    tz('Asia/Seoul'),
    chartOption({
        title: { text: "{TAG} 가격 밴드", left: "center", textStyle: { fontSize: 14 } },
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "Price" },
        dataZoom: [{ type: "slider" }, { type: "inside" }],
        series: [
            { type: "line", name: "MAX", data: column(0) },
            { type: "line", name: "MIN", data: column(1) },
            { type: "line", name: "AVG", data: column(2), lineStyle: { type: "dashed" } }
        ]
    })
)
```

### 1-4. 두 태그 비교 (Open vs Close 등)
용도: 두 태그를 오버레이하여 비교합니다. {TAG1}과 {TAG2}를 교체하세요.
```tql
SQL(`SELECT NAME, TIME, VALUE FROM {TABLE} WHERE NAME IN ('{TAG1}', '{TAG2}') AND TIME BETWEEN TO_DATE('{TIME_START}') AND TO_DATE('{TIME_END}') GROUP BY NAME, TIME, VALUE ORDER BY TIME LIMIT 500`)
SCRIPT({
    var arr1 = [];
    var arr2 = [];
},{
    if ($.values[0] == "{TAG1}") {
        arr1.push([$.values[1], $.values[2]]);
    } else {
        arr2.push([$.values[1], $.values[2]]);
    }
},{
    for (var i = 0; i < arr1.length; i++) {
        $.yield(arr1[i], arr2[i] || [0, 0]);
    }
})
CHART(
    tz('Asia/Seoul'),
    chartOption({
        title: { text: "{TAG1} vs {TAG2} 비교", left: "center", textStyle: { fontSize: 14 } },
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "Price" },
        dataZoom: [{ type: "slider" }, { type: "inside" }],
        series: [
            { type: "line", name: "{TAG1}", data: column(0) },
            { type: "line", name: "{TAG2}", data: column(1) }
        ]
    })
)
```

### 1-5. 거래량 추세 (합계)
용도: 거래량 합계로 거래 활성도를 파악합니다. volume 태그에 적합.
```tql
SQL(`SELECT ROLLUP({UNIT}, 1, TIME), SUM(VALUE) FROM {TABLE} WHERE NAME = '{TAG}' AND TIME BETWEEN TO_DATE('{TIME_START}') AND TO_DATE('{TIME_END}') GROUP BY ROLLUP({UNIT}, 1, TIME) ORDER BY ROLLUP({UNIT}, 1, TIME)`)
SCRIPT({
    $.yield([$.values[0], $.values[1]])
})
CHART(
    tz('Asia/Seoul'),
    chartOption({
        title: { text: "{TAG} 거래량 추세", left: "center", textStyle: { fontSize: 14 } },
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "Volume" },
        dataZoom: [{ type: "slider" }, { type: "inside" }],
        series: [{ type: "bar", data: column(0) }]
    })
)
```

### 1-6. 로그 가격 (수익률 분석)
용도: 로그 스케일로 가격을 변환하여 장기 수익률 추세를 분석합니다.
```tql
SQL(`SELECT ROLLUP({UNIT}, 1, TIME), AVG(VALUE) FROM {TABLE} WHERE NAME = '{TAG}' AND TIME BETWEEN TO_DATE('{TIME_START}') AND TO_DATE('{TIME_END}') GROUP BY ROLLUP({UNIT}, 1, TIME) ORDER BY ROLLUP({UNIT}, 1, TIME)`)
MAPVALUE(1, log(value(1)))
SCRIPT({
    $.yield([$.values[0], $.values[1]])
})
CHART(
    tz('Asia/Seoul'),
    chartOption({
        title: { text: "{TAG} 로그 가격", left: "center", textStyle: { fontSize: 14 } },
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "Log Price" },
        dataZoom: [{ type: "slider" }, { type: "inside" }],
        series: [{ type: "line", data: column(0) }]
    })
)
```

---

## 2. 센서/진동 데이터 (베어링, 모터, 가속도계 등)
고빈도 시계열 데이터, 진동 분석에 적합합니다.

### 2-1. RMS (Root Mean Square, 에너지 수준)
용도: 시간 구간별 RMS 값으로 진동 에너지 수준을 모니터링합니다.
```tql
SQL(`SELECT ROLLUP({UNIT}, 1, TIME), SUMSQ(VALUE), COUNT(VALUE) FROM {TABLE} WHERE NAME = '{TAG}' AND TIME BETWEEN TO_DATE('{TIME_START}') AND TO_DATE('{TIME_END}') GROUP BY ROLLUP({UNIT}, 1, TIME) ORDER BY ROLLUP({UNIT}, 1, TIME)`)
MAPVALUE(1, sqrt(value(1)/value(2)))
POPVALUE(2)
SCRIPT({
    $.yield([$.values[0], $.values[1]])
})
CHART(
    tz('Asia/Seoul'),
    chartOption({
        title: { text: "{TAG} RMS", left: "center", textStyle: { fontSize: 14 } },
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "RMS" },
        dataZoom: [{ type: "slider" }, { type: "inside" }],
        series: [{ type: "line", data: column(0) }]
    })
)
```

### 2-2. FFT (주파수 분석)
용도: 진동 데이터의 주파수 성분을 분석합니다. 주요 주파수 피크를 확인할 수 있습니다.
주의: SQL_SELECT는 from(테이블, 태그)과 between(시작, 끝) 형식을 사용합니다.
```tql
SQL_SELECT('time', 'value', from('{TABLE}', '{TAG}'), between('last-10s', 'last'))
MAPKEY('sample')
GROUPBYKEY()
FFT()
CHART_LINE(
    title('{TAG} FFT 주파수 분석'),
    size("600px", "350px"),
    xAxis(0, 'Hz'),
    yAxis(1, 'Amplitude'),
    dataZoom('slider', 0, 10)
)
```

### 2-3. Peak Envelope (최대값 포락선)
용도: 시간 구간별 최대값으로 포락선을 그려 피크 추세를 파악합니다.
```tql
SQL(`SELECT ROLLUP({UNIT}, 1, TIME), MAX(VALUE) FROM {TABLE} WHERE NAME = '{TAG}' AND TIME BETWEEN TO_DATE('{TIME_START}') AND TO_DATE('{TIME_END}') GROUP BY ROLLUP({UNIT}, 1, TIME) ORDER BY ROLLUP({UNIT}, 1, TIME)`)
SCRIPT({
    $.yield([$.values[0], $.values[1]])
})
CHART(
    tz('Asia/Seoul'),
    chartOption({
        title: { text: "{TAG} Peak Envelope", left: "center", textStyle: { fontSize: 14 } },
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "Peak" },
        dataZoom: [{ type: "slider" }, { type: "inside" }],
        series: [{ type: "line", data: column(0), areaStyle: { opacity: 0.3 } }]
    })
)
```

### 2-4. Peak-to-Peak (진폭 범위)
용도: 시간 구간별 MAX-MIN 차이로 진폭 범위를 측정합니다.
```tql
SQL(`SELECT ROLLUP({UNIT}, 1, TIME), MAX(VALUE), MIN(VALUE) FROM {TABLE} WHERE NAME = '{TAG}' AND TIME BETWEEN TO_DATE('{TIME_START}') AND TO_DATE('{TIME_END}') GROUP BY ROLLUP({UNIT}, 1, TIME) ORDER BY ROLLUP({UNIT}, 1, TIME)`)
MAPVALUE(1, value(1) - value(2))
POPVALUE(2)
SCRIPT({
    $.yield([$.values[0], $.values[1]])
})
CHART(
    tz('Asia/Seoul'),
    chartOption({
        title: { text: "{TAG} Peak-to-Peak", left: "center", textStyle: { fontSize: 14 } },
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "Peak-to-Peak" },
        dataZoom: [{ type: "slider" }, { type: "inside" }],
        series: [{ type: "line", data: column(0) }]
    })
)
```

### 2-5. Crest Factor (충격 지표)
용도: MAX/RMS 비율로 충격 성분을 감지합니다. 높은 값은 충격성 진동을 의미합니다.
```tql
SQL(`SELECT ROLLUP({UNIT}, 1, TIME), MAX(VALUE), SUMSQ(VALUE), COUNT(VALUE) FROM {TABLE} WHERE NAME = '{TAG}' AND TIME BETWEEN TO_DATE('{TIME_START}') AND TO_DATE('{TIME_END}') GROUP BY ROLLUP({UNIT}, 1, TIME) ORDER BY ROLLUP({UNIT}, 1, TIME)`)
MAPVALUE(1, value(1) / sqrt(value(2)/value(3)))
POPVALUE(2)
POPVALUE(2)
SCRIPT({
    $.yield([$.values[0], $.values[1]])
})
CHART(
    tz('Asia/Seoul'),
    chartOption({
        title: { text: "{TAG} Crest Factor", left: "center", textStyle: { fontSize: 14 } },
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "Crest Factor" },
        dataZoom: [{ type: "slider" }, { type: "inside" }],
        series: [{ type: "line", data: column(0) }]
    })
)
```

### 2-6. 데이터 밀도 (측정 빈도)
용도: 시간 구간별 데이터 개수로 센서의 측정 빈도나 누락을 확인합니다.
```tql
SQL(`SELECT ROLLUP({UNIT}, 1, TIME), COUNT(VALUE) FROM {TABLE} WHERE NAME = '{TAG}' AND TIME BETWEEN TO_DATE('{TIME_START}') AND TO_DATE('{TIME_END}') GROUP BY ROLLUP({UNIT}, 1, TIME) ORDER BY ROLLUP({UNIT}, 1, TIME)`)
SCRIPT({
    $.yield([$.values[0], $.values[1]])
})
CHART(
    tz('Asia/Seoul'),
    chartOption({
        title: { text: "{TAG} 데이터 밀도", left: "center", textStyle: { fontSize: 14 } },
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "Count" },
        dataZoom: [{ type: "slider" }, { type: "inside" }],
        series: [{ type: "bar", data: column(0) }]
    })
)
```

### 2-7. 에너지 스펙트럼 (시간-주파수 3D)
용도: 시간에 따른 주파수 변화를 3D로 시각화합니다. 주파수 성분이 시간에 따라 어떻게 변하는지 확인합니다.
주의: 고빈도 진동 데이터에 적합. roundTime으로 시간 윈도우를 분할합니다.
```tql
SQL_SELECT('time', 'value', from('{TABLE}', '{TAG}'), between('last-10s', 'last'))
MAPKEY( roundTime(value(0), '500ms') )
GROUPBYKEY()
FFT(minHz(0), maxHz(100))
FLATTEN()
PUSHKEY('fft')
CHART_BAR3D(
    title('{TAG} 3D Energy Spectrum'),
    xAxis(0, 'time', 'time'),
    yAxis(1, 'Hz'),
    zAxis(2, 'Amp'),
    size('600px', '600px'), visualMap(0, 1.5)
)
```

---

## 3. 일반 시계열 (범용)
모든 TAG 테이블에 적용 가능한 범용 템플릿입니다.

### 3-1. 시간 단위 롤업 (평균)
용도: 지정한 시간 단위로 평균값을 집계합니다.
```tql
SQL(`SELECT ROLLUP({UNIT}, 1, TIME), AVG(VALUE) FROM {TABLE} WHERE NAME = '{TAG}' AND TIME BETWEEN TO_DATE('{TIME_START}') AND TO_DATE('{TIME_END}') GROUP BY ROLLUP({UNIT}, 1, TIME) ORDER BY ROLLUP({UNIT}, 1, TIME)`)
SCRIPT({
    $.yield([$.values[0], $.values[1]])
})
CHART(
    tz('Asia/Seoul'),
    chartOption({
        title: { text: "{TAG} 롤업 평균", left: "center", textStyle: { fontSize: 14 } },
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "Average" },
        dataZoom: [{ type: "slider" }, { type: "inside" }],
        series: [{ type: "line", smooth: true, data: column(0) }]
    })
)
```

### 3-2. 태그 간 비교 (두 태그 오버레이)
용도: 두 태그의 시계열을 겹쳐서 상관관계를 비교합니다. {TAG1}과 {TAG2}를 교체하세요.
```tql
SQL(`SELECT NAME, TIME, VALUE FROM {TABLE} WHERE NAME IN ('{TAG1}', '{TAG2}') AND TIME BETWEEN TO_DATE('{TIME_START}') AND TO_DATE('{TIME_END}') GROUP BY NAME, TIME, VALUE ORDER BY TIME LIMIT 500`)
SCRIPT({
    var arr1 = [];
    var arr2 = [];
},{
    if ($.values[0] == "{TAG1}") {
        arr1.push([$.values[1], $.values[2]]);
    } else {
        arr2.push([$.values[1], $.values[2]]);
    }
},{
    for (var i = 0; i < arr1.length; i++) {
        $.yield(arr1[i], arr2[i] || [0, 0]);
    }
})
CHART(
    tz('Asia/Seoul'),
    chartOption({
        title: { text: "{TAG1} vs {TAG2} 비교", left: "center", textStyle: { fontSize: 14 } },
        xAxis: { type: "time" },
        yAxis: { type: "value" },
        dataZoom: [{ type: "slider" }, { type: "inside" }],
        series: [
            { type: "line", name: "{TAG1}", data: column(0) },
            { type: "line", name: "{TAG2}", data: column(1) }
        ]
    })
)
```

### 3-3. 데이터 카운트 추세
용도: 시간 구간별 데이터 건수로 데이터 수집 밀도나 결측을 확인합니다.
```tql
SQL(`SELECT ROLLUP({UNIT}, 1, TIME), COUNT(VALUE) FROM {TABLE} WHERE NAME = '{TAG}' AND TIME BETWEEN TO_DATE('{TIME_START}') AND TO_DATE('{TIME_END}') GROUP BY ROLLUP({UNIT}, 1, TIME) ORDER BY ROLLUP({UNIT}, 1, TIME)`)
SCRIPT({
    $.yield([$.values[0], $.values[1]])
})
CHART(
    tz('Asia/Seoul'),
    chartOption({
        title: { text: "{TAG} 카운트 추세", left: "center", textStyle: { fontSize: 14 } },
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "Data Count" },
        dataZoom: [{ type: "slider" }, { type: "inside" }],
        series: [{ type: "bar", data: column(0) }]
    })
)
```

### 3-4. MIN/MAX 엔벨로프 (이상치 범위)
용도: 시간 구간별 최대/최소 범위로 이상치 패턴을 감지합니다.
```tql
SQL(`SELECT ROLLUP({UNIT}, 1, TIME), MAX(VALUE), MIN(VALUE) FROM {TABLE} WHERE NAME = '{TAG}' AND TIME BETWEEN TO_DATE('{TIME_START}') AND TO_DATE('{TIME_END}') GROUP BY ROLLUP({UNIT}, 1, TIME) ORDER BY ROLLUP({UNIT}, 1, TIME)`)
SCRIPT({
    var maxArr = [];
    var minArr = [];
},{
    maxArr.push([$.values[0], $.values[1]]);
    minArr.push([$.values[0], $.values[2]]);
},{
    for (var i = 0; i < maxArr.length; i++) {
        $.yield(maxArr[i], minArr[i]);
    }
})
CHART(
    tz('Asia/Seoul'),
    chartOption({
        title: { text: "{TAG} MIN/MAX Envelope", left: "center", textStyle: { fontSize: 14 } },
        xAxis: { type: "time" },
        yAxis: { type: "value" },
        dataZoom: [{ type: "slider" }, { type: "inside" }],
        series: [
            { type: "line", name: "MAX", data: column(0), lineStyle: { color: "#FF4444" } },
            { type: "line", name: "MIN", data: column(1), lineStyle: { color: "#4444FF" } }
        ]
    })
)
```
