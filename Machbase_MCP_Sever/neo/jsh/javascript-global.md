# Machbase Neo JavaScript Global

추가 모듈을 불러오지 않아도 사용할 수 있는 전역 함수와 객체입니다.

타이머 API는 JSH 이벤트 루프가 제공하고, `console` 객체는 표준 출력과
로깅 도우미를 제공합니다.

## setTimeout()

지정한 밀리초만큼 지연한 뒤 콜백을 한 번 실행합니다.

추가 인자를 주면 콜백에 그대로 전달됩니다.

<h6>문법</h6>

```js
setTimeout(callback, delayMs[, ...args])
```

<h6>반환값</h6>

- 타이머 핸들 객체입니다. `clearTimeout()`에 전달하면 실행을 취소합니다.

<h6>사용 예제</h6>

```js
setTimeout((name, count) => {
    console.println("Timeout with args:", name, count);
}, 50, "test", 42);

// Output:
// Timeout with args: test 42
```

## clearTimeout()

`setTimeout()`으로 만든 콜백이 아직 실행되지 않았다면 취소합니다.

이미 취소되었거나 실행된 타이머에 다시 호출해도 아무 영향이 없습니다.

<h6>문법</h6>

```js
clearTimeout(timer)
```

<h6>사용 예제</h6>

```js
const timer = setTimeout(() => {
    console.println("should not run");
}, 100);

clearTimeout(timer);
clearTimeout(timer);
```

## setInterval()

지정한 밀리초 간격으로 콜백을 반복 실행합니다.

반복 실행을 멈추려면 반환된 핸들을 `clearInterval()`에 전달합니다.

<h6>문법</h6>

```js
setInterval(callback, delayMs[, ...args])
```

<h6>반환값</h6>

- 인터벌 핸들 객체입니다. `clearInterval()`에 전달하면 반복을 멈춥니다.

<h6>사용 예제</h6>

```js
let count = 0;
const timer = setInterval(() => {
    count++;
    console.println("count:", count);
    if (count >= 3) {
        clearInterval(timer);
    }
}, 100);
```

## clearInterval()

`setInterval()`로 만든 반복 콜백을 멈춥니다.

<h6>문법</h6>

```js
clearInterval(interval)
```

## setImmediate()

현재 실행이 끝난 뒤 다음 이벤트 루프 차례에 가능한 한 빨리 콜백이 실행되도록 예약합니다.

타이머 지연 없이 가벼운 비동기 후속 작업을 할 때 유용합니다.

<h6>문법</h6>

```js
setImmediate(callback[, ...args])
```

<h6>반환값</h6>

- immediate 핸들 객체입니다. `clearImmediate()`에 전달하면 실행을 취소합니다.

<h6>사용 예제</h6>

```js
console.println("Add event loop");
setImmediate(() => {
    console.println("event loop called");
});

// Output:
// Add event loop
// event loop called
```

## clearImmediate()

`setImmediate()`로 만든 콜백이 아직 실행되지 않았다면 취소합니다.

<h6>문법</h6>

```js
clearImmediate(immediate)
```

## console

전역 `console` 객체는 로그 출력과 표준 출력 도우미를 제공합니다.

## console.log()

info 수준 로그 메시지를 씁니다. 출력에 `INFO` 수준 접두가 포함됩니다.

<h6>사용 예제</h6>

```js
console.log("Hello, World!");

// Output:
// INFO  Hello, World!
```

## console.debug()

debug 수준 로그 메시지를 씁니다.

## console.info()

info 수준 로그 메시지를 씁니다. `console.log()`와 같은 수준을 사용합니다.

## console.warn()

warning 수준 로그 메시지를 씁니다.

## console.error()

error 수준 로그 메시지를 씁니다.

## console.print()

끝에 줄바꿈 없이 값을 씁니다.

<h6>사용 예제</h6>

```js
console.print("hello", "world");

// Output:
// helloworld
```

## console.println()

값들을 공백으로 구분해 쓰고 끝에 줄바꿈을 붙입니다.

<h6>사용 예제</h6>

```js
console.println("hello", "world");

// Output:
// hello world
```

## console.printf()

형식 문자열을 사용해 서식화된 출력을 씁니다.

<h6>문법</h6>

```js
console.printf(format, ...args)
```

<h6>사용 예제</h6>

```js
console.printf("value=%d, name=%s\n", 42, "neo");

// Output:
// value=42, name=neo
```
