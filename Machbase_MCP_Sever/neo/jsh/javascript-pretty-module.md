# Machbase Neo JavaScript Pretty Module

The `pretty` module formats values and renders terminal-friendly output for JSH applications. It is useful when you need readable tables, human-friendly byte and duration strings, or progress indicators for long-running jobs.

```js
const pretty = require('pretty');
```

## Table()

Creates a table writer.

<h6>Syntax</h6>

```js
Table(config)
```

<h6>Common options</h6>

| Option | Type | Description | Default |
| --- | --- | --- | --- |
| `format` | `String` | Output format: `box`, `csv`, `tsv`, `json`, `ndjson`, `html`, `md` | `box` |
| `boxStyle` | `String` | Box style: `light`, `double`, `bold`, `rounded`, `simple`, `compact` | `light` |
| `rownum` | `Boolean` | Include a leading `ROWNUM` column | `true` |
| `timeformat` | `String` | Datetime format | `default` |
| `tz` | `String` | Timezone: `local`, `UTC`, or IANA timezone name | `local` |
| `precision` | `Number` | Round floating-point values when `0` or greater | `-1` |
| `header` | `Boolean` | Show header row | `true` |
| `footer` | `Boolean` | Show footer or caption | `true` |
| `nullValue` | `String` | String used for null values | `NULL` |
| `stringEscape` | `Boolean` | Escape non-printable characters as `\uXXXX` | `false` |

<h6>Important methods</h6>

- `appendHeader(values)` append the header row
- `appendRow(row)` append one row
- `appendRows(rows)` append multiple rows
- `append(values)` append a row or rows
- `row(...values)` create a row with table value transformation
- `render()` return the current rendered output as a string
- `close()` flush the remaining rows and return the last rendered output
- `resetRows()` clear buffered rows

<h6>Usage example: basic box table</h6>

```js
const pretty = require('pretty');
const tw = pretty.Table({ boxStyle: 'light' });
tw.appendHeader(['Name', 'Age']);
tw.appendRow(tw.row('Alice', 30));
tw.appendRow(tw.row('Bob', 25));
console.println(tw.render());
```

Output:

```text
┌────────┬───────┬─────┐
│ ROWNUM │ NAME  │ AGE │
├────────┼───────┼─────┤
│      1 │ Alice │  30 │
│      2 │ Bob   │  25 │
└────────┴───────┴─────┘
```

<h6>Usage example: JSON output</h6>

```js
const pretty = require('pretty');
const tw = pretty.Table({ format: 'json', rownum: false });
tw.appendHeader(['ID', 'Status', 'Value']);
tw.append([1, 'active', 42.5]);
tw.append([2, 'pending', 31.2]);
console.println(tw.render());
```

<h6>Usage example: CSV output</h6>

```js
const pretty = require('pretty');
const tw = pretty.Table({ format: 'csv', rownum: false });
tw.appendHeader(['Name', 'Score']);
tw.append(['Alice', 98]);
tw.append(['Bob', 87]);
console.println(tw.render());
```

## Progress()

Creates a progress writer for terminal output.

<h6>Syntax</h6>

```js
Progress(options)
```

<h6>Options</h6>

- `showPercentage` `Boolean` show percentage, default `true`
- `showETA` `Boolean` show estimated remaining time, default `true`
- `showSpeed` `Boolean` show processing speed, default `true`
- `updateFrequency` `Number` refresh interval in milliseconds, default `250`
- `trackerLength` `Number` progress bar width, default `20`

<h6>Usage example</h6>

```js
const pretty = require('pretty');
const pw = pretty.Progress({ showPercentage: true, showETA: true });
const tracker = pw.tracker({ message: 'Processing', total: 100 });

let interval = setInterval(function() {
    tracker.increment(10);
    if (tracker.value() >= 100) {
        tracker.markAsDone();
        clearInterval(interval);
    }
}, 200);
```

## Bytes()

Formats byte counts as human-readable strings.

```js
pretty.Bytes(512);       // "512B"
pretty.Bytes(1536);      // "1.5KB"
pretty.Bytes(1048576);   // "1.0MB"
pretty.Bytes(1073741824);// "1.0GB"
```

## Ints()

Formats integers with grouping separators.

```js
pretty.Ints(1234567890); // "1,234,567,890"
```

## Durations()

Formats durations from nanoseconds into short readable strings.

```js
pretty.Durations(1234);           // "1.23μs"
pretty.Durations(2340000);        // "2.34ms"
pretty.Durations(3010000000);     // "3.01s"
pretty.Durations(3661000000000);  // "1h 1m"
pretty.Durations(86400000000000); // "1d 0h"
```

## Terminal helpers

- `isTerminal()` returns whether stdin is attached to a terminal
- `getTerminalSize()` returns terminal width and height
- `pauseTerminal()` waits for a key press
- `parseTime(value, format, tz)` parses text into a time value
