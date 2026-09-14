# Machbase Neo TQL GROUP Aggregation

*버전 8.0.7 이상*

## Syntax

```
GROUP( [lazy(boolean)] [, by()] [, aggregator...] )
```

**Parameters:**
- `lazy(boolean)` - lazy 모드 설정 (기본값: false)
- `by(value [, timewindow()] [, name])` - 주어진 값으로 그룹을 만드는 방식을 지정합니다. `by()`는 `GROUP()`에서 필수였으나, 전체 데이터에 한 번에 집계를 적용할 수 있도록 선택으로 바뀌었습니다(버전 8.0.14 이상).
- `aggregator` - 집계 함수 목록. 쉼표로 구분해 여러 개를 지정할 수 있습니다.

**Example:**

```js
FAKE(json({
    ["A", 1],
    ["A", 2],
    ["B", 3],
    ["B", 4]
}))
GROUP(
    by( value(0), "CATEGORY" ),
    avg( value(1), "AVG" ),
    sum( value(1), "SUM"),
    first( value(1) * 10, "x10")
)
CSV( header(true) )
```

## Options

### by()

`by()`는 첫 번째 인자로 값을 받고, 선택적으로 `timewindow()`와 `name`을 받습니다.

**문법**: `by( value [, timewindow] [, label] )`

**Parameters:**
- `value` - 그룹화 기준 값. 보통 시간입니다.
- `timewindow(from, until, period)` - 시간 창 옵션.
- `label` - 문자열, 새 컬럼 라벨 지정 (기본값 "GROUP")

### lazy()

**문법**: `lazy(boolean)`

기본값인 `false`이면 `GROUP()`은 현재 레코드의 `by()` 값을 이전 레코드의 값과 비교합니다. 값이 바뀌면 새 레코드를 만듭니다. 따라서 연속된 레코드가 같은 `by()` 값을 가질 때만 그룹이 만들어집니다.

`lazy(true)`를 설정하면 `GROUP()`은 모든 레코드를 모으기 위해 입력 스트림이 끝날 때까지 기다린 뒤 레코드를 내보냅니다. 정렬되지 않은 `by()` 값도 그룹화할 수 있지만 메모리 소비가 큽니다.

### timewindow()

**문법**: `timewindow( from, until, period )`

*버전 8.0.13 이상*

**Parameters:**
- `from`, `until` - 시간 범위. `from`은 포함, `until`은 제외입니다. 실제 데이터 존재 여부와 무관하게 원하는 시간 범위를 지정할 수 있습니다.
- `period` - 기간. `from`과 `until` 사이의 시간 간격을 나타냅니다.

timewindow 예제를 참고하세요

데이터베이스에 저장된 데이터를 분석·시각화하는 일은, 특히 원하는 시간 범위에 데이터가 없거나 데이터 포인트가 여러 개일 때 번거로울 수 있습니다.

예를 들어 고정 간격의 시간-값 차트를 그릴 때, SELECT 문으로 데이터를 조회해 그대로 차트 라이브러리에 넣으면 레코드 간 시간 간격이 차트의 시간축과 맞지 않을 수 있습니다. 중간 데이터가 없거나 특정 구간에 데이터가 몰려 있을 때 이런 어긋남이 생기며, 원하는 형태로 데이터를 맞추기 어려워집니다.

보통 애플리케이션 개발자는 고정 시간 간격의 배열을 만들고 조회 결과 레코드를 순회하며 배열의 칸(슬롯)을 채웁니다. 슬롯에 이미 값이 있으면 특정 연산(min, max, first, last 등)으로 하나의 값으로 유지합니다. 마지막에는 값이 없는 슬롯을 임의의 값(0이나 NULL 등)으로 채웁니다.

## 집계 함수

집계 함수를 지정하지 않으면 `GROUP`은 기본적으로 각 그룹의 원시 레코드로 새 배열을 만듭니다.

`by()` 값이 같은 연속 레코드들을 모아, 개별 값 전체를 담은 값 배열을 갖는 새 레코드를 만듭니다. 예를 들어 원래 레코드가 `{key:k, value:[v1, v2]}`, `{key:k, value:{v3, v4}}`...`{key:k, value:{vx, vy}}` 였다면, `GROUP( by(key()) )`는 `{key:k, value:[[v1,v2],[v3,v4],...,[vx,vy]]}` 형태의 새 레코드를 만듭니다.

**문법**: `function_name( value [, value...] [, where()] [, nullValue()] [, predict()] [, label])`

**Parameters:**
- `value` - 함수에 따라 하나 이상의 값.
- `where( predicate )` - 판정에 사용할 불리언 표현식을 받습니다.
- `nullValue(alternative)` - 집계 결과가 없을 때 `NULL` 대신 사용할 대체 값을 지정합니다.
- `predict(algorithm)` - 집계 결과가 없을 때 `NULL` 대신 사용할 값을 예측하는 알고리즘을 지정합니다.
- `label` - 문자열, 컬럼의 라벨 지정 (기본값은 집계 함수 이름).

집계 함수는 두 종류가 있습니다:
- **Type 1** 함수는 결과를 위한 최종 후보 값만 유지합니다.
- **Type 2** 함수는 그룹의 전체 데이터를 보관했다가 집계 결과를 만든 뒤 다음 그룹을 위해 메모리를 해제합니다.

`GROUP()`이 `lazy(true)`와 Type 2 함수를 함께 쓰면 관련 컬럼의 전체 입력 데이터를 보관하게 됩니다.

### 집계 함수 옵션

`where()`, `nullValue()`, `predict()`, `label` 인자는 선택이며, 아래 각 함수 문법 설명의 `option`에 해당합니다.

#### where()

**문법**: `where(predicate)`

*버전 8.0.13 이상*

where 예제를 참고하세요

#### nullValue()

**문법**: `nullValue(alternative)`

*버전 8.0.13 이상*

nullValue 예제를 참고하세요

#### predict()

**문법**: `predict(algorithm)`

*버전 8.0.13 이상*

predict 예제를 참고하세요

**사용 가능한 알고리즘:**

| 알고리즘 | 설명 |
| :--- | :--- |
| `PiecewiseConstant` | 좌연속 구간별 상수 1차원 보간기. |
| `PiecewiseLinear` | 구간별 선형 1차원 보간기 |
| `AkimaSpline` | 값과 1차 도함수가 연속인 구간별 3차 1차원 보간. 참고: https://www.iue.tuwien.ac.at/phd/rottinger/node60.html |
| `FritschButland` | 값과 1차 도함수가 연속인 구간별 3차 1차원 보간. 참고: Fritsch, F. N. and Butland, J., "A method for constructing local monotone piecewise cubic interpolants" (1984), SIAM J. Sci. Statist. Comput., 5(2), pp. 300-304. |
| `LinearRegression` | 인접 값을 이용한 선형 회귀 |

## 집계 함수 목록

### avg()

**Type 1**

**문법**: `avg(x [, option...])`

그룹 내 값들의 평균입니다.

### sum()

**Type 1**

**문법**: `sum(x [, option...])`

그룹 내 값들의 총합입니다.

### count()

**Type 1**

**문법**: `count(x [, option...])`

*버전 8.0.13 이상*

그룹 내 값들의 개수입니다.

### first()

**Type 1**

**문법**: `first(x [, option...])`

그룹의 첫 번째 값입니다.

### last()

**Type 1**

**문법**: `last(x [, option...])`

그룹의 마지막 값입니다.

### min()

**Type 1**

**문법**: `min(x [, option...])`

그룹의 최솟값입니다.

### max()

**Type 1**

**문법**: `max(x [, option...])`

그룹의 최댓값입니다.

### rss()

**Type 1**

**문법**: `rss(x [, option...])`

제곱합의 제곱근(Root sum square)

### rms()

**Type 1**

**문법**: `rms(x [, option...])`

제곱평균제곱근(Root mean square)

### list()

**Type 2**

**문법**: `list(x [, option...])`

*버전 8.0.15 이상*

**Parameters:**
- `x` - Float value

`list()`는 모든 x 값을 모아 개별 값들을 담은 하나의 리스트를 만듭니다.

#### 예제 1: JSON 출력

```js
FAKE(json({["A",1], ["A",2], ["B",3], ["B",4], ["C",5]}))
GROUP(
    by(value(0)),
    list(value(1))
)
JSON()
```

**Output:**

```json
{
    "data":{
        "columns":["GROUP","LIST"],
        "types":["string","float64"],
        "rows":[
            ["A",[1,2]],
            ["B",[3,4]],
            ["C",[5]]
        ]
    },
    "success":true,
    "reason":"success",
    "elapse":"220.375µs"
}
```

#### 예제 2: JSON(rowsArray) 출력

```js
FAKE(json({["A",1], ["A",2], ["B",3], ["B",4], ["C",5]}))
GROUP(
    by(value(0),"name"),
    avg(value(1), "avg"),
    list(value(1), "values")
)
JSON(rowsArray(true))
```

**Output:**

```json
{
    "data": {
        "columns": ["name", "values", "avg"],
        "types": [ "string", "list", "float64" ],
        "rows": [
            {  "name": "A", "avg": 1.5, "values": [ 1, 2 ] },
            {  "name": "B", "avg": 3.5, "values": [ 3, 4 ] },
            {  "name": "C", "avg": 5,  "values": [ 5 ] }
        ]
    },
    "success": true,
    "reason": "success",
    "elapse": "270.25µs"
}
```

#### 예제 3: FLATTEN 출력

```js
FAKE(json({["A",1], ["A",2], ["B",3], ["B",4], ["C",5]}))
GROUP(
    by(value(0)),
    list(value(1))
)
POPVALUE(0)
FLATTEN()
JSON()
```

**Output:**

```json
{
    "data": {
        "columns": ["LIST"],
        "types": ["list"],
        "rows": [
            [1,2],
            [3,4],
            [5]
        ]
    },
    "success": true,
    "reason": "success",
    "elapse": "252.625µs"
}
```

### lrs()

**Type 2**

**문법**: `lrs(x, y [, weight(w)] [, option...])`

*버전 8.0.13 이상*

**Parameters:**
- `x` - 실수 또는 시간
- `y` - Float value
- `weight(w)` - 생략하면 모든 가중치가 1입니다.

x-y를 직교 좌표계상의 점으로 보고 계산한 선형 회귀 기울기입니다. x는 숫자 또는 시간 타입일 수 있습니다.

### mean()

**Type 2**

**문법**: `mean(x [, weight(w)] [, option...])`

**Parameters:**
- `x` - Float value
- `weight(w)` - 생략하면 모든 가중치가 1입니다.

`mean()`은 그룹 값들의 가중 평균을 계산합니다. 모든 가중치가 1이면 성능을 위해 가벼운 `avg()`를 사용하세요.

**수식**: mean(x, weight(w)) = (Σ w<sub>i</sub> x<sub>i</sub>) / (Σ w<sub>i</sub>)

### cdf()

**Type 2**

**문법**: `cdf(x, q [, weight(w)] [, option...])`

*버전 8.0.14 이상*

**Parameters:**
- `x` - Float
- `q` - Float
- `weight(w)` - 생략하면 모든 가중치가 1입니다.

`cdf()`는 x의 경험적 누적분포함수 값, 즉 q 이하인 표본의 비율을 반환합니다. 이론적으로 `quantile()` 함수의 역함수이지만 모든 q에 대해 정확한 역함수는 아닐 수 있습니다.

### correlation()

**Type 2**

**문법**: `correlation(x, y [, weight(w)] [, option...])`

*버전 8.0.14 이상*

**Parameters:**
- `x`, `y` - Float value
- `weight(w)` - 생략하면 모든 가중치가 1입니다.

`correlation()`은 x와 y 표본 간의 가중 상관계수를 반환합니다.

**수식**: correlation(x, y, weight(w)) = (Σ w<sub>i</sub> (x<sub>i</sub> - x̄) (y<sub>i</sub> - ȳ)) / (stdX * stdY) (x̄는 x의 평균, ȳ는 y의 평균)

### covariance()

**Type 2**

**문법**: `covariance(x, y [, weight(w)] [, option...])`

*버전 8.0.14 이상*

**Parameters:**
- `x`, `y` - Float value
- `weight(w)` - 생략하면 모든 가중치가 1입니다.

`covariance()`는 x와 y 표본 간의 가중 공분산을 반환합니다.

**수식**: covariance(x, y, weight(w)) = (Σ w<sub>i</sub> (x<sub>i</sub> - x̄) (y<sub>i</sub> - ȳ)) / (Σ w<sub>i</sub> - 1) (x̄는 x의 평균, ȳ는 y의 평균)

### quantile()

**Type 2**

**문법**: `quantile(x, p [, weight(w)] [, option...])`

*버전 8.0.13 이상*

**Parameters:**
- `x` - Float value
- `p` - 실수 비율
- `weight(w)` - 생략하면 모든 가중치가 1입니다.

`quantile()`은 표본의 비율 p 이상이 되는 x 표본을 반환합니다. p는 0과 1 사이의 수여야 합니다.

표본의 비율 p 이상이 되는 가장 작은 값 q를 반환합니다.

### quantileInterpolated()

**Type 2**

**문법**: `quantileInterpolated(x, p [, weight(w)] [, option...])`

*버전 8.0.13 이상*

**Parameters:**
- `x` - Float value
- `p` - 실수 비율
- `weight(w)` - 생략하면 모든 가중치가 1입니다.

`quantileInterpolated()`는 표본의 비율 p 이상이 되는 x 표본을 반환합니다. p는 0과 1 사이의 수여야 합니다.

반환값은 선형 보간된 값입니다.

### median()

**Type 2**

**문법**: `median(x [, weight(w)] [, option...])`

**Parameters:**
- `x` - Float value
- `weight(w)` - 생략하면 모든 가중치가 1입니다.

`quantile(x, 0.5 [, option...])` 와 같습니다 

### medianInterpolated()

**Type 2**

**문법**: `medianInterpolated(x [, weight(w)] [, option...])`

**Parameters:**
- `x` - Float value
- `weight(w)` - 생략하면 모든 가중치가 1입니다.

`quantileInterpolated(x, 0.5 [, option...])` 와 같습니다

### stddev()

**Type 2**

**문법**: `stddev(x [, weight(w)] [, option...])`

**Parameters:**
- `weight(w)` - 생략하면 모든 가중치가 1입니다.

`stddev()`는 표본 표준편차를 반환합니다.

### stderr()

**Type 2**

**문법**: `stderr(x [, weight(w)] [, option...])`

**Parameters:**
- `weight(w)` - 생략하면 모든 가중치가 1입니다.

`stderr()`는 주어진 값들의 표준편차로 계산한 평균의 표준오차를 반환합니다.

### entropy()

**Type 2**

**문법**: `entropy(x [, option...])`

분포의 섀넌 엔트로피입니다. 자연로그를 사용합니다.

### mode()

**Type 2**

**문법**: `mode(x [, weight(w)] [, option...])`

**Parameters:**
- `weight(w)` - 생략하면 모든 가중치가 1입니다.

`mode()`는 값과 가중치로 지정된 데이터셋에서 가장 자주 나타나는 값을 반환합니다. 값 비교에 엄격한 float64 동등성을 사용하므로 주의가 필요합니다. 최빈값이 여러 개면 그중 아무거나 반환될 수 있습니다.

### moment()

**Type 2**

**문법**: `moment(x, n [, weight(w)] [, option...])`

*버전 8.0.14 이상*

**Parameters:**
- `x` - Float64 value
- `n` - Float64 적률(moment)
- `weight(w)` - 생략하면 모든 가중치가 1입니다.

`moment()`는 표본의 가중 n차 적률을 계산합니다.

### variance()

**Type 2**

**문법**: `variance(x [, weight(w)] [, option...])`

*버전 8.0.14 이상*

**Parameters:**
- `x` - Float value
- `weight(w)` - 생략하면 모든 가중치가 1입니다.

`variance()`는 그룹 값들의 불편 가중 분산을 계산합니다. 가중치 합이 1 이하이면 편향 분산 추정량을 사용해야 합니다.

**Example:**

```js
FAKE(json({[8,2], [2,2], [-9,6], [15,7], [4,1]}))
GROUP(
    variance(value(0), "VARIANCE"),
    variance(value(0), weight(value(1)), "WEIGHTED VARIANCE")
)
CSV(heading(true), precision(4))
```

## Examples

### timewindow() 예제

`FAKE()`는 1ms마다 시간-값을 생성하므로 1초에 1,000개의 레코드가 만들어집니다. 아래 TQL을 실행하면 1초 간격(`timewindow()`의 `period("1s")`)으로 데이터가 생성되며, 원하는 구간에 실제 데이터(레코드)가 없으면 기본값 NULL로 채워집니다.

```js
FAKE(
    oscillator(
        freq(10, 1.0), freq(35, 2.0), 
        range('now', '10s', '10ms')) 
)
GROUP(
    by( value(0),
        timewindow(time('now - 2s'), time('now + 13s'), period("1s")),
        "TIME"
    ),
    last( value(1),
          "LAST"
    )
)
CSV(sqlTimeformat('YYYY-MM-DD HH24:MI:SS'), heading(true))
```

### nullValue() 예제

nullValue(100)을 추가하고 다시 실행해 봅시다. NULL 값이 주어진 값 100으로 대체됩니다.

```js
FAKE(
    oscillator(
        freq(10, 1.0), freq(35, 2.0), 
        range('now', '10s', '10ms')) 
)
GROUP(
    by( value(0),
        timewindow(time('now - 2s'), time('now + 13s'), period("1s")),
        "TIME"
    ),
    last( value(1),
          nullValue(100),
          "LAST"
    )
)
CSV(sqlTimeformat('YYYY-MM-DD HH24:MI:SS'), heading(true))
```

### predict() 예제

`nullValue()`로 지정한 상수로 빈 값(NULL)을 채우는 것을 넘어, 인접 값을 참조해 보간된 데이터를 얻을 수도 있습니다. 위 예제에서 `last()`에 `predict("LinearRegression")`을 추가하고 다시 실행해 보세요. 값이 없어 NULL이 반환되던 레코드에 선형 회귀로 예측한 값이 채워지는 것을 볼 수 있습니다.

주변에 예측할 값이 충분하지 않으면 `predict()`가 보간값을 만들지 못할 수 있으며, 이때는 `nullValue()`가 대신 적용됩니다. `nullValue()`가 주어지지 않으면 `NULL`이 반환됩니다.

```js
FAKE(
    oscillator(
        freq(10, 1.0), freq(35, 2.0), 
        range('now', '10s', '10ms')) 
)
GROUP(
    by( value(0),
        timewindow(time('now - 2s'), time('now + 13s'), period("1s")),
        "TIME"
    ),
    last( value(1),
          predict("LinearRegression"),
          nullValue(100),
          "LAST"
    )
)
CSV(sqlTimeformat('YYYY-MM-DD HH24:MI:SS'), heading(true))
```

### where() 예제

온도와 습도를 측정하는 센서가 두 개 있고, 각각 1초마다 데이터를 저장한다고 합시다.
실제 환경에서는 센서 시스템 간에 항상 시간 차이가 있습니다. 따라서 저장된 데이터는 아래 샘플과 같을 수 있습니다.

5번 레코드의 습도 데이터가 예상보다 일찍 저장됐고, 9번 레코드에서도 같은 일이 일어났습니다. 데이터를 초 단위로 정규화해 봅시다.

```js
FAKE( json({
    ["temperature", 1691800174010, 16],
    ["humidity",    1691800174020, 64],
    ["temperature", 1691800175001, 17],
    ["humidity",    1691800175010, 63],
    ["humidity",    1691800176999, 66],
    ["temperature", 1691800176020, 18],
    ["temperature", 1691800177125, 18],
    ["humidity",    1691800177293, 66],
    ["humidity",    1691800177998, 66],
    ["temperature", 1691800178184, 18]
}) )
MAPVALUE(1, parseTime(value(1), "ms"))

GROUP(
    by( roundTime(value(1), "1s")),
    avg( value(2) )
)

CSV( timeformat("Default"), header(true) )
```

`roundTime(..., "1s")`는 시간 값을 초 단위로 정렬해 같은 시간을 가진 레코드를 묶습니다. `avg(...)`는 그룹의 평균값을 만듭니다.

하지만 값이 온도인지 습도인지 나타내는 첫 컬럼 정보가 사라져 결과값이 무의미해집니다. 이 문제는 `where()`로 해결합니다. 집계 함수는 `where()`의 판정이 `true`일 때만 값을 받아들입니다.

```js
GROUP(
    by( roundTime(value(1), "1s"), "TIME"),
    avg( value(2),
         where( value(0) == 'temperature' ),
         "TEMP" ),
    avg( value(2),
         where( value(0) == 'humidity' ),
         "HUMI" )
)
```

`predict()`와 `nullValue()`로 마지막 레코드의 누락 데이터를 보간할 수도 있습니다

```js
GROUP(
    by( roundTime(value(1), "1s"), "TIME"),
    avg( value(2),
         where( value(0) == 'temperature' ),
         "TEMP" ),
    avg( value(2),
         where( value(0) == 'humidity' ),
         predict("PiecewiseLinear"),
         "HUMI" )
)
```

### 차트 예제

```js
CSV(file("https://docs.machbase.com/assets/example/iris.csv"))
FILTER( strToUpper(value(4)) == "IRIS-SETOSA")
GROUP( by(value(4)), 
    min(value(0), "Min"),
    median(value(0), "Median"),
    avg(value(0), "Avg"),
    max(value(0), "Max"),
    stddev(value(0), "StdDev.")
)
CHART(
    chartOption({
        "xAxis": { "type": "category", "data": ["iris-setosa"]},
        "yAxis": {},
        "legend": {"show": "true"},
        "series": [
            {"type":"bar", "name": "Min", "data": column(1)},
            {"type":"bar", "name": "Median", "data": column(2)},
            {"type":"bar", "name": "Avg", "data": column(3)},
            {"type":"bar", "name": "Max", "data": column(4)},
            {"type":"bar", "name": "StdDev.", "data": column(5)}
        ]
    })
)
```
