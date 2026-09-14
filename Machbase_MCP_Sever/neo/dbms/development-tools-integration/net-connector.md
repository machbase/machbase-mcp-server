# .NET Connector

## 목차

* 개요
* 설치
* NuGet(통합 8.0.55)
* 커넥션 문자열 참고
* API 레퍼런스
* 사용 예시
* 프로토콜 4.0-full 전체 API

## 개요

Machbase는 와이어 프로토콜 2.1~4.0을 지원하는 범용 ADO.NET 프로바이더
**UniMachNetConnector**를 제공합니다. 현재 통합 패키지는 `UniMachNetConnector` 8.0.55이며
`net452`, `net5.0`, `net6.0`, `net7.0`, `net8.0` 타깃을 빌드합니다. 자동 협상은 연결
문자열에 `PROTOCOL=auto` 또는 `auto-full`을 지정했을 때만 동작합니다.

## 설치

설치된 Machbase 서버·클라이언트에는 `$MACHBASE_HOME/lib/` 경로에 범용 .NET 프로바이더가
함께 배포됩니다. 표준 Linux 설치에는 예를 들어 `UniMachNetConnector-net50-8.0.55.dll`과
`machNetConnector-40-net50-3.2.2.dll` 같은 프로토콜별 어셈블리가 포함될 수 있습니다.
소스 프로젝트는 필요한 .NET SDK가 있을 때 추가 target-framework flavor도 빌드할 수 있습니다.

- **UniMachNetConnector**: 프레임워크에 구애받지 않는 진입점입니다. 소스 빌드 파일 이름은
  `UniMachNetConnector-net{452|50|60|70|80}-<version>.dll` 형식이며, 배포 대상
  프레임워크에 맞는 파일을 선택합니다.
- **레거시 프로토콜 커넥터**: `machNetConnector-XX-net{40|50|60|70|80}-<version>.dll`과 같이
  프로토콜별로 나뉜 어셈블리입니다. UniMachNetConnector가 필요 시 로드합니다.

응용 프로그램에서는 대상 프레임워크에 맞는 DLL을 참조하거나, 배포 시 실행 파일과 같은 위치에 함께 배치하면 됩니다.

## 다중 데이터베이스

MachConnector 4.0은 연결 문자열의 `DATABASE` 또는 `DB_NAME`으로 초기 데이터베이스를
선택할 수 있습니다.

```text
SERVER=127.0.0.1;PORT_NO=5656;UID=APP_A;PWD=secret;DATABASE=FACTORY_A
```

표준 `Database` 설정 속성과 `ChangeDatabase()`를 current 카탈로그 전환 API로 보장하지
않으므로 SQL `USE`와 `CURRENT_DATABASE()`를 사용합니다. 연결 풀 반환 시 카탈로그 초기화도
자동으로 가정하지 않습니다. 자세한 제한은 다중 데이터베이스 운영 가이드를
참조하십시오.

## NuGet로 설치 (통합 커넥터, 8.0.55)

통합 커넥터의 패키지 ID는 `UniMachNetConnector`입니다. 새 프로젝트에서는 DLL 복사 대신 NuGet 패키지 참조 방식을 권장합니다.

- 지원 TFM: net452, net5.0, net6.0, net7.0, net8.0
- net5.0 이상 빌드는 self-contained입니다. net452 빌드는 소스 프로젝트 기준
  `System.ValueTuple` 4.5.0을 복원합니다.

### 빠른 시작(명령줄)

```bash
# 프로젝트 폴더에서 실행
dotnet add package UniMachNetConnector --version 8.0.55
dotnet build
```

소스(피드)를 명시적으로 제어해야 하면 참조 추가만 하고, 별도로 복원하십시오.

```bash
dotnet add package UniMachNetConnector --version 8.0.55 --no-restore

# nuget.org 메타데이터를 강제로 갱신
dotnet nuget locals http-cache --clear
dotnet restore --no-cache --source https://api.nuget.org/v3/index.json
```

### Visual Studio

- 프로젝트 마우스 오른쪽 클릭 → NuGet 패키지 관리 → 찾아보기 → “UniMachNetConnector” 검색 → 8.0.55 선택 → 설치.

### 프로젝트 파일 예시

```xml
<ItemGroup>
  <PackageReference Include="UniMachNetConnector" Version="8.0.55" />
  <!-- 추가 Machbase 패키지 불필요 -->
  <!-- 대상 프레임워크: net452|net5.0|net6.0|net7.0|net8.0 -->
</ItemGroup>
```

### 로컬/사내 피드 사용(선택)

사내 레지스트리 또는 폴더 피드를 사용할 경우 다음과 같이 소스를 추가하고 복원합니다. 폴더 피드는 `UniMachNetConnector.8.0.55.nupkg`를 해당 디렉터리에 배치하면 됩니다.

```bash
# 1회 설정
dotnet nuget add source /path/to/local-nuget -n mach-local

# nuget.org와 병행 복원
dotnet restore --no-cache \
  --source /path/to/local-nuget \
  --source https://api.nuget.org/v3/index.json
```

권한 제약이 있는 환경에서는 패키지 캐시 경로를 절대 경로로 지정하십시오.

```bash
PKG_DIR="$(pwd)/.nuget-packages"; mkdir -p "$PKG_DIR"
NUGET_PACKAGES="$PKG_DIR" dotnet restore --no-cache --source /path/to/local-nuget
NUGET_PACKAGES="$PKG_DIR" dotnet run --no-restore
```

> 팁: 게시 직후 NU1102(지정 버전을 찾지 못함)나 “incompatible with 'all' frameworks”가 보이면 보통 인덱싱/캐시 이슈입니다. `dotnet nuget locals http-cache --clear` 후 `--no-cache`로 복원하면 해결됩니다. 패키지는 net452 및 net5.0~net8.0을 지원합니다.

### 최소 사용 예시

```csharp
using System;
using Mach.Data.MachClient;

var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
var cs = $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
using var conn = new MachConnection(cs);
conn.Open();

using var cmd = new MachCommand("SELECT COUNT(*) FROM V$TABLES", conn);
var count = Convert.ToInt64(cmd.ExecuteScalar());
Console.WriteLine($"Tables: {count}");
```

## 커넥션 문자열 참고

커넥션 문자열의 각 항목은 세미콜론(`;`)으로 구분합니다. 표의 한 행에 표시된 키워드는 서로 동일한 의미를 갖습니다.

| 키워드                                                         | 설명                                                                                                  | 예시                                             | 기본값  |
|----------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|--------------------------------------------------|---------|
| `DSN`, `SERVER`, `HOST`                                        | 호스트명 또는 IP 주소                                                                                 | `SERVER=127.0.0.1`                               | 없음    |
| `PORT`, `PORT_NO`                                              | 수신 포트                                                                                             | `PORT=5656`                                     | `5656`  |
| `USERID`, `USERNAME`, `USER`, `UID`                            | 사용자 이름                                                                                            | `UID=SYS`                                        | `SYS`   |
| `PASSWORD`, `PWD`                                              | 비밀번호                                                                                               | `PWD=manager`                                    | 없음    |
| `CONNECT_TIMEOUT`, `ConnectionTimeout`, `connectTimeout`       | 커넥션 타임아웃(밀리초)                                                                                | `CONNECT_TIMEOUT=10000`                          | `60000` |
| `COMMAND_TIMEOUT`, `CommandTimeout`, `commandTimeout`          | 명령별 타임아웃(밀리초)                                                                               | `COMMAND_TIMEOUT=50000`                          | `60000` |
| `PROTOCOL`, `ProtocolVersion`, `MachProtocol`                  | 선호하는 와이어 프로토콜 (`2.1`, `3.0`, `4.0`, `4.0-full`, `auto`, `auto-full` 등). 입력하지 않으면 `4.0`을 사용합니다. | `PROTOCOL=auto`                                  | `4.0`   |

예시:

```csharp
var connectionString = string.Format(
    "SERVER={0};PORT_NO={1};UID=SYS;PWD=MANAGER;COMMAND_TIMEOUT=50000;PROTOCOL=4.0-full",
    host,
    port);
```

### 프로토콜 자동 감지 (`PROTOCOL=auto`)

서버 버전이 혼재된 환경이라면 `PROTOCOL=auto`를 지정해 UniMachNetConnector가 실행 시 적절한 레거시 프로토콜을 협상하도록 설정할 수 있습니다. 동작 방식은 다음과 같습니다.

- `PROTOCOL=auto`는 4.0 → 3.0 → 2.2 → 2.1 순서로 핸드셰이크를 시도하며, 커넥션 문자열에 전달한 호스트·포트·사용자·비밀번호·데이터베이스·`CONNECT_TIMEOUT` 값을 그대로 사용합니다.
- `PROTOCOL=auto-full`은 서버 major가 4이면 등록된 `4.0-full` 디스크립터를 선택합니다.
  디스크립터가 없는 빌드에서만 limited 4.0을 선택하며, full 연결 실패 후 limited로 자동
  재시도하지 않습니다.
- `SERVER=hostA:5700,hostB:6000`처럼 여러 호스트를 지정하면 순차적으로 시도하며, 실패 메시지에는 각 호스트/프로토콜 조합이 기록되어 문제 지점을 파악할 수 있습니다.
- 자격 증명은 기존 레거시 드라이버와 동일하게 대문자로 변환됩니다. 기본 데이터베이스(`data`)를 사용하지 않는다면 `DATABASE=` 값을 명시하십시오.
- `CONNECT_TIMEOUT` 값이 각 감지 라운드 트립에 적용됩니다. 예외 메시지에 `Protocol probe received an invalid response`가 보이면 포트·방화벽·TLS 설정을 다시 확인하십시오.

이미 서버 버전을 알고 있다면 `PROTOCOL=2.1`, `3.0`, `4.0`, `4.0-full`처럼 명시적으로 지정해 자동 감지를 건너뛸 수도 있습니다.

## API 레퍼런스

> **주의**
> 아래에 명시되지 않은 기능은 아직 구현되지 않았거나 정상적으로 동작하지 않을 수 있습니다.<br>
> 선언된 API라도 구현하지 않거나 지원하지 않는 기능은 `NotImplementedException` 또는
> `NotSupportedException`을 반환할 수 있습니다. 필요한 API가 설치한 프로바이더에 있는지
> 먼저 확인하십시오.

### MachConnection

```cs
public sealed class MachConnection : DbConnection
```

Machbase와의 연결을 담당하는 클래스입니다. `DbConnection`과 동일하게 `IDisposable`을 구현하므로 `Dispose()` 호출이나 `using` 문으로 안전하게 해제할 수 있습니다.

#### 생성자

```
MachConnection(string aConnectionString)
```

커넥션 문자열을 입력 받아 `MachConnection` 인스턴스를 생성합니다.

#### Open

```cs
void Open()
```

커넥션 문자열을 사용해 실제 연결을 수립합니다.

#### Close

```cs
void Close()
```

열려 있는 연결을 종료합니다.

#### SetConnectAppendFlush

```cs
void SetConnectAppendFlush(bool activeFlush)
```

Append 작업 중 자동으로 flush를 수행할지 여부를 설정합니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `State` | `System.Data.ConnectionState` 값을 나타냅니다. |
| `StatusString` | 현재 연결이 의존하는 `MachCommand`의 상태 문자열입니다. 내부 로깅용이므로 쿼리 상태 판단 용도로 사용하지 않는 것이 좋습니다. |

### MachCommand

```cs
public sealed class MachCommand : DbCommand
```

`MachConnection`을 통해 SQL 명령이나 Append 작업을 실행하는 클래스입니다. `DbCommand`와 마찬가지로 `IDisposable`을 구현합니다.

#### 생성자

```cs
MachCommand(string aQueryString, MachConnection aConn)
```

실행할 쿼리와 연결 객체를 지정해 인스턴스를 생성합니다.

```cs
MachCommand(MachConnection aConn)
```

쿼리가 필요 없는 Append 전용 커맨드를 생성합니다.

#### CreateParameter

```cs
MachParameter CreateParameter()
```

새로운 `MachParameter`를 생성합니다.

#### AppendOpen

```cs
MachAppendWriter AppendOpen(
    string aTableName,
    int aErrorCheckCount = 0,
    MachAppendOption option = MachAppendOption.None)
```

Append 세션을 열고 `MachAppendWriter`를 반환합니다.

* `aTableName`: 대상 테이블 이름
* `aErrorCheckCount`: 지정한 레코드 수마다 서버에 전송해 실패 여부를 확인합니다. 즉, 자동 `APPEND-FLUSH` 지점을 설정합니다.
* `option`: `None` 또는 `MicroSecTruncated` 옵션을 지정할 수 있습니다.

#### AppendData

```cs
void AppendData(MachAppendWriter writer, List<object> dataList)
```

리스트에 있는 값을 순서대로 Append 버퍼에 적재합니다. 각 값의 타입은 테이블 컬럼 타입과 일치해야 하며, 값이 부족하거나 초과하면 예외가 발생합니다.

> **참고**: `_arrival_time`을 `ulong`으로 직접 지정할 때는 Machbase가 기대하는 1970-01-01 UTC 기준 나노초 값을 입력해야 합니다.

```cs
void AppendDataWithTime(
    MachAppendWriter writer,
    List<object> dataList,
    DateTime arrivalTime)
```

`_arrival_time`을 `DateTime`으로 명시적으로 지정합니다.

```cs
void AppendDataWithTime(
    MachAppendWriter writer,
    List<object> dataList,
    ulong arrivalTime)
```

`_arrival_time`을 나노초 단위 `ulong`으로 지정합니다.

#### AppendFlush

```cs
void AppendFlush(MachAppendWriter writer)
```

버퍼에 쌓인 데이터를 서버로 전송합니다. 호출 주기를 줄이면 클라이언트 버퍼에 남는 데이터와
전송 지연을 줄일 수 있지만 통신 비용은 증가할 수 있습니다. 호출 성공만으로 디스크 내구성을
판단하지 말고, 서버 처리 결과와 대상 테이블의 내구성 정책을 함께 확인합니다.

#### AppendClose

```cs
void AppendClose(MachAppendWriter writer)
```

Append 세션을 종료합니다. 내부적으로 `AppendFlush()` 호출 후 프로토콜을 마무리합니다.

#### ExecuteNonQuery

```cs
int ExecuteNonQuery()
```

쿼리를 실행하고 영향을 받은 레코드 수를 반환합니다. 주로 `INSERT`, `UPDATE`, `DELETE`, DDL에서 사용합니다.

#### RowId

```cs
UInt64? RowId
```

Standard Edition에서 단일 `INSERT ... VALUES`가 성공하면 MachConnector 4.0/4.0-full과
Universal .NET의 `ExecuteNonQuery()` 호출 후 입력된 행의 ROWID를 확인할 수 있습니다.

```cs
using (var command = new MachCommand(
    "INSERT INTO orders(item) VALUES('pump')", connection))
{
    command.ExecuteNonQuery();
    ulong? rowId = command.RowId;
}
```

반환할 ROWID가 없으면 `null`입니다. ROWID는 64비트 `RowId`로 읽고, 기존 32비트
`LastInsertedId`는 사용하지 않습니다. 배치와 Append 등의 차이는
ROWID와 INSERT 결과 ID를 참고하십시오.

#### ExecuteScalar

```cs
object ExecuteScalar()
```

쿼리를 실행하고 첫 번째 컬럼 값을 반환합니다.

#### ExecuteDbDataReader

```cs
DbDataReader ExecuteDbDataReader(CommandBehavior behavior)
```

쿼리를 실행하고 결과를 순차적으로 읽을 수 있는 `DbDataReader`를 반환합니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `Connection` / `DbConnection` | 현재 연결된 `MachConnection`입니다. |
| `ParameterCollection` / `DbParameterCollection` | 바인딩에 사용할 파라미터 컬렉션입니다. |
| `CommandText` | 실행할 SQL 문자열입니다. |
| `CommandTimeout` | 서버 응답을 기다리는 최대 시간(밀리초)입니다. 값은 `MachConnection` 설정을 따르며 여기서는 조회만 가능합니다. |
| `FetchSize` | 서버에서 한 번에 가져올 레코드 수입니다. 기본값은 3000입니다. |
| `IsAppendOpened` | Append 세션이 열려 있는지 여부입니다. |
| `RowId` | 성공한 단일 INSERT의 64비트 ROWID입니다. 값이 없으면 `null`입니다. |

### MachDataReader

```cs
public sealed class MachDataReader : DbDataReader
```

Fetch된 결과를 순차적으로 읽는 리더입니다. `MachCommand.ExecuteDbDataReader()`로 획득한 객체만 사용할 수 있습니다.

#### GetName

```cs
string GetName(int ordinal)
```

지정한 인덱스의 컬럼 이름을 반환합니다.

#### GetDataTypeName

```cs
string GetDataTypeName(int ordinal)
```

Machbase 컬럼 타입 이름을 반환합니다.

#### GetFieldType

```cs
Type GetFieldType(int ordinal)
```

.NET 측 매핑 타입을 반환합니다.

#### GetOrdinal

```cs
int GetOrdinal(string name)
```

컬럼 이름에 해당하는 인덱스를 반환합니다.

#### GetValue

```cs
object GetValue(int ordinal)
```

현재 레코드의 값을 `object`로 반환합니다.

#### IsDBNull

```cs
bool IsDBNull(int ordinal)
```

해당 컬럼 값이 `NULL`인지 확인합니다.

#### GetValues

```cs
int GetValues(object[] values)
```

현재 레코드의 값을 배열에 채워 넣고 채워진 항목 수를 반환합니다.

#### GetSchemaTable

```cs
DataTable GetSchemaTable()
```

SELECT 결과 컬럼의 스키마 메타데이터를 반환합니다. `AllowDBNull`로 NULL 가능 여부를
확인합니다. 이 동작은 MachConnector40과 MachConnector40-full-API에 동일하게
적용됩니다.

```csharp
using var reader = command.ExecuteReader();
DataTable schema = reader.GetSchemaTable();

foreach (DataRow row in schema.Rows)
{
    string columnName = Convert.ToString(row["ColumnName"]);
    object allowDBNull = row["AllowDBNull"];

    if (allowDBNull is bool value && !value)
    {
        Console.WriteLine($"{columnName}: NO_NULLS");
    }
    else
    {
        // true 또는 DBNull.Value: NULL 처리 필요
        Console.WriteLine($"{columnName}: NULL 처리 필요");
    }
}
```

| `AllowDBNull` | 의미 |
|---------------|------|
| `false` | NULL이 될 수 없음 |
| `true` | NULL이 될 수 있음 |
| `DBNull.Value` | 판정할 수 없음 |

`DBNull.Value`는 `NOT NULL`을 의미하지 않습니다. NULL이 발생할 수 있는 것으로
처리합니다. SQL 결과의 판정 규칙은
Nullable 메타데이터 지원 범위를
참고합니다.

Machbase SQL에서 `''`은 SQL `NULL`이므로 `GetSchemaTable()`의 `AllowDBNull`은 `true`이고
해당 행에서 `IsDBNull()`은 `true`입니다. `''''`는 작은따옴표 한 글자이므로
`AllowDBNull=false`인 NULL이 아닌 문자열 결과입니다.

`GetSchemaTable()`은 `ColumnName`, `ColumnOrdinal`, `ColumnSize`, `NumericPrecision`,
`NumericScale`, `DataType`, `ProviderType`, `IsLong`, `AllowDBNull`, `IsKey`를 제공합니다.
`IsKey`가 `true`이면 SELECT 결과의 직접 컬럼이 PRIMARY KEY입니다. 표현식이나 집계식은
`false`입니다.

이전 버전 서버 또는 SDK와 연결한 경우에는 `IsKey`가 `false`로 반환될 수 있습니다.

Nullable 메타데이터는 DECIMAL 전체 자릿수 `1~65`, 소수 자릿수 `0~30`과 실제 값을 변경하지
않습니다. .NET에서는 전체 자릿수가 29 이하이고 소수 자릿수가 28 이하인 DECIMAL을
`System.Decimal`로 반환합니다. 이 범위를 넘는 DECIMAL은 정밀도 손실을 방지하기 위해
`System.String`으로 반환합니다. 이때 `GetSchemaTable().DataType`, `GetFieldType()`,
실제 행 값의 CLR 형식도 모두 `System.String`입니다.

#### Get*XXXX*

```cs
bool GetBoolean(int ordinal)
byte GetByte(int ordinal)
char GetChar(int ordinal)
short GetInt16(int ordinal)
int GetInt32(int ordinal)
long GetInt64(int ordinal)
DateTime GetDateTime(int ordinal)
string GetString(int ordinal)
decimal GetDecimal(int ordinal)
double GetDouble(int ordinal)
float GetFloat(int ordinal)
```

컬럼 값을 지정한 타입으로 반환합니다.

#### Read

```cs
bool Read()
```

다음 레코드를 읽습니다. 결과가 더 이상 없으면 `false`를 반환합니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `FetchSize` | 서버에서 한 번에 가져올 레코드 수입니다. 기본값은 3000이며 여기에서는 수정할 수 없습니다. |
| `FieldCount` | 결과 컬럼 수입니다. |
| `this[int ordinal]` | `GetValue(int ordinal)`과 동일합니다. |
| `this[string name]` | `GetValue(GetOrdinal(name))`과 동일합니다. |
| `HasRows` | 결과가 존재하는지 여부입니다. |
| `RecordsAffected` | Fetch된 레코드 수를 나타냅니다. |

### MachParameterCollection

```cs
public sealed class MachParameterCollection :
    DbParameterCollection,
    IEnumerable<MachParameter>
```

`MachCommand`에 바인딩할 파라미터 집합을 관리하는 클래스입니다.

파라미터를 설정한 뒤 실행하면 해당 값이 함께 전송됩니다.

> `MachParameter` 바인딩은 Prepared Statement 의미의 실행 계획 캐시를 제공하지 않습니다.
> 반복 실행 성능은 실제 쿼리와 서버 캐시 상태로 측정합니다.
>
> 현재 프로바이더는 파라미터를 타입별 SQL 리터럴로 렌더링한 뒤 ExecDirect로 실행합니다.
> 따라서 `MachParameterCollection`은 서버의 Prepared Named Bind 프로토콜이나 파라미터
> 메타데이터를 사용하지 않습니다.

#### Add

```cs
MachParameter Add(string parameterName, DbType dbType)
```

파라미터 이름과 타입을 지정해 `MachParameter`를 추가하고, 생성된 객체를 반환합니다.

```cs
int Add(object value)
```

값을 추가하고 추가된 인덱스를 반환합니다.

```cs
void AddRange(Array values)
```

단순 값 배열을 한 번에 추가합니다.

```cs
MachParameter AddWithValue(string parameterName, object value)
```

파라미터 이름과 값을 동시에 추가하고, 생성된 `MachParameter`를 반환합니다.

#### Contains

```cs
bool Contains(object value)
```

해당 값이 이미 추가되어 있는지 확인합니다.

```cs
bool Contains(string parameterName)
```

지정한 파라미터 이름이 존재하는지 확인합니다.

#### Clear

```cs
void Clear()
```

모든 파라미터를 제거합니다.

#### IndexOf

```cs
int IndexOf(object value)
```

해당 값이 있는 인덱스를 반환합니다.

```cs
int IndexOf(string parameterName)
```

파라미터 이름이 위치한 인덱스를 반환합니다.

#### Insert

```cs
void Insert(int index, object value)
```

지정한 위치에 값을 삽입합니다.

#### Remove

```cs
void Remove(object value)
```

해당 값을 포함한 파라미터를 제거합니다.

```cs
void RemoveAt(int index)
```

인덱스에 위치한 파라미터를 제거합니다.

```cs
void RemoveAt(string parameterName)
```

지정한 이름의 파라미터를 제거합니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `Count` | 파라미터 개수입니다. |
| `this[int index]` | 해당 인덱스의 `MachParameter`입니다. |
| `this[string name]` | 이름과 일치하는 `MachParameter`입니다. |

### MachParameter

```cs
public sealed class MachParameter : DbParameter
```

개별 파라미터의 바인딩 정보를 저장하는 클래스입니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `ParameterName` | 파라미터 이름입니다. |
| `Value` | 전송할 값입니다. |
| `Size` | 값의 길이입니다. |
| `Direction` | `ParameterDirection` 값입니다. 기본값은 `Input`입니다. |
| `DbType` | .NET 측 DB 타입입니다. |
| `MachDbType` | Machbase 고유 타입입니다. |
| `IsNullable` | `NULL` 허용 여부입니다. |
| `HasSetDbType` | `DbType`이 설정되었는지 여부입니다. |

### MachException

```cs
public class MachException : DbException
```

Machbase에서 발생한 오류를 표현하는 예외 클래스입니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `MachErrorCode` | 가능한 경우 Machbase 오류 코드입니다. Universal 프로바이더가 기존 호환 예외를 번역하면 `0`일 수 있습니다. |

### MachAppendWriter

```cs
public sealed class MachAppendWriter
```

Append 프로토콜을 다루기 위한 보조 클래스입니다. `MachCommand.AppendOpen()` 호출 시 인스턴스를 획득합니다.

#### SetErrorDelegator

```cs
void SetErrorDelegator(ErrorDelegateFuncType callback)

void ErrorDelegateFuncType(MachAppendException e);
```

Append 중 오류가 발생했을 때 호출할 델리게이트를 등록합니다.

#### 필드

| 이름 | 설명 |
|--|--|
| `SuccessCount` | 성공적으로 저장된 레코드 수입니다. `AppendClose()` 이후에 확인할 수 있습니다. |
| `FailureCount` | 실패한 레코드 수입니다. `AppendClose()` 이후에 설정됩니다. |
| `Option` | `AppendOpen()` 호출 시 사용한 `MachAppendOption` 값입니다. |

### MachAppendException

```cs
public sealed class MachAppendException : MachException
```

Append 과정에서 발생한 오류 정보를 추가로 제공하는 예외입니다. 서버가 반환한 오류 메시지를 그대로 전달하며, 실패한 레코드를 문자열로 확인할 수 있습니다.

#### GetRowBuffer

```cs
string GetRowBuffer()
```

오류가 발생한 원본 레코드를 문자열 형태로 반환합니다.

## 사용 예시

### 연결

다음 예제는 환경 변수 비밀번호로 연결하고 LOG 테이블을 생성·입력·조회한 뒤 삭제합니다.

```csharp
using System;
using Mach.Data.MachClient;

var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
var connString = $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();
const string tableName = "NET_QUERY_DEMO";

using (var create = new MachCommand(
    $"CREATE LOG TABLE {tableName} (id INTEGER, name VARCHAR(40))", connection))
{
    create.ExecuteNonQuery();
}
try
{
    using (var insert = new MachCommand(
        $"INSERT INTO {tableName} VALUES (1, 'pump')", connection))
    {
        insert.ExecuteNonQuery();
    }
    using var query = new MachCommand($"SELECT id, name FROM {tableName}", connection);
    using var reader = query.ExecuteReader();
    while (reader.Read())
    {
        for (var column = 0; column < reader.FieldCount; column++)
        {
            Console.WriteLine($"{reader.GetName(column)} : {reader.GetValue(column)}");
        }
    }
}
finally
{
    using var drop = new MachCommand($"DROP TABLE {tableName}", connection);
    drop.ExecuteNonQuery();
}
```

### 파라미터 바인딩

`MachParameterCollection`은 `:name`, `@name`, `?name` 자리표시자를 처리합니다. 공통 SQL
문법과 같은 `:name` 형식을 권장합니다. 이름 검색은 대소문자를 구분하지 않으며, 같은
이름이 반복되면 한 값이 모든 위치에 적용됩니다.

`:name` 형식은 Machbase 8.7.0 서버 연결에서 사용합니다. 이전 서버에 연결하면
`MachException`을 반환합니다. `@name`과 `?name`은 기존 프로바이더 호환 형식입니다.

```csharp
var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
var connString = $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();

const string sql = @"
    SELECT NAME
      FROM V$TABLES
     WHERE NAME = :table_name OR NAME = :table_name";

using var command = new MachCommand(sql, connection);

command.Parameters.AddWithValue(":table_name", "V$TABLES");

using var reader = command.ExecuteReader();
while (reader.Read())
{
    Console.WriteLine($"{reader.GetName(0)} : {reader.GetValue(0)}");
}
```

NULL은 `DBNull.Value`로 전달합니다. 공통 이름 문법은
Named Bind Parameter syntax를
참고하십시오.

### Append

Append 프로토콜을 사용하면 대량의 시계열 데이터를 빠르게 적재할 수 있습니다.

```csharp
using System;
using System.Collections.Generic;
using Mach.Data.MachClient;

var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
var connString = $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();

const string tableName = "NET_APPEND_DEMO";
using (var create = new MachCommand(
    $"CREATE LOG TABLE {tableName} (ID INTEGER, NAME VARCHAR(40))", connection))
{
    create.ExecuteNonQuery();
}

try
{
using var appendCommand = new MachCommand(connection);
var writer = appendCommand.AppendOpen(tableName);
writer.SetErrorDelegator(error =>
    Console.Error.WriteLine($"Append row error: {error.Message}\n{error.GetRowBuffer()}"));

try
{
    for (var i = 1; i <= 100000; i++)
    {
        appendCommand.AppendData(writer, new List<object> { i, $"NAME_{i % 100}" });
        if (i % 1000 == 0) appendCommand.AppendFlush(writer);
    }
}
finally
{
    if (appendCommand.IsAppendOpened) appendCommand.AppendClose(writer);
}

Console.WriteLine($"Success Count : {writer.SuccessCount}");
Console.WriteLine($"Failure Count : {writer.FailureCount}");
if (writer.FailureCount != 0)
    throw new InvalidOperationException($"Append failed rows: {writer.FailureCount}");
}
finally
{
    if (connection.State == System.Data.ConnectionState.Open)
    {
        try
        {
            using var drop = new MachCommand($"DROP TABLE {tableName}", connection);
            drop.ExecuteNonQuery();
        }
        catch (Exception cleanupError)
        {
            Console.Error.WriteLine($"cleanup failed: {cleanupError.Message}");
        }
    }
}
```

### ARRAY와 선택 컬럼 Append

Machbase DBMS 8.7.0 full/legacy 프로바이더는 ARRAY를 `object[]`로 반환합니다. 요소 NULL은
배열 안의 `null`, 배열 전체 NULL은 `IsDBNull()`로 구분합니다.

일반 `AppendOpen(table)`에서도 `MachSparseArray`를 ARRAY 컬럼 값으로 입력할 수 있습니다.

```csharp
var writer = append.AppendOpen("ARRAY_APPEND_FULL_EXAMPLE");
```

이때 입력 행은 테이블의 컬럼 순서를 따릅니다. `ID LONG, A INT32[4]` 테이블에 희소 값,
빈 희소 배열과 전체 NULL을 입력하는
일반 Open 예제에서
`AppendData()`와 Close·결과 확인까지 설명합니다.

`AppendOpen()`의 `IList<string>` 오버로드에는 일반 컬럼이나
`ARRAY_COLUMN[position]`을 전달할 수 있습니다. 행마다 다른 위치를 입력할 때는
`MachSparseArray`를 배열 전체 대상에 전달합니다. 요소 위치를 지정한 대상과
`MachSparseArray.Set()`의 위치는 0부터 시작하는 인덱스입니다.

```csharp
using var append = new MachCommand(connection);
var writer = append.AppendOpen(
    "ARRAY_APPEND_EXAMPLE",
    new List<string> { "ID", "A" });
var sparse = new MachSparseArray(MachDBType.INT32_ARRAY, 4)
    .Set(1, 200)
    .Set(3, 400);

try
{
    append.AppendData(writer, new List<object> { 2L, sparse });
}
finally
{
    if (append.IsAppendOpened)
        append.AppendClose(writer);
}
```

빈 `MachSparseArray`는 모든 요소가 NULL인 ARRAY이고 `DBNull.Value`는 배열 전체 NULL입니다.
오버로드와 전체 검증 예제는
Sparse ARRAY와 선택 컬럼 Append API를
참고하십시오.

### Error Delegator 설정

Append 중 행 오류는 위 예제처럼 writer를 연 직후 delegate로 받고, close 뒤 success/failure
건수를 확인합니다.

### 자동 AppendFlush 설정

AppendOpen은 자동 flush 스레드를 시작합니다. 끄려면 이미 열린 writer에 대해
`connection.SetConnectAppendFlush(false)`를 호출합니다. 자동 스레드 오류가 즉시 공개
exception으로 전달되지 않을 수 있으므로 명시 flush·close와 callback/count 확인을 유지합니다.

## 프로토콜 4.0-full 전체 API

`PROTOCOL=4.0-full`을 사용하면 확장된 ADO.NET 표면을 사용할 수 있습니다. 8.0.55 소스
패키지에서 4.0 limited connector는 3.1.3, 4.0-full connector는 3.2.2입니다.
설치된 Linux 패키지는 `$MACHBASE_HOME/lib/` 아래에 net50 flavor만 포함할 수 있으므로,
다른 대상 framework가 필요하면 소스 빌드 또는 NuGet 복원 산출물을 사용하십시오.

- `UniMachNetConnector-net50-8.0.55.dll` – DBMS Standard Linux 패키지에서 흔히 설치되는 universal entry point
- `machNetConnector-40-net50-3.1.3.dll` – 프로토콜 4.0 limited connector
- `machNetConnector-40-net50-3.2.2.dll` – 프로토콜 4.0-full connector

### 4.0-full에서 추가된 주요 타입

- `MachDbProviderFactory`: `Mach.Data` invariant 이름으로 프로바이더를 등록/생성할 수 있습니다.
- `MachConnectionStringBuilder`: 키워드 오타 없이 커넥션 문자열을 구성할 수 있습니다.
- `MachDataAdapter`, `MachRowUpdating`, `MachRowUpdated`: `DataTable`/`DataSet` 기반 워크플로를 지원합니다.
- `MachCommandBuilder`: SELECT 문으로부터 INSERT/DELETE(조건에 따라 UPDATE) 구문을 자동
  생성합니다. 자동 생성 SQL이 대상 테이블의 DML 제약에 맞는지 실행 전에 확인합니다.

### 전체 API 활성화

```csharp
var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
var connString =
    $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();
```

UPDATE/DELETE가 필요한 경우에는 테이블 타입별 조건과 드라이버의 SQL 생성 범위를 함께
확인합니다. LOG는 UPDATE를 지원하지 않습니다. Machbase DBMS 8.7.0 Standard Edition의
TAG UPDATE는 NAME과 BASETIME 조건을 요구하므로 범용 CommandBuilder가 만든 SQL에
의존하지 말고 TAG UPDATE 구문에
맞는 명령과 바인딩을 사용합니다.

### 커넥션 문자열 빌더 사용

```csharp
var builder = new MachConnectionStringBuilder
{
    Server = "127.0.0.1",
    Port = 5656,
    UserID = "SYS",
    Password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
        ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required")
};

builder["PROTOCOL"] = "4.0-full";

using var connection = new MachConnection(builder.ConnectionString);
connection.Open();
```

### 예시: MachDataAdapter로 SQL INSERT

Lookup 테이블을 `DataTable`로 가져와 새 행을 추가하면 command builder가 일반 SQL INSERT를
실행합니다. 이 경로는 Append 프로토콜이 아닙니다.

```csharp
using Mach.Data.MachClient;
using System;
using System.Data;

var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
var connString =
    $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
using var connection = new MachConnection(connString);
connection.Open();

using (var create = new MachCommand(
    "CREATE LOOKUP TABLE dotnet_lookup_demo (id INTEGER PRIMARY KEY, name VARCHAR(80))",
    connection))
{
    create.ExecuteNonQuery();
}

var adapter = new MachDataAdapter(
    "SELECT id, name FROM dotnet_lookup_demo ORDER BY id",
    connection);
var builder = new MachCommandBuilder(adapter);

var table = new DataTable();
adapter.Fill(table);

var newRow = table.NewRow();
newRow["id"] = 2001;
newRow["name"] = "Inserted from MachDataAdapter";
table.Rows.Add(newRow);

adapter.MachRowUpdating += (sender, args) =>
{
    Console.WriteLine(
        $"About to run {args.StatementType} with SQL: {args.Command?.CommandText}");
};

adapter.Update(table);

using var drop = new MachCommand("DROP TABLE dotnet_lookup_demo", connection);
drop.ExecuteNonQuery();
```

> **Tip**: 전송 전 SQL을 확인하려면 위처럼 `Update()` 전에 이벤트를 구독하십시오.

### 예시: DbProviderFactory 활용

`MachDbProviderFactory.Instance`를 사용하면 `DbProviderFactories`, Dapper 등 프로바이더 중립 구성에 Machbase를 연결할 수 있습니다.

```csharp
using System;
using System.Data.Common;
using Mach.Data.MachClient;

DbProviderFactory factory = MachDbProviderFactory.Instance;

using DbConnection connection = factory.CreateConnection()!;
var password = Environment.GetEnvironmentVariable("MACHBASE_PASSWORD")
    ?? throw new InvalidOperationException("MACHBASE_PASSWORD is required");
connection.ConnectionString =
    $"SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD={password};PROTOCOL=4.0-full";
connection.Open();

using DbCommand command = connection.CreateCommand();
command.CommandText = "SELECT COUNT(*) FROM V$TABLES";
var count = (long)command.ExecuteScalar();

Console.WriteLine($"Visible tables: {count}");
```

설정 기반 애플리케이션에서 팩터리를 자동으로 노출하려면 시작 시 `MachDbProviderFactory.Register()`를 한 번 호출해 `DbProviderFactories.GetFactory("Mach.Data")`가 동일한 인스턴스를 반환하도록 구성하십시오.

`4.0-full` 프로토콜은 Machbase 7.x 이상 서버에서만 사용 가능합니다. 더 낮은 버전에서는 `PROTOCOL=4.0`(제한된 기능) 또는 2.x/3.x 프로토콜을 사용해야 합니다.
