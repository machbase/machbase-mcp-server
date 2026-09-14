# Machbase Neo JavaScript NATS Module

`nats` 모듈은 JSH 애플리케이션에 이벤트 기반 NATS 클라이언트를 제공합니다.
`Client`를 만들면 클라이언트가 자동으로 연결을 시작합니다.

일반적인 사용법은 다음과 같습니다.

```js
const nats = require('nats');
```

## Client

NATS 클라이언트를 만들고 연결을 시작합니다.

<h6>문법</h6>

```js
new nats.Client(options)
```

<h6>옵션</h6>

| 옵션 | 타입 | 설명 |
|:-----|:-----|:-----|
| `servers` | String[] | `nats://127.0.0.1:4222` 같은 NATS 서버 URL 목록 |
| `name` | String | 연결 이름 |
| `user` | String | 인증 사용자 |
| `password` | String | 인증 비밀번호 |
| `token` | String | 인증 토큰 |
| `noRandomize` | Boolean | 서버 랜덤 선택 비활성화 |
| `noEcho` | Boolean | 자신이 발행한 메시지 echo 비활성화 |
| `verbose` | Boolean | verbose 프로토콜 동작 활성화 |
| `pedantic` | Boolean | pedantic 프로토콜 검사 활성화 |
| `allowReconnect` | Boolean | 재연결 허용 |
| `maxReconnect` | Number | 최대 재연결 횟수 |
| `reconnectWait` | Number | 재연결 대기 시간(밀리초) |
| `timeout` | Number | 연결 타임아웃(밀리초) |
| `drainTimeout` | Number | drain 타임아웃(밀리초) |
| `flusherTimeout` | Number | flush 타임아웃(밀리초) |
| `pingInterval` | Number | ping 간격(밀리초) |
| `maxPingsOut` | Number | 최대 outstanding ping 수 |
| `retryOnFailedConnect` | Boolean | 최초 연결 실패 시 재시도 |
| `skipHostLookup` | Boolean | host lookup 최적화 건너뛰기 |

`client.config` 속성은 현재 적용된 설정을 노출합니다.

<h6>사용 예제</h6>

```js
const nats = require('nats');

const client = new nats.Client({
    servers: ['nats://127.0.0.1:4222'],
    name: 'test-client',
    allowReconnect: true,
    maxReconnect: 10,
    reconnectWait: 2000,
    timeout: 10 * 1000,
});
```

## publish()

NATS subject로 메시지를 보냅니다.

<h6>문법</h6>

```js
client.publish(subject, message[, options])
```

<h6>옵션</h6>

- `reply` 요청/응답 패턴을 위한 선택적 응답 subject

연결이 열리기 전에 `publish()`를 호출하면 `error` 이벤트가 발생합니다.

## subscribe()

NATS subject를 구독합니다.

<h6>문법</h6>

```js
client.subscribe(subject[, options])
```

<h6>옵션</h6>

- `queue` 부하 분산 배분을 위한 queue 그룹 이름

연결이 열리기 전에 `subscribe()`를 호출하면 `error` 이벤트가 발생합니다.

## close()

NATS 연결을 종료합니다.

<h6>문법</h6>

```js
client.close()
```

## Events

- `open` - 연결 수립됨
- `message` - 구독에서 메시지 수신. 메시지 객체는 `subject`, `reply`, `payload`를 포함합니다
- `subscribed` - 서버가 구독을 수락함
- `published` - 발행 완료
- `error` - 연결 또는 작업 실패
- `close` - 연결 닫힘

## 사용 예제: Pub/Sub

```js
const nats = require('nats');

const sub = new nats.Client({ servers: 'nats://127.0.0.1:4222' });
sub.on('open', function() {
    sub.subscribe('demo.topic');
});
sub.on('message', function(msg) {
    console.println('Received:', msg.subject, msg.payload);
    sub.close();
});

const pub = new nats.Client({ servers: 'nats://127.0.0.1:4222' });
pub.on('open', function() {
    pub.publish('demo.topic', 'hello nats');
});
pub.on('published', function() {
    pub.close();
});
```

## 사용 예제: Request/Reply

```js
const nats = require('nats');

const responder = new nats.Client({ servers: 'nats://127.0.0.1:4222' });
responder.on('open', function() {
    responder.subscribe('rpc.echo');
});
responder.on('message', function(msg) {
    if (msg.reply) {
        responder.publish(msg.reply, 'reply: ' + msg.payload);
    }
});

const requester = new nats.Client({ servers: 'nats://127.0.0.1:4222' });
requester.on('open', function() {
    requester.subscribe('reply.inbox');
    requester.publish('rpc.echo', 'ping', { reply: 'reply.inbox' });
});
requester.on('message', function(msg) {
    console.println('Reply:', msg.payload);
    requester.close();
    responder.close();
});
```

## 동작 참고사항

- 클라이언트는 생성 시 자동으로 연결을 시작합니다.
- 연결이 열리기 전에 `publish()`나 `subscribe()`를 호출하면 `error` 이벤트가 발생합니다.
- queue 구독을 사용하면 여러 구독자에게 부하 분산된 메시지 배분이 가능합니다.
