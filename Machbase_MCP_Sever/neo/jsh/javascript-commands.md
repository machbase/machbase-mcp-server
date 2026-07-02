# Machbase Neo JavaScript Commands

This page covers the default JSH commands grouped by user-facing purpose.

## Overview

This page groups commands by what they do for the user.

**Notes**

- These commands operate inside the JSH virtual filesystem by default, not directly on the host OS filesystem.
- Relative paths are resolved from the current JSH working directory.
- Some commands affect the active shell session directly, such as the current directory or environment variables.
- Some commands intentionally provide a smaller feature set than their Unix counterparts.

## Filesystem Commands

### cd

Changes the current working directory of the active JSH shell session.

<h6>Syntax</h6>

```sh
cd [directory]
```

If no argument is provided, `cd` moves to `$HOME`.
If the target path does not exist, it prints an error and returns a non-zero status.

<h6>Usage example</h6>

```sh
/work > cd subdir
/work/subdir >
/work/subdir > cd
/work >
```

### cat

Concatenates files to standard output.
It supports line numbering, visible line endings and tabs, blank-line squeezing, and syntax highlighting.

<h6>Syntax</h6>

```sh
cat [OPTION]... [FILE]...
```

<h6>Options</h6>

- `-n, --number` number all output lines
- `-E, --showEnds` display `$` at the end of each line
- `-T, --showTabs` display tab characters as `^I`
- `-s, --squeeze` suppress repeated empty lines
- `-c, --color` enable syntax highlighting
- `-h, --help` show help

With `-c`, syntax highlighting is available for `.js`, `.json`, `.ndjson`, `.sql`, `.csv`, `.yaml`, `.yml`, and `.toml`.

<h6>Usage example</h6>

```sh
/work > cat -n notes.txt
/work > cat -c script.js
/work > cat -sE log.txt
```

### ls

Lists directory contents.
By default it prints entries in columns and supports hidden entries, long listing mode, time sorting, recursion, and simple wildcards.

<h6>Syntax</h6>

```sh
ls [OPTION]... [PATH]...
```

<h6>Options</h6>

- `-l, --long` use a detailed listing view
- `-a, --all` include hidden entries
- `-t, --time` sort by modification time, newest first
- `-R, --recursive` list subdirectories recursively

Path arguments may include simple wildcard patterns such as `*` and `?`.

<h6>Usage example</h6>

```sh
/work > ls
/work > ls -la
/work > ls -t /lib
/work > ls -R src
/work > ls *.js
```

### mkdir

Creates one or more directories.

<h6>Syntax</h6>

```sh
mkdir [OPTION]... DIRECTORY...
```

<h6>Options</h6>

- `-p, --parents` create parent directories as needed
- `-v, --verbose` print a message for each created directory
- `-h, --help` show help

Without `-p`, creating an existing directory reports an error.

<h6>Usage example</h6>

```sh
/work > mkdir data
/work > mkdir -p logs/app/2026
/work > mkdir -pv build/output
```

### pwd

Prints the current working directory.

<h6>Syntax</h6>

```sh
pwd
```

<h6>Usage example</h6>

```sh
/work > pwd
/work
```

### rm

Removes files or directories.

<h6>Syntax</h6>

```sh
rm [OPTION]... FILE...
```

<h6>Options</h6>

- `-r, -R, --recursive` remove directories and their contents recursively
- `-d, --dir, --directory` remove empty directories
- `-f, --force` ignore nonexistent paths and missing operand errors
- `-v, --verbose` print a message for each removed path
- `-h, --help` show help

<h6>Usage example</h6>

```sh
/work > rm old.txt
/work > rm -rf cache
/work > rm -d empty-dir
/work > rm -fv temp.txt missing.txt
```

## Environment Commands

### env

Prints environment variables.
With no arguments it prints the full environment in sorted order. With one or more names, it prints only those variables.

<h6>Syntax</h6>

```sh
env [NAME]...
```

<h6>Usage example</h6>

```sh
/work > env
/work > env HOME PWD
```

### alias

Defines or displays command aliases in the current shell session.
With no arguments, `alias` prints the currently defined aliases in sorted order. `alias NAME` prints one alias.
`alias NAME COMMAND [ARG]...` defines an alias, and the alias is expanded from the command head of later input in the same shell session.

<h6>Syntax</h6>

```sh
alias
alias NAME
alias NAME COMMAND [ARG]...
```

<h6>Usage example</h6>

```sh
/work > alias ll ls -l
/work > ll
/work > alias
/work > alias ll
```

### setenv

Sets an environment variable in the current shell session.

<h6>Syntax</h6>

```sh
setenv NAME VALUE
setenv NAME=VALUE
```

Variable names must start with a letter or `_`, and may then contain letters, digits, or `_`.

<h6>Usage example</h6>

```sh
/work > setenv GREETING hello
/work > setenv MESSAGE='hello world'
```

### unsetenv

Removes an environment variable from the current shell session.

<h6>Syntax</h6>

```sh
unsetenv NAME
```

Invalid names or missing arguments produce a usage error.

<h6>Usage example</h6>

```sh
/work > unsetenv GREETING
```

## System Commands

### pkg

Manages JSH packages and project manifests.
For subcommands, options, and workflows, refer to the Package Manager documentation.

<h6>Syntax</h6>

```sh
pkg <command> [options] [args...]
```

### servicectl

Manages long-running JSH services through the service controller.
For subcommands, options, and service-management workflows, refer to the Service Manager documentation.

<h6>Syntax</h6>

```sh
servicectl [--controller=<addr>] <command> [args...]
```

**servicectl controller**

Shows and resets service-controller RPC runtime metrics.

<h6>Syntax</h6>

```sh
servicectl [--controller=<addr>] controller [metrics|get|reset]
```

<h6>Behavior</h6>

- `controller` and `controller metrics` are equivalent.
- `controller get` is an alias of `controller metrics`.
- `controller reset` resets cumulative counters and starts a new accumulation window.
- `high_water_mark_connections` records the historical peak of concurrent RPC connections since the last reset.

<h6>Usage example</h6>

```sh
servicectl controller metrics
servicectl controller reset
servicectl controller get
```

## Text And Utility Commands

### echo

Prints its arguments separated by spaces and terminates with a newline.

<h6>Syntax</h6>

```sh
echo [ARG]...
```

The current implementation does not support shell-style flags such as `-n` or escape-sequence interpretation.

<h6>Usage example</h6>

```sh
/work > echo hello world
hello world
```

### sleep

Waits for the specified number of seconds before returning.

<h6>Syntax</h6>

```sh
sleep [OPTION] <sec>
```

<h6>Options</h6>

- `-h, --help` show help

<h6>Usage example</h6>

```sh
/work > sleep 5
```

### tail

Outputs the last part of a file.
With `-f`, it continuously prints new content appended to the file.

<h6>Syntax</h6>

```sh
tail [OPTION]... <file>
```

<h6>Options</h6>

- `-n, --lines <N>` output the last N lines, default `10`
- `-f, --follow` follow the file as it grows; stops on `SIGINT` or `SIGTERM`
- `-h, --help` show help

<h6>Usage example</h6>

```sh
/work > tail app.log
/work > tail -n 20 app.log
/work > tail -f app.log
```

### viz

Views, validates, and exports vizspec documents(ADVN).
It is intended for renderer-neutral analysis output produced by JSH or Machbase Neo workflows.

<h6>Syntax</h6>

```sh
viz <command> [options] <file>
```

<h6>Subcommands</h6>

- `viz view [options] <file>` render an vizspec as TUI blocks
- `viz validate <file>` validate an vizspec file
- `viz export [options] <file>` export an vizspec to SVG

<h6>`view` options</h6>

- `--compact` hide series summary and raw data tables
- `--rows <n>` limit detail rows per block
- `--width <n>` control sparkline, bar, and timeline width
- `--verbose-meta` show block metadata
- pretty-table options are also accepted

<h6>`export` options</h6>

- `--format svg` export format, currently only `svg` is supported
- `-o, --output <file>` write the SVG to a file instead of standard output
- `--width <n>` SVG width in pixels
- `--height <n>` SVG height in pixels
- `--padding <n>` outer SVG padding in pixels
- `--title <text>` optional SVG title
- `--background <color>` SVG background color
- `--font-family <name>` SVG font family
- `--font-size <n>` SVG base font size in pixels
- `--hide-legend` suppress legend rendering

<h6>Usage example</h6>

```sh
/work > viz validate sensor-overview.json
/work > viz view --width 80 sensor-overview.json
/work > viz export --title "CPU Overview" --output cpu.svg sensor-overview.json
```

### wc

Counts lines, words, bytes, and characters for each file.
If no file is given, or if `-` is used, it reads standard input.

<h6>Syntax</h6>

```sh
wc [OPTION]... [FILE]...
```

<h6>Options</h6>

- `-l, --lines` print line counts
- `-w, --words` print word counts
- `-c, --bytes` print byte counts
- `-m, --chars` print character counts
- `-h, --help` show help

If no count option is selected, `wc` prints lines, words, and bytes.

<h6>Usage example</h6>

```sh
/work > wc notes.txt
/work > wc -l *.log
/work > cat notes.txt | wc -w -
```

### which

Prints where a command resolves in the JSH command path.

<h6>Syntax</h6>

```sh
which <command>
```

If the command cannot be found, `which` prints an error and returns a non-zero status.

<h6>Usage example</h6>

```sh
/work > which ls
/sbin/ls.js
```

## Messaging Commands

### mqtt_pub

Publishes a message to an MQTT broker.

<h6>Syntax</h6>

```sh
mqtt_pub [OPTION]...
```

<h6>Options</h6>

- `-t, --topic` topic to publish to
- `-b, --broker` broker address, default `tcp://localhost:5653`
- `-m, --message` inline message payload
- `-f, --file` file containing the payload
- `-q, --qos` MQTT QoS level, one of `0`, `1`, `2`
- `-d, --debug` print debug logs
- `-h, --help` show help

`-m` and `-f` are mutually exclusive.

<h6>Usage example</h6>

```sh
/work > mqtt_pub -t sensors/temp -m '{"value":21.5}'
/work > mqtt_pub -b tcp://broker:1883 -t logs/app -f payload.json -q 1
```

### nats_pub

Publishes a message to a NATS subject.
It can optionally wait for one reply by using an explicit reply subject or request mode.

<h6>Syntax</h6>

```sh
nats_pub [OPTION]...
```

<h6>Options</h6>

- `-t, --topic` subject to publish to
- `-s, --subject` alias for `--topic`
- `-b, --broker` broker address, default `nats://localhost:4222`
- `-m, --message` inline message payload
- `-f, --file` file containing the payload
- `-r, --reply` reply subject to wait on
- `--request` generate a temporary inbox subject and wait for one response
- `--timeout` connect and reply timeout in milliseconds, default `10000`
- `-d, --debug` print debug logs
- `-h, --help` show help

`-m` and `-f` are mutually exclusive.

<h6>Usage example</h6>

```sh
/work > nats_pub -t events.demo -m 'hello'
/work > nats_pub -s rpc.echo -m 'ping' --request
/work > nats_pub -s rpc.echo -m 'ping' -r reply.demo --timeout 3000
```

## Interactive Commands

### repl

Starts the JSH JavaScript REPL.
This is an interactive JavaScript evaluation environment rather than the command-oriented shell prompt.

<h6>Syntax</h6>

```sh
repl
```

### shell

Starts a new JSH shell session.
Use it when you want to enter a separate shell loop from the current process environment.

<h6>Syntax</h6>

```sh
shell
```
