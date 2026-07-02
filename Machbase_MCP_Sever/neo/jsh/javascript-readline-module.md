# Machbase Neo JavaScript Readline Module

The `readline` module provides interactive line input for JSH applications.
It exposes a single `ReadLine` class backed by the native JSH readline implementation.

```js
const { ReadLine } = require('readline');
```

## ReadLine

Creates an interactive line reader.

<h6>Syntax</h6>

```js
new ReadLine([options])
```

<h6>Options</h6>

| Option | Type | Default | Description |
|:-------|:-----|:--------|:------------|
| history | String | `readline` | History file name stored under the JSH config directory. |
| prompt | Function | built-in prompt | Callback that returns the prompt string for each line. |
| submitOnEnterWhen | Function | always submit | Callback that decides whether Enter submits the current input. |
| autoInput | String[] | | Input sequence used mainly for automated testing. |

## readLine()

Reads one logical input value.

- If the input is single-line, the result is a single string.
- If multi-line input is accepted, the result joins lines with `\n`.
- When the native reader ends with an error, JSH returns an `Error` object.

<h6>Syntax</h6>

```js
reader.readLine([options])
```

<h6>Usage example</h6>

```js
const { ReadLine } = require('readline');

const reader = new ReadLine({
    prompt: () => 'input> ',
});
const line = reader.readLine();
if (line instanceof Error) {
    throw line;
}
console.println(line);
```

## addHistory()

Adds a line to readline history.

<h6>Syntax</h6>

```js
reader.addHistory(line)
```

If the same line already exists, the previous entry is removed and the new one is appended at the end.

## close()

Closes the current readline session.

If `close()` is called while `readLine()` is waiting for input, the pending call ends with `EOF`.

## prompt option

`prompt` generates the prompt string for each line.

```js
prompt(lineno) => string
```

- `lineno` is zero-based.

<h6>Usage example</h6>

```js
const reader = new ReadLine({
    prompt: (lineno) => lineno === 0 ? 'sql> ' : '...> ',
});
```

## submitOnEnterWhen option

Controls whether pressing Enter submits the current input or continues multi-line editing.

```js
submitOnEnterWhen(lines, idx) => boolean
```

<h6>Usage example</h6>

```js
const reader = new ReadLine({
    submitOnEnterWhen: (lines, idx) => {
        return lines[idx].endsWith(';');
    },
});
```

## autoInput option

Feeds predefined input into the reader. Mainly useful for tests and non-interactive scripts.

```js
const reader = new ReadLine({
    autoInput: ['Hello World', ReadLine.CtrlJ],
});
```

## Multi-line input example

```js
const { ReadLine } = require('readline');

const reader = new ReadLine({
    autoInput: ['select *', ReadLine.Enter, 'from dual;', ReadLine.Enter],
    submitOnEnterWhen: (lines, idx) => {
        return lines[idx].endsWith(';');
    },
});
const text = reader.readLine();
console.println(text);
```

## Static key constants

`ReadLine` exposes key constants for simulated input:

- Control keys: `CtrlA` ... `CtrlZ`, `CtrlLeft`, `CtrlRight`, `CtrlUp`, `CtrlDown`
- Navigation keys: `Up`, `Down`, `Left`, `Right`, `Home`, `End`, `PageUp`, `PageDown`
- Editing keys: `Backspace`, `Delete`, `Enter`, `ShiftTab`, `Escape`
- Alt keys: `AltA` ... `AltZ`, `ALTBackspace`
- Function keys: `F1` ... `F24`

## Behavior notes

- The module uses callback-free synchronous reads. `readLine()` returns the completed value directly.
- `readLine()` can return an `Error` object, so callers should check `line instanceof Error`.
- `close()` is primarily useful for canceling a pending read from another timer or event.
