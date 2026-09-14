# Machbase Neo HTTP Watch Latest Data

## Server-Sent Events 사용

클라이언트는 서버로부터 스트리밍 이벤트를 받을 수 있으며,
지정한 테이블의 최신 레코드를 계속 최신 상태로 유지할 때 유용합니다.

Server-Sent Events(SSE)는 하나의 HTTP 연결로 서버가 클라이언트에 갱신 내용을 밀어 보내는 기술입니다.
라이브 피드, 알림, 실시간 분석처럼 데이터가 계속 갱신되어야 하는 애플리케이션에 널리 쓰입니다.

**Server-Sent Events(SSE)의 주요 특징**

1. **단방향 통신**: 서버는 클라이언트로 업데이트를 보낼 수 있지만, 클라이언트는 같은 연결로 서버에 데이터를 보낼 수 없습니다.
2. **지속 연결**: 클라이언트가 열린 상태로 유지되는 HTTP 연결 하나를 맺어, 서버가 업데이트가 생길 때마다 보낼 수 있게 합니다.
3. **자동 재연결**: 연결이 끊기면 클라이언트가 자동으로 재연결을 시도합니다.
4. **단순한 API**: SSE는 웹 애플리케이션에서 구현하고 사용하기 쉬운 단순한 API를 씁니다.


**SSE 동작 방식**
1. **클라이언트가 업데이트 요청**: 클라이언트가 서버에 HTTP 요청을 보내 업데이트 수신을 시작합니다.
2. **서버가 업데이트 전송**: 서버는 text/event-stream MIME 타입으로 서식화된 업데이트 스트림으로 응답합니다.
3. **클라이언트가 업데이트 처리**: 클라이언트는 수신한 업데이트를 처리하며, 보통 사용자 인터페이스를 실시간으로 갱신합니다.

웹 브라우저는 한 호스트에 열 수 있는 동시 SSE 연결 수를 제한합니다. 자원 고갈을 막고 네트워크 자원을 공평하게 사용하기 위해서입니다. 이 제한과 관련해 알아둘 점은 다음과 같습니다:

**브라우저의 SSE 연결 제한**

1. **연결 수 제한**: 대부분의 최신 브라우저는 단일 호스트에 대한 동시 SSE 연결 수를 제한합니다. 보통 호스트당 6개입니다.
2. **자원 관리**: 연결 수를 제한하면 메모리와 네트워크 대역폭 같은 자원을 관리할 수 있어, 한 페이지가 브라우저나 서버를 압도하는 것을 막습니다.
3. **공정한 사용**: 이런 제한을 통해 브라우저는 여러 탭이나 애플리케이션이 네트워크 자원을 공정하게 나눠 쓰도록 하고, 한 애플리케이션이 연결을 독점하지 못하게 합니다.

SSE 연결에 대한 브라우저 제한을 이해하고 지키는 것은 견고하고 효율적인 실시간 웹 애플리케이션을 만드는 데 매우 중요합니다. 이 제한을 염두에 두고 설계하면 매끄러운 사용자 경험과 최적의 자원 사용을 확보할 수 있습니다.


## 최신 데이터 감시

SSE(server-sent events)의 엔드포인트는 다음과 같습니다:

```
/db/watch/{table}
```

*watch* API는 다음 질의 파라미터를 지원합니다:

| 파라미터       | 기본값 | 설명                   |
|:----------- |---------|:----------------------------- |
| timeformat  | `ns`     | 출력 시간 형식: s, ms, us, ns    |
| tz          | `UTC`    | 출력 시간대: UTC, Local, 지역 지정 |
| period      | `3s`     | 갱신 주기                |
| keep-alive  | `30s`    | 연결을 유지하고 TCP 타임아웃을 막기 위해 서버가 주석 메시지를 보내는 주기 |


**Tag Table**

대상 테이블이 태그 테이블이면 `tag` 파라미터가 필요합니다.

| 파라미터       | 기본값 | 설명                   |
|:----------- |---------|:----------------------------- |
| **tag**     |         | 태그 이름 배열 지정        |
| parallelism | `0`     | 병렬 처리 개수를 결정합니다.<br/>0이거나 태그 수보다 큰 값이면<br/>태그 수를 기본값으로 사용합니다. |

**참고: 이 API는 지정한 *period* 안에서 각 태그의 최신 데이터만 전달합니다. 해당 기간에 여러 값이 입력되면 서버는 가장 최근 값만 보냅니다.**

**Log Table**

| 파라미터       | 기본값 | 설명                   |
|:----------- |---------|:----------------------------- |
| max-rows    | `20`   | 서버가 한 주기에 보내는 최대 레코드 수.<br/>지정한 수보다 레코드가 많으면<br/> 서버는 그 주기의 초과분을 생략합니다.<br/>하드 리밋은 100입니다.|

## cURL 예제

*curl* 명령으로 태그의 최신 값 스트림을 받습니다:

```sh
curl -o - -v "http://127.0.0.1:5654/db/watch/example"\
"?tag=neo_load1&tag=neo_load5&period=3s&timeformat=s"
```

클라이언트가 연결을 유지하는 동안 서버는 데이터 스트림을 계속 보냅니다:

```sh
data: {"NAME":"neo_load1","TIME":1729070964,"VALUE":1.87}

data: {"NAME":"neo_load5","TIME":1729070964,"VALUE":1.37}

data: {"NAME":"neo_load1","TIME":1729070969,"VALUE":1.8}

data: {"NAME":"neo_load5","TIME":1729070969,"VALUE":1.36}

^C
```

## Javascript 예제

```html
<html>
<body>
    <h1>Server-Sent Events Example</h1>
    <div id="messages"></div>
    <script>
        // Create a new EventSource instance
        const addr = 'http://127.0.0.1:5654/db/watch/EXAMPLE';
        const params = 'tag=neo_load1&tag=neo_load5&period=3s&keep-alive=30s&timeformat=default';
        const eventSource = new EventSource(`${addr}?${params}`);

        // Get the messages div
        const messagesDiv = document.getElementById('messages');

        // Handle incoming messages
        eventSource.onmessage = function (event) {
            // Create a new element
            const pre = document.createElement('pre');
            const msg = JSON.parse(event.data);
            // Set the text content to the event data
            pre.textContent = event.data + ' => ' + msg.NAME + ':' + msg.VALUE;
            // Append the element to the messages div
            messagesDiv.appendChild(pre);
        };

        // Handle errors
        eventSource.onerror = function (event) {
            console.error('EventSource failed:', event);
        };
    </script>
</body>
</html>
```

## Python 예제

```python
import requests
import sseclient

# Define the URL to connect to the server-sent events endpoint
url = 'http://127.0.0.1:5654/db/watch/EXAMPLE'
params = {
    'tag': ['neo_load1', 'neo_load5'],
    'period': '3s',
    'keep-alive': '30s',
    'timeformat': 'default'
}

# Create a streaming request
response = requests.get(url, params=params, stream=True)

# Use sseclient to handle the server-sent events
client = sseclient.SSEClient(response)

# Print the received messages
for event in client.events():
    print(event.data)
```
