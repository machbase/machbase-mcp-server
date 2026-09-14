# Machbase SQL Driver

## 개요
`github.com/machbase/neo-client` 패키지는 Machbase Neo용 표준 Go `database/sql` 드라이버를 제공합니다.
네이티브 TCP 클라이언트 위에 구축되었으며 네이티브 포트(기본 `5656`)를 사용합니다.

애플리케이션이나 프레임워크가 이미 Go의 `database/sql` 인터페이스에 의존한다면 이 드라이버를 사용하세요.
`database/sql`이 필요 없는 새 코드라면 보통 `machgo`가 더 나은 선택입니다.

### 사전 준비

- **Machbase Neo 서버**: 네이티브 포트로 접근 가능한 실행 중인 서버 인스턴스
- **Go 1.22+**: `github.com/machbase/neo-client`가 요구합니다
- **자격 증명**: 유효한 Machbase 사용자 계정

## 시작하기

### Install

```sh
go get github.com/machbase/neo-client@latest
```

### Import

빈 식별자로 드라이버 패키지를 임포트합니다.
드라이버는 `machbase`라는 이름으로 자동 등록됩니다.

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

가장 단순한 DSN은 `server` 키를 사용합니다:

```text
server=tcp://sys:manager@127.0.0.1:5656
```

세미콜론으로 구분된 키/값 쌍으로 추가 옵션을 조합할 수도 있습니다:

```text
server=tcp://sys:manager@127.0.0.1:5656;fetch_rows=777;statement_cache=off;io_metrics=true
```

#### 지원하는 DSN 키

| 키 | 설명 |
|-----|-------------|
| `server` | `tcp://user:password@127.0.0.1:5656` 같은 서버 URL |
| `host`, `port` | 서버 호스트와 포트를 각각 지정 |
| `user` | Login user |
| `password` | 로그인 비밀번호 |
| `fetch_rows` | 한 번의 왕복으로 가져올 행 수 |
| `statement_cache` | statement 캐시 모드: `auto`, `on`, `off` |
| `io_metrics` | I/O 지표 활성화: `true` 또는 `false` |
| `alternative_servers` | `127.0.0.2:5656` 같은 대체 서버 주소 |
| `alternative_host`, `alternative_port` | 대체 서버 호스트와 포트를 각각 지정 |

## 조회 예제

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

## 입력 예제

다음 예제는 `EXAMPLE` 태그 테이블에 행을 입력합니다.

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

## 참고와 제약

- `?` 같은 위치 자리표시자를 사용하세요. 이름 있는 파라미터는 지원하지 않습니다.
- `database/sql` 커넥션 풀링은 평소처럼 `sql.DB`를 통해 동작합니다.
- 명시적 트랜잭션을 지원하지 않으므로 `Begin`과 `BeginTx`는 오류를 반환합니다.
- `LastInsertId()`는 지원하지 않습니다.
- 파라미터 타입 지원은 드라이버 구현을 따릅니다. 일반적인 SQL 타입, `time.Time`, `[]byte`, `net.IP`는 지원하지만 `bool` 파라미터는 지원하지 않습니다.
