# Machbase Neo JavaScript Service Module

The `service` module is a client interface for calling the service controller JSON-RPC API from JSH applications.

```js
const service = require('service');
```

## Client

Creates a service client instance.

### Syntax

```js
new service.Client([options])
```

### Options

| Option | Type | Default | Description |
|:-------|:-----|:--------|:------------|
| `controller` | String | `SERVICE_CONTROLLER` env var | Controller address (host:port, tcp://, unix://) |
| `timeout` | Number | 5000 | RPC timeout in milliseconds |

## Methods

### status(callback)

Retrieves service status information.

### read(callback)

Reads the current service configuration.

### update(config, callback)

Updates the service configuration.

### reload(callback)

Reloads the service configuration.

### install(config, callback)

Installs a new service.

### uninstall(callback)

Uninstalls the service.

### start(callback)

Starts the service.

### stop(callback)

Stops the service.

### call(method[, params], callback)

Invokes an arbitrary JSON-RPC method on the controller.

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `method` | String | RPC method name |
| `params` | Object | Optional method parameters |
| `callback` | Function | Error-first callback `(err, result)` |

## Runtime

### runtime.get(callback)

Retrieves runtime information from the service controller.

## Details

The `details` sub-API manages key-value pairs associated with the service.

### details.get(name[, key], callback)

Retrieves detail values.

### details.add(name, key, value, callback)

Adds a new detail entry.

### details.update(name, key, value, callback)

Updates an existing detail entry.

### details.set(name, key, value, callback)

Sets a detail entry (creates or updates).

### details.delete(name, key, callback)

Deletes a detail entry.

## Behavior notes

- All APIs use callback-based asynchronous style with error-first callbacks.
- The module maintains internal keepalive mechanisms to prevent premature script termination during pending requests.
- The keepalive duration is tied to the configured timeout value.
- The `SERVICE_CONTROLLER` environment variable is the standard way to provide the controller address.
