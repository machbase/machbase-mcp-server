# Machbase SQL Driver

## Overview
The `github.com/machbase/neo-client` package provides a standard Go `database/sql` driver for Machbase Neo.
It is built on top of the native TCP client and uses the native port (default `5656`).

Use this driver when your application or framework already depends on Go's `database/sql` interfaces.
For new code that does not require `database/sql`, `machgo` is usually the better choice.

### Prerequisites

- **Machbase Neo Server**: A running server instance reachable on the native port
- **Go 1.22+**: Required by `github.com/machbase/neo-client`
- **Credentials**: A valid Machbase user account

## Getting Started

### Install

```sh
go get github.com/machbase/neo-client@latest
```

### Import

Import the driver package with a blank identifier.
The driver registers itself automatically with the name `machbase`.

```go
import (
    "context"
    "database/sql"
    "fmt"
    "strings"

    _ "github.com/machbase/neo-client"
)
```

## Connection

### DSN format

The simplest DSN uses the `server` key:

```text
server=tcp://sys:manager@127.0.0.1:5656
```

You can also combine additional options as semicolon-separated key/value pairs:

```text
server=tcp://sys:manager@127.0.0.1:5656;fetch_rows=777;statement_cache=off;io_metrics=true
```

#### Supported DSN keys

| Key | Description |
|-----|-------------|
| `server` | Server URL such as `tcp://user:password@127.0.0.1:5656` |
| `host`, `port` | Server host and port provided separately |
| `user` | Login user |
| `password` | Login password |
| `fetch_rows` | Number of rows fetched per round trip |
| `statement_cache` | Statement cache mode: `auto`, `on`, or `off` |
| `io_metrics` | Enable I/O metrics: `true` or `false` |
| `alternative_servers` | Alternate server address such as `127.0.0.2:5656` |
| `alternative_host`, `alternative_port` | Alternate server host and port provided separately |

## Query Example

```go
package main

import (
	"context"
	"database/sql"
	"fmt"
	"strings"

	_ "github.com/machbase/neo-client"
)

func main() {
	fields := []string{
		"server=tcp://sys:manager@127.0.0.1:5656",
		"fetch_rows=777",
		"statement_cache=off",
		"io_metrics=true",
	}

	db, err := sql.Open("machbase", strings.Join(fields, ";"))
	if err != nil {
		panic(err)
	}
	defer db.Close()

	ctx := context.Background()

	rows, err := db.QueryContext(ctx, `SELECT * FROM M$SYS_TABLES ORDER BY NAME`)
	if err != nil {
		panic(err)
	}
	defer rows.Close()

	columns, err := rows.Columns()
	if err != nil {
		panic(err)
	}
	fmt.Println("Columns:", columns)

	var (
		name        string
		typ         int
		dbID        int64
		id          int64
		userID      int
		columnCount int
		flag        int
	)

	for rows.Next() {
		if err := rows.Scan(&name, &typ, &dbID, &id, &userID, &columnCount, &flag); err != nil {
			panic(err)
		}
		fmt.Println(name, typ, dbID, id, userID, columnCount, flag)
	}

	if err := rows.Err(); err != nil {
		panic(err)
	}
}
```

## Insert Example

The following example inserts rows into a tag table named `EXAMPLE`.

```sql
CREATE TAG TABLE IF NOT EXISTS example (
    name VARCHAR(100) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
);
```

```go
package main

import (
	"context"
	"database/sql"
	"fmt"
	"strings"
	"time"

	_ "github.com/machbase/neo-client"
)

func main() {
	fields := []string{
		"server=tcp://sys:manager@127.0.0.1:5656",
		"fetch_rows=777",
		"statement_cache=off",
	}

	db, err := sql.Open("machbase", strings.Join(fields, ";"))
	if err != nil {
		panic(err)
	}
	defer db.Close()

	ctx := context.Background()
	ts := time.Now()

	for i := 0; i < 10; i++ {
		result, err := db.ExecContext(
			ctx,
			`INSERT INTO EXAMPLE VALUES (?, ?, ?)`,
			"example-client",
			ts.Add(time.Second*time.Duration(i)),
			3.14*float64(i),
		)
		if err != nil {
			panic(err)
		}

		affected, err := result.RowsAffected()
		if err != nil {
			panic(err)
		}
		fmt.Println("Rows affected:", affected)
	}
}
```

## Notes and Limitations

- Use positional placeholders like `?`; named parameters are not supported.
- `database/sql` connection pooling works through `sql.DB` as usual.
- Explicit transactions are not supported, so `Begin` and `BeginTx` return an error.
- `LastInsertId()` is not supported.
- Parameter type support follows the driver implementation. Common SQL types, `time.Time`, `[]byte`, and `net.IP` are supported, but `bool` parameters are not.