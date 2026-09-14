# Machbase Neo JavaScript mathx Module

`mathx` 모듈은 TQL의 `SCRIPT()`와 `*.js` JSH 애플리케이션에서 쓸 수 있는 데이터 생성기, 샘플 배열 도우미, FFT, 통계 함수를 제공합니다.

```js
const m = require("mathx");
```

> **참고**: `series()`, `unzip()`, `zip()`, 그리고 `oscillator()`의 `noise` 옵션은 Machbase Neo v8.5.5에서 추가되었습니다.

## Generators

### oscillator()

합성 오실레이터 샘플을 `[time, value]` 튜플로 생성합니다.

```js
oscillator(options)
```

- `options.components` `Array<Object>` (필수) — 파형 성분들. 각각 `{ amplitude, frequencyHz, phaseRad?, bias? }` 형태입니다.
- `options.timeRange` `Object` (required) — `{ from, to }` (e.g. `{ from: "0s", to: "10s" }`).
- `options.sample` `Number | String` 선택 — 샘플 개수, 또는 `Hz` 접미가 붙은 샘플링 레이트 문자열.
- `options.noise` `Number | Object` 선택 — 각 샘플에 더할 노이즈.
  - `Number`: 노이즈 진폭으로 해석됩니다.
  - `Object`: `{ amplitude, seed? }` 이며 `amplitude`는 노이즈 세기, `seed`는 노이즈를 재현 가능하게 합니다.

```js
const m = require("mathx");
const gen = m.oscillator({
    components: [{ amplitude: 1.0, frequencyHz: 0.1 }],
    timeRange: { from: "0s", to: "10s" },
    sample: 5,
    noise: { amplitude: 0.1, seed: 123 },
});
// gen is Array<[time, value]>
```

### arrange(), linspace(), meshgrid()

- `arrange(start, end, step)` — `start`부터 `end`까지 주어진 증분으로 만든 숫자 배열.
- `linspace(start, end, count)` — 범위를 균등 간격으로 나눈 `count`개의 숫자.
- `meshgrid(arr1, arr2)` — 두 입력 배열로 만든 좌표 쌍.

## 샘플 배열 도우미

### series()

튜플 샘플을 별도의 배열들로 변환합니다.

```js
series(samples, options)
```

- `samples` `Array<[time, Number]>` — 튜플 샘플.
- `options` `Object` 선택 — `{ xKey?, yKey? }`, 반환 배열의 키 이름 (기본값 `"time"`, `"value"`).
- 두 개의 배열을 가진 `Object`를 반환하며 기본 형태는 `{ time, value }` 입니다.

```js
const m = require("mathx");
const s = m.series(gen);
console.log(s.time.length, s.value.length);

const custom = m.series(gen, { xKey: "ts", yKey: "amp" });
console.log(custom.ts.length, custom.amp.length);
```

### unzip()

튜플 샘플을 두 배열로 나눕니다: `Array<[x, y]>` → `[Array<x>, Array<y>]`.

```js
const m = require("mathx");
const [x, y] = m.unzip([[1, 10], [2, 20], [3, 30]]);
console.log(x); // [1, 2, 3]
console.log(y); // [10, 20, 30]
```

### zip()

길이가 같은 두 배열을 튜플 샘플로 결합합니다: `Array` 두 개 → `Array<[x, y]>`.

```js
const m = require("mathx");
const samples = m.zip([1, 2, 3], [10, 20, 30]);
console.log(samples[0]); // [1, 10]
```

## Analysis

### fft()

고속 푸리에 변환 분석을 수행합니다.

```js
fft(times, amplitudes)   // or fft(timesAndAmplitudes)
```

변환의 주파수/진폭 결과를 반환합니다.

## Statistics

이 모듈은 `Array<Number>`에 대해 동작하는 배열·통계 도우미도 제공합니다:

`sort()`, `sum()`, `mean()`, `median()`, `medianInterp()`, `mode()`, `quantile()`, `quantileInterp()`, `cdf()`, `stdDev()`, `stdErr()`, `meanStdDev()`, `moment()`, `covariance()`, `correlation()`, `circularMean()`, `geometricMean()`, `harmonicMean()`, `entropy()`, and `linearRegression()` (returns `{ slope, intercept }`).
