# Machbase Neo JavaScript Simplex Module

The `Simplex` class creates a Simplex noise generator for JSH applications.

## Simplex

Creates a noise generator using the Simplex noise algorithm.

<h6>Syntax</h6>

```js
new Simplex(seed)
```

<h6>Parameters</h6>

- `seed` `Number` seed value for the noise generator

<h6>Return value</h6>

A new Simplex noise generator object.

### eval()

Generates a noise value for the given coordinates.

<h6>Syntax</h6>

```js
eval(...args)
```

<h6>Parameters</h6>

Accepts 1 to 4 numeric arguments representing dimensions (1D to 4D noise).

<h6>Return value</h6>

`Number` a noise value. Repeated calls with the same inputs will produce the same output.

<h6>Usage example</h6>

```js
const {Simplex} = require("@jsh/mathx/simplex");

const simplex = new Simplex(123);
for (let i = 0; i < 5; i++) {
    console.println(i, simplex.eval(i, i * 0.6));
}

// 0 0.000
// 1 0.349
// 2 0.319
// 3 0.038
// 4 -0.364
```
