# Machbase Neo JavaScript WebSocket Module

`ws` 모듈(v8.5.2부터)은 JSH 애플리케이션에서 사용할 수 있는 WebSocket 클라이언트/서버 API를 제공합니다. Go 네이티브 WebSocket 위에 구현된 `WebSocket`과 `WebSocketServer` 클래스를 노출합니다.

```js
const { WebSocket, WebSocketServer } = require('ws');
```

## WebSocket

WebSocket 클라이언트 연결을 생성합니다.

<h6>문법</h6>

```js
new WebSocket(url)
new WebSocket(url, protocol)
new WebSocket(url, protocols)
```

<h6>파라미터</h6>

- `url` `String`: `ws://host:port/path`, `wss://host:port/path` 같은 WebSocket 서버 주소
- `protocol` `String`: 요청할 subprotocol 하나
- `protocols` `String[]`: 요청할 subprotocol 목록

`url`이 없거나 문자열이 아니면 constructor는 `TypeError`를 발생시킵니다.

## 속성

| 속성 | 타입 | 설명 |
|:-----|:-----|:-----|
| `url` | String | constructor에 전달한 원래 WebSocket URL |
| `protocol` | String | 협상된 subprotocol. 없으면 빈 문자열 |
| `readyState` | Number | 현재 연결 상태 |

### readyState 값

- `WebSocket.CONNECTING` = `0`
- `WebSocket.OPEN` = `1`
- `WebSocket.CLOSING` = `2`
- `WebSocket.CLOSED` = `3`

### 메시지 타입 상수

- `WebSocket.TextMessage` = `1`
- `WebSocket.BinaryMessage` = `2`

## send()

서버로 메시지를 전송합니다.

<h6>문법</h6>

```js
ws.send(data)
```

<h6>파라미터</h6>

- `data` `String`: 전송할 텍스트 메시지

현재 JSH 구현에서 `send()`는 텍스트 메시지 사용을 기준으로 설계되어 있습니다.

소켓이 아직 열려 있지 않으면 `error` 이벤트가 발생합니다.

<h6>사용 예제</h6>

```js
const { WebSocket } = require('ws');

const ws = new WebSocket('ws://127.0.0.1:8080');
ws.on('open', () => {
    ws.send('Hello, server');
});
```

## close()

현재 연결을 종료합니다.

<h6>문법</h6>

```js
ws.close()
```

`close()`를 호출하면 소켓은 `CLOSING`을 거쳐 `CLOSED`로 전환되고 `close` 이벤트를 emit합니다.

## 이벤트

`WebSocket`은 `EventEmitter`를 상속하므로 `on()`, `addListener()` 같은 일반적인 이벤트 리스너 패턴을 사용할 수 있습니다.

### open

클라이언트 연결이 성공한 뒤 발생합니다.

```js
ws.on('open', () => {
    console.println('connected');
});
```

### close

연결이 종료되면 발생합니다.

```js
ws.on('close', () => {
    console.println('closed');
});
```

### message

서버에서 메시지가 도착하면 발생합니다. callback은 다음 필드를 가진 event 비슷한 객체를 받습니다.

| 필드 | 타입 | 설명 |
|:-----|:-----|:-----|
| `type` | Number | `WebSocket.TextMessage`, `WebSocket.BinaryMessage` 같은 메시지 타입 |
| `data` | String 또는 byte data | 메시지 payload. 텍스트 메시지는 문자열로 노출됩니다. |

```js
const { WebSocket } = require('ws');

const ws = new WebSocket('ws://127.0.0.1:8080');
ws.on('message', (evt) => {
    console.println(evt.data);
});
```

### error

연결 또는 전송 작업이 실패하면 발생합니다.

```js
ws.on('error', (err) => {
    console.println(err.message);
});
```

## WebSocketServer

WebSocket 서버를 생성해 기존 `http.Server`에 연결합니다.

<h6>문법</h6>

```js
new WebSocketServer(options)
```

<h6>주요 옵션</h6>

- `server`: 연결할 `http.Server` 인스턴스. 필수.
- `path`: 수락할 WebSocket path. 기본값은 `/`.
- `clientTracking`: `true`면 `clients` 집합을 유지합니다. 기본값은 `true`.
- `verifyClient({ origin, req })`: handshake 수락 여부를 동기적으로 결정합니다. `false`를 반환하면 요청을 거부합니다.
- `handleProtocols(protocols, req)`: 요청된 subprotocol 목록에서 선택할 값을 반환합니다.

<h6>속성</h6>

| 속성 | 타입 | 설명 |
|:-----|:-----|:-----|
| `server` | http.Server | 연결된 HTTP 서버 |
| `path` | String | 수락할 WebSocket path |
| `clients` | Set | 연결된 client 집합. `clientTracking === false`이면 `null` |

### WebSocketServer 이벤트

- `connection(socket, request)`
- `error(err)`
- `close()`

### connection request 객체

`connection` 이벤트의 `request`는 Node.js의 `IncomingMessage`와 비슷한 helper 객체입니다.

주요 속성:

- `url`
- `method`
- `headers`
- `rawHeaders`
- `path`
- `host`
- `requestUri`
- `httpVersion`
- `complete`
- `remoteAddress`
- `socket.remoteAddress`

주요 메서드:

- `query(name)`
- `getHeader(name)`
- `hasHeader(name)`

<h6>사용 예제</h6>

```js
const http = require('http');
const { WebSocketServer } = require('ws');

const server = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
const wss = new WebSocketServer({
    server,
    path: '/ws',
    verifyClient: ({ req }) => req.query('token') === 'allow',
    handleProtocols: (protocols) => {
        if (protocols.indexOf('machbase.rpc') >= 0) {
            return 'machbase.rpc';
        }
        return false;
    },
});

wss.on('connection', (socket, request) => {
    console.println(request.path, request.httpVersion, socket.protocol);
    socket.on('message', (event) => {
        socket.send('echo:' + event.data);
    });
});

server.serve();
```

## 클라이언트 사용 예제

```js
const { WebSocket } = require('ws');

const ws = new WebSocket('ws://127.0.0.1:8080');

ws.on('open', () => {
    console.println('websocket open');
    ws.send('test message');
});

ws.on('message', (evt) => {
    console.println(evt.data);
    ws.close();
});

ws.on('close', () => {
    console.println('websocket closed');
});
```

## 동작 참고

- 클라이언트 연결 시작은 constructor 내부에서 비동기적으로 진행됩니다.
- 연결 실패는 `error` 이벤트로 보고됩니다.
- 수신 메시지는 text 또는 binary일 수 있지만, JavaScript의 `send()` 메서드는 텍스트 메시지 용도로 사용하는 것이 안전합니다.
- `WebSocketServer`는 저수준 `upgrade` 이벤트 대신 `http.Server`에 연결되는 상위 수준 API를 제공합니다.
- `verifyClient()`와 `handleProtocols()`는 동기적으로 동작합니다. 이 안에서 Promise/`await` 기반 비동기 흐름은 사용할 수 없습니다.
- `request`는 Node.js의 완전한 `IncomingMessage` 구현이 아니라 `url`, `headers`, `query()`, `getHeader()` 같은 주요 필드/메서드만 제공하는 helper 객체입니다.
- `clientTracking`은 `clients` 집합을 유지하지만, 저수준 소켓 제어 API를 추가로 제공하지는 않습니다.
- 저수준 `upgrade`, `handleUpgrade()`, `noServer` 같은 API는 현재 제공하지 않습니다.
- 장시간 동작하는 WebSocket 워커는 스크립트가 조기 종료되지 않도록 `setInterval` keepalive 패턴을 쓰는 것이 좋습니다.
