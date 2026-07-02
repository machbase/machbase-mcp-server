# Machbase Neo JavaScript Zlib Module

The `zlib` module provides Node.js-style compression and decompression APIs for JSH applications.
It supports gzip, deflate, raw deflate, auto-detected unzip, synchronous helpers, callback-based asynchronous helpers, and stream-style processing.

```js
const zlib = require('zlib');
```

## Synchronous methods

These methods return an `ArrayBuffer`.

### gzipSync()

Compresses data using gzip.

```js
gzipSync(data)
```

### gunzipSync()

Decompresses gzip data.

```js
gunzipSync(data)
```

### deflateSync()

Compresses data using deflate.

```js
deflateSync(data)
```

### inflateSync()

Decompresses deflate data.

```js
inflateSync(data)
```

### deflateRawSync()

Compresses data using raw deflate.

```js
deflateRawSync(data)
```

### inflateRawSync()

Decompresses raw deflate data.

```js
inflateRawSync(data)
```

### unzipSync()

Decompresses gzip or deflate data using automatic format detection.

```js
unzipSync(data)
```

<h6>Usage example</h6>

```js
const zlib = require('zlib');

const compressed = zlib.gzipSync('Hello, World!');
const decompressed = zlib.gunzipSync(compressed);
const text = String.fromCharCode.apply(null, new Uint8Array(decompressed));
console.println(text);
```

## Asynchronous methods

Callback-based: `gzip()`, `gunzip()`, `deflate()`, `inflate()`, `deflateRaw()`, `inflateRaw()`, `unzip()`.

The callback signature is `(err, result) => {}`. `result` is returned as an `ArrayBuffer`.

<h6>Usage example</h6>

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

## Stream factory methods

- `createGzip()`, `createGunzip()`
- `createDeflate()`, `createInflate()`
- `createDeflateRaw()`, `createInflateRaw()`
- `createUnzip()`

Each factory returns a zlib stream object with these members:

| Member | Description |
|:-------|:------------|
| `write(data)` | Writes input data into the stream. |
| `end([data])` | Optionally writes one final chunk and finishes the stream. |
| `on(event, callback)` | Registers a listener for `data`, `end`, or `error`. |
| `pipe(dest[, options])` | Pipes stream output to another writable destination. |
| `flush()` | Flushes pending compression output. |
| `close()` | Closes the underlying compression/decompression object. |
| `bytesWritten` | Number of input bytes accepted so far. |
| `bytesRead` | Number of output bytes produced so far. |

## Streaming example

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

The module exports zlib constants as `zlib.constants`.

- flush: `Z_NO_FLUSH`, `Z_SYNC_FLUSH`, `Z_FINISH`
- levels: `Z_NO_COMPRESSION`, `Z_BEST_SPEED`, `Z_BEST_COMPRESSION`, `Z_DEFAULT_COMPRESSION`
- status: `Z_OK`, `Z_STREAM_END`, `Z_DATA_ERROR`

## Behavior notes

- The API shape is Node.js-like, but it is not a full drop-in replacement for Node.js `zlib`.
- Stream `on()` supports `data`, `end`, and `error` callbacks only.
- Async helpers are callback-based only; promise-based variants are not provided.
