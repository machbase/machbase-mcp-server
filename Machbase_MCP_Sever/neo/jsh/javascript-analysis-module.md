# Machbase Neo JavaScript Analysis Module

## sort()

`sort` 함수는 배열의 요소를 오름차순으로 정렬합니다.
데이터를 정리하거나 추가 분석을 준비할 때 유용합니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
console.log(ana.sort([1.3, 1.2, 1.1])) // [1.1, 1.2, 1.3]
```

## sum()

`sum` 함수는 배열에 있는 모든 숫자의 총합을 계산합니다.
통계 및 수학 계산에서 흔히 사용됩니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
console.log(ana.sum([3, 1, 2]))       // 6
console.log(ana.sum([1.3, 1.2, 1.1])) // 3.6
```

## cdf()

`cdf` 함수는 주어진 데이터셋 `x`에 대한 누적분포함수(CDF)를 계산합니다 
즉 `q` 이하인 표본의 비율입니다.
확률 변수가 지정한 값 이하의 값을 가질 확률을 나타냅니다. 
이 함수는 데이터 분포를 이해하기 위해 통계 분석과 확률론에서 흔히 사용됩니다.

**문법**

```js
cdf(q, x, weights)
```

- `q` `Number`
- `x` `Number[]` `x` 데이터는 오름차순으로 정렬되어 있어야 합니다.
- `weights` `Number[]` 가중치를 지정하지 않으면 모든 가중치가 1입니다. 지정하면 `x`의 길이와 `weights`의 길이가 같아야 합니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
x = [];
for( i=1; i<=100; i++) {
    x.push(i);
}
x = ana.sort(x);
console.log(ana.cdf(1.0, x)); // 0.01
```

## mean()

`mean` 함수는 주어진 숫자 배열의 산술 평균을 계산합니다. 
배열의 모든 요소를 더한 뒤 요소 개수로 나누어 구합니다. 
이 함수는 데이터셋의 중심 경향을 파악하기 위해 통계 분석에서 흔히 사용됩니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
console.log(ana.mean([1, 2, 3, 4, 5]))  // 3
console.log(ana.mean([10, 20, 30]))     // 20
```

## circularMean()

`circularMean` 함수는 각도의 순환성을 고려해 라디안 단위 각도의 평균을 계산합니다. 
각도나 하루 중 시각처럼 값이 순환하는 데이터셋에 특히 유용합니다. 
선택적으로 가중치를 주면 가중 순환 평균을 계산합니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
x = [0, 0.25 * Math.PI, 0.75 * Math.PI];
w = [1, 2, 2.5];
console.log(ana.circularMean(x).toFixed(4))     // 0.9553
console.log(ana.circularMean(x, w).toFixed(4))  // 1.3704
```

## correlation()

`correlation` 함수는 두 데이터셋 간의 피어슨 상관계수를 계산합니다.
데이터셋 간의 선형 관계를 측정하며,
값은 -1(완전한 음의 상관)에서 1(완전한 양의 상관) 사이입니다.
선택적으로 가중치를 주면 가중 상관계수를 계산합니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
x = [8, -3, 7, 8, -4];
y = [10, 5, 6, 3, -1];
w = [2, 1.5, 3, 3, 2];
console.log(ana.correlation(x, y).toFixed(5))     // 0.61922
console.log(ana.correlation(x, y, w).toFixed(5))  // 0.59915
```

## covariance()

`covariance` 함수는 두 데이터셋 간의 공분산을 계산합니다.
공분산은 두 확률 변수가 함께 얼마나 변하는지를 나타내는 척도입니다.
양의 공분산은 두 변수가 함께 증가하는 경향을,
음의 공분산은 한 변수가 증가할 때 다른 변수가 감소하는 경향을 나타냅니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
x = [8, -3, 7, 8, -4];
y1 = [10, 2, 2, 4, 1];
y2 = [12, 1, 11, 12, 0];
console.log(ana.covariance(x, y1).toFixed(4)) // 13.8000
console.log(ana.covariance(x, y2).toFixed(4)) // 37.7000
console.log(ana.variance(x).toFixed(4))       // 37.7000
```

## entropy()

`entropy` 함수는 확률 분포의 섀넌 엔트로피를 계산합니다.
엔트로피는 분포의 불확실성 또는 무작위성을 나타내는 척도입니다.
정보 이론과 통계에서 흔히 사용됩니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
console.log(ana.entropy([0.05, 0.1, 0.9, 0.05]).toFixed(4)); // 0.6247
console.log(ana.entropy([0.2, 0.4, 0.25, 0.15]).toFixed(4)); // 1.3195
console.log(ana.entropy([0.2, 0, 0, 0.5, 0, 0.2, 0.1, 0, 0, 0]).toFixed(4)); // 1.2206
console.log(ana.entropy([0, 0, 1, 0]).toFixed(4));           // 0.0000
```

## geometricMean()

`geometricMean` 함수는 주어진 양수 배열의 기하 평균을 계산합니다. 
배열의 모든 요소를 곱한 뒤 요소 개수 n에 대한 n제곱근을 취해 구합니다. 
이 함수는 평균 수익률이나 성장률을 구하기 위해 금융·통계 분석에서 흔히 사용됩니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
console.log(ana.geometricMean([1, 3, 9]).toFixed(4))  // 3.0000
console.log(ana.geometricMean([2, 8, 32]).toFixed(4)) // 8.0000
```

## harmonicMean()

`harmonicMean` 함수는 주어진 양수 배열의 조화 평균을 계산합니다. 
각 요소의 역수의 산술 평균의 역수로 구합니다. 
이 함수는 속도나 밀도처럼 비율을 다루는 데이터셋에 특히 유용합니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
console.log(ana.harmonicMean([1, 2, 4]).toFixed(4))    // 1.7143
console.log(ana.harmonicMean([10, 20, 30]).toFixed(4)) // 16.3636
```

## median()

`median` 함수는 주어진 숫자 배열의 중앙값을 계산합니다. 
중앙값은 숫자를 오름차순으로 정렬했을 때 가운데 값입니다. 
요소 개수가 짝수이면 가운데 두 값의 평균이 중앙값입니다. 
이 함수는 데이터셋의 중심값을 파악하기 위해 통계 분석에서 흔히 사용됩니다.

입력 배열은 정렬되어 있어야 하며, 그렇지 않으면 예외가 발생합니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
console.log(ana.median(ana.sort([1, 3, 2, 5, 4])))      // 3
console.log(ana.median(ana.sort([10, 20, 30, 40, 50]))) // 30
```

## medianInterp()

`medianInterp` 함수는 선형 보간된 값을 반환한다는 점만 빼면 `median`과 같습니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
console.log(ana.medianInterp(ana.sort([1, 3, 2, 5, 4])))      // 2.5
console.log(ana.medianInterp(ana.sort([10, 20, 30, 40, 50]))) // 25
```

## quantile()

`quantile` 함수는 지정한 확률에 대한 데이터셋의 분위수를 계산합니다. 
분위수는 데이터셋을 사분위수(4구간)나 백분위수(100구간)처럼 같은 확률의 구간으로 나눕니다. 
이 함수는 데이터 분포를 이해하는 데 유용합니다.

**문법**

```js
quantile(p, x, weights)
```

- `p` `Number`
- `x` `Number[]` `x` 데이터는 오름차순으로 정렬되어 있어야 합니다.
- `weights` `Number[]` 가중치를 지정하지 않으면 모든 가중치가 1입니다. 지정하면 `x`의 길이와 `weights`의 길이가 같아야 합니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
data = ana.sort([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
console.log(ana.quantile(0.25, data)) // 3
console.log(ana.quantile(0.5, data))  // 5
console.log(ana.quantile(0.74, data)) // 8
```

## quantileInterp()

`quantileInterp` 함수는 선형 보간된 값을 반환한다는 점만 빼면 `quantile`과 같습니다.

**문법**

```js
quantileInterp(p, x, weights)
```

- `p` `Number`
- `x` `Number[]` `x` 데이터는 오름차순으로 정렬되어 있어야 합니다.
- `weights` `Number[]` 가중치를 지정하지 않으면 모든 가중치가 1입니다. 지정하면 `x`의 길이와 `weights`의 길이가 같아야 합니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
data = ana.sort([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
console.log(ana.quantileInterp(0.25, data)) // 2.5
console.log(ana.quantileInterp(0.5, data))  // 5
console.log(ana.quantileInterp(0.74, data)) // 7.4
```

## meanStdDev()

`meanStdDev` 함수는 주어진 숫자 배열의 평균과 표준편차를 함께 계산합니다. 
평균은 중심 경향을, 표준편차는 데이터의 퍼짐 정도를 나타냅니다. 
이 함수는 통계 분석에서 데이터셋을 요약할 때 유용합니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
data = [1, 2, 3, 4, 5]
result = ana.meanStdDev(data)
console.log(result.mean.toFixed(2))   // 3.00
console.log(result.stdDev.toFixed(2)) // 1.58
```

## mode()

`mode` 함수는 주어진 숫자 배열의 최빈값을 계산합니다. 
최빈값은 데이터셋에서 가장 자주 나타나는 값입니다. 
최빈값이 여러 개면 함수가 전부 반환하거나 구현에 따라 처리합니다.

It returns `{value: number, count: number}`.

**문법**

```js
mode(x, weights)
```

- `x` `Number[]` `x` 데이터는 오름차순으로 정렬되어 있어야 합니다.
- `weights` `Number[]` 가중치를 지정하지 않으면 모든 가중치가 1입니다. 지정하면 `x`의 길이와 `weights`의 길이가 같아야 합니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
data = ana.sort([1, 2, 2, 3, 4])
console.log(ana.mode(data)) // {value:2, count:2}
data = ana.sort([1, 1, 2, 3, 4])
console.log(ana.mode(data)) // {value:1, count:2}
```

## moment()

`moment` 함수는 지정한 지점을 기준으로 데이터셋의 n차 적률을 계산합니다. 
적률은 왜도(3차 적률)나 첨도(4차 적률)처럼 분포의 형태를 설명하는 데 사용됩니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
data = [1, 2, 3, 4, 5]
console.log(ana.moment(2, data).toFixed(4)) // 2.5000
console.log(ana.moment(4, data).toFixed(4)) // 6.8000
```

## stdDev()

`stdDev` 함수는 주어진 숫자 배열의 표준편차를 계산합니다. 
표준편차는 데이터셋의 변동 또는 분산 정도를 측정합니다. 
표준편차가 낮으면 데이터가 평균에 가깝고, 높으면 더 넓게 퍼져 있음을 의미합니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
console.log(ana.stdDev([1, 2, 3, 4, 5]).toFixed(4))      // 1.5811
console.log(ana.stdDev([10, 20, 30, 40, 50]).toFixed(4)) // 15.8114
```

## stdErr()

`stdErr` 함수는 주어진 숫자 배열에 대한 평균의 표준오차를 계산합니다. 
표준오차는 표본 평균이 모집단 평균을 얼마나 정확히 대표하는지를 측정합니다. 
표준편차를 표본 크기의 제곱근으로 나누어 구합니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
let stddev = ana.stdDev([1, 2, 3, 4, 5])
let sampleSize = 5
console.log(ana.stdErr(stddev, sampleSize).toFixed(4)) // 0.7071
```

## linearRegression()

`linearRegression` 함수는 두 데이터셋에 선형 회귀 분석을 수행합니다. 
관측값과 예측값의 잔차 제곱합을 최소화하는 최적합 직선을 계산합니다. 
이 함수는 예측 모델링과 추세 분석에서 흔히 사용됩니다.

`y = alpha*x + beta` 에서 `{slope: alpha, intercept: beta}` 를 반환합니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
result = ana.linearRegression(x, y)
console.log(result.slope.toFixed(4))     // 2.0000
console.log(result.intercept.toFixed(4)) // 0.0000
```

## fft()

`fft` 함수는 주어진 데이터셋에 고속 푸리에 변환(FFT)을 수행합니다. 
FFT는 신호의 주파수 성분을 분석하는 데 사용되어 신호 처리와 데이터 분석에 유용합니다.

```js
fft(times, amplitudes)
```

times와 amplitudes의 길이는 같아야 합니다.

## PiecewiseConstant

`PiecewiseConstant`는 데이터셋에 구간별 상수 보간을 수행합니다. 
각 구간에서 가장 가까운 데이터 점을 사용해 함숫값을 근사합니다. 
계단 형태의 데이터에 유용한 방법입니다.

**사용 예제**

```js
x = [1, 2, 3, 4]
y = [10, 20, 30, 40]
interp = new ana.PiecewiseConstant();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 30
```

## PiecewiseLinear

`PiecewiseLinear`는 데이터셋에 구간별 선형 보간을 수행합니다. 
데이터 점들을 직선으로 이어 함숫값을 근사합니다. 
데이터 점 사이를 부드럽게 잇는 데 유용한 방법입니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
x = [1, 2, 3, 4]
y = [10, 20, 30, 40]
interp = new ana.PiecewiseLinear();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## AkimaSpline

`AkimaSpline`은 데이터셋에 Akima 스플라인 보간을 수행합니다. 
데이터 점들을 지나는 부드러운 곡선을 만들며, 데이터가 드문 구간에서 진동을 피합니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
x = [1, 2, 3, 4]
y = [10, 20, 30, 40]
interp = new ana.AkimaSpline();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## FritschButland

`FritschButland`는 데이터셋에 Fritsch-Butland 보간을 수행합니다. 
보간 값의 단조성을 보장하므로 순서 보존이 중요한 데이터셋에 적합합니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
x = [1, 2, 3, 4]
y = [10, 20, 30, 40]
interp = new ana.FritschButland();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## LinearRegression

`LinearRegression`은 데이터셋에 선형 회귀 기반 보간을 수행합니다. 
데이터에서 도출한 최적합 직선을 사용해 주어진 지점의 함숫값을 예측합니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
x = [1, 2, 3, 4]
y = [10, 20, 30, 40]
interp = new ana.LinearRegression();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## ClampedCubic

`ClampedCubic`은 데이터셋에 clamped-cubic 보간을 수행합니다. 
데이터에서 도출한 최적합 직선을 사용해 주어진 지점의 함숫값을 예측합니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
x = [1, 2, 3, 4]
y = [10, 20, 30, 40]
interp = new ana.ClampedCubic();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## NaturalCubic

`NaturalCubic`은 데이터셋에 natural-cubic 보간을 수행합니다. 
데이터에서 도출한 최적합 직선을 사용해 주어진 지점의 함숫값을 예측합니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
x = [1, 2, 3, 4]
y = [10, 20, 30, 40]
interp = new ana.NaturalCubic();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```

## NotAKnotCubic

`NotAKnotCubic`은 데이터셋에 not-a-knot 3차 스플라인 보간을 수행합니다. 
데이터에서 도출한 최적합 직선을 사용해 주어진 지점의 함숫값을 예측합니다.

**사용 예제**

```js
const ana = require("@jsh/analysis")
x = [1, 2, 3, 4]
y = [10, 20, 30, 40]
interp = new ana.NotAKnotCubic();
interp.fit(x,y);
console.log(interp.predict(2.5)); // 25
```
