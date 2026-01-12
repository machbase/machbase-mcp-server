# Automatic Duplicate Removal

## Overview

Machbase can automatically detect and remove duplicate sensor readings within a configurable time window, ensuring data quality without manual intervention.

## Configuring Duplicate Removal

When creating the TAG table, the duration for duplicate removal is passed as a table property. The maximum configurable duration for duplicate removal is 43200 minutes (30 days).

```sql
-- If the newly inserted data duplicates existing data within 1440 minutes(one day) from system time those data will be deleted.

CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) TAG_DUPLICATE_CHECK_DURATION=1440;
```

The property of the duplication removal is shown in the table m$sys_table_property.
```sql
SELECT * FROM m$sys_table_property WHERE id={table_id} AND name = 'TAG_DUPLICATE_CHECK_DURATION';
```

Data insert/select example - duplication removal duration is 1440 minutes(one day)
```sql
-- Total inserted data are 6 and 4 of them are duplicates but 1 duplicated record was inserted 1440 minutes(one day) before
-- system time(1970-01-03 09:00:00 000:000:003).
-- Newly inserted duplicated data within the configured duration 1440 minutes(one day) are not displayed.

INSERT INTO tag VALUES('tag1', '1970-01-01 09:00:00 000:000:001', 0);
INSERT INTO tag VALUES('tag1', '1970-01-02 09:00:00 000:000:001', 0);
INSERT INTO tag VALUES('tag1', '1970-01-02 09:00:00 000:000:002', 0);
INSERT INTO tag VALUES('tag1', '1970-01-02 09:00:00 000:000:002', 1);
INSERT INTO tag VALUES('tag1', '1970-01-03 09:00:00 000:000:003', 0);
INSERT INTO tag VALUES('tag1', '1970-01-01 09:00:00 000:000:001', 0);

SELECT * FROM tag WHERE name = 'tag1';
NAME                  TIME                            VALUE                       
--------------------------------------------------------------------------------------
tag1                  1970-01-01 09:00:00 000:000:001 0
tag1                  1970-01-02 09:00:00 000:000:001 0                           
tag1                  1970-01-02 09:00:00 000:000:002 0
tag1                  1970-01-03 09:00:00 000:000:003 0      
tag1                  1970-01-01 09:00:00 000:000:001 0
  
```
## Changing configuration
TAG_DUPLICATE_CHECK_DURATION can be modified as shown below.

```sql
ALTER TABLE {table_name} set TAG_DUPLICATE_CHECK_DURATION={duration in minutes};
```

## Constraints of duplication removal

* The duplication removal setting can be configured on a minute basis, with a maximum limit of 43200 minutes (30 days).
* If the existing input data has already been deleted, any subsequent occurrence of the same data will not be considered as a duplicate for the purpose of duplication removal.

## Checking duplicates via TRACE log
Adding 32(SM_2) to TRACE_LOG_LEVEL outputs deduplication logs.
```sql
-- Check current setting
select name, value from v$property where name = 'TRACE_LOG_LEVEL';

-- Change setting
alter system set TRACE_LOG_LEVEL={current_value + 32};
```

**Configuration Example**
```sql
-- Check current value
Mach> select name, value from v$property where name = 'TRACE_LOG_LEVEL';
name                                                          value
---------------------------------------------------------------------------------------------------------------------------------------------------
TRACE_LOG_LEVEL                                               277
[1] row(s) selected.

-- Add 32 (277 + 32 = 309)
Mach> alter system set TRACE_LOG_LEVEL=309;
Altered successfully.
```

- Log file location: `$MACHBASE_HOME/trc/machbase.trc`
- Quick filter:
  ```bash
  tail -n 50 $MACHBASE_HOME/trc/machbase.trc | grep DUP_DROP
  ```
- Log format: `DUP_DROP Table=<table> TAG=<tag id> TIME=<timestamp> COL<n>=<value> ...`
- Real sample (same TIME for TAG=1, different COL3 values):
  ```
  [2025-11-29 13:50:27 P-151395 T-126344581076672][SM-INFO] DUP_DROP Table=TAG TAG=1 TIME=1998-12-24 09:00:00 000:000:012  COL3=12.000000
  ...
  [2025-11-29 13:50:27 P-151395 T-126344581076672][SM-INFO] DUP_DROP Table=TAG TAG=1 TIME=1998-12-24 09:00:00 000:000:048  COL3=48.000000
  ```
- How to use it
  - Check the TIME field to see which duplicates were dropped at the same timestamp.
  - Add `grep "Table=TAG"` or `grep "TAG=1"` for faster narrowing to a specific table/tag.
- Note: Each line is capped at ~4KB; with very many columns the tail may be truncated, but it won’t crash.