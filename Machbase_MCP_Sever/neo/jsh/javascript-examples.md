# Machbase Neo JavaScript Examples

## HTTP Server

이 예제는 `@jsh/http` 모듈로 간단한 HTTP 서버를 만드는 방법을 보여줍니다.
서버는 지정한 주소와 포트(`127.0.0.1:56802`)에서 수신하며
RESTful API 엔드포인트(`/hello/:name`)를 제공합니다.
클라이언트가 name 파라미터와 함께 이 엔드포인트로 GET 요청을 보내면,
서버는 인사 메시지와 전달받은 이름이 담긴 JSON 객체로 응답합니다.

JavaScript에서 동적 라우팅과 JSON 응답을 갖춘 가벼운 HTTP 서버를 만드는 법을 익히기에 좋은 예제입니다.

**주요 특징:**

1. **데몬화**: 스크립트가 `process.ppid()`로 데몬으로 실행 중인지 확인하고, 아니면 `process.daemonize()`로 스스로 데몬화해 백그라운드에서 실행합니다.
2. **라우팅**: 서버가 라우트(`/hello/:name`)로 URL에서 `name` 파라미터를 추출합니다.
3. **JSON 응답**: 서버가 `name`과 인사 메시지가 담긴 JSON 객체로 응답합니다.

```js
const process = require("@jsh/process");
const {println} = require("@jsh/process");
const http = require("@jsh/http")

// This ensures the server runs as a background process.
if( process.isDaemon() ) { // equiv. if( process.ppid() == 1)
    runServer();
} else {
    process.daemonize({reload:true});
}

function runServer() {
    // Creates an HTTP server bound to the specified address and port.
    const svr = new http.Server({
        network:'tcp',
        address:'127.0.0.1:56802',
    })
    // Route Handling
    svr.get("/hello/:name", ctx => {
        let name = ctx.param("name")
        // Defines a GET route that extracts the `name` parameter
        // from the URL and responds with a JSON object.
        ctx.JSON(http.status.OK, {
            "name": name,
            "message": "greetings",
        })
    })

    // Starts the server and logs the address it is listening on.
    svr.serve( evt => { 
        println("server started", "http://"+evt.address) ;
    });
}
```

**Usage:**

1. 스크립트를 실행해 서버를 시작합니다.
2. `curl` 같은 도구로 서버에 GET 요청을 보냅니다:

```sh
curl -o - http://127.0.0.1:56802/hello/Karl
```

서버는 다음과 같이 응답합니다:

```json
{"message":"greetings","name":"Karl"}
```

### Unix 도메인 소켓

Unix 도메인 소켓 예제는 TCP/IP 네트워크 소켓 대신 Unix 도메인 소켓으로 통신하는 HTTP 서버를 만드는 방법을 보여줍니다.
같은 장비 안에서의 프로세스 간 통신(IPC)에 유용한 방식입니다.

**Workflow:**

1. *Unix 도메인 소켓* 통신:
    - 로컬 통신에 파일 기반 소켓(/tmp/service.sock)을 사용합니다.
2. 효율적인 IPC:
    - 같은 장비의 프로세스들이 네트워크 부담 없이 통신해야 하는 상황에 적합합니다.
3. 도구 호환성:
    - 서버를 테스트하고 다루는 데 curl 같은 도구를 사용할 수 있습니다.

```js
const http = require("@jsh/http");

const svr = new http.Server({
    network: "unix",
    address: "/tmp/service.sock",
});
svr.get("/hello/:name", (ctx) => {
    const name = ctx.param("name");
    ctx.JSON(http.status.OK, { message: `Hello, ${name}!` });
});
svr.serve();
```

curl로 Unix 도메인 소켓을 통해 서버에 요청을 보냅니다:

```sh
curl -o - --unix-socket /tmp/service.sock http://localhost/hello/Karl
```

### 정적 콘텐츠

```js
svr.staticFile("/readme", "/path/to/file.txt");
svr.static("/static", "/path/to/static_dir");
```

### Redirect

```js
svr.get("/readme", ctx => {
    ctx.redirect(http.status.Found, "/docs/readme.html");
});
```

### RESTful API

```js
svr.get("/movies", ctx => {
    list = [
        {title:"Indiana Jones", id: 59793, studio: ["Paramount"]},
        {title:"Star Wars", id: 64821, studio: ["Lucasfilm"]},
    ]
    ctx.JSON(http.status.OK, list);
})
svr.post("/movies", ctx => {
    obj = ctx.request.body;
    console.log("post:", JSON.stringify(obj));
    ctx.JSON(http.status.Created, {success: true});
});
svr.delete("/movies/:id", ctx => {
    let id = ctx.param("id");
    console.log("delete:", id)
    ctx.TEXT(http.status.NoContent, "Deleted.")
})
```

- GET
```sh
curl -o - http://127.0.0.1:56802/movies
```
```json
[
  { "id": 59793, "studio": [ "Paramount" ], "title": "Indiana Jones" },
  { "id": 64821, "studio": [ "Lucasfilm" ], "title": "Star Wars" }
]
```

- POST

```sh
curl -o - -X POST http://127.0.0.1:56802/movies \
    -H "Content-Type: application/json" \
    -d '{"title":"new movie", "id":12345, "studio":["Unknown"]}'
```

- DELETE

```sh
curl -v -o - -X DELETE http://127.0.0.1:56802/movies/12345
```

```sh
< HTTP/1.1 204 No Content
< Content-Type: text/plain; charset=utf-8
< Date: Thu, 08 May 2025 20:39:34 GMT
<
```

### HTML 템플릿

이 줄은 서버가 `/*.html` 패턴에 맞는 모든 HTML 템플릿 파일을 불러오도록 합니다.
이 템플릿들로 서버는 미리 정의된 레이아웃과 런타임 데이터를 결합해 HTML 응답을 동적으로 생성합니다.

```js
svr.loadHTMLGlob("/*.html")

// Defines a GET route /movielist that serves an HTML page.
svr.get("/movielist", ctx => {
    obj = {
        subject: "Movie List",
        list: [
            {title:"Indiana Jones", id: 59793, studio: ["Paramount"]},
            {title:"Star Wars", id: 64821, studio: ["Lucasfilm"]},
        ]
    }
    ctx.HTML(http.status.OK, "movie_list.html", obj)
})
```

- HTML 템플릿 코드 `movie_list.html`

```html
<html>
    <body>
        <h1>{{.subject}}</h1>
        <ol>
        {{range .list }}
            <li> {{.id}} {{.title}} {{.studio}}
        {{end}}
        </ol>
    </body>
</html>
```

`/movielist` 엔드포인트로 GET 요청을 보냅니다.
서버는 `movie_list.html` 템플릿과 `obj` 데이터로 생성한 HTML 페이지로 응답합니다.

```sh
curl -o - http://127.0.0.1:56802/movielist
```

```html
<html>
    <body>
        <h1>Movie List</h1>
        <ol>
            <li> 59793 Indiana Jones [Paramount]
            <li> 64821 Star Wars [Lucasfilm]
        </ol>
    </body>
</html>
```

## HTTP Client

이 예제는 `@jsh/http` 모듈로 HTTP 클라이언트를 만드는 방법을 보여줍니다.
클라이언트가 지정한 URL로 GET 요청을 보내고 서버 응답을 처리합니다.
JavaScript에서 HTTP 요청을 처리하고 JSON 응답을 파싱하는 방법을 보여줍니다.

JavaScript에서 HTTP 클라이언트를 만들고, 응답을 처리하고, JSON 데이터를 파싱하는 법을 익히기에 좋은 예제입니다.

**주요 특징:**

1. **요청 처리**: 클라이언트가 서버로 HTTP GET 요청을 보냅니다.
2. **응답 파싱**: 응답을 파싱해 상태, 헤더, 본문 내용 등을 추출합니다.
3. **오류 처리**: 요청 중 발생할 수 있는 오류를 처리하기 위해 `try-catch` 블록을 포함합니다.

```js
const {println} = require("@jsh/process");
const http = require("@jsh/http")
try {
    // Creates an HTTP GET request to the specified URL.
    req = http.request("http://127.0.0.1:56802/hello/Steve")
    // Logs the URL, status, and headers.
    // Parses the response body as JSON 
    // and logs the `message` and `name` fields.
    req.do((rsp) => {
        // url: http://127.0.0.1:56802/hello/Steve
        println("url:", rsp.url);
        // error: <nil>
        println("error:", rsp.error());
        // status: 200
        println("status:", rsp.status);
        // statusText: 200 OK
        println("statusText:", rsp.statusText);
        // content-type: application/json; charset=utf-8
        println("content-type:", rsp.headers["Content-Type"]);
        obj = rsp.json(); // parse content body to JSON object
        // greetings, Steve
        println("body:", `${obj.message}, ${obj.name}`);
    })
} catch (e) {
    // Catches and logs any errors that occur during the request.
    println(e);
}
```

**Usage:**

1. HTTP 서버가 실행 중인지 확인합니다 (HTTP 서버 예제 참고).
2. 스크립트를 실행해 서버로 GET 요청을 보냅니다.

### Unix 도메인 소켓

Unix 도메인 소켓으로 서버에 연결하려면 `{unix: "/path/to/unix_domain_socket/file"}` 옵션을 사용하세요.

```js
const {println} = require("@jsh/process");
const http = require("@jsh/http")
try {
    req = http.request("http://localhost/movies", {unix:"/tmp/test.sock"})
    req.do((rsp) => {
        obj = rsp.json();
        println(JSON.stringify(obj))
    })
} catch (e) {
    println(e.toString());
}
```

## MQTT 발행자

- 애플리케이션을 `mqtt.js`로 만듭니다.

```js
const mqtt = require("@jsh/mqtt");
const process = require("@jsh/process");
const system = require("@jsh/system")

const log = new system.Log("mqtt-demo");
const testTopic = "test/string";

var client = new mqtt.Client({
    serverUrls: ["tcp://127.0.0.1:5653"],
});

try {
    client.onConnectError = err => { log.error("connect error", err); }
    client.onClientError = err => { log.error("client error", err); }
    client.onConnect = (ack) => { log.info("client connected"); }

    client.connect({timeout: 3*1000});
    
    for(i = 0; i < 10; i++) {
        process.sleep(1000);
        r = client.publish({topic: testTopic, qos: 1}, 'Hello World:'+i)
    }
} catch (e) {
    log.error("Error:", e.message);
} finally {
    client.disconnect()
}
```

## MQTT 구독자

MQTT 구독자 예제는 MQTT 브로커에 접속해
특정 토픽을 구독하고 들어오는 메시지를 처리하는 백그라운드 애플리케이션을 만드는 방법을 보여줍니다.
`@jsh/process`와 `@jsh/mqtt` 모듈을 사용해 스크립트가 데몬으로 실행되어 백그라운드에서 동작합니다.
연결 수립, 메시지 수신, 연결 종료 같은 이벤트를 처리하며 JavaScript로 견고하고 효율적인 MQTT 클라이언트를 만드는 방법을 보여줍니다.
실시간 메시지 처리와 가벼운 백그라운드 작업이 필요한 상황에 적합한 예제입니다.

- 애플리케이션을 `mqtt-sub.js`로 만듭니다.

```js
// This script creates a background MQTT subscriber that connects
// to a broker, subscribes to a topic (test/topic),
// and processes incoming messages.
// It demonstrates how to handle connection events, errors,
// and message reception efficiently using JavaScript.
//
// Provides utilities for process management,
// such as daemonizing and printing.
const process = require("@jsh/process");
const system = require("@jsh/system")
const log = new system.Log("mqtt-demo");
// Provides MQTT client functionality for connecting to brokers
// and handling messages.
const mqtt = require("@jsh/mqtt");

// Checks the parent process ID.
// If the process is already running as a daemon.
if( process.isDaemon() ) {  // equiv. if( process.ppid() == 1)
    // If the process is a daemon, it calls runBackground() to start
    // the MQTT subscriber logic.
    log.info("mqtt-sub start...");
    runBackground();
    log.info("mqtt-sub terminated.");
} else {
    // If the process is not a daemon, process.daemonize() is called to
    // restart the process as a background daemon.
    process.daemonize();
}

// Defines the main function for the MQTT subscriber logic.
function runBackground() {
    // A variable to hold the MQTT client instance.
    var client = new mqtt.Client({
        serverUrls: ["tcp://127.0.0.1:5653"],
    });
    try {
        // Triggered if there is an error during connection.
        client.onConnectError = err => { log.warn("connect error", err); }
        // Triggered when the client disconnects from the broker.
        client.onDisconnect = () => { log.info("disconnected."); }
        // Triggered when the client successfully connects to the broker.
        var count = 0;
        client.onConnect = ack => {
            log.info("connected.", ack.reasonCode);
            // It subscribes to the test/topic with QoS level 2.
            r = client.subscribe({subscriptions:[{topic:'test/topic', qos: 2}]})
            log.info("subscribe", 'test/topic', "result", r);
            client.onMessage = msg => {
                // Triggered when a message is received.
                // It logs the topic, QoS, and payload of the message.
                log.info("recv topic:", msg.topic,"payload:", msg.payload.string())
                count++;
                return true;
            }
        }

        // Initiates the connection to the MQTT broker.
        client.connect({timeout: 3*1000});

        // publish test messages to the topic.
        for( let i = 0; i < 10; i++) {
            client.publish({topic:'test/topic', qos: 1}, "test num="+i);
        }
        // wait the subscriber receives all messages.
        while(true) {
            if(count >= 10) break;
            process.sleep(100);
        }
        // unsubscribe
        client.unsubscribe({topics:['test/topic']})
        // disconnect
        client.disconnect()
    } catch (e) {
        log.error("Error", e.message);
    }
}
```

## Machbase 클라이언트

이 예제는 포트 5656으로 다른 Machbase 인스턴스에 접속해 쿼리를 실행하는 방법을 보여줍니다.

8번째 줄에서 `lowerCaseColumns: true`를 설정하면 21번째 줄처럼 조회 결과의 레코드 객체가 소문자 속성 이름을 사용합니다.

`dataSource`는 과거 호환을 위해 두 가지 형식을 지원합니다. 첫 번째는 세미콜론 구분자, 두 번째는 공백 구분자를 사용하며 둘은 동일합니다.

1. 전통 형식: `SERVER=${host};PORT_NO=${port};UID=${user};PWD=${pass}`
2. Name=Value 형식: `host=<ip> port=<port> user=<username> password=<pass>`

```js
db = require("@jsh/db");
host = "192.168.0.207"
port = 5656
user = "sys"
pass = "manager"
client = db.Client({
    driver: "machbase",
    dataSource: `host=${host} port=${port} user=${user} password=${pass}`,
    lowerCaseColumns: true
})

try {
    sqlText = "select * from example where name = ? limit ?,?";
    tag = "my-car";
    off = 10;
    limit = 5;

    conn = client.connect()
    rows = conn.query(sqlText, tag, off, limit)
    for( rec of rows) {
        console.log(rec.name, rec.time, rec.value)
    }
} catch(e) {
    console.error(e.message)
} finally {
    rows.close()
    conn.close()
}
```

## Machbase Append

```js
const db = require("@jsh/db");
const { now, parseTime } = require("@jsh/system");

client = new db.Client({lowerCaseColumns:true});
var conn = null;
var appender = null;
try{
    console.log("supportAppend:", client.supportAppend);
    conn = client.connect();
    appender = conn.appender("example", "name", "time", "value");
    let ts = (new Date()).getTime(); // unix epoch (ms.)
    for (let i = 0; i < 100; i++) {
        // add 10 millisec.
        ts = ts + 10;
        // name, time, value
        appender.append("tag-append", parseTime(ts, "ms"), i);
    }
} catch(e) {
    console.log("Error:", e);
} finally {
    if (appender) appender.close();
    if (conn) conn.close();
}
console.log("append:", appender.result());

// supportAppend: true
// append: {success:100, fail:0}
```

## SQLite 클라이언트

이 예제는 `@jsh/db` 모듈로 메모리 내 SQLite 데이터베이스를 다루는 방법을 보여줍니다.
테이블 생성, 데이터 입력, 조회를 다룹니다.
JavaScript에서 SQLite로 기본적인 데이터베이스 작업을 하는 법을 익히기에 좋은 예제입니다.

```js
const db = require("@jsh/db");

// Intializes a new SQLite client with an in-memory database.
client = new db.Client({
    driver:"sqlite",
    dataSource:"file::memory:?cache=shared"
});

try{
    conn = client.connect()
    // Creates a table named `mem_example`
    // with three columns: `id`, `company`, and `employee`.
    conn.exec(`
        CREATE TABLE IF NOT EXISTS mem_example(
            id         INTEGER NOT NULL PRIMARY KEY,
            company    TEXT,
            employee   INTEGER
        )
    `);

    // Inserts a record into the `mem_example` table with the values
    // `'Fedel-Gaylord'` for `company` and `12` for `employee`.
    conn.exec(`INSERT INTO mem_example(company, employee) values(?, ?);`, 
        'Fedel-Gaylord', 12);

    // Queries all rows from the `mem_example` table and logs 
    // the results to the console.
    rows = conn.query(`select * from mem_example`);
    for( rec of rows ) {
        console.log(...rec)
    }
}catch(e){
    // Handles any errors that occur during database operations 
    console.error(e.message);
}finally{
    // Ensures that the `rows` and `conn` objects are closed 
    // to release resources.
    rows.close();
    conn.close();
}
```

스크립트를 실행하면 입력된 레코드가 출력됩니다:
```plaintext
1 Fedel-Gaylord 12
```

## PostgreSQL 클라이언트

```js
const db = require("@jsh/db");
const { now, parseTime } = require("@jsh/system");

client = new db.Client({
    driver: "postgres",
    dataSource: "host=127.0.0.1 port=15455 dbname=db user=dbuser password=dbpass sslmode=disable",
    lowerCaseColumns:true,
});
var conn = null;
var rows = null;
try{
    conn = client.connect();
    r = conn.exec("CREATE TABLE test (id SERIAL PRIMARY KEY, name TEXT)");
    console.log("create table:", r.message);
    // create table: Created successfully.

    r = conn.exec("INSERT INTO test (name) VALUES ($1)", "foo")
    console.log("insert foo:", r.message, r.rowsAffected);
    // insert foo: a row inserted. 1

    r = conn.exec("INSERT INTO test (name) VALUES ($1)", "bar")
    console.log("insert bar:", r.message, r.rowsAffected);
    // insert bar: a row inserted. 1

    rows = conn.query("SELECT * FROM test ORDER BY id");
    console.log("cols.names:", JSON.stringify(rows.columnNames()));
    // cols.names: ["id","name"]

    for (const rec of rows) {
        console.log(...rec);
    }
    // 1 foo
    // 2 bar
} catch(e) {
    console.log("Error:", e.message);
} finally {
    if(rows) rows.close();
    if(conn) conn.close();
}
```

## 시스템 모니터링

### 데이터 수집기

시스템 모니터링 예제는 `@jsh/process`와 `@jsh/psutil` 모듈로 가벼운 시스템 모니터링 도구를 만드는 방법을 보여줍니다.
이 스크립트는 백그라운드 데몬으로 실행되며 CPU 사용률, 메모리 사용률, 최근 1·5·15분 부하 평균 같은 주요 시스템 지표를 주기적으로 수집합니다.

모니터링 작업은 cron과 유사한 문법으로 15초마다 실행되도록 예약됩니다.
수집된 데이터는 타임스탬프와 함께 서식화되어 출력되며, 일정 간격으로 시스템 성능의 스냅샷을 제공합니다.
이 예제는 JavaScript로 효율적인 프로세스 관리와 실시간 시스템 모니터링을 구현하는 방법을 보여줍니다.

예제 코드를 `sysmon.js`로 저장하고 `JSH` 터미널에서 실행합니다.
시스템 부하 평균, CPU 사용률, 메모리 사용률을 "EXAMPLE" 테이블에 저장합니다.

```sh
jsh / > sysmon
jsh / > ps
┌──────┬──────┬──────┬─────────────────┬──────────┐ 
│  PID │ PPID │ USER │ NAME            │ UPTIME   │ 
├──────┼──────┼──────┼─────────────────┼──────────┤ 
│ 1040 │ 1    │ sys  │ /sysmon.js      │ 2h37m43s │ 
│ 1042 │ 1025 │ sys  │ ps              │ 0s       │ 
└──────┴──────┴──────┴─────────────────┴──────────┘ 
```

- sysmon.js

```js
const process = require("@jsh/process");
const psutil = require("@jsh/psutil");
const db = require("@jsh/db");
const system = require("@jsh/system");

const tableName = "EXAMPLE";
const tagPrefix = "sys_";

// Checks the parent process ID. If it equals 1,
// the process is already running as a daemon.
if( process.isDaemon() ) {
    // If it is already a daemon,
    // the `runSysmon()` function is executed to start
    // system monitoring.
    runSysmon();
} else {
    // If the process is not a daemon,
    // `process.daemonize()` is called to restart the process
    // as a background daemon.
    process.daemonize({reload:true});
}

function runSysmon() {
  // Schedules a task to run at specific intervals.
  // Here, it runs every 15 seconds (0,15,30,45 in the cron-like syntax).
  // The callback function receives a UNIX epoch (tick) in milliseconds
  // for when the task is executed
  process.schedule("0,15,30,45 * * * * *", (tick) => {
    // Retrieves the system's load averages for the past 1,5 and 15 minutes.
    // The values are destructured into load1, load5, and load15.
    let {load1, load5, load15} = psutil.loadAvg();
    // Retrieves information about virtual memory usage,
    // including total, used, and free memory.
    let mem = psutil.memVirtual();
    // Calculates the CPU usage percentage since the last call.
    // The first argument (0) specifies the interval in seconds,
    // if it is 0 like this example, it calculates from the previous call.
    // the second argument (false) disables per-CPU statistics.
    let cpu = psutil.cpuPercent(0, false);
    // Convert current time from milliseconds UNIX epoch to native time.
    let ts = system.parseTime(tick, "ms")
    try{
      client = new db.Client({lowerCaseColumns:true});
      conn = client.connect();
      appender = conn.appender(tableName, "name","time","value");
      appender.append(tagPrefix+"load1", ts, load1);
      appender.append(tagPrefix+"load5", ts, load5);
      appender.append(tagPrefix+"load15", ts, load15);
      appender.append(tagPrefix+"cpu", ts, cpu[0]);
      appender.append(tagPrefix+"mem", ts, mem.usedPercent);
    } finally {
      appender.close();
      conn.close();
    }
  })
}
```

### Chart TQL

시스템 사용량 데이터가 데이터베이스에 저장되므로 조회와 시각화가 간단해집니다.

```js
SQL(`select time, value from EXAMPLE
    where name = ? and time between ? and ?`, 
    "sys_load1", time("now -12000s"), time("now"))
MAPVALUE(0, list(value(0), value(1)))
POPVALUE(1)
CHART(
    size("500px", "300px"),
    chartJSCode({
        function yformatter(val, idx){ return val.toFixed(1) }
    }),
    chartOption({
        animation: false,
        yAxis: { type: "value", axisLabel:{ formatter: yformatter }},
        xAxis: { type: "time", axisLabel:{ rotate: -90 }},
        series: [
            {type: "line", data: column(0), name: "LOAD1", symbol:"none"},
        ],
        tooltip: {trigger: "axis", valueFormatter: yformatter},
        legend: {}
    })
)
```

### SCRIPT()를 사용한 차트 TQL

```js
SCRIPT({
    const db = require("@jsh/db");
    const client = new db.Client();
    const tags = [ "load1", "load5", "load15" ];
    const end = (new Date()).getTime();
    const begin = end - 240*(60*1000);
    var result = {};
    try {
        conn = client.connect();
        for(tag of tags) {
            rows = conn.query(`
                select time, value from example
                where name = 'sys_${tag}'
                and time between ${begin}000000 and ${end}000000`);
            lst = [];
            for( r of rows ) lst.push([r.time, r.value]);
            if(rows) rows.close();
            result[tag] = lst;
        }
    } catch(e) {
        console.log(e.message);
    } finally {
        if(conn) conn.close();
    }
    $.yield({
      animation: false,
      yAxis: { type: "value", axisLabel:{ }},
      xAxis: { type: "time", axisLabel:{ rotate: -90 }},
      series: [
        {type:"line", data:result.load1, name:"LOAD1", symbol:"none", smooth:true},
        {type:"line", data:result.load5, name:"LOAD5", symbol:"none", smooth:true},
        {type:"line", data:result.load15, name:"LOAD15", symbol:"none", smooth:true},
      ],
      tooltip: {trigger: "axis"},
      legend: {}
    });
})
CHART( size("500px", "300px") )
```

### HTML 속 차트 TQL

다음 HTML 코드를 `sysmon.html`로 저장하고 웹 브라우저에서 열면 시스템 모니터링 데이터를 시각화할 수 있습니다.

- sysmon.html

```html
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>System Monitoring Chart</title>
  <script src="/web/echarts/echarts.min.js"></script>
  <script>
    function loadJS(url) {
      var scriptElement = document.createElement('script');
      scriptElement.src = url;
      document.getElementsByTagName('body')[0].appendChild(scriptElement);
      }
    function buildTQL(table, tag, begin, end, format) {
      return `
      SQL("select time, value from ${table} "+
        "where name = '${tag}' "+
        "and time between ${begin}000000 and ${end}000000")
      MAPVALUE(1, list(value(0), value(1)))
      CHART(
        size("400px", "200px"),
        chartJSCode({
            function unitFormat(val){
                return val.toFixed(1);
            }
            function percentFormat(val) {
                return ""+val.toFixed(0)+"%";
            }
        }),
        chartOption({
            animation: false,
            yAxis: { type: "value", axisLabel:{ formatter:${format} }},
            xAxis: { type: "time", axisLabel:{ rotate: -90 }},
            series: [
              {type:"line", data:column(1), name:"${tag}", symbol:"none"},
            ],
            tooltip: {trigger: "axis", valueFormatter:${format} },
            legend: {}
        })
      )`
    }
    function loadChart(containerID, table, tag, begin, end, format) {
      fetch('/db/tql',
        {method:"POST", body: buildTQL(table, tag, begin, end, format)}
      )
      .then(response => {
        return response.json()
      })
      .then(obj => {
        const container = document.getElementById(containerID)
        const chartDiv = document.createElement('div')
        chartDiv.setAttribute("id", obj.chartID)
        chartDiv.style.width = obj.style.width
        chartDiv.style.height = obj.style.height
        container.appendChild(chartDiv)
        obj.jsCodeAssets.forEach((js) => loadJS(js))
      })
      .catch(error => {
        console.error('Error fetching chart data:', error);
      });
    }
   </script>
</head>
<body>
  <div style='display:flex;float:left;flex-flow:row wrap'>
    <div id="chart1" style="width: 400px; height: 200px;"></div>
    <div id="chart2" style="width: 400px; height: 200px;"></div>
    <div id="chart3" style="width: 400px; height: 200px;"></div>
    <div id="chart4" style="width: 400px; height: 200px;"></div>
  </div>
  <script>
    let end = (new Date()).getTime(); // now in millisec.
    let begin = end - 30*(60*1000);   // 30 minutes before
    loadChart('chart1', "EXAMPLE", "sys_load1", begin, end, "unitFormat")
    loadChart('chart2', "EXAMPLE", "sys_load5", begin, end, "unitFormat")
    loadChart('chart3', "EXAMPLE", "sys_cpu", begin, end, "percentFormat")
    loadChart('chart4', "EXAMPLE", "sys_mem", begin, end, "percentFormat")
  </script>
</body>
</html>
```

### HTML 템플릿 속 차트

이 예제는 차트가 포함된 HTML 페이지를 제공하는 HTTP 서버 라우트(`/sysmon`)를 만드는 방법을 보여줍니다.
서버는 데이터베이스에서 부하 평균 같은 시스템 모니터링 데이터를 가져와
ECharts 라이브러리로 차트를 동적으로 생성합니다.
HTML 템플릿(`http-sysmon.html`)에 가져온 데이터가 채워져,
`load1`, `load5`, `load15` 같은 시스템 지표를 실시간으로 시각화할 수 있습니다.
이 방식은 서버 측 데이터 처리와 클라이언트 측 차트 렌더링을 결합해 효과적으로 데이터를 시각화하는 방법을 보여줍니다.

- `sysmon-server.js`
```js
const process = require("@jsh/process");
const http = require("@jsh/http")
const db = require("@jsh/db")

if( process.isDaemon() ) {  // equiv. if( process.ppid() == 1)
    runServer();
} else {
    process.daemonize({reload:true});
}

function runServer() {
    const tags = [ "load1", "load5", "load15", "cpu", "mem" ];
    const svr = new http.Server({address:'127.0.0.1:56802'})
    svr.loadHTMLGlob("/*.html")
    svr.get("/sysmon", ctx => {
        const end = (new Date()).getTime();
        const begin = end - 20*(60*1000); // last 20 min.
        var result = {};
        try {
            client = new db.Client({lowerCaseColumns:true});
            conn = client.connect();
            for( tag of tags ) {
                rows = conn.query(`
                    select time, value from example
                    where name = 'sys_${tag}'
                    and time between ${begin}000000 and ${end}000000`)
                lst = [];
                for( r of rows ) lst.push([r.time, r.value]);
                if(rows) rows.close();
                result[tag] = lst;
            }
        } catch(e) {
            console.log(e);
        } finally {
            if (conn) conn.close();
        }
        ctx.HTML(http.status.OK, "http-sysmon.html", result)
    })
    svr.serve( (result)=>{ 
        console.log("server started", "http://"+result.address) ;
    });
}
```

- `http-sysmon.html`

```html
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.6.0/dist/echarts.min.js"></script>
</head>
<body>
<div style='display:flex;float:left;flex-flow:row wrap;width:100%;'>
    <div id="load" style="width:400px;height:300px;margin:4px;"></div>
    <div id="cpu" style="width:400px;height:300px;margin:4px;"></div>
    <div id="mem" style="width:400px;height:300px;margin:4px;"></div>
</div>
<script>
    function doChart(element, title, data) {
        let chart = echarts.init(element, "dark");
        chart.setOption({
            animation:false, "color":["#80FFA5", "#00DDFF", "#37A2FF"],
            title:{"text":title},
            legend:{ bottom: 7 }, tooltip:{"trigger":"axis"},
            xAxis:{type:"time", axisLabel:{ rotate: -90 }},
            yAxis:{type:"value"},
            series: data,
        });
    }
    doChart(document.getElementById('load'), "System Load Avg.", [
        { type:"line", name:"load1", symbol:"none", data:{{.load1}} },
        { type:"line", name:"load5", symbol:"none", data:{{.load5}} },
        { type:"line", name:"load15", symbol:"none", data:{{.load15}} },
    ])
    doChart(document.getElementById('cpu'), "CPU Usage", [
        { type:"line", name:"cpu usage", symbol:"none", data:{{.cpu}} },
    ])
    doChart(document.getElementById('mem'), "Memory Usage", [
        { type:"line", name:"mem usage", symbol:"none", data:{{.mem}} },
    ])
</script>
</body>
</html>
```

## OPC UA 클라이언트

OPC UA 클라이언트 예제는 OPC UA 서버에 접속해 시스템 지표를 가져오고, 이후 분석·시각화를 위해 데이터베이스에 저장하는 데이터 수집기를 만드는 방법을 보여줍니다. 

**Workflow:**

1. OPC UA 연동:
    - `@jsh/opcua` 모듈로 OPC UA 서버에 접속해 데이터를 읽습니다.
    - 스크립트가 `opc.tcp://localhost:4840`의 OPC UA 서버에 접속합니다.
    - 특정 노드(`cpu_percent`, `mem_percent`, `load1` 등)를 읽어 시스템 지표를 가져옵니다.
2. 예약된 데이터 수집:
    - cron과 유사한 일정으로 OPC UA 서버에서 주기적으로 데이터를 가져옵니다.
    - `process.schedule`로 10초마다 실행되는 작업을 예약합니다.
    - 매 주기마다 지정한 노드의 값을 읽어 데이터베이스에 저장합니다.
3. 데이터베이스 저장:
    - 수집한 데이터를 영속 저장과 분석을 위해 데이터베이스 테이블(`EXAMPLE`)에 저장합니다.
    - 수집 데이터는 `name`, `time`, `value` 컬럼과 함께 `EXAMPLE` 테이블에 입력됩니다.
4. 데이터 시각화:
    - 수집한 데이터는 *시스템 모니터링* 예제의 차트 예제로 시각화할 수 있습니다.
    - 저장된 데이터는 *시스템 모니터링* 예제의 차트 예제로 시각화할 수 있습니다. 예를 들어 제공된 TQL 또는 HTML 차트 예제로 CPU 사용률, 메모리 사용률, 부하 평균 같은 지표를 표시할 수 있습니다.

### 데이터 수집기

스크립트를 opcua-client.js로 저장하고 JSH 터미널에서 백그라운드로 실행합니다:

```
jsh / > opcua-client
jsh / > ps
┌──────┬──────┬──────┬──────────────────┬────────┐ 
│  PID │ PPID │ USER │ NAME             │ UPTIME │ 
├──────┼──────┼──────┼──────────────────┼────────┤ 
│ 1044 │ 1    │ sys  │ /opcua-client.js │ 13s    │ 
│ 1045 │ 1025 │ sys  │ ps               │ 0s     │ 
└──────┴──────┴──────┴──────────────────┴────────┘ 
```

- opcua-client.js

```js
opcua = require("@jsh/opcua");
process = require("@jsh/process");
system = require("@jsh/system");
db = require("@jsh/db");

if( process.isDaemon() ) {  // equiv. if( process.ppid() == 1)
  runClient();
} else {
  process.daemonize({reload:true});
}

function runClient() {
  const nodes = [
    "ns=1;s=sys_cpu",
    "ns=1;s=sys_mem",
    "ns=1;s=load1",
    "ns=1;s=load5",
    "ns=1;s=load15",
  ];
  const tags = [
    "sys_cpu", "sys_mem", "sys_load1", "sys_load5", "sys_load15"
  ];
  const tableName = "EXAMPLE";
  try {
    uaClient = new opcua.Client({ endpoint: "opc.tcp://localhost:4840" });
    dbClient = new db.Client({lowerCaseColumns:true});
    conn = dbClient.connect();
    
    process.schedule("0,10,20,30,40,50 * * * * *", tick => {
      ts = system.parseTime(tick, "ms")
      vs = uaClient.read({
        nodes: nodes,
        timestampsToReturn: opcua.TimestampsToReturn.Both
      });
      sqlText = `INSERT INTO ${tableName} (name,time,value) values(?,?,?)`
      vs.forEach((v, idx) => {
        if( v.value !== null ) {
            conn.exec(sqlText, tags[idx], ts, v.value);
        }
      })
    })
  } catch (e) {
    process.println("Error:", e.message);
  } finally {
    conn.close();
    uaClient.close();
  }
}
```

### 시뮬레이터 서버

`opcua-client.js`를 테스트하려면 필요한 시스템 지표 노드를 제공하는 OPC UA 서버가 실행 중이어야 합니다.

편의를 위해 시뮬레이터 서버가 제공됩니다.
이 시뮬레이터는 실제 OPC UA 서버를 모사해 노드에 대한 샘플 데이터를 제공합니다
such as `sys_cpu`, `sys_mem`, `load1`, `load5`, and `load15`.

시뮬레이터를 사용하면 실제 OPC UA 장비 없이도
데이터 수집기와 시각화 작업 흐름을 개발하고 테스트할 수 있습니다.

시뮬레이터 서버 코드와 설정 방법은 다음 저장소에서 확인할 수 있습니다:

https://github.com/machbase/neo-server/tree/main/mods/jsh/opcua/test_server

`opcua-client.js` 스크립트를 실행하기 전에 저장소의 안내를 따라 시뮬레이터 서버를 시작하세요.
그러면 테스트와 시연을 위해 OPC UA 클라이언트가 정상적으로 접속해 데이터를 수집할 수 있습니다.

## Statistics

다음 TQL 예제는 JSH `@jsh/analysis` 모듈로 숫자 배열에 기본 통계 분석을 수행하는 방법을 보여줍니다.
이 예제는 평균, 중앙값, 분산, 표준편차 같은 일반적인 통계를 계산해 출력하며,
이는 데이터의 분포와 퍼짐을 이해하는 데 필수적입니다.

- 샘플 값 배열을 정의합니다.
- 스크립트가 `@jsh/analysis` 모듈의 함수로 다음을 계산합니다:
  - **평균(Mean)**: 데이터셋의 평균값.
  - **분산(Variance)**: 값들이 평균에서 얼마나 떨어져 있는지를 나타내는 척도.
  - **표준편차(Standard Deviation)**: 분산의 제곱근으로 데이터의 퍼짐을 나타냅니다.
  - **중앙값(Median)**: 데이터를 정렬했을 때의 가운데 값.
- 각 통계 결과를 `$.yield()`로 출력해 이후 처리나 내보내기(예: CSV)에 사용할 수 있게 합니다.

```js
SCRIPT({
    const system = require("@jsh/system");
    const ana = require("@jsh/analysis");
    xs = ana.sort([
		32.32, 56.98, 21.52, 44.32,
		55.63, 13.75, 43.47, 43.34,
		12.34,
    ]);
    $.yield("data", JSON.stringify(xs))

    mean = ana.mean(xs)
    variance = ana.variance(xs)
    stddev = Math.sqrt(variance)

    median = ana.quantile(0.5, xs)

    $.yield("mean", mean)
    $.yield("median", median)
    $.yield("variance", variance)
    $.yield("std-dev", stddev)
})
CSV()

// data     [12.34,13.75,21.52,32.32,43.34,43.47,44.32,55.63,56.98]
// mean     35.96333333333334
// median   43.34
// variance 285.306875
// std-dev  16.891029423927957
```
