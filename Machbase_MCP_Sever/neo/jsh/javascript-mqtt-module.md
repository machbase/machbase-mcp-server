# Machbase Neo JavaScript MQTT Module

## Client

MQTT 클라이언트입니다.

**사용 예제**

```js
const mqtt = require("@jsh/mqtt");
const client = new mqtt.Client({ serverUrls: ["tcp://127.0.0.1:1236"] });
try {
    client.onConnect = connAck => { println("connected."); }
    client.onConnectError = err => { println("connect error", err); }
    client.connect({timeout: 10*1000});
    client.publish("test/topic", "Hello, MQTT!", 0)
} catch(e) {
    console.log("Error:", e);
} finally {
    client.disconnect();
}
```

**생성**

| 생성자             | 설명                          |
|:------------------------|:----------------------------------------------|
| new Client(*options*)   | 옵션으로 MQTT 클라이언트 객체를 생성합니다 |

**옵션**

| 옵션                             | 타입         | 기본값        | 설명         |
|:-----------------------------------|:-------------|:---------------|:--------------------|
| serverUrls                         | String[]     |                | 서버 주소들    |
| keepAlive                          | Number       | `10`           |                     |
| cleanStart                         | Boolean      | `true`         | 클린 세션       |
| username                           | String       |                |                     |
| password                           | String       |                |                     |
| clientID                           | String       | random id      |                     |
| debug                              | Boolean      | `false`        |                     |
| sessionExpiryInterval              | Number       | `60`           |                     |
| connectRetryDelay                  | Number       | `10`           |                     |
| connectTimeout                     | Number       | `10`           |                     |
| packetTimeout                      | Number       | `5`            | 패킷 응답 대기 타임아웃(초) |
| queue                              | String       | `memory`       | 발행 큐 저장 방식     |

**config 속성**

`client.config`는 네이티브 MQTT 클라이언트가 실제로 사용하는, 파싱된 연결 설정을 노출합니다.

| 필드 | 타입 | 설명 |
|:-----|:-----|:-----|
| `serverUrls` | Array | 파싱된 브로커 URL 목록 |
| `connectUsername` | String | 설정된 사용자 이름 |
| `connectPassword` | byte data | 바이트 형태의 비밀번호 |
| `keepAlive` | Number | Keep Alive 간격 |
| `reconnectBackoff(n)` | Function | 재접속 지연 계산 함수 |
| `cleanStartOnInitialConnection` | Boolean | MQTT v5 clean start 플래그 |
| `connectTimeout` | Number | 연결 타임아웃 |

```js
console.log(client.config.serverUrls);
console.log(client.config.keepAlive);
```

### connect()

**문법**

```js
connect(opts)
```

**파라미터**

- `opts` `Object`

| 속성           | 타입       | 설명           |
|:-------------------|:-----------|:----------------------|
| timeout            | Number     | 연결 타임아웃(밀리초) |

**반환값**

None.

### disconnect()

**문법**

```js
disconnect(opts)
```

**파라미터**

- `opts` `Object`

| 속성           | 타입       | 설명           |
|:-------------------|:-----------|:----------------------|
| timeout            | Number     | 연결 종료 대기 타임아웃(밀리초) |

**반환값**

None.

### close()

클라이언트 연결을 종료합니다. `disconnect()`와 동일하게 연결을 닫습니다.

**문법**

```js
close()
```

**반환값**

없음. `close` 이벤트가 발생합니다.

### subscribe()

**문법**

```js
subscribe(opts)
```

**파라미터**

- `opts` `Object` *SubscriptionOption*

**SubscriptionOption**

| 속성           | 타입       | 설명           |
|:-------------------|:-----------|:----------------------|
| **subscriptions**  | Object[]   | *Subscription* 배열 |
| properties         | Object     | *Properties*            |

**Subscription**

| 속성           | 타입       | 설명           |
|:-------------------|:-----------|:----------------------|
| **topic**          | String     |                       |
| qos                | Number     | `0`, `1`, `2`         |
| retainHandling     | Number     |                       |
| noLocal            | Boolean    |                       |
| retainAsPublished  | Boolean    |                       |

**속성**

| 속성           | 타입       | 설명           |
|:-------------------|:-----------|:----------------------|
| user               | Object     | 키-값 속성  |

**반환값**

None.

**사용 예제**

```js
const topicName = 'sensor/temperature';
client.subscribe({subscriptions:[{topic:topicName, qos:0}]});
```

### unsubscribe()

**문법**

```js
unsubscribe(opts)
```

**파라미터**

- `opts` `Object` *UnsubscribeOption*

**UnsubscribeOption**

| 속성           | 타입       | 설명           |
|:-------------------|:-----------|:----------------------|
| **topics**         | String[]   | 구독 해제할 토픽 배열 |
| properties         | Object     | *Properties*          |

**속성**

| 속성           | 타입       | 설명           |
|:-------------------|:-----------|:----------------------|
| user               | Object     | 사용자 키-값 속성 |

**반환값**

None.

**사용 예제**

```js
const topicName = 'sensor/temperature';
client.unsubscribe({topics:[topicName]});
```

### publish()

**문법**

```js
publish(opts, payload)
```

**파라미터**

- `opts` `Object` *PublishOptions*
- `payload` `String` or `Number`

**PublishOptions**

| 속성           | 타입       | 설명           |
|:-------------------|:-----------|:----------------------|
| **topic**          | String     |                       |
| qos                | Number     | `0`, `1`, `2`         |
| packetID           | String     |                       |
| retain             | Boolean    |                       |
| properties         | Object     |                       |

**반환값**

- `Object`

| 속성           | 타입       | 설명           |
|:-------------------|:-----------|:----------------------|
| reasonCode         | Number     |                       |
| properties         | Object     |                       |

**사용 예제**

```js
let r = client.publish('sensor/temperature', 'Hello World', 1)
console.log(r.reasonCode)
```

### onMessage 콜백

메시지를 받는 콜백 함수입니다.

**문법**

```js
function (msg) { }
```

- `msg` `Object` Message

**Message**

| 속성           | 타입       | 설명           |
|:-------------------|:-----------|:----------------------|
| packetID           | Number     |                       |
| topic              | String     |                       |
| qos                | Number     | 0, 1, 2               |
| retain             | Boolean    |                       |
| payload            | Object     | 바이너리 안전한 메시지 페이로드 |
| payloadText        | String     | UTF-8로 디코딩한 텍스트 편의 필드 |
| properties         | Object     | MQTT v5 publish 속성   |

**Payload**

- `msg.payload.bytes()`
- `msg.payload.string()`

텍스트 메시지는 `msg.payloadText` 또는 `msg.payload.toString()`으로도 읽을 수 있습니다. 바이너리 메시지는 `msg.payload`를 그대로 사용합니다.

```js
client.onMessage = function(msg) {
    console.log('Payload bytes:', Array.from(msg.payload).join(','));
    console.log('Content type:', msg.properties.contentType);
    console.log('Response topic:', msg.properties.responseTopic);
};
```

**속성**

| 속성           | 타입       | 설명           |
|:-------------------|:-----------|:----------------------|
| correlationData    | byte[]     |                       |
| contentType        | String     |                       |
| responseTopic      | String     |                       |
| payloadFormat      | Number     | 또는 undefined          |
| messageExpiry      | Number     | 또는 undefined          |
| subscriptionIdentifier | Number | 또는 undefined          |
| topicAlias         | Number     | 또는 undefined          |
| user               | Object     | 사용자 속성       |

### onConnect 콜백

연결 시 호출되는 콜백입니다.

**문법**

```js
function (ack) { }
```

**파라미터**

- `ack` `Object`

| 속성           | 타입       | 설명           |
|:-------------------|:-----------|:----------------------|
| sessionPresent     | Boolean    |                       |
| reasonCode         | Number     |                       |
| properties         | Object     | 속성            |

**속성**

| Property              | Type       | Description           |
|:----------------------|:-----------|:----------------------|
| reasonString          | String     |                       |
| reasonInfo            | String     |                       |
| assignedClientID      | String     |                       |
| authMethod            | String     |                       |
| serverKeepAlive       | Number     | 또는 undefined          |
| sessionExpiryInterval | Number     | 또는 undefined          |
| user                  | Object     |                       |

**반환값**

None.

### onConnectError 콜백

연결 오류 시 호출되는 콜백입니다.

**문법**

```js
function (err) { }
```

**파라미터**

- `error` `String`

**반환값**

None.

### onDisconnect 콜백

연결 종료 시 호출되는 콜백입니다

**문법**

```js
function (disconn) { }
```

**파라미터**

- `disconn` `Object`

**반환값**

None.

### onClientError 콜백

클라이언트 오류 시 호출되는 콜백입니다

**문법**

```js
function (err) { }
```

**파라미터**

- `err` `String`

**반환값**

None.
