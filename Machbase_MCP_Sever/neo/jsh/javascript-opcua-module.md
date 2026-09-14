# Machbase Neo JavaScript OPCUA Module

## Client

OPC UA 클라이언트입니다.

**사용 예제**

```js
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

**생성**

| 생성자             | 설명                          |
|:------------------------|:----------------------------------------------|
| new Client(*options*)   | 옵션으로 OPC UA 클라이언트 객체를 생성합니다 |

**옵션**

| 옵션              | 타입         | 기본값        | 설명         |
|:--------------------|:-------------|:---------------|:--------------------|
| endpoint            | String       | `""`           | 서버 주소      |
| readRetryInterval   | Number       | `100`          | 읽기 재시도 주기(ms). |
| messageSecurityMode |              | |  MessageSecurityMode |

### close()

Disconnect.

**문법**

```js
close()
```

**파라미터**

None.

**반환값**

None.

### read()

**문법**

```js
read(read_request)
```

**파라미터**

`read_request` `Object` ReadRequest

**반환값**

`Object[]` ReadResult 배열

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

**문법**

```js
write(...write_request)
```

**파라미터**

`write_request` `Object` 가변 길이 WriteRequest

**반환값**

`Object` WriteResult

```js
rsp = client.write(
    {node: "ns=1;s=rw_bool", value: false},
    {node: "ns=1;s=rw_int32", value: 1234}
)
console.log("results:", rsp.results);
```

### browse()

하나 이상의 노드에 대한 참조를 탐색합니다.

**문법**

```js
browse(browseRequest)
```

**파라미터**

`browseRequest` `Object` BrowseRequest

**반환값**

`Object[]` BrowseResult 배열

`nodes`가 없거나 비어 있으면 예외가 발생합니다.

```js
const ua = require("@jsh/opcua");

let client;
try {
    client = new ua.Client({ endpoint: "opc.tcp://localhost:4840" });
    const results = client.browse({
        nodes: ["ns=1;i=85"],
        nodeClassMask: ua.NodeClass.Variable,
        requestedMaxReferencesPerNode: 2,
    });

    console.println("continuationPoint:", results[0].continuationPoint);
    results[0].references.forEach((ref) => {
        console.println(ref.browseName, ref.nodeId, ref.nodeClass);
    });
} catch (e) {
    console.println("Error:", e);
} finally {
    if (client !== undefined) client.close();
}
```

### browseNext()

`browse()` 또는 `browseNext()`가 반환한 continuation point를 사용해 다음 페이지를 계속 조회합니다.

**문법**

```js
browseNext(browseNextRequest)
```

**파라미터**

`browseNextRequest` `Object` BrowseNextRequest

**반환값**

`Object[]` BrowseResult 배열

`continuationPoints`가 없거나 비어 있으면 예외가 발생합니다.

```js
const ua = require("@jsh/opcua");

let client;
try {
    client = new ua.Client({ endpoint: "opc.tcp://localhost:4840" });

    let results = client.browse({
        nodes: ["ns=1;i=85"],
        nodeClassMask: ua.NodeClass.Variable,
        requestedMaxReferencesPerNode: 2,
    });

    while (results[0].continuationPoint) {
        results = client.browseNext({
            continuationPoints: [results[0].continuationPoint],
        });
        results[0].references.forEach((ref) => {
            console.println(ref.browseName, ref.nodeId, ref.nodeClass);
        });
    }
} catch (e) {
    console.println("Error:", e);
} finally {
    if (client !== undefined) client.close();
}
```

### children()

지정한 노드의 직접 자식 참조를 반환합니다.

**문법**

```js
children(childrenRequest)
```

**파라미터**

`childrenRequest` `Object` ChildrenRequest

**반환값**

`Object[]` ChildrenResult 배열

`node`가 없거나 비어 있으면 예외가 발생합니다.

```js
const ua = require("@jsh/opcua");

let client;
try {
    client = new ua.Client({ endpoint: "opc.tcp://localhost:4840" });
    const refs = client.children({
        node: "ns=1;i=85",
        nodeClassMask: ua.NodeClass.Variable,
    });

    refs.forEach((ref) => {
        console.println(ref.browseName, ref.nodeId, ref.nodeClass);
    });
} catch (e) {
    console.println("Error:", e);
} finally {
    if (client !== undefined) client.close();
}
```

## ReadRequest

| 속성            | 타입       | 기본값                       | 설명 |
|:--------------------|:-----------|:-----------------------------|:-----|
| nodes               | `string[]` |                               | 읽을 OPC UA 노드 ID 목록 |
| maxAge              | `number`   | `0`                           | 허용 가능한 캐시 연령(밀리초) |
| timestampsToReturn  | `number`   | `TimestampsToReturn.Neither` | 타임스탬프 반환 정책 |

## ReadResult

| 속성        | 타입     | 설명 |
|:----------------|:---------|:-----|
| status          | `number` | OPC UA 상태 코드(`uint32`) |
| statusText      | `string` | 상태 텍스트 |
| statusCode      | `string` | 상태 코드 이름(예: `StatusGood`) |
| value           | `any`    | 읽은 값 |
| type            | `string` | 값 타입 이름(예: `Boolean`, `Int32`, `Double`) |
| sourceTimestamp | `number` | 소스 타임스탬프(Unix epoch 밀리초) |
| serverTimestamp | `number` | 서버 타임스탬프(Unix epoch 밀리초) |

## WriteRequest

| 속성 | 타입     | 설명 |
|:---------|:---------|:-----|
| node     | `string` | 기록 대상 노드 ID |
| value    | `any`    | 기록할 값 |

## WriteResult

| 속성      | 타입       | 설명 |
|:--------------|:-----------|:-----|
| error         | `Error\|null` | 요청 처리 오류 |
| timestamp     | `number`   | 응답 타임스탬프(Unix epoch 밀리초) |
| requestHandle | `number`   | OPC UA 요청 핸들 |
| serviceResult | `number`   | OPC UA 서비스 결과 코드 |
| stringTable   | `string[]` | OPC UA 문자열 테이블 |
| results       | `number[]` | 노드별 상태 코드 배열 |

## BrowseRequest

| 속성                      | 타입       | 기본값                    | 설명 |
|:------------------------------|:-----------|:--------------------------|:-----|
| nodes                         | `string[]` |                           | 탐색할 OPC UA 노드 ID 목록 |
| browseDirection               | `number`   | `BrowseDirection.Forward` | 탐색 방향 |
| referenceTypeId               | `string`   | 모든 reference            | 따라갈 참조 타입 노드 ID |
| includeSubtypes               | `boolean`  | `true`                    | `referenceTypeId`의 하위 타입 포함 여부 |
| nodeClassMask                 | `number`   | `0`                       | 포함할 노드 클래스 비트마스크 |
| resultMask                    | `number`   | `BrowseResultMask.All`    | 반환할 필드 비트마스크 |
| requestedMaxReferencesPerNode | `number`   | `0`                       | 서버가 노드별 최대 참조 수를 나누어 반환하도록 요청하는 힌트 |

## BrowseNextRequest

| 속성                 | 타입       | 기본값  | 설명 |
|:-------------------------|:-----------|:--------|:-----|
| continuationPoints       | `string[]` |         | `browse()` 또는 `browseNext()`가 반환한 base64 continuation point 목록 |
| releaseContinuationPoints| `boolean`  | `false` | 다음 참조를 요청하지 않고 서버 측 continuation point를 해제할지 여부 |

## BrowseResult

| 속성          | 타입       | 설명 |
|:------------------|:-----------|:-----|
| status            | `number`   | OPC UA 상태 코드(`uint32`) |
| statusText        | `string`   | 상태 텍스트 |
| continuationPoint | `string`   | base64 continuation point. 다음 페이지가 없으면 빈 문자열 |
| references        | `object[]` | BrowseReference 배열 |

## BrowseReference

| 속성        | 타입      | 설명 |
|:----------------|:----------|:-----|
| referenceTypeId | `string`  | 참조 타입 노드 ID |
| isForward       | `boolean` | 정방향 참조 여부 |
| nodeId          | `string`  | 대상 노드 ID |
| browseName      | `string`  | Browse 이름 |
| displayName     | `string`  | Display 이름 |
| nodeClass       | `number`  | OPC UA 노드 클래스 값 |
| typeDefinition  | `string`  | 타입 정의 노드 ID |

## ChildrenRequest

| 속성      | 타입     | 설명 |
|:--------------|:---------|:-----|
| node          | `string` | 부모 노드 ID |
| nodeClassMask | `number` | 포함할 노드 클래스 비트마스크 |

## ChildrenResult

| 속성        | 타입      | 설명 |
|:----------------|:----------|:-----|
| referenceTypeId | `string`  | 참조 타입 노드 ID |
| isForward       | `boolean` | 정방향 참조 여부 |
| nodeId          | `string`  | 자식 노드 ID |
| browseName      | `string`  | Browse 이름 |
| displayName     | `string`  | Display 이름 |
| nodeClass       | `number`  | OPC UA 노드 클래스 값 |
| typeDefinition  | `string`  | 타입 정의 노드 ID |

## BrowseDirection

- `BrowseDirection.Forward`
- `BrowseDirection.Inverse`
- `BrowseDirection.Both`
- `BrowseDirection.Invalid`

## NodeClass

- `NodeClass.Unspecified`
- `NodeClass.Object`
- `NodeClass.Variable`
- `NodeClass.Method`
- `NodeClass.ObjectType`
- `NodeClass.VariableType`
- `NodeClass.ReferenceType`
- `NodeClass.DataType`
- `NodeClass.View`

## BrowseResultMask

- `BrowseResultMask.None`
- `BrowseResultMask.ReferenceTypeId`
- `BrowseResultMask.IsForward`
- `BrowseResultMask.NodeClass`
- `BrowseResultMask.BrowseName`
- `BrowseResultMask.DisplayName`
- `BrowseResultMask.TypeDefinition`
- `BrowseResultMask.All`
- `BrowseResultMask.ReferenceTypeInfo`
- `BrowseResultMask.TargetInfo`

## MessageSecurityMode

- `MessageSecurityMode.None`
- `MessageSecurityMode.Sign`
- `MessageSecurityMode.SignAndEncrypt`
- `MessageSecurityMode.Invalid`

## TimestampsToReturn

- `TimestampsToReturn.Source`
- `TimestampsToReturn.Server`
- `TimestampsToReturn.Both`
- `TimestampsToReturn.Neither`
- `TimestampsToReturn.Invalid`
