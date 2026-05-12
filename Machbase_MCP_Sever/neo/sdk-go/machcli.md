# Machbase CGo client

## Overview

The `machcli` package is a Go wrapper around Machbase's native C client library, designed to provide Go developers with high-performance access to Machbase databases. This wrapper leverages the power and efficiency of the underlying C library while offering a familiar Go API that follows standard database/sql patterns.

### Prerequisites

- **CGo Environment**: Since this is a wrapper around a C library, you'll need a CGo-enabled Go environment
- **Machbase Neo Server**: A running Machbase Neo server instance
- **Go 1.24+**: Modern Go version for optimal compatibility

## Getting Started

### Import

First, import the necessary packages. The `machcli` package provides the Go wrapper around Machbase's C client library:

```go
import (
    "context"
    "fmt"
    "time"
    
    "github.com/machbase/neo-server/v8/api"
    "github.com/machbase/neo-server/v8/api/machcli"
)
```

{{< callout type="info" >}}
**CGo Requirement**: Since `machcli` wraps a C library, your build environment must support CGo. Ensure `CGO_ENABLED=1` in your build environment.
{{< /callout >}}

### Configuration

Configure the database connection parameters using the `Config` struct. This allows you to customize connection behavior and performance characteristics:

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

#### Configuration Parameters

| Parameter | Description | Values |
|-----------|-------------|---------|
| `MaxOpenConn` | Maximum open connections | `< 0`: unlimited<br>`0`: CPU count × factor<br>`> 0`: specified limit |
| `MaxOpenConnFactor` | Multiplier when MaxOpenConn is 0 | Default: 1.5 |
| `MaxOpenQuery` | Maximum concurrent queries | `< 0`: unlimited<br>`0`: CPU count × factor<br>`> 0`: specified limit |
| `MaxOpenQueryFactor` | Multiplier when MaxOpenQuery is 0 | Default: 1.5 |

{{< callout type="tip" >}}
**Performance Tip**: For high-throughput applications, consider setting explicit limits based on your system resources and expected load patterns.
{{< /callout >}}

### Establishing Connection

Create a connection to the Machbase server using the configured database instance:

```go
ctx := context.Background()
conn, err := db.Connect(ctx, api.WithPassword("username", "password"))
if err != nil {
    panic(err)
}
defer conn.Close() // Always close connections when done
```

The connection supports password based authentication method:
- `api.WithPassword(user, password)`

{{< callout type="warning" >}}
**Connection Management**: Always use `defer conn.Close()` to ensure connections are properly released.
{{< /callout >}}

## Database Operations

### Single Row Query (QueryRow)

Use `QueryRow` when you expect exactly one result row. This method is optimized for single-row queries and provides automatic resource cleanup:

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
- Use parameterized queries with `?` placeholders to prevent SQL injection
- Always check `row.Err()` before scanning
- `Scan()` automatically handles type conversion between database and Go types

### Multiple Row Query (Query)

Use `Query` for retrieving multiple rows. This method returns a `Rows` object that you iterate through:

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

**Important Notes:**
- Always use `defer rows.Close()` to prevent resource leaks
- The iterator pattern with `rows.Next()` is familiar to Go developers

### Data Modification (Exec)

Use `Exec` for INSERT, DELETE, and DDL statements. This method returns a result object with execution information:

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
- **INSERT**: Adding new records to tables
- **DELETE**: Removing records
- **DDL**: Creating/altering tables and indexes

### High-Performance Bulk Insert (Appender)

For high-throughput data insertion, use the `Appender` interface. This provides optimal performance for time-series data ingestion:

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

To flush remaining data from the client buffer to the server over the network:

```go
if flusher, ok := apd.(api.Flusher); ok {
    flusher.Flush()
}
```

**Appender Best Practices:**

{{< callout type="warning" >}}
**Connection Isolation**: Never use a connection with an active Appender for other database operations. Create a dedicated connection for appending.
{{< /callout >}}

{{< callout type="tip" >}}
**Performance**: Appenders are designed for time-series workloads and can achieve millions of inserts per second with proper batching.
{{< /callout >}}

- **Batch Size**: Appenders automatically handle batching internally
- **Error Handling**: Check each `Append()` call for errors in critical applications
- **Resource Cleanup**: Always `Close()` the appender to ensure data is flushed

## Complete Example

Here's a complete example demonstrating all the concepts:

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

This example demonstrates the complete workflow from connection establishment to data manipulation, showcasing the power and simplicity of the `machcli` package for Go developers working with Machbase.