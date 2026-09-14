# Machbase Neo JavaScript Service Module

`service` 모듈은 JSH 애플리케이션에서 서비스 컨트롤러 JSON-RPC API를 호출하기 위한 클라이언트 인터페이스입니다.

```js
const service = require('service');
```

## Client

서비스 클라이언트 인스턴스를 만듭니다.

### Syntax

```js
new service.Client([options])
```

### Options

| 옵션 | 타입 | 기본값 | 설명 |
|:-------|:-----|:--------|:------------|
| `controller` | String | `SERVICE_CONTROLLER` 환경변수 | 컨트롤러 주소 (host:port, tcp://, unix://) |
| `timeout` | Number | 5000 | RPC 타임아웃(밀리초) |

## 메서드

### status(callback)

서비스 상태 정보를 조회합니다.

### read(callback)

현재 서비스 설정을 읽습니다.

### update(config, callback)

서비스 설정을 갱신합니다.

### reload(callback)

서비스 설정을 다시 불러옵니다.

### install(config, callback)

새 서비스를 설치합니다.

### uninstall(callback)

서비스를 제거합니다.

### start(callback)

서비스를 시작합니다.

### stop(callback)

서비스를 중지합니다.

### call(method[, params], callback)

컨트롤러의 임의 JSON-RPC 메서드를 호출합니다.

| 파라미터 | 타입 | 설명 |
|:----------|:-----|:------------|
| `method` | String | RPC 메서드 이름 |
| `params` | Object | 선택적 메서드 파라미터 |
| `callback` | Function | 오류 우선 콜백 `(err, result)` |

## Runtime

### runtime.get(callback)

서비스 컨트롤러에서 런타임 정보를 조회합니다.

## Details

`details` 하위 API는 서비스와 연결된 키-값 쌍을 관리합니다.

### details.get(name[, key], callback)

detail 값을 조회합니다.

### details.add(name, key, value, callback)

새 detail 항목을 추가합니다.

### details.update(name, key, value, callback)

기존 detail 항목을 갱신합니다.

### details.set(name, key, value, callback)

detail 항목을 설정합니다(생성 또는 갱신).

### details.delete(name, key, callback)

detail 항목을 삭제합니다.

## 서비스 설정 형식

서비스 정의는 JSON 객체입니다. 설치에 성공하면 컨트롤러는 서비스 정의를 `/etc/services/<name>.json` 파일로 저장합니다. 파일 이름은 JSON의 `name` 값으로 결정됩니다.

```json
{
  "name": "alpha",
  "enable": true,
  "working_dir": "/work/app",
  "environment": {
    "APP_MODE": "prod",
    "PORT": "8080"
  },
  "executable": "server.js",
  "args": ["--port", "8080"]
}
```

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `name` | `String` | 서비스 이름 |
| `enable` | `Boolean` | 서비스 활성화 여부 |
| `working_dir` | `String` | 서비스 프로세스의 작업 디렉터리 |
| `environment` | `Object` | `KEY: VALUE` 형식의 환경 변수 맵 |
| `executable` | `String` | 실행 파일 경로 또는 명령 이름 |
| `args` | `Array<String>` | 명령행 인자 목록 |

## servicectl 명령

셸에서는 `servicectl` 명령으로 같은 컨트롤러를 조작할 수 있습니다.

`servicectl read` 결과는 하나의 테이블로 출력되며, 각 행의 `STATUS` 컬럼에 `UNCHANGED`, `ADDED`, `UPDATED`, `REMOVED`, `ERRORED` 상태가 표시됩니다.

```sh
/work > servicectl read
┌────────┬───────────┬────────────┬──────────────┬─────────────┬────────────┐
│ NAME   │ STATUS    │ EXECUTABLE │ READ_ERROR   │ START_ERROR │ STOP_ERROR │
├────────┼───────────┼────────────┼──────────────┼─────────────┼────────────┤
│ alpha  │ UNCHANGED │ echo       │              │             │            │
│ beta   │ ADDED     │ node       │              │             │            │
│ old    │ REMOVED   │ sleep      │              │             │            │
│ broken │ ERRORED   │            │ invalid json │             │            │
└────────┴───────────┴────────────┴──────────────┴─────────────┴────────────┘
```

### update와 reload의 차이

두 명령 모두 컨트롤러에게 설정 변경 적용을 요청하지만 동작이 다릅니다.

- `update`: 현재 읽어 둔 변경분만 적용합니다. 추가·제거·수정된 서비스만 반영하고 나머지 서비스는 그대로 둡니다.
- `reload`: 설정 파일을 다시 읽은 뒤, 실행 중인 서비스를 모두 먼저 종료하고 변경 사항을 반영한 다음 `enable=true`인 서비스만 다시 시작합니다.

출력은 두 섹션으로 구성됩니다.

- `ACTIONS`: `UPDATE stop`, `UPDATE start`, `RELOAD stop`, `RELOAD start` 같은 수행 작업 목록
- `SERVICES`: 적용 후의 서비스 상태 표

## 동작 참고사항

- 모든 API는 오류 우선 콜백을 사용하는 콜백 기반 비동기 방식입니다.
- 이 모듈은 대기 중인 요청이 있을 때 스크립트가 조기 종료되지 않도록 내부 keepalive 메커니즘을 유지합니다.
- keepalive 지속 시간은 설정된 타임아웃 값과 연동됩니다.
- `SERVICE_CONTROLLER` 환경 변수가 컨트롤러 주소를 지정하는 표준 방법입니다.
