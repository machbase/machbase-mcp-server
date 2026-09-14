# Go

## neo-client 개요

`neo-client`는 Machbase Neo용 Go 클라이언트 모듈입니다. v2부터는 표준 `database/sql`
드라이버를 중심으로 재구성되었으며, 이전 버전(v1)에서 제공하던 네이티브 `machgo` 패키지는
더 이상 제공되지 않습니다. v1 기반 코드는 v2와 호환되지 않으므로, `machgo.Config`나
`mdb.Connect()`를 사용하는 기존 코드는 아래 내용을 참고해 `database/sql` 기반으로
마이그레이션하십시오.

`neo-client`는 다음 패키지를 제공합니다.

- `client`(모듈 루트, import 경로 `github.com/machbase/neo-client/v2`): 표준 `database/sql`
  드라이버, `Appender`, 구조체 스캔·Named 매개변수 헬퍼
- `api`: Machbase 전용 데이터 타입과 옵션 정의
- `machnet`: `client`가 내부적으로 사용하는 저수준 프로토콜/전송 구현으로, 응용 코드에서
  직접 import할 필요는 거의 없음

### 사전 요구사항

- **Machbase 서버**: 네이티브 포트(기본 `5656`)로 접근 가능한 실행 중인 DBMS 또는 Neo 서버
- **Go 1.22 이상**
- **계정 정보**: 유효한 Machbase 사용자 계정(로컬 개발 환경에서는 `sys` / `manager` 등)

## 시작하기

### 설치

```sh
go get github.com/machbase/neo-client/v2
```

### Import

드라이버 패키지는 blank identifier로 import합니다. 드라이버 이름 `machbase`로 자동
등록되므로 별도의 `sql.Register()` 호출은 필요하지 않습니다.

```go
import (
    "context"
    "database/sql"
    "fmt"

    _ "github.com/machbase/neo-client/v2"
)
```

## 연결

### DSN 형식

`neo-client`는 다음 DSN 형식을 지원합니다.

- 서버 값만 지정: `host` 또는 `host:port`
- URL 형식: `tcp://user:password@host:port/database?as=proxy&fetch_rows=100`
- 세미콜론으로 구분한 `key=value` 목록: `key=value;key=value;...`
  (예: `user=sys;password=manager;server=127.0.0.1:5656`)

`key=value` 형식에서는 다음 규칙을 따릅니다.

- 값은 `"..."` 또는 `'...'`로 인용할 수 있습니다.
- 인용된 값 안의 `;`는 리터럴 문자로 처리됩니다.
- 인용된 값 안에서는 백슬래시 이스케이프를 사용할 수 있습니다: 큰따옴표 값의 `\"`,
  작은따옴표 값의 `\'`, `\\`
- 인용부호가 닫히지 않았거나 짝이 맞지 않으면 파싱 오류가 발생합니다.

예:

```text
user="sys as demo";password="12;34";server=127.0.0.1:5656;
password="a\"b";server=127.0.0.1:5656;
```

지원하는 DSN 키는 다음과 같습니다.

| 키 | 설명 |
|----|------|
| `server` | `tcp://user:password@127.0.0.1:5656` 형식의 서버 URL |
| `host`, `port` | 서버 호스트와 포트를 별도로 지정(기본 포트: `5656`) |
| `user`, `uid` | 로그인 사용자 |
| `password`, `pwd` | 로그인 비밀번호 |
| `database`, `db` | 초기 데이터베이스 |
| `auth_mode` | 인증 방식: `password` 또는 `challenge` |
| `auth_key_file`, `auth_key_pem` | `auth_mode=challenge`의 개인키 파일 경로 또는 인라인 PEM |
| `auth_sig_scheme` | challenge 인증 서명 스킴 |
| `fetch_rows`, `fetchrows` | 한 번의 fetch에서 가져올 최대 행 수(기본값 `1000`) |
| `statement_cache`, `statementcache` | 문장 캐시 모드: `auto`, `on`, `off`(기본값 `auto`) |
| `io_metrics`, `iometrics` | I/O 지표 활성화 여부: `true`, `false` |
| `alternative_servers` | `127.0.0.2:5656,backup.example.com:5657`처럼 콤마로 구분한 대체 서버 목록 |

`auth_key_file` 또는 `auth_key_pem`을 지정하고 `auth_mode`를 생략하면 challenge 인증으로
처리됩니다. URL 쿼리 파라미터도 같은 옵션 이름을 사용합니다.

```text
tcp://sys:manager@127.0.0.1:5656/DATABASE_A?statement_cache=on&io_metrics=true
```

알 수 없는 키는 `key=value` DSN에서는 오류이지만 URL 쿼리 문자열에서는 무시됩니다. URL
경로는 초기 데이터베이스를 함께 지정합니다(`tcp://sys:manager@127.0.0.1:5656/DATABASE_A`).
매 물리 연결마다 지정한 데이터베이스가 선택되며, 애플리케이션 코드가 직접 `USE`를 실행한
경우 해당 연결이 풀에서 재사용되기 전에 지정한 데이터베이스로 복원됩니다.

## 조회 예제

다음 예제는 표준 `database/sql` 패키지로 `M$SYS_TABLES` 시스템 테이블을 조회합니다.

```go
package main

import (
	"context"
	"database/sql"
	"fmt"

	_ "github.com/machbase/neo-client/v2"
)

func main() {
	db, err := sql.Open("machbase", "server=tcp://sys:manager@127.0.0.1:5656")
	if err != nil {
		panic(err)
	}
	defer db.Close()

	ctx := context.Background()
	rows, err := db.QueryContext(ctx, `SELECT NAME, ID, TYPE FROM M$SYS_TABLES ORDER BY NAME`)
	if err != nil {
		panic(err)
	}
	defer rows.Close()

	for rows.Next() {
		var (
			name string
			id   int64
			typ  int
		)
		if err := rows.Scan(&name, &id, &typ); err != nil {
			panic(err)
		}
		fmt.Println(name, id, typ)
	}

	if err := rows.Err(); err != nil {
		panic(err)
	}
}
```

## 테이블 생성과 입력

다음 예제는 `database/sql`로 태그 테이블을 생성하고 `ExecContext`로 행을 입력합니다.

```sql
CREATE TAG TABLE IF NOT EXISTS example (
    name VARCHAR(100) PRIMARY KEY,
	time DATETIME BASE TIME,
    value DOUBLE
);
```

```go
package main

import (
	"context"
	"database/sql"
	"fmt"
	"time"

	_ "github.com/machbase/neo-client/v2"
)

func main() {
	dsn := "server=tcp://sys:manager@127.0.0.1:5656"

	db, err := sql.Open("machbase", dsn)
	if err != nil {
		panic(err)
	}
	defer db.Close()

	ctx := context.Background()

	_, err = db.ExecContext(ctx, `CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
		NAME   VARCHAR(100)  PRIMARY KEY,
		TIME   DATETIME      BASE TIME,
		VALUE  DOUBLE
	)`)
	if err != nil {
		panic(err)
	}

	ts := time.Now()
	for i := 0; i < 10; i++ {
		rec := []any{
			"example-client",
			ts.Add(time.Duration(i) * time.Second),
			3.14 * float64(i),
		}
		result, err := db.ExecContext(ctx, `INSERT INTO EXAMPLE VALUES (?, ?, ?)`, rec...)
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

ROWID를 지원하는 Standard Edition에서 단일 `INSERT ... VALUES`가 성공하면
`Result.LastInsertId()`로 입력된 행의 ROWID를 확인할 수 있습니다. 반환 타입이 `int64`이므로
ROWID의 64비트 값을 보존하려면 `uint64`로 변환합니다. 배치, Appender, `INSERT ... SELECT`,
UPSERT에서는 ROWID를 반환하지 않습니다. 자세한 조건은
ROWID와 INSERT 결과 ID를 참고하십시오.

## 트랜잭션

Machbase는 `CREATE TABLE`로 만든 일반 테이블(TRANSACTION 테이블)에서 `BEGIN`/`COMMIT`/
`ROLLBACK`을 지원합니다. TAG/LOG 테이블은 트랜잭션을 지원하지 않으며, 트랜잭션 안에서
TAG/LOG 테이블에 DML을 실행하면 `MACHCLI-ERR-2362` 오류가 발생합니다.

표준 `database/sql` 트랜잭션 API를 그대로 사용할 수 있습니다.

```go
tx, err := db.BeginTx(ctx, nil)
if err != nil {
	panic(err)
}
if _, err := tx.ExecContext(ctx, `INSERT INTO EXAMPLE_TX VALUES (?, ?, ?)`, name, ts, value); err != nil {
	tx.Rollback()
	panic(err)
}
if err := tx.Commit(); err != nil {
	panic(err)
}
```

반복되는 준비 코드를 줄이려면 `client.Tx`/`client.TxConn` 클로저 헬퍼를 사용합니다. 함수가
`nil`을 반환하면 커밋하고, 오류를 반환하면 롤백한 뒤 그 오류를 그대로 반환하며, panic이
발생하면 롤백 후 다시 panic을 발생시킵니다.

```go
import client "github.com/machbase/neo-client/v2"

err := client.Tx(ctx, db, func(tx *sql.Tx) error {
	if _, err := tx.ExecContext(ctx, `INSERT INTO EXAMPLE_TX VALUES (?, ?, ?)`, name, ts, value); err != nil {
		return err // 자동 ROLLBACK
	}
	return nil // 자동 COMMIT
})

// TxConn은 db.Conn(ctx)로 확보한 특정 연결에서 트랜잭션을 실행합니다.
conn, _ := db.Conn(ctx)
defer conn.Close()
err = client.TxConn(ctx, conn, func(tx *sql.Tx) error {
	// ...
	return nil
})
```

클로저가 반환한 오류는 그대로 반환되므로 `errors.Is`/`errors.As`를 계속 사용할 수 있습니다.
강제로 롤백하려면 sentinel 오류를 반환하는 방식이 관용적입니다. Machbase는 트랜잭션 옵션
(isolation level, read-only)을 지원하지 않으므로 드라이버가 이를 거부합니다.

## 고성능 대량 입력 (`Appender`)

행 단위 `INSERT` 대신 대량 시계열 입력에는 `client.Appender`를 사용합니다. appender는
클라이언트에서 레코드를 버퍼링한 뒤 전용 채널로 서버에 스트리밍하므로, 개별 INSERT 문보다
훨씬 빠릅니다.

```go
import client "github.com/machbase/neo-client/v2"

appender := &client.Appender{}
// 컬럼 일부만 지정: 아래 Append()는 이 세 값만 전송하고 나머지 컬럼은 NULL로 입력됩니다.
if err := appender.Connect(ctx, dsn, "EXAMPLE", "NAME", "TIME", "VALUE"); err != nil {
	panic(err)
}
defer func() {
	successCount, failCount, err := appender.Close() // 남은 버퍼를 flush
	if err != nil {
		panic(err)
	}
	fmt.Println("Append finished. Success:", successCount, "Fail:", failCount)
}()

for _, rec := range records {
	// Connect에 전달한 컬럼과 같은 순서로 값을 하나씩 전달합니다.
	if err := appender.Append(rec.Name, rec.Time, rec.Value); err != nil {
		panic(err)
	}
}
```

핵심 사항:

- **컬럼 선택**: `Connect`(또는 `WithInputColumns`)에 전달한 컬럼 목록이 각 `Append` 호출이
  순서대로 제공해야 하는 컬럼을 정확히 결정합니다. 목록에 없는 컬럼은 NULL로 입력됩니다.
- **컬럼 목록을 생략**하면(예: `appender.Connect(ctx, dsn, "EXAMPLE")`) appender는 테이블의
  **모든** 컬럼을 대상으로 하며, 각 `Append` 호출은 `nil`을 포함해 모든 컬럼의 값을 제공해야
  합니다. 그렇지 않으면 값 개수 오류가 발생합니다.
- `Append`는 행을 버퍼링합니다. 즉시 전송하려면 `Flush()`를 호출하고, `Close()`는 flush와
  함께 세션 단위 성공/실패 건수를 반환합니다.
- 버퍼링 동작은 `WithBatchMaxRows`, `WithBatchMaxBytes`, `WithBatchMaxDelay`로 조정할 수
  있습니다.
  - `WithBatchMaxRows(rows)`: 기본값 `512`, 최소값 `1`
  - `WithBatchMaxBytes(bytes)`: 기본값 `512KB`, 최소값 `4KB`
  - `WithBatchMaxDelay(duration)`: 기본값 `5ms`, 최소값 `1ms`, `0`을 지정하면 시간 기반
    임계값을 사용하지 않음
- appender는 TAG, LOG, TRANSACTION 테이블에서 동작하지만 SQL을 우회하므로 append는 어떤
  트랜잭션에도 포함되지 않습니다.

```go
appender := &client.Appender{}
if err := appender.Connect(ctx, dsn, "EXAMPLE", "NAME", "TIME", "VALUE"); err != nil {
	panic(err)
}
defer appender.Close()

appender.
	WithBatchMaxBytes(1024 * 1024).           // 1 MB 임계값
	WithBatchMaxRows(2000).                   // row 수 임계값
	WithBatchMaxDelay(500 * time.Millisecond) // 최대 지연 임계값
```

> **주의**
> 활성 appender를 사용하는 연결에서 일반 쿼리를 함께 실행하지 마십시오.
> append 워크로드에는 별도 연결을 사용하십시오.

### ARRAY와 선택 컬럼 Append

일반 `appender.Connect(ctx, dsn, table)`에서 컬럼 인자를 생략하고 ARRAY 컬럼 값으로
`api.NewSparseArray()`가 만든 객체를 전달할 수 있습니다. 고정된 요소 선택과는 다릅니다.

```go
if err := appender.Connect(ctx, dsn, "ARRAY_APPEND_FULL_EXAMPLE"); err != nil {
    return err
}
```

`ID LONG, A INT32[4]` 테이블의 입력 순서, 희소 값 구성, 오류 시 Close와 조회 확인은
일반 Connect 예제를 참고하십시오.

```go
func appendSelected(ctx context.Context, dsn string) error {
    appender := &client.Appender{}
    if err := appender.Connect(
        ctx,
        dsn,
        "ARRAY_APPEND_EXAMPLE",
        "ID",
        "A[0]",
        "A[3]",
    ); err != nil {
        return err
    }
    if err := appender.Append(int64(1), int32(10), int32(40)); err != nil {
        _, _, _ = appender.Close()
        return err
    }
    success, failed, err := appender.Close()
    if err != nil {
        return err
    }
    if failed != 0 {
        return fmt.Errorf(
            "append result: success=%d failed=%d",
            success,
            failed,
        )
    }
    return nil
}
```

위 예제는 `context`, `fmt`와
`client "github.com/machbase/neo-client/v2"`를 import한 상태를 전제로 합니다.

행마다 다른 위치를 입력할 때는 `api.NewSparseArray()`를 사용합니다. `Array.Set()`,
`Get()`, `Entries()`와 요소 위치를 지정한 Append 대상의 위치는 0부터 시작하는 인덱스입니다.
API와 버전 제한은
Sparse ARRAY와 선택 컬럼 Append API를
참고하십시오.

## 구조체로 결과 스캔하기

컬럼 순서대로 모든 대상을 나열하는 대신, `db` 태그로 컬럼을 구조체 필드에 매핑할 수
있습니다. 헬퍼는 이미 확보한 `*sql.Rows`를 그대로 받으므로 표준 `database/sql` API와
함께 사용할 수 있습니다.

```go
import client "github.com/machbase/neo-client/v2"

type TagRecord struct {
	Name  string    `db:"NAME"`
	Time  time.Time `db:"TIME"`
	Value float64   `db:"VALUE"`

	cached string // export되지 않았거나 태그가 없는 필드는 무시됨
}

records, err := client.Select[TagRecord](ctx, db,
	`SELECT NAME, TIME, VALUE FROM EXAMPLE WHERE NAME = ? ORDER BY TIME LIMIT 100`, "sensor-1")
```

제공하는 헬퍼:

| 함수 | 용도 |
| --- | --- |
| `Select[T](ctx, q, query, args...)` | 쿼리를 실행하고 모든 행을 `[]T`로 스캔 |
| `Get[T](ctx, q, query, args...)` | 쿼리를 실행하고 첫 행을 스캔. 결과가 없으면 `sql.ErrNoRows` |
| `ScanAll[T](rows)` / `ScanOne[T](rows)` | 호출자가 이미 연 rows에 대해 동일하게 동작 |
| `ScanEach[T](rows, fn)` | 메모리 사용량을 일정하게 유지하며 한 행씩 스트리밍 |
| `NewCursor[T](rows)` | 명시적인 `Next`/`Value`/`Err` 이터레이터 |
| `ScanStruct(rows, &dest)` | `rows.Next()`를 호출하지 않고 현재 행을 스캔 |
| `ScanRow(rows, &dest)` / `ScanRows(rows, &slice)` | 제네릭을 사용하지 않는 형태 |

`T`는 구조체, 구조체 포인터, 단일 컬럼 쿼리의 스칼라, 또는 `map[string]any`일 수 있습니다.

매핑 규칙:

- 태그 키는 `db`이며, 기존 DTO를 그대로 사용할 수 있도록 `json` 태그를 대체 수단으로
  사용합니다.
- 컬럼 이름은 대소문자를 구분하지 않고 매칭되므로 `db:"id"`는 `ID` 컬럼과 매칭됩니다.
- `db:"-"`는 필드를 제외하며, **태그가 없는 필드도 제외**됩니다. 태그 없는 필드를 이름으로
  매핑하려면 `WithNameMapper(client.NameMapperIdentity())`를 호출하십시오.
- 내장 구조체는 평탄화되고, 이름이 있는 중첩 구조체는 `parent.child`로 지정합니다.
- NULL 컬럼은 `nil`이 되는 `*T` 필드로 받거나 `sql.Null[T]`로 받을 수 있습니다.

기본적으로 매핑은 엄격합니다. 매칭되는 필드가 없는 컬럼과 매칭되는 컬럼이 없는 필드는 모두
오류이며, 이는 변경된 `SELECT *`가 값을 조용히 누락시키는 것을 방지합니다. 호출별로
`WithLaxColumns()` 또는 `WithLaxFields()`로 완화할 수 있습니다.

DATETIME 컬럼을 `string`, `int64`, `time.Time` 필드로 스캔할 때는 machbase-neo HTTP API의
`timeformat`/`tz` 쿼리 파라미터와 이름을 맞춘 추가 `db` 태그 옵션을 사용할 수 있습니다.

```go
type Row struct {
	Time  string    `db:"TIME,timeformat=2006-01-02 15:04:05,tz=Local"` // 사용자 지정 레이아웃 + 표시 타임존
	Epoch int64     `db:"TIME,timeformat=ms"`                           // 밀리초 단위 epoch
	At    time.Time `db:"TIME,tz=UTC"`                                  // 필드별 타임존 재정의
}
```

- `timeformat=<Go time layout>`: `string`/`*string` 필드에서 Go time layout(또는 epoch을
  숫자 문자열로 표현하는 `ns`/`us`/`ms`/`s`)
- `timeformat=ns|us|ms|s`: `int64`/`*int64` 필드에서 epoch 단위
- `tz=<IANA name>|Local|UTC`: `string`/`time.Time` 필드(및 포인터 형태)의 타임존

이 옵션은 태그가 없어도 적용됩니다. DATETIME 컬럼에 매칭된 `string`, `int64`, `time.Time`
필드는 기본값으로 `WithDateTime(timeformat, tz)`를 사용하며, `WithDateTime`도 설정하지
않았다면 `timeformat="2006-01-02 15:04:05.999"`와 `tz="Local"`을 사용합니다. 필드 자체의
태그가 항상 `WithDateTime`보다 우선합니다.

`Select`, `ScanAll`, `ScanRows`는 결과 전체를 메모리에 적재하므로 `WithMaxRows`(기본값
1000)를 넘으면 `ErrScanTooManyRows`로 중단됩니다. `WithMaxRows(n)`으로 상향하거나
`WithMaxRows(0)`으로 제거할 수 있으며, 제한이 없는 `ScanEach`나 `NewCursor`로 스트리밍할
수도 있습니다.

```go
rows, err := db.QueryContext(ctx, `SELECT NAME, TIME, VALUE FROM EXAMPLE`)
if err != nil {
	panic(err)
}
defer rows.Close() // 헬퍼는 전달받은 rows를 닫지 않음

var total float64
err = client.ScanEach(rows, func(rec TagRecord) error {
	total += rec.Value
	return nil
})
```

## Named 매개변수

`NamedArgs`는 구조체 또는 `map[string]any`를 같은 `db` 태그를 사용해 `sql.Named` 인자로
변환합니다. SQL 텍스트를 검사하거나 재작성하지 않으며, `:name` 자리표시자는 서버가 직접
해석합니다.

```go
type condition struct {
	Name string    `db:"name"`
	From time.Time `db:"from"`
	To   time.Time `db:"to"`
}

args, err := client.NamedArgs(condition{Name: "sensor-1", From: begin, To: end})
if err != nil {
	panic(err)
}

records, err := client.Select[TagRecord](ctx, db, `
	SELECT NAME, TIME, VALUE FROM EXAMPLE
	 WHERE NAME = :name AND TIME BETWEEN :from AND :to`, args...)
```

Named 매개변수는 파라미터 이름 메타데이터를 보고하는 서버(Machbase v8.7.0 이상)가
필요합니다. `client.SupportsNamedParameters(ctx, db)`로 확인하고, 지원하지 않으면 쿼리는
`client.ErrNamedParamsUnsupported`로 실패하므로 위치 기반 `?` 자리표시자를 사용해야
합니다. 일반 SQL 기능과 SDK별 차이는
Named Bind Parameter syntax를
참고하십시오.

## Machbase 8.7: DECIMAL과 Named 매개변수

Machbase 8.7은 정확한 DECIMAL 값, nullable 컬럼 정보, named 매개변수를 제공합니다.

```go
import "database/sql"
import client "github.com/machbase/neo-client/v2"

amount, err := client.ParseDecimal("1234567890.125", 30, 3)
if err != nil {
	panic(err)
}
result, err := conn.ExecContext(ctx,
	"INSERT INTO payments(id, amount) VALUES (:id, :amount)",
	sql.Named("id", int32(1)),
	sql.Named("amount", amount),
)
if err != nil {
	panic(err)
}
```

`database/sql` 드라이버는 `sql.Named`를 받아들이고 DECIMAL 조회 값을 정확한 문자열로
반환합니다. 파라미터 이름은 대소문자를 구분하지 않고 매칭되며, 반복된 자리표시자에는 한 번
전달한 값이 적용되고, named 인자와 positional 인자를 섞을 수 없습니다. `client.NamedArgs`는
구조체 또는 map으로부터 `sql.Named` 목록을 만듭니다.

Machbase 8.5.x에 연결한 경우에는 해당 서버 버전이 지원하는 테이블·데이터 타입과 함께 위치
기반 `?` 매개변수를 사용하십시오. Named 매개변수와 Machbase 8.7 데이터 타입은 사용할 수
없으며, nullable 컬럼 정보를 알 수 없는 경우(`ColumnType.Nullable()`이 `ok=false` 반환)가
있을 수 있습니다.

### Prepared statement와 statement cache

`db.PrepareContext`로 만든 문장은 여러 번 실행할 수 있습니다. 드라이버의 문장 캐시는
연결별로 동작하며, `statement_cache=auto|on|off` DSN 키로 설정합니다. 테이블을 삭제 후 다시
만들었거나 결과 컬럼 타입이 변경된 경우 캐시된 메타데이터가 갱신되도록 문장을 다시 준비합니다.
`USE`로 세션 데이터베이스를 변경한 뒤에도 기존 준비된 문장이나 커서를 다른 데이터베이스의
작업에 재사용하지 말고 새로 준비하거나 열어야 합니다.

## 포함된 예제 실행

실행 가능한 예제는 neo-client 저장소의 `_example/` 아래에 포함되어 있습니다.

```sh
go run ./_example/query.go -s 127.0.0.1:5656 -u sys -p manager
go run ./_example/append.go -s 127.0.0.1:5656 -u sys -p manager
go run ./_example/insert.go -s 127.0.0.1:5656 -u sys -p manager
go run ./_example/scanbytag.go -s 127.0.0.1:5656 -u sys -p manager
```

## 참고 사항 및 제한 사항

- 위치 기반 placeholder와 이름 기반 placeholder를 모두 사용할 수 있지만, 한 문장 안에서 두
  방식을 섞을 수 없습니다. 이름 기반 API는 `sql.Named()`를 사용합니다. 공통 SQL 기능과
  SDK별 차이는
  Named Bind Parameter syntax를
  참고하십시오.
- `database/sql`의 연결 풀은 일반적인 `sql.DB` 방식대로 동작합니다. DSN에 `database`/`db`를
  지정하면 매 물리 연결마다 지정한 데이터베이스를 선택하며, 애플리케이션 코드가 직접 `USE`를
  실행한 세션은 풀에 반환되기 전에 설정된 데이터베이스로 복원됩니다.
- ROWID를 지원하는 Standard Edition에서는 단일 INSERT 결과에서 `Result.LastInsertId()`를
  호출할 수 있습니다. 반환된 `int64`는 `uint64`로 변환해 ROWID의 bit pattern을 보존합니다.
  자세한 내용은 ROWID와 INSERT 결과 ID를 참고하십시오.
- 사용을 마친 `Rows`, `Stmt`, `sql.Conn`, `sql.DB`는 항상 닫으십시오. 구조체 스캔 헬퍼는
  전달받은 rows를 닫지 않습니다.
- `Appender.Close()`는 append 세션의 성공/실패 건수를 반환합니다.
- 파라미터 타입은 드라이버 구현을 따릅니다. 일반적인 SQL 타입, `time.Time`, `[]byte`,
  `net.IP`, `api.Decimal`을 지원하지만 `bool` 파라미터는 지원하지 않습니다.
