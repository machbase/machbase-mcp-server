# Machbase Neo JavaScript OS Module

`os` 모듈은 JSH 애플리케이션에서 사용할 수 있는 Node.js 호환 운영체제 정보 API를 제공합니다. (Machbase Neo 8.0.75부터)

```js
const os = require('os');
```

시스템 자원 지표를 더 자세히 다루려면 `@jsh/psutil` 모듈을 함께 사용할 수 있습니다.

## arch()

CPU 아키텍처를 반환합니다.

<h6>문법</h6>

```js
os.arch()
```

<h6>사용 예제</h6>

```js
const os = require('os');
console.println(os.arch());
```

## platform()

`darwin`, `linux`, `windows` 같은 플랫폼 이름을 반환합니다.

<h6>문법</h6>

```js
os.platform()
```

## type()

`Darwin`, `Linux`, `Windows_NT` 같은 OS 타입 문자열을 반환합니다.

<h6>문법</h6>

```js
os.type()
```

## release()

커널 릴리스/버전 문자열을 반환합니다.

<h6>문법</h6>

```js
os.release()
```

## hostname()

호스트 이름을 반환합니다.

<h6>문법</h6>

```js
os.hostname()
```

## homedir()

현재 사용자 홈 디렉터리 경로를 반환합니다.

<h6>문법</h6>

```js
os.homedir()
```

## tmpdir()

운영체제 기본 임시 디렉터리 경로를 반환합니다.

<h6>문법</h6>

```js
os.tmpdir()
```

## endianness()

CPU 엔디언을 반환합니다. 값은 `BE` 또는 `LE`입니다.

<h6>문법</h6>

```js
os.endianness()
```

## EOL

플랫폼별 줄바꿈 문자열입니다.

- POSIX: `\n`
- Windows: `\r\n`

<h6>사용 예제</h6>

```js
const os = require('os');
console.println(JSON.stringify(os.EOL));
```

## totalmem(), freemem()

시스템 전체/가용 메모리를 바이트 단위로 반환합니다.

<h6>문법</h6>

```js
os.totalmem()
os.freemem()
```

<h6>사용 예제</h6>

```js
const os = require('os');
console.println('total:', os.totalmem());
console.println('free :', os.freemem());
```

## uptime()

시스템 업타임을 초 단위로 반환합니다.

<h6>문법</h6>

```js
os.uptime()
```

## bootTime()

시스템 부팅 시각을 Unix timestamp로 반환합니다.

<h6>문법</h6>

```js
os.bootTime()
```

## loadavg()

로드 평균을 `[1분, 5분, 15분]` 배열로 반환합니다.

<h6>문법</h6>

```js
os.loadavg()
```

<h6>사용 예제</h6>

```js
const os = require('os');
const avg = os.loadavg();
console.println(Array.isArray(avg), avg.length);
```

## cpus()

CPU 코어별 정보 배열을 반환합니다. 각 항목에는 다음 필드가 포함됩니다.

- `model`, `speed`, `cores`
- `vendor`, `family`, `stepping`
- `times.user`, `times.nice`, `times.sys`, `times.idle`, `times.irq` (밀리초)

<h6>문법</h6>

```js
os.cpus()
```

<h6>사용 예제</h6>

```js
const os = require('os');
const list = os.cpus();
console.println(Array.isArray(list), list.length > 0);
```

## cpuCounts()

CPU 개수를 반환합니다.

- `true`: 논리 코어 수
- `false`: 물리 코어 수

<h6>문법</h6>

```js
os.cpuCounts(logical)
```

## cpuPercent()

CPU 사용률(%) 배열을 반환합니다.

- `intervalSec`: 샘플링 간격(초). `0`이면 즉시 값
- `perCPU`: `true`면 코어별 배열 반환

<h6>문법</h6>

```js
os.cpuPercent(intervalSec, perCPU)
```

<h6>사용 예제</h6>

```js
const os = require('os');
console.println(Array.isArray(os.cpuPercent(0, true)));
```

## networkInterfaces()

네트워크 인터페이스 정보를 객체로 반환합니다.

- key: 인터페이스 이름
- value: 주소 정보 배열
  - `address`
  - `family` (`IPv4` / `IPv6`)
  - `internal` (boolean)

<h6>문법</h6>

```js
os.networkInterfaces()
```

## hostInfo()

호스트 시스템 정보 객체를 반환합니다. 주요 필드는 다음과 같습니다.

- `hostname`, `uptime`, `bootTime`, `procs`
- `os`, `platform`, `platformFamily`, `platformVersion`
- `kernelVersion`, `kernelArch`
- `virtualizationSystem`, `virtualizationRole`, `hostId`

<h6>문법</h6>

```js
os.hostInfo()
```

<h6>사용 예제</h6>

```js
const os = require('os');
const info = os.hostInfo();
console.println(typeof info.hostname, typeof info.uptime);
```

## userInfo()

현재 사용자 정보를 반환합니다. 반환 필드는 다음과 같습니다.

- `username`, `homedir`, `shell`
- `uid`, `gid`

<h6>문법</h6>

```js
os.userInfo([options])
```

## diskPartitions()

디스크 파티션 목록을 반환합니다.

<h6>문법</h6>

```js
os.diskPartitions([all])
```

## diskUsage()

지정한 경로의 디스크 사용량 정보를 반환합니다. 일반적으로 `total`, `used`, `free`, `usedPercent` 필드를 포함합니다.

<h6>문법</h6>

```js
os.diskUsage(path)
```

<h6>사용 예제</h6>

```js
const os = require('os');
const usage = os.diskUsage('.');
console.println(typeof usage.total, typeof usage.usedPercent);
```

## diskIOCounters()

디스크 I/O 카운터를 반환합니다.

- `names` 생략 또는 빈 배열: 전체 디바이스
- `names` 지정: 선택한 디바이스

<h6>문법</h6>

```js
os.diskIOCounters([names])
```

## netProtoCounters()

네트워크 프로토콜 카운터를 반환합니다.

<h6>문법</h6>

```js
os.netProtoCounters([proto])
```

## constants

운영체제 관련 상수 객체입니다. 현재 다음 하위 객체를 제공합니다.

- `os.constants.signals`
- `os.constants.priority`

<h6>사용 예제</h6>

```js
const os = require('os');
console.println(typeof os.constants.signals.SIGINT);
console.println(typeof os.constants.priority.PRIORITY_NORMAL);
```

## os.constants.signals

시그널 이름과 숫자 값을 제공하는 상수 객체입니다.

이 상수들은 API 호환성을 위해 정규화된 Unix 스타일 시그널 번호를 사용합니다. Windows에서는 모든 숫자 값이 서로 다른 네이티브 시그널 동작에 일대일로 대응하지는 않습니다.

| 리터럴 | 숫자 |
| --- | --- |
| `SIGHUP` | `1` |
| `SIGINT` | `2` |
| `SIGQUIT` | `3` |
| `SIGABRT` | `6` |
| `SIGKILL` | `9` |
| `SIGUSR1` | `10` |
| `SIGSEGV` | `11` |
| `SIGUSR2` | `12` |
| `SIGPIPE` | `13` |
| `SIGALRM` | `14` |
| `SIGTERM` | `15` |

이 값들은 `process.kill()`에 숫자 시그널로 전달할 때 사용할 수 있습니다.

Windows에서 `SIGINT`는 특별하게 처리됩니다. JSH는 이를 가능한 한 interrupt 성격의 console control event로 전달하려고 시도합니다. 반면 `SIGTERM`, `SIGQUIT`, `SIGKILL`은 Windows에서 종료 요청으로 동작합니다.

<h6>사용 예제</h6>

```js
const os = require('os');
const process = require('process');

process.kill(12345, os.constants.signals.SIGTERM);
```

## process 시그널 API와의 관계

`os.constants.signals`는 시그널 번호를 제공하고, 실제 시그널 처리와 전송은 `process` 모듈이 수행합니다.

- 시그널 수신: `process.on('SIGINT', handler)`
- 시그널 전송: `process.kill(pid, os.constants.signals.SIGTERM)`

`process.on()`은 대소문자를 구분하지 않지만, 시그널 이벤트 이름은 `SIGINT`, `sigint`처럼 `SIG` 접두어를 포함한 정규 이름만 사용해야 합니다. `term` 같은 bare alias는 시그널 리스너 이름이 아닙니다.

반대로 `process.kill()`은 canonical 이름 외에 `term` 같은 alias도 허용합니다. `os.constants.signals`는 정규화된 상수 이름만 제공합니다.

Windows에서 `process.kill(pid, os.constants.signals.SIGINT)`는 best-effort 동작이며, Windows 콘솔 라우팅 제약에 따라 실패할 수 있습니다.

<h6>사용 예제</h6>

```js
const os = require('os');
const process = require('process');

process.on('sigint', () => {
  console.println('caught');
});

process.kill(process.pid, os.constants.signals.SIGINT);
```

## os.constants.priority

프로세스 우선순위 수준을 나타내는 상수 객체입니다.

| 상수 | 설명 |
| --- | --- |
| `PRIORITY_LOW` | 낮은 우선순위 |
| `PRIORITY_BELOW_NORMAL` | 보통보다 낮은 우선순위 |
| `PRIORITY_NORMAL` | 기본 우선순위 |
| `PRIORITY_ABOVE_NORMAL` | 보통보다 높은 우선순위 |
| `PRIORITY_HIGH` | 높은 우선순위 |
| `PRIORITY_HIGHEST` | 가장 높은 우선순위 |

<h6>사용 예제</h6>

```js
const os = require('os');
console.println(os.constants.priority.PRIORITY_NORMAL);
console.println(os.constants.priority.PRIORITY_HIGH);
```
