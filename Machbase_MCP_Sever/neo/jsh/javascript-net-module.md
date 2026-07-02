# Machbase Neo JavaScript Net Module

The `net` module provides Node.js-compatible TCP networking APIs for JSH applications.

## createServer()

Creates a TCP server.

<h6>Syntax</h6>

```js
createServer([options][, connectionListener])
```

- Returns: `Server`
- If `connectionListener` is provided, it is registered for the `connection` event.

<h6>Usage example</h6>

```js
const net = require('net');

const server = net.createServer((socket) => {
    socket.on('data', (data) => {
        const msg = data.toString();
        socket.write('Echo: ' + msg);
    });
});

server.listen(0, '127.0.0.1');
```

## createConnection() / connect()

Creates a TCP client socket and connects to a server.

<h6>Syntax</h6>

```js
createConnection(port[, host][, connectListener])
createConnection(options[, connectListener])
connect(port[, host][, connectListener])
connect(options[, connectListener])
```

- Returns: `Socket`

<h6>Usage example</h6>

```js
const net = require('net');

const client = net.createConnection({ port: 5650, host: '127.0.0.1' }, () => {
    client.write('Hello Server\n');
});

client.on('data', (data) => {
    console.println(data.toString().trim());
    client.end();
});
```

## IP validation utilities

- `isIP(input)` returns `4`, `6`, or `0`
- `isIPv4(input)` returns `boolean`
- `isIPv6(input)` returns `boolean`

<h6>Usage example</h6>

```js
const net = require('net');
console.println(net.isIP('127.0.0.1'));    // 4
console.println(net.isIPv4('127.0.0.1'));  // true
console.println(net.isIPv6('::1'));        // true
```

## Server

TCP server object returned by `createServer()`.

<h6>Main properties</h6>

- `listening`
- `connections`

**Server methods**

- `listen(port[, host][, backlog][, callback])`
- `listen(options[, callback])`
- `close([callback])`
- `address()`
- `getConnections([callback])`
- `ref()`
- `unref()`

**Server events**

- `connection` (`Socket`)
- `listening` ()
- `close` ()
- `error` (`Error`)

<h6>Usage example</h6>

```js
const net = require('net');
const server = net.createServer();

server.on('listening', () => {
    const addr = server.address();
    console.println(addr.family, addr.address, addr.port);
});

server.listen(0, '127.0.0.1', () => {
    console.println('server ready');
});
```

## Socket

TCP client/server connection object.

<h6>Main properties</h6>

- `connecting`, `readable`, `writable`, `destroyed`
- `bytesRead`, `bytesWritten`
- `localAddress`, `localPort`
- `remoteAddress`, `remotePort`, `remoteFamily`

**Socket methods**

- `connect(port[, host][, connectListener])`
- `connect(options[, connectListener])`
- `write(data[, encoding][, callback])`
- `end([data[, encoding]][, callback])`
- `destroy([error])`
- `setTimeout(timeout[, callback])`
- `setNoDelay([noDelay])`
- `setKeepAlive([enable][, initialDelay])`
- `setEncoding([encoding])`
- `address()`
- `pause()`, `resume()`
- `ref()`, `unref()`

**Socket events**

- `connect` ()
- `data` (`Buffer`)
- `end` ()
- `close` (`hadError`)
- `error` (`Error`)
- `finish` ()

**Behavior notes**

- `data` event payload is emitted as `Buffer`.
- `write()` supports `string`, `Buffer`, `Array`, and `Uint8Array`-compatible values.
- `pause()` / `resume()` are currently no-op in the native implementation.

<h6>Usage example</h6>

```js
const net = require('net');
const client = net.connect(5650, '127.0.0.1');

client.on('connect', () => {
    client.setNoDelay(true);
    client.write('ping\n');
});

client.on('data', (data) => {
    console.println('received:', data.toString().trim());
    client.end();
});

client.on('close', (hadError) => {
    console.println('closed, hadError=', hadError);
});
```
