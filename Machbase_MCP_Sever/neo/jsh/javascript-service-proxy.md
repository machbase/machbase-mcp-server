# Machbase Neo JavaScript Service Proxy

The Service Proxy feature (since v8.5.2) enables JSH services to expose internal HTTP servers through machbase-neo without publishing separate ports.

Requests to the public route are reverse-proxied to the registered target.

## Public Route Format

```
/web/services/<service_name>/<prefix>/*
```

Example: `/web/services/github.com/acme/chart/api/series`

## Registration

### service.proxy.register()

Registers a proxy endpoint.

```js
service.proxy.register({
    name: 'my-service',
    prefix: '/api',
    target: 'http://127.0.0.1:9090',
    stripPrefix: true,
    healthPath: '/health'
});
```

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `name` | String | Service identifier (package name recommended) |
| `prefix` | String | URL prefix for routing |
| `target` | String | Internal server URL |
| `stripPrefix` | Boolean | Whether to strip the prefix before forwarding |
| `healthPath` | String | Optional health check path |

### Target Restrictions

Allowed targets:
- `http://127.0.0.1:<port>`
- `http://localhost:<port>`
- Loopback IP addresses
- `unix://<absolute_socket_path>`

External hosts and `https://` targets are not allowed by default to prevent the proxy from becoming an open relay.

### service.proxy.unregister()

Removes proxy endpoints. Omitting prefix removes all endpoints for the service.

### proxy.list()

Lists all registered proxy endpoints.

### proxy.get(name)

Gets proxy registration details for a specific service.

## CLI Management

```sh
servicectl proxy list
servicectl proxy get <name>
```

## Behavior notes

- Registrations are runtime state and require re-registration after restarts.
- No separate namespace restrictions exist; first registration owns the name/prefix pair.
- Single services can register multiple proxy endpoints simultaneously.
- Package names are recommended as service identifiers to prevent conflicts.
