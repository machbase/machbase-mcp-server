# Machbase Neo JavaScript WebSocket Module

The `ws` module (since v8.5.2) provides WebSocket client and server capabilities for JSH applications.

```js
const ws = require('@jsh/ws');
```

## WebSocket (Client)

### Constructor

```js
new ws.WebSocket(url[, protocols][, options])
```

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `url` | String | WebSocket server URL (`ws://` or `wss://`) |
| `protocols` | String or Array | Optional sub-protocol(s) |
| `options` | Object | Optional connection options |

### Properties

| Property | Type | Description |
|:---------|:-----|:------------|
| `readyState` | Number | Current connection state |
| `protocol` | String | Negotiated sub-protocol |
| `url` | String | The URL used to create the connection |
| `bufferedAmount` | Number | Bytes queued for transmission |

### readyState Values

| Constant | Value | Description |
|:---------|:------|:------------|
| `ws.CONNECTING` | 0 | Connection not yet open |
| `ws.OPEN` | 1 | Connection is open and ready |
| `ws.CLOSING` | 2 | Connection is closing |
| `ws.CLOSED` | 3 | Connection is closed |

### Message Type Constants

| Constant | Description |
|:---------|:------------|
| `ws.TEXT` | Text message |
| `ws.BINARY` | Binary message |
| `ws.PING` | Ping frame |
| `ws.PONG` | Pong frame |

### send(data[, options])

Sends data through the WebSocket connection.

**Syntax**

```js
socket.send(data[, options])
```

**Parameters**

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `data` | String, ArrayBuffer, Buffer | Data to send |
| `options` | Object | Optional send options |
| `options.compress` | Boolean | Whether to compress the data |
| `options.binary` | Boolean | Whether data is binary |
| `options.fin` | Boolean | Whether this is the final fragment |

**Usage example**

```js
const socket = new ws.WebSocket('ws://127.0.0.1:5654/ws');

socket.on('open', function() {
    socket.send('Hello Server!');
    socket.send(JSON.stringify({ type: 'greeting', msg: 'hello' }));
});

socket.on('message', function(evt) {
    console.log('Received:', evt.data);
});
```

### close([code[, reason]])

Closes the WebSocket connection.

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `code` | Number | Optional status code (default: 1000) |
| `reason` | String | Optional human-readable reason |

### Events

#### open

Emitted when the connection is established.

```js
socket.on('open', function() {
    console.log('Connected');
});
```

#### close

Emitted when the connection is closed.

```js
socket.on('close', function(evt) {
    console.log('Closed:', evt.code, evt.reason);
});
```

#### message

Emitted when a message is received.

| Field | Type | Description |
|:------|:-----|:------------|
| `evt.data` | String or Buffer | The message payload |
| `evt.type` | Number | Message type constant |
| `evt.isBinary` | Boolean | Whether the message is binary |

```js
socket.on('message', function(evt) {
    if (evt.isBinary) {
        console.log('Binary message, length:', evt.data.length);
    } else {
        console.log('Text message:', evt.data);
    }
});
```

#### error

Emitted when an error occurs.

```js
socket.on('error', function(err) {
    console.error('WebSocket error:', err);
});
```

## WebSocketServer

Creates a WebSocket server that listens for incoming connections.

### Syntax

```js
new ws.WebSocketServer(options[, callback])
```

### Options

| Option | Type | Default | Description |
|:-------|:-----|:--------|:------------|
| `server` | Object | - | An existing HTTP server to attach to |
| `path` | String | - | Accept connections only on this path |
| `clientTracking` | Boolean | true | Whether to track connected clients |
| `verifyClient` | Function | - | Function to validate incoming connections |
| `handleProtocols` | Function | - | Function to handle sub-protocol negotiation |

### Properties

| Property | Type | Description |
|:---------|:-----|:------------|
| `clients` | Set | Set of connected clients (when `clientTracking` is true) |
| `path` | String | The path the server is listening on |

### Events

#### connection

Emitted when a new client connects.

```js
wss.on('connection', function(socket, request) {
    console.log('Client connected from:', request.remoteAddress);
    socket.on('message', function(evt) {
        console.log('Received:', evt.data);
    });
});
```

#### error

Emitted when a server error occurs.

```js
wss.on('error', function(err) {
    console.error('Server error:', err);
});
```

#### close

Emitted when the server is closed.

```js
wss.on('close', function() {
    console.log('Server closed');
});
```

### Connection Request Object

The `request` object passed to the `connection` event has the following properties and methods:

| Property/Method | Type | Description |
|:----------------|:-----|:------------|
| `remoteAddress` | String | Client IP address |
| `headers` | Object | HTTP request headers |
| `url` | String | Request URL |

## Full Usage Example (Server)

```js
const ws = require('@jsh/ws');
const http = require('@jsh/http');

const server = http.createServer(function(req, res) {
    res.writeHead(200);
    res.end('WebSocket server running');
});

const wss = new ws.WebSocketServer({ server: server, path: '/ws' });

wss.on('connection', function(socket, request) {
    console.log('New client connected');

    socket.on('message', function(evt) {
        // Echo message back to client
        socket.send('Echo: ' + evt.data);

        // Broadcast to all clients
        wss.clients.forEach(function(client) {
            if (client !== socket && client.readyState === ws.OPEN) {
                client.send(evt.data);
            }
        });
    });

    socket.on('close', function() {
        console.log('Client disconnected');
    });
});

server.listen(9090, function() {
    console.log('Server listening on port 9090');
});
```

## Client Usage Example

```js
const ws = require('@jsh/ws');

const socket = new ws.WebSocket('ws://127.0.0.1:9090/ws');

socket.on('open', function() {
    console.log('Connected to server');
    socket.send('Hello from client!');
});

socket.on('message', function(evt) {
    console.log('Server says:', evt.data);
});

socket.on('close', function(evt) {
    console.log('Disconnected:', evt.code, evt.reason);
});

socket.on('error', function(err) {
    console.error('Connection error:', err);
});
```

## Behavior notes

- The WebSocket module follows the standard WebSocket API pattern adapted for JSH.
- Both text and binary messages are supported.
- The `WebSocketServer` can be attached to an existing HTTP server or run standalone.
- Client tracking is enabled by default and can be used for broadcasting.
- The `verifyClient` callback can be used to implement authentication and authorization.
- Connections are automatically cleaned up when scripts terminate.
- The `setInterval` keepalive pattern is recommended for long-running WebSocket workers to prevent premature script termination.
