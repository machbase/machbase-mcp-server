# Machbase Neo SQL Rollup

## Introduction

Querying large-scale time-series datasets for statistical aggregates presents significant performance challenges. Performing aggregations over extensive time ranges or the entire dataset can be computationally expensive and time-consuming. Machbase addresses this through its Rollup feature, a specialized mechanism designed to optimize statistical analysis on time-series data stored within TAG tables. Rollup tables automatically pre-aggregate data at defined time granularities, enabling rapid retrieval of common statistical metrics.

## Core Concepts

A **Rollup Table** in Machbase is a derived table that stores pre-calculated aggregate data originating from a source TAG table or another Rollup table. This pre-aggregation process is managed internally by Machbase, significantly reducing the overhead associated with on-the-fly statistical computations during query execution.

### Supported Aggregations

Rollup tables intrinsically support the following standard aggregate functions:
*   `MIN()`: Minimum value within the interval.
*   `MAX()`: Maximum value within the interval.
*   `SUM()`: Sum of values within the interval.
*   `COUNT()`: Count of data points within the interval.
*   `AVG()`: Average of values within the interval.
*   `SUMSQ()`: Sum of the squares of values within the interval.

### Extended Aggregations (Optional)

By utilizing the `EXTENSION` keyword during creation, Rollup tables can additionally support:
*   `FIRST()`: The first recorded value within the interval.
*   `LAST()`: The last recorded value within the interval.

### Time Granularity

Rollup aggregation operates based on fixed time intervals, specifically:
*   Seconds (`SEC`)
*   Minutes (`MIN`)
*   Hours (`HOUR`)

Queries utilizing the Rollup mechanism can request aggregates based on these fundamental units or multiples thereof, including larger conceptual units like days, weeks, months, or years, which are internally mapped to the appropriate base Rollup table (typically HOUR-based for intervals >= 1 day).

## Rollup Table Types

Machbase provides two primary methods for creating and managing Rollup tables:

### Default Rollup

*   Automatically generated when a TAG table is created using the `WITH ROLLUP` clause.
*   Creates a standard hierarchy of Rollup tables (Second, Minute, Hour), depending on the specified minimum granularity. For instance, `WITH ROLLUP (MIN)` creates Minute and Hour Rollups. `WITH ROLLUP` or `WITH ROLLUP (SEC)` creates Second, Minute, and Hour Rollups.
*   Rollup table names are automatically derived from the source TAG table name (e.g., `_mytag_ROLLUP_SEC`).
*   Only one set of Default Rollup tables can exist per TAG table.

### Custom Rollup

*   Manually created by the user using the `CREATE ROLLUP` statement.
*   Allows specification of custom aggregation intervals (e.g., 10 seconds, 5 minutes).
*   Can be based on a TAG table or another Custom Rollup table, enabling multi-level aggregation hierarchies.
*   Provides flexibility in defining specific aggregation needs beyond the default granularities.

## Creating Rollup Tables

### Default Rollup Creation

Default Rollup tables are created implicitly during TAG table definition.

Important: TAG tables must consist of exactly 3 columns: name, time, and value.
- name: Tag identifier (VARCHAR, PRIMARY KEY)
- time: Timestamp (DATETIME BASETIME)  
- value: Measured value (numeric datatype, SUMMARIZED - target for rollup aggregation)

Additional columns are not allowed. To store multiple types of sensor values, 
you must create separate TAG tables for each value type.

**Syntax:**

```sql
CREATE TAG TABLE table_name (
    name datatype PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE [SUMMARIZED]
    [, additional_columns...]
)
WITH ROLLUP [ ( SEC | MIN | HOUR ) ] [ EXTENSION ];
```

*   `SEC | MIN | HOUR`: Specifies the finest granularity required. If omitted, `SEC` is assumed. Higher granularities (MIN, HOUR) are automatically included based on the specified unit (e.g., `MIN` includes `HOUR`).
*   `EXTENSION`: Optional keyword to enable `FIRST()` and `LAST()` aggregate functions.

**Examples:**

Create SEC, MIN, HOUR Rollups:

```sql
CREATE TAG TABLE sensor_data (...) WITH ROLLUP;
```

Create MIN, HOUR Rollups:

```sql
CREATE TAG TABLE hourly_stats (...) WITH ROLLUP (MIN);
```

Create HOUR Rollup only:

```sql
CREATE TAG TABLE daily_summary (...) WITH ROLLUP (HOUR);
```

Create SEC, MIN, HOUR Rollups with FIRST/LAST support:

```sql
CREATE TAG TABLE detailed_sensor_data (...) WITH ROLLUP EXTENSION;
```

### Custom Rollup Creation

Custom Rollup tables are created explicitly using a dedicated DDL statement.

**Syntax:**

```sql
CREATE ROLLUP rollup_name
ON source_table_or_rollup_name ( source_value_column )
INTERVAL interval_value ( SEC | MIN | HOUR )
[ EXTENSION ];
```

*   `rollup_name`: User-defined name for the new Rollup table.
*   `source_table_or_rollup_name`: The name of the source TAG table or an existing Rollup table.
*   `source_value_column`: The numeric column in the source table to be aggregated. (Omitted if the source is another Rollup table).
*   `interval_value`: The numeric value defining the aggregation period (e.g., 10, 30).
*   `SEC | MIN | HOUR`: The time unit for the interval.
*   `EXTENSION`: Optional keyword to enable `FIRST()` and `LAST()` aggregate functions.

**Constraints:**

*   The source must be a TAG table or another Rollup table.
*   If the source is a Rollup table, the new `INTERVAL` must be a multiple of the source Rollup table's interval and represent a coarser granularity.

**Examples:**

Create a 30-second Rollup based on the 'tag_data' table's 'value' column:

```sql
CREATE ROLLUP _tag_data_rollup_30sec ON tag_data(value) INTERVAL 30 SEC;
```

Create a 10-minute Rollup based on the previously created 30-second Rollup:

```sql
CREATE ROLLUP _tag_data_rollup_10min ON _tag_data_rollup_30sec INTERVAL 10 MIN;
```

Create a 15-minute Rollup with FIRST/LAST support:

```sql
CREATE ROLLUP _tag_data_rollup_15min_ext ON tag_data(value) INTERVAL 15 MIN EXTENSION;
```

## Rollup vs Regular Aggregation

When a TAG table has Rollup tables (created via `WITH ROLLUP` or `CREATE ROLLUP`), you must use the `ROLLUP()` function to leverage pre-aggregated data. Using regular SQL aggregation functions without `ROLLUP()` will scan all raw data, resulting in significantly slower performance.

### Performance Comparison

Assuming a TAG table with millions of rows and WITH ROLLUP enabled:

SLOW — Regular aggregation scans all raw data (scans millions of raw records):

```sql
SELECT
    DATE_TRUNC('hour', time) as hour_time,
    AVG(value) as avg_value
FROM sensor_data
WHERE name = 'SENSOR_A'
  AND time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-12-31')
GROUP BY DATE_TRUNC('hour', time)
ORDER BY hour_time;
```

FAST — ROLLUP() function uses pre-aggregated data (100x+ faster):

```sql
SELECT
    ROLLUP('hour', 1, time) AS hour_time,
    AVG(value) AS avg_value
FROM sensor_data
WHERE name = 'SENSOR_A'
  AND time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-12-31')
GROUP BY hour_time
ORDER BY hour_time;
```

### Key Rules

1. **If Rollup tables exist, always use `ROLLUP()` function** for time-based aggregations
2. Regular `GROUP BY` aggregation should only be used when:
   - No Rollup tables exist for the TAG table
   - You need aggregations not supported by Rollup (e.g., STDDEV, PERCENTILE)
   - You need non-time-based grouping

## Querying Rollup Data

To leverage the performance benefits of pre-aggregated data, queries must utilize the `ROLLUP()` function (or the deprecated `ROLLUP` keyword syntax). Machbase automatically selects the most appropriate Rollup table based on the requested interval and granularity.

**Syntax (Recommended):**

```sql
SELECT
    ROLLUP( time_unit, period, basetime_column [, origin ] ) AS rollup_time,
    AGGREGATE_FUNCTION( value_column ) AS aggregate_result
    [, other_aggregates... ]
FROM
    source_tag_table
WHERE
    [ time_range_predicate ]
    [ AND name_predicate ]
    [ AND other_predicates... ]
GROUP BY
    rollup_time -- Or GROUP BY ROLLUP(...) expression directly
ORDER BY
    rollup_time;
```

*   `time_unit`: The desired unit for the aggregation interval ('sec', 'min', 'hour', 'day', 'week', 'month', 'year', etc.).
*   `period`: The numeric value of the aggregation interval relative to the `time_unit`. Must be a valid multiple of the underlying Rollup table's interval.
*   `basetime_column`: The DATETIME column designated with the `BASETIME` attribute in the TAG table.
*   `origin`: (Optional) A DATETIME literal specifying the alignment anchor for time bins. Defaults to '1970-01-01 00:00:00'. Crucial for week/month/year alignment.
*   `AGGREGATE_FUNCTION`: One of the supported functions (MIN, MAX, AVG, SUM, COUNT, SUMSQ, or FIRST/LAST if `EXTENSION` was used).

**Important Considerations:**

*   The query must include a `GROUP BY` clause referencing the `ROLLUP()` expression (or its alias).
*   Only the supported aggregate functions can be applied to the value column when using the `ROLLUP()` mechanism.

**Query Examples:**

Hourly MIN and MAX values for TAG_00001 within a specific month:

```sql
SELECT
    ROLLUP('hour', 1, time) as mtime,
    MIN(value),
    MAX(value)
FROM TAG
WHERE name = 'TAG_00001'
  AND time BETWEEN TO_DATE('2023-01-01 00:00:00') AND TO_DATE('2023-01-31 23:59:59')
GROUP BY mtime
ORDER BY mtime;
```

15-minute average values, assuming a MIN or SEC level Rollup exists:

```sql
SELECT
    ROLLUP('min', 15, time) AS rollup_interval,
    AVG(value)
FROM TAG
WHERE name = 'SENSOR_A'
GROUP BY rollup_interval
ORDER BY rollup_interval;
```

Daily FIRST and LAST values using Extension Rollup, aligning bins to Jan 1st, 2024:

```sql
SELECT
    ROLLUP('day', 1, time, '2024-01-01') as day_interval,
    FIRST(time, value),
    LAST(time, value)
FROM TAG_WITH_EXTENSION
WHERE name = 'SENSOR_B'
GROUP BY day_interval
ORDER BY day_interval;
```

Weekly average, aligned to Mondays (assuming '2024-01-01' was a Monday):

```sql
SELECT
    ROLLUP('week', 1, time, '2024-01-01') AS week_start,
    AVG(value)
FROM TAG
WHERE name = 'SENSOR_C'
GROUP BY week_start
ORDER BY week_start;
```

## Managing Rollup Tables

### Lifecycle Control

The aggregation process performed by Rollup threads can be manually controlled.

**Commands:**

Start the aggregation thread for a specific Rollup:

```sql
EXEC ROLLUP_START('rollup_name');
```

Stop the aggregation thread for a specific Rollup:

```sql
EXEC ROLLUP_STOP('rollup_name');
```

Force immediate aggregation processing for a specific Rollup, bypassing the normal interval wait time:

```sql
EXEC ROLLUP_FORCE('rollup_name');
```

**Examples:**

```sql
EXEC ROLLUP_START('_tag_data_rollup_30sec');
```

```sql
EXEC ROLLUP_STOP('_tag_data_rollup_10min');
```

Process pending data for the hourly rollup now:

```sql
EXEC ROLLUP_FORCE('_tag_rollup_hour');
```

### Rollup Data Deletion

Deleting data from the source TAG table does **not** automatically remove the corresponding aggregated data from Rollup tables. Rollup data must be explicitly deleted.

**Syntax:**

Delete all Rollup data for the specified table:

```sql
DELETE FROM table_name ROLLUP;
```

Delete Rollup data before a specific timestamp for the specified table:

```sql
DELETE FROM table_name ROLLUP BEFORE TO_DATE('YYYY-MM-DD HH24:MI:SS');
```

Delete all Rollup data for a specific tag within the table:

```sql
DELETE FROM table_name ROLLUP WHERE name = 'specific_tag_id';
```

Delete Rollup data for a specific tag before a specific timestamp:

```sql
DELETE FROM table_name ROLLUP WHERE name = 'specific_tag_id' AND time <= TO_DATE('YYYY-MM-DD HH24:MI:SS');
``` 

**Examples:**

Remove all Rollup data associated with the 'TAG' table older than Jan 15, 2024:

```sql
DELETE FROM TAG ROLLUP BEFORE TO_DATE('2024-01-15 00:00:00');
```

Remove all Rollup data for 'TAG01' from the 'TAG' table:

```sql
DELETE FROM TAG ROLLUP WHERE name = 'TAG01';
```

### Rollup Table Deletion

Custom Rollup tables can be dropped individually. Default Rollup tables are typically removed when the parent TAG table is dropped.

**Syntax:**

Drop a specific Custom Rollup table:

```sql
DROP ROLLUP rollup_name;
```

Drop a TAG table and all its dependent Rollup tables (Default and Custom):

```sql
DROP TABLE tag_table_name CASCADE;
```

**Constraint:** A Rollup table cannot be dropped if another Rollup table depends on it. Dependent Rollups must be dropped first (in reverse order of creation).

**Example:**

Assuming _rollup_min depends on _rollup_sec, drop in reverse order:

```sql
DROP ROLLUP _rollup_min;
```

```sql
DROP ROLLUP _rollup_sec;
```

Drop the 'sensor_data' TAG table and all associated Rollups:

```sql
DROP TABLE sensor_data CASCADE;
```

## Rollup Gap

The **Rollup Gap** refers to the time difference between the latest data inserted into the source TAG table and the latest data processed and reflected in the Rollup tables. Due to the periodic nature of aggregation, a small gap is expected. However, significant or growing gaps can indicate performance bottlenecks.

### Checking Rollup Gap

The current status of Rollup processing, including any existing gaps, can be inspected.

**Command:**

```sql
SHOW ROLLUPGAP;
```

This command displays information about each active Rollup process, including the count of pending data points contributing to the gap. A `GAP` count of 0 indicates that the Rollup is up-to-date.

### Mitigating Rollup Gap

If a significant gap develops, the following actions can be considered:

1.  **Force Aggregation:** Use `EXEC ROLLUP_FORCE('rollup_name');` to trigger immediate processing of pending data for a specific Rollup.
2.  **Increase Parallelism:** Increase the `TAG_PARTITION_COUNT` property of the source TAG table. This allows more Rollup threads to potentially operate in parallel but increases memory consumption.
3.  **Hardware Resources:** Enhance server resources, particularly CPU speed/cores and disk I/O performance.
4.  **Ingestion Rate Management:** If the data ingestion rate consistently exceeds the system's processing capacity, consider strategies to moderate the input flow or scale the hardware further.

Persistent gaps often signify that the system resources are insufficient to handle the combined load of data ingestion and Rollup aggregation.

## Limitations

While powerful, the Machbase Rollup feature has certain limitations:

*   **Fixed Aggregate Functions:** Only the built-in aggregate functions (MIN, MAX, AVG, SUM, COUNT, SUMSQ, optionally FIRST/LAST) are supported. Custom aggregation logic requires alternative approaches.
*   **Source Data Integrity:** Erroneous or outlier data ingested into the source TAG table will be reflected in the Rollup aggregates. Data quality measures should be applied prior to or during ingestion.
*   **Resource Consumption:** The Rollup process consumes CPU and I/O resources to read from the source and write to the Rollup tables. Under high ingestion loads, this can lead to resource contention and potentially growing Rollup Gaps if resources are inadequate.
*   **Latency:** There is inherent latency between data arrival in the TAG table and its reflection in Rollup tables, corresponding to the aggregation interval and processing time (the Rollup Gap). Near real-time queries requiring microsecond precision on aggregates might need to query the raw TAG data directly.

## Rollup Examples

This section provides practical examples illustrating the creation, management, and querying of Machbase Rollup tables.

### Example 1: Default Rollup Creation and Query

This example demonstrates creating a TAG table with default Rollup tables (SEC, MIN, HOUR) and querying hourly aggregates.

**Step 1.** Create a TAG table with default Rollups enabled (creates _iot_sensors_ROLLUP_SEC, _iot_sensors_ROLLUP_MIN, _iot_sensors_ROLLUP_HOUR):

```sql
CREATE TAG TABLE iot_sensors (
    sensor_id VARCHAR(50) PRIMARY KEY,
    event_time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED
) WITH ROLLUP;
```

**Step 2.** Insert sample data:

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 10:05:15', 20.1);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 10:15:30', 20.5);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 10:55:00', 21.0);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 11:05:00', 21.5);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 11:35:45', 21.8);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_B', '2024-03-10 10:10:00', 15.0);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_B', '2024-03-10 11:10:00', 16.0);
```

**Step 3.** Query the average hourly temperature for sensor TEMP_A:

```sql
SELECT
    ROLLUP('hour', 1, event_time) AS hour_interval,
    AVG(temperature) AS avg_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time BETWEEN TO_DATE('2024-03-10 10:00:00') AND TO_DATE('2024-03-10 12:00:00')
GROUP BY
    hour_interval
ORDER BY
    hour_interval;
```

Expected approximate output:

```text
hour_interval                   avg_temp
---------------------------------------------------------------
2024-03-10 10:00:00 000:000:000 20.533...  -- Avg of 20.1, 20.5, 21.0
2024-03-10 11:00:00 000:000:000 21.65      -- Avg of 21.5, 21.8
```

### Example 2: Custom Rollup Creation and Query

This example creates a custom Rollup table aggregating data every 15 minutes.

Prerequisite: Assume iot_sensors table exists from Example 1.

**Step 1.** Create a custom 15-minute Rollup table based on the 'temperature' column:

```sql
CREATE ROLLUP _iot_sensors_rollup_15min
ON iot_sensors (temperature)
INTERVAL 15 MIN;
```

**Step 2.** Query MIN and MAX temperature aggregated over 15-minute intervals for TEMP_A:

```sql
SELECT
    ROLLUP('min', 15, event_time) AS interval_15min,
    MIN(temperature) AS min_temp,
    MAX(temperature) AS max_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time BETWEEN TO_DATE('2024-03-10 10:00:00') AND TO_DATE('2024-03-10 12:00:00')
GROUP BY
    interval_15min
ORDER BY
    interval_15min;
```

Expected approximate output:

```text
interval_15min                  min_temp    max_temp
---------------------------------------------------------------
2024-03-10 10:00:00 000:000:000 20.1        20.1        -- 10:00 to 10:14:59
2024-03-10 10:15:00 000:000:000 20.5        20.5        -- 10:15 to 10:29:59
2024-03-10 10:45:00 000:000:000 21.0        21.0        -- 10:45 to 10:59:59 (data at 10:55)
2024-03-10 11:00:00 000:000:000 21.5        21.5        -- 11:00 to 11:14:59
2024-03-10 11:30:00 000:000:000 21.8        21.8        -- 11:30 to 11:44:59
```

### Example 3: Extended Rollup Query (FIRST/LAST)

This example demonstrates querying the first and last values within an interval using an Extended Rollup.

**Step 1.** Create a TAG table with default Rollups and EXTENSION (enable FIRST() and LAST()):

```sql
DROP TABLE IF EXISTS iot_sensors_ext CASCADE;
```

```sql
CREATE TAG TABLE iot_sensors_ext (
    sensor_id VARCHAR(50) PRIMARY KEY,
    event_time DATETIME BASETIME,
    pressure DOUBLE SUMMARIZED
) WITH ROLLUP EXTENSION;
```

**Step 2.** Insert sample data:

```sql
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 09:01:00', 1000.1);
```

```sql
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 09:05:00', 1000.5);
```

```sql
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 09:55:00', 1001.0);
```

```sql
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 10:02:00', 1001.2);
```

```sql
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 10:08:00', 1001.5);
```

```sql
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 10:40:00', 1001.8);
```

**Step 3.** Query the first and last pressure readings per hour for PRES_1:

```sql
SELECT
    ROLLUP('hour', 1, event_time) AS hour_interval,
    FIRST(event_time, pressure) AS first_pressure,
    LAST(event_time, pressure) AS last_pressure
FROM
    iot_sensors_ext
WHERE
    sensor_id = 'PRES_1'
GROUP BY
    hour_interval
ORDER BY
    hour_interval;
```

Expected approximate output:

```text
hour_interval                   first_pressure last_pressure
----------------------------------------------------------------------
2024-03-10 09:00:00 000:000:000 1000.5         1001.0
2024-03-10 10:00:00 000:000:000 1001.2         1001.8
```

### Example 4: Querying Different Granularities (Daily/Weekly)

This example uses the `iot_sensors` table (assuming it has data spanning multiple days/weeks) to query daily and weekly averages.

Assume 'iot_sensors' table has data for TEMP_A from 2024-03-01 to 2024-03-15.

**Query 1.** Daily Average Temperature for TEMP_A:

```sql
SELECT
    ROLLUP('day', 1, event_time) AS day_interval,
    AVG(temperature) AS avg_daily_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-03-01') AND event_time < TO_DATE('2024-03-16')
GROUP BY
    day_interval
ORDER BY
    day_interval;
```

**Query 2.** Weekly Average Temperature for TEMP_A, aligning weeks starting on Monday ('2024-03-04'):

```sql
SELECT
    ROLLUP('week', 1, event_time, '2024-03-04') AS week_start_monday,
    AVG(temperature) AS avg_weekly_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-03-01') AND event_time < TO_DATE('2024-03-16')
GROUP BY
    week_start_monday
ORDER BY
    week_start_monday;
```


### Example 5: Monthly Rollup Queries

This example demonstrates how to aggregate data on a monthly basis using the Rollup feature. This typically relies on the underlying HOUR-level Rollup table for efficient computation.

Assume the 'iot_sensors' table (from Example 1) has data spanning several months (January 2024 to April 2024 for sensor 'TEMP_A'). Insert additional example data:

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-01-15 12:00:00', 18.0);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-01-25 14:00:00', 18.5);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-02-10 08:00:00', 19.0);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-02-20 09:00:00', 19.2);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-05 10:00:00', 19.5);
```

```sql
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-20 11:00:00', 20.0);
```

**Query 1.** Average Monthly Temperature for TEMP_A (the origin defaults to '1970-01-01', which works for standard calendar months):

```sql
SELECT
    ROLLUP('month', 1, event_time) AS month_interval,
    AVG(temperature) AS avg_monthly_temp,
    COUNT(temperature) AS data_points_per_month
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-01-01') AND event_time < TO_DATE('2024-04-01')
GROUP BY
    month_interval
ORDER BY
    month_interval;
```

Expected approximate output:

```text
month_interval                  avg_monthly_temp data_points_per_month
--------------------------------------------------------------------------
2024-01-01 00:00:00 000:000:000 18.25            2
2024-02-01 00:00:00 000:000:000 19.1             2
2024-03-01 00:00:00 000:000:000 20.55            8
```

**Query 2.** Quarterly (3-Month) SUM and COUNT for TEMP_A (using period=3 with 'month' unit):

```sql
SELECT
    ROLLUP('month', 3, event_time) AS quarter_interval,
    SUM(temperature) AS sum_quarterly_temp,
    COUNT(temperature) AS data_points_per_quarter
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-01-01') AND event_time < TO_DATE('2024-04-01')
GROUP BY
    quarter_interval
ORDER BY
    quarter_interval;
```

Expected approximate output:

```text
quarter_interval                sum_quarterly_temp data_points_per_quarter
----------------------------------------------------------------------------
2024-01-01 00:00:00 000:000:000 241.1              12
```

**Query 3.** Explicitly setting Origin (if setting origin for 'month', it MUST be the first day of some month):

```sql
SELECT
    ROLLUP('month', 1, event_time, '2024-01-01') AS month_interval,
    MIN(temperature) AS min_monthly_temp,
    MAX(temperature) AS max_monthly_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-01-01') AND event_time < TO_DATE('2024-04-01')
GROUP BY
    month_interval
ORDER BY
    month_interval;
```

Expected approximate output:

```text
month_interval                  min_monthly_temp max_monthly_temp
--------------------------------------------------------------------
2024-01-01 00:00:00 000:000:000 18.0             18.5
2024-02-01 00:00:00 000:000:000 19.0             19.2
2024-03-01 00:00:00 000:000:000 19.5             21.8
```

### Example 6: Rollup Management Commands

This example shows how to check the status, force processing, delete old Rollup data, and drop tables with Rollups.

**Step 1.** Check the current Rollup gap status for all Rollups:

```sql
SHOW ROLLUPGAP;
```

**Step 2.** Force immediate processing for a specific custom Rollup:

```sql
EXEC ROLLUP_FORCE('_iot_sensors_rollup_15min');
```

**Step 3.** Delete Rollup data older than March 1st, 2024 from the iot_sensors table's Rollups:

```sql
DELETE FROM iot_sensors ROLLUP BEFORE TO_DATE('2024-03-01 00:00:00');
```

**Step 4.** Drop the iot_sensors_ext table and all its associated Rollup tables:

```sql
DROP TABLE iot_sensors_ext CASCADE;
```