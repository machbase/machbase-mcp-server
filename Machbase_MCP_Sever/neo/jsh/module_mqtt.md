---
title: "@jsh/mqtt"
type: docs
weight: 11
---

{{< neo_since ver="8.0.52" />}}


## Client

The MQTT client.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
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
    client.disconnect({waitForEmptyQueue:true});
}
```

<h6>Creation</h6>

| Constructor             | Description                          |
|:------------------------|:----------------------------------------------|
| new Client(*options*)   | Instantiates a MQTT client object with an options |

<h6>Options</h6>

| Option                             | Type         | Default        | Description         |
|:-----------------------------------|:-------------|:---------------|:--------------------|
| serverUrls                         | String[]     |                | server addresses    |
| keepAlive                          | Number       | `10`           |                     |
| cleanStart                         | Boolean      | `true`         | clean session       |
| username                           | String       |                |                     |
| password                           | String       |                |                     |
| clientID                           | String       | random id      |                     |
| debug                              | Boolean      | `false`        |                     |
| sessionExpiryInterval              | Number       | `60`           |                     |
| connectRetryDelay                  | Number       | `10`           |                     |
| connectTimeout                     | Number       | `10`           |                     |
| packetTimeout                      | Number       | `5`            |                     |
| queue                              | String       | `memory`       |                     |

### connect()

<h6>Syntax</h6>

```js
connect(opts)
```

<h6>Parameters</h6>

- `opts` `Object`

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| timeout            | Number     | connection timeout in milliseconds |

<h6>Return value</h6>

None.

### disconnect()

<h6>Syntax</h6>

```js
disconnect(opts)
```

<h6>Parameters</h6>

- `opts` `Object`

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| waitForEmptyQueue  | Boolean    |                       |
| timeout            | Number     | disconnect wait timeout in milliseconds |

<h6>Return value</h6>

None.

### subscribe()

<h6>Syntax</h6>

```js
subscribe(opts)
```

<h6>Parameters</h6>

- `opts` `Object` *SubscriptionOption*

<h6>SubscriptionOption</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| **subscriptions**  | Object[]   | Array of *Subscription* |
| properties         | Object     | *Properties*            |

<h6>Subscription</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| **topic**          | String     |                       |
| qos                | Number     | `0`, `1`, `2`         |
| retainHandling     | Number     |                       |
| noLocal            | Boolean    |                       |
| retainAsPublished  | Boolean    |                       |

<h6>Properties</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| user               | Object     | key-value properties  |

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js
const topicName = 'sensor/temperature';
client.subscribe({subscriptions:[{topic:topicName, qos:0}]});
```

### unsubscribe()

<h6>Syntax</h6>

```js
unsubscribe(opts)
```

<h6>Parameters</h6>

- `opts` `Object` *UnsubscribeOption*

<h6>UnsubscribeOption</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| **topics**         | String[]   | Array of topics to unsubscribe |
| properties         | Object     | *Properties*          |

<h6>Properties</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| user               | Object     | user key-value properties |

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js
const topicName = 'sensor/temperature';
client.unsubscribe({topics:[topicName]});
```

### publish()

<h6>Syntax</h6>

```js
publish(opts, payload)
```

<h6>Parameters</h6>

- `opts` `Object` *PublishOptions*
- `payload` `String` or `Number`

<h6>PublishOptions</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| **topic**          | String     |                       |
| qos                | Number     | `0`, `1`, `2`         |
| packetID           | String     |                       |
| retain             | Boolean    |                       |
| properties         | Object     |                       |


<h6>Return value</h6>

- `Object`

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| reasonCode         | Number     |                       |
| properties         | Object     |                       |

<h6>Usage example</h6>

```js
let r = client.publish('sensor/temperature', 'Hello World', 1)
console.log(r.reasonCode)
```

### onMessage callback

Callback function that receives a message.

<h6>Syntax</h6>

```js
function (msg) { }
```

- `msg` `Object` Message

<h6>Message</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| packetID           | Number     |                       |
| topic              | String     |                       |
| qos                | Number     | 0, 1, 2               |
| retain             | Boolean    |                       |
| payload            | Object     | Payload               |
| properties         | Object     | Properties            |

<h6>Payload</h6>

- `msg.payload.bytes()`
- `msg.payload.string()`

<h6>Properties</h6>

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| correlationData    | byte[]     |                       |
| contentType        | String     |                       |
| responseTopic      | String     |                       |
| payloadFormat      | Number     | or undefined          |
| messageExpiry      | Number     | or undefined          |
| subscriptionIdentifier | Number | or undefined          |
| topicAlias         | Number     | or undefined          |
| user               | Object     | user properties       |

### onConnect callback

On connect callback.

<h6>Syntax</h6>

```js
function (ack) { }
```

<h6>Parameters</h6>

- `ack` `Object`

| Property           | Type       | Description           |
|:-------------------|:-----------|:----------------------|
| sessionPresent     | Boolean    |                       |
| reasonCode         | Number     |                       |
| properties         | Object     | Properties            |

<h6>Properties</h6>

| Property              | Type       | Description           |
|:----------------------|:-----------|:----------------------|
| reasonString          | String     |                       |
| reasonInfo            | String     |                       |
| assignedClientID      | String     |                       |
| authMethod            | String     |                       |
| serverKeepAlive       | Number     | or undefined          |
| sessionExpiryInterval | Number     | or undefined          |
| user                  | Object     |                       |

<h6>Return value</h6>

None.

### onConnectError callback

On connect error callback.

<h6>Syntax</h6>

```js
function (err) { }
```

<h6>Parameters</h6>

- `error` `String`

<h6>Return value</h6>

None.

### onDisconnect callback

On disconnect callback

<h6>Syntax</h6>

```js
function (disconn) { }
```

<h6>Parameters</h6>

- `disconn` `Object`

<h6>Return value</h6>

None.

### onClientError callback

On client error callback

<h6>Syntax</h6>

```js
function (err) { }
```

<h6>Parameters</h6>

- `err` `String`

<h6>Return value</h6>

None.
