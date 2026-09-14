# Machbase Neo MQTT v3.1 Write Guide

## 토픽 MQTT v3.1/v3.1.1

데이터를 쓰는 토픽의 이름은 대상 테이블 이름을 사용합니다.

JSON 외의 페이로드 형식을 사용하려면 테이블 이름, 페이로드 형식, 압축 방식을 콜론(`:`)으로 구분해 이어 붙여 MQTT 토픽을 구성합니다.

토픽의 전체 문법은 다음과 같습니다:

```
db/{method}/{table}:{format}:{compress}
```

**method**: 데이터를 쓰는 방식은 `append`와 `write` 두 가지입니다.
일반적인 MQTT 환경에서는 `append`를 권장합니다.
- `append`: append 모드로 데이터를 씁니다.
- `write`: INSERT SQL 문으로 데이터를 씁니다.

**format**: 현재 버전의 machbase-neo는 `json`과 `csv`를 지원합니다. 기본 형식은 `json`입니다.

**compress**: 현재 `gzip`을 지원합니다.

**예제**

- `db/append/EXAMPLE`은 `append` 방식으로 `EXAMPLE` 테이블에 데이터를 쓰며 페이로드가 JSON임을 뜻합니다.

- `db/append/EXAMPLE:json`은 위 예와 같습니다. `json`이 기본 형식이므로 끝의 `:json`은 생략할 수 있습니다.

- `db/append/EXAMPLE:json:gzip`은 `append` 방식으로 `EXAMPLE` 테이블에 데이터를 쓰며 페이로드가 gzip 압축된 JSON임을 뜻합니다.

- `db/append/EXAMPLE:csv`는 `append` 방식으로 `EXAMPLE` 테이블에 데이터를 쓰며 페이로드가 CSV임을 뜻합니다.

- `db/write/EXAMPLE:csv`는 `INSERT INTO...` SQL 문으로 `EXAMPLE` 테이블에 데이터를 쓰며 페이로드가 CSV임을 뜻합니다.

- `db/write/EXAMPLE:csv:gzip`은 `INSERT INTO...` SQL 문으로 `EXAMPLE` 테이블에 데이터를 쓰며 페이로드가 gzip 압축된 CSV임을 뜻합니다.


## APPEND 방식

MQTT는 연결 지향 프로토콜이므로 클라이언트 프로그램이 같은 MQTT 세션을 유지하면서 계속 데이터를 보낼 수 있습니다. 
이것이 데이터 쓰기에서 HTTP 대신 MQTT를 쓰는 진짜 이점입니다.

이 예제에서는 시연을 위해 `mosquitto_pub`을 사용합니다.
메시지 하나를 발행할 때마다 MQTT 서버에 연결했다가 끊기 때문입니다.
HTTP `write` API 대비 성능 이득이 거의 없거나 오히려 나쁠 수 있습니다.
클라이언트가 연결을 비교적 오래 유지하며 여러 메시지를 보낼 수 있을 때만 이 MQTT 방식을 사용하세요.

### JSON

**여러 레코드 PUBLISH**

아래 예제의 페이로드 형식은 튜플 배열(JSON의 배열의 배열)입니다.
MQTT 메시지 하나로 여러 레코드를 테이블에 추가합니다.
아래처럼 단일 튜플을 발행할 수도 있습니다. Machbase Neo는 MQTT로 두 형태의 페이로드를 모두 받습니다.

- mqtt-data.json

```json
[
    [ "my-car", 1670380342000000000, 32.1 ],
    [ "my-car", 1670380343000000000, 65.4 ],
    [ "my-car", 1670380344000000000, 76.5 ]
]
```

- mosquitto_pub

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/append/EXAMPLE \
    -f ./mqtt-data.json
```

- JSH app

다음 JSH 앱은 JavaScript에서 MQTT로 Machbase Neo 테이블에 여러 레코드를 발행하는 방법을 보여줍니다.
이 코드는 독립 JSH 스크립트로도, TQL 스크립트의 SCRIPT() 함수로도 실행됩니다.

이 예제는 MQTT와 JSH 애플리케이션으로 Machbase Neo 테이블에 여러 레코드를 효율적으로 보내는 방법을 보여줍니다.
append 방식과 배열 페이로드를 사용하면 높은 처리량으로 데이터를 적재할 수 있어,
IoT와 실시간 데이터 수집 시나리오에 적합합니다.

코드의 주요 부분을 단계별로 설명하면 다음과 같습니다:

```js
// The script imports the required modules and creates an MQTT client
// configured to connect to the local MQTT broker at port 5653.
const system = require("@jsh/system");
const mqtt = require("@jsh/mqtt");
var conf = { serverUrls: ["tcp://127.0.0.1:5653"] };
var client = new mqtt.Client(conf);

// Sets up the publish options:
var pubOpt = {
    topic:"db/write/EXAMPLE", // Data will be written to the EXAMPLE table.
    qos:0,                    // Quality of Service level 0 (at most once).
    properties: {
        user: {
            method: "append", // "append" mode.
            timeformat: "ms", // timestamps are in milliseconds.
        },
    },
};

// Prepares an array of records to be written.
// Each record contains a name,
// a timestamp (in milliseconds), and a value.
ts = (new Date()).getTime();
var pubPayload = [
    [ "my-car", ts+0, 32.1 ],
    [ "my-car", ts+1, 65.4 ],
    [ "my-car", ts+2, 76.5 ],
];

client.onConnect = ()=>{
    // When the client connects to the broker,
    // it publishes the prepared payload to the specified topic
    // with the defined options.
    client.publish(pubOpt, JSON.stringify(pubPayload))
}

// The client connects to the broker (with a 3-second timeout),
// sends the data,
// and then disconnects after ensuring all messages have been sent.
client.connect({timeout:3000});
client.disconnect({timeout:3000});
```

**단일 레코드 PUBLISH**

- mqtt-data.json

```json
[ "my-car", 1670380345000000000, 87.6 ]
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/append/EXAMPLE \
    -f ./mqtt-data.json
```

**gzip JSON PUBLISH**

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/append/EXAMPLE:json:gzip \
    -f mqtt-data.json.gz
```

### NDJSON

NDJSON(Newline Delimited JSON)은 각 줄이 하나의 유효한 JSON 객체인 스트리밍 JSON 형식입니다. 대용량 데이터셋이나 스트리밍 데이터를 처리할 때 유용합니다.
각 줄은 모든 필드 이름이 테이블 컬럼과 일치하는 완전한 JSON 객체여야 합니다.

- mqtt-nd.json

```json
{"NAME":"ndjson-data", "TIME":1670380342000000000, "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":1670380343000000000, "VALUE":2.002}
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/append/EXAMPLE:ndjson \
    -f mqtt-nd.json
```

### CSV

MQTT v3.1에는 첫 줄이 헤더인지 데이터인지 표시할 방법이 없습니다.
따라서 페이로드에는 헤더가 없어야 하며, 모든 필드는 테이블의 컬럼 순서와 일치해야 합니다.

- mqtt-data.csv

```
my-car,1670380346000000000,87.7
my-car,1670380347000000000,98.6
my-car,1670380348000000000,99.9
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/append/EXAMPLE:csv \
    -f mqtt-data.csv
```

**gzip CSV PUBLISH**

Topic = Table + `:csv:gzip`

```csv
my-car,1670380346,87.7
my-car,1670380347,98.6
my-car,1670380348,99.9
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/append/EXAMPLE:csv:gzip \
    -f mqtt-data.csv.gz
```

## INSERT 방식

MQTT에서는 성능을 위해 append 방식 사용을 강력히 권장합니다.
데이터 필드 순서가 테이블 컬럼 순서와 다르거나 모든 컬럼이 맞지 않는 경우에만 `insert` 방식을 고려하세요.

데이터의 필드 개수나 순서가 테이블 컬럼과 다르면,
기본 `append` 방식 대신 `insert` 방식을 사용하세요.

### JSON

`db/write`는 `INSERT INTO table(...) VALUE(...)` SQL 문으로 동작하므로 json 페이로드에 컬럼이 필요합니다.
`data-write.json`의 예는 아래와 같습니다.

- mqtt-data.json
```json
{
  "data": {
    "columns": ["name", "time", "value"],
    "rows": [
      [ "wave.pi", 1687481466000000000, 1.2345],
      [ "wave.pi", 1687481467000000000, 3.1415]
    ]
  }
}
```

Topic `db/write/{table}` is for `INSERT`.

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE \
    -f mqtt-data.json
```

### NDJSON

이 요청 메시지는 `INSERT into {table} (columns...) values (values...)` INSERT SQL 문을 구성하는 것과 같습니다

- mqtt-nd.json

```json
{"NAME":"ndjson-data", "TIME":1670380342000000000, "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":1670380343000000000, "VALUE":2.002}
```

Topic `db/write/{table}:ndjson` is for `INSERT`.

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/append/EXAMPLE:ndjson \
    -f mqtt-nd.json
```

### CSV

테이블 컬럼과 필드 개수나 순서가 다른 CSV 데이터의 insert 방식은 MQTT v5의 사용자 정의 속성으로만 지원됩니다.

```csv
my-car,1670380346000000000,87.7
my-car,1670380347000000000,98.6
my-car,1670380348000000000,99.9
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/write/EXAMPLE:csv \
    -f mqtt-data.csv
```

## TQL

`db/tql/{file.tql}` 토픽은 TQL 파일을 호출하기 위한 것입니다.

데이터베이스에 쓰기 전에 데이터 변환이 필요하면 적절한 *tql* 스크립트를 준비하고 `db/tql/{file.tql}` 이름의 토픽으로 데이터를 발행하세요.

MQTT와 *tql*로 데이터를 쓰는 방법은 쓰기 API 항목을 참고하세요.


## 최대 메시지 크기

MQTT 사양상 PUBLISH 메시지 페이로드의 최대 크기는 256MB입니다. 악의적이거나 오작동하는 클라이언트가 큰 메시지를 계속 보내면 서버의 네트워크 대역폭과 컴퓨팅 자원을 모두 소모해 서비스 불능 상태가 될 수 있습니다. 클라이언트 애플리케이션이 요구하는 크기보다 조금 더 크게 최대 메시지 크기를 설정하는 것이 좋습니다. 기본 MQTT 최대 메시지 크기는 1MB(`1048576`)이며, 아래처럼 명령행 플래그나 설정 파일의 `MaxMessageSizeLimit`로 조정할 수 있습니다.

```sh
machbase-neo serve --mqtt-max-message 1048576
```
