# Machbase Neo JavaScript Tail Module

The `util/tail` module provides file-tailing functionality for JSH applications, enabling real-time monitoring of log files and other continuously-appended files.

```js
const tail = require('@jsh/util/tail');
```

## tail.create()

Creates a tail watcher for a file.

### Syntax

```js
tail.create(path[, options])
```

### Parameters

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `path` | String | Absolute path to the file to tail |
| `options` | Object | Optional configuration |
| `options.fromBeginning` | Boolean | Start reading from the beginning of the file (default: false) |
| `options.follow` | Boolean | Continue watching for new data (default: true) |
| `options.encoding` | String | File encoding (default: `"utf-8"`) |
| `options.separator` | String | Line separator (default: `"\n"`) |

### Returned Object

| Property/Method | Type | Description |
|:----------------|:-----|:------------|
| `on(event, callback)` | Function | Registers an event listener |
| `close()` | Function | Stops tailing and releases resources |
| `path` | String | The file path being tailed |

### Events

| Event | Callback Signature | Description |
|:------|:-------------------|:------------|
| `line` | `function(line)` | Emitted for each new line |
| `error` | `function(err)` | Emitted on error |
| `close` | `function()` | Emitted when tailing stops |

### Basic Usage Example

```js
const tail = require('@jsh/util/tail');

const watcher = tail.create('/var/log/machbase-neo.log', {
    fromBeginning: false,
    follow: true
});

watcher.on('line', function(line) {
    console.log('New line:', line);
});

watcher.on('error', function(err) {
    console.error('Tail error:', err);
});

watcher.on('close', function() {
    console.log('Tailing stopped');
});

// Stop tailing after 60 seconds
setTimeout(function() {
    watcher.close();
}, 60000);
```

## SSE Adapter

The `tail/sse` sub-module provides a Server-Sent Events adapter for streaming tail output to HTTP clients.

### tail/sse.create()

Creates an SSE-compatible tail stream.

### Syntax

```js
const tailSSE = require('@jsh/util/tail/sse');
tailSSE.create(path, response[, options])
```

### Parameters

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `path` | String | Absolute path to the file to tail |
| `response` | Object | HTTP response object (from CGI or HTTP server) |
| `options` | Object | Optional configuration |
| `options.fromBeginning` | Boolean | Start from beginning of file (default: false) |
| `options.event` | String | SSE event name (default: `"message"`) |
| `options.retry` | Number | SSE retry interval in milliseconds |

### Returned Object

| Property/Method | Type | Description |
|:----------------|:-----|:------------|
| `close()` | Function | Stops the SSE stream |
| `on(event, callback)` | Function | Registers an event listener |

### cgi-bin SSE Example

```js
#!/usr/bin/env jsh
// cgi-bin/tail-log.js

const tailSSE = require('@jsh/util/tail/sse');
const path = '/data/logs/machbase-neo.log';

// Set SSE headers
console.write('Content-Type: text/event-stream\r\n');
console.write('Cache-Control: no-cache\r\n');
console.write('Connection: keep-alive\r\n');
console.write('\r\n');

const stream = tailSSE.create(path, {
    fromBeginning: false,
    event: 'log'
});

stream.on('error', function(err) {
    console.error('SSE tail error:', err);
    stream.close();
});

// Keep the CGI process alive
const keepalive = setInterval(function() {}, 30000);

// Clean up on exit
process.on('exit', function() {
    clearInterval(keepalive);
    stream.close();
});
```

## Behavior notes

- The tail module uses filesystem watchers internally and efficiently detects file changes.
- When `follow` is true, the watcher continues monitoring even after reaching the end of the file.
- File truncation is detected automatically; tailing restarts from the beginning of the truncated file.
- The SSE adapter automatically formats output as Server-Sent Events, including `data:` prefixes and double-newline terminators.
- In CGI mode, a `setInterval` keepalive is required to prevent the process from terminating while the tail stream is active.
- Resources are released when `close()` is called; always call `close()` to prevent file descriptor leaks.
