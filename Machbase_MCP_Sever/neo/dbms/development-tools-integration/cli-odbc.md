# Machbase SQLCLI와 ODBC

Machbase SQLCLI는 C/C++ 애플리케이션에서 사용하는 함수 호출 인터페이스(Call-Level
Interface)입니다. ODBC 드라이버는 표준 ODBC 애플리케이션에서 사용합니다. 두 인터페이스는
환경·연결·문장 핸들을 사용하는 실행 흐름을 공유하며, SQLCLI에는 고속 Append를
위한 확장 함수가 추가되어 있습니다.

## 선택 기준

| 요구사항 | 인터페이스 |
|----------|------------|
| Machbase 설치 패키지와 함께 C/C++ 애플리케이션 개발 | SQLCLI |
| 범용 ODBC 도구 또는 드라이버 관리자 사용 | ODBC |
| Append 확장 API로 대량 입력 | SQLCLI |
| 표준 SQL 실행과 결과 조회 | SQLCLI 또는 ODBC |

## 헤더와 라이브러리

설치 디렉터리에서 다음 파일을 확인합니다.

```bash
test -f "$MACHBASE_HOME/include/machbase_sqlcli.h"
test -f "$MACHBASE_HOME/lib/libmachbasecli_dll.so"
```

Linux 동적 링크 예시는 다음과 같습니다.

```bash
gcc cli_quickstart.c   -I"$MACHBASE_HOME/include"   -L"$MACHBASE_HOME/lib"   -lmachbasecli_dll   -o cli_quickstart

LD_LIBRARY_PATH="$MACHBASE_HOME/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"   MACHBASE_PASSWORD='your-password' ./cli_quickstart
```

운영 빌드는 설치 패키지의 `install/machbase_env.mk`와 플랫폼별 링커 설정을 기준으로
구성합니다.

## 연결 문자열

SQLCLI에서 기본 연결 문자열은 다음 키를 사용합니다.

```text
SERVER=127.0.0.1;PORT_NO=5656;UID=APP_USER;PWD=secret;CONNTYPE=1
```

ODBC 데이터 소스를 사용한다면 DSN, 계정, 비밀번호를 지정합니다.

```text
DSN=MACHBASE;UID=APP_USER;PWD=secret
```

다중 데이터베이스 초기값을 지원하는 드라이버에서는 `DATABASE` 또는 `DBNAME`을 사용할 수
있습니다. 실제 배포 드라이버의 지원 여부를 확인하고, 연결 후
`SELECT CURRENT_DATABASE()`로 선택 결과를 검증합니다.

## 빠른 시작

다음 프로그램은 5656 포트에 연결해 시스템 테이블 조회를 실행한 뒤 모든 핸들을
해제합니다. 비밀번호는 환경 변수로 전달합니다.

```c
#include <stdio.h>
#include <stdlib.h>
#include <machbase_sqlcli.h>

int main(void)
{
    SQLHENV env = SQL_NULL_HENV;
    SQLHDBC dbc = SQL_NULL_HDBC;
    SQLHSTMT stmt = SQL_NULL_HSTMT;
    char conn[512];
    const char *password = getenv("MACHBASE_PASSWORD");

    if (password == NULL) {
        fputs("MACHBASE_PASSWORD is required\n", stderr);
        return 2;
    }

    snprintf(conn, sizeof(conn),
        "SERVER=127.0.0.1;PORT_NO=5656;"
        "UID=SYS;PWD=%s;CONNTYPE=1", password);

    if (SQLAllocEnv(&env) != SQL_SUCCESS) {
        return 3;
    }
    if (SQLAllocConnect(env, &dbc) != SQL_SUCCESS) {
        SQLFreeEnv(env);
        return 4;
    }
    if (SQLDriverConnect(
            dbc, NULL, (SQLCHAR *)conn, SQL_NTS,
            NULL, 0, NULL, SQL_DRIVER_NOPROMPT) != SQL_SUCCESS) {
        SQLFreeConnect(dbc);
        SQLFreeEnv(env);
        return 5;
    }
    if (SQLAllocStmt(dbc, &stmt) != SQL_SUCCESS) {
        SQLDisconnect(dbc);
        SQLFreeConnect(dbc);
        SQLFreeEnv(env);
        return 6;
    }
    if (SQLExecDirect(
            stmt, (SQLCHAR *)"SELECT COUNT(*) FROM V$TABLES",
            SQL_NTS) != SQL_SUCCESS) {
        SQLFreeStmt(stmt, SQL_DROP);
        SQLDisconnect(dbc);
        SQLFreeConnect(dbc);
        SQLFreeEnv(env);
        return 7;
    }

    puts("query succeeded");
    SQLFreeStmt(stmt, SQL_DROP);
    SQLDisconnect(dbc);
    SQLFreeConnect(dbc);
    SQLFreeEnv(env);
    return 0;
}
```

실패 원인을 출력해야 하는 애플리케이션은 `SQLGetDiagRec()` 또는 기존 코드의
`SQLError()`로 SQLSTATE, 네이티브 오류 코드, 메시지를 읽습니다.

## 표준 실행 흐름

1. 환경과 연결 핸들을 할당합니다.
2. `SQLDriverConnect()` 또는 `SQLConnect()`로 연결합니다.
3. 문장 핸들을 할당합니다.
4. `SQLPrepare()`와 `SQLExecute()` 또는 `SQLExecDirect()`로 SQL을 실행합니다.
5. SELECT 결과는 `SQLBindCol()`과 `SQLFetch()`로 읽습니다.
6. 문장, 연결, 환경 순서로 자원을 해제합니다.

입력값은 문자열로 연결하지 말고 `SQLBindParameter()`로 바인딩합니다. nullable 여부는
`SQLDescribeCol()`의 마지막 인자 또는 `SQLColAttribute(..., SQL_DESC_NULLABLE, ...)`로
확인합니다.

## Named Bind Parameter

서버와 드라이버가 이름 기반 매개변수를 지원하면 `:name` 자리표시자를 사용하고
`SQLBindParameterByName()`으로 바인딩할 수 있습니다. 같은 이름이 여러 번 나오면 하나의
값이 모든 위치에 적용됩니다. 공통 제약과 예제는
Named Bind Parameter를
참고합니다.

지원 여부를 확인하지 못한 환경에서는 표준 `?` 자리표시자와 `SQLBindParameter()`를 사용합니다.

## INSERT 결과 ROWID

Standard Edition에서 단일 `INSERT ... VALUES`가 성공한 뒤 생성된 ROWID가 필요하면 다음
방식을 사용합니다.

- SQLCLI 확장: `SQLGetGeneratedRowID()`
- 표준 ODBC: generated ROWID 전용 표준 API 없음

배치, Append, `INSERT ... SELECT`, UPSERT에서는 같은 반환을 가정하지 않습니다. 자세한
범위는 ROWID와 INSERT 결과 ID를
참고합니다.

## Append 확장 API

고속 입력은 일반 문장과 분리된 Append 흐름을 사용합니다.

| 단계 | 주요 함수 |
|------|-----------|
| 열기 | `SQLAppendOpen()`, 선택 컬럼은 `SQLAppendOpenColumns()`/`W()` |
| 단건 입력 | `SQLAppendDataV2()` 또는 지원 버전의 Append 함수 |
| 배치 입력 | `SQLAppendBatch()` |
| 서버 반영 | `SQLAppendFlush()` |
| 오류 콜백 | `SQLAppendSetErrorCallback()` |
| 닫기 | `SQLAppendClose()` |

Append 행의 컬럼 순서와 타입은 대상 테이블 스키마와 정확히 일치해야 합니다. 문자열,
binary, IP, DATETIME, NULL 표현은 설치된 `machbase_sqlcli.h`의 `SQL_APPEND_PARAM` 정의를
기준으로 작성합니다. 오류 콜백에서는 실패한 행과 서버 오류를 기록하되 비밀번호나 원문
민감정보를 로그에 남기지 않습니다.

활성 Append 핸들이 있는 연결은 일반 쿼리와 공유하지 말고, close 결과의 성공·실패
건수를 확인합니다.

## 멀티스레드와 자원 관리

- 스레드마다 연결과 문장을 분리합니다.
- 하나의 문장 또는 Append 핸들을 여러 스레드가 동시에 사용하지 않습니다.
- 모든 오류 경로에서도 핸들이 역순으로 해제되도록 정리 함수를 둡니다.
- 재시도 전에 이전 연결과 Append 상태가 완전히 닫혔는지 확인합니다.
- 대량 입력은 성공 건수와 실패 건수를 모두 기록합니다.

## API 세부사항 확인

함수 원형, 상수, 구조체는 설치된
`$MACHBASE_HOME/include/machbase_sqlcli.h`가 해당 라이브러리와 일치하는 기준입니다.
샘플을 다른 버전의 헤더와 혼용하지 말고, 컴파일·링크·5656 연결 테스트를 배포 파이프라인에
포함합니다.

## DECIMAL Append

`SQLAppendDataV2()`와 `SQLAppendBatch()`로 `DECIMAL` 또는 `NUMERIC` 값을 입력할 때는
32바이트 opaque 타입 `SQL_APPEND_NUMERIC`과 공개 생성 함수를 사용합니다. 내부 바이트를
애플리케이션에서 직접 만들거나 수정하지 않습니다.

| 입력 | 함수 |
|---|---|
| UTF-8 숫자 문자열 | `SQLAppendNumericFromString()` |
| signed·unsigned 정수 | `SQLAppendNumericFromInt64()`, `SQLAppendNumericFromUInt64()` |
| `SQL_NUMERIC_STRUCT` | `SQLAppendNumericFromSQLNumeric()` |
| NULL | `SQLAppendNumericSetNull()` |

정확한 값을 보존하려면 문자열 또는 `SQL_NUMERIC_STRUCT`를 우선 사용합니다. 타입 배열에는
`SQL_APPEND_TYPE_NUMERIC` 또는 `SQL_APPEND_TYPE_DECIMAL`을 지정하고, 대상 컬럼의
전체 자릿수와 소수 자릿수를 기준으로 overflow와 반올림을 확인하십시오.

## ARRAY와 선택 컬럼 Append

Machbase DBMS 8.7.0은 `SQL_MACHBASE_ARRAY_DESC`를 사용한 typed ARRAY 조회·bind와
`SQL_MACHBASE_SPARSE_ARRAY_DESC`를 사용한 희소 입력을 지원합니다. 일반 Open에서도
ARRAY 컬럼에 희소 디스크립터를 전달할 수 있습니다.

```c
SQLAppendOpen(statement, (SQLCHAR *)"ARRAY_APPEND_FULL_EXAMPLE", 0);
row[0].mLong = 1;
row[1].mVar.mData = &sparse;
row[1].mVar.mLength = SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH;
SQLAppendDataV3(statement, row, 2);
SQLAppendClose(statement, &success, &failure);
```

위 코드는 `ID LONG, A INT32[4]` 테이블의 입력 순서를 따릅니다. 연결·디스크립터·버퍼
준비와 오류 처리를 포함한 일반 Open 전체 예제를
먼저 확인하십시오. 구형 `SQLAppendData(void *[])`에 디스크립터를 넘기는 방식과는 다릅니다.

일부 컬럼이나 고정 ARRAY 요소만 선택할 때는 `SQLAppendOpenColumns()` 또는
`SQLAppendOpenColumnsW()`를 사용합니다.

```c
SQLCHAR *targets[] = {
    (SQLCHAR *)"ID",
    (SQLCHAR *)"CHANNELS[0]",
    (SQLCHAR *)"CHANNELS[3]",
    NULL
};

SQLAppendOpenColumns(statement, (SQLCHAR *)"SENSOR_ARRAY", targets, 0);
```

ARRAY 요소 대상과 희소 디스크립터의 위치는 0부터 시작하는 인덱스입니다. 컬럼명 목록은
마지막 원소가 `NULL`이어야 합니다. `SQLAppendBatch()`는 ARRAY를 지원하지
않습니다. 디스크립터 정의, 배열 전체 NULL와 요소 NULL 처리, direct ODBC 핸들 제약은
Sparse ARRAY와 선택 컬럼 Append API를
참고하십시오.
