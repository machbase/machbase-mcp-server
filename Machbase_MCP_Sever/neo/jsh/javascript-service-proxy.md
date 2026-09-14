# Machbase Neo JavaScript Service Proxy

서비스 프록시 기능(v8.5.2부터)을 사용하면 JSH 서비스가 별도 포트를 열지 않고도 machbase-neo를 통해 내부 HTTP 서버를 노출할 수 있습니다.

공개 라우트로 들어온 요청은 등록된 대상으로 리버스 프록시됩니다.

## Public Route Format

```
/web/services/<service_name>/<prefix>/*
```

Example: `/web/services/github.com/acme/chart/api/series`

## Registration

### service.proxy.register()

프록시 엔드포인트를 등록합니다.

```js
service.proxy.register({
    name: 'my-service',
    prefix: '/api',
    target: 'http://127.0.0.1:9090',
    stripPrefix: true,
    healthPath: '/health'
});
```

| 파라미터 | 타입 | 설명 |
|:----------|:-----|:------------|
| `name` | String | 서비스 식별자(패키지 이름 권장) |
| `prefix` | String | 라우팅에 사용할 URL 접두어 |
| `target` | String | Internal server URL |
| `stripPrefix` | Boolean | 전달 전에 접두어를 제거할지 여부 |
| `healthPath` | String | 선택적 헬스 체크 경로 |

### Target Restrictions

허용되는 대상:
- `http://127.0.0.1:<port>`
- `http://localhost:<port>`
- 루프백 IP 주소
- `unix://<absolute_socket_path>`

프록시가 오픈 릴레이가 되는 것을 막기 위해 외부 호스트와 `https://` 대상은 기본적으로 허용되지 않습니다.

### service.proxy.unregister()

프록시 엔드포인트를 제거합니다. prefix를 생략하면 해당 서비스의 모든 엔드포인트가 제거됩니다.

### proxy.list()

등록된 모든 프록시 엔드포인트를 나열합니다.

### proxy.get(name)

특정 서비스의 프록시 등록 정보를 가져옵니다.

## CLI Management

```sh
servicectl proxy list
servicectl proxy get <name>
```

## 동작 참고사항

- 등록 정보는 런타임 상태이므로 재시작 후 다시 등록해야 합니다.
- 별도의 네임스페이스 제한은 없으며, 먼저 등록한 쪽이 이름/prefix 쌍을 차지합니다.
- 하나의 서비스가 여러 프록시 엔드포인트를 동시에 등록할 수 있습니다.
- 충돌을 막기 위해 서비스 식별자로 패키지 이름을 사용하는 것을 권장합니다.
