# Machbase Neo JavaScript SplitFields Module

The `util/splitFields` module splits a string into fields using whitespace separators while preserving quoted substrings.

```js
const { splitFields } = require('util/splitFields');
```

## splitFields()

Splits a string into an array of field strings.

<h6>Syntax</h6>

```js
splitFields(input[, options])
```

<h6>Parameters</h6>

- `input` `String` the string to split
- `options` `Object` (currently unused)

<h6>Return value</h6>

`String[]` array of parsed fields.

<h6>Behavior</h6>

- Consecutive whitespace is treated as a single separator.
- Empty fields are omitted from the result.
- Quote characters are removed from the returned values.
- Tabs and newlines within quoted sections remain intact.
- Unclosed quotation marks continue consuming text until the string ends.
- Escape sequences within quotes receive no special interpretation.

<h6>Usage example</h6>

```js
const { splitFields } = require('util/splitFields');

console.println(splitFields('hello "world foo" bar'));
// ['hello', 'world foo', 'bar']

console.println(splitFields("hello 'world foo' bar"));
// ['hello', 'world foo', 'bar']

console.println(splitFields("a \"b c\" d 'e f' g"));
// ['a', 'b c', 'd', 'e f', 'g']
```

## Behavior notes

- The function is designed for shell-like tokenization when full command parsing is unnecessary.
- Both single and double quotes are supported.
