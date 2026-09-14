# Machbase Neo Security Guide

## 키와 토큰 생성

### Web UI

1. 가장 왼쪽의 메뉴 아이콘을 선택합니다.

2. 그리고 좌측 상단 창에서 `+` 아이콘을 클릭합니다.

3. 고유한 이름으로 "Client Id"를 지정하고 유효 기간을 설정합니다(기본값은 오늘부터 3년).
그다음 "Generate"를 눌러 클라이언트용 키 파일을 생성합니다.

4. "Download *.zip" 버튼을 누르거나 각 파일 내용을 복사해 둡니다. 재생성이 불가능하므로 이때만 사본을 만들 수 있습니다.

### 셸 명령

하위 명령 `machbase-neo shell key`는 클라이언트 키와 토큰을 관리합니다.

**등록된 클라이언트 인증 키와 토큰 목록**

```
machbase-neo shell key list
```

미리 등록된 모든 client-id와 유효 기간을 나열합니다.

```
$ machbase-neo shell key list
┌────────┬──────────────────────┬───────────────────────────────┬───────────────────────────────┐
│ ROWNUM │ ID                   │ VALID FROM                    │ EXPIRE                        │
├────────┼──────────────────────┼───────────────────────────────┼───────────────────────────────┤
│      1 │ myid2                │ 2023-02-05 01:55:18 +0000 UTC │ 2033-02-02 01:55:18 +0000 UTC │
│      2 │ myid3                │ 2023-02-05 01:56:36 +0000 UTC │ 2033-02-02 01:56:36 +0000 UTC │
......
```

**기존 클라이언트 인증 키와 토큰 삭제**

```
machbase-neo shell key del <client-id>
```

```
$ machbase-neo shell key del myid2
deleted
```

**새 클라이언트 인증 키와 토큰 등록**

`machbase-neo shell key gen` 하위 명령은 주어진 client-id에 대해 새 키 쌍과 토큰을 생성합니다.
`--output` 옵션으로 지정한 파일에 키와 토큰을 기록합니다.

```
machbase-neo shell key gen <client-id> --output <output_file>
```

client-id `myapp01`에 대해 새 키를 생성하고 등록합니다. 생성된 키와 토큰은 `*_cert.pem`, `*_key.pem`, `*_token` 파일에 저장됩니다.

```
$ machbase-neo shell key gen myapp01 --output ./myapp01 
Save certificate ./myapp01_cert.pem
Save private key ./myapp01_key.pem
Save token ./myapp01_token
```

생성된 파일을 확인합니다.

```
$ ls -al ./myapp01*
-rw-r--r--  1 eirny  staff  782 Feb 20 19:33 ./myapp01_cert.pem
-rw-------  1 eirny  staff  390 Feb 20 19:33 ./myapp01_key.pem
-rw-------  1 eirny  staff   81 Feb 20 19:33 ./myapp01_token
```

- `*_cert.pem` 파일은 서버가 서명한 클라이언트용 X.509 인증서입니다.
- `*_key.pem` 파일은 클라이언트의 개인 키입니다.
- `*_token` 파일에는 클라이언트용 토큰 문자열이 들어 있습니다.

토큰 기반 인증에는 `*_token` 파일의 내용을 사용합니다.

```
$ cat ./myapp01_token 
myapp01:b:d59310703c1ebf627f8b781fb50437326ec65b067257ebc72f07b12846761d17   
```

**서버 인증서**

서버 인증서를 얻으려면 `machbase-neo key server-key --output <path>` 명령을 실행하세요. 지정한 경로의 파일로 서버 인증서를 내보냅니다.

```
machbase-neo shell key server-cert --output ./machbase-neo.crt
```

## HTTP 토큰 인증

machbase-neo의 HTTP API는 토큰 기반 인증을 지원합니다.

`--http-enable-token-auth true` 명령행 옵션을 지정하거나 설정 파일에서 `EnableTokenAuth = true`로 설정해 활성화합니다.
이 옵션으로 서버를 실행하면 모든 HTTP API 호출에 미리 등록된 토큰이 담긴 `Authorization` 헤더가 필요합니다.

```
machbase-neo serve --http-enable-token-auth true
```

시작 로그에 HTTP 토큰 인증이 활성화되었다고 표시됩니다.

```
......
2023/02/20 20:14:29.878 INFO  neo neosvr           HTTP token authentication enabled
2023/02/20 20:14:29.878 INFO  neo neosvr           HTTP Listen tcp://127.0.0.1:5654
......
```

### 토큰을 사용하는 HTTP 클라이언트

이 토큰으로 API 인증을 해 봅시다. 토큰 파일의 내용으로 `Authorization` bearer 헤더를 설정합니다.

```
curl --output - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2" \
    -H "Authorization: Bearer `cat ./http-api-app01_token`"
```

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      [ "wave.sin", 1675851592000000000, 0 ],
      [ "wave.cos", 1675851592000000000, 1 ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "1.866708ms"
}
```

이번에는 `Authorization` 헤더 없이, 또는 잘못된 토큰으로 시도해 봅시다.

```
curl --output - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2" \
    -H "Authorization: Bearer http-api-app01:b:intended-wrong-value"
```

클라이언트가 유효하지 않은 토큰을 보내면 서버는 아래와 같은 오류 json 메시지와 함께 `HTTP/1.1 401 Unauthorized`로 응답합니다.

```json
{"success":false,"reason":"invalid token"}
```

## MQTT 토큰 인증

machbase-neo의 MQTT API는 토큰 기반 인증을 지원합니다.

`--mqtt-enable-token-auth true` 명령행 옵션을 지정하거나 설정 파일에서 `EnableTokenAuth = true`로 설정해 활성화합니다.
이 옵션으로 서버를 실행하면 MQTT CONNECT 메시지에 미리 등록된 id와 토큰을 담은 `client-id`, `username`이 필요합니다.

```
machbase-neo serve --mqtt-enable-token-auth true
```

시작 로그에 MQTT 토큰 인증이 활성화되었다고 표시됩니다.

```
......
2023/02/21 13:43:11.178 INFO  neosvr           MQTT token authentication enabled
2023/02/21 13:43:11.180 INFO  mqtt-tcp         MQTT Listen tcp://127.0.0.1:5653
......
```

### 토큰을 사용하는 MQTT 클라이언트

CONNECT 메시지의 `username`에 등록된 토큰을 넣고 `password` 필드는 비워 둡니다.

```
mosquitto_pub -h 127.0.0.1 -p 5653 \
    --username `cat ./mqtt-api-app01_token` \
    -t db/write/EXAMPLE            \
    -m '[ "wave.pi", `date +%s000000000`, 3.1415]'
```

클라이언트가 `username` 필드에 올바른 토큰을 넣지 않으면 서버는 CONNECT 메시지를 거부합니다.

```
mosquitto_pub -h 127.0.0.1 -p 5653 -t db/write/EXAMPLE \
    -m '[ "wave.pi", `date +%s000000000`, 3.1415]'

Connection error: Connection Refused: not authorized.
Error: The connection was refused.
```

## MQTT X.509 인증

machbase-neo를 `--mqtt-enable-tls true` 명령행 옵션으로 시작하거나 설정 파일에서 `Tls.Enabled = true`로 설정하면,
machbase-neo는 클라이언트로부터 TLS(SSL) 연결을 받습니다. 
TLS가 활성화되면 토큰 기반 인증은 무시되고, 미리 등록된 X.509 인증서로 ssl 핸드셰이크를 성공적으로 마친 
연결만 허용됩니다.

> TLS 옵션이 적용되면 machbase-neo mqtt 서버는 CONNECT 메시지의 `username`과 `password` 필드를 무시합니다.
> 이 값들은 지정하지 마세요. 다만 명확성을 위해 `client-id`는 여전히 설정해야 합니다.

### X.509를 사용하는 MQTT 클라이언트

클라이언트는 위 절에서 생성한, 미리 등록된 client-id와 키, 인증서를 사용해야 합니다.
CONNECT 메시지의 `client-id`에 client-id를 지정하고 `username`과 `password`는 설정하지 않습니다.

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    --id myapp01            \
    --cert ./myapp01_cert.pem \
    --key ./myapp01_key.pem   \
    --cafile ./machbase-neo.crt --insecure \
    -t db/append/EXAMPLE            \
    -m '[ "wave.pi", `date +%s000000000`, 3.1415]'
```

- `--id` 키 생성에 사용한 `client-id`를 지정
- `--cert` `*_cert.pem`으로 생성된 클라이언트 인증서 파일
- `--key` `*_key.pem`으로 생성된 클라이언트 키 파일
- `--cafile` 클라이언트 인증서가 서버에 의해 서명되었으므로 서버 인증서를 지정합니다. 이 파일을 얻는 방법은 아래를 참고하세요.
- `--insecure` 서버 인증서가 자체 서명되어 있으므로 추가로 필요합니다.

---

## 보안 설정 요약

| 인증 방식 | 활성화 옵션 | 사용 예 |
|----------------------|-------------------|---------------|
| HTTP Token | `--http-enable-token-auth true` | curl -H "Authorization: Bearer token" |
| MQTT Token | `--mqtt-enable-token-auth true` | mosquitto_pub --username token |
| MQTT X.509 | `--mqtt-enable-tls true` | mosquitto_pub --cert cert.pem --key key.pem |
