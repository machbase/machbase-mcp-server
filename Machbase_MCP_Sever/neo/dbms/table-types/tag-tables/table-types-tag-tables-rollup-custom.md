# Custom Rollup: User-Defined Aggregation

## Overview

Custom Rollup executes a user-defined `SELECT` aggregation query periodically and appends the result into a target TAG table.

It is useful for multi-column aggregation, condition-based aggregation, and hierarchical rollup pipelines.

## Differences from Standard Rollup

| Category | Standard Rollup | Custom Rollup |
|---|---|---|
| Create syntax | `CREATE ROLLUP ... ON table(column)` | `CREATE ROLLUP ... INTO (...) AS (SELECT ...)` |
| Aggregation logic | Engine-defined | User-defined `SELECT` |
| Destination | Internal rollup table | User-created TAG table |
| WHERE location | External `INTERVAL ... WHERE ...` | Internal `SELECT ... WHERE ...` |
| Query pattern | `rollup()` hint path | Query destination table with re-aggregation |
| Metadata type | `v$rollup.ext_type = 0/1` | `v$rollup.ext_type = 2` |

## Execution Model and Re-Aggregation

Custom Rollup stores data as incremental `INSERT INTO <dest> SELECT ...` results.

Multiple partial rows can exist for the same time bucket. Because of this, final queries should re-aggregate by the bucket key.

```sql
SELECT code,
       time,
       SUM(sum_price) / SUM(cnt) AS avg_price
  FROM stock_rollup_1m
 GROUP BY code, time
 ORDER BY time;
```

## Syntax

### Create Custom Rollup

```sql
CREATE ROLLUP <rollup_name>
INTO (<dest_tag_table>)
AS (
  SELECT ...
  FROM <source_tag_table>
  [WHERE ...]
  GROUP BY ...
)
INTERVAL <n> (SEC | MIN | HOUR)
[WAKEUP INTERVAL <m> (SEC | MIN | HOUR)];
```

### Control Commands

```sql
ALTER ROLLUP <rollup_name> START;
ALTER ROLLUP <rollup_name> STOP;
ALTER ROLLUP <rollup_name> FORCE;
DROP ROLLUP <rollup_name>;
```

Note: Rollup worker threads are started automatically after creation. Calling `START` immediately can return an already-started error.

## Validation Rules and Constraints

### Source and Destination Tables

- Only one TAG table is allowed as the source.
- The destination must be a pre-created TAG table.
- Destination `DROP TABLE` is blocked while the rollup exists.

### SELECT Constraints

- The query inside `AS (...)` must be a valid `SELECT`.
- Exactly one table is allowed in `FROM`.
- `JOIN`, `FROM` subqueries, and `ON/USING` are not allowed.
- SELECT text length is limited (internal 1024-based limit).
- Result column count/types must be compatible with the destination table.

### WHERE Constraints

- Internal `WHERE` in `SELECT` is allowed.
- Direct filtering on the source BASETIME column in `WHERE` is rejected.
- External `INTERVAL ... WHERE ...` is not allowed for Custom Rollup syntax.

### Interval Constraints

- `INTERVAL` must be positive.
- If `WAKEUP INTERVAL` is omitted, it defaults to `INTERVAL`.
- `WAKEUP INTERVAL` must be `<= INTERVAL` and must divide `INTERVAL` exactly.

### DATE_BIN Origin Guidance

`DATE_BIN` origin must be a valid DATETIME value. Boundary origins may fail depending on environment/timezone behavior, so use a safe origin value.

## Basic Example

### 1) Source and Destination Tables

```sql
CREATE TAG TABLE stock_tick (
  code      VARCHAR(20) PRIMARY KEY,
  time      DATETIME BASETIME,
  price     DOUBLE,
  volume    DOUBLE,
  bid_price DOUBLE,
  ask_price DOUBLE
);

CREATE TAG TABLE stock_rollup_1m (
  code       VARCHAR(20) PRIMARY KEY,
  time       DATETIME BASETIME,
  sum_price  DOUBLE,
  sum_volume DOUBLE,
  sum_bid    DOUBLE,
  sum_ask    DOUBLE,
  cnt        INTEGER
);
```

### 2) Create Custom Rollup

```sql
CREATE ROLLUP rollup_stock_1m
INTO (stock_rollup_1m)
AS (
  SELECT code,
         DATE_TRUNC('minute', time) AS time,
         SUM(price)                 AS sum_price,
         SUM(volume)                AS sum_volume,
         SUM(bid_price)             AS sum_bid,
         SUM(ask_price)             AS sum_ask,
         COUNT(*)                   AS cnt
    FROM stock_tick
   GROUP BY code, time
)
INTERVAL 1 MIN;
```

### 3) Re-Aggregation Query

```sql
SELECT code,
       time,
       SUM(sum_price)  / SUM(cnt) AS avg_price,
       SUM(sum_volume)            AS total_volume,
       SUM(sum_bid)    / SUM(cnt) AS avg_bid,
       SUM(sum_ask)    / SUM(cnt) AS avg_ask
  FROM stock_rollup_1m
 GROUP BY code, time
 ORDER BY time;
```

## OHLCV Pattern (FIRST/LAST)

When using `FIRST/LAST`, keeping helper time columns (`firsttime`, `lasttime`) improves correctness during re-aggregation.

```sql
SELECT code,
       time,
       FIRST(firsttime, open) AS open,
       MAX(high)              AS high,
       MIN(low)               AS low,
       LAST(lasttime, close)  AS close,
       SUM(volume)            AS volume,
       SUM(cnt)               AS cnt
  FROM stock_candle_1m
 GROUP BY code, time
 ORDER BY code, time;
```

## Hierarchical Pipeline Example (1m -> 10m)

A Custom Rollup destination table can be used as the source of another rollup stage.

```sql
CREATE ROLLUP rollup_stock_candle_10m
INTO (stock_candle_10m)
AS (
  SELECT code,
         DATE_BIN('min', 10, time, TO_DATE('2000-01-01 00:00:00')) AS time,
         MIN(firsttime)         AS firsttime,
         MAX(lasttime)          AS lasttime,
         FIRST(firsttime, open) AS open,
         MAX(high)              AS high,
         MIN(low)               AS low,
         LAST(lasttime, close)  AS close,
         SUM(volume)            AS volume,
         SUM(cnt)               AS cnt
    FROM stock_candle_1m
   GROUP BY code, time
)
INTERVAL 10 MIN;
```

## Metadata Check

```sql
SELECT rollup_table,
       source_table,
       ext_type,
       enabled,
       frequency,
       wakeup_interval,
       predicate
  FROM v$rollup
 WHERE rollup_table = 'ROLLUP_STOCK_1M';
```

- `ext_type = 2`: Custom Rollup
- `predicate`: Custom `SELECT` text

## Operational Notes

- Destination `DROP TABLE` is blocked while the rollup exists.
- If corrected source data requires rebuilding destination buckets, follow [Rollup Rebuild Guide](./rollup-rebuild/).
- Recommended drop order:

```sql
ALTER ROLLUP <name> STOP;
DROP ROLLUP <name>;
DROP TABLE <dest_table>;
DROP TABLE <source_table>;
```

- `DROP TAG TABLE ... CASCADE` removes dependent rollups.
- Custom Rollup destination tables are not auto-dropped and should be removed separately when needed.

## Best Practices

- Standardize result queries as re-aggregation queries.
- Keep `firsttime`/`lasttime` helper columns for FIRST/LAST patterns.
- For destination schema changes, stop/drop/recreate the rollup.
- After correcting anomalous data, rebuild by bucket using delete followed by insert. In rollup-on-rollup pipelines, always rebuild from lower stages first.
- Configure `WAKEUP INTERVAL` explicitly to balance latency and load.