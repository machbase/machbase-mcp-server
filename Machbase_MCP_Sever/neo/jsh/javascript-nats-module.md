# Machbase Neo JavaScript NATS Module

The `nats` module provides an event-driven NATS client for JSH applications.
The client automatically starts connecting when a `Client` is created.

Typical usage looks like this.

```js
const nats = require('nats');
```

## Client

Creates a NATS client and begins connecting.

<h6>Syntax</h6>

```js
new nats.Client(options)
```

<h6>Options</h6>

- `servers` server URLs (e.g. `nats://localhost:4222`)
- `user` authentication user
- `password` authentication password
- `token` authentication token
- `timeout` connection timeout in milliseconds
- `reconnect` enable automatic reconnection
- `maxReconnectAttempts` maximum reconnection attempts

The `config` property exposes the active configuration.

## publish()

Sends a message to a NATS subject.

<h6>Syntax</h6>

```js
client.publish(subject, message[, options])
```

<h6>Options</h6>

- `reply` optional reply subject for request/reply patterns

Calling `publish()` before the connection is open emits an `error` event.

## subscribe()

Subscribes to a NATS subject.

<h6>Syntax</h6>

```js
client.subscribe(subject[, options])
```

<h6>Options</h6>

- `queue` queue group name for load-balanced distribution

Calling `subscribe()` before the connection is open emits an `error` event.

## close()

Terminates the NATS connection.

<h6>Syntax</h6>

```js
client.close()
```

## Events

- `open` - connection established
- `message` - message received from subscription; message object includes `subject`, `reply`, and `payload`
- `subscribed` - server accepted the subscription
- `published` - publish completed
- `error` - connection or operation failure
- `close` - connection closed

## Usage example: Pub/Sub

```js
const nats = require('nats');

const sub = new nats.Client({ servers: 'nats://127.0.0.1:4222' });
sub.on('open', function() {
    sub.subscribe('demo.topic');
});
sub.on('message', function(msg) {
    console.println('Received:', msg.subject, msg.payload);
    sub.close();
});

const pub = new nats.Client({ servers: 'nats://127.0.0.1:4222' });
pub.on('open', function() {
    pub.publish('demo.topic', 'hello nats');
});
pub.on('published', function() {
    pub.close();
});
```

## Usage example: Request/Reply

```js
const nats = require('nats');

const responder = new nats.Client({ servers: 'nats://127.0.0.1:4222' });
responder.on('open', function() {
    responder.subscribe('rpc.echo');
});
responder.on('message', function(msg) {
    if (msg.reply) {
        responder.publish(msg.reply, 'reply: ' + msg.payload);
    }
});

const requester = new nats.Client({ servers: 'nats://127.0.0.1:4222' });
requester.on('open', function() {
    requester.subscribe('reply.inbox');
    requester.publish('rpc.echo', 'ping', { reply: 'reply.inbox' });
});
requester.on('message', function(msg) {
    console.println('Reply:', msg.payload);
    requester.close();
    responder.close();
});
```

## Behavior notes

- The client automatically starts connecting when created.
- Calling `publish()` or `subscribe()` before the connection is open emits an `error` event.
- Queue subscriptions enable load-balanced message distribution across multiple subscribers.
