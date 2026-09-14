# Machbase Neo JavaScript Processs Module

`@jsh/process` 모듈은 JSH 애플리케이션 전용으로 설계되었으며 
다른 JSH 모듈과 달리 TQL의 `SCRIPT()` 함수에서는 사용할 수 없습니다.

## pid()

현재 프로세스의 프로세스 id를 가져옵니다.

**문법**

```js
pid()
```

**파라미터**

None.

**반환값**

프로세스 ID를 나타내는 숫자 값입니다.

**사용 예제**

```js
const m = require("@jsh/process")
console.log("my pid =", m.pid())
```

## ppid()

부모 프로세스의 프로세스 id를 가져옵니다.

**문법**

```js
ppid()
```

**파라미터**

None.

**반환값**

부모 프로세스 ID를 나타내는 숫자 값입니다.

**사용 예제**

```js
const m = require("@jsh/process")
console.log("parent pid =", m.ppid())
```

## args()

명령행 인자를 가져옵니다

**문법**

```js
args()
```

**파라미터**

None.

**반환값**

`String[]`

**사용 예제**

```js
p = require("@jsh/process");
args = p.args();
x = parseInt(args[1]);
console.log(`x = ${x}`);
```

## cwd()

현재 작업 디렉터리를 가져옵니다

**문법**

```js
cwd()
```

**파라미터**

None.

**반환값**

String

**사용 예제**

```js
p = require("@jsh/process");
console.log("cwd :", p.cwd());
```

## cd()

현재 작업 디렉터리를 변경합니다.

**문법**

```js
cd(path)
```

**파라미터**

`path` : 이동할 디렉터리 경로

**반환값**

None.

**사용 예제**

```js
p = require("@jsh/process");
p.cd('/dir/path');
console.log("cwd :", p.cwd());
```

## readDir()

주어진 디렉터리의 파일과 하위 디렉터리를 읽습니다.

**문법**

```js
readDir(path, callback)
```

**파라미터**

- `path`: `String` 디렉터리 경로
- `callback`: function (DirEntry) [undefined|Boolean] 콜백 함수. false를 반환하면 순회를 멈춥니다.

**반환값**

None.

**사용 예제**

```js

```

## DirEntry

| 속성           | 타입       | 설명        |
|:-------------------|:-----------|:-------------------|
| name               | String     |                    |
| isDir              | Boolean    |                    |
| readOnly           | Boolean    |                    |
| type               | String     |                    |
| size               | Number     |                    |
| virtual            | Boolean    |                    |

## print()

인자를 출력에 씁니다. 기본 출력은 로그 파일이며, 로그 파일명이 설정되지 않았으면 stdout입니다.

**문법**

```js
print(...args)
```

**파라미터**

`args` `...any` 쓸 가변 길이 인자.

**반환값**

None.

**사용 예제**

```js
p = require("@jsh/process")
p.print("Hello", "World!", "\n")
```

## println()

인자를 출력에 씁니다. 기본 출력은 로그 파일이며, 로그 파일명이 설정되지 않았으면 stdout입니다.

**문법**

```js
print(...args)
```

**파라미터**

`args` `...any` 쓸 가변 길이 인자.

**반환값**

None.

**사용 예제**

```js
p = require("@jsh/process")
p.println("Hello", "World!")
```

## exec()

다른 JavaScript 애플리케이션을 실행합니다.

**문법**

```js
exec(cmd, ...args)
```

**파라미터**

`cmd` `String` 실행할 .js 파일 경로
`args` `...String` cmd에 전달할 인자.

**반환값**

None.

**사용 예제**

```js
p = require("@jsh/process")
p.exec("/sbin/hello.js")
```

## daemonize()

현재 스크립트 파일을 부모 프로세스 ID가 `1`인 데몬 프로세스로 실행합니다.

**문법**

```js
daemonize(opts)
```

**파라미터**

- `opts` `Object` Options

| 속성           | 타입       | 설명        |
|:-------------------|:-----------|:-------------------|
| reload             | Boolean    | 핫 리로드 활성화  |

`reload`를 `true`로 설정하면 데몬 프로세스가 소스 코드 변경 감시자와 함께 시작됩니다.
메인 소스 코드 파일이 수정되면 현재 데몬 프로세스가 중지되고 즉시 재시작되어 변경 사항이 적용됩니다.
이 기능은 개발과 테스트 중에 유용하지만
파일 변경 감시에 추가 시스템 자원이 필요하므로 운영 환경에서는 켜지 않는 것이 좋습니다.

**반환값**

None.

**사용 예제**

```js
const p = require("@jsh/process")
if( p.ppid() == 1) {
    doBackgroundJob()
} else {
    p.daemonize()
    p.print("daemonize self, then exit")
}

function doBackgroundJob() {
    for(true){
        p.sleep(1000);
    }
}
```

## isDaemon()

부모 프로세스 ID(`ppid()`)가 `1`이면 `true`를 반환합니다. `ppid() == 1` 조건과 같습니다.

**문법**

```js
isDaemon()
```

**파라미터**

None.

**반환값**

Boolean

## isOrphan()

부모 프로세스 ID가 할당되지 않았으면 `true`를 반환합니다. `ppid() == 0xFFFFFFFF` 조건과 같습니다.

**문법**

```js
isOrphan()
```

**파라미터**

None.

**반환값**

Boolean

## schedule()

지정한 일정에 따라 콜백 함수를 실행합니다.
토큰의 `stop()` 메서드가 호출될 때까지 제어 흐름이 블록됩니다.

**문법**

```js
schedule(spec, callback)
```

**파라미터**

- `spec` `String` 일정 사양. 타이머 일정 사양을 참고하세요.
- `callback` `(time_epoch, token) => {}` 첫 번째 파라미터 `time_epoch`는 밀리초 단위 UNIX epoch 타임스탬프입니다.
    두 번째 파라미터 `token`으로 일정을 멈출 수 있습니다.

**반환값**

None.

**사용 예제**

```js
const {schedule} = require("@jsh/process");

var count = 0;
schedule("@every 2s", (ts, token)=>{
    count++;
    console.log(count, new Date(ts));
    if(count >= 5) token.stop();
})

// 1 2025-05-02 16:45:48
// 2 2025-05-02 16:45:50
// 3 2025-05-02 16:45:52
// 4 2025-05-02 16:45:54
// 5 2025-05-02 16:45:56
```

## sleep()

현재 제어 흐름을 일시 정지합니다.

**문법**

```js
sleep(duration)
```

**파라미터**

`duration` `Number` 대기 시간(밀리초).

**반환값**

None.

**사용 예제**

```js
p = require("@jsh/process")
p.sleep(1000) // 1 sec.
```

## kill()

지정한 프로세스 ID(pid)로 프로세스를 종료합니다.

**문법**

```js
kill(pid)
```

**파라미터**

`pid` `Number` 대상 프로세스의 pid.

**반환값**

None.

**사용 예제**

```js
p = require("@jsh/process")
p.kill(123)
```

## ps()

현재 실행 중인 모든 프로세스를 나열합니다.

**문법**

```js
ps()
```

**파라미터**

None.

**반환값**

`Object[]`: Process 객체 배열.

**사용 예제**

```js
p = require("@jsh/process")
list = p.ps()
for( const x of list ) {
    console.log(
        p.pid, 
        p.isOrphan() ? "-" : p.ppid,
        p.user, 
        p.name, 
        p.uptime)
}
```

## Process

`ps()`가 반환하는 프로세스 정보입니다.

| 속성           | 타입       | 설명        |
|:-------------------|:-----------|:-------------------|
| pid                | Number     | 프로세스 ID         |
| ppid               | Number     | 부모의 프로세스 ID |
| user               | String     | 사용자 이름 (예: `sys`)    |
| name               | String     | 스크립트 파일 이름         |
| uptime             | String     | 시작 이후 경과 시간  |

## addCleanup()
현재 JavaScript VM이 종료될 때 실행할 함수를 추가합니다.

**문법**

```js
addCleanup(fn)
```

**파라미터**

`fn` `()=>{}` 콜백 함수

**반환값**

`Number` 정리 콜백을 제거하기 위한 토큰입니다.

**사용 예제**

```js
p = require("@jsh/process")
p.addCleanup(()=>{ console.log("terminated") })
for(i = 0; i < 3; i++) {
    console.log("run -", i)
}

// run - 0
// run - 1
// run - 2
// terminated
```

### 실행 보장

훅은 JSH 런타임이 관리하는 종료 경로에 들어갈 때 실행되며, 정상적인 스크립트 완료와 명시적 `process.exit()` 호출이 포함됩니다.

다음 상황에서는 훅 실행이 **보장되지 않습니다**:
- 강제 종료 (SIGKILL, `kill -9`)
- 치명적인 OS 또는 Go 런타임 오류
- 처리되지 않은 시그널의 기본 동작

훅이 여러 개 등록되면 **역순으로** 실행됩니다. 한 훅에서 예외가 나도 남은 훅의 실행을 막지 않습니다.

> **참고:** `addShutdownHook()`은 모든 종료 상황을 보장하지 않습니다. 파일 플러시나 트랜잭션 정리 같은 중요한 작업은 정상 종료 흐름이 시작되기 전에 `process.on(signal, handler)`에서 명시적으로 정리하는 편이 좋습니다.

## removeCleanup()

주어진 토큰으로 앞서 등록한 정리 콜백을 제거합니다.

**문법**

```js
removeCleanup(token)
```

**파라미터**

`token` `Number` `addCleanup()`이 반환한 토큰.

**반환값**

None.

**사용 예제**

```js
p = require("@jsh/process")
token = p.addCleanup(()=>{ console.log("terminated") })
for(i = 0; i < 3; i++) {
    console.log("run -", i)
}
p.removeCleanup(token)

// run - 0
// run - 1
// run - 2
```
