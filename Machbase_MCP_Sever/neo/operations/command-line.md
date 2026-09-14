# Machbase Neo Command line

## machbase-neo serve

machbase-neo 서버 프로세스를 시작합니다.

### Flags

**일반 플래그**
             
| flag             | desc                                                              |
|:-----------------|:----------------------------------------------------------------- |
| `--host`         | 수신 네트워크 주소 (기본값: `127.0.0.1`) 예) `--host 0.0.0.0`                  |
| `-c`, `--config` | 설정 파일 위치. 예) `--config /data/machbase-neo.conf`|
| `--pid`          | pid를 저장할 파일 경로. 예) `--pid /data/machbase-neo.pid`    |
| `--data`         | 데이터베이스 경로 (기본값: `./machbase_home`) 예) `--data /data/machbase`                 |
| `--file`         | 파일 경로 (기본값: `.`) 예) `--file /data/files`                       |
| `--backup-dir`   | 백업 디렉토리 경로 (기본값: `./backups`) 예) `--backup-dir /data/backups` |
| `--pref`         | 환경설정 디렉토리 경로 (기본값: `~/.config/machbase`)                                |
| `--preset`       | 데이터베이스 프리셋 `auto`, `fog`, `edge` (기본값: `auto`) 예) `--preset edge`    |

**데이터베이스 세션 플래그**

개념적으로 machbase-neo를 tql을 포함한 API 부분(http, mqtt 등)과 DBMS 부분으로 나누어 보면, 지금까지 API와 DBMS 사이의 트래픽에는 제한이 없었습니다.

MQTT 클라이언트 100개와 HTTP 클라이언트 100개, 총 200개 클라이언트가 "동시에" db 질의를 실행하면 DBMS에서 200개 세션이 실행됩니다. DBMS로 전달되는 트래픽 흐름을 제어할 수 있는 수단이 있다면 상황에 따라 유연하게 구성할 수 있습니다. 이를 위해 `machbase-neo serve`에서 사용할 수 있는 새 플래그가 추가되었습니다.

데이터베이스 세션 풀 플래그 (Machbase Neo v8.5.5 이상):

| flag                     | desc                                                              |
|:-------------------------|:----------------------------------------------------------------- |
| `--max-open-conn`        | 데이터베이스에 대한 최대 열린 커넥션 수. (기본값 `-1`, 무제한) |
| `--max-idle-conn`        | 유휴 커넥션 풀의 최대 커넥션 수. `<= 0`이면 유휴 커넥션을 유지하지 않습니다. (기본값 `2`) |
| `--conn-max-lifetime`    | 커넥션을 재사용할 수 있는 최대 시간. 만료된 커넥션은 재사용 전에 지연 종료될 수 있습니다. `<= 0`이면 수명으로는 닫지 않습니다. (기본값 `10m`) |
| `--conn-max-idletime`    | 커넥션이 유휴 상태로 있을 수 있는 최대 시간. 만료된 커넥션은 재사용 전에 지연 종료될 수 있습니다. `<= 0`이면 유휴 시간으로는 닫지 않습니다. (기본값 `1m`) |

> **참고**: 이 직접 풀 설정 플래그들은 이전의 CPU 계수 기반 커넥션 설정(`--max-open-conn-factor`, `--max-open-query`, `--max-open-query-factor`)을 대체합니다.

**HTTP 플래그**

| 플래그                  | 기본값      | 설명                                                                      |
|:------------------------|:------------|:------------------------------------------------------------------------- |
| `--http-linger`         | `-1`        | HTTP 소켓 옵션. `-1`은 SO_LINGER 비활성화, `>=0`은 SO_LINGER 설정 |
| `--http-readbuf-size`   | `0`         | HTTP 소켓 읽기 버퍼 크기. `0`은 시스템 기본값 사용.                 |
| `--http-writebuf-size`  | `0`         | HTTP 소켓 쓰기 버퍼 크기. `0`은 시스템 기본값 사용.                |
| `--http-debug`          | `false`     | HTTP 디버그 로그 활성화                                                      |
| `--http-debug-latency`  | `"0"`       | 지정한 시간(예: "3s")보다 응답이 오래 걸린 HTTP 요청을 로그로 남깁니다. "0"은 모든 요청을 뜻합니다. |
| `--http-allow-statz`    |             | `/db/statz` API에 접근할 수 있는 출발지 IP(쉼표 구분)를 허용합니다. 기본값은 `127.0.0.1`만 허용합니다. |

**로그 플래그**

| 플래그                  | 기본값      | 설명                                                                      |
|:------------------------|:------------|:------------------------------------------------------------------------- |
| `--log-filename`        | `-` (stdout)| 로그 파일 경로. 예) `--log-filename /data/logs/machbase-neo.log`       |
| `--log-level`           | `INFO`      | 로그 레벨. TRACE, DEBUG, INFO, WARN, ERROR. 예) `--log-level INFO`    |
| `--log-append`          | `true`      | 기존 로그 파일에 이어 씁니다.                   |
| `--log-rotate-schedule` | `@midnight` | 시간 기반 로그 파일 회전            |
| `--log-max-size`        | `10`        | 파일 최대 크기(MB)                         |
| `--log-max-backups`     | `1`         | 로그 파일 백업 최대 개수                    |
| `--log-max-age`         | `7`         | 백업 파일 최대 보관 일수                | 
| `--log-compress`        | `false`     | 백업 파일을 gzip으로 압축              |
| `--log-time-utc`        | `false`     | 로깅에 UTC 시간 사용                    |

**리스너 플래그** (neo_since ver="8.0.36")

| 플래그           | 기본값    | 설명                            |
|:-----------------|:----------|-------------------------------- |
| `--shell-port`   | `5652`    | ssh 수신 포트                 |
| `--mqtt-port`    | `5653`    | mqtt 수신 포트                |
| `--mqtt-sock`    | `/tmp/machbase-neo-mqtt-5653.sock`| mqtt 유닉스 소켓 |
| `--http-port`    | `5654`    | http 수신 포트                |
| `--http-sock`    | `/tmp/machbase-neo-http-5654.sock` | http 유닉스 소켓 |
| `--mach-port`    | `5656`    | machbase 네이티브 수신 포트     |

> **📌 IMPORTANT**  
> `--host`의 기본값이 루프백 주소이므로 원격 호스트에서는 machbase-neo에 접속할 수 없습니다.  
> 원격 클라이언트의 네트워크 연결을 받으려면 `--host <host-address>` 또는 `--host 0.0.0.0`을 설정하세요.

플래그 없이 `machbase-neo serve`를 실행하면

```sh
$ machbase-neo serve
```

다음과 동일합니다

```sh
$ machbase-neo serve --host 127.0.0.1 --data ./machbase_home --file . --preset auto
```

## machbase-neo shell

machbase-neo 셸을 시작합니다. 다른 인자가 없으면 대화형 모드 셸로 시작합니다.

**플래그**

| 플래그(긴 형식)   | 기본값                 | 설명                                                             |
|:------------------|:-----------------------|:-----------------------------------------------------------------|
| `-s`, `--server`  | `127.0.0.1:5654`       | machbase-neo의 HTTP 주소. 예) `--server 127.0.0.1:5654` |
| `--user`          | `sys`                  | 사용자명. 환경 변수: `NEOSHELL_USER`         |
| `--password`      | `manager`              | 비밀번호. 환경 변수: `NEOSHELL_PASSWORD`      |

machbase-neo 셸이 시작되면 OS 환경 변수 `NEOSHELL_USER`와 `NEOSHELL_PASSWORD`에서 사용자명과 비밀번호를 찾습니다. 그리고 `--user`, `--password` 플래그가 주어지면 환경 변수 대신 플래그 값이 우선합니다.

### 사용자명과 비밀번호의 우선순위

#### 1단계: 명령행 플래그

`--user`, `--password`가 주어졌는가? 주어진 값을 사용합니다

#### 2단계: 환경 변수

`$NEOSHELL_USER`(윈도우는 `%NEOSHELL_USER%`)가 설정되어 있는가? 그 값을 사용자명으로 사용합니다.

`$NEOSHELL_PASSWORD`(윈도우는 `%NEOSHELL_PASSWORD%`)가 설정되어 있는가? 그 값을 비밀번호로 사용합니다.

#### 3단계: 기본값

아무것도 주어지지 않았는가? 기본값 `sys`와 `manager`를 사용합니다.

### 실전 사용법

보안을 위해 아래 예제처럼 일회성 환경 변수를 사용하세요.

```sh
$ NEOSHELL_PASSWORD='my-secret' machbase-neo shell --user sys
```

`--password` 플래그를 사용하면 아래 예제처럼 단순한 `ps` 명령만으로도 비밀번호가 노출될 수 있으니 주의하세요.

```sh
$ machbase-neo shell --user sys --password manager
```

```sh
$ ps -aef |grep machbase-neo
  501 13551  3598   0  9:33AM ttys000    0:00.07 machbase-neo shell --user sys --password manager
```

**질의 실행**

```sh
machbase-neo» select binary_signature from v$version;
┌────────┬─────────────────────────────────────────────┐
│ ROWNUM │ BINARY_SIGNATURE                            │
├────────┼─────────────────────────────────────────────┤
│      1 │ 8.0.2.develop-LINUX-X86-64-release-standard │
└────────┴─────────────────────────────────────────────┘
a row fetched.
```

**테이블 생성**

```sh
machbase-neo» create tag table if not exists example (name varchar(20) primary key, time datetime basetime, value double summarized);
executed.
```

**테이블 스키마**

```sh
machbase-neo» desc example;
┌────────┬───────┬──────────┬────────┐
│ ROWNUM │ NAME  │ TYPE     │ LENGTH │
├────────┼───────┼──────────┼────────┤
│      1 │ NAME  │ varchar  │     20 │
│      2 │ TIME  │ datetime │      8 │
│      3 │ VALUE │ double   │      8 │
└────────┴───────┴──────────┴────────┘
```

**테이블 입력**

```sh
machbase-neo» insert into example values('tag0', to_date('2021-08-12'), 100);
a row inserted.
```

**테이블 조회**

```sh
machbase-neo» select * from example;
┌────────┬──────┬─────────────────────┬───────┐
│ ROWNUM │ NAME │ TIME(LOCAL)         │ VALUE │
├────────┼──────┼─────────────────────┼───────┤
│      1 │ tag0 │ 2021-08-12 00:00:00 │ 100   │
└────────┴──────┴─────────────────────┴───────┘
a row fetched.
```

**테이블 삭제**

```sh
machbase-neo» drop table example;
executed.
```

### 하위 명령 — 실행

#### explain

Syntax `explain [--full] <sql>`

sql의 실행 계획을 보여줍니다.

```sh
machbase-neo» explain select * from example where name = 'tag.1';
 PROJECT
  TAG READ (RAW)
   KEYVALUE INDEX SCAN (_EXAMPLE_DATA_0)
    [KEY RANGE]
     * IN ()
   VOLATILE INDEX SCAN (_EXAMPLE_META)
    [KEY RANGE]
     *
```

#### export

```
  export [options] <table>
  arguments:
    table                    table name to read
  options:
    -o,--output <file>       output file (default:'-' stdout)
    -f,--format <format>     output format
                csv          csv format (default)
                json         json format
       --compress <method>   compression method [gzip] (default is not compressed)
       --[no-]heading        print header message (default:false)
       --[no-]footer         print footer message (default:false)
    -d,--delimiter           csv delimiter (default:',')
       --tz                  timezone for handling datetime
    -t,--timeformat          time format [ns|ms|s|<timeformat>] (default:'ns')
                             consult "help timeformat"
    -p,--precision <int>     set precision of float value to force round
```

#### import

```
  import [options] <table>
  arguments:
    table                 table name to write
  options:
    -i,--input <file>     input file, (default: '-' stdin)
    -f,--format <fmt>     file format [csv] (default:'csv')
       --compress <alg>   input data is compressed in <alg> (support:gzip)
       --no-header        there is no header, do not skip first line (default)
	   --charset          set character encoding, if input is not UTF-8
       --header           first line is header, skip it
       --method           write method [insert|append] (default:'insert')
       --create-table     create table if it doesn't exist (default:false)
       --truncate-table   truncate table ahead importing new data (default:false)
    -d,--delimiter        csv delimiter (default:',')
       --tz               timezone for handling datetime
    -t,--timeformat       time format [ns|ms|s|<timeformat>] (default:'ns')
                          consult "help timeformat"
       --eof <string>     specify eof line, use any string matches [a-zA-Z0-9]+ (default: '.')
```

### 하위 명령 — show

#### show info

서버 정보를 표시합니다.

```sh
machbase-neo» show info;
┌────────────────────┬─────────────────────────────┐
│ NAME               │ VALUE                       │
├────────────────────┼─────────────────────────────┤
│ build.version      │ v2.0.0                      │
│ build.hash         │ #c953293f                   │
│ build.timestamp    │ 2023-08-29T08:08:00         │
│ build.engine       │ static_standard_linux_amd64 │
│ runtime.os         │ linux                       │
│ runtime.arch       │ amd64                       │
│ runtime.pid        │ 57814                       │
│ runtime.uptime     │ 2h 30m 57s                  │
│ runtime.goroutines │ 45                          │
│ mem.sys            │ 32.6 MB                     │
│ mem.heap.sys       │ 19.0 MB                     │
│ mem.heap.alloc     │ 9.7 MB                      │
│ mem.heap.in-use    │ 13.0 MB                     │
│ mem.stack.sys      │ 1,024.0 KB                  │
│ mem.stack.in-use   │ 1,024.0 KB                  │
└────────────────────┴─────────────────────────────┘
```

#### show ports

서버의 인터페이스 포트를 표시합니다

```sh
machbase-neo» show ports;
┌─────────┬────────────────────────────────────────┐
│ SERVICE │ PORT                                   │
├─────────┼────────────────────────────────────────┤
│ http    │ tcp://127.0.0.1:5654                   │
│ mach    │ tcp://127.0.0.1:5656                   │
│ mqtt    │ tcp://127.0.0.1:5653                   │
│ shell   │ tcp://127.0.0.1:5652                   │
└─────────┴────────────────────────────────────────┘
```

#### show tables

Syntax: `show tables [-a]`

테이블 목록을 표시합니다. `-a` 플래그를 지정하면 숨겨진 테이블도 결과에 포함됩니다.

```sh
machbase-neo» show tables;
┌────────┬────────────┬──────┬─────────────┬───────────┐
│ ROWNUM │ DB         │ USER │ NAME        │ TYPE      │
├────────┼────────────┼──────┼─────────────┼───────────┤
│      1 │ MACHBASEDB │ SYS  │ EXAMPLE     │ Tag Table │
│      2 │ MACHBASEDB │ SYS  │ TAG         │ Tag Table │
│      3 │ MACHBASEDB │ SYS  │ TAGDATA     │ Tag Table │
└────────┴────────────┴──────┴─────────────┴───────────┘
```

#### show table

Syntax `show table [-a] <table>`

테이블의 컬럼 목록을 표시합니다. `-a` 플래그를 지정하면 숨겨진 컬럼도 결과에 포함됩니다.

```sh
machbase-neo» show table example -a;
┌────────┬───────┬──────────┬────────┬──────────┐
│ ROWNUM │ NAME  │ TYPE     │ LENGTH │ DESC     │
├────────┼───────┼──────────┼────────┼──────────┤
│      1 │ NAME  │ varchar  │    100 │ tag name │
│      2 │ TIME  │ datetime │     31 │ basetime │
│      3 │ VALUE │ double   │     17 │          │
│      4 │ _RID  │ long     │     20 │          │
└────────┴───────┴──────────┴────────┴──────────┘
```

#### show meta-tables

```sh
machbase-neo» show meta-tables;
┌────────┬─────────┬────────────────────────┬─────────────┐
│ ROWNUM │      ID │ NAME                   │ TYPE        │
├────────┼─────────┼────────────────────────┼─────────────┤
│      1 │ 1000020 │ M$SYS_TABLESPACES      │ Fixed Table │
│      2 │ 1000024 │ M$SYS_TABLESPACE_DISKS │ Fixed Table │
│      3 │ 1000049 │ M$SYS_TABLES           │ Fixed Table │
│      4 │ 1000051 │ M$TABLES               │ Fixed Table │
│      5 │ 1000053 │ M$SYS_COLUMNS          │ Fixed Table │
│      6 │ 1000054 │ M$COLUMNS              │ Fixed Table │
......
```

#### show virtual-tables

```sh
machbase-neo» show virtual-tables;
┌────────┬─────────┬─────────────────────────────────────────┬────────────────────┐
│ ROWNUM │      ID │ NAME                                    │ TYPE               │
├────────┼─────────┼─────────────────────────────────────────┼────────────────────┤
│      1 │      65 │ V$HOME_STAT                             │ Fixed Table (stat) │
│      2 │      93 │ V$DEMO_STAT                             │ Fixed Table (stat) │
│      3 │     227 │ V$SAMPLEBENCH_STAT                      │ Fixed Table (stat) │
│      4 │     319 │ V$TAGDATA_STAT                          │ Fixed Table (stat) │
│      5 │     382 │ V$EXAMPLE_STAT                          │ Fixed Table (stat) │
│      6 │     517 │ V$TAG_STAT                              │ Fixed Table (stat) │
......
```

#### show users

```sh
machbase-neo» show users;
┌────────┬───────────┐
│ ROWNUM │ USER_NAME │
├────────┼───────────┤
│      1 │ SYS       │
└────────┴───────────┘
a row fetched.
```

#### show license

```sh
 machbase-neo» show license;
┌────────┬──────────┬──────────────┬──────────┬────────────┬──────────────┬─────────────────────┐
│ ROWNUM │ ID       │ TYPE         │ CUSTOMER │ PROJECT    │ COUNTRY_CODE │ INSTALL_DATE        │
├────────┼──────────┼──────────────┼──────────┼────────────┼──────────────┼─────────────────────┤
│      1 │ 00000023 │ FOGUNLIMITED │ VUTECH   │ FORESTFIRE │ KR           │ 2024-04-22 15:56:14 │
└────────┴──────────┴──────────────┴──────────┴────────────┴──────────────┴─────────────────────┘
a row fetched.
```

### 하위 명령 — 세션·스키마

#### session list

Syntax: `session list`

```sh
 machbase-neo» session list;
┌────┬───────────┬─────────┬────────────┬─────────┬─────────┬──────────┐
│ ID │ USER_NAME │ USER_ID │ STMT_COUNT │ CREATED │ LAST    │ LAST SQL │
├────┼───────────┼─────────┼────────────┼─────────┼─────────┼──────────┤
│ 25 │ SYS       │ 1       │          1 │ 1.667ms │ 1.657ms │ CONNECT  │
└────┴───────────┴─────────┴────────────┴─────────┴─────────┴──────────┘
```

#### session kill

Syntax `session kill <ID>`

#### session stat

Syntax: `session stat`

```sh
machbase-neo» session stat;
┌────────────────┬───────┐
│ NAME           │ VALUE │
├────────────────┼───────┤
│ CONNS          │ 1     │
│ CONNS_USED     │ 17    │
│ STMTS          │ 0     │
│ STMTS_USED     │ 20    │
│ APPENDERS      │ 0     │
│ APPENDERS_USED │ 0     │
│ RAW_CONNS      │ 1     │
└────────────────┴───────┘
```

#### desc

Syntax `desc [-a] <table>`

테이블 구조를 설명합니다.

```sh
machbase-neo» desc example;
┌────────┬───────┬──────────┬────────┬──────────┐
│ ROWNUM │ NAME  │ TYPE     │ LENGTH │ DESC     │
├────────┼───────┼──────────┼────────┼──────────┤
│      1 │ NAME  │ varchar  │    100 │ tag name │
│      2 │ TIME  │ datetime │     31 │ basetime │
│      3 │ VALUE │ double   │     17 │          │
└────────┴───────┴──────────┴────────┴──────────┘
```

## machbase-neo restore

Syntax `machbase-neo restore --data <machbase_home_dir> <backup_dir>`

백업에서 데이터베이스를 복원합니다.

```sh
$ machbase-neo restore --data <machbase home dir>  <backup dir>
```

## machbase-neo gen-config

기본 설정 템플릿을 출력합니다.

```
$ machbase-neo gen-config ↵

define DEF {
    LISTEN_HOST       = flag("--host", "127.0.0.1")
    SHELL_PORT        = flag("--shell-port", "5652")
    MQTT_PORT         = flag("--mqtt-port", "5653")
    HTTP_PORT         = flag("--http-port", "5654")
......
```
