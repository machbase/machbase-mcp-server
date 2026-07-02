# Machbase Neo JavaScript Semver Module

The `semver` module provides semantic version comparison helpers for JSH applications.

```js
const semver = require('semver');
```

## satisfies()

Checks whether a version matches a semantic version constraint.

<h6>Syntax</h6>

```js
semver.satisfies(version, constraint)
```

<h6>Return value</h6>

Returns `true` when `version` satisfies `constraint`, otherwise `false`.
An empty constraint and `latest` are treated as `*`.

## maxSatisfying()

Returns the highest version that satisfies a constraint.

<h6>Syntax</h6>

```js
semver.maxSatisfying(versions, constraint)
```

<h6>Parameters</h6>

- `versions` `String[]`
- `constraint` `String`

<h6>Return value</h6>

Returns the original version string of the best match.
If no version matches, an empty string is returned. Invalid candidate versions are skipped.

## compare()

Compares two semantic versions.

<h6>Syntax</h6>

```js
semver.compare(left, right)
```

<h6>Return value</h6>

- `-1` if `left < right`
- `0` if `left === right`
- `1` if `left > right`

## Usage example

```js
const semver = require('semver');

console.println(semver.satisfies('1.4.2', '1.2 - 1.4'));
console.println(semver.satisfies('2.0.0', '1.2 - 1.4'));
console.println(semver.maxSatisfying(['1.2.0', '1.4.2', '2.0.0'], '1.2 - 1.4'));
console.println(semver.maxSatisfying(['1.0.0', '1.1.4', '1.2.0'], '~1.1'));
console.println(semver.compare('1.1.0', '1.2.0'));
console.println(semver.compare('1.2.0', '1.1.0'));
console.println(semver.compare('1.2.0', '1.2.0'));
```

## Behavior notes

- Invalid `version`, `left`, `right`, or `constraint` values raise an error.
- Leading and trailing spaces are trimmed before parsing.
- Constraint parsing follows semantic version rules including range expressions such as `1.2 - 1.4` and `~1.1`.
