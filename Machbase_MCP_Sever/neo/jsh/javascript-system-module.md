# Machbase Neo JavaScript System Module

## now()

현재 프로세스의 프로세스 id를 가져옵니다.

**문법**

```js
now()
```

**파라미터**

None.

**반환값**

현재 시각을 네이티브 객체로 반환합니다.

**사용 예제**

```js
const m = require("@jsh/system")
console.log("now =", m.now())
```

## parseTime()

**문법**

```js
parseTime(epoch, epoch_format)
parseTime(datetime, format)
parseTime(datetime, format, location)
```

**파라미터**

- `epoch` `Number`
- `epoch_format` `String` "s", "ms", "us", "ns"
- `datetime` `String`
- `format` `String`
- `location` `Location` 시간대. 생략하면 기본값은 'Local'입니다. 예: system.location('EST'), system.location('America/New_York')

**반환값**

시각을 네이티브 객체로 반환

**사용 예제**

```js
const {println} = require("@jsh/process");
const system = require("@jsh/system");
ts = system.parseTime(
    "2023-10-01 12:00:00",
    "2006-01-02 15:04:05",
    system.location("UTC"));
println(ts.In(system.location("UTC")).Format("2006-01-02 15:04:05"));

// 2023-10-01 12:00:00
```

## location()

**문법**

```js
location(timezone)
```

**파라미터**

- `timezone` `String` time zone, e.g. `"UTC"`, `"Local"`, `"GMT"`, `"ETS"`, `"America/New_York"`...

**반환값**

위치를 네이티브 객체로 반환

**사용 예제**

```js
const {println} = require("@jsh/process");
const system = require("@jsh/system");
ts = system.time(1).In(system.location("UTC"));
println(ts.Format("2006-01-02 15:04:05"));

// 1970-01-01 00:00:01
```

## Log

**생성**

| 생성자             | 설명                          |
|:------------------------|:----------------------------------------------|
| new Log(*name*)         | 주어진 이름으로 로거를 생성합니다     |

**옵션**

- `name` `String` logger name

**사용 예제**

```js
const system = require("@jsh/system");
const log = new system.Log("testing");

log.info("hello", "world");

// Log output:
//
// 2025/05/13 14:08:41.937 INFO  testing    hello world
```

### trace()

**문법**

```js
trace(...args)
```

**파라미터**

- `args` `any` 로그 메시지를 쓰기 위한 가변 길이 인자.

**반환값**

None.

### debug()

**문법**

```js
debug(...args)
```

**파라미터**

- `args` `any` 로그 메시지를 쓰기 위한 가변 길이 인자.

**반환값**

None.

### info()

**문법**

```js
info(...args)
```

**파라미터**

- `args` `any` 로그 메시지를 쓰기 위한 가변 길이 인자.

**반환값**

None.

### warn()

**문법**

```js
warn(...args)
```

**파라미터**

- `args` `any` 로그 메시지를 쓰기 위한 가변 길이 인자.

**반환값**

None.

### error()

**문법**

```js
error(...args)
```

**파라미터**

- `args` `any` 로그 메시지를 쓰기 위한 가변 길이 인자.

**반환값**

None.
