# Machbase Neo JavaScript Path Module

The `path` module provides path manipulation utilities similar to Node.js for JSH applications.

The default export is POSIX-oriented, using `/` as the separator and `:` as the delimiter.
`path.posix` and `path.win32` namespaces are available for explicit behavior control.

```js
const path = require('path');
```

## resolve()

Resolves a sequence of paths into an absolute path.

<h6>Syntax</h6>

```js
path.resolve([...paths])
```

## normalize()

Resolves `.` and `..` segments and normalizes path separators.

<h6>Syntax</h6>

```js
path.normalize(p)
```

## isAbsolute()

Determines if a path is absolute.

<h6>Syntax</h6>

```js
path.isAbsolute(p)
```

## join()

Joins path segments using the active path style and normalizes the result.

<h6>Syntax</h6>

```js
path.join(...paths)
```

## relative()

Calculates the relative path from one location to another.

<h6>Syntax</h6>

```js
path.relative(from, to)
```

## dirname()

Extracts the directory portion of a path.

<h6>Syntax</h6>

```js
path.dirname(p)
```

## basename()

Returns the last path component, optionally removing a suffix.

<h6>Syntax</h6>

```js
path.basename(p[, ext])
```

## extname()

Returns the file extension including the leading dot.

<h6>Syntax</h6>

```js
path.extname(p)
```

## parse()

Breaks a path into structured components.

<h6>Syntax</h6>

```js
path.parse(p)
```

<h6>Return value</h6>

Returns an object with `root`, `dir`, `base`, `ext`, `name`.

## format()

Reconstructs a path from a parsed object.

<h6>Syntax</h6>

```js
path.format(pathObject)
```

## sep

The platform path separator. Default: `/`.

## delimiter

The platform path delimiter. Default: `:`.

## posix / win32

Explicit POSIX or Windows path handling namespaces.
`path.win32` is available for Windows path handling even when JSH is running on a non-Windows system.

## Usage example

```js
const path = require('path');

console.println(path.join('/work', 'data', 'file.txt'));  // /work/data/file.txt
console.println(path.dirname('/work/data/file.txt'));      // /work/data
console.println(path.basename('/work/data/file.txt'));     // file.txt
console.println(path.extname('file.txt'));                 // .txt
console.println(path.isAbsolute('/work'));                 // true

const parsed = path.parse('/work/data/file.txt');
console.println(parsed.dir, parsed.name, parsed.ext);     // /work/data file .txt
```

## Behavior notes

- All public functions require string arguments where applicable and throw `TypeError` for invalid input.
- The default JSH export is POSIX-oriented.
