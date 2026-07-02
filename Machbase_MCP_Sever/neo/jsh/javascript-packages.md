# Machbase Neo JavaScript Packages

The `pkg` command manages `package.json`, installs JSH packages, and runs package scripts.
It is intended for JSH applications that keep their dependencies in a project directory such as `/work`.

## Overview

The `pkg` command supports these tasks:

- Create a new `package.json`
- Install dependencies into `node_modules`
- Copy a GitHub project into a destination directory and install its project dependencies in place
- Maintain `package-lock.json`
- Run commands defined in `package.json` `scripts`
- Generate executable wrappers from installed package `bin` entries
- Remove dependencies together with generated wrappers

## package.json

`pkg` treats `package.json` as the manifest of the selected package root.
For a normal project install, that root is the current directory or the directory selected by `--dir`.
For `pkg install -g` and `pkg uninstall -g`, packages are installed under `/work/node_modules`, but `pkg` does not create `/work/package.json` or `/work/package-lock.json`.

A minimal project manifest looks like this.

```json
{
  "name": "demo-app",
  "version": "1.0.0",
  "scripts": {
    "start": "./main.js"
  },
  "dependencies": {
    "generic-pkg": "^1.2.0",
    "github.com/acme/demo": "#tag=v1.1.0"
  }
}
```

Common fields used by `pkg` are:

| Field | Type | Description |
| --- | --- | --- |
| `name` | `String` | Project package name |
| `version` | `String` | Project version |
| `scripts` | `Object` | Named command lines for `pkg run` |
| `dependencies` | `Object` | Package name to version specifier map |

## pkg init

Creates a new `package.json` in the current project directory.

<h6>Syntax</h6>

```sh
pkg init [options] <name>
```

<h6>Options</h6>

- `-C, --dir <dir>` use the given project directory instead of the current working directory
- `-h, --help` show help

<h6>Usage example</h6>

```sh
/work > pkg init demo-app
Created /work/package.json
```

## pkg install

Installs dependencies from `package.json`, or installs a single package request and updates both
`package.json` and `package-lock.json`.

<h6>Syntax</h6>

```sh
pkg install [options] [name]
```

<h6>Options</h6>

- `-C, --dir <dir>` use the given project directory instead of the current working directory
- `-g, --global` install into the global package directory and ignore `--dir`
- `-h, --help` show help

If `name` is omitted, `pkg install` installs the dependencies already declared in the selected project manifest.

### Global install

`pkg install -g <name>` uses `/work/node_modules` as the installation target.

### npm packages

If the package name is not a GitHub repository path, `pkg` installs it from the npm registry.

```sh
/work > pkg install generic-pkg
Installed generic-pkg@1.2.0
```

### GitHub repository packages

If the package name matches `github.com/<org>/<repo>`, `pkg` installs the repository contents directly from GitHub.

Supported forms are:

- `github.com/<org>/<repo>`
- `github.com/<org>/<repo>@<tag>`
- `github.com/<org>/<repo>#tag=<tag>`
- `github.com/<org>/<repo>#branch=<branch>`

Behavior:

- If `@<tag>` or `#tag=<tag>` is specified, that tag is used.
- If `#branch=<branch>` is specified, that branch is used even if the repository also has tags.
- If no tag is specified and the repository has tags, the latest tag returned by the GitHub tags API is used.
- If no tag is specified and the repository has no tags, the repository `default_branch` is used.

<h6>Usage example</h6>

```sh
/work > pkg install github.com/acme/demo
Installed github.com/acme/demo#tag=v1.1.0
```

## pkg copy

Copies a GitHub repository package into the requested destination directory instead of installing the repository itself under `node_modules`.
After copying the project files, `pkg copy` installs dependencies in the copied project root and, when present, in `cgi-bin`.

<h6>Syntax</h6>

```sh
pkg copy [options] <source> <dest>
```

<h6>Options</h6>

- `-f, --force` continue even if the destination directory already exists and is not empty
- `-h, --help` show help

<h6>Usage example</h6>

```sh
/work > pkg copy github.com/acme/helloapp public/hello
Copying github.com/acme/helloapp#branch=main to /work/public/hello
Installing dependencies in /work/public/hello
Installing dependencies in /work/public/hello/cgi-bin
```

## pkg run

Runs a named entry from `package.json` `scripts`.

<h6>Syntax</h6>

```sh
pkg run [options] <key> [...args]
```

<h6>Options</h6>

- `-C, --dir <dir>` use the given project directory instead of the current working directory
- `-h, --help` show help

`pkg run` changes the current working directory to the selected project directory before executing the script.

<h6>Usage example</h6>

```sh
/work > pkg run start
```

## pkg uninstall

Removes a dependency together with its generated wrappers.

<h6>Syntax</h6>

```sh
pkg uninstall [options] <name>
```

<h6>Options</h6>

- `-C, --dir <dir>` use the given project directory instead of the current working directory
- `-g, --global` remove the package from `/work/node_modules` and ignore `--dir`
- `-h, --help` show help

<h6>Usage example</h6>

```sh
/work > pkg uninstall github.com/acme/demo
Removed github.com/acme/demo
```

## Typical workflow

```sh
/work > pkg init demo-app
/work > pkg install github.com/acme/demo
/work > pkg install generic-pkg
/work > pkg run start
```

## Notes

- `pkg` expects a valid `package.json` for `install` without an explicit package name and for `run`.
- `pkg run` executes the script line through JSH command resolution, not through a POSIX shell.
- Relative script commands such as `./tool.js` are recommended for project-local executables.
