# Machbase Neo JavaScript Mat Module

## Dense()

밀집 행렬(Dense Matrix)

**생성**

```js
new Dense(r, c, data)
```

**파라미터**

- `r` `Number` rows
- `c` `Number` cols
- `data` `Number[]`

r개 행과 c개 열을 가진 새 밀집 행렬을 만듭니다.

### dims()

### at()

### set()

### T()

전치된 새 밀집 행렬을 만듭니다.

```js
const mat = require("@jsh/mat");
A = new mat.Dense(2, 2, [
    1, 2,
    3, 4,
])
B = A.T()
console.log(mat.format(B))

// ⎡1 3⎤
// ⎣2 4⎦
```

### add()

```js
const mat = require("@jsh/mat");
A = new mat.Dense(2, 2, [
    1, 2,
    3, 4,
])
B = new mat.Dense(2, 2, [
    10, 20,
    30, 40,
])
C = new mat.Dense()
C.add(A, B) // C = A + B
console.log(mat.format(C))

// ⎡11 22⎤ 
// ⎣33 44⎦
```

### sub()

```js
const mat = require("@jsh/mat");
A = new mat.Dense(2, 2, [
    1, 2,
    3, 4,
])
B = new mat.Dense(2, 2, [
    10, 20,
    30, 40,
])
C = new mat.Dense()
C.sub(B, A) // C = B - A
console.log(mat.format(C))

// ⎡ 9 18⎤ 
// ⎣27 36⎦
```

### mul()

```js
const mat = require("@jsh/mat");
A = new mat.Dense(2, 2, [
    1, 2,
    3, 4,
])
B = new mat.Dense(2, 2, [
    10, 20,
    30, 40,
])
C = new mat.Dense()
C.mul(A, B) // C = A * B
console.log(mat.format(C))

// ⎡ 70 100⎤ 
// ⎣150 220⎦
```

### mulElem()

```js
const mat = require("@jsh/mat");
A = new mat.Dense(2, 2, [
    1, 2,
    3, 4,
])
B = new mat.Dense(2, 2, [
    10, 20,
    30, 40,
])
C = new mat.Dense()
C.mulElem(A, B)
console.log(mat.format(C))

// ⎡ 10 40⎤ 
// ⎣ 90 160⎦
```

### divElem()
### inverse()

```js
const mat = require("@jsh/mat");
A = new mat.Dense(2, 2, [
    1, 2,
    3, 4,
])

B = new mat.Dense()
B.inverse(A)

C = new mat.Dense()
C.mul(A, B)

console.log(mat.format(B, {format:"B=%.f", prefix:"  "}))
console.log(mat.format(C, {format:"C=%.f", prefix:"  "}))

//B=⎡-2  1⎤
//  ⎣ 1 -0⎦
//C=⎡1 0⎤
//  ⎣0 1⎦
```

### solve()
### exp()
### pow()
### scale()

## VecDense

Vector

**생성**

```js
new VecDense(n, data)
```

**파라미터**

- `n` `Number` 길이 n의 새 VecDense를 만듭니다. 0보다 커야 합니다.
- `data` `Number[]` 요소 배열. 생략하면 빈 배열이 할당됩니다.

### cap()
### len()
### atVec()
### setVec()
### addVec()
### subVec()
### mulVec()
### mulElemVec()
### scaleVec()
### solveVec()

## QR

**QR 분해**는 행렬 *A*를 직교행렬 *Q*와 상삼각행렬 *R*의 곱 `A = QR`로 분해하는 것입니다.
QR 분해는 선형 최소제곱(LLS) 문제를 푸는 데 자주 쓰이며, 고유값 알고리즘의 하나인 QR 알고리즘의 기초가 됩니다.

임의의 실수 정사각행렬 *A*는 다음과 같이 분해할 수 있습니다

```
A = QR
```

여기서 *Q*는 직교행렬, *R*은 상삼각행렬입니다.
*A*가 가역이면, *R*의 대각 원소를 양수로 제한할 때 분해가 유일합니다.

**사용 예제**

```js
const m = require("@jsh/mat")
A = new m.Dense(4, 2, [
    0, 1,
    1, 1,
    1, 1,
    2, 1,
])

qr = new m.QR()
qr.factorize(A)

Q = new m.Dense()
qr.QTo(Q)

R = new m.Dense()
qr.RTo(R)

B = new m.Dense(4, 1, [1, 0, 2, 1])
x = new m.Dense()
qr.solveTo(x, false, B)
console.log(m.format(x, { format: "x = %.2f", prefix: "    " }))

// x = ⎡0.00⎤
//     ⎣1.00⎦
```

## format()

```js
const m = require("@jsh/mat")
A = new m.Dense(100, 100)
for (let i = 0; i < 100; i++) {
    for (let j = 0; j < 100; j++) {
        A.set(i, j, i + j)
    }
}
console.log(m.format(A, {
    format: "A = %v",
    prefix: "    ",
    squeeze: true,
    excerpt: 3,
}))

// A = Dims(100, 100)
//     ⎡ 0    1    2  ...  ...   97   98   99⎤
//     ⎢ 1    2    3             98   99  100⎥
//     ⎢ 2    3    4             99  100  101⎥
//      .
//      .
//      .
//     ⎢97   98   99            194  195  196⎥
//     ⎢98   99  100            195  196  197⎥
//     ⎣99  100  101  ...  ...  196  197  198⎦
```
