# Machbase Neo JavaScript Generator Module

## arrange()

숫자 배열을 반환합니다.

**문법**

```js
arrange(start, end, step)
```

**파라미터**

- `start` `Number` start from
- `end` `Number` end to
- `step` `Number` increments

**반환값**

`Number[]` 생성된 숫자들의 배열.

**사용 예제**

```js
const { arrange } = require("@jsh/generator")
arrange(0, 6, 3).forEach((i) => console.log(i))

// 0
// 3
// 6
```

## linspace()

숫자 배열을 반환합니다.

**문법**

```js
linspace(start, end, count)
```

**파라미터**

- `start` `Number` start from
- `end` `Number` end to
- `count` `Number` 생성할 숫자의 총 개수

**반환값**

`Number[]` 생성된 숫자들의 배열.

**사용 예제**

```js
const { linspace } = require("@jsh/generator")
linspace(0, 1, 3).forEach((i) => console.log(i))

// 0
// 1.5
// 1
```

## meshgrid()

숫자 배열의 배열을 반환합니다.

**문법**

```js
meshgrid(arr1, arr2)
```

**파라미터**

- `arr1` `Number[]`
- `arr2` `Number[]`

**반환값**

`Number[][]` 생성된 숫자들의 배열의 배열.

**사용 예제**

```js
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

[0.0, 1.0) 범위의 난수를 반환합니다.

**문법**

```js
random()
```

**파라미터**

None.

**반환값**

`Number` 0.0과 1.0 사이의 난수 : `[0.0, 1.0)`

**사용 예제**

```js
const { random } = require("@jsh/generator")
for(i=0; i < 3; i++) {
    console.log(random().toFixed(2))
}

// 0.54
// 0.12
// 0.84
```

## Simplex

Simplex 노이즈 알고리즘 기반 노이즈 생성기입니다.

**문법**

```js
new Simplex(seed)
```

**파라미터**

`seed` seed number.

**반환값**

새 Simplex 생성기 객체입니다.

### eval()

무작위 노이즈 값을 반환합니다. 같은 인자로 반복 호출하면 같은 출력이 나옵니다.

**문법**

```js
eval(arg1)
eval(arg1, arg2)
eval(arg1, arg2, arg3)
eval(arg1, arg2, arg3, arg4)
```

**파라미터**

`args` `Number` 차원을 나타내는 가변 길이 숫자 목록입니다. 최소 1개(1차원)에서 최대 4개(4차원) 인자를 받습니다.

**반환값**

`Number` 무작위 노이즈 값

**사용 예제**

```js
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

UUID 생성기

**문법**

```js
new UUID(ver)
```

**파라미터**

`ver` UUID 버전 번호입니다. 1, 4, 6, 7 중 하나여야 합니다.

**반환값**

새 UUID 생성기 객체입니다.

### eval()

**문법**

```js
eval()
```

**파라미터**

None.

**반환값**

`String` a new UUID.

**사용 예제**

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
