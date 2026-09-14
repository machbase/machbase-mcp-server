# Machbase Neo Bridge - NATS

NATS 브리지를 사용하면 machbase-neo가 NATS 서버(https://nats.io)와 메시지를 주고받을 수 있습니다.

## NATS 서버 브리지 등록

브리지 등록

```
bridge add -t nats my_nats server=nats://127.0.0.1:3000 name=client-name;
```

NATS 브리지는 machbase-neo가 외부 브로커에 어떻게 접속할지만 정의합니다. 메시지를 받으려면 아래 구독자 항목을 참고하세요.

사용 가능한 연결 옵션입니다. 자세한 내용은 NATS 공식 문서를 참고하세요.

| 옵션           | 설명                          |
| :-----------     | :---------------------------------   |
| `Server`         | 서버 주소. 접속 지점이 여러 개면 "broker" 옵션을 여러 번 사용하세요 |
| `Name`           | CONNECT 시 클라이언트를 식별하기 위해 서버로 보내는 선택적 이름 라벨입니다. |
| `NoRandomize`    | 서버 풀을 무작위로 섞을지 설정합니다. |
| `NoEcho`         | 일치하는 구독이 있을 때 이 연결로 보낸 메시지를 서버가 되돌려 보낼지 설정합니다. 서버 1.2 이상, Proto 1 이상에서 지원됩니다. |
| `Verbose`        | 서버가 정상 처리한 명령에 OK 응답을 보내도록 알립니다. |
| `Pedantic`       | 서버가 subject를 추가로 검증할지 알립니다. |
| `AllowReconnect` | 현재 서버와의 연결이 끊겼을 때 재연결 로직을 사용하도록 합니다. |
| `MaxReconnect`   | 포기하기 전까지 시도할 재연결 횟수를 설정합니다. |
| `ReconnectWait`  | 이전에 접속했던 서버로 재연결을 시도한 뒤 대기할 시간을 설정합니다. |
| `Timeout`        | 연결의 Dial 작업 타임아웃을 설정합니다. |
| `PingInterval`   | 클라이언트가 서버로 ping 명령을 보내는 주기입니다. 0 이하이면 비활성화됩니다. (예: `PingInterval=2m`) |
| `User`           | 서버 접속 시 사용할 사용자 이름을 설정합니다. |
| `Password`       | 서버 접속 시 사용할 비밀번호를 설정합니다. |
| `Token`          | 서버 접속 시 사용할 토큰을 설정합니다. |
| `RetryOnFailedConnect` | 초기 서버 목록에 접속하지 못하면 즉시 재연결 상태로 전환합니다. |
| `SkipHostLookup` | 서버 호스트명의 DNS 조회를 생략합니다. (예: `SkipHostLookup=true`) |

## 메시지 수신 - 구독자

브리지와 구독자를 활용해 NATS 서버에서 메시지를 받아 데이터베이스에 저장하는 예제를 만들어 봅시다.

### 1. NATS 서버 실행

NATS 서버를 설치해야 한다면 https://nats.io 를 참고하세요. 독립 실행 모드 설치는 간단합니다.

```sh
$ nats-server
[61052] 2021/10/28 16:53:38.003205 [INF] Starting nats-server
[61052] 2021/10/28 16:53:38.003329 [INF]   Version:  2.6.1
[61052] 2021/10/28 16:53:38.003333 [INF]   Git:      [not set]
[61052] 2021/10/28 16:53:38.003339 [INF]   Name:     NDUP6JO4T5LRUEXZUHWXMJYMG4IZAJDNWETTA4GPJ7DKXLJUXBN3UP3M
[61052] 2021/10/28 16:53:38.003342 [INF]   ID:       NDUP6JO4T5LRUEXZUHWXMJYMG4IZAJDNWETTA4GPJ7DKXLJUXBN3UP3M
[61052] 2021/10/28 16:53:38.004046 [INF] Listening for client connections on 0.0.0.0:4222
[61052] 2021/10/28 16:53:38.004683 [INF] Server is ready
...
```

### 2. NATS용 브리지 등록

machbase-neo 셸에서 `bridge add...` 명령을 실행합니다.

```
bridge add -t nats my_nats server=nats://127.0.0.1:4222 name=demo;
```

machbase-neo가 NATS 서버에 접속하는 방법을 정의합니다.

```
┌──────────┬──────────┬──────────────────────────────────────────┐
│ NAME     │ TYPE     │ CONNECTION                               │
├──────────┼──────────┼──────────────────────────────────────────┤
│ my_nats  │ nats     │ server=nats://127.0.0.1:4222 name=demo   │
└──────────┴──────────┴──────────────────────────────────────────┘
```

### 3-A. 쓰기 서술자를 사용하는 구독자

machbase-neo 셸을 열어 브리지와 데이터베이스 테이블을 잇는 새 구독자를 추가합니다.

```
subscriber add --autostart nats_subr my_nats iot.sensor db/append/EXAMPLE:csv;
```

`subscriber list`를 실행해 확인합니다.

```
┌───────────┬─────────┬────────────┬───────────────────────┬───────────┬─────────┐
│ NAME      │ BRIDGE  │ TOPIC      │ DESTINATION           │ AUTOSTART │ STATE   │
├───────────┼─────────┼────────────┼───────────────────────┼───────────┼─────────┤
│ NATS_SUBR │ my_nats │ iot.sensor │ db/append/EXAMPLE:csv │ true      │ RUNNING │
└───────────┴─────────┴────────────┴───────────────────────┴───────────┴─────────┘
```

다음을 지정합니다...
- `--autostart`는 machbase-neo와 함께 구독자를 시작합니다. 수동으로 시작·중지하려면 생략하세요.
- `nats_subr` 구독자의 이름입니다.
- `my_nats` 구독자가 사용할 브리지의 이름입니다.
- `iot.sensor` 구독할 subject 이름입니다. NATS subject 문법을 따라야 합니다.
- `db/append/EXAMPLE:csv` 쓰기 서술자입니다. 들어오는 데이터가 CSV 형식이고 `EXAMPLE` 테이블에 *append* 모드로 쓴다는 뜻입니다.

쓰기 서술자 자리에 *TQL* 스크립트 파일 경로를 대신 넣을 수 있습니다. 예제는 뒤에서 다룹니다.

쓰기 서술자의 문법은 다음과 같습니다 ...

```
db/{method}/{table_name}:{format}:{compress}?{options}
```

**method**

`append`와 `write` 두 가지 방식이 있습니다. NATS 같은 스트림 환경에서는 `append`를 권장합니다.

- `append` append 모드로 데이터를 씁니다
- `write` INSERT SQL 문으로 데이터를 씁니다

**table_name**

대상 테이블 이름을 지정합니다. 대소문자를 구분하지 않습니다.

**format**

- `json` (default)
- `csv`

**compress**

현재 `gzip`을 지원합니다. `:{compress}` 부분을 생략하면 데이터가 압축되지 않았다는 뜻입니다.

**options**

쓰기 서술자에는 물음표로 구분된 URL 인코딩 파라미터를 선택적으로 넣을 수 있습니다.

| 이름          | 기본값      | 설명                                                    |
| :------------ | :----------- | :------------------------------------------------------------- |
| `timeformat`  | `ns`         | 시간 형식: s, ms, us, ns                                     |
| `tz`          | `UTC`        | 시간대: UTC, Local, 지역 지정                        |
| `delimiter`   | `,`          | CSV 구분자. 내용이 CSV가 아니면 무시됩니다                   |
| `heading`     | `false`      | CSV에 헤더 줄이 있으면 `true`로 두어 첫 줄을 건너뜁니다 |

구독자의 대기 메시지 제한은 nats.io를 참고하세요

Examples)

- `db/append/EXAMPLE:csv?timeformat=s&heading=true`
- `db/write/EXAMPLE:csv:gzip?timeformat=s`
- `db/append/EXAMPLE:json?timeformat=2&pendingMsgLimit=1048576`

#### NATS 클라이언트 애플리케이션

NATS 서버의 `iot.sensor` subject로 여러 건의 CSV 데이터를 보내는 간단한 Go 애플리케이션을 만들어 봅시다.

```go
package main

import (
	"fmt"
	"strings"
	"time"

	"github.com/nats-io/nats.go"
)

func main() {
    // connect to the NATS server
	opts := nats.GetDefaultOptions()
	opts.Servers = []string{"nats://127.0.0.1:4222"}
	conn, err := opts.Connect()
	if err != nil {
		panic(err)
	}
	defer conn.Close()

	tick := time.Now()

    // make CSV data
    lines := []string{}
	for i := 0; i < 10; i++ {
        // NAME,TIME,VALUE
		line := fmt.Sprintf("hello-nats,%d,3.1415", tick.Add(time.Duration(i)).UnixNano())
		lines = append(lines, line)
	}
	reqData := []byte(strings.Join(lines, "\n"))

	// A) request-respond model
	if rsp, err := conn.Request("iot.sensor", reqData, 100*time.Millisecond); err != nil {
		panic(err)
	} else {
		fmt.Println("RESP:", string(rsp.Data))
	}
	// B) fire-and-forget model
	// if err := conn.Publish("iot.sensor", reqData); err != nil {
	// 	panic(err)
	// }
}
```

이 프로그램을 실행하면 NATS 서버의 `iot.sensor` subject로 CSV 10줄을 보내고, 구독자 `nats_subr`이 이를 받아 `EXAMPLE` 테이블에 씁니다.

```sh
$ go run nats_pub.go ↵
RESP: {"success":true,"reason":"10 records appended","elapse":"2.186209ms"}
```

### 3-B. TQL을 사용하는 구독자

#### 데이터 쓰기 TQL 스크립트

CSV 데이터를 받아 `example` 테이블에 쓰는 tql 스크립트를 만들어 `test.tql`로 저장합시다.

```js
CSV(payload())
MAPVALUE(1, parseTime(value(1), "ns"))
MAPVALUE(2, parseFloat(value(2)))
APPEND( table("example") )
```

machbase-neo 셸을 열어 브리지와 TQL 스크립트를 잇는 새 구독자를 추가합니다.

```
subscriber add --autostart nats_subr my_nats iot.sensor /test.tql;
```

다음을 지정합니다...
- `--autostart`는 machbase-neo와 함께 구독자를 시작합니다.
- `nats_subr` 구독자의 이름
- `my_nats` 구독자가 사용할 브리지의 이름
- `iot.sensor` 구독할 subject 이름입니다. NATS subject 문법을 지원합니다.
- `/test.tql` 들어온 데이터를 받을 tql 파일 경로입니다.

`subscriber list`를 실행해 확인합니다.

```
┌───────────┬─────────┬────────────┬─────────────┬───────────┬─────────┐
│ NAME      │ BRIDGE  │ TOPIC      │ DESTINATION │ AUTOSTART │ STATE   │
├───────────┼─────────┼────────────┼─────────────┼───────────┼─────────┤
│ NATS_SUBR │ my_nats │ test.topic │ /test.tql   │ true      │ RUNNING │
└───────────┴─────────┴────────────┴─────────────┴───────────┴─────────┘
```

#### NATS 클라이언트 애플리케이션

그리고 위 예제 코드와 같은 NATS 클라이언트 애플리케이션을 실행합니다.

#### NATS 발행자 (Go)

아래는 NATS subject로 메시지를 발행하는 완전한 Go 프로그램입니다. 요청-응답과 fire-and-forget 패턴을 모두 지원합니다.

```go
package main

import (
	"flag"
	"fmt"
	"strings"
	"time"

	"github.com/nats-io/nats.go"
)

func main() {
	optServer := flag.String("server", "nats://127.0.0.1:4222", "nats server address")
	optSubject := flag.String("subject", "hello", "subject to subscribe")
	optRequest := flag.Bool("request", false, "request-response model")
	flag.Parse()

	opts := nats.GetDefaultOptions()
	opts.Servers = []string{*optServer}
	conn, err := opts.Connect()
	if err != nil {
		panic(err)
	}
	defer conn.Close()

	tick := time.Now()
	lines := []string{}
	linesPerMsg := 1
	msgCount := 1000000
	serial := 0

	for n := 0; n < msgCount; n++ {
		for i := 0; i < linesPerMsg; i++ {
			line := fmt.Sprintf("hello-nats,%d,1.2345", tick.Add(time.Duration(serial)*time.Microsecond).UnixNano())
			lines = append(lines, line)
			serial++
		}
		reqData := []byte(strings.Join(lines, "\n"))
		lines = lines[0:0]

		if *optRequest {
			// A) request-respond model
			if rsp, err := conn.Request(*optSubject, reqData, 100*time.Millisecond); err != nil {
				panic(err)
			} else {
				fmt.Println("RESP:", string(rsp.Data))
			}
		} else {
			// B) fire-and-forget model
			if err := conn.Publish(*optSubject, reqData); err != nil {
				panic(err)
			}
		}
	}

	fmt.Println("msg sent: ", conn.OutMsgs)
}
```
