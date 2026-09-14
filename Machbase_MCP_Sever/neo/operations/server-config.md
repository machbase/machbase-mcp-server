# Machbase Neo Config file

## 새 설정 파일 생성

machbase-neo를 `gen-config`로 실행하고 그 출력을 기본 설정 파일로 저장합니다

```sh
machbase-neo gen-config > ./machbase-neo.conf
```

생성된 설정을 원하는 대로 수정한 뒤, `--config <path>` 또는 `-c <path>` 옵션으로 설정 파일 위치를 지정해 machbase-neo를 시작합니다.

```sh
machbase-neo serve --config ./machbase-neo.conf
```

## 데이터베이스 디렉토리

`DataDir`의 기본값은 `${execDir()}/machbase_home`으로, `machbase-neo` 실행 파일이 있는 위치의 하위 디렉토리입니다.

데이터베이스 파일을 저장하려는 새 경로로 바꾸세요. 폴더가 비어 있고 데이터베이스 파일이 없으면 machbase-neo가 자동으로 새 데이터베이스를 만듭니다.

## 환경설정 디렉토리

`PrefDir`의 기본값은 `prefDir("machbase")`이며 이는 `$HOME/.config/machbase`입니다.

## Listeners

| 리스너                    | 설정 키                   | 기본값                  |
|:--------------------------|:--------------------------|:------------------------|
| SSH Shell                 | Shell.Listeners           | `tcp://127.0.0.1:5652`  |
| MQTT                      | Mqtt.Listeners            | `tcp://127.0.0.1:5653` `unix://${tempDir()}/machbase-neo-mqtt.sock`  |
| HTTP                      | Http.Listeners            | `tcp://127.0.0.1:5654` `unix://${tempDir()}/machbase-neo.sock`  |
| Machbase 네이티브         | Machbase.PORT_NO          | `5656`                  |
|                           | Machbase.BIND_IP_ADDRESS  | `127.0.0.1`             |

> **ℹ️ Info**  
> Machbase 네이티브 포트 `5656`은 JDBC, ODBC 같은 네이티브 클라이언트가 사용합니다.  
> JDBC, ODBC 드라이버는 Machbase 홈페이지에서 받을 수 있습니다.

## 설정 레퍼런스

설정 파일은 HCL 문법을 따릅니다.

### functions

설정 항목의 값으로 몇 가지 함수를 사용할 수 있습니다.

- `flag(A, B)` : 명령행 플래그 'A'의 값을 가져옵니다. 지정되지 않았으면 B를 기본값으로 사용합니다.
- `env(A, B)` : 환경 변수 'A'의 값을 가져옵니다. 지정되지 않았으면 B를 기본값으로 사용합니다
- `execDir()` : 실행 파일이 있는 디렉토리 경로를 가져옵니다.
- `tempDir()` : 시스템 임시 디렉토리 경로를 가져옵니다.
- `userDir()` : 사용자 홈 디렉토리를 가져옵니다. Linux와 macOS에서는 $HOME 환경 변수를 반환합니다.
- `prefDir(subdir)` : 사용자 환경설정 디렉토리를 가져옵니다. Linux와 macOS에서는 $HOME/.config/{subdir}의 실제 경로를 반환합니다

> **ℹ️ env()와 flag() 조합**  
> 사용자 설정을 찾을 때는 명령행 플래그를 먼저 확인하고, 그다음 환경 변수를 찾고, 둘 다 없으면 기본값을 적용하는 것이 일반적인 방식입니다.  
> 이런 경우 `flag("--my-var", env("MY_VAR", "myvalue"))`처럼 작성할 수 있습니다

### define DEF

이 섹션은 기본값을 정의합니다. 여기의 변수들은 다른 섹션에서 참조됩니다. 사용자가 직접 변수를 정의할 수 있고 명령행 플래그도 바꿀 수 있습니다. 아래 예제에서 `LISTEN_HOST`는 명령행의 `--host` 플래그에서 값을 가져오되, `--host` 플래그가 없으면 `"127.0.0.1"`을 기본값으로 사용합니다.

`"127.0.0.1"`을 `"192.168.1.10"`으로 바꾸면 기본값이 바뀝니다.

예를 들어 `"--host"`를 `"--bind"`로 바꾸면 명령행 플래그가 바뀝니다. 그 후로는 `machbase-neo serve --host <ip_addr>` 대신 `machbase-neo serve --bind <ip_addr>`를 사용할 수 있습니다.

```hcl
define DEF {
    LISTEN_HOST       = flag("--host", "127.0.0.1")
    SHELL_PORT        = flag("--shell-port", "5652")
    MQTT_PORT         = flag("--mqtt-port", "5653")
    HTTP_PORT         = flag("--http-port", "5654")
    MACH_PORT         = flag("--mach-port", "5656")
}
```

### define VARS

이 섹션은 공통으로 사용되는 변수를 정의합니다. 

```hcl
define VARS {
    PREF_DIR              = flag("--pref", prefDir("machbase"))
    DATA_DIR              = flag("--data", "${execDir()}/machbase_home")
    FILE_DIR              = flag("--file", "${execDir()}")
    UI_DIR                = flag("--ui", "")
    MACH_LISTEN_HOST      = flag("--mach-listen-host", DEF_LISTEN_HOST)
    MACH_LISTEN_PORT      = flag("--mach-listen-port", DEF_MACH_PORT)
    SHELL_LISTEN_HOST     = flag("--shell-listen-host", DEF_LISTEN_HOST)
    SHELL_LISTEN_PORT     = flag("--shell-listen-port", DEF_SHELL_PORT)
    HTTP_LISTEN_HOST      = flag("--http-listen-host", DEF_LISTEN_HOST)
    HTTP_LISTEN_PORT      = flag("--http-listen-port", DEF_HTTP_PORT)
    MQTT_LISTEN_HOST      = flag("--mqtt-listen-host", DEF_LISTEN_HOST)
    MQTT_LISTEN_PORT      = flag("--mqtt-listen-port", DEF_MQTT_PORT)
    MQTT_MAXMESSAGE       = flag("--mqtt-max-message", 1048576) // 1MB

    HTTP_ENABLE_TOKENAUTH = flag("--http-enable-token-auth", false)
    MQTT_ENABLE_TOKENAUTH = flag("--mqtt-enable-token-auth", false)
    MQTT_ENABLE_TLS       = flag("--mqtt-enable-tls", false)

    HTTP_ENABLE_WEBUI     = flag("--http-enable-web", true)
    HTTP_DEBUG_MODE       = flag("--http-debug", false)

    EXPERIMENT_MODE       = flag("--experiment", false)

    MACHBASE_ENABLE_SIGHANDLER = flag("--machbase-enable-sighandler", false)
    MACHBASE_INIT_OPTION       = flag("--machbase-init-option", 2)

    CREATEDB_SCRIPT_FILES  = flag("--createdb-script-files", "")
}
```

### 로깅 설정

| 키                          | 타입      | 설명                                                     |
|:----------------------------|:----------|----------------------------------------------------------|
| Console                     | bool      | 콘솔에 로그 메시지 출력                                  |
| Filename                    | string    | 로그 파일 경로. `-`는 표준 출력. 예) /logs/machbase-neo.log |
| DefaultPrefixWidth          | int       | 로그 접두어 정렬 폭                                      |
| DefaultEnableSourceLocation | bool      | 소스 파일명과 줄 번호 기록 활성화                        |
| DefaultLevel                | string    | `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`                |
| Levels                      | array     | Level 객체의 배열                                    |
| Append                      | bool      | 로그 파일이 있으면 이어 쓰기                             |
| RotateSchedule              | string    | 로그 파일 회전 스케줄. 예) "@midnight"              |
| MaxSize                     | int       | 로그 파일 최대 크기(MB)                                  |
| MaxBackups                  | int       | 백업 파일 최대 개수                               |
| MaxAge                      | int       | 백업 파일을 보관할 최대 일수                        |
| Compress                    | bool      | 백업 파일 압축                                           |
| UTC                         | bool      | 로깅에 UTC 시간 사용                                 |

- Level 객체

| 키                          | 타입      | 설명                                                     |
|:----------------------------|:----------|----------------------------------------------------------|
| Pattern                     | string    | 로거 이름에 대한 glob 패턴                          |
| Level                       | string    | 해당 로거의 로그 레벨                                 |

```hcl
module "machbase.com/neo-logging" {
    name = "neolog"
    config {
        Console                     = false
        Filename                    = flag("--log-filename", "-")
        Append                      = flag("--log-append", true)
        RotateSchedule              = flag("--log-rotate-schedule", "@midnight")
        MaxSize                     = flag("--log-max-size", 10)
        MaxBackups                  = flag("--log-max-backups", 1)
        MaxAge                      = flag("--log-max-age", 7)
        Compress                    = flag("--log-compress", false)
        UTC                         = flag("--log-time-utc", false)
        DefaultPrefixWidth          = 16
        DefaultEnableSourceLocation = flag("--log-source-location", false)
        DefaultLevel                = flag("--log-level", "INFO")
        Levels = [
            { Pattern="neo*", Level="TRACE" },
            { Pattern="http-log", Level="DEBUG" },
        ]
    }
}
```

### 서버 설정

이 섹션은 데이터베이스 서버에 대한 것으로, 여러 부분으로 구성되며 각 부분은 절별로 설명합니다.

#### MachbaseHome

| 키                          | 타입      | 설명                                                     |
|:----------------------------|:----------|----------------------------------------------------------|
| MachbaseHome                | string    | 데이터베이스 파일이 저장되는 디렉토리 경로           |

#### Machbase

Machbase 코어 속성이 여기에 있습니다. 자세한 내용은 Machbase 매뉴얼의 Property 절을 참고하세요.

#### Shell

ssh를 통해 machbase-neo 셸에 원격 접속할 수 있게 합니다. 기본 `LISTEN_HOST`가 `"127.0.0.1"`이므로 ssh 접속은 같은 호스트에서만 가능합니다. 원격 접속을 허용하려면 `"0.0.0.0"` 또는 호스트 머신의 정확한 IP 주소를 설정하세요.

> **⚠️ Security**  
> 원격 접속을 허용하기 전에 `SYS`의 기본 비밀번호를 `manager`에서 직접 정한 값으로 바꾸기를 강력히 권장합니다.

| 키                          | 타입               | 설명                                                     |
|:----------------------------|:-------------------|----------------------------------------------------------|
| Listeners                   | array of string    | 수신 주소 (예: `tcp://127.0.0.1:5652`, `tcp://0.0.0.0:5652`)|
| IdleTimeout                 | duration           | 지정한 시간 동안 활동이 없으면 서버가 ssh 연결을 닫습니다 |

#### Http

서버의 HTTP 리스너 설정입니다.

| 키                          | 타입               | 설명                                                     |
|:----------------------------|:-------------------|----------------------------------------------------------|
| Listeners                   | array of string    | 수신 주소                                      |
| EnableTokenAuth             | bool               | 토큰 기반 인증 활성화 (기본값 `false`)      |
| EnableWebUI                 | bool               | 웹 사용자 인터페이스 활성화 (기본값 `true`)               |

#### Mqtt

| 키                          | 타입               | 설명                                                     |
|:----------------------------|:-------------------|----------------------------------------------------------|
| Listeners                   | array of string    | 수신 주소                                       |
| MaxMessageSizeLimit         | int                | PUBLISH 페이로드의 최대 크기 제한 (기본값 1048576 = 1MB) |
| EnableTokenAuth             | bool               | 토큰 기반 인증 활성화 (기본값 `false`)      |
| EnableTls                   | bool               | TCP 리스너에 TLS 활성화 (기본값 `false`)                 |

### neo-server 설정

```hcl
module "machbase.com/neo-server" {
    name = "neosvr"
    config {
        PrefDir          = VARS_PREF_DIR
        DataDir          = VARS_DATA_DIR
        FileDirs         = [ VARS_FILE_DIR ]
        ExperimentMode   = VARS_EXPERIMENT_MODE
        CreateDBScriptFiles = [ VARS_CREATEDB_SCRIPT_FILES ]
        Machbase         = {
            HANDLE_LIMIT     = 2048
            PORT_NO          = VARS_MACH_LISTEN_PORT
            BIND_IP_ADDRESS  = VARS_MACH_LISTEN_HOST
        }
        Shell = {
            Listeners        = [ "tcp://${VARS_SHELL_LISTEN_HOST}:${VARS_SHELL_LISTEN_PORT}" ]
            IdleTimeout      = "5m"
        }
        Http = {
            Listeners        = [ "tcp://${VARS_HTTP_LISTEN_HOST}:${VARS_HTTP_LISTEN_PORT}" ]
            WebDir           = VARS_UI_DIR
            EnableTokenAuth  = VARS_HTTP_ENABLE_TOKENAUTH
            DebugMode        = VARS_HTTP_DEBUG_MODE
            EnableWebUI      = VARS_HTTP_ENABLE_WEBUI
        }
        Mqtt = {
            Listeners           = [ "tcp://${VARS_MQTT_LISTEN_HOST}:${VARS_MQTT_LISTEN_PORT}"]
            EnableTokenAuth     = VARS_MQTT_ENABLE_TOKENAUTH
            EnableTls           = VARS_MQTT_ENABLE_TLS
            MaxMessageSizeLimit = VARS_MQTT_MAXMESSAGE
        }
        Jwt = {
            AtDuration = flag("--jwt-at-expire", "5m")
            RtDuration = flag("--jwt-rt-expire", "60m")
        }
        MachbaseInitOption       = VARS_MACHBASE_INIT_OPTION
        EnableMachbaseSigHandler = VARS_MACHBASE_ENABLE_SIGHANDLER
    }
}
```
