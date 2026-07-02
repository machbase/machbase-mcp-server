# Machbase Neo IP Address and ports

## Bind Address

machbase-neo runs and listens to only localhost by default for the security reason. If clients on the remote hosts need to read/write data from/to machbase-neo through network, it requires that machbase-neo starts with bind address option `--host <bind address>`.

To allow listening from all addresses, use `0.0.0.0`

```sh
machbase-neo serve --host 0.0.0.0
```

To allow listening from specific address, set the IP address of the host.

```sh
machbase-neo serve --host 192.168.1.10
```

## Listening Ports

There are more flag options for the protocol ports.

| flag             | default          | desc                            |
|:-----------------|:----------------:|-------------------------------- |
| `--shell-port`   | `5652`           | ssh listen port                 |
| `--mqtt-port`    | `5653`           | mqtt listen port                |
| `--http-port`    | `5654`           | http listen port                |
| `--mach-port`    | `5656`           | machbase native listen port for JDBC/ODBC drivers |

If a listener requires to listen different network interface, use listen host and port flags.

| flag                   | default                | desc                            |
|:-----------------------|:-----------------------|-------------------------------- |
| `--mach-listen-host`   | value of `--host`      |                                 |
| `--mach-listen-port`   | value of `--mach-port` |                                 |
| `--shell-listen-host`  | value of `--host`      |                                 |
| `--shell-listen-port`  | value of `--shell-port`|                                 |
| `--http-listen-host`   | value of `--host`      |                                 |
| `--http-listen-port`   | value of `--http-port` |                                 |
| `--mqtt-listen-host`   | value of `--host`      |                                 |
| `--mqtt-listen-port`   | value of `--mqtt-port` |                                 |