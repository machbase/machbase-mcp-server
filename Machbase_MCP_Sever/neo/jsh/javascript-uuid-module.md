# Machbase Neo JavaScript UUID Module

UUID generator for JSH applications.

## UUID

<h6>Syntax</h6>

```js
new UUID(ver)
```

<h6>Parameters</h6>

`ver` UUID version number. It should be one of 1, 4, 6, 7.

<h6>Return value</h6>

A new UUID generator object.

### eval()

Generates a new UUID string.

<h6>Syntax</h6>

```js
eval()
```

<h6>Return value</h6>

`String` a new UUID.

<h6>Usage example</h6>

```js
const {UUID} = require("@jsh/generator")
gen = new UUID(1);
for(i=0; i < 3; i++) {
    console.log(gen.eval());
}

// 868c8ec0-2180-11f0-b223-8a17cad8d69c
// 868c97b2-2180-11f0-b223-8a17cad8d69c
// 868c98d4-2180-11f0-b223-8a17cad8d69c
```
