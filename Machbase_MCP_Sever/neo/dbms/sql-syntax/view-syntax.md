# VIEW

VIEW는 `SELECT` 결과를 이름 있는 논리 객체로 저장해 재사용하는 기능입니다. 데이터를 별도로 저장하지 않으며, 조회 시 저장된 정의 SQL이 내부적으로 다시 전개되어 실행됩니다.

## CREATE VIEW

```sql
CREATE VIEW view_name AS
SELECT ...
FROM ...;
```

```sql
CREATE VIEW view_name (col1, col2, ...) AS
SELECT ...
FROM ...;
```

```sql
CREATE OR REPLACE VIEW view_name AS
SELECT ...
FROM ...;
```

Standard Edition에서는 VIEW 정의의 `SELECT` 앞에 비재귀 CTE를 선언할 수 있습니다.

```sql
CREATE VIEW view_name AS
WITH cte_name AS (
    SELECT ...
    FROM ...
)
SELECT ...
FROM cte_name;
```

- `CREATE OR REPLACE VIEW`는 기존 VIEW 정의를 교체합니다. 교체 대상이 VIEW가 아닌 객체이면 오류를 반환합니다.
- 컬럼 리스트를 명시하면 해당 이름이 VIEW의 공식 컬럼명이 됩니다. 생략하면 alias 또는 원본 컬럼명이 사용됩니다.
- `view_name`은 `db.user.view_name` 형태의 schema-qualified 이름도 사용할 수 있습니다.

### 기본 예시

```sql
CREATE LOOKUP TABLE customer (
    id INTEGER PRIMARY KEY,
    name VARCHAR(20),
    city VARCHAR(20),
    amount INTEGER
);

CREATE VIEW v_customer AS
SELECT id, name, city, amount
FROM customer;

SELECT name, city
FROM v_customer
WHERE id = 100;
```

### 컬럼 이름 명시

```sql
CREATE VIEW v_customer_short (cust_id, cust_name) AS
SELECT id, name
FROM customer;
```

### 기존 VIEW 정의 교체

```sql
CREATE OR REPLACE VIEW v_customer_amount AS
SELECT id, amount * 10 AS amount
FROM customer
WHERE id <= 10;
```

### CTE를 포함한 VIEW

```sql
CREATE VIEW v_customer_city_summary AS
WITH city_summary AS (
    SELECT city, COUNT(*) AS customer_count, SUM(amount) AS total_amount
    FROM customer
    GROUP BY city
)
SELECT city, customer_count, total_amount
FROM city_summary;
```

VIEW 정의에는 바인드 매개변수(`?`)를 사용할 수 없습니다. 실행할 때마다 달라지는 조건은
VIEW를 조회하는 `SELECT`에 작성합니다.

## VIEW 사용자 컨텍스트

Machbase 8.7.0부터 VIEW 내부에서 `CURRENT_*`와 `SESSION_*` 함수를 사용해 definer와 caller를
구분할 수 있습니다. 다음 예제에서 `VIEW_OWNER`는 VIEW를 만들고, `VIEW_CALLER`는 부여받은
권한으로 조회합니다.

```sql
CONNECT sys/manager;
CREATE USER view_owner IDENTIFIED BY 'VIEW_OWNER';
CREATE USER view_caller IDENTIFIED BY 'VIEW_CALLER';

CONNECT view_owner/VIEW_OWNER;
CREATE LOOKUP TABLE user_context_source (id INTEGER PRIMARY KEY);
INSERT INTO user_context_source VALUES (1);

CREATE VIEW v_user_context AS
SELECT CURRENT_USER() AS current_name,
       SESSION_USER() AS session_name,
       CURRENT_USER_ID() AS current_id,
       SESSION_USER_ID() AS session_id
  FROM user_context_source;

CONNECT sys/manager;
GRANT SELECT ON view_owner.v_user_context TO view_caller;

CONNECT view_caller/VIEW_CALLER;
SELECT current_name,
       session_name,
       CASE WHEN current_id <> session_id THEN 'DIFF' ELSE 'SAME' END AS id_context
  FROM view_owner.v_user_context;
```

```text
CURRENT_NAME  SESSION_NAME  ID_CONTEXT
VIEW_OWNER    VIEW_CALLER   DIFF
```

VIEW 내부의 `CURRENT_*`는 VIEW owner를 반환하고, `SESSION_*`는 연결한 caller를 반환합니다.
일반 SQL에서는 두 계열이 같은 사용자를 반환합니다. 함수 계약은
사용자 컨텍스트 함수를 참고합니다.

```sql
CONNECT view_owner/VIEW_OWNER;
DROP VIEW v_user_context;
DROP TABLE user_context_source;

CONNECT sys/manager;
DROP USER view_caller;
DROP USER view_owner;
```

## DROP VIEW

```sql
DROP VIEW view_name;
DROP VIEW IF EXISTS view_name;
```

- `DROP VIEW IF EXISTS`는 대상이 없어도 오류 없이 통과합니다.
- 다른 VIEW가 해당 VIEW를 참조하고 있으면 삭제가 차단됩니다.
- `DROP TABLE view_name`으로 VIEW를 삭제할 수 없습니다.

## 메타 확인

```sql
SHOW VIEWS;
DESC view_name;

SELECT USER_NAME, DB_NAME, VIEW_NAME, VIEW_SQL
FROM M$SYS_VIEWS
WHERE VIEW_NAME = 'V_CUSTOMER';
```

- `M$SYS_TABLES`에서 VIEW는 `TYPE = 7`로 확인할 수 있습니다.

## 지원되는 VIEW 형태

| 형태 | 지원 여부 |
|------|-----------|
| 단순 projection과 predicate | O |
| expression, 함수, 상수, CASE | O |
| JOIN | O |
| subquery 포함 | O |
| nested VIEW | O |
| GROUP BY, HAVING | O |
| DISTINCT | O |
| UNION ALL | O |

## Tag / BINARY 컬럼 활용 예시

TAG 테이블의 `BINARY` 컬럼을 `extract_*()` 함수로 해석해 논리 컬럼처럼 노출하는 패턴입니다.

```sql
CREATE TAG TABLE dam (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    frame BINARY(16)
);

CREATE VIEW damdata AS
SELECT name,
       time,
       extract_bit(frame, 0)                         AS bit0,
       extract_ulong(frame, 0, 16)                   AS u16,
       extract_float(frame, 0)                       AS f32,
       extract_scaled_double(frame, 0, 12, 0, 0.5, 0.5) AS sd12
FROM dam;

SELECT name, time, bit0, u16, f32, sd12
FROM damdata
WHERE name = 'main'
  AND time >= TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
  AND time <  TO_DATE('2024-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS')
ORDER BY time;
```

## 제한사항

- VIEW 정의 SQL(`SELECT` 본문)은 최대 256KB까지 지원됩니다.
- VIEW는 데이터를 별도로 저장하지 않으므로, 성능은 원본 조회식과 옵티마이저 판단에 의존합니다.
- `DISTINCT`, 계산식 컬럼 기반 predicate는 full scan으로 처리될 수 있으므로 `EXPLAIN`으로 확인이 필요합니다.
- 재귀 VIEW(자기 자신을 참조하는 VIEW)는 지원하지 않습니다.

## 관련 문서

- SELECT syntax — FROM 절에서 VIEW 사용
- WITH / CTE syntax — CTE를 포함한 VIEW 정의
