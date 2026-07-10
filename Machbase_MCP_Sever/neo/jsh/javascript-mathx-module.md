# Machbase Neo JavaScript mathx Module

The `mathx` module provides data generators, sample-array helpers, FFT, and statistics functions for use in `SCRIPT()` within TQL and in `*.js` JSH applications.

```js
const m = require("mathx");
```

> **Note**: `series()`, `unzip()`, `zip()`, and the `oscillator()` `noise` option were added in Machbase Neo v8.5.5.

## Generators

### oscillator()

Generates synthetic oscillator samples as `[time, value]` tuples.

```js
oscillator(options)
```

- `options.components` `Array<Object>` (required) — wave components, each `{ amplitude, frequencyHz, phaseRad?, bias? }`.
- `options.timeRange` `Object` (required) — `{ from, to }` (e.g. `{ from: "0s", to: "10s" }`).
- `options.sample` `Number | String` Optional — number of samples, or a sampling rate string with an `Hz` suffix.
- `options.noise` `Number | Object` Optional — noise added to each sample.
  - `Number`: interpreted as the noise amplitude.
  - `Object`: `{ amplitude, seed? }`, where `amplitude` is the noise strength and `seed` makes the noise reproducible.

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

- `arrange(start, end, step)` — array of numbers from `start` to `end` with the given increment.
- `linspace(start, end, count)` — `count` evenly spaced numbers across the range.
- `meshgrid(arr1, arr2)` — coordinate pairs from two input arrays.

## Sample-array helpers

### series()

Converts tuple samples into separate arrays.

```js
series(samples, options)
```

- `samples` `Array<[time, Number]>` — tuple samples.
- `options` `Object` Optional — `{ xKey?, yKey? }`, key names for the returned arrays (defaults `"time"` and `"value"`).
- Returns an `Object` with two arrays; default shape is `{ time, value }`.

```js
const m = require("mathx");
const s = m.series(gen);
console.log(s.time.length, s.value.length);

const custom = m.series(gen, { xKey: "ts", yKey: "amp" });
console.log(custom.ts.length, custom.amp.length);
```

### unzip()

Splits tuple samples into two arrays: `Array<[x, y]>` → `[Array<x>, Array<y>]`.

```js
const m = require("mathx");
const [x, y] = m.unzip([[1, 10], [2, 20], [3, 30]]);
console.log(x); // [1, 2, 3]
console.log(y); // [10, 20, 30]
```

### zip()

Combines two equal-length arrays into tuple samples: two `Array` → `Array<[x, y]>`.

```js
const m = require("mathx");
const samples = m.zip([1, 2, 3], [10, 20, 30]);
console.log(samples[0]); // [1, 10]
```

## Analysis

### fft()

Performs Fast Fourier Transform analysis.

```js
fft(times, amplitudes)   // or fft(timesAndAmplitudes)
```

Returns the frequency/amplitude result of the transform.

## Statistics

The module also provides array/statistics helpers that operate on `Array<Number>`:

`sort()`, `sum()`, `mean()`, `median()`, `medianInterp()`, `mode()`, `quantile()`, `quantileInterp()`, `cdf()`, `stdDev()`, `stdErr()`, `meanStdDev()`, `moment()`, `covariance()`, `correlation()`, `circularMean()`, `geometricMean()`, `harmonicMean()`, `entropy()`, and `linearRegression()` (returns `{ slope, intercept }`).
