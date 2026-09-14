# Machbase Neo JavaScript Stream Module

`stream` 모듈은 네이티브 Go의 `io.Reader`·`io.Writer` 객체를 감싸, JSH 애플리케이션에 Node.js 방식의 스트림 기본 요소를 제공합니다.

```js
const stream = require('stream');
```

## 내보내는 클래스

- `Readable`
- `Writable`
- `Duplex`
- `PassThrough`
- `Transform`

모든 클래스는 `EventEmitter`를 상속합니다.

## Readable

네이티브 reader 객체를 감쌉니다.

<h6>문법</h6>

```js
new stream.Readable(nativeReader)
```

<h6>메서드</h6>

- `read([size])` 스트림에서 데이터를 읽습니다
- `readString([size[, encoding]])` 문자열로 읽습니다
- `pause()` 스트림을 일시 정지합니다
- `resume()` 스트림을 재개합니다
- `isPaused()` 일시 정지 상태인지 확인합니다
- `pipe(destination[, options])` 쓰기 가능한 대상으로 데이터를 전달합니다
- `unpipe([destination])` stop piping
- `destroy([error])` 스트림을 파기합니다
- `close()` 스트림을 닫습니다

<h6>속성</h6>

- `readable`, `readableEnded`, `readableFlowing`, `readableHighWaterMark`

<h6>이벤트</h6>

- `data`, `end`, `error`, `close`, `pause`, `resume`

## Writable

네이티브 writer 객체를 감쌉니다.

<h6>문법</h6>

```js
new stream.Writable(nativeWriter)
```

<h6>메서드</h6>

- `write(data[, encoding])` 데이터를 씁니다. 성공하면 `true`, 아니면 `false`를 반환합니다
- `end([data[, encoding]])` 스트림을 종료합니다
- `destroy([error])` 스트림을 파기합니다
- `close()` 스트림을 닫습니다

<h6>속성</h6>

- `writable`, `writableEnded`, `writableFinished`, `writableHighWaterMark`

<h6>이벤트</h6>

- `finish`, `error`, `close`

## Duplex

읽기와 쓰기 기능을 모두 결합합니다.

<h6>문법</h6>

```js
new stream.Duplex(reader, writer)
```

`Readable`과 `Writable`의 모든 메서드를 동시에 지원합니다.

## PassThrough

쓰인 데이터를 그대로 통과시키는 메모리 내 양방향 스트림입니다. 네이티브 reader·writer 없이 테스트하거나 버퍼링할 때 유용합니다.

<h6>문법</h6>

```js
new stream.PassThrough()
```

## Transform

JavaScript로 구현하는 사용자 정의 변환의 기반 클래스입니다. 하위 클래스는 `_transform()`을, 필요하면 `_flush()`도 재정의합니다.

<h6>문법</h6>

```js
class MyTransform extends stream.Transform {
    _transform(chunk, encoding, callback) {
        this.push(transformedData);
        callback();
    }
    _flush(callback) {
        callback();
    }
}
```

## 사용 예제

```js
const stream = require('stream');
const fs = require('fs');

const rs = fs.createReadStream('/work/input.txt', { encoding: 'utf8' });
const ws = fs.createWriteStream('/work/output.txt', { encoding: 'utf8' });
rs.pipe(ws);
```

## 동작 참고사항

- high-water mark는 16384바이트로 고정되어 있습니다.
- EOF 상황에서는 `null` 또는 빈 문자열을 반환하고 `readableEnded`를 갱신합니다.
- `write()`는 `string`, `Buffer`, `Array`, `Uint8Array` 값을 지원합니다.
- Node.js 스트림을 완전히 대체하지는 않습니다.
- 최적의 결과를 위해 `Transform`을 상속하고 `this.push()`로 직접 출력을 내보내세요.
