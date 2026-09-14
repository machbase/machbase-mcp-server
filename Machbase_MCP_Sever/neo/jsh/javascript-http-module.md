# Machbase Neo JavaScript HTTP Module

## request()

HTTP 클라이언트 요청을 간편하게 보내는 함수입니다.

**문법**

```js
request(url, option)
```

**파라미터**

- `url` `String` 대상 주소. 예: `http://192.168.0.120/api/members`
- `option` `Object` 선택적 ClientRequestOption.

**반환값**

- `Object` ClientRequest

**사용 예제**

```js
const {println} = require("@jsh/process");
const http = require("@jsh/http")
try {
    req = http.request("http://127.0.0.1:29876/hello")
    req.do((rsp) => {
        println("url:", rsp.url);
        println("error:", rsp.error());
        println("status:", rsp.status);
        println("statusText:", rsp.statusText);
        println("body:", rsp.text());
    })
} catch (e) {
    println(e.toString());
}
```

## Client

HTTP 클라이언트입니다.

**생성**

| 생성자             | 설명                          |
|:------------------------|:-------------------------------------|
| new Client()            | HTTP 클라이언트를 생성합니다           |

### do()

do() 함수는 지정한 URL로 HTTP 요청을 보내고 응답을 처리하는 HTTP 클라이언트의 메서드입니다.
선택적 요청 옵션(method, headers, body 등)과 응답을 처리할 콜백 함수를 지원합니다.

**문법**

```js
client.do(url)
client.do(url, option)
client.do(url, option, callback)
```

**파라미터**

- `url` `String`
- `option` `Object` ClientRequestOption
- `callback` `(response) => {}` ClientResponse를 받는 콜백 함수.

**반환값**

- `Object`

| 속성           | 타입       | 설명        |
|:-------------------|:-----------|:-------------------|
| status             | Number     | HTTP 상태 코드   |
| statusText         | String     | HTTP 상태 메시지|
| url                | String     | 요청 URL        |
| error              | String     | 오류 메시지      |

**사용 예제**

```js
const http = require("@jsh/http");

const client = new http.Client()
client.do(
    "http://127.0.0.1:29876/hello",
    { method:"GET" }, 
    (rsp)=>{
        println("url:", rsp.url);
        println("error:", rsp.error());
        println("status:", rsp.status);
        println("statusText:", rsp.statusText);
        println("content-type:", rsp.headers["Content-Type"]);
        println("body:", rsp.text());
    })
```

## ClientRequestOption

| 옵션              | 타입         | 기본값        | 설명         |
|:--------------------|:-------------|:---------------|:--------------------|
| method              | String       | `GET`          | GET, POST, DELETE, PUT... |
| headers             | Object       |                |                     |
| body                | String       |                | 보낼 내용     |
| unix                | String       |                | Unix 도메인 소켓 파일 경로 |

`unix` 옵션을 지정하면 HTTP 클라이언트가 주어진 Unix 도메인 소켓 파일 경로로 서버에 연결을 시도합니다.

## ClientRequest

### do()

do() 함수는 지정한 URL로 HTTP 요청을 보내고 응답을 처리하는 HTTP 클라이언트의 메서드입니다.

**문법**

```js
do(callback)
```

**파라미터**

- `callback` `(response) => {}` 콜백 함수.

**반환값**

None.

### 헤더 메서드

| 메서드 | 설명 |
|:-------|:-----|
| `setHeader(name, value)` | 요청 헤더를 설정합니다 |
| `getHeader(name)` | 요청 헤더 값을 반환합니다 |
| `hasHeader(name)` | 해당 헤더가 있는지 반환합니다 |
| `removeHeader(name)` | 요청 헤더를 제거합니다 |
| `getHeaders()` | 설정된 헤더 전체를 객체로 반환합니다 |
| `getHeaderNames()` | 설정된 헤더 이름 배열을 반환합니다 |

```js
const http = require('http');
const req = http.request('http://127.0.0.1:8080/hello');
req.setHeader('X-Test-Header', 'TestValue');
console.println(req.hasHeader('X-Test-Header'));
console.println(req.getHeader('X-Test-Header'));
req.end();
```

### write()

요청 본문 청크를 기록합니다. `chunk`는 `string`, `Uint8Array`를 지원하며 성공 시 `true`, 실패 시 `false`를 반환합니다.

**문법**

```js
write(chunk[, encoding][, callback])
```

### end()

요청을 종료하고 전송합니다. `callback`을 전달하면 응답 객체를 인자로 받습니다.

**문법**

```js
end([data[, encoding]][, callback])
```

### destroy()

요청 객체를 파기하고 필요 시 error 이벤트를 발생시킵니다.

**문법**

```js
destroy([err])
```

### 이벤트

- `response` (응답 객체)
- `error` (`Error`)
- `end` ()

## ClientResponse

HTTP 응답 객체입니다. Node.js 호환 API에서는 `IncomingMessage`라고도 부릅니다.

**속성**

| 속성           | 타입       | 설명        |
|:-------------------|:-----------|:-------------------|
| status             | Number     | 상태 코드. 예: 200, 404 |
| statusCode         | Number     | 상태 코드 (Node 호환 이름) |
| statusText         | String     | 예: 200 OK        |
| statusMessage      | String     | 상태 메시지 (Node 호환 이름) |
| ok                 | Boolean    | 상태 코드가 2xx이면 `true` |
| headers            | Object     | 응답 헤더   |
| rawHeaders         | Array      | 정규화하지 않은 원본 헤더 |
| httpVersion        | String     | HTTP 버전   |
| complete           | Boolean    | 본문 수신 완료 여부 |
| method             | String     | 요청 메서드     |
| url                | String     | 요청 URL        |
| error              | String     | 오류 메시지      |
| raw                | Object     | 내부 Go 응답 객체 |

### text()

응답 본문 전체를 하나의 문자열로 반환합니다. 기본 인코딩은 `utf-8`입니다.

### json()

응답 본문을 파싱해 JSON 객체로 반환합니다. 파싱에 실패하면 예외가 발생할 수 있습니다.

### csv()

응답 본문을 파싱해 문자열 배열의 배열로 반환하며, 각 내부 배열이 CSV 데이터의 한 행을 나타냅니다.

### readBody()

응답 본문을 문자열로 읽습니다. 기본 인코딩은 `utf-8`입니다.

**문법**

```js
readBody([encoding])
```

### readBodyBuffer()

응답 본문을 바이너리 버퍼로 읽습니다.

### setTimeout(), close()

`setTimeout(msecs[, callback])`으로 응답 대기 시간을 설정합니다. 응답 본문은 일반적인 처리 흐름에서 자동으로 닫히며, 필요하면 `close()`를 명시적으로 호출할 수 있습니다.

```js
const http = require('http');
http.get('http://127.0.0.1:8080/hello', (res) => {
  console.println(res.ok, res.statusCode);
  console.println(res.text());
});
```

## Server

HTTP 서버입니다.

**사용 예제**

```js
const http = require("@jsh/http")
const svr = new http.Server({
    network:'tcp',
    address:'127.0.0.1:8080',
})
svr.get("/hello/:name", (ctx) => {
    let name = ctx.param("name");
    let hello = ctx.query("greeting");
    hello = hello == "" ?  "hello" : hello;
    ctx.JSON(http.status.OK, {
        greeting: hello,
        name:  name,
    })
})
svr.static("/html", "/html")
svr.serve();
```

**생성**

| 생성자             | 설명                          |
|:------------------------|:-------------------------------------|
| new Server(options)      | HTTP 서버를 생성합니다          |

**옵션**

| 옵션       | 타입      | 기본값    | 설명         |
|:-------------|:----------|:-----------|:--------------------|
| network      | String    | `tcp`      | `tcp`, `unix`       |
| address      | String    |            | `host:port`, `/path/to/file` |

- TCP/IP: `{network:"tcp", address:"192.168.0.100:8080"}`
- Unix 도메인 소켓: `{network:"unix", address:"/tmp/http.sock"}`

### all()

all() 함수는 GET, POST, PUT, DELETE 등 모든 HTTP 메서드를 처리하는 라우트를 추가하는 HTTP 서버의 메서드입니다. 여러 요청 유형에 대해 하나의 핸들러를 정의할 수 있습니다.

주요 특징:

1. 모든 메서드 처리: 특정 라우트에 대해 모든 HTTP 메서드를 처리합니다.
2. 사용자 정의 요청 처리: 요청별 세부 정보를 담은 context 파라미터로 들어오는 요청을 처리하는 콜백 함수를 제공합니다.

**문법**

```js
all(request_path, handler)
```

**파라미터**

- `request_path` `String` 매칭할 URL 경로.
- `handler` `(context) => {}` 들어오는 요청을 처리하는 콜백 함수이며, context 파라미터가 요청 헤더·파라미터·본문 등의 정보를 제공합니다.

**반환값**

None.

**사용 예제**

```js
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.all("/api/resource", (ctx) => {
    ctx.JSON(http.status.OK, { message: "Handled all methods" });
});
svr.serve();
```

### get()

get() 함수는 HTTP GET 요청을 처리하는 라우트를 추가하는 HTTP 서버의 메서드입니다. 특정 URL 경로로 들어오는 GET 요청을 처리할 핸들러를 정의할 수 있습니다.

**문법**

```js
get(request_path, handler)
```

**파라미터**

- `request_path` `String` 매칭할 URL 경로.
- `handler` `(context) => {}` 들어오는 요청을 처리하는 콜백 함수이며, context 파라미터가 요청 헤더·파라미터·본문 등의 정보를 제공합니다.

**반환값**

None.

**사용 예제**

```js
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.get("/hello/:name", (ctx) => {
    const name = ctx.param("name");
    ctx.JSON(http.status.OK, { message: `Hello, ${name}!` });
});
svr.serve();
```

### post()

post() 함수는 HTTP POST 요청을 처리하는 라우트를 추가하는 HTTP 서버의 메서드입니다. 특정 URL 경로로 들어오는 POST 요청을 처리할 핸들러를 정의할 수 있습니다.

**문법**

```js
post(request_path, handler)
```

**파라미터**

- `request_path` `String`  매칭할 URL 경로.
- `handler` `(context) => {}` 들어오는 요청을 처리하는 콜백 함수이며, context 파라미터가 요청별 세부 정보를 제공합니다.

**반환값**

None.

**사용 예제**

```js
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.post("/submit", (ctx) => {
    const data = ctx.body; // Access the request body
    ctx.JSON(http.status.Created, { message: "Data received", data: data });
});
svr.serve();
```

### put()

PUT 메서드를 처리하는 라우트를 추가합니다.

**문법**

```js
put(request_path, handler)
```

**파라미터**

- `request_path` `String`
- `handler` `(context) => {}` 들어오는 요청을 처리하는 콜백 함수이며, context 파라미터가 요청별 세부 정보를 제공합니다.

**반환값**

None.

### delete()

DELETE 메서드를 처리하는 라우트를 추가합니다.

**문법**

```js
delete(request_path, handler)
```

**파라미터**

- `request_path` `String`
- `handler` `(context) => {}` 들어오는 요청을 처리하는 콜백 함수이며, context 파라미터가 요청별 세부 정보를 제공합니다.

**반환값**

None.

### static()

static() 함수는 지정한 정적 디렉터리의 파일을 제공하는 라우트를 정의하는 HTTP 서버의 메서드입니다. HTML, CSS, JavaScript, 이미지 등 정적 자산을 HTTP 요청에 응답해 제공할 때 유용합니다.

주요 특징:

1. 정적 파일 제공: 주어진 경로와 일치하는 요청에 대해 지정한 디렉터리의 파일을 제공합니다.
2. 효율적인 리소스 전달: 웹 애플리케이션에서 정적 자산을 전달하기에 적합합니다.

**문법**

```js
static(request_path, dir_path)
```

**파라미터**

- `request_path` `String` 매칭할 URL 경로.
- `dir_path` `String` 제공할 정적 파일이 들어 있는 디렉터리 경로.

**반환값**

None.

**사용 예제**

```js
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.static("/public", "/path/to/static/files");
svr.serve();
```

### staticFile()

staticFile() 함수는 주어진 요청 경로에 대해 특정 정적 파일을 제공하는 라우트를 정의하는 HTTP 서버의 메서드입니다. 단일 HTML 페이지, 이미지, 설정 파일 같은 개별 파일을 제공할 때 유용합니다.

주요 특징:

- 단일 파일 제공: 지정한 요청 경로에 대해 특정 파일을 제공합니다.
- 효율적인 리소스 전달: 개별 정적 리소스를 전달하기에 적합합니다.

**문법**

```js
staticFile(request_path, file_path)
```

**파라미터**

- `request_path` `String` 매칭할 URL 경로.
- `file_path` `String` 제공할 정적 파일의 경로.

**반환값**

None.

**사용 예제**

```js
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.staticFile("/favicon.ico", "/path/to/favicon.ico");
svr.serve();
```

### loadHTMLGlob()

**문법**

```js
loadHTMLGlob(pattern)
```

**파라미터**

- `pattern` `String` 파일 경로 glob 패턴.

**반환값**

None.

**사용 예제**

```js
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.loadHTMLGlob("/templates/*.html")
svr.get("/docs/hello.html", ctx => {
    ctx.HTML(http.status.OK, "hello.html", {str:"Hello World", num: 123, bool: true})
})
svr.serve();
```

### ws() (since v8.5.2)

`ws()` 메서드는 HTTP 서버에 WebSocket 엔드포인트를 붙입니다. WebSocket 처리를 HTTP 서버에 직접 통합하고 싶을 때 `ws` 모듈의 `WebSocketServer` 대신 사용할 수 있습니다.

**문법**

```js
ws(path, options)
```

**파라미터**

- `path` `String` WebSocket 연결을 받을 URL 경로.
- `options` `Object`:
  - `verifyClient` `({origin, req}) => Boolean` 핸드셰이크 수락 여부를 동기적으로 결정합니다. 거부하려면 `false`를 반환하세요.
  - `handleProtocols` `(protocols, req) => String|false` 요청된 하위 프로토콜 중 하나를 선택합니다.

**사용 예제**

```js
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.ws('/ws', {
    verifyClient: ({ req }) => req.query('token') === 'secret',
    handleProtocols: (protocols) => {
        if (protocols.indexOf('my-protocol') >= 0) return 'my-protocol';
        return false;
    },
});
svr.serve();
```

> **참고:** `verifyClient()`와 `handleProtocols()`는 동기 함수입니다. Promise나 await 방식은 지원하지 않습니다. WebSocket 서버의 전체 기능은 `ws` 모듈 문서를 참고하세요.

### serve()

serve() 함수는 서버를 시작하고 stop() 함수가 호출될 때까지 제어 흐름을 막는 HTTP 서버의 메서드입니다.
지정한 네트워크와 주소에서 들어오는 요청을 수신하기 시작합니다.

**문법**

```js
serve()
serve(callback)
```

**파라미터**

- `callback` `(result)=>{}` 네트워크 유형과 주소 등의 정보를 담은 ServerResult 객체를 받는 선택적 콜백 함수.

**반환값**

None.

**사용 예제**

```js
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.serve((result) => {
    console.log(`Server is listening on ${result.network}://${result.message}`);
});
```

### close()

서버를 멈추고 종료합니다.

**문법**

```js
close()
```

**파라미터**

None.

**반환값**

None.

## ServerResult

**속성**

| 속성           | 타입       | 설명           |
|:-------------------|:-----------|:----------------------|
| network            | String     | 예: `tcp`            |
| message            | String     | 예: `127.0.0.1:8080` |

## ServerContext

**속성**

| 속성           | 타입       | 설명           |
|:-------------------|:-----------|:----------------------|
| request            | Object     | ServerRequest |

### abort()

**문법**

```js
abort()
```

**파라미터**

None.

**반환값**

None.

### redirect()

**문법**

```js
redirect(statusCode, url)
```

**파라미터**

- `statusCode` `Number` HTTP 상태 코드. 예: `302`, `http.status.Found`
- `url` `String` 리다이렉트할 주소.

**반환값**

None.

### setHeader()

**문법**

```js
setHeader(name, value)
```

**파라미터**

- `name` `String`
- `value` `String`

**반환값**

None.

### param()

**문법**

```js
param(name)
```

**파라미터**

- `name` `String`

**반환값**

- `String`

### query()

**문법**

```js
query(name)
```

**파라미터**

- `name` `String`

**반환값**

- `String`

### TEXT()

**문법**

```js
TEXT(statusCode, content)
```

**파라미터**

None.

**반환값**

None.

**사용 예제**

```js
svr.get("/formats/text", ctx => {
    ctx.TEXT(http.status.OK, "Hello World");
})

// Content-Type: "text/plain; charset=utf-8"
//
// Hello World
```

```js
svr.get("/formats/text", ctx => {
    name = "PI";
    pi = 3.1415;
    ctx.TEXT(http.status.OK, "Hello %s, %3.2f", name, pi);
})

// Content-Type: "text/plain; charset=utf-8"
//
// Hello PI, 3.14
```

### JSON()

**문법**

```js
JSON(statusCode, content)
```

**파라미터**

None.

**반환값**

None.

**사용 예제**

```js
svr.get("/formats/json", ctx => {
    obj = {str:"Hello World", num: 123, bool: true};
    ctx.JSON(http.status.OK, obj);
})

// Content-Type: application/json; charset=utf-8
//
// {"bool":true,"num":123,"str":"Hello World"}
```

```js
svr.get("/formats/json-indent", ctx => {
    obj = {str:"Hello World", num: 123, bool: true};
    ctx.JSON(http.status.OK, obj, {indent: true})
})

// Content-Type: application/json; charset=utf-8
//
// {
//     "bool": true,
//     "num": 123,
//     "str": "Hello World"
// }
```

### YAML()

**문법**

```js
YAML(statusCode, content)
```

**파라미터**

None.

**반환값**

None.

**사용 예제**

```js
svr.get("/formats/yaml", ctx => {
    ctx.YAML(http.status.OK, {str:"Hello World", num: 123, bool: true})
})

// Content-Type: application/yaml; charset=utf-8
//
// bool: true
// num: 123
// str: Hello World
```

### TOML

**문법**

```js
TOML(statusCode, content)
```

**파라미터**

None.

**반환값**

None.

**사용 예제**

```js
svr.get("/formats/toml", ctx => {
    ctx.TOML(http.status.OK, {str:"Hello World", num: 123, bool: true})
})

// Content-Type: application/toml; charset=utf-8
//
// bool = true
// num = 123
// str = 'Hello World'
```

### XML()

**문법**

```js
XML(statusCode, content)
```

**파라미터**

None.

**반환값**

None.

**사용 예제**

```js
svr.get("/formats/xml", ctx => {
    ctx.XML(http.status.OK, {str:"Hello World", num: 123, bool: true})
})

// Content-Type: application/xml; charset=utf-8
//
// <map><str>Hello World</str><num>123</num><bool>true</bool></map>
```

### HTML()

**문법**

```js
HTML(statusCode, template, obj)
```

**파라미터**

- `statusCode` `Number` HTTP 응답 상태 코드
- `template` `String` 템플릿 이름
- `obj` `any` 템플릿 값

**반환값**

None.

**사용 예제**

```js
svr.loadHTMLGlob("/templates/*.html")

svr.get("/hello.html", ctx => {
    obj = {str:"World", num: 123, bool: true};
    ctx.HTML(http.status.OK, "hello.html", obj);
})

// Content-Type: text/html; charset=utf-8
//
// <html>
//     <body>
//         <h1>Hello, World!</h1>
//         <p>num: 123</p>
//         <p>bool: true</p>
//     </body>
// </html>
```

- /templates/hello.html

```html
<html>
    <body>
        <h1>Hello, {{.str}}!</h1>
        <p>num: {{.num}}</p>
        <p>bool: {{.bool}}</p>
    </body>
</html>
```

## ServerRequest

**속성**

| 속성           | 타입       | 설명           |
|:-------------------|:-----------|:----------------------|
| method             | String     |                       |
| host               | String     |                       |
| path               | String     |                       |
| query              | String     |                       |
| header             | Object     |                       |
| body               | Object     |                       |
| remoteAddress      | String     |                       |

### getHeader()

**문법**

```js
getHeader(name)
```

**파라미터**

- `name` `String` head name. e.g. `Content-Type`, `Content-Length`

**반환값**

- `String` 헤더 값.

## status

HTTP 상태 코드를 정의합니다.

```js
const http = require("@jsh/http");

http.status.OK =                              200;
http.status.Created =                         201;
http.status.Accepted =                        202;
http.status.NonAuthoritativeInfo =            203;
http.status.NoContent =                       204;
http.status.ResetContent =                    205;
http.status.PartialContent =                  206;
http.status.MultipleChoices =                 300;
http.status.MovedPermanently =                301;
http.status.Found =                           302;
http.status.SeeOther =                        303;
http.status.NotModified =                     304;
http.status.UseProxy =                        305;
http.status.TemporaryRedirect =               307;
http.status.PermanentRedirect =               308;
http.status.BadRequest =                      400;
http.status.Unauthorized =                    401;
http.status.PaymentRequired =                 402;
http.status.Forbidden =                       403;
http.status.NotFound =                        404;
http.status.MethodNotAllowed =                405;
http.status.NotAcceptable =                   406;
http.status.ProxyAuthRequired =               407;
http.status.RequestTimeout =                  408;
http.status.Conflict =                        409;
http.status.Gone =                            410;
http.status.LengthRequired =                  411;
http.status.PreconditionFailed =              412;
http.status.RequestEntityTooLarge =           413;
http.status.RequestURITooLong =               414;
http.status.UnsupportedMediaType =            415;
http.status.RequestedRangeNotSatisfiable =    416;
http.status.ExpectationFailed =               417;
http.status.Teapot =                          418;
http.status.UnprocessableEntity =             422;
http.status.Locked =                          423;
http.status.FailedDependency =                424;
http.status.TooEarly =                        425;
http.status.UpgradeRequired =                 426;
http.status.PreconditionRequired =            428;
http.status.TooManyRequests =                 429;
http.status.RequestHeaderFieldsTooLarge =     431;
http.status.UnavailableForLegalReasons =      451;
http.status.InternalServerError =             500;
http.status.NotImplemented =                  501;
http.status.BadGateway =                      502;
http.status.ServiceUnavailable =              503;
http.status.GatewayTimeout =                  504;
http.status.HTTPVersionNotSupported =         505;
http.status.VariantAlsoNegotiates =           506;
http.status.InsufficientStorage =             507;
http.status.LoopDetected =                    508;
http.status.NotExtended =                     510;
http.status.NetworkAuthenticationRequired =   511;
```
