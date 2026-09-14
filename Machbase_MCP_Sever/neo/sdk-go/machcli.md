# Machbase CGo client

## 개요

`machcli` 패키지는 Machbase의 네이티브 C 클라이언트 라이브러리를 감싼 Go 래퍼로, Go 개발자에게 Machbase 데이터베이스에 대한 고성능 접근을 제공합니다. 내부 C 라이브러리의 성능을 활용하면서 표준 database/sql 패턴을 따르는 익숙한 Go API를 제공합니다.

### 사전 준비

- **CGo 환경**: C 라이브러리 래퍼이므로 CGo가 활성화된 Go 환경이 필요합니다
- **Machbase Neo 서버**: 실행 중인 Machbase Neo 서버 인스턴스
- **Go 1.24+**: 최적 호환을 위한 최신 Go 버전

## 시작하기

### Import

먼저 필요한 패키지를 임포트합니다. `machcli` 패키지는 Machbase C 클라이언트 라이브러리를 감싼 Go 래퍼입니다:

```go
import (
    "context"
    "fmt"
    "time"
    
    "github.com/machbase/neo-server/v8/api"
    "github.com/machbase/neo-server/v8/api/machcli"
)
```

> **주의**
> **CGo 요구사항**: `machcli`는 C 라이브러리를 감싸므로 빌드 환경이 CGo를 지원해야 합니다. 빌드 환경에서 `CGO_ENABLED=1`을 확인하세요.

### 설정

`Config` 구조체로 데이터베이스 연결 파라미터를 설정합니다. 연결 동작과 성능 특성을 조정할 수 있습니다:

```go
conf := &machcli.Config{
    Host:         "127.0.0.1",    // Machbase server host
    Port:         5656,           // Machbase server port
    MaxOpenConn:  0,              // Max Connection threshold
    MaxOpenQuery: 0,              // Max Query concurrency limit
}

// Create a database instance with the configuration
db, err := machcli.NewDatabase(conf)
if err != nil {
    panic(err)
}
```

#### 설정 Parameters

| 파라미터 | 설명 | Values |
|-----------|-------------|---------|
| `MaxOpenConn` | 최대 열린 연결 수 | `< 0`: 무제한<br>`0`: CPU 수 × 계수<br>`> 0`: 지정한 제한 |
| `MaxOpenConnFactor` | MaxOpenConn이 0일 때의 배수 | 기본값: 1.5 |
| `MaxOpenQuery` | 최대 동시 쿼리 수 | `< 0`: 무제한<br>`0`: CPU 수 × 계수<br>`> 0`: 지정한 제한 |
| `MaxOpenQueryFactor` | MaxOpenQuery가 0일 때의 배수 | 기본값: 1.5 |

> **주의**
> **성능 팁**: 높은 처리량이 필요한 애플리케이션은 시스템 자원과 예상 부하 패턴에 맞춰 제한값을 명시적으로 설정하세요.

### 연결 수립

설정한 데이터베이스 인스턴스로 Machbase 서버 연결을 만듭니다:

```go
ctx := context.Background()
conn, err := db.Connect(ctx, api.WithPassword("username", "password"))
if err != nil {
    panic(err)
}
defer conn.Close() // Always close connections when done
```

이 연결은 비밀번호 기반 인증 방식을 지원합니다:
- `api.WithPassword(user, password)`

> **주의**
> **연결 관리**: 연결이 제대로 해제되도록 항상 `defer conn.Close()`를 사용하세요.

## 데이터베이스 작업

### 단일 행 조회 (QueryRow)

결과가 정확히 한 행일 때 `QueryRow`를 사용하세요. 단일 행 조회에 최적화되어 있고 자원을 자동으로 정리합니다:

```go
var name = "tag1"
var tm time.Time
var val float64

// Execute query expecting a single row
row := conn.QueryRow(ctx, 
    `SELECT time, value FROM example_table WHERE name = ? ORDER BY TIME DESC LIMIT 1`, 
    name)

// Check for query execution errors
if err := row.Err(); err != nil {
    panic(err)
}

// Scan the result into variables
if err := row.Scan(&tm, &val); err != nil {
    panic(err)
}

// Convert to local timezone for display
tm = tm.In(time.Local)
fmt.Println("name:", name, "time:", tm, "value:", val)
```

**Key Points:**
- SQL 인젝션을 막기 위해 `?` 자리표시자를 쓰는 파라미터 쿼리를 사용하세요
- 스캔 전에 항상 `row.Err()`를 확인하세요
- `Scan()`이 데이터베이스와 Go 타입 간 변환을 자동으로 처리합니다

### 다중 행 조회 (Query)

여러 행을 가져올 때는 `Query`를 사용하세요. 순회할 수 있는 `Rows` 객체를 반환합니다:

```go
var name = "tag1"
var tm time.Time
var val float64

// Execute query that may return multiple rows
rows, err := conn.Query(ctx, 
    `SELECT time, value FROM example_table WHERE name = ? ORDER BY TIME DESC LIMIT 10`, 
    name)
if err != nil {
    panic(err)
}
defer rows.Close() // Critical: always close rows to free resources

// Iterate through all returned rows
for rows.Next() {
    if err := rows.Scan(&tm, &val); err != nil {
        panic(err)
    }
    tm = tm.In(time.Local)
    fmt.Println("name:", name, "time:", tm, "value:", val)
}
```

**중요 참고사항:**
- 자원 누수를 막기 위해 항상 `defer rows.Close()`를 사용하세요
- `rows.Next()` 반복자 패턴은 Go 개발자에게 익숙합니다

### 데이터 변경 (Exec)

INSERT, DELETE, DDL 문에는 `Exec`를 사용하세요. 실행 정보를 담은 결과 객체를 반환합니다:

```go
var name = "tag1"
var tm = time.Now()
var val = 3.14

// Execute an INSERT statement
result := conn.Exec(ctx, 
    `INSERT INTO example_table VALUES(?, ?, ?)`, 
    name, tm, val)

// Check for execution errors
if err := result.Err(); err != nil {
    panic(err)
}

// Get execution results
fmt.Println("RowsAffected:", result.RowsAffected()) 
fmt.Println("Message:", result.Message())
```

**Use Cases:**
- **INSERT**: 테이블에 새 레코드 추가
- **DELETE**: 레코드 삭제
- **DDL**: 테이블·인덱스 생성 및 변경

### 고성능 대량 입력 (Appender)

대량 데이터 입력에는 `Appender` 인터페이스를 사용하세요. 시계열 데이터 적재에 최적의 성능을 제공합니다:

```go
// IMPORTANT: Dedicate a separate connection for the Appender
// A connection with an active Appender should not be used for other operations
conn, err := db.Connect(ctx, api.WithPassword("username", "password"))
if err != nil {
    panic(err)
}
defer conn.Close()

// Create an appender for the target table
apd, err := conn.Appender(ctx, "example_table")
if err != nil {
    panic(err)
}
defer apd.Close() // Always close the appender to flush remaining data

// High-speed bulk insertion
for i := range 10_000 {
    err := apd.Append("tag1", time.Now(), 1.23*float64(i))
    if err != nil {
        panic(err)
    }
}
```

**Appender flush**

클라이언트 버퍼에 남은 데이터를 네트워크로 서버에 플러시하려면:

```go
if flusher, ok := apd.(api.Flusher); ok {
    flusher.Flush()
}
```

**Appender 권장 사항:**

> **주의**
> **연결 분리**: 활성 Appender가 있는 연결을 다른 데이터베이스 작업에 절대 쓰지 마세요. append 전용 연결을 따로 만드세요.

> **주의**
> **성능**: Appender는 시계열 워크로드를 위해 설계되었으며 적절한 배치와 함께 초당 수백만 건의 입력을 처리할 수 있습니다.

- **배치 크기**: Appender가 내부적으로 배치를 자동 처리합니다
- **오류 처리**: 중요한 애플리케이션에서는 `Append()` 호출마다 오류를 확인하세요
- **자원 정리**: 데이터가 플러시되도록 appender를 항상 `Close()`하세요

## 전체 예제

모든 개념을 보여주는 전체 예제입니다:

```go
package main

import (
    "context"
    "fmt"
    "log"
    "time"

    "github.com/machbase/neo-server/v8/api"
    "github.com/machbase/neo-server/v8/api/machcli"
)

func main() {
    // Configure database connection
    conf := &machcli.Config{
        Host: "127.0.0.1",
        Port: 5656,
        MaxOpenConn: 10,
        MaxOpenQuery: 5,
    }
    
    db, err := machcli.NewDatabase(conf)
    if err != nil {
        panic(err)
    }
    ctx := context.Background()
    
    // Connect to database
    conn, err := db.Connect(ctx, api.WithPassword("sys", "manager"))
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()
    
    // Create a sample table
    result := conn.Exec(ctx, `
        CREATE TAG TABLE IF NOT EXISTS sample_data (
            name VARCHAR(100) primary key,
            time DATETIME basetime,
            value DOUBLE
        )
    `)
    if err := result.Err(); err != nil {
        log.Fatal(err)
    }
    
    // Insert sample data
    for i := 0; i < 5; i++ {
        result := conn.Exec(ctx,
            `INSERT INTO sample_data VALUES (?, ?, ?)`,
            fmt.Sprintf("sensor_%d", i), time.Now(), float64(i)*1.5)
        if err := result.Err(); err != nil {
            log.Fatal(err)
        }
    }
    
    // Query the data
    rows, err := conn.Query(ctx, `SELECT name, time, value FROM sample_data ORDER BY time`)
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()
    
    fmt.Println("Retrieved data:")
    for rows.Next() {
        var name string
        var tm time.Time
        var value float64
        
        if err := rows.Scan(&name, &tm, &value); err != nil {
            log.Fatal(err)
        }
        tm = tm.Local()
        fmt.Printf("Name: %s, Time: %s, Value: %.2f\n", 
            name, tm.Format(time.RFC3339), value)
    }
}
```

이 예제는 연결 수립부터 데이터 조작까지 전체 흐름을 보여주며, Machbase를 다루는 Go 개발자에게 `machcli` 패키지의 강력함과 단순함을 잘 드러냅니다.
