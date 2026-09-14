# Machbase Neo MQTT JavaScript & WebSocket Client

JavaScript 클라이언트로는 MQTT.js GitHub 저장소에서 제공하는 MQTT.js 라이브러리를 사용합니다.

## Node.js

`mqtt.js` 라이브러리를 설치합니다.

```sh
npm install mqtt --save
```

Create `main.js` file.

```js
const mqtt = require("mqtt");

const client = mqtt.connect("mqtt://127.0.0.1:5653", {
    clean: true,
    connectTimeout: 3000,
    autoUseTopicAlias: true,
    protocolVersion: 5,
});

client.on("connect", () => {
    client.subscribe("db/reply/#", (err) => {
        if (!err) {
            const req = {
                q: "SELECT * FROM example where name = 'neo_cpu.percent' limit 3",
                format: "box",
                timeformat: "default",
                tz: "local",
                precision: 2
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

`node` 명령으로 `main.js`를 실행합니다.

```sh
$ node main.js

+-----------------+-------------------------+-------+
| NAME            | TIME                    | VALUE |
+-----------------+-------------------------+-------+
| neo_cpu.percent | 2024-09-06 14:46:19.852 | 69.40 |
| neo_cpu.percent | 2024-09-06 14:46:22.853 | 26.40 |
| neo_cpu.percent | 2024-09-06 14:46:25.852 | 42.80 |
+-----------------+-------------------------+-------+
```

## Websocket

Machbase Neo v8.0.28부터 WebSocket 기반 MQTT를 지원합니다.

프로젝트에 MQTT.js를 포함하려면 다음 스크립트 태그로 CDN에서 불러옵니다:

```html
<script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
````

기본적으로 MQTT의 WebSocket 주소는 Machbase Neo HTTP 서버가 제공하는 `ws://127.0.0.1:5654/web/api/mqtt` 입니다.

```html
<html>

<head>
    <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
</head>

<body>
    <script type="text/javascript">
        const url = 'ws://localhost:5654/web/api/mqtt'

        // Create an MQTT client instance
        const options = {
            // Clean session
            clean: true,
            connectTimeout: 4000,
        }
        const client = mqtt.connect(url, options)
        client.on('connect', function () {
            console.log('Connected')
            // Subscribe to a 'db/reply' topic to receive the result of our query
            client.subscribe('db/reply', function (err) {
                if (!err) {
                    // Publish a query to a topic 'db/query'
                    const req = {q: "SELECT * FROM example limit 10", format:"box", precision: 2}
                    client.publish('db/query', JSON.stringify(req))
                }
            })
        })

        // Receive messages
        client.on('message', function (topic, message) {
            // display the message we received
            document.getElementById("rspQuery").innerHTML = '<pre>'+message.toString()+'</pre>'
            client.end()
        })

    </script>
    <div id="rspQuery"></div>
</body>

</html>
```
