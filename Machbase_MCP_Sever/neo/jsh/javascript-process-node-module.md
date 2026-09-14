# Machbase Neo JavaScript Process Module (Node 호환)

`process` 모듈은 JSH 애플리케이션에서 사용할 수 있는 Node.js 호환 프로세스 API입니다. (Machbase Neo 8.0.75부터)

```js
const process = require('process');
```

Machbase 고유 프로세스 제어 API(`daemonize()`, `schedule()`, `ps()`, `readDir()` 등)는 `@jsh/process` 모듈에서 제공합니다. 시그널 상수는 `os.constants.signals`에 있습니다.

## addShutdownHook()

현재 프로세스가 종료될 때 호출할 콜백 함수를 추가합니다. 이 hook은 JSH 런타임이 관리하는 종료 경로에 들어왔을 때 호출됩니다. 예를 들어 스크립트가 정상적으로 끝나거나 `process.exit()`를 호출한 경우 실행됩니다.

다음 경우에는 호출이 보장되지 않습니다.

- `SIGKILL`, `kill -9` 같은 강제 종료
- OS 또는 Go 런타임 수준의 치명적인 비정상 종료
- `process.on(signal, handler)`로 가로채지 않은 시그널의 기본 동작에 의한 종료

catch 가능한 시그널에 대해 정리가 필요하면 `process.on(signal, handler)`에서 정리 코드를 수행한 뒤 종료 흐름으로 들어가도록 작성하는 것이 좋습니다.

여러 shutdown hook이 등록되면 역순으로 실행됩니다. 어떤 hook이 panic이나 예외를 발생시켜도 나머지 hook은 계속 실행됩니다.

<h6>문법</h6>

```js
process.addShutdownHook(() => {})
```

<h6>사용 예제</h6>

```js
const process = require('process');
process.addShutdownHook(() => {
    console.println("shutdown hook called.");
})
console.println("running...")

// Output:
// running...
// shutdown hook called.
```

강제 종료까지 포함한 절대적인 보장이 필요하다면 파일 flush, 외부 트랜잭션 정리, lock 해제 같은 작업은 hook에만 의존하지 말고 가능한 시점마다 명시적으로 수행해야 합니다.

## arch

호스트 머신의 운영체제 아키텍처를 식별하는 문자열입니다. 일반적인 값은 `amd64`, `aarch64`입니다.

## platform

호스트 머신의 운영체제 플랫폼을 식별하는 문자열입니다. 일반적인 값은 `windows`, `linux`, `darwin`(macOS)입니다.

## argv

현재 프로세스에 전달된 명령행 인자 배열입니다.

- `argv[0]`: JSH 실행 파일의 절대 경로
- `argv[1]`: 실행 중인 스크립트 이름(또는 경로)
- `argv[2:]`: 스크립트에 전달된 나머지 인자

<h6>사용 예제</h6>

```js
const process = require('process');
console.println('argv[0]:', process.argv[0]);
console.println('argv[1]:', process.argv[1]);
console.println('argv   :', process.argv);
```

## chdir()

현재 작업 디렉터리를 변경합니다. `path`가 빈 문자열이면 JSH는 이를 `$HOME`으로 해석합니다.

<h6>문법</h6>

```js
process.chdir(path)
```

## cwd()

현재 작업 디렉터리 경로를 반환합니다.

## exit()

현재 프로세스를 종료합니다. *code*를 생략하면 기본값은 `0`입니다.

<h6>문법</h6>

```js
process.exit([code])
```

## which()

`PATH`에서 JavaScript 명령을 찾아 해석된 파일 경로를 반환합니다. 명령에 `.js` 확장자가 없으면 자동으로 추가됩니다.

<h6>문법</h6>

```js
process.which(command)
```

## expand()

문자열에서 `$HOME`, `${HOME}` 같은 환경 변수를 확장합니다.

<h6>문법</h6>

```js
process.expand(value)
```

## env

JSH 런타임 환경 객체입니다. `process.env.get('NAME')` 형태로 값을 읽을 수 있습니다.

## exec()

JavaScript 명령 파일을 실행하고 종료 코드를 반환합니다.

<h6>문법</h6>

```js
process.exec(command, ...args)
```

<h6>사용 예제</h6>

```js
const process = require('process');
const path = process.which('echo');
const code = process.exec(path, 'hello from exec');
```

## execPath

호스트 운영체제에서 현재 프로세스 실행 파일의 절대 경로입니다.

## execString()

문자열로 전달한 JavaScript 소스 코드를 실행하고 종료 코드를 반환합니다.

<h6>문법</h6>

```js
process.execString(source, ...args)
```

## hrtime()

고해상도 시간 튜플 `[seconds, nanoseconds]`을 반환합니다. 이전 튜플을 전달하면 해당 시점부터의 경과 시간을 반환합니다.

<h6>문법</h6>

```js
process.hrtime([previous])
```

<h6>사용 예제</h6>

```js
const process = require('process');
const start = process.hrtime();
const diff = process.hrtime([start[0], start[1]]);
```

## kill()

지정한 프로세스 ID로 실제 OS 시그널을 전송합니다.

- `pid`는 양의 정수여야 합니다.
- `signal`을 생략하면 기본값은 `SIGTERM`입니다.
- 성공하면 `true`를 반환하고, 실패하면 `Error` 객체를 반환합니다.
- `signal`에는 문자열 이름 또는 숫자 시그널 번호를 사용할 수 있습니다.

문자열 이름은 대소문자를 구분하지 않으며 `SIG` 접두어를 생략할 수 있습니다. 이 별칭 지원은 `process.kill()`에만 적용됩니다. 예: `SIGTERM`, `term`, `sigint`

숫자 시그널은 `os.constants.signals`의 값과 같습니다(`1` SIGHUP, `2` SIGINT, `3` SIGQUIT, `6` SIGABRT, `9` SIGKILL, `10` SIGUSR1, `11` SIGSEGV, `12` SIGUSR2, `13` SIGPIPE, `14` SIGALRM, `15` SIGTERM).

<h6>문법</h6>

```js
process.kill(pid[, signal])
```

## memoryUsage()

메모리 사용량 정보를 객체로 반환합니다. 현재 구현은 모든 필드를 숫자 `0`으로 반환하는 플레이스홀더입니다.

<h6>반환 필드</h6>

- `rss`
- `heapTotal`
- `heapUsed`
- `external`
- `arrayBuffers`

## cpuUsage()

CPU 사용량 정보를 반환합니다. 현재 구현은 `user`, `system` 두 필드 모두 숫자 `0`을 반환하는 플레이스홀더입니다.

## nextTick()

다음 이벤트 루프 턴에서 실행할 콜백을 예약합니다. 첫 번째 인자가 함수가 아니면 아무 동작도 하지 않고 `undefined`를 반환합니다.

<h6>문법</h6>

```js
process.nextTick(callback, ...args)
```

<h6>사용 예제</h6>

```js
const process = require('process');
process.nextTick((a, b) => console.println('tick:', a, b), 'first', 'second');
```

## now()

현재 시각을 JavaScript 날짜-시간 객체로 반환합니다.

## uptime()

프로세스 업타임을 초 단위 숫자로 반환합니다.

## pid, ppid

`pid`는 현재 프로세스의 ID, `ppid`는 부모 프로세스의 ID입니다. 값의 타입은 숫자입니다.

## title

현재 프로그램을 식별하는 문자열입니다.

## version, versions

`version`은 JSH 런타임 버전을 식별하는 문자열입니다. `versions`는 상세 버전 정보를 제공하는 객체입니다.

- `versions.jsh`: JSH 런타임 버전 문자열
- `versions.go`: Go 런타임 버전 문자열

## stdin, stdout, stderr

`stdin`, `stdout`, `stderr` 스트림입니다.

<h6>사용 예제</h6>

```js
const process = require('process');
process.stdout.write('Enter text: ');
const text = process.stdin.readLine();
```

## Signal Events

`process`는 `EventEmitter`처럼 시그널 이벤트를 받을 수 있습니다. 다음 시그널 이름을 지원합니다.

`SIGHUP`, `SIGINT`, `SIGQUIT`, `SIGABRT`, `SIGKILL`, `SIGUSR1`, `SIGSEGV`, `SIGUSR2`, `SIGPIPE`, `SIGALRM`, `SIGTERM`

시그널 이벤트 리스너는 대소문자를 구분하지 않습니다. 다만 이벤트 이름은 `SIG` 접두어를 포함한 형태만 지원합니다. 예를 들어 `SIGTERM`과 `sigterm`은 동일하게 동작하지만, `term` 같은 bare alias는 시그널 이벤트 이름으로 취급하지 않고 일반 `EventEmitter` 이벤트 이름으로 유지됩니다.

리스너를 등록하면 JSH가 해당 OS 시그널을 이벤트로 전달합니다. 리스너가 없으면 운영체제의 기본 시그널 동작을 따릅니다.

<h6>사용 예제</h6>

```js
const process = require('process');
process.on('sigint', () => {
  console.println('caught SIGINT');
});
```

```js
process.on('sigterm', handler);
process.once('SIGTERM', handler);
process.addListener('sigquit', handler);
```

## dispatchEvent()

등록된 리스너에 이벤트를 직접 전달합니다.

## dumpStack()

현재 실행 중인 스택을 출력합니다. 디버깅 용도로 사용합니다.
