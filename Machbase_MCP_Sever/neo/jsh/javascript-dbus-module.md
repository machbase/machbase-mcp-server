# Machbase Neo JavaScript dbus Module

`dbus` 모듈은 JSH 애플리케이션에 Linux 전용 D-Bus API를 제공하며 메서드 호출, 속성 접근, 인트로스펙션, 시그널 구독, 이름 소유자 감시를 지원합니다.

```js
const dbus = require("dbus");
const conn = new dbus.Connection({ busType: dbus.BusType.Session });
```

> **참고**: D-Bus 기능은 Linux 전용입니다. 런타임 OS가 Linux가 아니면 연결 생성에 실패합니다.

## BusType

- `dbus.BusType.Session`
- `dbus.BusType.System`

## Connection

서비스와 상호작용하기 위한 D-Bus 연결 객체입니다.

### new dbus.Connection(options)

**Options:**

| 옵션 | 타입 | 기본값 | 설명 |
|--------|------|---------|-------------|
| `busType` | String | `dbus.BusType.Session` | D-Bus 버스 타입 |

잘못된 `busType`이거나 Linux가 아닌 플랫폼에서는 예외를 던집니다.

### close()

D-Bus 연결을 닫습니다. 멱등적이며 여러 번 호출해도 안전합니다.

### object(destination, path)

주어진 destination/path에 바인딩된 `ObjectProxy`를 만듭니다.

- `destination` `String` — 서비스 이름 (예: `org.freedesktop.DBus`).
- `path` `String` — 객체 경로 (예: `/org/freedesktop/DBus`).

### call(request)

D-Bus 메서드를 호출합니다. `request`는 `CallRequest`이며 `CallResult`를 반환합니다. 필드가 없거나 객체 경로가 잘못되면 예외를 던집니다.

### getProperty(request) / setProperty(request)

D-Bus 속성을 읽거나 씁니다. `getProperty`는 `PropertyRequest`를 받아 `PropertyResult`를 반환하고, `setProperty`는 `SetPropertyRequest`를 받습니다.

### introspect(request)

객체의 인트로스펙션 메타데이터를 가져옵니다. `request`는 `IntrospectRequest`이며 `IntrospectionNode`를 반환합니다.

### subscribeSignal(request) / unsubscribeSignal(request)

`SignalWatchRequest`의 조건에 맞는 D-Bus 시그널을 구독하거나 해제합니다. 체이닝을 위해 `Connection`을 반환합니다. `subscribeSignal`은 모든 매칭 조건 필드가 비어 있으면 예외를 던지고, `unsubscribeSignal`은 일치하는 구독이 없으면 예외를 던집니다.

### watchName(name) / unwatchName(name)

버스 이름(`name`은 D-Bus well-known 이름)의 소유자 변경 감시를 시작하거나 중지합니다. 체이닝을 위해 `Connection`을 반환합니다. 활성 감시가 없으면 `unwatchName`은 `"name watch not found"` 예외를 던집니다.

### getNameOwner(name)

버스 이름의 현재 소유자를 가져옵니다. `NameOwnerResult`를 반환합니다. 소유자가 없으면 `hasOwner: false`를 반환하며 예외를 던지지 않습니다.

## Events

`Connection` extends `EventEmitter`.

### "signal"

구독한 D-Bus 시그널마다 발생합니다.

```js
conn.on("signal", (sig) => {
    console.println(sig.interface, sig.member, sig.body);
});
```

### "name-owner-changed"

감시 중인 이름의 소유자가 바뀌면 발생합니다.

```js
conn.on("name-owner-changed", (evt) => {
    console.println(evt.name, evt.oldOwner, evt.newOwner);
});
```

## ObjectProxy

Created via `conn.object(destination, path)`.

- `call(method, ...args)` — 객체의 메서드를 호출합니다. `CallResult`와 같은 형태를 반환합니다.
- `getProperty(name, interfaceName)` / `get(name, interfaceName)` — `PropertyResult` 전체 또는 속성 값만(`get`) 반환합니다.
- `setProperty(name, value, interfaceName)` / `set(name, value, interfaceName)` — 속성을 씁니다.
- `introspect()` — returns an `IntrospectionNode`.
- `subscribeSignal(member, interfaceName)` / `unsubscribeSignal(member, interfaceName)` — destination/path를 자동으로 전달하는 편의 래퍼입니다.

## 요청 / 응답 구조

### CallRequest

| 속성 | 타입 | 설명 |
|----------|------|-------------|
| `destination` | String | 서비스 이름 |
| `path` | String | 객체 경로 |
| `method` | String | 정규화된 메서드 이름 (`Interface.Method`) |
| `args` | any[] | 메서드 인자 |
| `flags` | Number | D-Bus 호출 플래그 |

#### 인자 타입 힌트

JavaScript 숫자는 `uint16`, `int32` 같은 엄격한 정수 D-Bus 타입에 대해 모호합니다. 정확한 D-Bus 타입이 필요하면 인자를 `"type:value"` 문자열로 전달하세요.

```js
"uint16:123"
"int32:-7"
"bool:true"
"objectpath:/org/freedesktop/DBus"
```

지원 타입:

- Integers: `byte`, `uint8`, `uint16`, `uint32`, `uint64`, `int16`, `int32`, `int64`
- Floats: `float32`, `float64`, `double`
- Other: `bool`, `string`, `objectpath`, `path`, `signature`

동작 참고사항:

- 타입 접두가 없는 문자열은 일반 문자열로 전달됩니다.
- 알 수 없는 타입 접두(예: `"custom:123"`)는 변환되지 않고 그대로 전달됩니다.
- 인식된 타입의 파싱이 실패하면 호출이 오류를 던집니다.

### CallResult

| 속성 | 타입 | 설명 |
|----------|------|-------------|
| `destination` | String | 서비스 이름 |
| `path` | String | 객체 경로 |
| `method` | String | 호출에 사용된 메서드 이름 |
| `body` | any[] | 반환된 값들 |

### PropertyRequest / SetPropertyRequest

| 속성 | 타입 | 설명 |
|----------|------|-------------|
| `destination` | String | 서비스 이름 |
| `path` | String | 객체 경로 |
| `interface` | String | 인터페이스 이름 |
| `name` | String | 속성 이름 |
| `value` | any | 쓸 속성 값 (`SetPropertyRequest` 전용) |

### PropertyResult

| 속성 | 타입 | 설명 |
|----------|------|-------------|
| `signature` | String | D-Bus 시그니처 |
| `value` | any | 속성 값 |

### IntrospectRequest / IntrospectionNode

`IntrospectRequest`는 `destination`과 `path`를 가집니다. `IntrospectionNode`는 `name`(String), `interfaces`(object[]), `children`(object[])을 가집니다. 각 인터페이스는 메서드, 시그널, 속성, 애너테이션을 포함합니다.

### SignalWatchRequest

| 속성 | 타입 | 설명 |
|----------|------|-------------|
| `destination` | String | 선택. 형태 일관성을 위해 유지됩니다 |
| `sender` | String | 시그널 발신자 필터 |
| `path` | String | 객체 경로 필터 |
| `interface` | String | 인터페이스 필터 |
| `member` | String | 멤버 필터 |

`sender`, `path`, `interface`, `member` 중 최소 하나는 지정해야 합니다.

### NameOwnerResult

| 속성 | 타입 | 설명 |
|----------|------|-------------|
| `name` | String | 요청한 버스 이름 |
| `owner` | String | 고유 이름(`:1.xx`) 또는 빈 문자열 |
| `hasOwner` | Boolean | 소유자 존재 여부 |

## 예제

### 기본 메서드 호출

```js
const dbus = require("dbus");

const conn = new dbus.Connection();
const obj = conn.object("com.plc.manufacture.Service", "/com/plc/device0");

const temp = obj.call("com.plc.manufacture.Interval.GetTemperature");
console.println("temperature:", temp.body[0]);

conn.close();
```

### 속성 연산

```js
const dbus = require("dbus");

const conn = new dbus.Connection();
const dev = conn.object("com.plc.manufacture.Service", "/com/plc/device0");

console.println("mode:", dev.get("Mode", "com.plc.manufacture.Status"));
dev.set("Mode", "MANUAL", "com.plc.manufacture.Status");
console.println("mode:", dev.get("Mode", "com.plc.manufacture.Status"));

conn.close();
```

### 인트로스펙션

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

### 시그널 구독

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

### 이름 감시

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

## 오류 동작

- `conn.close()` 이후 메서드를 호출하면 `"connection not initialized"` 예외가 발생합니다.
- 필수 요청 필드가 없으면 오류가 발생합니다.
- 잘못된 객체 경로는 오류를 발생시킵니다.
- 소유자가 없는 이름에 대해 `getNameOwner()`는 `{ hasOwner: false }`를 반환합니다.
- D-Bus 기능은 Linux 전용입니다.
