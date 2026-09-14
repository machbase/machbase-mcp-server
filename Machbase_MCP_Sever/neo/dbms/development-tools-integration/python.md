# Python

## 개요

2.4 패키지 기준입니다. PyPI 패키지명은 `machbaseapi`(소문자)이고, 순수 Python 구현이라
네이티브 바이너리(`.so/.dll/.dylib`)가 필요 없습니다. 기존 `machbase` 사용 흐름은
그대로 유지됩니다.

- 패키지 설치명: `machbaseapi`
- 기존과 동일하게 `import machbaseAPI` 사용
- DB-API 방식 `connect()`, `cursor()` 지원
- 2.4부터 `cursor(prepared=True)`로 서버 문장을 여러 호출에서 재사용
- `append*`는 `on_ack` 콜백을 추가할 수 있어 ACK 관찰 가능
- `append()`, `appendByTime()`, `appendData()`, `appendDataByTime()`는 타입 리스트를 생략해도 동작합니다. 서버 메타데이터 기반으로 타입을 자동 추론합니다.
- 2.3부터 append 행의 마지막 일부 컬럼을 생략하면 append null-bit를 통해 `NULL`로 저장합니다.
- TAG 테이블은 `value` 컬럼까지 필수이며, 이후 추가 컬럼과 메타데이터 컬럼은 생략 시 `NULL`로 저장할 수 있습니다.
- 커넥션 풀 옵션(`pool_name`, `pool_size`, `pool_reset_session`) 미지원

## 다중 데이터베이스

`connect(database=...)`로 초기 데이터베이스를 지정할 수 있습니다. current 카탈로그 getter/setter는
없으므로 연결 후 `SELECT CURRENT_DATABASE()`로 확인하고 SQL `USE`로 변경합니다.

```python
conn = connect(
    host='127.0.0.1', port=5656,
    user='APP_A', password='secret', database='FACTORY_A',
)
cur = conn.cursor()
cur.execute('SELECT CURRENT_DATABASE()')
print(cur.fetchone())
cur.execute('USE FACTORY_B')
```

기존 호환 `machbase.open()`에는 데이터베이스 인자가 없습니다. multi-database 작업에는 최신
`connect()`를 사용하십시오. 자세한 연결 풀·문장 바인딩 규칙은
다중 데이터베이스 운영 가이드를
참조하십시오.

## 설치

### 요구 사항

- `pip`을 사용할 수 있는 Python 3.6 이상
- 접속 가능한 Machbase 서버와 계정 정보(기본 계정 `SYS/MANAGER`, 포트 `5656`)
- 2.4는 네이티브 라이브러리 의존성이 없습니다.

### PyPI에서 설치

```bash
pip3 install machbaseapi
```

`pip3`가 PATH에 없다면 `python3 -m pip install machbaseapi` 명령을 사용합니다.

### 설치 패키지에서 오프라인 설치

인터넷에 연결할 수 없는 환경에서는 Machbase 설치 패키지에 포함된 wheel을 설치합니다.

```bash
python3 -m pip install \
  $MACHBASE_HOME/3rd-party/python3-module/machbaseapi-2.4-py3-none-any.whl
```

같은 디렉터리의 `machbaseapi-2.4.tar.gz` 소스 배포 파일도 사용할 수 있습니다. 설치 전에
Python 3.6 이상인지 확인합니다.

### 모듈 확인

```bash
python3 - <<'PY'
from machbaseAPI import machbase, connect
print('machbase 클래스 import:', bool(machbase))
print('connect 함수 존재:', callable(connect))
print('module import:', __import__('machbaseAPI'))
PY
```

위 명령이 성공하면 패키지를 정상적으로 import할 수 있습니다.

## 빠르게 시작하기

다음 DB-API 예제는 샘플 LOG 테이블을 만들고 입력·조회한 뒤 테이블과 연결을 정리합니다.
비밀번호는 환경 변수로 전달합니다.

```python
import os
from machbaseAPI import connect

conn = connect(
    host=os.getenv('MACH_HOST', '127.0.0.1'),
    port=int(os.getenv('MACH_PORT', '5656')),
    user=os.getenv('MACH_USER', 'SYS'),
    password=os.environ['MACHBASE_PASSWORD'],
)
cur = conn.cursor()

try:
    cur.execute(
        'CREATE LOG TABLE py_sample '
        '(ts DATETIME, device VARCHAR(40), value DOUBLE)'
    )
    cur.execute(
        "INSERT INTO py_sample VALUES ("
        "TO_DATE('2026-01-01','YYYY-MM-DD'), 'sensor-1', 20.5)"
    )
    cur.execute('SELECT device, value FROM py_sample')
    print(cur.fetchall())
finally:
    cur.execute('DROP TABLE py_sample')
    cur.close()
    conn.close()
```

## 결과 처리

DB-API 커서는 `execute()`, `fetchone()`, `fetchall()`을 제공합니다. 작업이 끝나면 커서와
연결을 닫고, 샘플 객체가 운영 데이터베이스에 남지 않도록 정리합니다.

### INSERT 결과 ROWID

Standard Edition에서 DB-API 커서로 단일 `INSERT ... VALUES`를 실행한 뒤
`cursor.lastrowid`에서 입력된 행의 ROWID를 확인할 수 있습니다.

```python
cursor.execute(
    "INSERT INTO orders(item) VALUES(%s)",
    ("pump",),
)
row_id = cursor.lastrowid
```

값은 임의 정밀도 Python `int`이며 unsigned 64비트 ROWID를 양수로 보존합니다. ROWID가 없는
실행에서는 `None`입니다. `executemany()`, Append, `INSERT ... SELECT`, UPSERT에서는
ROWID를 반환하지 않습니다. 실행 실패 후에도 이전 값을 재사용하지 마십시오. 자세한 조건은
ROWID와 INSERT 결과 ID를 참고하십시오.

### DB-API 결과의 Nullable 메타데이터

DB-API 커서에서는 `cursor.description[i][6]`의 `null_ok` 값으로 SELECT 결과 컬럼의
NULL 가능 여부를 확인합니다.

```python
cursor.execute(sql)

for column in cursor.description:
    name = column[0]
    null_ok = column[6]
    print(name, null_ok)
```

| `null_ok` | 의미 |
|-----------|------|
| `False` | NULL이 될 수 없음 |
| `True` | NULL이 될 수 있음 |
| `None` | 판정할 수 없음 |

`None`은 `NOT NULL`을 의미하지 않으므로 NULL이 발생할 수 있는 것으로 처리합니다.
SQL 결과의 판정 규칙은
Nullable 메타데이터 지원 범위를
참고합니다.

Machbase SQL에서 `''`은 SQL `NULL`이므로 `null_ok`는 `True`입니다. 다만 Python
connector는 문자열 SQL `NULL`을 기존 호환성에 따라 Python 빈 문자열 `""`으로 반환할 수
있습니다. `null_ok`는 컬럼의 NULL 가능성을 설명하며 개별 행이 NULL인지 알려 주지는
않습니다. 개별 행을 구분해야 하면 SQL의 `IS NULL` 조건이나 이를 이용한 CASE 결과를
함께 조회하십시오.

### SELECT 결과의 PRIMARY KEY 메타데이터

Machbase 8.7.0 서버와 해당 버전 SDK를 사용하면 `cursor.column_metadata`의
`is_primary_key`에서 SELECT 결과 직접 컬럼의 PRIMARY KEY 여부를 확인할 수 있습니다.

```python
cursor.execute("SELECT ID, VALUE, ID + 1 AS ID_EXPR FROM T_PK")
for column in cursor.column_metadata:
    print(column.name, column.is_primary_key)
```

`cursor.description`의 DB-API 표준 일곱 번째 값(`null_ok`)은 그대로 NULL 가능 여부만
나타냅니다. 표현식·집계식·외부 조인의 NULL 공급 측 컬럼은 PK가 아니므로
`is_primary_key`가 `False`입니다. 이전 버전 서버 또는 SDK와 연결한 경우에는 PK 플래그가
제공되지 않을 수 있습니다.

### Named Bind Parameter

Python DB-API 모듈의 `paramstyle`은 `"named"`입니다. `cursor.execute()`와
`cursor.executemany()`에 매핑을 전달하면 `:name` SQL을 서버의 prepare/bind 경로로
실행합니다.

```python
from decimal import Decimal
from machbaseAPI import connect

conn = connect(host="127.0.0.1", port=5656,
               user="SYS", password="MANAGER")
cur = conn.cursor(dictionary=False)

cur.execute(
    """INSERT INTO SENSOR_DATA (ID, NAME, VALUE)
       VALUES (:id, :name, :value)""",
    {
        "id": 600,
        "name": "python-client",
        "value": Decimal("52.125000"),
    },
)

cur.execute(
    """SELECT ID, NAME FROM SENSOR_DATA
       WHERE ID = :id OR PARENT_ID = :id""",
    {"id": 600},
)
```

`executemany()`는 각 행을 매핑으로 전달합니다.

```python
cur.executemany(
    "INSERT INTO SENSOR_DATA (ID, NAME, VALUE) "
    "VALUES (:id, :name, :value)",
    [
        {"id": 601, "name": "batch-a", "value": Decimal("1.5")},
        {"id": 602, "name": "batch-b", "value": None},
    ],
)
```

서버 Prepared Statement의 수명은 커서 종류와 호출 방식에 따라 다릅니다.

| Cursor | 호출 | 서버 문장 재사용 범위 |
|--------|------|----------------------------|
| 일반 커서 | `execute(sql, params)` | 해당 호출만 |
| 일반 커서 | `executemany(sql, rows)` | 해당 호출 내부 |
| 준비된 커서 | `execute()` / `executemany()` | 동일한 원본 SQL을 사용하는 후속 호출 |

일반 커서의 `:name`과 매핑은 서버 prepare/bind를 사용하지만 호출이 끝나면
문장을 닫습니다. 여러 호출에서 같은 문장을 재사용하려면
`cursor(prepared=True)`를 사용합니다.

매핑 키는 선행 콜론 없이 지정하며 대소문자를 구분합니다. 같은 이름이 반복되면 한
값을 모든 위치에 적용합니다. 이름 누락, extra 키와 named/positional 혼용은
`ProgrammingError`를 반환합니다. 이전 서버에서 이름 기반 API를 사용하면 SQLSTATE
`0A000`의 `NotSupportedError`를 반환합니다.

호환을 위해 `%s`와 `%(name)s` 문법도 유지합니다. 이 두 형식은 클라이언트에서 SQL
리터럴을 렌더링하는 일반 커서의 기존 경로입니다. 준비된 커서에서는 `%s`를 `?`로,
`%(name)s`를 `:name`으로 변환하여 서버 prepare/bind 경로로 실행합니다.

공통 이름 문법은
Named Bind Parameter syntax를
참고하십시오.

## Prepared Cursor (2.4)

`connection.cursor(prepared=True)`는 서버 Prepared Statement 하나를 보유하고 동일한 SQL을
여러 번 실행할 때 재사용합니다. 반복 INSERT, 반복 조건 조회와 동일 SQL의 배치 실행에
사용합니다.

```python
from machbaseAPI import connect

conn = connect(
    host="127.0.0.1",
    port=5656,
    user="SYS",
    password="MANAGER",
)
cur = conn.cursor(dictionary=False, raw=False, prepared=True)

sql = "INSERT INTO SENSOR_DATA (ID, NAME, VALUE) VALUES (%s, %s, %s)"
cur.execute(sql, (700, "sensor-a", 21.5))
cur.execute(sql, (701, "sensor-b", 22.1))
cur.executemany(
    sql,
    [
        (702, "sensor-c", 23.0),
        (703, "sensor-d", None),
    ],
)

cur.close()
conn.close()
```

`cursor()`의 관련 인자는 다음과 같습니다.

- `dictionary=True`: 조회 결과를 컬럼 이름 기반 dictionary로 반환합니다.
- `dictionary=False`: 조회 결과를 tuple로 반환합니다.
- `raw=True`: 기존 raw 결과 계약을 유지합니다.
- `prepared=True`: 공개 타입인 `MachbasePreparedCursor`를 반환합니다.
- `prepared=False`: 기존 일반 커서를 반환하는 기본값입니다.

### Parameter marker

준비된 커서는 Python DB-API 형식과 Machbase 네이티브 형식을 모두 지원합니다.

| 공개 자리표시자 | 서버 자리표시자 | Parameter 형태 |
|---------------|-------------|----------------|
| `%s` | `?` | tuple, list 등의 sequence |
| `?` | `?` | tuple, list 등의 sequence |
| `%(name)s` | `:name` | dictionary 등의 매핑 |
| `:name` | `:name` | dictionary 등의 매핑 |

문자열 리터럴, 따옴표로 묶은 식별자, `--` 주석과 `/* ... */` 주석 안의 자리표시자 모양은
변환하지 않습니다. 한 SQL에서 위치 기반 자리표시자와 이름 기반 자리표시자를 혼용할 수 없습니다.
이름 기반 자리표시자 이름은 영문자, `_`, `$`로 시작하고 이후에는 숫자도 사용할 수 있습니다.
이름 기반 자리표시자는 Machbase 8.7.0 서버와 해당 버전 SDK에서 지원합니다.

```python
sql = (
    "SELECT ID, NAME FROM SENSOR_DATA "
    "WHERE ID = %(target)s OR PARENT_ID = %(target)s"
)
cur.execute(sql, {"target": 700})
rows = cur.fetchall()
```

### Statement 재사용

준비된 커서는 원본 SQL 문자열이 이전 호출과 정확히 같을 때 캐시된 서버 문장을
재사용합니다. 공백이나 주석을 포함하여 문자열이 달라지면 기존 문장을 해제하고 새
문장을 준비합니다.

```python
insert_cur = conn.cursor(prepared=True)
select_cur = conn.cursor(prepared=True)
```

커서 하나는 서버 문장 하나만 보유합니다. 여러 SQL을 각각 계속 재사용하려면 위와
같이 SQL별 준비된 커서를 생성합니다. `executemany()`가 끝난 뒤에도 문장은
유지되며 동일 SQL의 후속 `execute()` 또는 `executemany()`에서 재사용됩니다. 빈 매개변수
목록을 전달하면 문장을 준비하거나 실행하지 않고 `0`을 반환합니다.

### 오류와 종료

다음 입력에는 `ProgrammingError`가 발생합니다.

- 자리표시자가 있지만 매개변수를 전달하지 않은 경우
- 위치 기반 자리표시자에 매핑을 전달하거나 이름 기반 자리표시자에 sequence를 전달한 경우
- 위치 기반 자리표시자와 이름 기반 자리표시자를 혼용한 경우
- 이름 기반 매개변수 키가 누락되거나 불필요한 키가 추가된 경우
- 자리표시자가 없는 SQL에 비어 있지 않은 매개변수를 전달한 경우

자리표시자가 없는 SQL에는 `None`, 빈 sequence 또는 빈 매핑을 매개변수 없음으로 전달할
수 있습니다. 빈 매핑은 내부적으로 `None`으로 정규화되므로 프로토콜 버전과 관계없이
같은 의미로 처리됩니다.

매개변수 오류가 발생해도 캐시된 문장은 유지되므로 올바른 매개변수로 같은 SQL을
다시 실행할 수 있습니다. 이전 버전 서버에서 이름 기반 매개변수를 사용하면
서버 PREPARE 전에 `NotSupportedError`와 SQLSTATE `0A000`이 발생합니다. 이 오류는 현재
캐시된 문장을 해제하거나 교체하지 않습니다. 구형 서버에서는 위치 기반 자리표시자를
사용합니다.

`cursor.close()`는 캐시된 서버 문장을 해제합니다. 같은 커서를 두 번 닫아도
안전하며, 연결이 먼저 닫힌 경우에는 네트워크 요청 없이 로컬 상태만 정리합니다.
닫힌 준비된 커서에서 `execute()`, `executemany()` 또는 fetch API를 호출하면
`InterfaceError`가 발생합니다.

준비된 커서는 SQL의 허용 범위나 Python API의 auto-commit 동작을 변경하지 않습니다.
테이블별 DML 범위는 지원 범위와 제약을 참고하십시오.

## 지원 API 매트릭스

| 클래스 | API | 설명 | 반환 |
| -- | -- | -- | -- |
| `machbase` | `open(host, user, password, port)` | 기본 계정과 포트로 Machbase 서버에 연결합니다. | 성공 시 `1`, 실패 시 `0` |
| `machbase` | `openEx(host, user, password, port, conn_str)` | 추가 연결 문자열 속성을 사용해 확장 연결을 수행합니다. | `1` 또는 `0` |
| `machbase` | `close()` | 현재 세션을 종료합니다. | `1` 또는 `0` |
| `machbase` | `isOpened()` | 핸들이 열려 있는지 확인합니다. | `1` 또는 `0` |
| `machbase` | `isConnected()` | 서버와의 연결 상태를 확인합니다. | `1` 또는 `0` |
| `machbase` | `execute(sql)` | SQL을 직접 실행합니다. `SELECT`, `WITH`, `DESC`, `DESCRIBE`, `SHOW`는 `select()`로 처리하고, 그 외 SQL은 `exec_direct()`로 실행합니다. | `1` 또는 `0` |
| `machbase` | `schema(sql)` | 스키마 관련 명령을 실행합니다. | `1` 또는 `0` |
| `machbase` | `tables()` | 모든 테이블의 메타데이터를 조회합니다. | `1` 또는 `0` |
| `machbase` | `columns(table_name)` | 특정 테이블의 컬럼 메타데이터를 조회합니다. | `1` 또는 `0` |
| `machbase` | `column(table_name)` | 저수준 카탈로그 호출로 컬럼 레이아웃을 가져옵니다. | `1` 또는 `0` |
| `machbase` | `statistics(table_name, user='SYS')` | CLI를 통해 테이블 통계를 요청합니다. | `1` 또는 `0` |
| `machbase` | `select(sql)` | 스트리밍 `SELECT` 또는 `DESC`를 실행합니다. | `1` 또는 `0` |
| `machbase` | `fetch()` | `select()` 호출 이후 다음 행을 가져옵니다. | `(rc, json_str)` |
| `machbase` | `selectClose()` | 열린 결과 집합 커서를 닫습니다. | `1` 또는 `0` |
| `machbase` | `result()` | 최신 JSON 페이로드를 반환합니다. | JSON 문자열 |
| `machbase` | `appendOpen(table_name, types=None)` | 컬럼 타입 코드를 지정하여 Append 프로토콜을 시작합니다. 생략 시 서버 메타데이터로 타입을 사용할 수 있습니다. | `1` 또는 `0` |
| `machbase` | `appendOpenColumns(table_name, columns, types=None)` | Machbase DBMS 8.7.0에서 선택 컬럼 또는 ARRAY 요소 대상으로 Append를 시작합니다. | `1` 또는 `0` |
| `machbase` | `appendData(table_name, rows_or_types, values=None, format='YYYY-MM-DD HH24:MI:SS', on_ack=None)` | 활성 Append 세션으로 행을 추가합니다. 타입 리스트를 생략하려면 두 번째 인자로 행을 전달합니다. 호출 시 데이터 패킷을 즉시 전송합니다. | `1` 또는 `0` |
| `machbase` | `appendDataByTime(table_name, rows_or_types, values=None, format='YYYY-MM-DD HH24:MI:SS', aTimes=None, on_ack=None)` | 명시적 타임스탬프로 행을 추가합니다. 타입 리스트를 생략하려면 두 번째 인자로 행을 전달하고 `aTimes`로 타임스탬프를 지정합니다. 호출 시 데이터 패킷을 즉시 전송합니다. | `1` 또는 `0` |
| `machbase` | `appendFlush()` | 이미 전송된 Append 데이터의 아직 받지 않은 서버 응답을 확인하는 동기화 지점입니다. 전송 지연 버퍼를 비우는 API가 아닙니다. | `1` 또는 `0` |
| `machbase` | `appendClose()` | Append 세션을 종료합니다. | `1` 또는 `0` |
| `machbase` | `append(table_name, rows_or_types, aValues=None, format='YYYY-MM-DD HH24:MI:SS')` | 열기·추가·닫기를 한 번에 처리하는 편의 함수입니다. 타입 리스트를 생략하려면 두 번째 인자로 행을 전달합니다. | `1` 또는 `0` |
| `machbase` | `appendByTime(table_name, rows_or_types, aValues=None, format='YYYY-MM-DD HH24:MI:SS', aTimes=None)` | 타임스탬프 인지 Append를 위한 편의 함수입니다. 타입 리스트를 생략하려면 두 번째 인자로 행을 전달하고 `aTimes`로 타임스탬프를 지정합니다. | `1` 또는 `0` |

## DB-API 스타일 API (2.4)

| API | 설명 | 반환 |
| -- | -- | -- |
| `connect(**kwargs)` | DB-API 연결 생성. `host`, `port`, `user`, `password` 등은 키워드 인자로 전달합니다. | `MachbaseConnection` |
| `cursor(dictionary=True, raw=False, prepared=False)` | 일반 또는 준비된 커서 생성 | `MachbaseCursor` 또는 `MachbasePreparedCursor` |
| `cursor.execute(sql, params=None)` | SQL 실행 | `cursor` |
| `cursor.executemany(sql, seq_of_params)` | 같은 SQL을 여러 매핑 또는 sequence로 실행 | 실행 횟수 |
| `cursor.fetchone()` | 한 건 조회 | `tuple | dict | None` |
| `cursor.fetchmany(size)` | 최대 `size`건 조회 | `list` |
| `cursor.fetchall()` | 전체 조회 | `list` |
| `cursor.description` | 결과 컬럼 메타데이터. 일곱 번째 값은 `null_ok`입니다. | `tuple | None` |
| `cursor.lastrowid` | 성공한 단일 INSERT의 ROWID. 지원되지 않는 입력 방식이나 실패 후에는 `None`입니다. | `int | None` |
| `cursor.close()` | 커서 종료 | `None` |
| `cursor.rowcount` | 영향 행 수 | `int` |
| `connection.append(table, rows, *, types=None, times=None, date_format=..., strict=False, columns=None)` | Append로 행을 추가합니다. `columns`는 선택 컬럼 또는 ARRAY 요소 대상을 지정합니다. | 입력 행 수 |

## 2.3 append 타입 생략과 trailing NULL padding (권장)

`append()`와 `appendByTime()`는 타입 리스트를 생략하고 호출할 수 있습니다.
두 번째 인자로 행 집합을 그대로 전달하면 서버 메타데이터 기반으로 처리합니다.
2.3부터는 입력 행의 마지막 일부 컬럼을 생략할 수 있고, 생략된 컬럼은 append null-bit를 통해 `NULL`로 저장됩니다.

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        db.execute('drop table py_append_auto')
        db.result()
        ddl = 'create table py_append_auto(ts datetime, tag varchar(16), reading double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        db.result()

        rows = [
            ['2024-01-01 10:00:00', 'node-1', 30.0],
            ['2024-01-01 10:01:00', 'node-1', 30.5],
        ]
        if db.append('PY_APPEND_AUTO', rows) == 0:
            raise SystemExit(db.result())
        print('append without types result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### DB-API append trailing NULL 예제

`connect().append()`도 같은 trailing `NULL` padding 규칙을 사용합니다. 중간 컬럼을 건너뛰는 위치 기반 입력은 지원하지 않으므로, 중간 값을 `NULL`로 입력하려면 해당 위치에 `None`을 명시합니다.

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

try:
    cur.execute('drop table py_append_null')
except Exception:
    pass
cur.execute('create table py_append_null(ts datetime, name varchar(20), value double, note varchar(40))')

conn.append('PY_APPEND_NULL', [
    ['2024-01-01 10:00:00', 'sensor-1', 12.3],
    ['2024-01-01 10:00:01', 'sensor-2', None, 'manual null'],
])

cur.execute('select ts, name, value, note from py_append_null order by ts')
print(cur.fetchall())
conn.close()
```

첫 번째 행은 `note` 컬럼을 생략했으므로 `NULL`로 저장됩니다. 두 번째 행은 `value` 위치에 `None`을 명시했으므로 `value`가 `NULL`로 저장됩니다.

### TAG 테이블 append와 metadata NULL 예제

TAG 테이블은 `name`, `time`, `value`에 해당하는 값까지는 반드시 입력해야 합니다. `value` 뒤에 정의한 추가 컬럼 또는 메타데이터 컬럼은 생략할 수 있으며, 생략된 컬럼은 `NULL`로 저장됩니다.

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

try:
    cur.execute('drop table py_tag_append_null')
except Exception:
    pass
cur.execute('''
    create tag table py_tag_append_null (
        name varchar(40) primary key,
        time datetime basetime,
        value double summarized,
        status varchar(20)
    ) metadata (
        site varchar(20),
        line integer
    )
''')

conn.append('PY_TAG_APPEND_NULL', [
    ['tag-1', '2024-01-01 10:00:00', 12.3],
])

cur.execute('select name, time, value, status, site, line from py_tag_append_null')
print(cur.fetchall())
conn.close()
```

위 예제에서 `status`, `site`, `line`은 모두 `NULL`로 저장됩니다. 반대로 `value`를 생략한 TAG append는 오류로 처리됩니다.

## `machbase` 클래스 호환 API

기존 애플리케이션과의 호환을 위해 유지되는 `machbase` 클래스 사용법을 설명합니다. 신규
코드에는 앞의 DB-API `connect()` 방식을 권장합니다.
`getSessionId()`, `count()`, `checkBit()`와 같은 API는 예전 네이티브 패키지에는 있었지만
현재 pure-Python 구현에서는 제공되지 않습니다. 필요 시 2.4 DB-API 예제를 참고하십시오.

각 스크립트에서 호스트·포트·계정 정보를 환경에 맞게 수정하십시오. 모든 예제는 독립 실행이 가능하며 `python3 script.py` 형태로 실행할 수 있습니다.

### 연결 관리

#### machbase.open(), machbase.isOpened(), machbase.isConnected(), machbase.close()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    print('isOpened before open:', db.isOpened())
    print('isConnected before open:', db.isConnected())

    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    print('isOpened after open:', db.isOpened())
    print('isConnected after open:', db.isConnected())

    if db.close() == 0:
        raise SystemExit(db.result())

    print('isOpened after close:', db.isOpened())
    print('isConnected after close:', db.isConnected())

if __name__ == '__main__':
    main()
```

#### machbase.openEx()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    conn_str = 'APP_NAME=python-demo'
    if db.openEx('127.0.0.1', 'SYS', 'MANAGER', 5656, conn_str) == 0:
        raise SystemExit(db.result())
    print('connected with openEx:', db.isConnected())
    if db.close() == 0:
        raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### DML과 결과 버퍼

#### machbase.execute(), machbase.result()

```python
#!/usr/bin/env python3
import json
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        rc = db.execute('drop table py_exec_demo')
        print('drop table rc:', rc)
        print('drop table result:', db.result())

        ddl = 'create table py_exec_demo(id integer, note varchar(32))'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        print('create table result:', db.result())

        for idx in range(2):
            sql = f"insert into py_exec_demo values ({idx}, 'row-{idx}')"
            if db.execute(sql) == 0:
                raise SystemExit(db.result())
            print('insert result:', db.result())

        if db.execute('select * from py_exec_demo order by id') == 0:
            raise SystemExit(db.result())
        payload = db.result()
        print('select payload:', payload)
        rows = json.loads(payload)
        print('decoded rows:', rows)
        print('row count:', len(rows))
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### 스트리밍 SELECT 도우미

#### machbase.select(), machbase.fetch(), machbase.selectClose()

```python
#!/usr/bin/env python3
import json
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        rc = db.execute('drop table py_select_demo')
        print('drop table rc:', rc)
        print('drop table result:', db.result())

        ddl = 'create table py_select_demo(id integer, value double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        print('create table result:', db.result())

        for idx in range(5):
            sql = f"insert into py_select_demo values ({idx}, {idx * 1.5})"
            if db.execute(sql) == 0:
                raise SystemExit(db.result())
            print('insert result:', db.result())

        if db.select('select id, value from py_select_demo order by id') == 0:
            raise SystemExit(db.result())

        fetched = 0
        while True:
            rc, payload = db.fetch()
            if rc == 0:
                break
            print('fetched row:', json.loads(payload))
            fetched += 1
        print('fetched rows:', fetched)

        db.selectClose()
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### 스키마 도우미

#### machbase.schema()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        rc = db.schema('drop table py_schema_demo')
        print('schema drop rc:', rc)
        print('schema drop result:', db.result())

        ddl = 'create table py_schema_demo(name varchar(20), created datetime)'
        if db.schema(ddl) == 0:
            raise SystemExit(db.result())
        print('schema create result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### 메타데이터와 통계

#### machbase.tables(), machbase.columns(), machbase.column(), machbase.statistics()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        if db.tables() == 0:
            raise SystemExit(db.result())
        print('tables metadata:', db.result())

        if db.columns('PY_EXEC_DEMO') == 0:
            raise SystemExit(db.result())
        print('columns metadata:', db.result())

        if db.column('PY_EXEC_DEMO') == 0:
            raise SystemExit(db.result())
        print('column metadata:', db.result())

        if db.statistics('PY_EXEC_DEMO') == 0:
            raise SystemExit(db.result())
        print('statistics output:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### Append 프로토콜 기본기

`appendOpen()`, `appendData()`, `appendFlush()`, `appendClose()`를 조합하면 행을 효율적으로 스트리밍할 수 있습니다. 2.1 이후에는 타입을 생략하고 `appendOpen()`으로 시작할 수 있습니다.
`appendData()`와 `appendDataByTime()`는 호출 시 데이터 패킷을 즉시 전송합니다. `appendFlush()`는 이미 전송된 append 데이터의 아직 받지 않은 서버 응답을 확인하는 동기화 지점입니다.

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        rc = db.execute('drop table py_append_demo')
        print('drop table rc:', rc)
        print('drop table result:', db.result())

        ddl = 'create table py_append_demo(ts datetime, device varchar(32), value double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        print('create table result:', db.result())

        if db.appendOpen('PY_APPEND_DEMO') == 0:
            raise SystemExit(db.result())

        rows = [
            ['2024-01-01 09:00:00', 'sensor-a', 21.5],
            ['2024-01-01 09:05:00', 'sensor-b', 22.1],
        ]
        if db.appendData('PY_APPEND_DEMO', rows) == 0:
            raise SystemExit(db.result())
        print('appendData result:', db.result())

        if db.appendFlush() == 0:
            raise SystemExit(db.result())
        print('appendFlush result:', db.result())

        if db.appendClose() == 0:
            raise SystemExit(db.result())
        print('appendClose result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### Append 편의 함수

#### machbase.append()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        db.execute('drop table py_append_auto')
        db.result()
        ddl = 'create table py_append_auto(ts datetime, tag varchar(16), reading double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        db.result()

        values = [
            ['2024-01-01 10:00:00', 'node-1', 30.0],
            ['2024-01-01 10:01:00', 'node-1', 30.5],
        ]
        if db.append('PY_APPEND_AUTO', values) == 0:
            raise SystemExit(db.result())
        print('append() result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

#### machbase.appendDataByTime(), machbase.appendByTime()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        db.execute('drop table py_append_time')
        db.result()
        ddl = 'create table py_append_time(ts datetime, tag varchar(16), reading double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        db.result()

        rows = [
            ['2024-01-01 11:00:00', 'node-2', 40.1],
            ['2024-01-01 11:01:00', 'node-2', 40.7],
        ]
        epoch_times = [
            1704106800 * 1_000_000_000,
            1704106860 * 1_000_000_000,
        ]

        if db.appendOpen('PY_APPEND_TIME') == 0:
            raise SystemExit(db.result())
        if db.appendDataByTime('PY_APPEND_TIME', rows, aTimes=epoch_times) == 0:
            raise SystemExit(db.result())
        print('appendDataByTime result:', db.result())
        db.appendClose()

        if db.appendByTime('PY_APPEND_TIME', rows, aTimes=epoch_times) == 0:
            raise SystemExit(db.result())
        print('appendByTime result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

`aTimes`는 행과 같은 순서의 epoch 나노초 sequence입니다. 초 단위 Unix 타임스탬프를
그대로 전달하지 마십시오.

## ARRAY와 선택 컬럼 Append

Machbase DBMS 8.7.0은 ARRAY를 Python `list`로 반환하며 prepared 입력에는 `list` 또는
`tuple`을 사용할 수 있습니다. 요소 NULL은 컬렉션 내부의 `None`, 배열 전체 NULL은
컬럼 자체의 `None`입니다.

컬럼 목록 없이 `connection.append(table, rows)`에 `SparseArray`를 전달할 수도 있습니다.

```python
from machbaseAPI import SparseArray

sparse = SparseArray(4).set(1, 200).set(3, 400)
connection.append("ARRAY_APPEND_FULL_EXAMPLE", [[2, sparse]])
```

이 코드는 `ID LONG, A INT32[4]` 테이블과 열린 연결을 전제로 합니다. 전체 NULL·빈 희소
배열과 결과 확인을 포함한 일반 입력 예제를
참고하십시오. legacy wrapper는
`appendOpen(table)` 예제를 제공합니다.

선택 대상은 `connection.append(..., columns=...)`로 지정합니다. 행마다 다른 ARRAY
위치를 입력할 때는 `SparseArray`를 사용합니다. 요소 위치를 지정한 대상과 `SparseArray.set()`의
위치는 0부터 시작하는 인덱스입니다.

```python
from machbaseAPI import SparseArray, connect

connection = connect(
    host="127.0.0.1",
    port=5656,
    user="SYS",
    password="MANAGER",
)
try:
    connection.append(
        "ARRAY_APPEND_EXAMPLE",
        [[1, 10, 40]],
        columns=["ID", "A[0]", "A[3]"],
    )

    sparse = SparseArray(4).set(1, 200).set(3, 400)
    connection.append(
        "ARRAY_APPEND_EXAMPLE",
        [[2, sparse]],
        columns=["ID", "A"],
    )
finally:
    connection.close()
```

`SparseArray.clear()`는 요소 수를 유지하면서 모든 요소를 NULL로 되돌립니다. 자세한
NULL 구분, 검증과 기존 호환 API 예제는
Sparse ARRAY와 선택 컬럼 Append API를
참고하십시오.
