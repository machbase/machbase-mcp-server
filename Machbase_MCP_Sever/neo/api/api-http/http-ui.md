# Machbase Neo HTTP User Interface API

이 사용자 인터페이스 API는 JWT 기반 인증으로 클라이언트의 요청을 검증합니다.

## 사용자 인증

### Login

**POST `/web/api/login`**

**Request:**
```json
{
    "loginName": "sys",
    "password": "manager"
}
```

**Response:**
```json
{
    "success": true,
    "accessToken": "jwt-access-token",
    "refreshToken": "jwt-refresh-token",
    "reason": "string",
    "elapse": "string",
    "server": { "version": "v1.2.3" }
}
```

### 토큰 갱신

**POST `/web/api/relogin`**

**Request:**
```json
{
    "refreshToken": "refresh token that was issued with 'login'"
}
```

**Response:**
```json
{
    "success": true,
    "accessToken": "jwt access token",
    "refreshToken": "jwt refresh token",
    "reason": "string",
    "elapse": "string",
    "server": { "version": "v1.2.3" }
}
```

### Logout

**POST `/web/api/logout`**

- `LogoutReq`:

```json
{
    "refreshToken": "refresh token that was issued with 'login'"
}
```

### Status

**GET `/web/api/check`**

현재 토큰 상태를 검증합니다.

- `LoginCheckRsp`
```json
{
    "success": true,
    "reason": "string",
    "elapse": "string",
    "experimentMode": false,
    "server": {"version":"v1.2.3"},
    "shells": [{"ShellDefinition"}]
}
```

- `ShellDefinition`
```json
{
    "id": "shell definition id (uuid)",
    "type": "type",
    "icon": "icon name",
    "label": "display name",
    "theme": "theme name",
    "command": "terminal shell command",
    "attributes": [
        { "removable": true },
        { "cloneable": true },
        { "editable": true }
    ]
}
```

- types

| 타입 | 설명      |
|:-----| :------------    |
| sql  | SQL 에디터       |
| tql  | TQL 에디터       |
| wrk  | 워크스페이스 에디터 |
| taz  | 태그 분석기     |
| term | 터미널         |

## Database

### Execute SQL

**GET,POST `/web/machbase`**

`/db/query` API와 동일하게 동작하며 인증 방식만 다릅니다.
`/db/query`는 API 토큰으로 클라이언트 애플리케이션을 인가하고, `/web/machbase`는 사용자 상호작용을 위해 JWT를 검증합니다.

### List tables

**GET `/web/api/tables?showall=false&name=pattern`**

테이블 목록을 반환합니다

- `showall` `true`면 숨겨진 테이블까지 모두 반환합니다
- `name` 테이블 이름 필터 패턴. glob(`?`나 `*` 포함) 또는 접두(`?`와 `*`가 없는 경우)를 쓸 수 있습니다

```json
{
    "success": true,
    "reason": "success or other message",
    "elapse": "elapse time in string format",
    "data": {
        "columns": ["ROWNUM", "DB", "USER", "NAME", "TYPE"],
        "types": ["int32", "string", "string", "string", "string"],
        "rows":[
            [1, "MACHBASE", "SYS", "TABLENAME", "TAG TABLE"],
        ]
    }
}
```

### List tags

**GET `/web/api/tables/:table/tags?name=prefix`**

테이블의 태그 목록을 반환합니다

- `name` 주어진 접두로 시작하는 태그만 반환합니다

```json
{
    "success": true,
    "reason": "success or other message",
    "elapse": "elapse time in string format",
    "data": {
        "columns": ["ROWNUM", "NAME"],
        "types": ["int32", "string"],
        "rows":[
            [1, "temperature"],
        ]
    }
}
```

### Tag stat

**GET `/web/api/tables/:table/:tag/stat`**

테이블 태그의 통계를 반환합니다

```json
{
    "success": true,
    "reason": "success or other message",
    "elapse": "elapse time in string format",
    "data": {
        "columns": ["ROWNUM", "NAME", "ROW_COUNT", "MIN_TIME", "MAX_TIME",
			"MIN_VALUE", "MIN_VALUE_TIME", "MAX_VALUE", "MAX_VALUE_TIME", "RECENT_ROW_TIME"],
        "types": ["int32", "string", "int64", "datetime", "datetime","double", 
            "datetime", "double", , "datetime",, "datetime"],
        "rows":[
            ["...omit...."],
        ]
    }
}
```

## 셸 & 터미널

### 데이터 채널

**`ws:///web/api/term/:term_id/data`**

터미널용 웹소켓

### Window size

**POST `/web/api/term/:term_id/windowsize`**

터미널 크기 변경

`TerminalSize`

```json
{ "rows": 24, "cols": 80 }
```

### 셸 정의 조회

**GET `/web/api/shell/:id`**

주어진 id의 `ShellDefinition`을 반환합니다

### 셸 정의 수정

**POST `/web/api/shell/:id`**

주어진 id의 `ShellDefinition`을 수정합니다

### 셸 복사본 만들기

**GET `/web/api/shell/:id/copy`**

주어진 id의 셸을 복사한 새 `ShellDefinition`을 반환합니다

### 셸 정의 삭제 

**DELETE `/web/api/shell/:id`**

주어진 id의 셸을 삭제합니다

```json
{
    "success": true,
    "reason": "success of error message",
    "elapse": "time represents in text"
}
```

## 서버 이벤트

### 이벤트 채널

**`ws:/web/api/console/:console_id/data?token={jwt_token}`**

양방향 메시지용 웹소켓입니다. WebSocket 핸드셰이크는 HTTP `Authorization` 헤더를 보낼 수 없으므로, 이 엔드포인트는 `token` 쿼리 파라미터로 JWT 액세스 토큰을 전달해야 합니다.

- 메시지 타입

```json
{
    "type": "type(see below)",
    "ping": {
        "tick": 1234
    },
    "log": {
        "level": "INFO",
        "message": "log message"
    }
}
```

| 타입           |  필드          | 설명        |
|:---------------| :----------------| :------------------|
| `ping`         |                  | ping 메시지       |
|                | `ping.tick`      | 임의의 정수. 서버가 클라이언트가 보낸 것과 같은 수로 응답합니다 |
| `log`          | `log.level`      | log level `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`|
|                | `log.message`    | log message        |
|                | `log.repeat`     | 같은 메시지가 연속으로 두 번 넘게 반복될 때의 횟수 |


## TQL & 워크스페이스

**TQL의 Content-type**

| 헤더 <br/>`Content-Type` | 헤더 <br/>`X-Chart-Type` |          내용            |
|:--------------------------:| :-------------------------:| :-------------------------- |
| text/html                  | "echart", "geomap"         | 전체 HTML <br/>예) `<iframe>` 안에 넣을 수 있습니다|
| text/html                  | -                          | 전체 HTML <br/>예) `<iframe>` 안에 넣을 수 있습니다 |
| text/csv                   | -                          | CSV                         |
| text/markdown              | -                          | 마크다운                    |
| application/json           | "echart", "geomap"         | JSON (echart 또는 geomap 데이터)|
| application/json           | -                          | JSON                        |
| application/xhtml+xml      | -                          | HTML 요소, 예) `<div>...</div>` |


### Run tql file

**GET `/web/api/tql/*path`**

해당 경로의 tql을 실행합니다. 응답은 'Content-types of TQL' 항목을 참고하세요

**POST `/web/api/tql/*path`**

해당 경로의 tql을 실행합니다. 응답은 'Content-types of TQL' 항목을 참고하세요

### tql 스크립트 실행

**POST `/web/api/tql`**

tql 스크립트를 내용 페이로드로 전송하면 서버가 실행 결과를 응답합니다.
응답은 'Content-types of TQL' 항목을 참고하세요.

요청에 `$` 이름의 쿼리 파라미터가 있으면 그것을 tql 스크립트로 취급하고,
페이로드는 데이터로 취급합니다. 이 `$` 쿼리 파라미터는 v8.0.17부터 사용할 수 있습니다.

### 마크다운 렌더링

**POST `/web/api/md`**

마크다운을 내용 페이로드로 전송하면 서버가 xhtml로 렌더링 결과를 응답합니다

## 파일 관리

### Content-Type

파일 유형과 content-type

| 파일 유형 | Content-Type             |
|:----------|:-------------------------|
| .sql      | text/plain               |
| .tql      | text/plain               |
| .taz      | application/json         |
| .wrk      | application/json         |
| 알 수 없음   | application/octet-stream |

### Read file

**GET `/web/api/files/*path`**

경로가 파일을 가리키면 파일 내용을 반환합니다.

경로가 디렉터리를 가리키면 디렉터리 항목들을 반환합니다.

- `Entry`

```json
{
    "isDir": true,
    "name": "name",
    "content": "bytes array, if the entry is a file",
    "children": [{"SubEntry, if the entry is a directory"}],
}
```

- `SubEntry`

```json
{
    "isDir": true,
    "name": "name",
    "type": "type",
    "size": 1234,
    "lastModifiedUnixMillis": 169384757
}
```

### 쓰기 file

**POST `/web/api/files/*path`**

- `path`가 파일을 가리키면 페이로드 내용을 파일에 씁니다.

- `path`가 디렉터리이고 내용 없이 요청하면 빈 디렉터리를 만듭니다.
  그리고 해당 디렉터리의 `Entry`를 반환합니다

- `path`가 디렉터리이고 페이로드가 `GitCloneReq` json이면,
  원격 git 저장소를 `path`에 클론하고 해당 디렉터리의 `Entry`를 반환합니다.

`GitCloneReq`

```json
{
    "command": "clone",
    "url": "https://github.com/machbase/neo-samples.git"
}
```

- `command` : `clone`, `pull`

### 파일 이름 변경/이동

**PUT `/web/api/files/*path`**

파일(또는 디렉터리)의 이름을 바꾸거나 이동합니다.

`RenameReq`

```json
{
    "destination": "target path",
}
```

작업이 정상적으로 완료되면 이 API는 상태 코드 `200 OK`를 반환합니다.


### Remove file

**DELETE `/web/api/files/*path`**

`path`의 파일을 삭제합니다. 경로가 비어 있지 않은 디렉터리를 가리키면 오류를 반환합니다.

## 키 관리

### List Key

**GET `/web/api/keys/:id`**

키 정보 목록을 반환합니다

`response`

```json
{
    "success": true,
    "reason": "success",
    "data": [
        {
            "idx": 0,
            "id": "eleven",
            "notBefore": 1713171461,
            "notAfter": 2028531461
        }
    ],
    "elapse": "131.9µs"
}
```
### 키 생성

**POST `/web/api/keys`**

키 생성
- `name` is required
- `notAfter` 만료일

**Request:**
```json
{
    "name": "eleven",
    "notBefore": 0,
    "notAfter": 0
}
```

**Response:**
```json
{
    "success": true,
    "reason": "success",
    "elapse": "5.4961ms",
    "certificate": "-----BEGIN CERTIFICATE-----\nXXXXXXXXXXXXXXXXXX\n-----END CERTIFICATE-----\n",
    "privateKey": "-----BEGIN EC PRIVATE KEY-----\nXXXXXXXXXXXXXXXX\n-----END EC PRIVATE KEY-----\n",
    "token": "eleven:b:XXXXXXXXXXXXXXXXX"
}
```

### Delete Key

**DELETE `/web/api/keys/:id`**

주어진 id의 키를 삭제합니다

`response`

```json
{
    "success": true,
    "reason": "success",
    "elapse": "112.8µs"
}
```

## Ssh Key

### List Ssh Key

**GET `/web/api/sshkeys`**

ssh 키 정보 목록을 반환합니다

`response`

```json
{
    "data": [
        {
            "keyType": "ssh-rsa",
            "fingerprint": "f08h89fhf0dkv0v0v9c9x0cx9v9",
            "comment": "example@machbase.com"
        }
    ],
    "elapse": "67.6µs",
    "reason": "success",
    "success": true
}
```

### SSH 키 생성

**POST `/web/api/sshkeys`**

**SSH 공개 키 인증 사용**   

machbase-neo 서버에 공개 키를 추가하면 프롬프트나 비밀번호 입력 없이 모든 `machbase-neo shell` 명령을 실행할 수 있습니다.

**Request:**
```json
{
    "key": "your publickey"
}
```

**Response:**
```json
{
    "elapse": "138.801µs",
    "reason": "success",
    "success": true
}
```

### SSH 키 삭제

**DELETE `/web/api/sshkeys/:fingerprint`**

주어진 지문의 ssh 키를 삭제합니다   

`response`
```json
{
    "elapse": "198.8µs",
    "reason": "success",
    "success": true
}
```

## Timer

### Get Timer

**GET `/web/api/timers/:name`**

타이머 정보를 반환합니다

- state: `RUNNING`, `STARTING`, `STOP`, `STOPPING`,`FAILED`, `UNKNWON`

`response`

```json
{
    "success": true,
    "reason": "success",
    "data": [
        {
            "name": "ELEVEN",
            "type": "TIMER",
            "state": "STOP", 
            "task": "timer.tql",
            "schedule": "0 30 * * * *"
        }
    ],
    "elapse": "92.1µs"
}
```

### List Timer

**GET `/web/api/timers`**

타이머 정보 목록을 반환합니다
- state: `RUNNING`, `STARTING`, `STOP`, `STOPPING`,`FAILED`, `UNKNWON`

`response`

```json
{
    "success": true,
    "reason": "success",
    "data": [
        {
            "name": "ELEVEN",
            "type": "TIMER",
            "state": "STOP",
            "task": "timer.tql",
            "schedule": "0 30 * * * *"
        },
        {
            "name": "TWELVE",
            "type": "TIMER",
            "state": "RUNNING",
            "task": "timer2.tql",
            "schedule": "1 30 * * * *"
        }
    ],
    "elapse": "92.1µs"
}
```

### Add Timer

**POST `/web/api/timers`**

Add Timer
- `name`, `autoStart`, `schedule`, `path` is required  

Timer `schedule`
- `0 30 * * * *`           매시 30분마다
- `@every 1h30m`           1시간 30분마다
- `@daily`                 Every day

**Request:**
```json
{
    "name":"eleven",
    "autoStart":false,
    "schedule":"@every 10s",
    "path":"timer.tql"
}
```

**Response:**
```json
{
    "success": true,
    "reason": "success",
    "elapse": "4.9658ms"
}
```

### Start Timer

**POST `/web/api/timers/:name/state`**

Start Timer
- `state` is required

**Request:**
```json
{
    "state":"start",
}
```

**Response:**
```json
{
    "success": true,
    "reason": "success",
    "elapse": "822.601µs"
}
```

### Stop Timer

**POST `/web/api/timers/:name/state`**

Stop Timer
- `state` is required

**Request:**
```json
{
    "state":"stop",
}
```

**Response:**
```json
{
    "success": true,
    "reason": "success",
    "elapse": "26.2µs"
}
```

### 타이머 수정

**PUT `/web/api/timers/:name`**

타이머 수정
- `autoStart`, `schedule`, `path` 

**Request:**
```json
{
    "audoStart" : true,
    "schedule":"@every 5s",
    "path":"timer.tql"
}
```

**Response:**
```json
{
    "elapse": "459.6µs",
    "reason": "success",
    "success": true
}
```

### 타이머 삭제

**DELETE `/web/api/timers/:name`**

타이머 삭제

`Response`
```json
{
    "success": true,
    "reason": "success",
    "elapse": "4.8664ms"
}
```

## Bridge

### List Bridge

**GET `/web/api/bridges`**

브리지 정보 목록을 반환합니다

`response`

```json
{
    "success": true,
    "reason": "success",
    "data": [
        {
            "name": "pg",
            "type": "postgres",
            "path": "host=127.0.0.1 port=5432 user=postgres password=1234 dbname=bridgedb sslmode=disable"
        }
    ],
    "elapse": "1.328301ms"
}
```
### Add Bridge

**POST `/web/api/bridges`**

Add Bridge
- `name`, `type`, `path` is required
- 지원 브리지 `SQLite`, `PostgreSql`, `Mysql`, `MSSQL`, `MQTT`

**Request:**
```json
{
    "name":"pg",
    "type":"postgres", // sqlite, postgres, mysql, mssql, mqtt
    "path":"host=127.0.0.1 port=5432 user=postgres password=1234 dbname=bridgedb sslmode=disable"
}
```

**Response:**
```json
{
    "success": true,
    "reason": "success",
    "elapse": "193.499µs"
}
```

### Exec Bridge

**POST `/web/api/bridges/:name/state`**

Exec Bridge
- `state`, `command` is required

**Request:**
```json
{
    "state":"exec",
    "command":"CREATE TABLE IF NOT EXISTS pg_example(id SERIAL PRIMARY KEY,company VARCHAR(50) UNIQUE NOT NULL,employee  INT,discount REAL,plan FLOAT(8),code UUID,valid BOOL, memo TEXT, created_on TIMESTAMP NOT NULL)"
}
```

**Response:**
```json
{
    "success": true,
    "reason": "success",
    "elapse": "217.4µs"
}
```

### 브리지 조회

**POST `/web/api/bridges/:name/state`**

브리지 조회
- `state`, `command` is required

**Request:**
```json
{
    "state":"query",
    "command":"select * from pg_example"
}
```

**Response:**
```json
{
    "success": true,
    "reason": "success",
    "column": [
        "id",
        "company",
        "employee",
        "discount",
        "plan",
        "code",
        "valid",
        "memo",
        "created_on"
    ],
    "rows": [
        [
            2,
            "test-company",
            10,
            1.234,
            2.3456,
            "c2d29867-3d0b-d497-9191-18a9d8ee7830",
            true,
            "test memo",
            "2023-08-09T14:20:00+09:00"
        ],
        [
            3,
            "test-company2",
            10,
            1.234,
            2.3456,
            null,
            null,
            null,
            "2023-08-09T14:20:00+09:00"
        ]
    ],
    "elapse": "53.015905ms"
}
```

### Test Bridge

**POST `/web/api/bridges/:name/state`**

Test Bridge

**Request:**
```json
{
    "state":"test",
}
```

**Response:**
```json
{
    "success": true,
    "reason": "success",
    "elapse": "331.1µs"
}
```

### 브리지 삭제

**DELETE `/web/api/bridges/:name`**

주어진 이름의 브리지를 삭제합니다

`response`

```json
{
    "success": true,
    "reason": "success",
    "elapse": "112.8µs"
}
```

## Subscriber

### 구독자 조회

**GET `/web/api/subscribers/:name`**

구독자 정보를 반환합니다
- state: `RUNNING`, `STARTING`, `STOP`, `STOPPING`,`FAILED`, `UNKNWON`
- `autoStart`, `queue`, `Qos` 필드는 omitempty입니다

`response`

```json
{
    "data": [
        {
            "name": "NATS_SUBR",
            "type": "SUBSCRIBER",
            "autoStart": true,  // omitempty
            "state": "RUNNING", 
            "task": "db/append/EXAMPLE:csv",
            "bridge": "my_nats",
            "topic": "iot.sensor",
            "queue":"", // omitempty
            "QoS":""    // omitempty
        }
    ],
    "elapse": "253.4µs",
    "reason": "success",
    "success": true
}
```

### 구독자 목록

**GET `/web/api/subscribers`**

구독자 정보 목록을 반환합니다
- state: `RUNNING`, `STARTING`, `STOP`, `STOPPING`,`FAILED`, `UNKNWON`
- `autoStart`, `queue`, `Qos` 필드는 omitempty입니다

`response`

```json
{
    "data": [
        {
            "name": "NATS_SUBR",
            "type": "SUBSCRIBER",
            "autoStart": true,  // omitempty
            "state": "RUNNING",
            "task": "db/append/EXAMPLE:csv",
            "bridge": "my_nats",
            "topic": "iot.sensor",
            "queue":"", // omitempty
            "QoS":""    // omitempty
        },
        {
            "name": "NATS_SUBR2",
            "type": "SUBSCRIBER",
            "autoStart": true,  // omitempty
            "state": "STARTING",
            "task": "db/insert/EXAMPLE2:csv",
            "bridge": "my_nats2",
            "topic": "iot.sensor2",
            "queue":"", // omitempty
            "QoS":""    // omitempty
        }
    ],
    "elapse": "253.4µs",
    "reason": "success",
    "success": true
}
```

### 구독자 추가

**POST `/web/api/subscribers`**

구독자 추가   
- `autostart`:   '--autostart'는 machbase-neo와 함께 구독자를 시작합니다. 수동 시작·중지하려면 생략하세요.   
- `name` 'nats_subr' 구독자의 이름입니다.   
- `bridge` 'my_nats' 구독자가 사용할 브리지의 이름입니다.   
- `topic` 'iot.sensor' 구독할 subject 이름입니다. NATS subject 문법을 따라야 합니다.   
- `task` 'db/append/EXAMPLE:csv' 쓰기 서술자입니다. 들어오는 데이터가 CSV 형식이고 append 모드로 EXAMPLE 테이블에 쓴다는 뜻입니다.   
- `autostart`는 machbase-neo가 시작될 때 구독자를 자동으로 시작합니다. autostart 모드가 아니면 subscriber start <name>, subscriber stop <name> 명령으로 수동 시작·중지할 수 있습니다.
- `QoS` <int> 브리지가 MQTT 타입이면 토픽 구독의 QoS 수준을 지정합니다. 0과 1을 지원하며 지정하지 않으면 기본값은 0입니다.
- `queue` <string> 브리지가 NATS 타입이면 Queue Group을 지정합니다.

nats-bridge 매뉴얼 https://docs.machbase.com/neo/bridges/31.nats/

**Request:**
```json
{
    "name":"nats_subr",
    "autoStart":true,
    "bridge":"my_nats",
    "topic":"iot.sensor",
    "task":"db/append/EXAMPLE:csv",
    "QoS": "",  // mqtt bridge option 0 or 1 ( default 0 )
    "queue": "" // nats birdge option
}
```

**Response:**
```json
{
    "elapse": "260µs",
    "reason": "success",
    "success": true
}
```

### 구독자 시작

**POST `/web/api/subscribers/:name/state`**

- `state` is required

**Request:**
```json
{
    "state":"start",
}
```

**Response:**
```json
{
    "elapse": "166.1µs",
    "reason": "success",
    "success": true
}
```

### 구독자 중지

**POST `/web/api/subscribers/:name/state`**

- `state` is required

**Request:**
```json
{
    "state":"stop",
}
```

**Response:**
```json
{
    "elapse": "54.2µs",
    "reason": "success",
    "success": true
}
```

### 구독자 삭제

**DELETE `/web/api/subscribers/:name`**

주어진 이름의 구독자를 삭제합니다

`response`

```json
{
    "elapse": "77.1µs",
    "reason": "success",
    "success": true
}
```

## Backup

### Get Backup

**GET `/web/api/backup/archives`**

백업 목록을 반환합니다
- 기본 백업 디렉터리 `$MACHBASE_HOME/dbs/backup`
- machbase-neo serve 시 `--backup-dir={path}` 필요

`response`

```json
{
    "data": [
        {
            "path": "example_backup1",
            "isMount": true,
            "mountName": "backup1"
        },
        {
            "path": "example_backup2",
            "isMount": false
        }
    ],
    "elapse": "6.562299ms",
    "reason": "success",
    "success": true
}
```

### DB Backup

**POST `/web/api/backup/archive`**

데이터베이스 백업</br>
- **전체 백업**:   전체 데이터 백업
- **증분 백업**:   전체 백업 또는 직전 증분 백업 이후 추가된 데이터 백업
- **기간 백업**:   특정 기간의 데이터 백업

`request`

**Full Backup:**
```json
{
    "type":"database", // database or table
    "tableName":"",
    "duration":{
        "type":"full",
        "after":"",
        "from":"",
        "to":""
    },
    "path":"example_backup1" 
    // "path":"/home/neo/backups/example_backup1" 
}
```

**증분 백업:**
```json
{
    "type":"database", // database or table
    "tableName":"",
    "duration":{
        "type":"incremental",
        "after":"{previous_backup_dir}",
        "from":"",
        "to":""
    },
    "path":"example_backup1" 
    // "path":"/home/neo/backups/example_backup1" 
}
```

**Time Backup:**
```json
{
    "type":"database", // database or table
    "tableName":"",
    "duration":{
        "type":"time",
        "after":"",
        "from":"2024-08-01 00:00:00",
        "to":"2024-08-02 23:59:59"
    },
    "path":"example_backup1" 
    // "path":"/home/neo/backups/example_backup1" 
}
```

**테이블 백업:**
```json
{
    "type":"table", // database or table
    "tableName":"example",
    "duration":{
        "type":"full",
        "after":"",
        "from":"",
        "to":""
    },
    "path":"example_backup1" 
    // "path":"/home/neo/backups/example_backup1" 
}
```

`response`
```json
{
    "success": true,
    "reason": "success",
    "elapse": "231.3µs"
}
```

### 백업 상태

**GET `/web/api/backup/archive/status`**

백업 상태 반환</br>

`response`
```json
{
    "data": {
        "type": "database",
        "tableName": "",
        "duration": {
            "type": "full",
            "after": "",
            "from": "",
            "to": ""
        },
        "path": "/home/neo/neo-server/tmp/machbase_home/dbs/example_backup1",
    },
    "elapse": "1.1µs",
    "reason": "success",
    "success": true
}
```

## Mount

### Mount List

**GET `/web/api/backup/mounts`**

마운트 목록을 반환합니다

`response`

```json
{
    "data": [
        {
            "name": "machbase_backup_19700101090000_20240726104832_15",
            "path": "backup1",
            "tbsid": 23,
            "scn": 15,
            "mountdb": "MOUNT_BACKUP1",
            "dbBeginTime": "1970-01-01 09:00:00",
            "dbEndTime": "2024-07-26 10:48:32",
            "backupBeginTime": "2024-07-26 10:48:32",
            "backupEndTime": "2024-07-26 10:48:34",
            "flag": 0
        }
    ],
    "elapse": "424.3µs",
    "reason": "success",
    "success": true
}
```

### DB Mount

**POST `/web/api/backup/mounts/:name`**

데이터베이스 마운트
- `:name` mount name
- `path` 백업 데이터베이스 경로 (`절대 경로`, `상대 경로` 모두 가능)

**Request:**
```json
{
    "path":"example_backup1" // Relative Path
    // "path":"/home/machbase/machbase_home/dbs/example_backup1" // Absolute Path
}
```

**Response:**
```json
{
    "elapse": "46.8694ms",
    "reason": "success",
    "success": true
}
```

### DB Unmount

**DELETE `/web/api/backup/mounts/:name`**

데이터베이스 언마운트
- `:name` 언마운트할 이름

`response`
```json
{
    "elapse": "46.8694ms",
    "reason": "success",
    "success": true
}
```

## Package

### Search

**GET `/web/api/pkgs/search?name=pkg_name&possibles=10`**

`Query Parameter`
 - `name` 패키지 이름, 필수
 - `possible` 검색 개수 ( possible=0 이면 전체 검색 )


`response`

```json
{
    "success": true,
    "reason": "success",
    "data":{},
    "elapse": "547.1µs"
}
```
### Sync

**GET `/web/api/pkgs/sync`**

패키지 동기화 

`response`

```json
{
    "success": true,
    "reason": "success",
    "elapse": "30.9144ms"
}
```

### Install

**GET `/web/api/pkgs/insall/:name`**

 - `:name` 설치할 패키지 이름, 필수

`response`
```json
{
    "success": true,
    "reason": "success",
    "data":{}, // omitempty
    "log":"",
    "elapse": "23.1491ms"
}
```

### Uninstall

**GET `/web/api/pkgs/uninsall/:name`**

 - `:name` 제거할 패키지 이름, 필수

`response`
```json
{
    "success": true,
    "reason": "success",
    "data":{}, // omitempty
    "log":"",
    "elapse": "88.4133ms"
}
```

## Others

### References

**GET `/web/api/refs/*path`**

- `ReferenceGroup`
```json
{
    "label": "group name",
    "items":[{"ReferenceItem"}]
}
```

- `ReferenceItem`
```json
{
    "type": "type",
    "title": "display title",
    "address": "url address",
    "target": "browser link target"
}
```

- type: `url`, `wrk`, `tql`, `sql`
- address: 주소에 `serverfile://<path>` 접두가 있으면 서버 측 파일을 가리키고, 
  그 외에는 `https://`로 시작하는 외부 웹 URL입니다


### SQL 문 분할기

**POST `/web/api/splitter/sql`**

```json
{
    "success": true,
    "reason": "success or error reason",
    "elapse": "elapse time",
    "data": {
        "statements": [
            {
                "text": "-- env: bridge=sqlite",
                "beginLine": 1,
                "endLine": 1,
                "isComment": true,
                "env": {
                    "bridge": "sqlite",
                    "error": "if there are syntax error in `-- env: bridge=database`"
                }
            },
            {
                "text": "select * from table",
                "beginLine": 2,
                "endLine": 2,
                "isComment": false,
                "env": {
                    "bridge": "sqlite",
                    "error": "if there are syntax error in `-- env: bridge=database`"
                }
            },
            {
                "text": "-- comment",
                "beginLine": 3,
                "endLine": 3,
                "isComment": true,
                "env": {}
            }
        ]
    }
}
```

### 라이선스 정보

**GET `/web/api/license`**

```json
{
    "success": true,
    "reason": "success or error reason",
    "elapse": "elapse time",
    "data": {
        "id": "license id",
        "type": "type",
        "customer": "customer",
        "project": "project",
        "countryCode": "country code",
        "installDate": "installation date",
        "issueDate": "license issue date"
    }
}
```

### 라이선스 설치

**POST `/web/api/license`**

라이선스 파일을 설치합니다
