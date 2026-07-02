# Machbase Neo SQL VIEW

## What is a Stored VIEW?

This document describes a **stored VIEW** created with `CREATE VIEW`, not an inline
view written as `FROM (SELECT ...)`.

A VIEW stores a `SELECT` definition as a named logical object so that it can be reused.

* A VIEW does not store data separately.
* When queried, the stored VIEW definition SQL is expanded and executed internally.
* A VIEW can be used as a `SELECT` target like a table, but it is not a physical storage feature.
* The behaviors covered in this document are `CREATE VIEW`, `DROP VIEW`, `SELECT`,
  `DESC`, `SHOW VIEWS`, `M$SYS_VIEWS`, and `EXPLAIN`.

In practice, a VIEW should be understood as "a reusable named query" rather than
"copied data stored in another object".

## Why Use VIEW in Machbase?

VIEW is especially useful in Machbase in the following situations.

* When you want to reuse the same query under a simple name
* When you want to share complex `JOIN`, `GROUP BY`, `CASE`, or `UNION ALL` logic
* When you want to expose decoded `BINARY` values from Tag tables as logical columns
* When you want to inspect metadata and execution plans with `SHOW VIEWS`, `DESC`,
  `M$SYS_VIEWS`, and `EXPLAIN`

The characteristics of the base table still matter under a VIEW.

* VIEWs over Lookup / Volatile tables still depend on efficient primary-key-based predicates.
* VIEWs over Tag tables should still be checked with `name`, `time`, and `EXPLAIN`.
* Because a VIEW reuses the base query and optimizer path, its performance follows the base query.

## Basic Syntax

### Create a VIEW

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

* `view_name` may also be schema-qualified, such as `db.user.view_name`.
* `CREATE OR REPLACE VIEW` replaces the existing VIEW definition.
* If an object with the same name already exists and it is not a VIEW, replacement fails.
* In the currently validated implementation, `CREATE OR REPLACE VIEW` keeps the same object id.
* If validation of the new definition fails, the old VIEW definition remains unchanged.

### Drop a VIEW

```sql
DROP VIEW view_name;
DROP VIEW IF EXISTS view_name;
```

* `DROP VIEW IF EXISTS` succeeds even when the target does not exist.
* If another VIEW depends on the target VIEW, `DROP VIEW` is blocked.
* `DROP TABLE view_name` cannot be used to remove a VIEW.

### Metadata Queries

```sql
SHOW VIEWS;
DESC view_name;

SELECT USER_NAME, DB_NAME, VIEW_NAME, VIEW_SQL
FROM M$SYS_VIEWS;
```

## Basic Examples

The following example shows a simple Lookup-based VIEW.

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

You can also define the exposed column names explicitly.

```sql
CREATE VIEW v_customer_short (cust_id, cust_name) AS
SELECT id, name
FROM customer;

SELECT cust_id, cust_name
FROM v_customer_short
WHERE cust_id = 100;
```

To change an existing VIEW definition, use `CREATE OR REPLACE VIEW`.

```sql
CREATE VIEW v_customer_amount AS
SELECT id, amount
FROM customer;

CREATE OR REPLACE VIEW v_customer_amount AS
SELECT id, amount * 10 AS amount
FROM customer
WHERE id <= 10;
```

## How Column Names Are Determined

### When an Explicit Column List Is Given

```sql
CREATE VIEW v_sales (sales_id, sales_name) AS
SELECT id, name
FROM t_sales;
```

In this case, the official VIEW column names are `sales_id` and `sales_name`.

### When No Explicit Column List Is Given

Column names are determined in the following order.

1. `SELECT` alias
2. Original column name for a simple column reference
3. Auto-generated names such as `EXPR1`, `EXPR2`, ...

```sql
CREATE VIEW v_expr AS
SELECT id,
       name AS user_name,
       val + 10
FROM t1;
```

The resulting column names are in the form of `ID`, `USER_NAME`, and `EXPR3`.

### Column Names in `UNION ALL` VIEWs

A `UNION ALL` VIEW uses the target names from the left-most `SELECT`.

```sql
CREATE VIEW v_union AS
SELECT id FROM t1
UNION ALL
SELECT id FROM t2;
```

Therefore `DESC v_union` shows `ID`, and `SELECT id FROM v_union` works normally.

## Supported VIEW Shapes

The currently validated VIEW shapes include:

* Simple projection and predicates
* Expressions, functions, constants, and `CASE`
* `JOIN`
* VIEWs containing subqueries
* Nested VIEWs
* `GROUP BY`, `HAVING`
* `DISTINCT`
* `UNION ALL`

Examples:

```sql
CREATE VIEW v_expr_case AS
SELECT id,
       CASE WHEN amount >= 100 THEN 'VIP' ELSE 'NORMAL' END AS grade,
       UPPER(city) AS city_upper
FROM customer;
```

```sql
CREATE VIEW v_city_sum AS
SELECT city, SUM(amount) AS total_amount
FROM customer
GROUP BY city
HAVING SUM(amount) >= 100;
```

```sql
CREATE VIEW v_union AS
SELECT id FROM customer WHERE city = 'SEOUL'
UNION ALL
SELECT id FROM customer WHERE city = 'BUSAN';
```

```sql
CREATE VIEW v_nested AS
SELECT id, total_amount
FROM v_city_sum
JOIN (
    SELECT city AS city_name, COUNT(*) AS city_cnt
    FROM customer
    GROUP BY city
) x
ON v_city_sum.city = x.city_name;
```

## Machbase-Specific Examples

### Decoding Tag / BINARY Data

One of the most practical Machbase VIEW patterns is exposing decoded values from
a Tag table `BINARY` column as logical columns.

```sql
CREATE TAG TABLE dam (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    frame BINARY(16)
);

CREATE VIEW damdata AS
SELECT name,
       time,
       extract_bit(frame, 0) AS bit0,
       extract_ulong(frame, 0, 16) AS u16,
       extract_long(frame, 0, 16) AS s16,
       extract_float(frame, 0) AS f32,
       extract_scaled_double(frame, 0, 12, 0, 0.5, 0.5) AS sd12
FROM dam;
```

```sql
SELECT name, time, bit0, u16, s16, f32, sd12
FROM damdata
WHERE name = 'main'
  AND time >= TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
  AND time <  TO_DATE('2024-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS')
ORDER BY time;
```

For this type of VIEW, it is still important to check `name`, `time`, and `EXPLAIN`
just as you would on the base Tag table.

### Schema-Qualified and Quoted Names

VIEW names may be schema-qualified and may also use quoted identifiers.

```sql
CREATE VIEW machbasedb.sys.v_local AS
SELECT id, val
FROM other_user.v_src
WHERE id >= 2;

CREATE VIEW "V_QUOTED" AS
SELECT id, val
FROM t1;

CREATE VIEW v_dep AS
SELECT id
FROM "V_QUOTED"
WHERE val >= 20;
```

## Metadata and Operational Checks

### SHOW VIEWS

`SHOW VIEWS` lists the visible VIEWs and their definition SQL.

The output columns are: `USER_NAME`, `DB_NAME`, `VIEW_NAME`, `VIEW_SQL`.

```sql
SHOW VIEWS;
```

### M$SYS_VIEWS

`M$SYS_VIEWS` is the public metadata interface for checking VIEW definition SQL.

```sql
SELECT USER_NAME, DB_NAME, VIEW_NAME, VIEW_SQL
FROM M$SYS_VIEWS
WHERE VIEW_NAME = 'V_CUSTOMER';
```

### DESC, M$SYS_TABLES, M$SYS_COLUMNS

```sql
DESC v_customer;

SELECT ID, NAME, TYPE
FROM M$SYS_TABLES
WHERE TYPE = 7;

SELECT TABLE_ID, ID, NAME, TYPE, LENGTH
FROM M$SYS_COLUMNS
WHERE TABLE_ID = (
    SELECT ID
    FROM M$SYS_TABLES
    WHERE TYPE = 7
      AND NAME = 'V_CUSTOMER'
);
```

* `DESC` shows the exposed column names and types of the VIEW.
* `M$SYS_TABLES` shows VIEW entries as `TYPE = 7`.
* After `CREATE OR REPLACE VIEW`, `M$SYS_TABLES.ID` is preserved while `M$SYS_VIEWS.VIEW_SQL` is updated.

### EXPLAIN

Because a VIEW does not own physical data, actual performance depends on the base
query and the optimizer path. In production, `EXPLAIN` should be checked first.

```sql
EXPLAIN
SELECT *
FROM v_customer
WHERE id = 3;
```

## Performance and Limits

### Index Usage and Predicate Pushdown

The following cases are more likely to use the base-table index path:

* A simple projection VIEW exposing base columns directly
* A VIEW that only renames columns
* A VIEW with a simple filter where the outer predicate maps directly to base columns

The following cases may fall back to a full scan, so `EXPLAIN` is important:

* An outer predicate on top of a `DISTINCT` VIEW
* A predicate on an expression-derived column such as `id + 1 AS id2`

### VIEW Definition SQL Length Limit

In the current implementation, the VIEW definition SQL after `AS` is supported up to `256KB`.

### Drop and Dependency Rules

* `DROP VIEW` is blocked when a dependent VIEW exists.
* Dependency resolution is based on real referenced objects.
* A name appearing only in a string literal or alias is not treated as a dependency.

## Common Failure Cases

### Column Count Mismatch

```sql
-- Fails: 3 names but SELECT produces 2 columns
CREATE VIEW v_bad (c1, c2, c3) AS
SELECT id, val FROM t1;
```

### Direct Recursive VIEW

```sql
-- Fails: self-reference
CREATE VIEW v_recursive AS
SELECT id FROM v_recursive;
```

### Dropping a VIEW with DROP TABLE

```sql
-- Fails: use DROP VIEW instead
DROP TABLE v_customer;
```

### Reserved Names

```sql
-- Fails: names starting with v$ or _tag are reserved
CREATE VIEW v$bad AS SELECT id FROM t1;
CREATE VIEW _tag_bad AS SELECT id FROM t1;
```
