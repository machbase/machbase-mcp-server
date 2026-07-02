# Machbase Neo JavaScript Events Module

The `events` module provides a small `EventEmitter` implementation for JSH.
Many built-in JSH modules use this class as the base for event-driven APIs.

Typical usage looks like this.

```js
const EventEmitter = require('events');
```

## EventEmitter

Creates a new event emitter instance.

<h6>Syntax</h6>

```js
new EventEmitter()
```

The implementation stores listeners per event name and returns the emitter instance from most mutating methods so calls can be chained.

## on()

Registers a listener for an event.

<h6>Syntax</h6>

```js
emitter.on(event, listener)
```

`listener` must be a function, otherwise `TypeError` is thrown.

## addListener()

Alias of `on()`.

<h6>Syntax</h6>

```js
emitter.addListener(event, listener)
```

## once()

Registers a listener that runs only once.

<h6>Syntax</h6>

```js
emitter.once(event, listener)
```

After the first invocation, the listener is removed automatically.

## removeListener()

Removes one matching listener.

<h6>Syntax</h6>

```js
emitter.removeListener(event, listener)
```

## off()

Alias of `removeListener()`.

<h6>Syntax</h6>

```js
emitter.off(event, listener)
```

## removeAllListeners()

Removes all listeners for one event, or all events when called without an argument.

<h6>Syntax</h6>

```js
emitter.removeAllListeners()
emitter.removeAllListeners(event)
```

## emit()

Emits an event and passes all remaining arguments to listeners.

<h6>Syntax</h6>

```js
emitter.emit(event, ...args)
```

<h6>Return value</h6>

- `true` if at least one listener existed for the event
- `false` otherwise

If a listener throws while handling a non-`error` event and the emitter has an `error` listener, the emitter forwards the error through `emit('error', err)`.

## Introspection helpers

### listeners()

Returns a shallow copy of the current listeners for an event.

```js
emitter.listeners(event)
```

### listenerCount()

Returns the number of listeners registered for an event.

```js
emitter.listenerCount(event)
```

### eventNames()

Returns the registered event names.

```js
emitter.eventNames()
```

## Listener limits

### setMaxListeners()

Sets the warning threshold for listener counts.

```js
emitter.setMaxListeners(n)
```

### getMaxListeners()

Returns the current listener warning threshold.

```js
emitter.getMaxListeners()
```

The default maximum is `10` listeners per event.
When the limit is exceeded, the implementation writes a warning using `console.warn()`, but it still keeps the listeners.

## Usage example

```js
const EventEmitter = require('events');

const emitter = new EventEmitter();
emitter.on('greet', function(name) {
    console.println('Hello, ' + name + '!');
});

emitter.emit('greet', 'Alice');
emitter.emit('greet', 'Bob');
```

## once() example

```js
const EventEmitter = require('events');

const emitter = new EventEmitter();
emitter.once('greet', function(name) {
    console.println('Hello, ' + name + '!');
});

emitter.emit('greet', 'Alice');
emitter.emit('greet', 'Bob');
```

## Behavior notes

- The module exports the `EventEmitter` class directly.
- This is a lightweight implementation, not a full drop-in replacement for Node.js `events`.
- Listener arrays are copied during `emit()`, so removing listeners while emitting does not affect the current dispatch pass.
- Only one warning mechanism is provided for too many listeners; it does not prevent registration.
