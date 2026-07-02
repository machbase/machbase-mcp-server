# Machbase Neo JavaScript Stream Module

The `stream` module provides Node.js-style stream primitives for JSH applications, wrapping native Go `io.Reader` and `io.Writer` objects.

```js
const stream = require('stream');
```

## Exported classes

- `Readable`
- `Writable`
- `Duplex`
- `PassThrough`
- `Transform`

All classes inherit from `EventEmitter`.

## Readable

Wraps a native reader object.

<h6>Syntax</h6>

```js
new stream.Readable(nativeReader)
```

<h6>Methods</h6>

- `read([size])` read data from the stream
- `readString([size[, encoding]])` read as string
- `pause()` pause the stream
- `resume()` resume the stream
- `isPaused()` check if paused
- `pipe(destination[, options])` forward data to a writable destination
- `unpipe([destination])` stop piping
- `destroy([error])` destroy the stream
- `close()` close the stream

<h6>Properties</h6>

- `readable`, `readableEnded`, `readableFlowing`, `readableHighWaterMark`

<h6>Events</h6>

- `data`, `end`, `error`, `close`, `pause`, `resume`

## Writable

Wraps a native writer object.

<h6>Syntax</h6>

```js
new stream.Writable(nativeWriter)
```

<h6>Methods</h6>

- `write(data[, encoding])` write data; returns `true` on success, `false` otherwise
- `end([data[, encoding]])` end the stream
- `destroy([error])` destroy the stream
- `close()` close the stream

<h6>Properties</h6>

- `writable`, `writableEnded`, `writableFinished`, `writableHighWaterMark`

<h6>Events</h6>

- `finish`, `error`, `close`

## Duplex

Combines both readable and writable capabilities.

<h6>Syntax</h6>

```js
new stream.Duplex(reader, writer)
```

Supports all `Readable` and `Writable` methods simultaneously.

## PassThrough

An in-memory duplex stream that passes written data through unchanged. Useful for testing and buffering without native readers or writers.

<h6>Syntax</h6>

```js
new stream.PassThrough()
```

## Transform

Base class for custom transforms implemented in JavaScript. Subclasses override `_transform()` and optionally `_flush()`.

<h6>Syntax</h6>

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

## Usage example

```js
const stream = require('stream');
const fs = require('fs');

const rs = fs.createReadStream('/work/input.txt', { encoding: 'utf8' });
const ws = fs.createWriteStream('/work/output.txt', { encoding: 'utf8' });
rs.pipe(ws);
```

## Behavior notes

- High-water mark is fixed at 16384 bytes.
- EOF conditions return `null` or empty strings and update `readableEnded`.
- `write()` supports `string`, `Buffer`, `Array`, and `Uint8Array` values.
- This is not a full drop-in replacement for Node.js streams.
- Subclass `Transform` with manual output emission via `this.push()` for best results.
