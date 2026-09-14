# Machbase Neo MQTT Query

MQTT의 데이터베이스 조회 토픽은 `db/query`입니다. 이 토픽으로 조회 요청을 보내면 서버가 `db/reply` 토픽 또는 요청의 `reply` 필드에 지정된 토픽으로 결과를 응답합니다.

## 조회 JSON

| 파라미터       | 기본값 | 설명                   |
|:----------- |---------|:----------------------------- |
| **q**       | _해당 없음_   | SQL 쿼리 문자열              |
| p           |         | SQL 쿼리의 `?` 바인드 자리표시자에 넣을 파라미터 JSON 배열. 예: `"p": [2]`. SQL에서는 `?`를 자리표시자로 사용합니다: `SELECT * FROM EXAMPLE WHERE name = ? LIMIT ?` |
| reply       | db/reply| 쿼리 결과를 받을 토픽 |
| format      | json    | 결과 데이터 형식: json, csv, box |
| timeformat  | ns      | 시간 형식: s, ms, us, ns    |
| tz          | UTC     | 시간대: UTC, Local, 지역 지정 |
| compress    | _압축 안 함_   | 압축 방식: gzip      |
| rownum      | false   | rownum 포함: true, false |
| heading     | true    | 헤더 표시: true, false  |
| precision   | -1      | 실수 값의 정밀도. -1은 반올림 없음, 0은 정수 |s

**`format=json`의 추가 파라미터**

이 옵션들은 `format=json`일 때만 사용할 수 있습니다

| 파라미터       | 기본값 | 설명                   |
|:----------- |---------|:----------------------------- |
| transpose   | false   | rows 대신 cols 배열을 생성합니다. |
| rowsFlatten | false   | JSON 객체의 *rows* 필드 배열 차원을 낮춥니다. |
| rowsArray   | false   | 레코드마다 객체 배열만 담은 JSON을 생성합니다.  |

기본 조회 예제는 클라이언트가 `db/reply/#`을 구독하고, *reply* 필드에 `db/reply/my_query`를 지정해 `db/query`로 조회 요청을 발행함으로써 여러 메시지 중 자신의 응답을 구분하는 방법을 보여줍니다.

```json
{
    "q": "select name,time,value from example limit 5",
    "format": "csv",
    "reply": "db/reply/my_query"
}
```

## 클라이언트 예제

### JSH app

> machbase-neo v8.5.0부터 JSH 앱은 기존의 `@jsh/process` / `@jsh/mqtt` 콜백 API 대신 표준 Node.js 방식의 `process`, `mqtt` 모듈(이벤트 기반 `.on()` 핸들러)을 사용합니다.

이 예제에서는 응답 토픽을 구독하고,
SQL 쿼리 요청을 보내 MQTT로 결과를 받는 방법을 배웁니다.

1. **응답 토픽 구독**  
   클라이언트가 먼저 `db/reply/my_query` 같은 응답 토픽을 구독합니다.
   서버는 이 토픽으로 쿼리 결과를 보냅니다.

2. **SQL 쿼리 요청 발행**  
   그다음 클라이언트가 `db/query` 토픽으로 메시지를 발행합니다.
   메시지에는 SQL 쿼리(`q`),
   원하는 결과 형식(`format`),
   결과를 받을 응답 토픽(`reply`)이 포함됩니다.

3. **응답 수신 및 처리**  
   서버가 쿼리를 처리하면
   지정된 응답 토픽으로 결과를 보냅니다.
   클라이언트는 이 메시지를 받아 결과를 출력합니다.

전체 코드 예제는 다음과 같습니다:

```js
const process = require("process");
const mqtt = require("mqtt");

const topicReply = "db/reply/my_query";
const topicQuery = "db/query";
const queryRequest = {
    q: `select name,time,value from example limit 5`,
    format: 'csv',
    reply: topicReply,
};

var client = new mqtt.Client({
    servers: ["tcp://127.0.0.1:5653"],
    keepAlive: 10,
});
client.on('open', () => {
    console.println('---- subscribe:', topicReply);
    client.subscribe(topicReply, {qos:0})
});
client.on('error', (err) => {
    console.println('MQTT ERROR:', err.message);
});
client.on('close', () => {
    console.println('---- disconnected');
});
client.on('subscribed', (topic, reason) => {
    console.println('---- publish:', topicQuery);
    client.publish(topicQuery, JSON.stringify(queryRequest));
});
client.on('message', (msg) => {
    console.println('---- reply')
    console.println(msg.payload);
    client.unsubscribe(msg.topic);
});
client.on('unsubscribed', (topic, reason) => {
    console.println('---- unsubscribed:', topic, 'reason:', reason);
    setTimeout(()=>{
        client.close();
    }, 500)
});
```

실행과 결과:

```sh
/work > ./mqtt_query.js
---- subscribe: db/reply/my_query ----
---- publish: db/query ----
---- reply ----
name,time,value
my-car,1782260468085501458,1.2345
my-car,1782260474814668541,1.35795
my-car,1782260474827077041,1.4814
my-car,1782260474839257291,1.60485

---- unsubscribed: db/reply/my_query reason: 0 ----
---- disconnected ----
```

### Node.js 클라이언트

```sh
npm install mqtt --save
```

```js
const mqtt = require("mqtt");

const client = mqtt.connect("mqtt://127.0.0.1:5653", {
    clean: true,
    connectTimeout: 3000,
    autoUseTopicAlias: true,
    protocolVersion: 5,
});

const sqlText = "SELECT time,value FROM example "+
    "where name = 'neo_cpu.percent' limit 3";

client.on("connect", () => {
    client.subscribe("db/reply/#", (err) => {
        if (!err) {
            const req = {
                q: sqlText,
                format: "box",
                precision: 1,
                timeformat: "15:04:05",
            };
            client.publish("db/query", JSON.stringify(req));
        }
    });
});

client.on("message", (topic, message) => {
    console.log(message.toString());
    client.end();
});
```

```sh
$ node main.js

+----------+-------+
| TIME     | VALUE |
+----------+-------+
| 05:46:19 | 69.4  |
| 05:46:22 | 26.4  |
| 05:46:25 | 42.8  |
+----------+-------+
```

### Go client

**응답용 데이터 구조 정의**

```go
type Result struct {
	Success bool       `json:"success"`
	Reason  string     `json:"reason"`
	Elapse  string     `json:"elapse"`
	Data    ResultData `json:"data"`
}

type ResultData struct {
	Columns []string `json:"columns"`
	Types   []string `json:"types"`
	Rows    [][]any  `json:"rows"`
}
```

**'db/reply' 구독**

```go
client.Subscribe("db/reply", 1, func(_ paho.Client, msg paho.Message) {
    buff := msg.Payload()
    result := Result{}
    if err := json.Unmarshal(buff, &result); err != nil {
        panic(err)
    }
    if !result.Success {
        fmt.Println("RECV: query failed:", result.Reason)
        return
    }
    if len(result.Data.Rows) == 0 {
        fmt.Println("Empty result")
        return
    }
    for i, rec := range result.Data.Rows {
        // do something for each record
        name := rec[0].(string)
        ts := time.Unix(0, int64(rec[1].(float64)))
        value := float64(rec[2].(float64))
        fmt.Println(i+1, name, ts, value)
    }
})
```

**'db/query' 발행**

```go
jsonStr := `{ "q": "select * from EXAMPLE order by time desc limit 5" }`
client.Publish("db/query", 1, false, []byte(jsonStr))
```
