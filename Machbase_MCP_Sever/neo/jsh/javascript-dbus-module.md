# Machbase Neo JavaScript dbus Module

The `dbus` module provides Linux-only D-Bus APIs for JSH applications, supporting method calls, property access, introspection, signal subscription, and name-owner watching.

```js
const dbus = require("dbus");
const conn = new dbus.Connection({ busType: dbus.BusType.Session });
```

> **Note**: D-Bus functionality is Linux-only. Creating a connection fails if the runtime OS is not Linux.

## BusType

- `dbus.BusType.Session`
- `dbus.BusType.System`

## Connection

D-Bus connection object for interacting with services.

### new dbus.Connection(options)

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `busType` | String | `dbus.BusType.Session` | D-Bus bus type |

Throws for an invalid `busType` or on non-Linux platforms.

### close()

Closes the D-Bus connection. Idempotent and safe to call multiple times.

### object(destination, path)

Creates an `ObjectProxy` bound to the given destination/path.

- `destination` `String` — service name (e.g. `org.freedesktop.DBus`).
- `path` `String` — object path (e.g. `/org/freedesktop/DBus`).

### call(request)

Calls a D-Bus method. `request` is a `CallRequest`. Returns a `CallResult`. Throws for missing fields or invalid object paths.

### getProperty(request) / setProperty(request)

Reads / writes a D-Bus property. `getProperty` takes a `PropertyRequest` and returns a `PropertyResult`; `setProperty` takes a `SetPropertyRequest`.

### introspect(request)

Gets introspection metadata for an object. `request` is an `IntrospectRequest`; returns an `IntrospectionNode`.

### subscribeSignal(request) / unsubscribeSignal(request)

Subscribes / unsubscribes to D-Bus signals matching the criteria in a `SignalWatchRequest`. Returns the `Connection` for chaining. `subscribeSignal` throws if all match-criteria fields are empty; `unsubscribeSignal` throws when no matching subscription exists.

### watchName(name) / unwatchName(name)

Starts / stops watching owner changes for a bus name (`name` is a D-Bus well-known name). Returns the `Connection` for chaining. `unwatchName` throws `"name watch not found"` when no active watch exists.

### getNameOwner(name)

Gets the current owner for a bus name. Returns a `NameOwnerResult`. Returns `hasOwner: false` when the name has no owner; it does not throw.

## Events

`Connection` extends `EventEmitter`.

### "signal"

Emitted on every subscribed D-Bus signal.

```js
conn.on("signal", (sig) => {
    console.println(sig.interface, sig.member, sig.body);
});
```

### "name-owner-changed"

Emitted when a watched name changes owner.

```js
conn.on("name-owner-changed", (evt) => {
    console.println(evt.name, evt.oldOwner, evt.newOwner);
});
```

## ObjectProxy

Created via `conn.object(destination, path)`.

- `call(method, ...args)` — calls a method on the object. Returns the same shape as `CallResult`.
- `getProperty(name, interfaceName)` / `get(name, interfaceName)` — returns a `PropertyResult` (full) or the property value only (`get`).
- `setProperty(name, value, interfaceName)` / `set(name, value, interfaceName)` — writes a property.
- `introspect()` — returns an `IntrospectionNode`.
- `subscribeSignal(member, interfaceName)` / `unsubscribeSignal(member, interfaceName)` — convenience wrappers that pass destination/path automatically.

## Request / Response Structures

### CallRequest

| Property | Type | Description |
|----------|------|-------------|
| `destination` | String | Service name |
| `path` | String | Object path |
| `method` | String | Fully qualified method name (`Interface.Method`) |
| `args` | any[] | Method arguments |
| `flags` | Number | D-Bus call flags |

#### Argument Type Hints

JavaScript numbers are ambiguous for strict integer D-Bus types (`uint16`, `int32`, and so on). When an exact D-Bus type is required, pass the argument as a `"type:value"` string.

```js
"uint16:123"
"int32:-7"
"bool:true"
"objectpath:/org/freedesktop/DBus"
```

Supported types:

- Integers: `byte`, `uint8`, `uint16`, `uint32`, `uint64`, `int16`, `int32`, `int64`
- Floats: `float32`, `float64`, `double`
- Other: `bool`, `string`, `objectpath`, `path`, `signature`

Behavior notes:

- Strings without a type prefix are passed as plain strings.
- Unknown type prefixes (for example, `"custom:123"`) are not converted and are passed as-is.
- If parsing fails for a recognized type, the call throws an error.

### CallResult

| Property | Type | Description |
|----------|------|-------------|
| `destination` | String | Service name |
| `path` | String | Object path |
| `method` | String | Method name used for the call |
| `body` | any[] | Returned values |

### PropertyRequest / SetPropertyRequest

| Property | Type | Description |
|----------|------|-------------|
| `destination` | String | Service name |
| `path` | String | Object path |
| `interface` | String | Interface name |
| `name` | String | Property name |
| `value` | any | Property value to write (`SetPropertyRequest` only) |

### PropertyResult

| Property | Type | Description |
|----------|------|-------------|
| `signature` | String | D-Bus signature |
| `value` | any | Property value |

### IntrospectRequest / IntrospectionNode

`IntrospectRequest` has `destination` and `path`. `IntrospectionNode` has `name` (String), `interfaces` (object[]), and `children` (object[]). Each interface includes methods, signals, properties, and annotations.

### SignalWatchRequest

| Property | Type | Description |
|----------|------|-------------|
| `destination` | String | Optional; kept for symmetry |
| `sender` | String | Signal sender filter |
| `path` | String | Object path filter |
| `interface` | String | Interface filter |
| `member` | String | Member filter |

At least one of `sender`, `path`, `interface`, `member` must be provided.

### NameOwnerResult

| Property | Type | Description |
|----------|------|-------------|
| `name` | String | Requested bus name |
| `owner` | String | Unique name (`:1.xx`) or empty string |
| `hasOwner` | Boolean | Whether an owner exists |

## Examples

### Basic method call

```js
const dbus = require("dbus");

const conn = new dbus.Connection();
const obj = conn.object("com.plc.manufacture.Service", "/com/plc/device0");

const temp = obj.call("com.plc.manufacture.Interval.GetTemperature");
console.println("temperature:", temp.body[0]);

conn.close();
```

### Property operations

```js
const dbus = require("dbus");

const conn = new dbus.Connection();
const dev = conn.object("com.plc.manufacture.Service", "/com/plc/device0");

console.println("mode:", dev.get("Mode", "com.plc.manufacture.Status"));
dev.set("Mode", "MANUAL", "com.plc.manufacture.Status");
console.println("mode:", dev.get("Mode", "com.plc.manufacture.Status"));

conn.close();
```

### Introspection

```js
const dbus = require("dbus");

const conn = new dbus.Connection();
const obj = conn.object("com.plc.manufacture.Service", "/com/plc/device0");
const node = obj.introspect();

for (const iface of node.interfaces) {
    console.println("iface:", iface.name);
}

conn.close();
```

### Signal subscription

```js
const dbus = require("dbus");

const conn = new dbus.Connection();
const obj = conn.object("com.plc.manufacture.Service", "/com/plc/device0");

obj.subscribeSignal("TemperatureChanged", "com.plc.manufacture.Interval");
conn.on("signal", (sig) => {
    if (sig.member !== "TemperatureChanged") {
        return;
    }
    console.println("temperature changed:", sig.body[0]);
});
```

### Name watching

```js
const dbus = require("dbus");

const conn = new dbus.Connection();
const name = "com.example.Worker";

const owner = conn.getNameOwner(name);
console.println("has owner:", owner.hasOwner);

conn.watchName(name);
conn.on("name-owner-changed", (evt) => {
    if (evt.name === name) {
        console.println("owner changed:", evt.oldOwner, "->", evt.newOwner);
    }
});
```

## Error Behavior

- Calling methods after `conn.close()` throws `"connection not initialized"`.
- Missing required request fields throw errors.
- Invalid object paths throw errors.
- `getNameOwner()` returns `{ hasOwner: false }` for names without owners.
- D-Bus functionality is Linux-only.
