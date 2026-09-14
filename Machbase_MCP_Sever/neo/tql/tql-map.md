# Machbase Neo TQL MAP Functions

*MAP* 함수는 데이터 변환의 핵심입니다.

## TAKE()

**문법**: `TAKE( [offset,] n )`

앞의 *n*개 레코드를 취하고 스트림을 멈춥니다.

- `offset` *숫자* 선택. 해당 위치부터 레코드를 취합니다. (생략 시 기본값 0) (v8.0.6부터)
- `n` *숫자* 취할 레코드 수를 지정합니다.

**예제: TAKE(n)**

```js
FAKE( json({
    [ "TAG0", 1628694000000000000, 10],
    [ "TAG0", 1628780400000000000, 11],
    [ "TAG0", 1628866800000000000, 12],
    [ "TAG0", 1628953200000000000, 13],
    [ "TAG0", 1629039600000000000, 14],
    [ "TAG0", 1629126000000000000, 15]
}))
TAKE(2)
CSV()
```

```csv
TAG0,1628694000000000000,10
TAG0,1628780400000000000,11
```

**예제: TAKE(offset, n)**

```js
FAKE( json({
    [ "TAG0", 1628694000000000000, 10],
    [ "TAG0", 1628780400000000000, 11],
    [ "TAG0", 1628866800000000000, 12],
    [ "TAG0", 1628953200000000000, 13],
    [ "TAG0", 1629039600000000000, 14],
    [ "TAG0", 1629126000000000000, 15]
}))
TAKE(3, 2)
CSV()
```

```csv
TAG0,1628953200000000000,13
TAG0,1629039600000000000,14
```

## DROP()

**문법**: `DROP( [offset,] n  )`

앞의 *n*개 레코드를 무시합니다. 즉 *n*개를 버립니다.

- `offset` *숫자* 선택. 해당 위치부터 레코드를 버립니다. (생략 시 기본값 0) (v8.0.6부터)
- `n` *숫자* 버릴 레코드 수를 지정합니다.

**예제: DROP(n)**

```js
FAKE( json({
    [ "TAG0", 1628694000000000000, 10],
    [ "TAG0", 1628780400000000000, 11],
    [ "TAG0", 1628866800000000000, 12],
    [ "TAG0", 1628953200000000000, 13],
    [ "TAG0", 1629039600000000000, 14],
    [ "TAG0", 1629126000000000000, 15]
}))
DROP(3)
CSV()
```

```csv
TAG0,1628953200000000000,13
TAG0,1629039600000000000,14
TAG0,1629126000000000000,15
```

**예제: DROP(offset, n)**

```js
FAKE( json({
    [ "TAG0", 1628694000000000000, 10],
    [ "TAG0", 1628780400000000000, 11],
    [ "TAG0", 1628866800000000000, 12],
    [ "TAG0", 1628953200000000000, 13],
    [ "TAG0", 1629039600000000000, 14],
    [ "TAG0", 1629126000000000000, 15]
}))
DROP(2, 3)
CSV()
```

```csv
TAG0,1628694000000000000,10
TAG0,1628780400000000000,11
TAG0,1629126000000000000,15
```

## FILTER()

**문법**: `FILTER( condition )`

들어온 레코드에 조건문을 적용해, *condition*이 *true*일 때만 레코드를 통과시킵니다.

예를 들어 원래 레코드가 `{key: k1, value[v1, v2]}` 일 때 `FILTER(count(V) > 2)`를 적용하면 레코드가 버려집니다. 조건이 `FILTER(count(V) >= 2)` 였다면 레코드를 다음 함수로 넘깁니다.

```js
FAKE( json({
    [ "TAG0", 1628694000000000000, 10],
    [ "TAG0", 1628780400000000000, 11],
    [ "TAG0", 1628866800000000000, 12],
    [ "TAG0", 1628953200000000000, 13],
    [ "TAG0", 1629039600000000000, 14],
    [ "TAG0", 1629126000000000000, 15]
}))
FILTER( value(2) < 12 )
CSV()
```

```csv
TAG0,1628694000000000000,10
TAG0,1628780400000000000,11
```

## FILTER_CHANGED()

**문법**: `FILTER_CHANGED( value [, retain(time, duration)] [, useFirstWithLast()] )` (since v8.0.15)

- `retain(time, duration)`
- `useFirstWithLast(boolean)`

이전과 값이 달라진 `value`만 통과시킵니다.
첫 레코드는 항상 통과합니다. 첫 레코드를 버리려면 `FILTER_CHANGED()` 뒤에 `DROP(1)`을 사용하세요.

`retain()` 옵션을 지정하면, 바뀐 `value`를 `time` 기준으로 주어진 `duration` 동안 유지한 레코드만 통과합니다.

**예제: 기본 사용법**

```js
FAKE(json({
    ["A", 1692329338, 1.0],
    ["A", 1692329339, 2.0],
    ["B", 1692329340, 3.0],
    ["B", 1692329341, 4.0],
    ["B", 1692329342, 5.0],
    ["B", 1692329343, 6.0],
    ["B", 1692329344, 7.0],
    ["B", 1692329345, 8.0],
    ["C", 1692329346, 9.0],
    ["D", 1692329347, 9.1]
}))
MAPVALUE(1, parseTime(value(1), "s"))
FILTER_CHANGED(value(0))
CSV(timeformat("s"))
```

```csv
A,1692329338,1
B,1692329340,3
C,1692329346,9
D,1692329347,9.1
```

**예제: retain() 사용**

```js
FAKE(json({
    ["A", 1692329338, 1.0],
    ["A", 1692329339, 2.0],
    ["B", 1692329340, 3.0],
    ["B", 1692329341, 4.0],
    ["B", 1692329342, 5.0],
    ["B", 1692329343, 6.0],
    ["B", 1692329344, 7.0],
    ["B", 1692329345, 8.0],
    ["C", 1692329346, 9.0],
    ["D", 1692329347, 9.1]
}))
MAPVALUE(1, parseTime(value(1), "s"))
FILTER_CHANGED(value(0), retain(value(1), "2s"))
CSV(timeformat("s"))
```

```csv
A,1692329338,1
B,1692329342,5
```

**예제: retain()과 useFirstWithLast(false) 사용**

```js
FAKE(json({
    ["A", 1692329338, 1.0],
    ["A", 1692329339, 2.0],
    ["B", 1692329340, 3.0],
    ["B", 1692329341, 4.0],
    ["B", 1692329342, 5.0],
    ["B", 1692329343, 6.0],
    ["B", 1692329344, 7.0],
    ["B", 1692329345, 8.0],
    ["C", 1692329346, 9.0],
    ["D", 1692329347, 9.1]
}))
MAPVALUE(1, parseTime(value(1), "s"))
FILTER_CHANGED(value(0), retain(value(1), "2s"), useFirstWithLast(false))
CSV(timeformat("s"))
```

```csv
A,1692329338,1
B,1692329340,3
```

**예제: useFirstWithLast(true) 사용**

```js
FAKE(json({
    ["A", 1692329338, 1.0],
    ["A", 1692329339, 2.0],
    ["B", 1692329340, 3.0],
    ["B", 1692329341, 4.0],
    ["B", 1692329342, 5.0],
    ["B", 1692329343, 6.0],
    ["B", 1692329344, 7.0],
    ["B", 1692329345, 8.0],
    ["C", 1692329346, 9.0],
    ["D", 1692329347, 9.1]
}))
MAPVALUE(1, parseTime(value(1), "s"))
FILTER_CHANGED(value(0), useFirstWithLast(true))
CSV(timeformat("s"))
```

```csv
A,1692329338,1
A,1692329339,2
B,1692329340,3
B,1692329345,8
C,1692329346,9
C,1692329346,9
D,1692329347,9.1
D,1692329347,9.1
```

## SET()

**문법**: `SET(name, expression)` (since v8.0.12)

- `name` *keyword* 변수 이름
- `expression` *표현식* 값

*SET*은 주어진 이름과 값으로 레코드 범위의 변수를 정의합니다. `SET(var, 10)`으로 변수 `var`를 정의하면 `$var`로 참조할 수 있습니다. 변수는 값의 일부가 아니므로 SINK의 최종 결과에는 포함되지 않습니다.

```js
FAKE( linspace(0, 1, 3))
SET(temp, value(0) * 10)
SET(temp, $temp + 1)
MAPVALUE(1, $temp)
CSV()
```

```csv
0,1
0.5,6
1,11
```

## GROUP()

**문법**: `GROUP( [lazy(boolean),] by [, aggregators...] )` (since v8.0.7)

- `lazy(boolean)` 기본값인 `false`이면 `by()`의 값이 이전 레코드와 달라질 때마다 *GROUP()* 이 새 집계 레코드를 내보냅니다. `true`이면 *GROUP()* 은 입력 스트림이 끝날 때까지 기다렸다가 레코드를 내보냅니다.

- `by(value [, label])` 값을 어떻게 묶을지 지정하는 값.

- `aggregators` *집계 함수 배열* 집계 함수들

그룹 집계 함수입니다. 자세한 설명은 GROUP() 항목을 참고하세요.

## PUSHVALUE()

**문법**: `PUSHVALUE( idx, value [, name] )` (since v8.0.5)

- `idx` *number* newValue를 삽입할 위치의 인덱스입니다. (0부터 시작)
- `value` *표현식* 새 값
- `name` *string* 컬럼 이름입니다. (기본값 'column')

주어진 값(새 컬럼)을 현재 값들에 삽입합니다.

```js
FAKE( linspace(0, 1, 3))
PUSHVALUE(1, value(0) * 10)
CSV()
```

```csv
0.0,0
0.5,5
1.0,10
```

## POPVALUE()

**문법**: `POPVALUE( idx [, idx2, idx3, ...] )` (since v8.0.5)

- `idx` *number* 값에서 제거할 인덱스들의 배열입니다

값 배열에서 `idx`로 지정한 컬럼을 제거합니다.

```js
FAKE( linspace(0, 1, 3))
PUSHVALUE(1, value(0) * 10)
POPVALUE(0)
CSV()
```

```csv
0
5
10
```

## MAPVALUE()

**문법**: `MAPVALUE( idx, newValue [, newName] )`

- `idx` *number*  값 튜플의 인덱스입니다. (0부터 시작)
- `newValue` *expression* 새 값입니다
- `newName` *string* 컬럼 이름을 주어진 문자열로 바꿉니다

`MAPVALUE()`는 주어진 인덱스 위치의 값을 바꿉니다. 예를 들어 `MAPVALUE(0, value(0)*10)`은 값 튜플의 첫 요소를 10배한 값으로 바꿉니다.

`idx`가 범위를 벗어나면 `PUSHVALUE()`처럼 동작합니다. `MAPVALUE(-1, value(1)+'_suffix')`는 값의 두 번째 요소에 '_suffix'를 붙인 새 문자열 값을 삽입합니다.

```js
FAKE( linspace(0, 1, 3))
MAPVALUE(0, value(0) * 10)
CSV()
```

```csv
0
5
10
```

`MAPVALUE`로 수학 연산을 사용하는 예제입니다.

```js
FAKE(
    meshgrid(
        linspace(-4,4,100),
        linspace(-4,4, 100)
    )
)
MAPVALUE(2, sin(pow(value(0), 2) + pow(value(1), 2)) / (pow(value(0), 2) + pow(value(1), 2)))
MAPVALUE(0, list(value(0), value(1), value(2)))
POPVALUE(1, 2)
CHART(
    plugins("gl"),
    size("600px", "600px"),
    chartOption({
        grid3D:{},
        xAxis3D:{}, yAxis3D:{}, zAxis3D:{},
        series:[
            {type: "line3D", data: column(0)},
        ]
    })
)
```

## MAP_DIFF()

**문법**: `MAP_DIFF( idx, value [, newName] )` (since v8.0.8)

- `idx` *number*  값 튜플의 인덱스입니다. (0부터 시작)
- `value` *number*
- `newName` *string* 컬럼 이름을 주어진 문자열로 바꿉니다

`MAP_DIFF()`는 주어진 인덱스 위치의 값을 현재와 이전 값의 차이(*현재 - 이전*)로 바꿉니다. 

```js
FAKE( linspace(0.5, 3, 10) )
MAPVALUE(0, log(value(0)), "VALUE")
MAP_DIFF(1, value(0), "DIFF")
CSV( header(true), precision(3) )
```

```csv
VALUE,DIFF
-0.693,NULL
-0.251,0.442
0.054,0.305
0.288,0.234
0.477,0.189
0.636,0.159
0.773,0.137
0.894,0.121
1.001,0.108
1.099,0.097
```

## MAP_ABSDIFF()

**문법**: `MAP_ABSDIFF( idx, value [, label]  )` (since v8.0.8)

- `idx` *number*  값 튜플의 인덱스입니다. (0부터 시작)
- `value` *number*
- `label` *string* 컬럼 라벨을 주어진 문자열로 바꿉니다

`MAP_ABSDIFF()`는 주어진 인덱스 위치의 값을 현재와 이전 값의 절대 차이 abs(*현재 - 이전*)로 바꿉니다.

## MAP_NONEGDIFF()

**문법**: `MAP_NONEGDIFF( idx, value [, label]  )` (since v8.0.8)

- `idx` *number*  값 튜플의 인덱스입니다. (0부터 시작)
- `value` *number*
- `label` *string* 컬럼 라벨을 주어진 문자열로 바꿉니다

`MAP_NONEGDIFF()`는 주어진 인덱스 위치의 값을 현재와 이전 값의 차이(*현재 - 이전*)로 바꿉니다. 
차이가 0보다 작으면 음수 대신 0을 적용합니다.

## MAP_AVG()

**문법**: `MAP_AVG(idx, value [, label] )`  (since v8.0.15)

- `idx` *number*  값 튜플의 인덱스입니다. (0부터 시작)
- `value` *number*
- `label` *string* 컬럼 라벨을 주어진 문자열로 바꿉니다

`MAP_AVG`는 주어진 인덱스 위치의 값을 값들의 평균(평균 필터)으로 설정합니다.

$k$는 데이터의 개수입니다.

Let $\alpha = \frac{1}{k}$

$\overline{x_k} = (1 - \alpha) \overline{x_{k-1}} + \alpha x_k$

```js
FAKE(arrange(0, 1000, 1))
MAPVALUE(1, sin(2 * PI *10*value(0)/1000))
MAP_AVG(2, value(1))
CHART(
    chartOption({
        xAxis:{ type:"category", data:column(0)},
        yAxis:{},
        series:[
            { type:"line", data:column(1), name:"RAW" },
            { type:"line", data:column(2), name:"AVG" }
        ],
        legend:{ bottom:10}
    })
)
```

## MAP_MOVAVG()

**문법**: `MAP_MOVAVG(idx, value, window [, label] )`  (since v8.0.8)

- `idx` *number*  값 튜플의 인덱스입니다. (0부터 시작)
- `value` *number*
- `window` *숫자* 몇 개의 레코드를 누적할지 지정합니다.
- `label` *string* 컬럼 라벨을 주어진 문자열로 바꿉니다

`MAP_MOVAVG`는 주어진 인덱스 위치의 값을 지정한 window 개수만큼의 이동평균으로 설정합니다.
값이 `window`만큼 누적되지 않았으면 대신 `sum/값의개수`를 적용합니다.
최근 `window` 개수만큼의 값이 모두 `NULL`(또는 숫자가 아님)이면 `NULL`을 적용합니다.
누적된 값 중 일부가 `NULL`(또는 숫자가 아님)이면 `NULL`을 제외한 유효한 값들로만 평균을 계산합니다.

```js
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig + $noise)
MAP_MOVAVG(2, value(1), 10)
CHART(
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"MA(10)" },
        ],
        legend: { bottom: 10 }
    })
)
```

## MAP_LOWPASS()

**문법**: `MAP_LOWPASS(idx, value, alpha [, label] )` (since v8.0.15)

- `idx` *number*  값 튜플의 인덱스입니다. (0부터 시작)
- `value` *number*
- `alpha` *숫자*, 0 < alpha < 1
- `label` *string* 컬럼 라벨을 주어진 문자열로 바꿉니다

`MAP_LOWPASS`는 주어진 인덱스 위치의 값을 지수 가중 이동평균으로 설정합니다.

When $ 0 < \alpha < 1$

$\overline{x_k} = (1 - \alpha) \overline{x_{k-1}} + \alpha x_k$

```js
FAKE(arrange(1,5,0.03))
MAPVALUE(0, round(value(0)*100)/100)
SET(sig, sin(1.2*2*PI*value(0)) )
SET(noise, 0.09*cos(9*2*PI*value(0)) + 0.15*sin(12*2*PI*value(0)))
MAPVALUE(1, $sig + $noise)
MAP_LOWPASS(2, $sig + $noise, 0.40)
CHART(
    chartOption({
        xAxis:{ type: "category", data: column(0)},
        yAxis:{ max:1.5, min:-1.5 },
        series:[
            { type: "line", data: column(1), name:"value+noise" },
            { type: "line", data: column(2), name:"lpf" },
        ],
        legend: { bottom: 10 }
    })
)
```

## MAP_KALMAN()

**문법**: `MAP_KALMAN(idx, value, model() [, label])` (since v8.0.15)
- `idx` *number*  값 튜플의 인덱스입니다. (0부터 시작)
- `value` *number*
- `model` *model(initial, progress, observation)* 시스템 행렬을 설정합니다
- `label` *string* 컬럼 라벨을 주어진 문자열로 바꿉니다

```js
FAKE(arrange(0, 10, 0.1))
MAPVALUE(0, round(value(0)*100)/100 )

SET(real, 14.4)
SET(noise, 4 * simplex(1234, value(0)))
SET(measure, $real + $noise)

MAPVALUE(1, $real )
MAPVALUE(2, $measure)
MAP_KALMAN(3, $measure, model(0.1, 0.001, 1.0))
CHART(
    chartOption({
        title:{text:"Kalman filter"},
        xAxis:{type:"category", data:column(0)},
        yAxis:{ min:10, max: 18 },
        series:[
            {type:"line", data:column(1), name:"real"},
            {type:"line", data:column(2), name:"measured"},
            {type:"line", data:column(3), name:"filtered"}
        ],
        tooltip: {show: true, trigger:"axis"},
        legend: { bottom: 10},
        animation: false
    })
)
```

## HISTOGRAM()

`HISTOGRAM()`에는 두 종류가 있습니다. 첫째는 "고정 구간"으로 입력 값 범위(min~max)가 예측 가능하거나 고정일 때 유용합니다. 둘째는 "동적 구간"으로 값 범위를 모를 때 유용합니다.

### Fixed Bins

**문법**: `HISTOGRAM(value, bins [, category] [, order] )`  (since v8.0.15)

- `value` *number*
- `bins` *bins(min, max, step)* 히스토그램 구간 설정.
- `category` *category(name_value)*
- `order` *order(name...string)* 카테고리 순서

`HISTOGRAM()`은 값들을 받아 각 구간의 분포를 셉니다. 구간은 값의 min/max 범위와 구간 개수로 설정합니다.
실제 값이 min/max 범위를 벗어나면 `HISTOGRAM()`이 더 낮거나 높은 구간을 자동으로 추가합니다.

**예제: CSV 출력**

```js
FAKE( arrange(1, 100, 1) )
MAPVALUE(0, (simplex(12, value(0)) + 1) * 100)
HISTOGRAM(value(0), bins(0, 200, 40))
CSV( precision(0), header(true) )
```

```csv
low,high,count
0,40,2
40,80,31
80,120,47
120,160,16
160,200,4
```

**예제: CHART 출력**

```js
FAKE( arrange(1, 100, 1) )
MAPVALUE(0, (simplex(12, value(0)) + 1) * 100)
HISTOGRAM(value(0), bins(0, 200, 40))
MAPVALUE(0, strSprintf("%.f~%.f", value(0), value(1)))
CHART(
    chartOption({
        xAxis:{ type:"category", data:column(0)},
        yAxis:{},
        tooltip:{trigger:"axis"},
        series:[
            {type:"bar", data: column(2)}
        ]
    })
)
```

**예제: CATEGORY 사용**

```js
FAKE( arrange(1, 100, 1) )
MAPVALUE(0, (simplex(12, value(0)) + 1) * 100)
PUSHVALUE(0, key() % 2 == 0 ? "Cat.A" : "Cat.B")
HISTOGRAM(value(1), bins(0, 200, 40), category(value(0)))
MAPVALUE(0, strSprintf("%.f~%.f", value(0), value(1)))
CHART(
    chartOption({
        xAxis:{ type:"category", data:column(0)},
        yAxis:{},
        tooltip:{trigger:"axis"},
        legend:{bottom:5},
        series:[
            {type:"bar", data: column(2), name:"Cat.A"},
            {type:"bar", data: column(3), name:"Cat.B"},
        ]
    })
)
```

### 동적 구간(Dynamic Bins)

**문법**: `HISTOGRAM(value [, bins(maxBins)] )`  (since v8.0.46)

- `value` *number*
- `bins` *숫자* 최대 구간 수를 지정합니다. 지정하지 않으면 기본값은 100입니다.

`HISTOGRAM()`은 값들과 최대 구간 수를 받습니다.
구간은 입력 값에 따라 동적으로 조정되며 지정한 `bins(maxBins)`까지 늘어날 수 있습니다.
결과의 `value` 컬럼은 각 구간의 평균값을 나타내고,
`count` 컬럼은 그 범위 안의 값 개수를 나타냅니다.
따라서 한 구간의 `value`와 `count`의 곱은 그 구간에 속한 값들의 합과 같습니다.

```js
FAKE( arrange(1, 100, 1) )
MAPVALUE(0, (simplex(12, value(0)) + 1) * 100)
HISTOGRAM(value(0), bins(5))
CSV( precision(0), header(true) )
```

```csv
value,count
47,12
75,29
99,29
119,18
156,12
```

## BOXPLOT()

**문법**: `BOXPLOT(value, category [, order] [, boxplotInterp] [, boxplotOutput])` (since v8.0.15)

- `value` *number*
- `category` *category(name_value)*
- `order` *order(name...string)* 카테고리 순서
- `boxplotOutput` *boxplotOutput( "" | "chart" | "dict" )*
- `boxplotInterp` *boxplotInterop(Q1 boolean, Q2 boolean, Q3 boolean)*

## TRANSPOSE()

**문법**: `TRANSPOSE( [fixed(columnIdx...) | columnIdx...] [, header(boolean)] )` (since v8.0.8)

TQL이 CSV나 'bridge'된 SQL 쿼리로 외부 RDBMS에서 데이터를 불러올 때, 레코드 형태를 MACHBASE TAG 테이블에 맞추기 위해 컬럼 전치가 필요할 수 있습니다.
`TRANSPOSE`는 여러 컬럼을 가진 레코드로부터 여러 레코드를 만듭니다.

- `fixed(columnIdx...)` 어떤 컬럼을 "고정"할지 지정합니다. 전치 대상 컬럼과 함께 쓸 수 없습니다.
- `columnIdx...` "전치"할 여러 컬럼을 지정합니다. "fixed()"와 함께 쓸 수 없습니다.
- `header(boolean)` `header(true)`로 지정하면 `TRANSPOSE`가 첫 레코드를 헤더 레코드로 간주합니다. 그리고 전치된 컬럼 레코드의 헤더를 새 컬럼으로 만들어 냅니다.

**예제: header를 사용한 TRANSPOSE**

```js
FAKE(csv(`CITY,DATE,TEMPERATURE,HUMIDITY,NOISE
Tokyo,2023/12/07,23,30,40
Beijing,2023/12/07,24,50,60
`))
TRANSPOSE( header(true), 2, 3, 4 )
MAPVALUE(0, strToUpper(value(0)) + "-" + value(2))
MAPVALUE(1, parseTime(value(1), sqlTimeformat("YYYY/MM/DD")))
MAPVALUE(3, parseFloat(value(3)))
POPVALUE(2)
CSV(timeformat("s"))
```

이 예제는 흔한 사용 사례입니다.

```csv
TOKYO-TEMPERATURE,1701907200,23
TOKYO-HUMIDITY,1701907200,30
TOKYO-NOISE,1701907200,40
BEIJING-TEMPERATURE,1701907200,24
BEIJING-HUMIDITY,1701907200,50
BEIJING-NOISE,1701907200,60
```

**예제: 전체 컬럼 TRANSPOSE**

```js
FAKE(csv(`CITY,DATE,TEMPERATURE,HUMIDITY,NOISE
Tokyo,2023/12/07,23,30,40
Beijing,2023/12/07,24,50,60
`))
TRANSPOSE()
CSV()
```

옵션이 없으면 모든 컬럼을 행으로 전치합니다.

```csv
CITY
DATE
TEMPERATURE
HUMIDITY
NOISE
Tokyo
2023/12/07
23
30
40
Beijing
2023/12/07
24
50
60
```

**예제: header()를 사용한 TRANSPOSE**

```js
FAKE(csv(`CITY,DATE,TEMPERATURE,HUMIDITY,NOISE
Tokyo,2023/12/07,23,30,40
Beijing,2023/12/07,24,50,60
`))
TRANSPOSE( header(true) )
CSV()
```

첫 레코드를 헤더로 취급하고 전치된 각 레코드에 새 컬럼을 추가합니다.

```csv
CITY,Tokyo
DATE,2023/12/07
TEMPERATURE,23
HUMIDITY,30
NOISE,40
CITY,Beijing
DATE,2023/12/07
TEMPERATURE,24
HUMIDITY,50
NOISE,60
```

**예제: fixed()를 사용한 TRANSPOSE**

```js
FAKE(csv(`CITY,DATE,TEMPERATURE,HUMIDITY,NOISE
Tokyo,2023/12/07,23,30,40
Beijing,2023/12/07,24,50,60
`))
TRANSPOSE( header(true), fixed(0, 1) )
// Equiv. with
// TRANSPOSE( header(true), 2, 3, 4 )
CSV()
```

새 레코드에 "fixed" 컬럼을 유지합니다.

```csv
Tokyo,2023/12/07,TEMPERATURE,23
Tokyo,2023/12/07,HUMIDITY,30
Tokyo,2023/12/07,NOISE,40
Beijing,2023/12/07,TEMPERATURE,24
Beijing,2023/12/07,HUMIDITY,50
Beijing,2023/12/07,NOISE,60
```

## FFT()

**문법**: `FFT([minHz(value), maxHz(value)])`
- `minHz(value`) *분석에 사용할 최소 Hz*
- `maxHz(value`) *분석에 사용할 최대 Hz*

들어온 레코드의 값이 *시간,진폭* 튜플 배열이라고 보고 *고속 푸리에 변환*을 적용해 값을 *주파수,진폭* 튜플 배열로 바꿉니다. 키는 그대로입니다.

예를 들어 들어온 레코드가 `{key: k, value[ [t1,a1],[t2,a2],...[tn,an] ]}` 이면 값을 `{key:k, value[ [F1,A1], [F2,A2],...[Fm,Am] ]}` 로 변환합니다.

```js
FAKE(
    oscillator(
        freq(15, 1.0), freq(24, 1.5),
        range('now', '10s', '1ms')
    ) 
)
MAPKEY('sample')
GROUPBYKEY()
FFT()
CHART_LINE(
    xAxis(0, 'Hz'),
    yAxis(1, 'Amplitude'),
    dataZoom('slider', 0, 10) 
)
```

3D 샘플 코드를 포함한 자세한 내용은 FFT() 항목을 참고하세요

## WHEN()

**문법**: `WHEN(condition, doer)` (since v8.0.7)

- `condition` *boolean*
- `doer` *doer*

`WHEN`은 주어진 조건이 `true`이면 `doer` 동작을 실행합니다.
이 함수는 레코드의 흐름에 영향을 주지 않고 정의된 *부수 작업*만 실행합니다.

### doLog()

**문법**: `doLog(args...)` (since v8.0.7)

웹 콘솔에 로그 메시지를 출력합니다.

```js
FAKE( linspace(1, 2, 2))
WHEN( mod(value(0), 2) == 0, doLog(value(0), "is even."))
CSV()
```

### doHttp()

**문법**: `doHttp(method, url, body [, header...])` (since v8.0.7)

- `method` *string*
- `url` *string*
- `body` *string*
- `header` *string* optional

`doHttp`는 주어진 메서드, URL, 본문, 헤더로 http 엔드포인트에 요청합니다.

**활용 사례**

- 특정 HTTP 엔드포인트로 이벤트를 알립니다.

```js
FAKE( linspace(1, 4, 4))
WHEN(
    mod(value(0), 2) == 0,
    doHttp("GET", strSprintf("http://127.0.0.1:8888/notify?value=%.0f", value(0)), nil)
)
CSV()
```

- `doHttp`의 기본 형식인 CSV로 현재 레코드를 특정 HTTP 엔드포인트에 전송합니다.

```js
FAKE( linspace(1, 4, 4))
WHEN(
    mod(value(0), 2) == 0,
    doHttp("POST", "http://127.0.0.1:8888/notify", value())
)
CSV()
```

- 현재 레코드를 사용자 정의 JSON 형식으로 특정 HTTP 엔드포인트에 전송합니다.

```js
FAKE( linspace(1, 4, 4))
WHEN(
    mod(value(0), 2) == 0,
    doHttp("POST", "http://127.0.0.1:8888/notify", 
        strSprintf(`{"message": "even", "value":%f}`, value(0)),
        "Content-Type: application/json",
        "X-Custom-Header: notification"
    )
)
CSV()
```

### do()

**문법**: `do(args..., { sub-flow-code })` (since v8.0.7)

`do`는 `args...` 인자를 전달하며 주어진 하위 흐름 코드를 실행합니다.

`WHEN()`은 특정 조건에서 부수 작업을 실행하기 위한 것일 뿐이라는 점을 기억해야 합니다.
`WHEN-do` 하위 흐름은 메인 흐름에 영향을 줄 수 없습니다. 즉 `CSV`, `JSON`, `CHART_*`처럼 출력 스트림에 결과를 내는 SINK를 사용할 수 없습니다. 하위 흐름의 출력은 조용히 무시되며, SINK의 쓰기 시도는 무시되고 경고 메시지가 표시됩니다.

하위 흐름에서 유효한 SINK는 출력 스트림과 무관한 `INSERT`와 `APPEND`이며, 메인 TQL 흐름과 다른 테이블에 값을 쓸 수 있습니다. 그 외에는 `DISCARD()` SINK를 사용하세요. 경고 메시지 없이 하위 흐름의 레코드를 조용히 버립니다.

```js
FAKE( json({
    [ 1, "hello" ],
    [ 2, "你好" ],
    [ 3, "world" ],
    [ 4, "世界" ]
}))
WHEN(
    value(0) % 2 == 0,
    do( "Greetings:", value(0), value(1), {
        ARGS()
        WHEN( true, doLog( value(0), value(2), "idx:", value(1) ) )
        DISCARD()
    })
)
CSV()
```

위 코드의 로그 메시지는 두 가지 중요한 점을 보여줍니다.

1. 메인 흐름은 하위 흐름이 작업을 마칠 때까지 블록되어 기다립니다.
2. 하위 흐름은 조건에 맞는 레코드마다 매번 실행됩니다.

```sh
2023-12-02 07:54:42.160 TRACE 0xc000bfa580 Task compiled FAKE() → WHEN() → CSV()
2023-12-02 07:54:42.160 TRACE 0xc000bfa840 Task compiled ARGS() → WHEN() → DISCARD()
2023-12-02 07:54:42.160 INFO  0xc000bfa840 Greetings: 你好 idx: 2
2023-12-02 07:54:42.160 DEBUG 0xc000bfa840 Task elapsed 254.583µs
2023-12-02 07:54:42.161 TRACE 0xc000bfa9a0 Task compiled ARGS() → WHEN() → DISCARD()
2023-12-02 07:54:42.161 INFO  0xc000bfa9a0 Greetings: 世界 idx: 4
2023-12-02 07:54:42.161 DEBUG 0xc000bfa9a0 Task elapsed 190.552µs
2023-12-02 07:54:42.161 DEBUG 0xc000bfa580 Task elapsed 1.102681ms
```

**활용 사례**

하위 흐름이 인자 이외의 데이터를 가져올 때는 `args([idx])` 옵션 함수로 인자에 접근할 수 있습니다.

- 하위 흐름의 인자로 쿼리를 실행합니다.

```js
// pseudo code
// ...
WHEN( condition,
    do(value(0), {
        SQL(`select time, value from table where name = ?`, args(0))
        // ... some map functions...
        INSERT(...)
    })
)
// ...
```

- 외부 웹 서버에서 csv 파일을 가져옵니다

```js
// pseudo code
// ...
WHEN( condition,
    do(value(0), value(1), {
        CSV( file( strSprintf("https://exmaple.com/data_%s.csv?id=%s", args(0), escapeParam(args(1)) )))
        WHEN(true, doHttp("POST", "http://my_server", value()))
        DISCARD()
    })
)
// ...
```

## FLATTEN()

**문법**: `FLATTEN()`

*GROUPBYKEY()*와 반대로 동작합니다. 값이 다차원 튜플인 레코드를 받아, 튜플의 각 요소마다 레코드를 만들어 차원을 낮춥니다.

예를 들어 원래 레코드가 `{key:k, value:[[v1,v2],[v3,v4],...,[vx,vy]]}` 이면, `{key:k, value:[v1, v2]}`, `{key:k, value:{v3, v4}}`...`{key:k, value:{vx, vy}}` 처럼 여러 레코드를 만듭니다.

## MAPKEY()

**문법**: `MAPKEY( newkey )`

현재 키 값을 주어진 newkey로 바꿉니다.

```js
FAKE( json({
    [ "TAG0", 1628694000000000000, 10],
    [ "TAG0", 1628780400000000000, 11],
    [ "TAG0", 1628866800000000000, 12],
    [ "TAG0", 1628953200000000000, 13],
    [ "TAG0", 1629039600000000000, 14],
    [ "TAG0", 1629126000000000000, 15]
}))
MAPKEY(time("now"))
PUSHKEY("do-not-see")
CSV()
```

```csv
1701343504143299000,TAG0,1628694000000000000,10
1701343504143303000,TAG0,1628780400000000000,11
1701343504143308000,TAG0,1628866800000000000,12
1701343504143365000,TAG0,1628953200000000000,13
1701343504143379000,TAG0,1629039600000000000,14
1701343504143383000,TAG0,1629126000000000000,15
```

## PUSHKEY()

**문법**: `PUSHKEY( newkey )`

각 레코드에 새 키를 적용합니다. 원래 키는 값 튜플로 밀려 들어갑니다.

예를 들어 원래 레코드가 `{key: 'k1', value: [v1, v2]}` 이고 `PUSHKEY(newkey)`를 적용하면 `{key: newkey, values: [k1, v1, v1]}` 로 바뀝니다.

```js
FAKE( json({
    [ "TAG0", 1628694000000000000, 10],
    [ "TAG0", 1628780400000000000, 11],
    [ "TAG0", 1628866800000000000, 12],
    [ "TAG0", 1628953200000000000, 13],
    [ "TAG0", 1629039600000000000, 14],
    [ "TAG0", 1629126000000000000, 15]
}))
MAPKEY(time("now"))
PUSHKEY("do-not-see")
CSV()
```

```csv
1701343504143299000,TAG0,1628694000000000000,10
1701343504143303000,TAG0,1628780400000000000,11
1701343504143308000,TAG0,1628866800000000000,12
1701343504143365000,TAG0,1628953200000000000,13
1701343504143379000,TAG0,1629039600000000000,14
1701343504143383000,TAG0,1629126000000000000,15
```

## POPKEY()

**문법**: `POPKEY( [idx] )`

레코드의 현재 키를 버리고 *tuple*의 *idx*번째 요소를 새 키로 올립니다.

예를 들어 원래 레코드가 `{key: k, value: [v1, v2, v3]}` 이고 `POPKEY(1)`을 적용하면 `{key: v2, value:[v1, v3]}` 로 바뀝니다.

인자 없이 `POPKEY()`를 쓰면 `POPKEY(0)`과 같으며, 값 튜플의 첫 요소를 키로 올립니다.

**예제: POPKEY()**

```js
FAKE( json({
    [ "TAG0", 1628694000000000000, 10],
    [ "TAG0", 1628780400000000000, 11],
    [ "TAG0", 1628866800000000000, 12],
    [ "TAG0", 1628953200000000000, 13],
    [ "TAG0", 1629039600000000000, 14],
    [ "TAG0", 1629126000000000000, 15]
}))
POPKEY()
CSV()
```

```csv
1628694000000000000,10
1628780400000000000,11
1628866800000000000,12
1628953200000000000,13
1629039600000000000,14
1629126000000000000,15
```

**예제: POPKEY(idx)**

```js
FAKE( json({
    [ "TAG0", 1628694000000000000, 10],
    [ "TAG0", 1628780400000000000, 11],
    [ "TAG0", 1628866800000000000, 12],
    [ "TAG0", 1628953200000000000, 13],
    [ "TAG0", 1629039600000000000, 14],
    [ "TAG0", 1629126000000000000, 15]
}))
POPKEY(1)
CSV()
```

```csv
TAG0,10
TAG0,11
TAG0,12
TAG0,13
TAG0,14
TAG0,15
```

## GROUPBYKEY()

**문법**: `GROUPBYKEY( [lazy(boolean)] )`

- `lazy(boolean)` 기본값인 `false`이면 들어오는 레코드의 키가 이전 레코드와 달라질 때마다 *GROUPBYKEY()* 가 새 그룹 레코드를 내보냅니다. `true`이면 *GROUPBYKEY()* 는 입력 스트림이 끝날 때까지 기다렸다가 레코드를 내보냅니다. 

`GROUPBYKEY`는 `GROUP( by( key() ) )`와 같은 표현입니다.

## THROTTLE()

**문법**: `THROTTLE(tps)` (since v8.0.8)

- `tps` *숫자* 초당 레코드 수로 지정합니다.

`THROTTLE`은 지정한 *tps*에 맞추어 지연을 두고 레코드를 다음 단계로 전달합니다.
저장된 데이터(예: CSV 파일)로부터 일정 주기를 갖는 데이터 흐름을 만들어, 
주기적으로 측정값을 보내는 센서 장치를 *시뮬레이션*합니다.

```js
FAKE(linspace(1,5,5))
THROTTLE(5.0)
WHEN(true, doLog("===>tick", value(0)))
CSV()
```

- 콘솔 로그에서 "tick" 메시지의 각 로그 시각은 *200ms* 차이가 납니다(초당 5회).

```
2023-12-07 09:33:30.131 TRACE 0x14000f88b00 Task compiled FAKE() → THROTTLE() → WHEN() → CSV()
2023-12-07 09:33:30.332 INFO  0x14000f88b00 ===>tick 1
2023-12-07 09:33:30.533 INFO  0x14000f88b00 ===>tick 2
2023-12-07 09:33:30.734 INFO  0x14000f88b00 ===>tick 3
2023-12-07 09:33:30.935 INFO  0x14000f88b00 ===>tick 4
2023-12-07 09:33:31.136 INFO  0x14000f88b00 ===>tick 5
2023-12-07 09:33:31.136 DEBUG 0x14000f88b00
Task elapsed 1.005070167s
```

## SCRIPT()

사용자 정의 스크립트 언어를 지원합니다.

자세한 내용과 예제는 SCRIPT 항목을 참고하세요.
