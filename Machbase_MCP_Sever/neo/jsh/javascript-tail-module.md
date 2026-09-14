# Machbase Neo JavaScript Tail Module

`util/tail` 모듈은 단일 파일을 `tail -F`처럼 추적하기 위한 polling 기반 tailer를 제공합니다. 이 모듈은 호출자가 `setInterval()`로 `poll()`을 주기적으로 호출하는 패턴을 기준으로 설계되었습니다.

```js
const tail = require('util/tail');
```

## tail.create()

tailer 인스턴스를 생성합니다.

<h6>문법</h6>

```js
tail.create(path, options)
```

<h6>파라미터</h6>

- `path` `String`: 추적할 파일 경로
- `options` `Object`:
  - `fromStart` `Boolean` (기본값: `false`)
    - `false`: 생성 시점의 파일 끝부터 추적
    - `true`: 생성 시점 파일 시작부터 읽기

<h6>반환 객체</h6>

| 메서드/필드 | 타입 | 설명 |
|:------------|:-----|:-----|
| `path` | String | 생성에 사용한 경로 |
| `poll(callback?)` | Function | 새 줄을 읽어 `String[]`로 반환 |
| `close()` | Function | 파일 핸들을 닫고 tailer 종료 |

`poll(callback?)` 동작:

- 반환값: 새로 감지된 줄 배열 (`String[]`)
- `callback`을 전달하면 동일한 배열을 callback 인자로도 전달
- 읽을 새 줄이 없으면 빈 배열 반환
- 파일 truncate/rotation 상황을 polling 시점에 반영

## 기본 사용 예제

```js
const tail = require('util/tail');

const follower = tail.create('/tmp/app.log', { fromStart: false });

const tm = setInterval(function () {
    const lines = follower.poll(function (arr) {
        // arr is String[]
    });

    for (let i = 0; i < lines.length; i++) {
        console.println(lines[i]);
    }
}, 500);

// cleanup example
setTimeout(function () {
    clearInterval(tm);
    follower.close();
}, 10_000);
```

## SSE 어댑터

`util/tail/sse`는 tail 결과를 SSE 형식으로 출력하기 위한 어댑터입니다.

- `require('util/tail/sse')`
- `require('util/tail').sse`

### tail/sse.create()

<h6>문법</h6>

```js
tailSSE.create(path, options)
```

<h6>파라미터</h6>

- `path` `String`: 추적할 파일 경로
- `options` `Object`:
  - `fromStart` `Boolean` (기본값: `false`)
  - `event` `String` (기본값: 빈 문자열)
  - `retryMs` `Number` (선택)
  - `write` `Function` (선택). 출력 함수를 지정하지 않으면 `process.stdout.write()`를 사용합니다.

<h6>반환 객체</h6>

| 메서드 | 설명 |
|:-------|:-----|
| `writeHeaders()` | SSE 응답 헤더 출력 |
| `poll()` | 새 줄을 읽어 `event/data` 프레임 출력 후 `String[]` 반환 |
| `send(data, event?)` | 임의 데이터 1건을 SSE 프레임으로 출력 |
| `comment(text)` | SSE comment 프레임(`: ...`) 출력 |
| `close()` | 내부 tailer 종료 |

## cgi-bin SSE 예제

```js
const tailSSE = require('util/tail/sse');
const process = require('process');

const path = process.env.get('SCRIPT_NAME');
const target = '/work/'+path.substring(0, path.lastIndexOf('/')) + '/app.log';

const intervalMs = Number(process.env.QUERY_INTERVAL_MS || 500);

const adapter = tailSSE.create(target, {
    fromStart: false,
    event: 'log',
    retryMs: 1500,
});

adapter.writeHeaders();

const timer = setInterval(function () {
    try {
        adapter.poll();
    } catch (err) {
        adapter.send(String(err), 'error');
        clearInterval(timer);
        adapter.close();
        process.exit(0);
    }
}, intervalMs);

process.on('SIGINT', function () {
    clearInterval(timer);
    adapter.close();
    process.exit(0);
});

process.on('SIGTERM', function () {
    clearInterval(timer);
    adapter.close();
    process.exit(0);
});
```

## 동작 참고

- polling 주기와 생명주기(종료·정리)는 호출자가 제어합니다.
- 파일이 없으면 `poll()`은 빈 배열을 반환하며, 파일이 생성된 이후 다음 polling에서 추적을 시작합니다.
- rotation/truncate는 polling 시점에 감지되어 반영됩니다.
