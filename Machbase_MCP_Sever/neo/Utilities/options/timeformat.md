---
title: timeformat
type: docs
weight: 10
---

## Available time formats

The value of `timeformat` is *case-insensitive*.

| timeformat    |  result                             |
|:------------- |:------------------------------------|
| `DEFAULT`     | 2006-01-02 15:04:05.999             |
| `DEFAULT_MS`  | 2006-01-02 15:04:05.999             |
| `DEFAULT_US`  | 2006-01-02 15:04:05.999999          |
| `DEFAULT_NS`  | 2006-01-02 15:04:05.999999999       |
| `DEFAULT.MS`  | 2006-01-02 15:04:05.000             |
| `DEFAULT.US`  | 2006-01-02 15:04:05.000000          |
| `DEFAULT.NS`  | 2006-01-02 15:04:05.000000000       |
| `Numeric`     | 01/02 03:04:05PM '06 -0700          |
| `Ansic`       | Mon Jan _2 15:04:05 2006            |
| `Unix`        | Mon Jan _2 15:04:05 MST 2006        |
| `Ruby`        | Mon Jan 02 15:04:05 -0700 2006      |
| `RFC822`      | 02 Jan 06 15:04 MST                 |
| `RFC822Z`     | 02 Jan 06 15:04 -0700               |
| `RFC850`      | Monday, 02-Jan-06 15:04:05 MST      |
| `RFC1123`     | Mon, 02 Jan 2006 15:04:05 MST       |
| `RFC1123Z`    | Mon, 02 Jan 2006 15:04:05 -0700     |
| `RFC3339`     | 2006-01-02T15:04:05Z07:00           |
| `RFC3339Nano` | 2006-01-02T15:04:05.999999999Z07:00 |
| `Kitchen`     | 3:04:05PM                           |
| `Stamp`       | Jan _2 15:04:05                     |
| `StampMilli`  | Jan _2 15:04:05.000                 |
| `StampMicro`  | Jan _2 15:04:05.000000              |
| `StampNano`   | Jan _2 15:04:05.000000000           |
| `S_NS`        | 05.999999999                        |
| `S_US`        | 05.999999                           |
| `S_MS`        | 05.999                              |
| `S.NS`        | 05.000000000                        |
| `S.US`        | 05.000000                           |
| `S.MS`        | 05.000                              |

Unix epoch timeformat. {{< neo_since ver="8.0.40" />}}

| timeformat    |  result                             |
|:------------- |:------------------------------------|
| `ns`          | unix epoch time in nano-seconds     |
| `ns.str`      | string type instead of number       |
| `us`          | unix epoch time in micro-seconds    |
| `us.str`      | string type instead of number       |
| `ms`          | unix epoch time in milli-seconds    |
| `ms.str`      | string type instead of number       |
| `s`           | unix epoch time in seconds          |
| `s.str`       | string type instead of number       |

## Examples

### Select in Default Time

**Request**

Set query param `timeformat=Default`

```sh
 curl -o - http://127.0.0.1:5654/db/query      \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=box"              \
    --data-urlencode "timeformat=Default"
```

**Response**

```
+----------+-------------------------+----------+
| NAME     | TIME                    | VALUE    |
+----------+-------------------------+----------+
| wave.sin | 2023-02-15 03:39:21     | 0.111111 |
| wave.sin | 2023-02-15 03:39:22.111 | 0.222222 |
| wave.sin | 2023-02-15 03:39:23.222 | 0.333333 |
| wave.sin | 2023-02-15 03:39:24.333 | 0.444444 |
| wave.sin | 2023-02-15 03:39:25.444 | 0.555555 |
+----------+-------------------------+----------+
```

### Select rows in default time format with `Asia/Seoul`

**Request**
Set query param `timeformat=Default` and `tz=Asia/Seoul`

```sh
 curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=box"              \
    --data-urlencode "timeformat=Default"      \
    --data-urlencode "tz=Asia/Seoul"
```

**Response**

```
 +----------+-------------------------+----------+
| NAME     | TIME                    | VALUE    |
+----------+-------------------------+----------+
| wave.sin | 2023-02-15 12:39:21     | 0.111111 |
| wave.sin | 2023-02-15 12:39:22.111 | 0.222222 |
| wave.sin | 2023-02-15 12:39:23.222 | 0.333333 |
| wave.sin | 2023-02-15 12:39:24.333 | 0.444444 |
| wave.sin | 2023-02-15 12:39:25.444 | 0.555555 |
+----------+-------------------------+----------+
```

### Select rows in `RFC3339`

**Request**

Set query param `timeformat=Default`

```sh
 curl -o - http://127.0.0.1:5654/db/query      \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=box"              \
    --data-urlencode "timeformat=RFC3339"
```

**Response**

```
+----------+----------------------+----------+
| NAME     | TIME                 | VALUE    |
+----------+----------------------+----------+
| wave.sin | 2023-02-15T03:39:21Z | 0.111111 |
| wave.sin | 2023-02-15T03:39:22Z | 0.222222 |
| wave.sin | 2023-02-15T03:39:23Z | 0.333333 |
| wave.sin | 2023-02-15T03:39:24Z | 0.444444 |
| wave.sin | 2023-02-15T03:39:25Z | 0.555555 |
+----------+----------------------+----------+
```

### Select in RFC3339 with Nano precision

**Request**

Set query param `timeformat=Default`

```sh
 curl -o - http://127.0.0.1:5654/db/query      \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=box"              \
    --data-urlencode "timeformat=RFC3339Nano"
```

**Response**

```
 +----------+--------------------------------+----------+
| NAME     | TIME                           | VALUE    |
+----------+--------------------------------+----------+
| wave.sin | 2023-02-15T03:39:21Z           | 0.111111 |
| wave.sin | 2023-02-15T03:39:22.111111111Z | 0.222222 |
| wave.sin | 2023-02-15T03:39:23.222222322Z | 0.333333 |
| wave.sin | 2023-02-15T03:39:24.333333233Z | 0.444444 |
| wave.sin | 2023-02-15T03:39:25.444444444Z | 0.555555 |
+----------+--------------------------------+----------+
```

### Select in RFC3339 with Nano precision in America/New_York Time Zone

**Request**

Set query param `timeformat=Default`

```sh
 curl -o - http://127.0.0.1:5654/db/query      \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=box"              \
    --data-urlencode "timeformat=RFC3339Nano"  \
    --data-urlencode "tz=America/New_York"
```

**Response**

```
+----------+-------------------------------------+----------+
| NAME     | TIME                                | VALUE    |
+----------+-------------------------------------+----------+
| wave.sin | 2023-02-14T22:39:21-05:00           | 0.111111 |
| wave.sin | 2023-02-14T22:39:22.111111111-05:00 | 0.222222 |
| wave.sin | 2023-02-14T22:39:23.222222222-05:00 | 0.333333 |
| wave.sin | 2023-02-14T22:39:24.333333333-05:00 | 0.444444 |
| wave.sin | 2023-02-14T22:39:25.444444444-05:00 | 0.555555 |
+----------+-------------------------------------+----------+
```

### Select in Custom Time Format

In Machbase Neo Rest API, specific numbers are used to replace the format of certain time.
Set query param `timeformat=<custom-format-as-below>`

```bash
 custom format
      year           2006
      month          01
      day            02
      hour           03 or 15
      minute         04
      second         05 or with sub-seconds '05.999999999'
```

### Typical Custom Time Format

**Request**

```sh
 curl -o - http://127.0.0.1:5654/db/query      \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=box"              \
    --data-urlencode "timeformat=2006-01-02 03:04:05.999999999"
```

**Response**
```
+----------+-------------------------------+----------+
| NAME     | TIME                          | VALUE    |
+----------+-------------------------------+----------+
| wave.sin | 2023-02-15 03:39:21           | 0.111111 |
| wave.sin | 2023-02-15 03:39:22.111111111 | 0.222222 |
| wave.sin | 2023-02-15 03:39:23.222222222 | 0.333333 |
| wave.sin | 2023-02-15 03:39:24.333333333 | 0.444444 |
| wave.sin | 2023-02-15 03:39:25.444444444 | 0.555555 |
+----------+-------------------------------+----------+
```

### Typical Re-ordered Custom Time Format

**Request**

```sh
 curl -o - http://127.0.0.1:5654/db/query      \
    --data-urlencode "q=select * from EXAMPLE" \
    --data-urlencode "format=box"              \
    --data-urlencode "timeformat=03:04:05.999999999-ReOrder-2006-01-02 "
```

**Response**

```
+----------+----------------------------------------+----------+
| NAME     | TIME                                   | VALUE    |
+----------+----------------------------------------+----------+
| wave.sin | 03:39:21-ReOrder-2023-02-15            | 0.111111 |
| wave.sin | 03:39:22.111111111-ReOrder-2023-02-15  | 0.222222 |
| wave.sin | 03:39:23.222222222-ReOrder-2023-02-15  | 0.333333 |
| wave.sin | 03:39:24.333333333-ReOrder-2023-02-15  | 0.444444 |
| wave.sin | 03:39:25.444444444-ReOrder-2023-02-15  | 0.555555 |
+----------+----------------------------------------+----------+
```

### Typical Re-ordered Custom Time Format in America/New_York Time Zone

**Request**

```sh
 curl -o - http://127.0.0.1:5654/db/query                                 \
    --data-urlencode "q=select * from EXAMPLE"                            \
    --data-urlencode "format=box"                                         \
    --data-urlencode "timeformat=03:04:05.999999999-ReOrder-2006-01-02 "  \
    --data-urlencode "tz=America/New_York"
```

**Response**

```
+----------+----------------------------------------+----------+
| NAME     | TIME                                   | VALUE    |
+----------+----------------------------------------+----------+
| wave.sin | 10:39:21-ReOrder-2023-02-14            | 0.111111 |
| wave.sin | 10:39:22.111111111-ReOrder-2023-02-14  | 0.222222 |
| wave.sin | 10:39:23.222222222-ReOrder-2023-02-14  | 0.333333 |
| wave.sin | 10:39:24.333333333-ReOrder-2023-02-14  | 0.444444 |
| wave.sin | 10:39:25.444444444-ReOrder-2023-02-14  | 0.555555 |
+----------+----------------------------------------+----------+
```
