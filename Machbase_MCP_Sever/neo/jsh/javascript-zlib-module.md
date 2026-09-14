# Machbase Neo JavaScript Zlib Module

`zlib` 모듈은 JSH 애플리케이션에 Node.js 방식의 압축·해제 API를 제공합니다.
gzip, deflate, raw deflate, 형식 자동 감지 unzip과 동기 도우미, 콜백 기반 비동기 도우미, 스트림 방식 처리를 지원합니다.

```js
const zlib = require('zlib');
```

## 동기 메서드

이 메서드들은 `ArrayBuffer`를 반환합니다.

### gzipSync()

gzip으로 데이터를 압축합니다.

```js
gzipSync(data)
```

### gunzipSync()

gzip 데이터를 해제합니다.

```js
gunzipSync(data)
```

### deflateSync()

deflate로 데이터를 압축합니다.

```js
deflateSync(data)
```

### inflateSync()

deflate 데이터를 해제합니다.

```js
inflateSync(data)
```

### deflateRawSync()

raw deflate로 데이터를 압축합니다.

```js
deflateRawSync(data)
```

### inflateRawSync()

raw deflate 데이터를 해제합니다.

```js
inflateRawSync(data)
```

### unzipSync()

형식을 자동 감지해 gzip 또는 deflate 데이터를 해제합니다.

```js
unzipSync(data)
```

<h6>사용 예제</h6>

```js
const zlib = require('zlib');

const compressed = zlib.gzipSync('Hello, World!');
const decompressed = zlib.gunzipSync(compressed);
const text = String.fromCharCode.apply(null, new Uint8Array(decompressed));
console.println(text);
```

## 비동기 메서드

콜백 기반: `gzip()`, `gunzip()`, `deflate()`, `inflate()`, `deflateRaw()`, `inflateRaw()`, `unzip()`.

콜백 시그니처는 `(err, result) => {}` 이며 `result`는 `ArrayBuffer`로 반환됩니다.

<h6>사용 예제</h6>

```js
const zlib = require('zlib');

zlib.gzip('Hello, World!', (err, compressed) => {
    if (err) { console.println(err.message); return; }
    zlib.gunzip(compressed, (err2, decompressed) => {
        if (err2) { console.println(err2.message); return; }
        const text = String.fromCharCode.apply(null, new Uint8Array(decompressed));
        console.println(text);
    });
});
```

## 스트림 팩토리 메서드

- `createGzip()`, `createGunzip()`
- `createDeflate()`, `createInflate()`
- `createDeflateRaw()`, `createInflateRaw()`
- `createUnzip()`

각 팩토리는 다음 멤버를 가진 zlib 스트림 객체를 반환합니다:

| 멤버 | 설명 |
|:-------|:------------|
| `write(data)` | 스트림에 입력 데이터를 씁니다. |
| `end([data])` | 선택적으로 마지막 조각을 쓰고 스트림을 종료합니다. |
| `on(event, callback)` | `data`, `end`, `error`에 대한 리스너를 등록합니다. |
| `pipe(dest[, options])` | 스트림 출력을 다른 쓰기 가능한 대상으로 전달합니다. |
| `flush()` | 대기 중인 압축 출력을 플러시합니다. |
| `close()` | 내부 압축·해제 객체를 닫습니다. |
| `bytesWritten` | 지금까지 받은 입력 바이트 수. |
| `bytesRead` | 지금까지 생성한 출력 바이트 수. |

## 스트리밍 예제

```js
const zlib = require('zlib');

const gzip = zlib.createGzip();
gzip.on('data', (chunk) => {
    console.println('compressed bytes:', chunk.byteLength);
});
gzip.on('end', () => {
    console.println('done');
});

gzip.write('Hello, ');
gzip.end('World!');
```

## constants

이 모듈은 zlib 상수를 `zlib.constants`로 내보냅니다.

- flush: `Z_NO_FLUSH`, `Z_SYNC_FLUSH`, `Z_FINISH`
- levels: `Z_NO_COMPRESSION`, `Z_BEST_SPEED`, `Z_BEST_COMPRESSION`, `Z_DEFAULT_COMPRESSION`
- status: `Z_OK`, `Z_STREAM_END`, `Z_DATA_ERROR`

## 동작 참고사항

- API 형태는 Node.js와 비슷하지만 Node.js `zlib`을 완전히 대체하지는 않습니다.
- 스트림 `on()`은 `data`, `end`, `error` 콜백만 지원합니다.
- 비동기 도우미는 콜백 기반만 제공하며 Promise 방식은 없습니다.
