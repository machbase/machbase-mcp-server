# Machbase Neo JavaScript Simplex Module

`Simplex` 클래스는 JSH 애플리케이션용 Simplex 노이즈 생성기를 만듭니다.

## Simplex

Simplex 노이즈 알고리즘을 사용하는 노이즈 생성기를 만듭니다.

<h6>문법</h6>

```js
new Simplex(seed)
```

<h6>파라미터</h6>

- `seed` `Number` 노이즈 생성기의 시드 값

<h6>반환값</h6>

새 Simplex 노이즈 생성기 객체입니다.

### eval()

주어진 좌표에 대한 노이즈 값을 생성합니다.

<h6>문법</h6>

```js
eval(...args)
```

<h6>파라미터</h6>

차원을 나타내는 1~4개의 숫자 인자를 받습니다(1D~4D 노이즈).

<h6>반환값</h6>

`Number` 노이즈 값. 같은 입력으로 반복 호출하면 같은 출력이 나옵니다.

<h6>사용 예제</h6>

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
