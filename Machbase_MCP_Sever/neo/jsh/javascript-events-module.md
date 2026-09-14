# Machbase Neo JavaScript Events Module

`events` 모듈은 JSH를 위한 간단한 `EventEmitter` 구현을 제공합니다.
많은 JSH 내장 모듈이 이벤트 기반 API의 기반으로 이 클래스를 사용합니다.

일반적인 사용법은 다음과 같습니다.

```js
const EventEmitter = require('events');
```

## EventEmitter

새 이벤트 emitter 인스턴스를 만듭니다.

<h6>문법</h6>

```js
new EventEmitter()
```

이 구현은 이벤트 이름별로 리스너를 저장하며, 대부분의 변경 메서드가 emitter 인스턴스를 반환하므로 메서드 체이닝이 가능합니다.

## on()

이벤트에 리스너를 등록합니다.

<h6>문법</h6>

```js
emitter.on(event, listener)
```

`listener`는 함수여야 하며, 아니면 `TypeError`가 발생합니다.

## addListener()

Alias of `on()`.

<h6>문법</h6>

```js
emitter.addListener(event, listener)
```

## once()

한 번만 실행되는 리스너를 등록합니다.

<h6>문법</h6>

```js
emitter.once(event, listener)
```

첫 호출 이후 리스너가 자동으로 제거됩니다.

## removeListener()

일치하는 리스너 하나를 제거합니다.

<h6>문법</h6>

```js
emitter.removeListener(event, listener)
```

## off()

Alias of `removeListener()`.

<h6>문법</h6>

```js
emitter.off(event, listener)
```

## removeAllListeners()

한 이벤트의 모든 리스너를 제거하며, 인자 없이 호출하면 모든 이벤트의 리스너를 제거합니다.

<h6>문법</h6>

```js
emitter.removeAllListeners()
emitter.removeAllListeners(event)
```

## emit()

이벤트를 발생시키고 나머지 인자를 모두 리스너에 전달합니다.

<h6>문법</h6>

```js
emitter.emit(event, ...args)
```

<h6>반환값</h6>

- 해당 이벤트에 리스너가 하나라도 있었으면 `true`
- `false` otherwise

`error`가 아닌 이벤트를 처리하는 중 리스너가 예외를 던지고 emitter에 `error` 리스너가 있으면, emitter는 `emit('error', err)`로 오류를 전달합니다.

## 내부 조회 도우미

### listeners()

이벤트에 등록된 현재 리스너들의 얕은 복사본을 반환합니다.

```js
emitter.listeners(event)
```

### listenerCount()

이벤트에 등록된 리스너 수를 반환합니다.

```js
emitter.listenerCount(event)
```

### eventNames()

등록된 이벤트 이름들을 반환합니다.

```js
emitter.eventNames()
```

## 리스너 제한

### setMaxListeners()

리스너 수 경고 임계값을 설정합니다.

```js
emitter.setMaxListeners(n)
```

### getMaxListeners()

현재 리스너 경고 임계값을 반환합니다.

```js
emitter.getMaxListeners()
```

기본 최대치는 이벤트당 리스너 `10`개입니다.
제한을 넘으면 `console.warn()`으로 경고를 남기지만 리스너는 그대로 유지합니다.

## 사용 예제

```js
const EventEmitter = require('events');

const emitter = new EventEmitter();
emitter.on('greet', function(name) {
    console.println('Hello, ' + name + '!');
});

emitter.emit('greet', 'Alice');
emitter.emit('greet', 'Bob');
```

## once() 예제

```js
const EventEmitter = require('events');

const emitter = new EventEmitter();
emitter.once('greet', function(name) {
    console.println('Hello, ' + name + '!');
});

emitter.emit('greet', 'Alice');
emitter.emit('greet', 'Bob');
```

## 동작 참고사항

- 이 모듈은 `EventEmitter` 클래스를 직접 내보냅니다.
- 가벼운 구현이며 Node.js `events`를 완전히 대체하지는 않습니다.
- `emit()` 중에는 리스너 배열이 복사되므로, 발생 도중 리스너를 제거해도 현재 전달 과정에는 영향이 없습니다.
- 리스너가 너무 많을 때는 경고만 제공하며 등록 자체를 막지는 않습니다.
