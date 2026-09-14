# Machbase Neo JavaScript UUID Module

JSH 애플리케이션용 UUID 생성기입니다.

## UUID

<h6>문법</h6>

```js
new UUID(ver)
```

<h6>파라미터</h6>

`ver` UUID 버전 번호입니다. 1, 4, 6, 7 중 하나여야 합니다.

<h6>반환값</h6>

새 UUID 생성기 객체입니다.

### eval()

새 UUID 문자열을 생성합니다.

<h6>문법</h6>

```js
eval()
```

<h6>반환값</h6>

`String` a new UUID.

<h6>사용 예제</h6>

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
