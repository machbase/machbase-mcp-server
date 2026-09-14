# Named Bind Parameter

Named Bind Parameter는 SQL의 값 위치에 `:name` 형식의 이름을 지정하고 실행할 때 값을
바인딩하는 기능입니다. 반복되는 파라미터의 의미를 이름으로 표현할 수 있어 SQL과
애플리케이션 코드의 대응 관계를 명확하게 유지할 수 있습니다.

```sql
SELECT ID, NAME
FROM SENSOR_DATA
WHERE ID = :id;
```

## 이름 문법

Named marker는 다음 형식을 사용합니다.

```text
:[A-Za-z_$][A-Za-z0-9_$]*
```

| 구분 | 예 |
|---|---|
| 유효한 이름 | `:id`, `:sensor_id`, `:value2`, `:_from_time`, `:select` |
| 유효하지 않은 이름 | `:1id`, `:`, `::id` |

여러 SDK에서 같은 SQL을 공유하려면 `[A-Za-z][A-Za-z0-9_]*` 형식의 이름을 사용하는
것이 좋습니다.

파라미터 이름은 대소문자를 구분합니다. 따라서 `:VALUE`, `:value`, `:VaLuE`는 서로
다른 이름입니다. .NET의 `MachParameterCollection`은 기존 provider 호환을 위해 이름을
대소문자 구분 없이 찾습니다.

## 사용할 수 있는 위치

Named marker는 값이나 표현식이 들어가는 위치에 사용합니다.

```sql
SELECT ID, NAME, VALUE
FROM SENSOR_DATA
WHERE CREATED_AT >= :from_time
  AND CREATED_AT < :to_time
  AND VALUE >= :minimum_value
ORDER BY CREATED_AT
LIMIT :row_count OFFSET :start_row;
```

다음과 같은 식별자나 SQL 구조는 파라미터로 대체할 수 없습니다.

```sql
SELECT * FROM :table_name;               -- 사용할 수 없음
SELECT :column_name FROM SENSOR_DATA;     -- 컬럼 식별자 대체가 아님
SELECT * FROM SENSOR_DATA ORDER BY ID :direction; -- 사용할 수 없음
```

동적 식별자가 필요하면 애플리케이션에서 허용 목록을 검사한 뒤 SQL을 구성합니다.

문자열과 SQL 주석 안의 콜론은 파라미터로 인식하지 않습니다.

```sql
SELECT ':not_a_parameter'
FROM SENSOR_DATA
WHERE ID = :id /* :ignored */;
```

## 파라미터 발생 순서

파라미터 개수는 고유 이름 수가 아니라 SQL에 나타난 횟수로 계산합니다. 다음 SQL에는
`target`이라는 이름이 두 번 나타나므로 파라미터가 두 개입니다.

```sql
SELECT ID, NAME
FROM SENSOR_DATA
WHERE ID = :target
   OR PARENT_ID = :target;
```

- `SQLNumParams()`는 `2`를 반환합니다.
- ordinal API는 첫 번째와 두 번째 위치를 각각 바인딩합니다.
- 이름 기반 API는 `target` 값 하나를 이름이 같은 두 위치에 모두 적용합니다.
- 파라미터 메타데이터에는 각 위치가 별도 항목으로 나타납니다.

한 SQL 문에 사용할 수 있는 파라미터 발생 횟수는 최대 256개입니다.

## Positional marker와의 관계

저수준 ordinal API는 `?`와 `:name`을 SQL에 나타난 순서대로 바인딩할 수 있습니다.
이름, 객체 또는 매핑 기반 API는 anonymous marker인 `?`와 named marker를 함께 사용하면
오류를 반환합니다. 한 SQL 문에서는 한 종류의 marker를 사용하십시오.

| 방식 | SQL marker | 바인딩 |
|---|---|---|
| Positional | `?` | SQL 출현 순서의 1-based ordinal |
| Named SQL과 ordinal API | `:name` | SQL 출현 순서의 1-based ordinal |
| Named API | `:name` | 파라미터 이름 |

## DML 사용 예

Named Bind Parameter는 기존 Prepared Statement와 같은 타입 규칙을 사용합니다.

```sql
INSERT INTO SENSOR_DATA
    (ID, PARENT_ID, NAME, VALUE, CREATED_AT)
VALUES
    (:id, :parent_id, :name, :value, :created_at);
```

Named Bind Parameter는 테이블별 DML 정책이나 Edition 제약을 변경하지 않습니다.
지원되는 DML과 조건은 DML syntax 및
지원 범위와 제약을 참고하십시오.

Standard Edition과 Cluster Edition은 같은 `:name` 문법과 ordinal 규칙을 사용합니다.
실제로 실행할 수 있는 SQL과 테이블 타입은 각 Edition의 기존 지원 범위를 따릅니다.

### TAG data UPDATE에서 사용

Machbase 8.7.0부터 Standard Edition의 TAG data UPDATE는 `WHERE` 절의 NAME과 BASETIME
조건 값에 named marker를 사용할 수 있습니다.

```sql
UPDATE sensor_tag
   SET value = :value,
       status = :status,
       note = :note
 WHERE name = :name
   AND time = :time;
```

같은 prepared statement를 다시 실행할 때 SET, NAME, TIME 값을 새로 바인딩할 수 있습니다.
일치하는 행이 없으면 affected rows `0`으로 성공합니다. bind 사용 여부와 관계없이 태그 선택
조건과 BASETIME 조건은 모두 필요하고, SET 대상 컬럼 제약도 그대로 적용됩니다.

지원되는 조건 형태와 parameter metadata는
TAG data UPDATE를
참고하십시오.

## CTE에서 사용

Standard Edition에서는 CTE 본문과 주 `SELECT`에서 Named Bind Parameter를 사용할 수
있습니다.

```sql
WITH FILTERED AS (
    SELECT ID, NAME, VALUE
    FROM SENSOR_DATA
    WHERE ID > :minimum_id
      AND NAME = :label
)
SELECT ID, NAME, VALUE
FROM FILTERED
WHERE ID = :target_id
ORDER BY ID;
```

위 SQL의 파라미터 ordinal은 `minimum_id`, `label`, `target_id` 순서입니다. CTE의 지원
범위와 Standard Edition 제약은 WITH / CTE syntax를 참고하십시오.

## NULL과 데이터 타입

NULL은 각 SDK의 표준 NULL 값 또는 indicator를 사용해 전달합니다.

| SDK | NULL 값 |
|---|---|
| Machbase SQLCLI | indicator의 `SQL_NULL_DATA` |
| ODBC | indicator의 `SQL_NULL_DATA` |
| JDBC | `null` |
| Node.js/TypeScript | `null` |
| Python | `None` |
| .NET | `DBNull.Value` |

`column = :value`에 NULL을 바인딩해도 `column IS NULL`과 같은 조건이 되지 않습니다.
NULL을 검색하려면 SQL의 NULL 비교 규칙에 따라 `IS NULL`을 사용합니다.

`INTEGER`, `VARCHAR`, `DOUBLE`, `DECIMAL`, `NUMERIC`, `DATETIME` 등 기존 Prepared
Statement 데이터 타입을 사용할 수 있습니다. `DECIMAL` 또는 `NUMERIC`의 정밀도를
보존하려면 SDK의 decimal 타입이나 문자열 표현을 사용하십시오.

## SDK별 바인딩 방식

| SDK 또는 도구 | 이름 기반 사용 방식 |
|---|---|
| Machbase SQLCLI | `SQLBindParameterByName()`, `SQLBindParameterByNameW()` |
| ODBC | `:name` SQL을 `SQLBindParameter()` ordinal로 바인딩 |
| JDBC | `MachPreparedStatement.setObject(String name, Object value)` |
| Node.js/TypeScript | 배열은 positional, 객체는 named 입력 |
| Python DB-API | mapping 전달. 2.4 prepared cursor는 `:name`과 `%(name)s`를 호출 간 재사용 |
| .NET | `MachCommand.Parameters.AddWithValue(":name", value)` |
| Go native | `api.Named("name", value)` |
| Go `database/sql` | `sql.Named("name", value)` |
| machsql | SQL은 `:name`, 값은 `$1`, `$2` 순서로 지정 |

자세한 API와 오류 처리는 개발 도구 연동과
machsql 명령/옵션 사전을 참고하십시오.

## 호환성과 오류

Machbase 8.7.0의 이름 기반 SDK API를 사용하려면 해당 기능을 지원하는 클라이언트와 서버가
모두 필요합니다. 이전 버전과 함께 사용해야 하면 `?`와 ordinal API를 사용하십시오.

| 상황 | 대표 오류 |
|---|---|
| 필요한 이름이 누락됨 | missing parameter |
| SQL에 없는 이름을 전달함 | unknown 또는 extra parameter |
| named와 positional 방식을 혼용함 | sequence 또는 mixed error |
| 값 타입이 SQL 타입과 맞지 않음 | type 또는 conversion error |
| 이름 기반 API를 이전 서버에 사용함 | unsupported |

운영 코드에서는 오류 문자열보다 SQLSTATE, 오류 코드와 예외 타입을 우선 확인하십시오.
버전 조합별 동작과 SDK별 오류 코드는
클라이언트/서버 프로토콜 호환성을
참고하십시오.
