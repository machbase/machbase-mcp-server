---
title: "@jsh/opcua"
type: docs
weight: 100
---

{{< neo_since ver="8.0.52" />}}

## Client

The OPCUA client.

**Usage example**

```js {linenos=table,linenostart=1}
opcua = require("@jsh/opcua");
nodes = [
    "ns=1;s=NoPermVariable",
    "ns=1;s=ReadWriteVariable",
    "ns=1;s=ReadOnlyVariable",
    "ns=1;s=NoAccessVariable",
];

try {
    client = new opcua.Client({ endpoint: "opc.tcp://localhost:4840" });
    vs = client.read({
        nodes: nodes,
        timestampsToReturn: opcua.TimestampsToReturn.Both
    });
    vs.forEach((v, idx) => {
        console.log(nodes[idx], v.status, v.statusCode, v.value, v.type);
    })
} catch (e) {
    console.log("Error:", e.message);
} finally {
    if (client !== undefined) client.close();
}
```

<h6>Creation</h6>

| Constructor             | Description                          |
|:------------------------|:----------------------------------------------|
| new Client(*options*)   | Instantiates a opcua client object with an options |

<h6>Options</h6>

| Option              | Type         | Default        | Description         |
|:--------------------|:-------------|:---------------|:--------------------|
| endpoint            | String       | `""`           | server address      |
| readRetryInterval   | Number       | `100`          | read retry interval in ms. |
| messageSecurityMode |              | |  [MessageSecurityMode](#messagesecuritymode) |

### close()

Disconnect.

<h6>Syntax</h6>

```js
close()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

None.

### read()

<h6>Syntax</h6>

```js
read(read_request)
```

<h6>Parameters</h6>

`read_request` `Object` [ReadRequest](#readrequest)

<h6>Return value</h6>

`Object[]` Array of [ReadResult](#readresult)

```js
vs = client.read({
    nodes: [ "ns=1;s=ro_bool", "ns=1;s=rw_int32"],
    timestampsToReturn:ua.TimestampsToReturn.Both
});
vs.forEach((v, idx) => {
    console.log(nodes[idx], v.status, v.statusCode, v.value, v.type);
})
```

### write()

<h6>Syntax</h6>

```js
write(...write_request)
```

<h6>Parameters</h6>

`write_request` `Object` Variable length of [WriteRequest](#writerequest)

<h6>Return value</h6>

`Object` [WriteResult](#writeresult)

```js
rsp = client.write(
    {node: "ns=1;s=rw_bool", value: false},
    {node: "ns=1;s=rw_int32", value: 1234}
)
console.log("results:", rsp.results);
```

## ReadRequest

| Option              | Type         | Default        | Description         |
|:--------------------|:-------------|:---------------|:--------------------|
| nodes               | String[]     |                | array of node IDs   |
| maxAge              | Number       | `100`          | read retry interval in ms. |
| timestampsToReturn  |              |  | [TimestampToReturn](#timestamptoreturn)     |

## ReadResult

<h6>Properties</h6>

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| status             | Number     |                    |
| statusText         | String     |                    |
| statusCode         | String     |                    |
| value              | any        |                    |
| sourceTimestamp    | Number     | Unix epoch (milliseconds) |
| sourceTimestamp    | Number     | Unix epoch (milliseconds) |


## WriteRequest

<h6>Properties</h6>

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| node               | String     | node ID            |
| value              | any        | value to write     |

## WriteResult

<h6>Properties</h6>

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| results            | Number[]   | array of status codes     |
| timestamp          | Number     | Unix epoch (milliseconds) |
| stringTables       | String[]   | array of strings   |

## MessageSecurityMode

- `MessageSecurityMode.None`
- `MessageSecurityMode.Sign`
- `MessageSecurityMode.SignAndEncrypt`

## TimestampToReturn

- `TimestampToReturn.Source`
- `TimestampToReturn.Server`
- `TimestampToReturn.Both`
- `TimestampToReturn.Neither`
