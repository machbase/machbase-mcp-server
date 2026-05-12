# Machbase gRPC Client

## Overview

The `machrpc` package provides a standard Go database interface for connecting to and interacting with machbase-neo servers. Built on gRPC, it offers high-performance connectivity while maintaining compatibility with Go's `database/sql` package conventions.
For a standard Go `database/sql` interface, please refer to the **SQL driver** section.

## Installation

To use the machbase-neo SQL driver in your Go project, install the package:

```sh
go get github.com/machbase/neo-server/v8
```

## TLS Configuration

Since the machbase-neo SQL driver is based on gRPC, **TLS certificates are required** for secure communication between client and server. You need to prepare the following certificate files:

- **Server Certificate** (`server-cert.pem`): The server's public certificate
- **Client Certificate** (`client-cert.pem`): The client's public certificate  
- **Client Key** (`client-key.pem`): The client's private key

### Generating Certificates

Please see the [API Security](/neo/security/) guide for step‑by‑step instructions to generate the TLS certificates required by the driver — `server-cert.pem`, `client-cert.pem`, and `client-key.pem`. The guide explains creating a CA, signing certificates.

## Basic Usage

### Establishing a Connection

```go {linenos=table,hl_lines=["20-27",31,35,39]}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/machbase/neo-server/v8/api"
	"github.com/machbase/neo-server/v8/api/machrpc"
)

func main() {
	// Configure server address and TLS certificates
	serverAddr := "127.0.0.1:5655"
	serverCert := "/path/to/server-cert.pem"
	clientKey := "/path/to/client-key.pem"
	clientCert := "/path/to/client-cert.pem"

	// Create a new gRPC client
	cli, err := machrpc.NewClient(&machrpc.Config{
		ServerAddr: serverAddr,
		Tls: &machrpc.TlsConfig{
			ClientKey:  clientKey,
			ClientCert: clientCert,
			ServerCert: serverCert,
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	defer cli.Close()

	// Connect with authentication
	ctx := context.Background()
	conn, err := cli.Connect(ctx, api.WithPassword("sys", "manager"))
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	fmt.Println("Successfully connected to machbase-neo")
}
```

### Configuration Options

The `machrpc.Config` struct accepts the following options:

| Field | Type | Description |
|-------|------|-------------|
| `ServerAddr` | string | Server address in `host:port` format (default: `127.0.0.1:5655`) |
| `Tls` | *TlsConfig | TLS configuration for secure communication |

The `machrpc.TlsConfig` struct:

| Field | Type | Description |
|-------|------|-------------|
| `ServerCert` | string | Path to server certificate file |
| `ClientCert` | string | Path to client certificate file |
| `ClientKey` | string | Path to client private key file |

## Querying Data

### Simple SELECT Query

```go {linenos=table,hl_lines=[41,45,48,53]}
package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/machbase/neo-server/v8/api"
	"github.com/machbase/neo-server/v8/api/machrpc"
)

func main() {
	serverAddr := "127.0.0.1:5655"
	serverCert := "/path/to/server-cert.pem"
	clientKey := "/path/to/client-key.pem"
	clientCert := "/path/to/client-cert.pem"

	cli, err := machrpc.NewClient(&machrpc.Config{
		ServerAddr: serverAddr,
		Tls: &machrpc.TlsConfig{
			ClientKey:  clientKey,
			ClientCert: clientCert,
			ServerCert: serverCert,
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	defer cli.Close()

	ctx := context.Background()
	conn, err := cli.Connect(ctx, api.WithPassword("sys", "manager"))
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	// Execute query with parameters
	sqlText := `SELECT name, time, value FROM example LIMIT ?`
	rows, err := conn.Query(ctx, sqlText, 3)
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()

	// Iterate through results
	for rows.Next() {
		var name string
		var ts time.Time
		var value float64
		
		err = rows.Scan(&name, &ts, &value)
		if err != nil {
			log.Fatal(err)
		}
		
		fmt.Printf("Name: %s, Time: %s, Value: %.2f\n", 
			name, ts.Format(time.RFC3339), value)
	}

	// Check for errors during iteration
	if err = rows.Err(); err != nil {
		log.Fatal(err)
	}
}
```

### Parameterized Queries

Always use parameterized queries to prevent SQL injection:

```go {linenos=table}
// Good: Using parameters
rows, err := conn.Query(ctx, 
	"SELECT * FROM sensors WHERE name = ? AND time > ?", 
	"sensor1", startTime)

// Bad: String concatenation (vulnerable to SQL injection)
// rows, err := conn.Query(ctx, 
//     fmt.Sprintf("SELECT * FROM sensors WHERE name = '%s'", userInput))
```

## Executing Commands

### INSERT Statement

```go {linenos=table}
func insertData(conn api.Conn) error {
	ctx := context.Background()

	sqlText := `INSERT INTO example (name, time, value) VALUES (?, ?, ?)`
	result := conn.Exec(ctx, sqlText, "sensor1", time.Now(), 123.45)
	if err := result.Err(); err != nil {
		return err
	}
	rowsAffected := result.RowsAffected()
	fmt.Printf("Inserted %d row(s)\n", rowsAffected)

	return nil
}
```

### DELETE Statement

```go {linenos=table}
func deleteData(conn api.Conn) error {
	ctx := context.Background()

	sqlText := `DELETE FROM example WHERE name = ?`
	result := conn.Exec(ctx, sqlText, "sensor1")
	if err := result.Err(); err != nil {
		return err
	}

	rowsAffected := result.RowsAffected()
	fmt.Printf("Deleted %d row(s)\n", rowsAffected)

	return nil
}
```

## High-Performance Bulk Insert (Appender)

For high-throughput data insertion, use the `Appender` interface. This provides optimal performance for time-series data ingestion:

```go
// IMPORTANT: Dedicate a separate connection for the Appender
// A connection with an active Appender should not be used for other operations

apd, err := conn.Appender(ctx, "example")
if err != nil {
	panic(err)
}
defer apd.Close() // Always close the appender to flush remaining data

// High-speed bulk insertion
for i := range 10_000 {
	err := apd.Append("grpc", time.Now(), 1.23*float64(i))
	if err != nil {
		panic(err)
	}
}
```

{{< callout type="warning" >}}
**Connection Isolation**: Never use a connection with an active Appender for other database operations. Create a dedicated connection for appending.
{{< /callout >}}

{{< callout type="tip" >}}
**Performance**: Appenders are designed for time-series workloads and can achieve million of inserts per second with proper batching.
{{< /callout >}}

## Best Practices

**1. Always Use Context**

Pass context to all operations for proper timeout and cancellation handling:

```go
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

rows, err := conn.Query(ctx, "SELECT * FROM large_table")
```

**2. Close Resources**

Always close connections, statements, and result sets:

```go
defer cli.Close()
defer conn.Close()
defer rows.Close()
```

**3. Handle Errors Appropriately**

Don't ignore errors; wrap them with context for better debugging:

```go
if err != nil {
	return fmt.Errorf("failed to query sensor data: %w", err)
}
```

**4. Use Connection Pooling in Production**

Reuse connections to reduce overhead and improve performance.

```go {linenos=table}
type ConnectionPool struct {
	mu      sync.Mutex
	client  *machrpc.Client
	maxSize int
	conns   []api.Conn
	config  *machrpc.Config
}

func NewConnectionPool(config *machrpc.Config, maxSize int) *ConnectionPool {
	return &ConnectionPool{
		conns:   make([]api.Conn, 0, maxSize),
		config:  config,
		maxSize: maxSize,
	}
}

func (p *ConnectionPool) Close() {
	p.mu.Lock()
	defer p.mu.Unlock()
	for _, conn := range p.conns {
		conn.Close()
	}
	p.client.Close()
}

func (p *ConnectionPool) GetConnection(ctx context.Context) (api.Conn, error) {
	p.mu.Lock()
	defer p.mu.Unlock()

	if len(p.conns) > 0 {
		conn := p.conns[len(p.conns)-1]
		p.conns = p.conns[:len(p.conns)-1]
		return conn, nil
	}

	if p.client == nil {
		cli, err := machrpc.NewClient(p.config)
		if err != nil {
			return nil, err
		}
		p.client = cli
	}

	conn, err := p.client.Connect(ctx, api.WithPassword("sys", "manager"))
	if err != nil {
		return nil, err
	}

	return conn, nil
}

func (p *ConnectionPool) ReleaseConnection(conn api.Conn) {
	p.mu.Lock()
	defer p.mu.Unlock()

	if len(p.conns) < p.maxSize {
		p.conns = append(p.conns, conn)
	} else {
		conn.Close()
	}
}
```

## Complete Example

Here's a complete example demonstrating various operations:

```go {linenos=table}
package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/machbase/neo-server/v8/api"
	"github.com/machbase/neo-server/v8/api/machrpc"
)

func main() {
	serverAddr := "192.168.1.165:5655"
	serverCert := "./server.pem"
	clientKey := "./client_key.pem"
	clientCert := "./client_cert.pem"

	cli, err := machrpc.NewClient(&machrpc.Config{
		ServerAddr: serverAddr,
		Tls: &machrpc.TlsConfig{
			ClientKey:  clientKey,
			ClientCert: clientCert,
			ServerCert: serverCert,
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	defer cli.Close()

	ctx := context.Background()
	conn, err := cli.Connect(ctx, api.WithPassword("sys", "manager"))
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	// Create table
	result := conn.Exec(ctx, `
		CREATE TAG TABLE IF NOT EXISTS example (
			name VARCHAR(20) PRIMARY KEY,
			time DATETIME BASETIME,
			value DOUBLE SUMMARIZED
		)
	`)
	if err := result.Err(); err != nil {
		log.Fatal(err)
	}

	// Insert data
	for i := 0; i < 5; i++ {
		result = conn.Exec(ctx,
			`INSERT INTO example (name, time, value) VALUES (?, ?, ?)`,
			fmt.Sprintf("sensor%d", i),
			time.Now().Add(time.Duration(i)*time.Second),
			float64(i)*10.5)
		if err := result.Err(); err != nil {
			log.Fatal(err)
		}
	}

	// Query data
	sqlText := `SELECT name, time, value FROM example LIMIT ?`
	rows, err := conn.Query(ctx, sqlText, 3)
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()

	fmt.Println("Query Results:")
	for rows.Next() {
		var name string
		var ts time.Time
		var value float64

		err = rows.Scan(&name, &ts, &value)
		if err != nil {
			log.Fatal(err)
		}

		fmt.Printf("Name: %s, Time: %s, Value: %.2f\n",
			name, ts.Format(time.RFC3339), value)
	}

	if err = rows.Err(); err != nil {
		log.Fatal(err)
	}
}
```

## Troubleshooting

### Common Issues

**Connection Refused**
- Verify the server is running and accessible
- Check the server address and port
- Ensure firewall rules allow the connection

**TLS Certificate Errors**
- Verify certificate file paths are correct
- Ensure certificates are valid and not expired
- Check file permissions on certificate files

**Authentication Failed**
- Verify username and password are correct
- Check user permissions in machbase-neo

**Query Timeout**
- Increase context timeout for long-running queries
- Optimize query performance with appropriate indexes
- Consider pagination for large result sets