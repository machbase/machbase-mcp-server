# Machbase Go Client

## 개요

`machgo` 패키지는 Machbase 네이티브 프로토콜 접근을 위한 순수 Go 클라이언트입니다.
`machcli`와 같은 API 스타일을 제공하지만 CGo에 의존하지 않습니다.
순수 Go 툴체인으로 네이티브 포트 성능이 필요하다면 `machgo`가 좋은 선택입니다.

### machgo를 쓰는 이유

- **CGo 의존성 없음**: 순수 Go 환경으로 빌드·배포
- **네이티브 프로토콜 접근**: Machbase 네이티브 포트(기본 `5656`)로 접속
- **machcli와 API 호환**: 동일한 연결/조회/appender 패턴을 그대로 사용
- **운영 친화적**: 컨테이너·크로스 플랫폼 Go 배포에 적합

### 사전 준비

- **Machbase Neo 서버**: 실행 중인 Machbase Neo 서버 인스턴스
- **Go 1.22+**: 최신 Go 버전 권장
- **네트워크 접근**: 접근 가능한 네이티브 포트(기본 `5656`)

## 시작하기

### Install

```sh
go get github.com/machbase/neo-client@latest
```

### Import

API 패키지와 `machgo` 클라이언트 패키지를 임포트합니다:

```go
import (
    "context"
    "fmt"
    "time"

    "github.com/machbase/neo-client/api"
    "github.com/machbase/neo-client/machgo"
)
```

### 설정

`machgo.Config`로 호스트/포트와 동시성 옵션을 설정합니다:

```go
conf := &machgo.Config{
    Host:         "127.0.0.1", // Machbase server host
    Port:         5656,          // Machbase native port
    MaxOpenConn:  0,             // Max Connection threshold
    MaxOpenQuery: 0,             // Max Query concurrency limit
}

// Create a database instance
// API usage is the same as machcli
mdb, err := machgo.NewDatabase(conf)
if err != nil {
    panic(err)
}
```

#### 설정 Parameters

| 파라미터 | 설명 | Values |
|-----------|-------------|--------|
| `MaxOpenConn` | 최대 열린 연결 수 | `< 0`: 무제한<br>`0`: CPU 수 × 계수<br>`> 0`: 지정한 제한 |
| `MaxOpenConnFactor` | MaxOpenConn이 0일 때의 배수 | 기본값: 1.5 |
| `MaxOpenQuery` | 최대 동시 쿼리 수 | `< 0`: 무제한<br>`0`: CPU 수 × 계수<br>`> 0`: 지정한 제한 |
| `MaxOpenQueryFactor` | MaxOpenQuery가 0일 때의 배수 | 기본값: 1.5 |

#### FlowControl 동작

`MaxOpenConn`과 `MaxOpenQuery`는 흐름 제어 제한값입니다.
값을 `-1`로 설정하면 해당 제한이 비활성화됩니다(그 차원에는 FlowControl이 적용되지 않음).

```go
conf := &machgo.Config{
    Host:         "127.0.0.1",
    Port:         5656,
    MaxOpenConn:  -1, // disable connection FlowControl
    MaxOpenQuery: -1, // disable query FlowControl
}
```

### 연결 수립

```go
ctx := context.Background()
conn, err := mdb.Connect(ctx, api.WithPassword("sys", "manager"))
if err != nil {
    panic(err)
}
defer conn.Close()
```

인증 옵션:

- `api.WithPassword(user, password)`

### 연결 수준 튜닝 옵션

`machgo`는 `Connect()` 시점에 연결별 재정의를 지원합니다.
이렇게 하면 전역 기본값은 `machgo.Config`에 두고 연결마다 다르게 조정할 수 있습니다.

#### 반복 SQL을 위한 StatementCache

하나의 연결 수명 동안 같은 SQL을 반복해서 쓴다면,
prepared statement를 재사용해 성능을 높일 수 있습니다.

`machgo.Config.StatementCache`에 기본 모드를 설정하고 연결별로 `api.WithStatementCache(...)`로 재정의할 수 있습니다.

```go {linenos=table,linenostart=1,hl_lines=[5,16]}
// Connection A: aggressive statement reuse
connA, err := mdb.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithStatementCache(api.StatementCacheAuto),
)
if err != nil {
    panic(err)
}
defer connA.Close()

// Connection B: disable statement reuse for this connection only
connB, err := mdb.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithStatementCache(api.StatementCacheOff),
)
if err != nil {
    panic(err)
}
defer connB.Close()
```

#### FetchRows 선반입 크기

`FetchRows`는 한 번의 fetch에서 서버로부터 미리 가져올 최대 레코드 수를 제어합니다.
`machgo.Config.FetchRows`를 기본값으로 설정하고, 연결별로 `api.WithFetchRows(...)`로 재정의합니다.
기본값은 `1000`입니다.

> **주의**
> 워크로드 검증 없이 `FetchRows`를 지나치게 크거나 작게 설정하지 마세요.
> 네트워크 지연과 쿼리 특성에 따라 부적절한 값은 심각한 성능 저하와 메모리 소비 증가를 유발할 수 있습니다.

```go {linenos=table,linenostart=1,hl_lines=[5]}
// Connection C: larger pre-fetch for scan-heavy workloads
connC, err := mdb.Connect(
    ctx,
    api.WithPassword("sys", "manager"),
    api.WithFetchRows(5000),
)
if err != nil {
    panic(err)
}
defer connC.Close()
```

> **주의**
> 자원을 해제하려면 연결에 항상 `Close()`를 호출하세요.

## 데이터베이스 작업

### 단일 행 조회 (`QueryRow`)

정확히 한 행이 예상될 때 `QueryRow`를 사용하세요.

```go
var name = "tag1"
var tm time.Time
var val float64

row := conn.QueryRow(
    ctx,
    `SELECT time, value FROM example_table WHERE name = ? ORDER BY time DESC LIMIT 1`,
    name,
)
if err := row.Err(); err != nil {
    panic(err)
}
if err := row.Scan(&tm, &val); err != nil {
    panic(err)
}

fmt.Println("name:", name, "time:", tm.Local(), "value:", val)
```

### 다중 행 조회 (`Query`)

여러 행 결과에는 `Query`를 사용하세요.

```go
rows, err := conn.Query(
    ctx,
    `SELECT time, value FROM example_table WHERE name = ? ORDER BY time DESC LIMIT 10`,
    "tag1",
)
if err != nil {
    panic(err)
}
defer rows.Close()

for rows.Next() {
    var tm time.Time
    var val float64

    if err := rows.Scan(&tm, &val); err != nil {
        panic(err)
    }
    fmt.Println("time:", tm.Local(), "value:", val)
}
```

### 데이터 변경 (`Exec`)

INSERT, DELETE, DDL 문에는 `Exec`를 사용하세요.

```go
result := conn.Exec(
    ctx,
    `INSERT INTO example_table VALUES(?, ?, ?)`,
    "tag1", time.Now(), 3.14,
)
if err := result.Err(); err != nil {
    panic(err)
}

fmt.Println("RowsAffected:", result.RowsAffected())
fmt.Println("Message:", result.Message())
```

## 고성능 대량 입력 (`Appender`)

대량 적재에는 전용 연결과 함께 `Appender`를 사용하세요.

```go
apd, err := conn.Appender(ctx, "example_table")
if err != nil {
    panic(err)
}
defer apd.Close()

for i := range 10_000 {
    if err := apd.Append("tag1", time.Now(), float64(i)); err != nil {
        panic(err)
    }
}
```

서버로 보내는 클라이언트 측 전송 버퍼 임계값을 다음으로 조정할 수 있습니다:

appender는 `Append()` 호출의 데이터를 내부 버퍼에 쌓아두었다가 설정된 임계값에 도달했을 때만 서버로 보냅니다.
바이트 크기, 행 수, 지연(버퍼의 가장 오래된 레코드와 가장 새로운 레코드의 시간 차)으로 임계값을 설정할 수 있습니다.
이 임계값 중 하나라도 넘으면 버퍼의 데이터가 서버로 전송됩니다.

- `WithBatchMaxRows(rows)` : 기본값 `512`, 최소 `1`
- `WithBatchMaxBytes(bytes)`: 기본값 `512KB`, 최소 `4KB`
- `WithBatchMaxDelay(duration)` : 기본값 `5ms`, 최소 `1ms`
- `WithBatchMaxDelay(0)`은 시간 기반 임계값을 비활성화합니다

```go
apd, err := conn.Appender(ctx, "example_table")
if err != nil {
    panic(err)
}
defer apd.Close()

apd.WithBatchMaxBytes(1024 * 1024).    // 1 MB threshold
    WithBatchMaxRows(2000).            // row-count threshold
    WithBatchMaxDelay(500 * time.Millisecond) // max delay threshold
```

Appender flush 예제:

`Flush()`는 프로그램에서 직접 호출하는 플러시 메서드입니다.
임계값 기반 자동 플러시와 달리, 설정된 바이트/행/지연 임계값과 무관하게 버퍼의 레코드를 즉시 전송합니다.

```go
if flusher, ok := apd.(api.Flusher); ok {
    flusher.Flush()
}
```

> **주의**
> 활성 appender를 보유한 연결에서는 일반 쿼리를 실행하지 마세요.
> append 작업에는 별도의 연결을 사용하세요.

## 전체 예제

```go
package main

import (
    "context"
    "fmt"
    "log"
    "time"

    "github.com/machbase/neo-client/api"
    "github.com/machbase/neo-client/machgo"
)

func main() {
    conf := &machgo.Config{
        Host:         "127.0.0.1",
        Port:         5656,
        MaxOpenConn:  -1,
        MaxOpenQuery: -1,
    }

    mdb, err := machgo.NewDatabase(conf)
    if err != nil {
        log.Fatal(err)
    }

    ctx := context.Background()
    conn, err := mdb.Connect(ctx, api.WithPassword("sys", "manager"))
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()

    result := conn.Exec(ctx, `
        CREATE TAG TABLE IF NOT EXISTS sample_data (
            name VARCHAR(100) PRIMARY KEY,
            time DATETIME BASETIME,
            value DOUBLE
        )
    `)
    if err := result.Err(); err != nil {
        log.Fatal(err)
    }

    for i := 0; i < 5; i++ {
        result := conn.Exec(
            ctx,
            `INSERT INTO sample_data VALUES (?, ?, ?)`,
            fmt.Sprintf("sensor_%d", i),
            time.Now(),
            float64(i)*1.5,
        )
        if err := result.Err(); err != nil {
            log.Fatal(err)
        }
    }

    rows, err := conn.Query(ctx, 
        `SELECT name, time, value FROM sample_data ORDER BY time`)
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()

    for rows.Next() {
        var name string
        var tm time.Time
        var value float64

        if err := rows.Scan(&name, &tm, &value); err != nil {
            log.Fatal(err)
        }
        fmt.Printf("Name: %s, Time: %s, Value: %.2f\n", 
            name, tm.Local().Format(time.RFC3339), value)
    }
}
```

이 작업 흐름은 기존 코드를 최소한의 변경으로 이전할 수 있도록 의도적으로 `machcli`와 동일하게 설계되었습니다.
