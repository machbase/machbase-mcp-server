# Machbase Neo JavaScript Net Module

`net` 모듈은 JSH 애플리케이션에 Node.js 호환 TCP 네트워킹 API를 제공합니다.

## createServer()

TCP 서버를 만듭니다.

<h6>문법</h6>

```js
createServer([options][, connectionListener])
```

- Returns: `Server`
- `connectionListener`를 주면 `connection` 이벤트에 등록됩니다.

<h6>사용 예제</h6>

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

TCP 클라이언트 소켓을 만들어 서버에 연결합니다.

<h6>문법</h6>

```js
createConnection(port[, host][, connectListener])
createConnection(options[, connectListener])
connect(port[, host][, connectListener])
connect(options[, connectListener])
```

- Returns: `Socket`

<h6>사용 예제</h6>

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

## IP 검증 유틸리티

- `isIP(input)` returns `4`, `6`, or `0`
- `isIPv4(input)` returns `boolean`
- `isIPv6(input)` returns `boolean`

<h6>사용 예제</h6>

```js
const net = require('net');
console.println(net.isIP('127.0.0.1'));    // 4
console.println(net.isIPv4('127.0.0.1'));  // true
console.println(net.isIPv6('::1'));        // true
```

## Server

`createServer()`가 반환하는 TCP 서버 객체입니다.

<h6>주요 속성</h6>

- `listening`
- `connections`

**서버 메서드**

- `listen(port[, host][, backlog][, callback])`
- `listen(options[, callback])`
- `close([callback])`
- `address()`
- `getConnections([callback])`
- `ref()`
- `unref()`

**서버 이벤트**

- `connection` (`Socket`)
- `listening` ()
- `close` ()
- `error` (`Error`)

<h6>사용 예제</h6>

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

TCP 클라이언트·서버 연결 객체입니다.

<h6>주요 속성</h6>

- `connecting`, `readable`, `writable`, `destroyed`
- `bytesRead`, `bytesWritten`
- `localAddress`, `localPort`
- `remoteAddress`, `remotePort`, `remoteFamily`

**소켓 메서드**

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

**소켓 이벤트**

- `connect` ()
- `data` (`Buffer`)
- `end` ()
- `close` (`hadError`)
- `error` (`Error`)
- `finish` ()

**동작 참고사항**

- `data` 이벤트의 페이로드는 `Buffer`로 전달됩니다.
- `write()`는 `string`, `Buffer`, `Array`, `Uint8Array` 호환 값을 지원합니다.
- `pause()` / `resume()`은 현재 네이티브 구현에서 아무 동작도 하지 않습니다.

<h6>사용 예제</h6>

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
