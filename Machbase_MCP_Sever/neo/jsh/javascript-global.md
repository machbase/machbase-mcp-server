# Machbase Neo JavaScript Global

These are global functions and objects available without loading any additional module.

Timer APIs are provided by the JSH event loop, and the `console` object provides standard output and
logging helpers.

## setTimeout()

Execute a callback once after the specified delay in milliseconds.

If extra arguments are provided, they are passed to the callback as-is.

<h6>Syntax</h6>

```js
setTimeout(callback, delayMs[, ...args])
```

<h6>Return value</h6>

- A timer handle object. Pass it to `clearTimeout()` to cancel execution.

<h6>Usage example</h6>

```js
setTimeout((name, count) => {
    console.println("Timeout with args:", name, count);
}, 50, "test", 42);

// Output:
// Timeout with args: test 42
```

## clearTimeout()

Cancel a pending callback created by `setTimeout()` if it has not executed yet.

Calling it again for an already cancelled or already executed timer has no further effect.

<h6>Syntax</h6>

```js
clearTimeout(timer)
```

<h6>Usage example</h6>

```js
const timer = setTimeout(() => {
    console.println("should not run");
}, 100);

clearTimeout(timer);
clearTimeout(timer);
```

## setInterval()

Execute a callback repeatedly at the specified interval in milliseconds.

To stop repeated execution, pass the returned handle to `clearInterval()`.

<h6>Syntax</h6>

```js
setInterval(callback, delayMs[, ...args])
```

<h6>Return value</h6>

- An interval handle object. Pass it to `clearInterval()` to stop repetition.

<h6>Usage example</h6>

```js
let count = 0;
const timer = setInterval(() => {
    count++;
    console.println("count:", count);
    if (count >= 3) {
        clearInterval(timer);
    }
}, 100);
```

## clearInterval()

Stop a repeating callback created by `setInterval()`.

<h6>Syntax</h6>

```js
clearInterval(interval)
```

## setImmediate()

Schedule a callback to run as soon as possible on the next event loop turn after the current execution finishes.

It is useful for lightweight asynchronous follow-up work without a timer delay.

<h6>Syntax</h6>

```js
setImmediate(callback[, ...args])
```

<h6>Return value</h6>

- An immediate handle object. Pass it to `clearImmediate()` to cancel execution.

<h6>Usage example</h6>

```js
console.println("Add event loop");
setImmediate(() => {
    console.println("event loop called");
});

// Output:
// Add event loop
// event loop called
```

## clearImmediate()

Cancel a pending callback created by `setImmediate()` if it has not executed yet.

<h6>Syntax</h6>

```js
clearImmediate(immediate)
```

## console

The global `console` object provides log output and standard output helpers.

## console.log()

Write an info-level log message. The output includes the `INFO` level prefix.

<h6>Usage example</h6>

```js
console.log("Hello, World!");

// Output:
// INFO  Hello, World!
```

## console.debug()

Write a debug-level log message.

## console.info()

Write an info-level log message. It uses the same level as `console.log()`.

## console.warn()

Write a warning-level log message.

## console.error()

Write an error-level log message.

## console.print()

Write values without a trailing newline.

<h6>Usage example</h6>

```js
console.print("hello", "world");

// Output:
// helloworld
```

## console.println()

Write values separated by spaces and append a trailing newline.

<h6>Usage example</h6>

```js
console.println("hello", "world");

// Output:
// hello world
```

## console.printf()

Write formatted output using a format string.

<h6>Syntax</h6>

```js
console.printf(format, ...args)
```

<h6>Usage example</h6>

```js
console.printf("value=%d, name=%s\n", 42, "neo");

// Output:
// value=42, name=neo
```
