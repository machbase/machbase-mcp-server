# Machbase Neo JavaScript ParseArgs Module

The `util/parseArgs` module parses command-line style argument arrays for JSH applications.

```js
const { parseArgs } = require('util/parseArgs');
```

## parseArgs()

Parses an argument array with one or more configuration objects.

<h6>Syntax</h6>

```js
parseArgs(args, ...configs)
```

When multiple configs with `command` fields are provided, the parser matches `args[0]` to determine which configuration to use.

<h6>Configuration options</h6>

| Option | Type | Default | Description |
|:-------|:-----|:--------|:------------|
| `options` | Object | | Defines available flags and their types |
| `strict` | Boolean | `true` | Validates against unknown options |
| `allowPositionals` | Boolean | `false` | Permits positional arguments |
| `positionals` | Array | | Defines positional argument structure |
| `allowNegative` | Boolean | `false` | Enables `--no-` prefix for boolean flags |
| `tokens` | Boolean | `false` | Returns detailed token information |
| `command` | String | | Sub-command name for multi-config dispatch |

<h6>Option types</h6>

Supported types: `boolean`, `string`, `integer`, `float`.

Each option definition can include:
- `type` the option type
- `short` single-character short flag
- `default` default value
- `description` help description

The parser automatically converts camelCase names to kebab-case flags. For example, `maxRetryCount` maps to `--max-retry-count`.

<h6>Return value</h6>

Returns an object containing:
- `values` parsed option values
- `positionals` positional arguments in order
- `namedPositionals` named positional values (when configured)
- `tokens` token details (when `tokens: true`)
- `command` matched sub-command name (when applicable)

<h6>Usage example</h6>

```js
const { parseArgs } = require('util/parseArgs');

const result = parseArgs(['--name', 'Alice', '--verbose', 'file.txt'], {
    options: {
        name: { type: 'string', short: 'n' },
        verbose: { type: 'boolean', short: 'v' }
    },
    allowPositionals: true
});

console.println(result.values.name);     // Alice
console.println(result.values.verbose);  // true
console.println(result.positionals[0]);  // file.txt
```

## parseArgs.formatHelp()

Generates human-readable help documentation from configuration structures.

<h6>Syntax</h6>

```js
parseArgs.formatHelp(config)
```

## parseArgs.toKebabCase()

Converts camelCase to kebab-case format.

<h6>Syntax</h6>

```js
parseArgs.toKebabCase(name)
```

## Behavior notes

- `integer` rejects values that contain a decimal point.
- Both `integer` and `float` types return JavaScript numbers.
- The parser supports option terminator `--` and boolean grouping like `-abc`.
- Unknown options raise an error when `strict` is `true`.
