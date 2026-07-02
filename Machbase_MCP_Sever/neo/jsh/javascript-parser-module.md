# Machbase Neo JavaScript Parser Module

The `parser` module provides streaming decoders for CSV and NDJSON data.
It is designed for use with JSH streams and emits parsed objects through events.

```js
const parser = require('parser');
```

## Exported members

- `csv(options)`
- `ndjson(options)`
- `CSVParser`
- `NDJSONParser`

## csv()

Creates a CSV parser stream.

<h6>Syntax</h6>

```js
parser.csv([options])
```

<h6>Options</h6>

| Option | Type | Default | Description |
|:-------|:-----|:--------|:------------|
| `separator` | String | `,` | Field separator |
| `quote` | String | `"` | Quote character |
| `escape` | String | same as `quote` | Escape character used for escaped quotes |
| `headers` | `true` / `false` / `String[]` | `true` | Header handling mode |
| `skipLines` | Number | `0` | Number of initial lines to ignore |
| `skipComments` | Boolean \| String | `false` | Skip comment lines |
| `strict` | Boolean | `false` | Fail when a row has a different column count |
| `mapHeaders` | Function | | Maps header names |
| `mapValues` | Function | | Maps field values before row emission |
| `trimLeadingSpace` | Boolean | `true` | Trim leading spaces from each field |

<h6>Return value</h6>

Returns a `CSVParser` instance.

## CSVParser

<h6>Events</h6>

- `headers`: emitted once after the header row is parsed
- `data`: emitted for each parsed row object
- `error`: emitted when strict parsing fails
- `end`: emitted when the upstream stream finishes

<h6>Properties</h6>

- `bytesWritten`: number of input bytes received
- `bytesRead`: number of bytes consumed by the parser

<h6>Row shape</h6>

- When `headers` is omitted or `true`, the first non-skipped line becomes the header row.
- When `headers` is `false`, fields are exposed as `"0"`, `"1"`, `"2"`, ...
- When `headers` is an array, those names are used and the first line is treated as data.

## ndjson()

Creates an NDJSON parser stream.

<h6>Syntax</h6>

```js
parser.ndjson([options])
```

<h6>Options</h6>

| Option | Type | Default | Description |
|:-------|:-----|:--------|:------------|
| `strict` | Boolean | `true` | Fail on invalid JSON lines instead of skipping them |

## NDJSONParser

<h6>Events</h6>

- `data`: emitted for each parsed JSON object
- `warning`: emitted for invalid lines when `strict: false`
- `error`: emitted when strict parsing fails
- `end`: emitted when the upstream stream finishes

`warning` event objects contain `line`, `data`, and `error`.

## CSV example

```js
const fs = require('fs');
const parser = require('parser');

fs.createReadStream('/work/sample.csv')
    .pipe(parser.csv({
        headers: true,
        mapValues: ({ header, value }) => header === 'age' ? parseInt(value, 10) : value,
    }))
    .on('headers', (headers) => {
        console.println(headers.join(','));
    })
    .on('data', (row) => {
        console.println(row.name, row.age);
    });
```

## NDJSON example

```js
const fs = require('fs');
const parser = require('parser');

fs.createReadStream('/work/sample.ndjson')
    .pipe(parser.ndjson({ strict: false }))
    .on('data', (obj) => {
        console.println(obj.id);
    })
    .on('warning', (warn) => {
        console.println('Skipped line:', warn.line);
    });
```

## Behavior notes

- Both parser classes extend the JSH `stream.Transform` implementation.
- Parsed rows and objects are emitted through `data` events.
- Empty lines are ignored by both parsers.
- `NDJSONParser` trims each line before parsing.
- `CSVParser` removes a trailing `\r` so `\r\n` input is handled correctly.
