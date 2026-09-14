# WITH / CTE

공통 테이블 표현식(Common Table Expression, CTE)은 한 SQL 문 안에서 `SELECT` 결과에 이름을
붙여 사용하는 기능입니다. 복잡한 인라인 뷰를 단계별로 분리하거나, 집계 결과를 다른
테이블과 조인할 때 사용합니다.

Machbase 8.7.0 Standard Edition은 비재귀 SELECT CTE를 지원합니다. CTE는 현재 SQL 문에서만
유효하며 별도 데이터베이스 객체로 저장되지 않습니다.

## 지원 범위

| 기능 | 지원 여부 | 설명 |
|---|:---:|---|
| 단일 비재귀 CTE | O | CTE 본문과 주 쿼리는 `SELECT`입니다. |
| 다중 CTE | O | 쉼표로 구분하며, 뒤 CTE가 앞 CTE를 참조할 수 있습니다. |
| 명시적 결과 컬럼명 | O | CTE 이름 뒤에 결과 컬럼 목록을 지정합니다. |
| 중첩 CTE | O | 바깥 CTE는 하위 `SELECT`에서 참조할 수 있습니다. |
| `INSERT SELECT` | O | `INSERT INTO ... WITH ... SELECT` 순서를 사용합니다. |
| VIEW 정의 | O | `CREATE VIEW ... AS WITH ... SELECT`를 사용합니다. |
| prepared statement | O | CTE 본문과 주 `SELECT`에서 `?` 또는 `:name`을 사용할 수 있습니다. |
| EXPLAIN | O | `EXPLAIN`, `EXPLAIN FULL`, `EXPLAIN TRACE`를 지원합니다. |
| `UNION ALL`, PIVOT | O | 기존 `SELECT`의 지원 범위와 제약을 따릅니다. |
| 테이블 유형 | O | LOG, TAG, LOOKUP, VOLATILE, TRANSACTION 테이블을 조회할 수 있습니다. |
| 재귀 CTE | X | `WITH RECURSIVE`, 자기 참조와 상호 재귀를 지원하지 않습니다. |
| 구체화 제어 | X | `MATERIALIZED`, `NOT MATERIALIZED`를 지원하지 않습니다. |
| 데이터 변경 CTE | X | CTE 본문에 DML이나 DDL을 사용할 수 없습니다. |

CTE 본문에서는 JOIN, 집계 함수, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`, `UNION ALL`,
PIVOT을 기존 `SELECT` 규칙에 따라 사용할 수 있습니다. LOG 테이블의 `DURATION`,
`SERIES BY`, 윈도우 함수와 TAG 테이블의 ROLLUP도 기존 규칙을 따릅니다.

Named parameter의 이름 규칙과 SDK별 바인딩 방법은
Named Bind Parameter syntax를 참고하십시오.

## 기본 문법

### SELECT

```sql
WITH cte_name [(column_name [, ...])] AS (
    select_statement
)
[, cte_name [(column_name [, ...])] AS (select_statement) ...]
select_statement;
```

### 기본 문법 INSERT SELECT

```sql
INSERT INTO target_table [(target_column [, ...])]
WITH cte_name [(column_name [, ...])] AS (
    select_statement
)
[, cte_name [(column_name [, ...])] AS (select_statement) ...]
select_statement;
```

`INSERT SELECT`에서는 `WITH` 절을 대상 테이블과 대상 컬럼 목록 뒤에 작성합니다.
다른 DBMS에서 사용하는 문장 선두의 `WITH ... INSERT INTO ...` 형식은 지원하지 않습니다.

### VIEW

```sql
CREATE [OR REPLACE] VIEW view_name AS
WITH cte_name [(column_name [, ...])] AS (
    select_statement
)
[, cte_name [(column_name [, ...])] AS (select_statement) ...]
select_statement;
```

### 기본 문법 EXPLAIN

```sql
EXPLAIN [FULL | TRACE]
WITH cte_name [(column_name [, ...])] AS (
    select_statement
)
[, cte_name [(column_name [, ...])] AS (select_statement) ...]
select_statement;
```

## 기본 사용법

다음 예제는 현재 사용자가 아래 테이블을 소유한다고 가정합니다.

| 테이블 | 종류 | 사용 컬럼 |
|---|---|---|
| `sensor_data` | LOG | `name`, `device_id`, `time`, `value` |
| `device_info` | TRANSACTION | `device_id`, `device_name` |
| `device_summary` | LOG | `device_id`, `sample_count`, `avg_value` |

### 조회 결과에 이름 지정

```sql
WITH recent_data AS (
    SELECT name, time, value
    FROM sensor_data
    WHERE time >= NOW - 10m
)
SELECT name, time, value
FROM recent_data
ORDER BY time DESC;
```

최종 출력 순서를 보장하려면 주 `SELECT`에 `ORDER BY`를 지정합니다. CTE 본문의
`ORDER BY`만으로 바깥 결과의 순서는 보장되지 않습니다.

### 집계 결과 조인

```sql
WITH top_devices AS (
    SELECT device_id,
           AVG(value) AS avg_value
    FROM sensor_data
    WHERE time >= NOW - 1h
    GROUP BY device_id
    ORDER BY avg_value DESC
    LIMIT 10
)
SELECT d.device_id,
       d.device_name,
       t.avg_value
FROM device_info d
JOIN top_devices t
  ON d.device_id = t.device_id
ORDER BY t.avg_value DESC;
```

대량 시계열 데이터를 먼저 집계하고 결과 건수를 제한한 뒤 기준정보와 조인할 때 사용할 수
있습니다.

### 여러 CTE 연결

```sql
WITH recent_data AS (
    SELECT device_id, value
    FROM sensor_data
    WHERE time >= NOW - 30m
),
device_avg AS (
    SELECT device_id, AVG(value) AS avg_value
    FROM recent_data
    GROUP BY device_id
)
SELECT device_id, avg_value
FROM device_avg
WHERE avg_value >= 80;
```

`device_avg`는 앞에서 선언한 `recent_data`를 참조할 수 있습니다. 앞 CTE가 뒤 CTE를
참조하는 전방 참조는 지원하지 않습니다.

### 결과 컬럼명 지정

```sql
WITH device_stat (id, sample_count, average_value) AS (
    SELECT device_id, COUNT(*), AVG(value)
    FROM sensor_data
    GROUP BY device_id
)
SELECT id, sample_count, average_value
FROM device_stat;
```

명시한 컬럼 수는 CTE 본문의 결과 컬럼 수와 같아야 하며 컬럼명을 중복해서 지정할 수
없습니다. 컬럼 목록을 생략하면 `SELECT` alias와 인라인 뷰의 컬럼 이름 결정 규칙을
따릅니다.

## 사용할 수 있는 SQL 문맥

### 하위 SELECT

```sql
WITH active_devices AS (
    SELECT device_id
    FROM sensor_data
    WHERE time >= NOW - 1m
)
SELECT d.device_id, d.device_name
FROM device_info d
WHERE d.device_id IN (
    SELECT device_id
    FROM active_devices
);
```

바깥 `SELECT`에 선언한 CTE는 스칼라 서브쿼리, `IN (subquery)`, 인라인 뷰 등의 하위
`SELECT`에서 참조할 수 있습니다. JOIN `ON` 조건의 스칼라 서브쿼리와
`IN (subquery)` 같은 기존 `SELECT` 제약은 CTE를 사용해도 변경되지 않습니다.

### 사용할 수 있는 SQL 문맥 INSERT SELECT

```sql
INSERT INTO device_summary
WITH hourly_summary AS (
    SELECT device_id,
           COUNT(*) AS sample_count,
           AVG(value) AS avg_value
    FROM sensor_data
    WHERE time >= NOW - 1h
    GROUP BY device_id
)
SELECT device_id, sample_count, avg_value
FROM hourly_summary;
```

CTE는 결과 행을 만들며, 실제 입력 가능 여부와 중복 키 처리는 대상 테이블의 기존
`INSERT SELECT` 규칙을 따릅니다. CTE를 사용한다고 대상 테이블의 제약이나 원자성 범위가
변경되지는 않습니다.

### VIEW 정의

```sql
CREATE VIEW active_device_summary AS
WITH recent_data AS (
    SELECT device_id, value
    FROM sensor_data
    WHERE time >= NOW - 10m
)
SELECT device_id,
       COUNT(*) AS sample_count,
       AVG(value) AS avg_value
FROM recent_data
GROUP BY device_id;
```

VIEW에는 CTE를 포함한 `SELECT` 정의가 저장되며, 조회 시 해당 정의가 다시 해석됩니다.
`CREATE OR REPLACE VIEW`에도 같은 문법을 사용할 수 있습니다.

VIEW 정의에는 바인드 매개변수(`?`)를 사용할 수 없습니다. 실행 시마다 달라지는 조건은
VIEW를 조회하는 `SELECT`에 작성합니다.

### 사용할 수 있는 SQL 문맥 EXPLAIN

```sql
EXPLAIN FULL
WITH recent_data AS (
    SELECT name, time, value
    FROM sensor_data
    WHERE time >= NOW - 5m
)
SELECT *
FROM recent_data
WHERE name = 'sensor-01';
```

`EXPLAIN`, `EXPLAIN FULL`, `EXPLAIN TRACE`로 CTE가 전개된 뒤 실제 테이블에 적용되는 스캔,
필터와 JOIN 계획을 확인합니다.

### Prepared statement

CTE 본문과 주 `SELECT`에서 바인드 매개변수(`?`)를 사용할 수 있습니다.

```sql
WITH selected_data AS (
    SELECT device_id, time, value
    FROM sensor_data
    WHERE device_id = ?
)
SELECT device_id, time, value
FROM selected_data
WHERE value >= ?;
```

참조하지 않는 CTE의 바인드 매개변수도 문장의 매개변수로 등록되므로 값을 바인드해야
합니다. 같은 CTE를 여러 번 참조하더라도 원래 CTE 본문의 매개변수 개수가 참조 횟수만큼
늘어나지는 않습니다.

## 이름과 유효 범위

### 선언 순서

뒤 CTE는 앞 CTE를 참조할 수 있습니다. 전방 참조, 자기 참조와 CTE 간 상호 참조는 지원하지
않습니다.

### 실제 테이블과 이름이 같은 경우

한정하지 않은 이름이 CTE와 실제 TABLE 또는 VIEW에 모두 존재하면 현재 유효 범위의 CTE가
우선합니다.

```sql
WITH device_info AS (
    SELECT device_id
    FROM sensor_data
)
SELECT *
FROM device_info;
```

실제 테이블을 선택하려면 `user_name.device_info`처럼 소유자를 명시합니다. 소유자를 명시한
이름은 CTE가 아니라 실제 TABLE 또는 VIEW를 찾습니다.

### 중첩 범위

바깥 CTE는 안쪽 `SELECT`에서 참조할 수 있습니다. 안쪽 `SELECT`에 선언한 CTE는 바깥에서
참조할 수 없으며, 안쪽 CTE가 바깥 CTE와 같은 이름이면 안쪽 CTE가 우선합니다.

## 실행 특성과 성능

Machbase는 CTE 참조를 기존 인라인 뷰 형태로 전개하여 계획합니다. CTE 결과가 임시 테이블에
구체화되거나 한 번만 평가된다고 보장하지 않습니다.

같은 CTE를 여러 번 참조하면 각 참조가 별도로 계획되고 실행될 수 있습니다.

```sql
WITH recent_data AS (
    SELECT device_id, time, value
    FROM sensor_data
    WHERE time >= NOW - 1d
)
SELECT a.device_id, a.value, b.value
FROM recent_data a
JOIN recent_data b
  ON a.device_id = b.device_id
 AND a.time = b.time;
```

성능을 관리할 때는 다음 기준을 적용합니다.

- 대량 테이블을 읽는 CTE를 반복해서 참조하지 않습니다.
- 시간, TAG 이름과 키 조건 등 선택도를 높이는 조건을 CTE 본문에 가능한 한 일찍 적용합니다.
- 필터 pushdown이나 CTE 결과의 자동 재사용을 전제로 성능을 예측하지 않습니다.
- 반복 참조가 필요하면 쿼리를 분리하거나 실제 저장 객체 사용을 검토합니다.
- `EXPLAIN`으로 각 참조의 실제 실행 계획을 확인합니다.

`MATERIALIZED`와 `NOT MATERIALIZED`를 지원하지 않으므로 CTE 평가 방식을 사용자가 강제할 수
없습니다.

### CTE 확장 한도

한 SQL 문에서 CTE 전개 과정으로 생성되는 `SELECT` 단위는 최대 1,024개입니다. 이는 선언할
수 있는 CTE 이름의 개수가 아니라, 다중 참조와 연쇄 참조를 모두 전개한 `SELECT` 단위의
합계입니다.

한도를 초과하면 다음 오류가 발생합니다.

```text
CTE expansion limit exceeded
```

오류가 발생하면 반복 다중 참조 체인을 줄이거나 중간 결과를 별도 테이블 또는 VIEW로
분리합니다.

## 제한사항

다음 기능은 지원하지 않습니다.

- `WITH RECURSIVE`와 재귀 CTE
- `RECURSIVE` 키워드를 생략한 자기 참조 및 CTE 간 상호 재귀
- 전방 참조
- `MATERIALIZED`, `NOT MATERIALIZED`
- 재귀 CTE 문법의 `SEARCH DEPTH FIRST`, `SEARCH BREADTH FIRST`, `CYCLE`
- 문장 선두의 `WITH ... INSERT`, `WITH ... UPDATE`, `WITH ... DELETE`, `WITH ... MERGE`
- CTE 본문의 INSERT, UPDATE, DELETE, MERGE 또는 DDL
- `UNION`, `INTERSECT`, `EXCEPT`
- `FROM` 절 없는 리터럴 `SELECT`끼리의 `UNION ALL`
- `EXISTS` 식
- CTE 본문의 INTERPOLATION 힌트와 `FREQUENCY`
- 사용자 정의 `CREATE ROLLUP ... AS (...)` 쿼리의 CTE

CTE 본문의 INTERPOLATION 힌트는 기존 인라인 뷰 제한과 동일하게 다음 오류를 반환합니다.

```text
ERR-02304: Interpolation is not applicable on (INLINE-VIEW).
```

CTE는 테이블 유형별 DML 기능을 확장하지 않습니다. LOG, TAG, LOOKUP, VOLATILE과 TRANSACTION
테이블의 조회 및 입력은 각 테이블의 기존 규칙을 따릅니다.

## 오류 확인

| 상황 | 확인할 내용 |
|---|---|
| CTE 이름 중복 | 같은 `WITH` 절에서 이름을 한 번만 선언했는지 확인합니다. |
| 컬럼 개수 불일치 | 명시한 CTE 컬럼 수와 `SELECT` 결과 컬럼 수를 맞춥니다. |
| 컬럼 이름 중복 | 명시적 컬럼 목록에서 중복 이름을 제거합니다. |
| 전방 참조 | 참조 대상 CTE를 먼저 선언합니다. |
| 자기 참조 | 재귀 구조를 제거하거나 고정 깊이 SQL 또는 애플리케이션 반복으로 변경합니다. |
| 테이블을 찾을 수 없음 | 한정 이름이 CTE가 아닌 실제 TABLE/VIEW를 찾는지 확인합니다. |
| 확장 한도 초과 | 반복 참조 체인을 줄이거나 중간 결과를 별도 객체로 분리합니다. |
| VIEW bind 오류 | VIEW 정의와 CTE에서 `?`를 제거하고 조회 시 조건으로 옮깁니다. |
| 문법 오류 | 지원하지 않는 재귀, 구체화 또는 문장 선두 `WITH ... DML` 문법인지 확인합니다. |

## 다른 DBMS에서 이전

| 원본 DBMS 기능 | Machbase에서의 처리 |
|---|---|
| PostgreSQL/MySQL의 `WITH RECURSIVE` | 고정 깊이 SQL 또는 애플리케이션 반복으로 변경합니다. |
| PostgreSQL/SQLite의 `MATERIALIZED` | 키워드를 제거하고 한 번 평가된다고 가정하지 않습니다. |
| PostgreSQL/SQLite의 `NOT MATERIALIZED` | 키워드를 제거하고 실제 계획을 `EXPLAIN`으로 확인합니다. |
| Oracle의 재귀 subquery factoring | 자기 참조를 제거한 비재귀 CTE만 이전합니다. |
| SQL Server의 `WITH ... UPDATE/DELETE/MERGE` | CTE와 DML을 분리하고 테이블별 DML 규칙을 적용합니다. |
| 재귀 CTE의 `SEARCH` 또는 `CYCLE` | 경로와 cycle 검사를 애플리케이션이나 저장 컬럼으로 처리합니다. |

## 관련 문서

- SELECT syntax
- DML syntax
- VIEW syntax
- 집합 연산자
- PIVOT syntax
- 윈도우 함수와 OVER
- 쿼리 분석과 EXPLAIN
