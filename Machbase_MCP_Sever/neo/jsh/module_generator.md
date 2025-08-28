---
title: "@jsh/generator"
type: docs
weight: 50
---

{{< neo_since ver="8.0.52" />}}

## arrange()

Returns array of numbers.

<h6>Syntax</h6>

```js
arrange(start, end, step)
```

<h6>Parameters</h6>

- `start` `Number` start from
- `end` `Number` end to
- `step` `Number` increments

<h6>Return value</h6>

`Number[]` generated numbers in an array.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const { arrange } = require("@jsh/generator")
arrange(0, 6, 3).forEach((i) => console.log(i))

// 0
// 3
// 6
```

## linspace()

Returns array of numbers.

<h6>Syntax</h6>

```js
linspace(start, end, count)
```

<h6>Parameters</h6>

- `start` `Number` start from
- `end` `Number` end to
- `count` `Number` total count of numbers to generate

<h6>Return value</h6>

`Number[]` generated numbers in an array.

<h6>Usage example</h6>


```js {linenos=table,linenostart=1}
const { linspace } = require("@jsh/generator")
linspace(0, 1, 3).forEach((i) => console.log(i))

// 0
// 1.5
// 1
```

## meshgrid()

Returns array of numbers array.

<h6>Syntax</h6>

```js
meshgrid(arr1, arr2)
```

<h6>Parameters</h6>

- `arr1` `Number[]`
- `arr2` `Number[]`

<h6>Return value</h6>

`Number[][]` generated numbers in an array of numbers.

<h6>Usage example</h6>


```js {linenos=table,linenostart=1}
const { meshgrid } = require("@jsh/generator")

const gen = meshgrid([1, 2, 3], [4, 5]);
for(i=0; i < gen.length; i++) {
    console.log(JSON.stringify(gen[i]));
}

// [1,4]
// [1,5]
// [2,4]
// [2,5]
// [3,4]
// [3,5]
```

## random()

Returns a random number between [0.0, 1.0).

<h6>Syntax</h6>

```js
random()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

`Number` random number between 0.0 and 1.0 : `[0.0, 1.0)`

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const { random } = require("@jsh/generator")
for(i=0; i < 3; i++) {
    console.log(random().toFixed(2))
}

// 0.54
// 0.12
// 0.84
```

## Simplex

A noise generator based on the Simplex noise algorithm.

<h6>Syntax</h6>

```js
new Simplex(seed)
```

<h6>Parameters</h6>

`seed` seed number.

<h6>Return value</h6>

A new Simplex generator object.

### eval()

Returns a random noise value. Repeated calls with the same args inputs will have the same output.

<h6>Syntax</h6>

```js
eval(arg1)
eval(arg1, arg2)
eval(arg1, arg2, arg3)
eval(arg1, arg2, arg3, arg4)
```

<h6>Parameters</h6>

`args` `Number` A variable-length list of numbers, representing dimensions. The function accepts a minimum of one argument (1-dimensional) and a maximum of four arguments (4-dimensional).

<h6>Return value</h6>

`Number` random noise value

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const g = require("@jsh/generator")
simplex = new g.Simplex(123);
for(i=0; i < 5; i++) {
    noise = simplex.eval(i, i * 0.6).toFixed(3);
    console.log(i, (i*0.6).toFixed(1), "=>", noise);
}

// 0 0.0 => 0.000
// 1 0.6 => 0.349
// 2 1.2 => 0.319
// 3 1.8 => 0.038
// 4 2.4 => -0.364
```

## UUID

UUID generator

<h6>Syntax</h6>

```js
new UUID(ver)
```

<h6>Parameters</h6>

`ver` UUID version number. It should be one of 1, 4, 6, 7.

<h6>Return value</h6>

a new UUID generator object.

### eval()

<h6>Syntax</h6>

```js
eval()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

`String` a new UUID.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const {UUID} = require("@jsh/generator")
gen = new UUID(1);
for(i=0; i < 3; i++) {
    console.log(gen.eval());
}

// 868c8ec0-2180-11f0-b223-8a17cad8d69c
// 868c97b2-2180-11f0-b223-8a17cad8d69c
// 868c98d4-2180-11f0-b223-8a17cad8d69c
```
