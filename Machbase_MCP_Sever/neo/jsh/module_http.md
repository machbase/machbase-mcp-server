---
title: "@jsh/http"
type: docs
weight: 12
---

{{< neo_since ver="8.0.52" />}}

## request()

Convenient function for making HTTP client requests.

<h6>Syntax</h6>

```js
request(url, option)
```

<h6>Parameters</h6>

- `url` `String` destination address. e.g. `http://192.168.0.120/api/members`
- `option` `Object` optional [ClientRequestOption](#clientrequestoption).

<h6>Return value</h6>

- `Object` [ClientRequest](#clientrequest)

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
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

The HTTP client.

<h6>Creation</h6>

| Constructor             | Description                          |
|:------------------------|:-------------------------------------|
| new Client()            | Instantiates a HTTP client           |


### do()

The do() function is a method of the HTTP client that sends an HTTP request to a specified URL and processes the response.
It supports optional request options (e.g., method, headers, body) and a callback function to handle the response.

<h6>Syntax</h6>

```js
client.do(url)
client.do(url, option)
client.do(url, option, callback)
```

<h6>Parameters</h6>

- `url` `String`
- `option` `Object` [ClientRequestOption](#clientrequestoption)
- `callback` `(response) => {}` callback function with [ClientResponse](#clientresponse).

<h6>Return value</h6>

- `Object`

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| status             | Number     | http status code   |
| statusText         | String     | http status message|
| url                | String     | request url        |
| error              | String     | error message      |

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
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

| Option              | Type         | Default        | Description         |
|:--------------------|:-------------|:---------------|:--------------------|
| method              | String       | `GET`          | GET, POST, DELETE, PUT... |
| headers             | Object       |                |                     |
| body                | String       |                | Content to send     |
| unix                | String       |                | Unix Domain Socket file path |

If the `unix` option is specified, the HTTP client will attempt to connect to the server using the provided Unix domain socket file path.

## ClientRequest

### do()

The do() function is a method of the HTTP client that sends an HTTP request to a specified URL and processes the response.

<h6>Syntax</h6>

```js
do(callback)
```

<h6>Parameters</h6>

- `callback` `(response) => {}` callback function.

<h6>Return value</h6>

None.

## ClientResponse

<h4>Properties</h4>

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| status             | Number     | status code. e.g. 200, 404 |
| statusText         | String     | e.g. 200 OK        |
| headers            | Object     | response headers   |
| method             | String     | request method     |
| url                | String     | request url        |
| error              | String     | error message      |

### text()

Returns the entire response body as a single string.

### json()

Parses the response body and returns it as a JSON object.

### csv()

Parses the response body and returns it as an array of string arrays, where each inner array represents a row of CSV data.

<!-- ### blob() 
    todo implement bytes stream first.
-->

## Server

The HTTP server.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
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

<h6>Creation</h6>

| Constructor             | Description                          |
|:------------------------|:-------------------------------------|
| new Server(options)      | Instantiates a HTTP server          |

<h6>Options</h6>

| Option       | Type      | Default    | Description         |
|:-------------|:----------|:-----------|:--------------------|
| network      | String    | `tcp`      | `tcp`, `unix`       |
| address      | String    |            | `host:port`, `/path/to/file` |

- TCP/IP: `{network:"tcp", address:"192.168.0.100:8080"}`
- Unix Domain Socket: `{network:"unix", address:"/tmp/http.sock"}`

### all()

The all() function is a method of the HTTP server that adds a route to handle all HTTP methods, including GET, POST, PUT, DELETE, and others. It allows you to define a single handler for multiple request types.

Key Features:

1. Universal Method Handling: Handles all HTTP methods for a specific route.
2. Custom Request Processing: Provides a callback function to process incoming requests using the context parameter, which contains request-specific details.

<h6>Syntax</h6>

```js
all(request_path, handler)
```

<h6>Parameters</h6>

- `request_path` `String` The URL path to match.
- `handler` `(context) => {}` A callback function that processes incoming requests, with the [context](#servercontext) parameter providing details like request headers, parameters, and body.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.all("/api/resource", (ctx) => {
    ctx.JSON(http.status.OK, { message: "Handled all methods" });
});
svr.serve();
```

### get()

The get() function is a method of the HTTP server that adds a route to handle HTTP GET requests. It allows you to define a handler for processing incoming GET requests to a specific URL path.

<h6>Syntax</h6>

```js
get(request_path, handler)
```

<h6>Parameters</h6>

- `request_path` `String` The URL path to match.
- `handler` `(context) => {}` A callback function that processes incoming requests, with the [context](#servercontext) parameter providing details like request headers, parameters, and body.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.get("/hello/:name", (ctx) => {
    const name = ctx.param("name");
    ctx.JSON(http.status.OK, { message: `Hello, ${name}!` });
});
svr.serve();
```


### post()

The post() function is a method of the HTTP server that adds a route to handle HTTP POST requests. It allows you to define a handler for processing incoming POST requests to a specific URL path.

<h6>Syntax</h6>

```js
put(request_path, handler)
```

<h6>Parameters</h6>

- `request_path` `String`  The URL path to match.
- `handler` `(context) => {}` A callback function that processes incoming requests, with the [context](#servercontext) parameter providing request-specific details.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.post("/submit", (ctx) => {
    const data = ctx.body; // Access the request body
    ctx.JSON(http.status.Created, { message: "Data received", data: data });
});
svr.serve();
```

### put()

Add a route to handle PUT method.

<h6>Syntax</h6>

```js
put(request_path, handler)
```

<h6>Parameters</h6>

- `request_path` `String`
- `handler` `(context) => {}` A callback function that processes incoming requests, with the [context](#servercontext) parameter providing request-specific details.

<h6>Return value</h6>

None.

### delete()

Add a route to handle DELETE method.

<h6>Syntax</h6>

```js
delete(request_path, handler)
```

<h6>Parameters</h6>

- `request_path` `String`
- `handler` `(context) => {}` A callback function that processes incoming requests, with the [context](#servercontext) parameter providing request-specific details.

<h6>Return value</h6>

None.

### static()

The static() function is a method of the HTTP server that defines a route to serve files from a specified static directory. It is useful for serving static assets like HTML, CSS, JavaScript, images, or other files in response to HTTP requests.

Key Features:

1. Static File Serving: Serves files from a specified directory for requests matching a given path.
2. Efficient Resource Delivery: Ideal for delivering static assets in web applications.

<h6>Syntax</h6>

```js
static(request_path, dir_path)
```

<h6>Parameters</h6>

- `request_path` `String` The URL path to match.
- `dir_path` `String` The directory path containing the static files to serve.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.static("/public", "/path/to/static/files");
svr.serve();
```

### staticFile()

The staticFile() function is a method of the HTTP server that defines a route to serve a specific static file for a given request path. It is useful for serving individual files, such as a single HTML page, image, or configuration file, in response to HTTP requests.

Key Features:

- Single File Serving: Serves a specific file for a specified request path.
- Efficient Resource Delivery: Ideal for delivering individual static resources.


<h6>Syntax</h6>

```js
staticFile(request_path, file_path)
```

<h6>Parameters</h6>

- `request_path` `String` The URL path to match.
- `file_path` `String` The file path of the static file to serve.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.staticFile("/favicon.ico", "/path/to/favicon.ico");
svr.serve();
```

### loadHTMLGlob()


<h6>Syntax</h6>

```js
loadHTMLGlob(pattern)
```

<h6>Parameters</h6>

- `pattern` `String` The file path glob pattern.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.loadHTMLGlob("/templates/*.html")
svr.get("/docs/hello.html", ctx => {
    ctx.HTML(http.status.OK, "hello.html", {str:"Hello World", num: 123, bool: true})
})
svr.serve();
```

### serve()

The serve() function is a method of the HTTP server that starts the server and blocks the control flow until the stop() function is called.
It begins listening for incoming requests on the specified network and address.

<h6>Syntax</h6>

```js
serve()
serve(callback)
```

<h6>Parameters</h6>

- `callback` `(result)=>{}` An optional callback function that receives a [ServerResult](#ServerResult) object containing details like the network type and address.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const http = require("@jsh/http");

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
svr.serve((result) => {
    console.log(`Server is listening on ${result.network}://${result.message}`);
});
```

### close()

Stop and shutdown the server.

<h6>Syntax</h6>

```js
close()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

None.

<!-- #### router()

## Router

### Methods

#### all()

#### get()

#### post()

#### put()

#### delete()

#### static()

#### staticFile() -->

## ServerResult

<h6>Properties</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| network            | String     | e.g. `tcp`            |
| message            | String     | e.g. `127.0.0.1:8080` |

## ServerContext

<h6>Properties</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| request            | Object     | [ServerRequest](#serverrequest) |


### abort()

<h6>Syntax</h6>

```js
abort()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

None.

### redirect()

<h6>Syntax</h6>

```js
redirect(statusCode, url)
```

<h6>Parameters</h6>

- `statusCode` `Number` HTTP status code. e.g. `302`, `http.status.Found`
- `url` `String` address to redirect.

<h6>Return value</h6>

None.

### setHeader()

<h6>Syntax</h6>

```js
setHeader(name, value)
```

<h6>Parameters</h6>

- `name` `String`
- `value` `String`

<h6>Return value</h6>

None.

### param()

<h6>Syntax</h6>

```js
param(name)
```

<h6>Parameters</h6>

- `name` `String`

<h6>Return value</h6>

- `String`

### query()

<h6>Syntax</h6>

```js
query(name)
```

<h6>Parameters</h6>

- `name` `String`

<h6>Return value</h6>

- `String`

### TEXT()

<h6>Syntax</h6>

```js
TEXT(statusCode, content)
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
svr.get("/formats/text", ctx => {
    ctx.TEXT(http.status.OK, "Hello World");
})

// Content-Type: "text/plain; charset=utf-8"
//
// Hello World
```

```js {linenos=table,linenostart=1}
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

<h6>Syntax</h6>

```js
JSON(statusCode, content)
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
svr.get("/formats/json", ctx => {
    obj = {str:"Hello World", num: 123, bool: true};
    ctx.JSON(http.status.OK, obj);
})

// Content-Type: application/json; charset=utf-8
//
// {"bool":true,"num":123,"str":"Hello World"}
```

```js {linenos=table,linenostart=1}
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

<h6>Syntax</h6>

```js
YAML(statusCode, content)
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
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

<h6>Syntax</h6>

```js
TOML(statusCode, content)
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
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

<h6>Syntax</h6>

```js
XML(statusCode, content)
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
svr.get("/formats/xml", ctx => {
    ctx.XML(http.status.OK, {str:"Hello World", num: 123, bool: true})
})

// Content-Type: application/xml; charset=utf-8
//
// <map><str>Hello World</str><num>123</num><bool>true</bool></map>
```

### HTML()

<h6>Syntax</h6>

```js
HTML(statusCode, template, obj)
```

<h6>Parameters</h6>

- `statusCode` `Number` HTTP Response Status Code
- `template` `String` Template name
- `obj` `any` Template value

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
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

<h6>Properties</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| method             | String     |                       |
| host               | String     |                       |
| path               | String     |                       |
| query              | String     |                       |
| header             | Object     |                       |
| body               | Object     |                       |
| remoteAddress      | String     |                       |

### getHeader()

<h6>Syntax</h6>

```js
getHeader(name)
```

<h6>Parameters</h6>

- `name` `String` head name. e.g. `Content-Type`, `Content-Length`

<h6>Return value</h6>

- `String` header value.

## status

Defines http status codes.

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